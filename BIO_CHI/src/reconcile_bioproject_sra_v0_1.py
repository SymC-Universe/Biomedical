#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, io, json, pathlib, time, urllib.error, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"P0D_BIOPROJECT_SRA_RECONCILIATION_FREEZE_v0_1.json"
OUT=BIO/"artifacts"/"generated"
OUT.mkdir(parents=True,exist_ok=True)
OUT_FILE=OUT/"bioproject_sra_reconciliation_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
    last = None
    for attempt in range(6):
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        try:
            with urllib.request.urlopen(req,timeout=180) as r:
                data = r.read()
            time.sleep(0.4)
            return data
        except urllib.error.HTTPError as exc:
            last = exc
            if exc.code != 429 or attempt == 5:
                raise
            retry_after = exc.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else min(16.0, 1.0 * (2 ** attempt))
            time.sleep(delay)
    raise last

def sha256(b): return hashlib.sha256(b).hexdigest()

def search(term):
    q=urllib.parse.urlencode({"db":"sra","term":term,"retmax":100000,"retmode":"json","tool":"BioChiSourceQualification"})
    raw=fetch("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"+q)
    return json.loads(raw.decode("utf-8"))

def runinfo(ids):
    q=urllib.parse.urlencode({"db":"sra","id":",".join(ids),"rettype":"runinfo","retmode":"text","tool":"BioChiSourceQualification"})
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"+q
    raw=fetch(url)
    return raw,url

def uniq(rows,key):
    return sorted({(r.get(key) or "").strip() for r in rows if (r.get(key) or "").strip()})

def main():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    audits=[]
    failures=[]
    for p in cfg["projects"]:
        sr=search(p["bioproject"])
        ids=sr.get("esearchresult",{}).get("idlist",[])
        if not ids:
            failures.append(p["bioproject"]+": no SRA records")
            audits.append({**p,"status":"NO_SRA_RECORDS"})
            continue
        raw,url=runinfo(ids)
        rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig",errors="replace"))))
        if not rows:
            failures.append(p["bioproject"]+": empty RunInfo")
            audits.append({**p,"status":"EMPTY_RUNINFO"})
            continue
        projects=uniq(rows,"BioProject")
        if p["bioproject"] not in projects:
            failures.append(p["bioproject"]+": BioProject mismatch "+repr(projects))
        audits.append({
            **p,
            "status":"PASS",
            "runinfo_url":url,
            "runinfo_sha256":sha256(raw),
            "runinfo_size_bytes":len(raw),
            "run_count":len(rows),
            "runs":uniq(rows,"Run"),
            "sra_studies":uniq(rows,"SRAStudy"),
            "experiments":uniq(rows,"Experiment"),
            "samples":uniq(rows,"Sample"),
            "biosamples":uniq(rows,"BioSample"),
            "library_strategy_counts":dict(Counter((r.get("LibraryStrategy") or "").strip() for r in rows)),
            "library_layout_counts":dict(Counter((r.get("LibraryLayout") or "").strip() for r in rows)),
            "platform_counts":dict(Counter((r.get("Platform") or "").strip() for r in rows)),
            "sequence_reads_downloaded":False,
            "molecular_values_interpreted":False
        })
    result={
      "schema_version":"0.1",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],
      "audits":audits,
      "failures":failures,
      "sequence_reads_downloaded":False,
      "molecular_values_interpreted":False,
      "status":"PASS_BIOPROJECT_SRA_RECONCILIATION" if not failures else "FAIL_SOURCE_RECONCILIATION"
    }
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "output":str(OUT_FILE.relative_to(ROOT)),
      "status":result["status"],
      "audits":[{"id":a.get("id"),"bioproject":a.get("bioproject"),"run_count":a.get("run_count"),"sra_studies":a.get("sra_studies")} for a in audits],
      "failures":failures
    },indent=2))
    if failures: raise SystemExit("BIO_CHI_BIOPROJECT_SRA_RECONCILIATION_FAIL")
    print("BIO_CHI_BIOPROJECT_SRA_RECONCILIATION_PASS")

if __name__=="__main__": main()
