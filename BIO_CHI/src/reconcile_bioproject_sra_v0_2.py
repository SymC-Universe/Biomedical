#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, io, json, pathlib, time, urllib.error, urllib.parse, urllib.request
from collections import Counter
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"P0D_BIOPROJECT_SRA_RECONCILIATION_FREEZE_v0_2.json"
OUT=BIO/"artifacts"/"generated"
OUT.mkdir(parents=True,exist_ok=True)
OUT_FILE=OUT/"bioproject_sra_reconciliation_v0_2.json"
UA="BioChiReviewerReproducibility/0.2"

def fetch(url):
    last=None
    for attempt in range(7):
        req=urllib.request.Request(url,headers={"User-Agent":UA})
        try:
            with urllib.request.urlopen(req,timeout=180) as r: data=r.read()
            time.sleep(0.5)
            return data
        except urllib.error.HTTPError as exc:
            last=exc
            if exc.code!=429 or attempt==6: raise
            ra=exc.headers.get("Retry-After")
            delay=float(ra) if ra and ra.isdigit() else min(24.0,1.0*(2**attempt))
            time.sleep(delay)
    raise last

def sha256(b): return hashlib.sha256(b).hexdigest()

def search(term):
    q=urllib.parse.urlencode({"db":"sra","term":term,"retmax":100000,"retmode":"json","tool":"BioChiSourceQualification"})
    raw=fetch("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"+q)
    return json.loads(raw.decode("utf-8"))

def runinfo_for_ids(ids):
    q=urllib.parse.urlencode({"db":"sra","id":",".join(ids),"rettype":"runinfo","retmode":"text","tool":"BioChiSourceQualification"})
    url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"+q
    raw=fetch(url)
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig",errors="replace"))))
    return raw,url,rows

def query_bioproject(acc):
    sr=search(acc+"[BioProject]")
    ids=sr.get("esearchresult",{}).get("idlist",[])
    if not ids:
        sr=search(acc)
        ids=sr.get("esearchresult",{}).get("idlist",[])
    if not ids: return {"accession":acc,"ids":[],"rows":[],"error":"NO_RECORDS"}
    raw,url,rows=runinfo_for_ids(ids)
    return {"accession":acc,"ids":ids,"rows":rows,"runinfo_url":url,"runinfo_sha256":sha256(raw),"runinfo_size_bytes":len(raw)}

def vals(rows,key):
    return sorted({(r.get(key) or "").strip() for r in rows if (r.get(key) or "").strip()})

def main():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    audits=[]; failures=[]
    for anchor in cfg["anchors"]:
        parent=query_bioproject(anchor["query_bioproject"])
        rows=parent.get("rows",[])
        if not rows:
            failures.append(anchor["id"]+": parent query returned no rows")
            audits.append({**anchor,"status":"FAIL_NO_PARENT_ROWS"})
            continue
        parent_runs=set(vals(rows,"Run"))
        child_projects=vals(rows,"BioProject")
        child_records=[]
        union=set()
        for cp in child_projects:
            child=query_bioproject(cp)
            crows=child.get("rows",[])
            cruns=set(vals(crows,"Run"))
            child_records.append({
                "bioproject":cp,
                "run_count":len(cruns),
                "runs":sorted(cruns),
                "sra_studies":vals(crows,"SRAStudy"),
                "runinfo_sha256":child.get("runinfo_sha256")
            })
            union |= cruns
        missing=sorted(parent_runs-union)
        extra=sorted(union-parent_runs)
        status="PASS_PARENT_CHILD_RUNSET_RECONCILIATION" if child_projects and not missing and not extra else "FAIL_PARENT_CHILD_RUNSET_RECONCILIATION"
        if status.startswith("FAIL"):
            failures.append(anchor["id"]+f": missing={missing} extra={extra} child_projects={child_projects}")
        audits.append({
            **anchor,
            "status":status,
            "parent_query_run_count":len(parent_runs),
            "parent_query_runs":sorted(parent_runs),
            "parent_query_runinfo_sha256":parent.get("runinfo_sha256"),
            "parent_query_sra_studies":vals(rows,"SRAStudy"),
            "runinfo_bioprojects":child_projects,
            "child_projects":child_records,
            "child_union_run_count":len(union),
            "missing_from_child_union":missing,
            "extra_in_child_union":extra,
            "sequence_reads_downloaded":False,
            "molecular_values_interpreted":False
        })
    result={
      "schema_version":"0.2",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],
      "audits":audits,
      "failures":failures,
      "sequence_reads_downloaded":False,
      "molecular_values_interpreted":False,
      "status":"PASS_BIOPROJECT_PARENT_CHILD_RECONCILIATION" if not failures else "FAIL_BIOPROJECT_PARENT_CHILD_RECONCILIATION"
    }
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "output":str(OUT_FILE.relative_to(ROOT)),
      "status":result["status"],
      "audits":[{
        "id":a["id"],"parent_query":a["query_bioproject"],
        "parent_runs":a.get("parent_query_run_count"),
        "sra_studies":a.get("parent_query_sra_studies"),
        "child_projects":a.get("runinfo_bioprojects"),
        "child_union_runs":a.get("child_union_run_count"),
        "missing":a.get("missing_from_child_union"),"extra":a.get("extra_in_child_union")
      } for a in audits],
      "failures":failures
    },indent=2))
    if failures: raise SystemExit("BIO_CHI_BIOPROJECT_SRA_RECONCILIATION_V02_FAIL")
    print("BIO_CHI_BIOPROJECT_SRA_RECONCILIATION_V02_PASS")

if __name__=="__main__": main()
