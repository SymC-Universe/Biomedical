#!/usr/bin/env python3
# workflow trigger after registration
"""Source-only qualification for GEO GSE342354.

This script enumerates NCBI GEO source files, hashes bounded processed objects,
and verifies frozen sample identities. It does not parse expression values or
compute any biological outcome.
"""
from __future__ import annotations
import gzip, hashlib, json, re
from pathlib import Path
from urllib.parse import urljoin, unquote
import requests

ACC="GSE342354"
ROOT="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE342nnn/GSE342354/"
DIRS={"suppl":"suppl/","matrix":"matrix/","soft":"soft/"}
FROZEN=[
"GSM9929032","GSM9929033","GSM9929034",
"GSM9929035","GSM9929036","GSM9929037",
"GSM9929038","GSM9929039","GSM9929040",
"GSM9929041","GSM9929042","GSM9929043",
]
OUT=Path(__file__).resolve().parent/"gse342354_source_qualification"
RAW=OUT/"downloaded_sources"
OUT.mkdir(parents=True,exist_ok=True); RAW.mkdir(parents=True,exist_ok=True)
MAX_FILE=200*1024*1024
MAX_TOTAL=600*1024*1024
UA={"User-Agent":"SymC-BioChi-source-qualification/0.1 (GEO GSE342354)"}

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def list_dir(url):
    r=requests.get(url,headers=UA,timeout=90)
    r.raise_for_status()
    hrefs=re.findall(r'href=["\']([^"\']+)["\']',r.text,re.I)
    out=[]
    for h in hrefs:
        h=unquote(h)
        if h in ("../","./") or h.startswith("?") or h.startswith("/"): continue
        if h.endswith("/"): continue
        out.append(h)
    return sorted(set(out)), r.text

def head_meta(url):
    r=requests.head(url,headers=UA,timeout=60,allow_redirects=True)
    if r.status_code>=400:
        r=requests.get(url,headers={**UA,"Range":"bytes=0-0"},timeout=60,allow_redirects=True,stream=True)
    size=r.headers.get("content-length")
    return {"status":r.status_code,"content_length":int(size) if size and size.isdigit() else None,
            "content_type":r.headers.get("content-type"),"last_modified":r.headers.get("last-modified"),
            "etag":r.headers.get("etag")}

def likely_processed(group,name):
    low=name.lower()
    if group=="matrix": return True
    if group=="soft": return True
    if group=="suppl":
        if low.endswith(".tar") or "_raw.tar" in low: return False
        return low.endswith((".txt",".txt.gz",".tsv",".tsv.gz",".csv",".csv.gz",".xlsx",".xls",".gz"))
    return False

def textual_identity_scan(p):
    name=p.name.lower()
    data=None
    try:
        if name.endswith(".gz"):
            with gzip.open(p,"rt",encoding="utf-8",errors="ignore") as f:
                data=f.read(25_000_000)
        elif name.endswith((".txt",".csv",".tsv",".soft")):
            data=p.read_text(encoding="utf-8",errors="ignore")[:25_000_000]
    except Exception:
        data=None
    if data is None: return {}
    return {g:(g in data) for g in FROZEN}

def main():
    manifest=[]; listings={}; downloaded=[]; total=0
    for group,rel in DIRS.items():
        url=urljoin(ROOT,rel)
        names,html=list_dir(url)
        listings[group]={"url":url,"files":names}
        for name in names:
            furl=urljoin(url,name)
            meta=head_meta(furl)
            rec={"group":group,"name":name,"url":furl,**meta,"likely_processed":likely_processed(group,name)}
            size=meta["content_length"]
            if rec["likely_processed"] and size is not None and size<=MAX_FILE and total+size<=MAX_TOTAL:
                p=RAW/(group+"__"+name.replace("/","__"))
                rr=requests.get(furl,headers=UA,timeout=180,stream=True)
                rr.raise_for_status()
                with open(p,"wb") as f:
                    for chunk in rr.iter_content(1<<20):
                        if chunk: f.write(chunk)
                rec["downloaded"]=True
                rec["sha256"]=sha256(p)
                rec["downloaded_bytes"]=p.stat().st_size
                rec["identity_scan"]=textual_identity_scan(p)
                total += p.stat().st_size
                downloaded.append(p)
            else:
                rec["downloaded"]=False
                if rec["likely_processed"] and size is None: rec["skip_reason"]="unknown_size"
                elif rec["likely_processed"] and size>MAX_FILE: rec["skip_reason"]="per_file_size_cap"
                elif rec["likely_processed"] and size is not None and total+size>MAX_TOTAL: rec["skip_reason"]="total_size_cap"
                else: rec["skip_reason"]="not_selected_processed_source"
            manifest.append(rec)

    # Frozen GSM presence may be established by filename, directory page, or metadata text in downloaded objects.
    evidence={g:[] for g in FROZEN}
    for group,listing in listings.items():
        corpus="\n".join(listing["files"])
        for g in FROZEN:
            if g in corpus: evidence[g].append(f"{group}_filename_listing")
    for rec in manifest:
        for g,present in rec.get("identity_scan",{}).items():
            if present: evidence[g].append(f"{rec['group']}:{rec['name']}")
    all_present=all(bool(v) for v in evidence.values())

    processed=[r for r in manifest if r["likely_processed"]]
    hashed=[r for r in processed if r.get("downloaded")]
    result={
      "schema_version":"0.1",
      "experiment_id":"GSE342354_U2OS_CCCP_RECOVERY_SOURCE_QUALIFICATION_V01",
      "status":"SOURCE_QUALIFIED" if all_present and len(hashed)>0 else "SOURCE_QUALIFICATION_INCOMPLETE",
      "geo_accession":ACC,
      "root":ROOT,
      "frozen_gsm_identity_evidence":evidence,
      "all_12_frozen_gsm_ids_resolved":all_present,
      "processed_candidate_count":len(processed),
      "hashed_processed_object_count":len(hashed),
      "downloaded_total_bytes":total,
      "analysis_values_opened":False,
      "next_gate":"freeze processed-expression analysis contract before parsing expression values" if all_present and len(hashed)>0 else "investigate source identity/processed-file availability before biological analysis"
    }
    (OUT/"GSE342354_SOURCE_MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
    (OUT/"GSE342354_DIRECTORY_LISTINGS.json").write_text(json.dumps(listings,indent=2)+"\n")
    (OUT/"GSE342354_SAMPLE_IDENTITY_EVIDENCE.json").write_text(json.dumps(evidence,indent=2)+"\n")
    (OUT/"GSE342354_SOURCE_QUALIFICATION_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
