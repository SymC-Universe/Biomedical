#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,io,json,pathlib,urllib.parse,urllib.request
from collections import Counter
from datetime import datetime,timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"; CFG=BIO/"config"/"HARMANGE2023_SRA_ROLE_DISCOVERY_FREEZE_v0_4.json"
OUTDIR=BIO/"artifacts"/"generated"; OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"harmange2023_sra_role_discovery_v0_4.json"
UA="BioChiReviewerReproducibility/0.4"

def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA})
 with urllib.request.urlopen(req,timeout=180) as r:
  b=r.read()
  return b,{"resolved_url":r.geturl(),"content_type":r.headers.get("Content-Type"),"content_length":r.headers.get("Content-Length")}

def sha(b):return hashlib.sha256(b).hexdigest()

def try_runinfo(term):
 urls=[
  "https://www.ncbi.nlm.nih.gov/sra/?term="+urllib.parse.quote(term)+"&report=runinfo&format=text",
  "https://trace.ncbi.nlm.nih.gov/Traces/sra-db-be/run_new?acc="+urllib.parse.quote(term)
 ]
 errors=[]
 for u in urls:
  try:
   b,m=fetch(u)
   txt=b.decode("utf-8-sig",errors="replace")
   if "Run," in txt[:2000] or txt.lstrip().startswith("Run,"):
    return b,m,u
   errors.append({"url":u,"preview":txt[:200]})
  except Exception as e:errors.append({"url":u,"error":f"{type(e).__name__}: {e}"})
 raise RuntimeError(json.dumps(errors))

def main():
 cfg=json.loads(CFG.read_text())
 raw,meta,url=try_runinfo(cfg["bioproject"])
 txt=raw.decode("utf-8-sig",errors="replace")
 rd=csv.DictReader(io.StringIO(txt))
 rows=list(rd)
 if not rows:raise SystemExit("empty RunInfo")
 keys=rd.fieldnames or []
 desired=["Run","ReleaseDate","LoadDate","spots","bases","spots_with_mates","avgLength","size_MB","AssemblyName","download_path","Experiment","LibraryName","LibraryStrategy","LibrarySelection","LibrarySource","LibraryLayout","InsertSize","InsertDev","Platform","Model","SRAStudy","BioProject","Study_Pubmed_id","ProjectID","Sample","BioSample","SampleType","TaxID","ScientificName","SampleName","g1k_pop_code","source","g1k_analysis_group","Subject_ID","Sex","Disease","Tumor","Affection_Status","Analyte_Type","Histological_Type","Body_Site","CenterName","Submission","dbgap_study_accession","Consent","RunHash","ReadHash"]
 compact=[]
 keywords=["lineage","barcode","lenti","feature","clone","tracer","memory"]
 hits=[]
 for row in rows:
  rec={k:row.get(k) for k in desired if k in row}
  # preserve all nonempty source-metadata fields not in desired that might identify samples/roles
  extras={k:v for k,v in row.items() if k not in rec and v not in (None,"")}
  rec["extra_fields"]=extras
  compact.append(rec)
  hay=" | ".join(str(v) for v in row.values()).lower()
  kh=[k for k in keywords if k in hay]
  if kh:hits.append({"Run":row.get("Run"),"Experiment":row.get("Experiment"),"Sample":row.get("Sample"),"BioSample":row.get("BioSample"),"LibraryName":row.get("LibraryName"),"keywords":kh,"row":rec})
 result={
  "schema_version":"0.4","generated_at_utc":datetime.now(timezone.utc).isoformat(),
  "status":"PASS_SRA_RUNINFO_AUDIT","runinfo_url":url,"runinfo_sha256":sha(raw),"runinfo_bytes":len(raw),"meta":meta,
  "fieldnames":keys,"run_count":len(rows),"experiment_count":len(set(r.get("Experiment") for r in rows)),
  "sample_count":len(set(r.get("Sample") for r in rows)),"biosample_count":len(set(r.get("BioSample") for r in rows)),
  "library_strategy_counts":dict(Counter(r.get("LibraryStrategy") for r in rows)),
  "library_source_counts":dict(Counter(r.get("LibrarySource") for r in rows)),
  "library_selection_counts":dict(Counter(r.get("LibrarySelection") for r in rows)),
  "runs":compact,"keyword_hits":hits,"sequencing_payload_opened":False
 }
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
 print("BIO_CHI_HARMANGE_SRA_ROLE_DISCOVERY_PASS")
if __name__=="__main__":main()
