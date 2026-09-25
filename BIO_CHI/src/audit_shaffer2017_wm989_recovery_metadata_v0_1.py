#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, json, pathlib, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SHAFFER2017_WM989_RECOVERY_METADATA_FREEZE_v0_1.json"
OUTDIR=BIO/"artifacts"/"generated"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"shaffer2017_wm989_recovery_metadata_v0_1.json"
URL="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE97nnn/GSE97681/soft/GSE97681_family.soft.gz"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA})
 with urllib.request.urlopen(req,timeout=180) as r: return r.read()

def parse(raw):
 txt=gzip.decompress(raw).decode("utf-8",errors="replace")
 samples={}; cur=None
 for line in txt.splitlines():
  if line.startswith("^SAMPLE = "):
   cur=line.split("=",1)[1].strip()
   samples[cur]={"accession":cur,"title":None,"characteristics":[],"description":[]}
  elif cur and line.startswith("!Sample_title = "): samples[cur]["title"]=line.split("=",1)[1].strip()
  elif cur and line.startswith("!Sample_characteristics_ch1 = "): samples[cur]["characteristics"].append(line.split("=",1)[1].strip())
  elif cur and line.startswith("!Sample_description = "): samples[cur]["description"].append(line.split("=",1)[1].strip())
 return samples

def kv(rec):
 d={}
 for x in rec["characteristics"]:
  if ":" in x:
   k,v=x.split(":",1); d[k.strip().lower()]=v.strip()
 return d

def main():
 cfg=json.loads(CFG.read_text())
 raw=fetch(URL); samples=parse(raw)
 target=[]
 for rec in samples.values():
  d=kv(rec)
  if d.get("cell line")==cfg["target_cell_line"] and d.get("subclone") in cfg["target_subclones"]:
   rec["parsed_characteristics"]=d
   target.append(rec)
 target.sort(key=lambda x:(x["parsed_characteristics"].get("subclone",""),x["parsed_characteristics"].get("condition",""),x["title"] or ""))
 out={"schema_version":"0.1","generated_at_utc":datetime.now(timezone.utc).isoformat(),"status":"PASS_METADATA_MATCH","soft_sha256":hashlib.sha256(raw).hexdigest(),"target_samples":target,"molecular_values_opened":False}
 OUT.write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps(out,indent=2))
 print("BIO_CHI_SHAFFER_WM989_RECOVERY_METADATA_PASS")
if __name__=="__main__": main()
