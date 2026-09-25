#!/usr/bin/env python3
from __future__ import annotations
import gzip,hashlib,io,json,pathlib,tarfile,tempfile,urllib.request
from datetime import datetime,timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"; CFG=BIO/"config"/"HARMANGE2023_METADATA_MEMBER_HEADER_FREEZE_v0_3.json"
OUTDIR=BIO/"artifacts"/"generated"; OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"harmange2023_metadata_member_header_v0_3.json"
BASE="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE237nnn/GSE237228"
UA="BioChiReviewerReproducibility/0.3"

def get(url,timeout=600):
 req=urllib.request.Request(url,headers={"User-Agent":UA})
 with urllib.request.urlopen(req,timeout=timeout) as r:return r.read()

def sha(b):return hashlib.sha256(b).hexdigest()

def parse_soft(raw,target):
 txt=gzip.decompress(raw).decode("utf-8",errors="replace")
 out={}; cur=None
 for line in txt.splitlines():
  if line.startswith("^SAMPLE = "):
   cur=line.split("=",1)[1].strip()
   if cur in target:out[cur]={"accession":cur,"title":None,"source_name":None,"description":[],"characteristics":[],"relations":[],"supplementary":[]}
  elif cur in out:
   r=out[cur]
   if line.startswith("!Sample_title = "):r["title"]=line.split("=",1)[1].strip()
   elif line.startswith("!Sample_source_name_ch1 = "):r["source_name"]=line.split("=",1)[1].strip()
   elif line.startswith("!Sample_description = "):r["description"].append(line.split("=",1)[1].strip())
   elif line.startswith("!Sample_characteristics_ch1 = "):r["characteristics"].append(line.split("=",1)[1].strip())
   elif line.startswith("!Sample_relation = "):r["relations"].append(line.split("=",1)[1].strip())
   elif line.startswith("!Sample_supplementary_file") and " = " in line:r["supplementary"].append(line.split(" = ",1)[1].strip())
 return out

def main():
 cfg=json.loads(CFG.read_text())
 rawtar=get(BASE+"/suppl/GSE237228_RAW.tar")
 if sha(rawtar)!=cfg["raw_tar_sha256"]:raise SystemExit("RAW tar SHA mismatch")
 headers={}
 with tarfile.open(fileobj=io.BytesIO(rawtar),mode="r:*") as tf:
  names={m.name:m for m in tf.getmembers()}
  for name in cfg["metadata_members"]:
   if name not in names:raise SystemExit(f"missing metadata member {name}")
   f=tf.extractfile(names[name])
   payload=f.read() if f else b""
   with gzip.GzipFile(fileobj=io.BytesIO(payload),mode="rb") as gz:
    header=gz.readline().decode("utf-8",errors="replace").rstrip("\r\n")
   headers[name]={"compressed_bytes":len(payload),"sha256":sha(payload),"header":header,"data_rows_read":0}
 soft=get(BASE+"/soft/GSE237228_family.soft.gz",240)
 roles=parse_soft(soft,{"GSM7597476","GSM7597477"})
 result={"schema_version":"0.3","generated_at_utc":datetime.now(timezone.utc).isoformat(),
         "status":"PASS_METADATA_HEADER_ROLE_DISCOVERY","raw_tar_sha256":sha(rawtar),"metadata_headers":headers,
         "geo_sample_roles":roles,"metadata_data_rows_read":0,"molecular_values_opened":False}
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
 print("BIO_CHI_HARMANGE_METADATA_HEADER_ROLE_PASS")
if __name__=="__main__":main()
