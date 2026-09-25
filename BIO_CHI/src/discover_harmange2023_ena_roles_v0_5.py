#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,io,json,pathlib,urllib.parse,urllib.request
from collections import Counter
from datetime import datetime,timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"; CFG=BIO/"config"/"HARMANGE2023_ENA_ROLE_DISCOVERY_FREEZE_v0_5.json"
OUTDIR=BIO/"artifacts"/"generated"; OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"harmange2023_ena_role_discovery_v0_5.json"
UA="BioChiReviewerReproducibility/0.5"

def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/tab-separated-values,text/plain"})
 with urllib.request.urlopen(req,timeout=180) as r:
  b=r.read()
  return b,{"resolved_url":r.geturl(),"content_type":r.headers.get("Content-Type"),"content_length":r.headers.get("Content-Length")}

def sha(b):return hashlib.sha256(b).hexdigest()

def main():
 cfg=json.loads(CFG.read_text())
 fields=",".join(cfg["query_fields"])
 params={
   "accession":cfg["bioproject"],"result":"read_run","fields":fields,
   "format":"tsv","download":"false"
 }
 url="https://www.ebi.ac.uk/ena/portal/api/filereport?"+urllib.parse.urlencode(params)
 raw,meta=fetch(url)
 txt=raw.decode("utf-8-sig",errors="replace")
 rd=csv.DictReader(io.StringIO(txt),delimiter="\t")
 rows=list(rd)
 if not rows:raise SystemExit("ENA returned zero rows")
 keyword_terms=["lineage","barcode","lenti","feature","clone","memory","tracer","scmemory"]
 hits=[]
 for row in rows:
  hay=" | ".join(str(v) for v in row.values()).lower()
  ks=[k for k in keyword_terms if k in hay]
  if ks:hits.append({"keywords":ks,"row":row})
 result={
   "schema_version":"0.5","generated_at_utc":datetime.now(timezone.utc).isoformat(),
   "status":"PASS_ENA_RUN_METADATA_AUDIT","query_url":url,"response_sha256":sha(raw),"response_bytes":len(raw),"meta":meta,
   "fieldnames":rd.fieldnames,"run_count":len(rows),
   "experiment_count":len(set(r.get("experiment_accession") for r in rows)),
   "sample_count":len(set(r.get("sample_accession") for r in rows)),
   "secondary_sample_count":len(set(r.get("secondary_sample_accession") for r in rows)),
   "study_accessions":sorted(set(r.get("study_accession") for r in rows)),
   "secondary_study_accessions":sorted(set(r.get("secondary_study_accession") for r in rows)),
   "library_strategy_counts":dict(Counter(r.get("library_strategy") for r in rows)),
   "library_source_counts":dict(Counter(r.get("library_source") for r in rows)),
   "library_selection_counts":dict(Counter(r.get("library_selection") for r in rows)),
   "runs":rows,"keyword_hits":hits,"sequencing_payload_opened":False
 }
 if len(rows)!=cfg["expected_runs"]:
  result["status"]="PASS_WITH_RUN_COUNT_MISMATCH"
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
 print("BIO_CHI_HARMANGE_ENA_ROLE_DISCOVERY_DONE")
if __name__=="__main__":main()
