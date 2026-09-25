#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, io, json, pathlib, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SHAFFER2017_GSE97681_FILEMAP_FREEZE_v0_1.json"
OUTDIR=BIO/"artifacts"/"generated"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"shaffer2017_gse97681_filemap_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=180) as r:
        b=r.read()
        return b,{"resolved_url":r.geturl(),"content_type":r.headers.get("Content-Type"),"content_length":r.headers.get("Content-Length"),"last_modified":r.headers.get("Last-Modified")}

def sha(b): return hashlib.sha256(b).hexdigest()

def parse_soft(raw):
    txt=gzip.decompress(raw).decode("utf-8",errors="replace")
    samples={}; cur=None
    for line in txt.splitlines():
        if line.startswith("^SAMPLE = "):
            cur=line.split("=",1)[1].strip()
            samples[cur]={"accession":cur,"title":None,"characteristics":[],"description":[]}
        elif cur and line.startswith("!Sample_title = "):
            samples[cur]["title"]=line.split("=",1)[1].strip()
        elif cur and line.startswith("!Sample_characteristics_ch1 = "):
            samples[cur]["characteristics"].append(line.split("=",1)[1].strip())
        elif cur and line.startswith("!Sample_description = "):
            samples[cur]["description"].append(line.split("=",1)[1].strip())
    return samples

def labels(rec):
    text=" | ".join([rec.get("title") or ""]+rec["characteristics"]+rec["description"]).lower()
    out=[]
    for lab in ["48hrholiday","7dayholiday","nodrug","drug"]:
        if lab in text: out.append(lab)
    return out

def main():
    cfg=json.loads(CFG.read_text())
    base="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE97nnn/GSE97681"
    soft,softmeta=fetch(base+"/soft/GSE97681_family.soft.gz")
    samples=parse_soft(soft)
    groups={"48hrholiday":[],"7dayholiday":[],"nodrug":[],"drug":[]}
    for acc,rec in samples.items():
        labs=labels(rec)
        rec["labels"]=labs
        for lab in labs: groups[lab].append(rec)
    files=[]
    for name in cfg["processed_files"]:
        raw,meta=fetch(base+"/suppl/"+name)
        if name.endswith(".gz"):
            with gzip.GzipFile(fileobj=io.BytesIO(raw),mode="rb") as gz:
                header=gz.readline().decode("utf-8",errors="replace").rstrip("\r\n")
        else:
            header=raw.splitlines()[0].decode("utf-8",errors="replace")
        files.append({"name":name,"compressed_bytes":len(raw),"sha256":sha(raw),"header":header,"meta":meta,"data_rows_read":0})
    result={
      "schema_version":"0.1","generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "status":"PASS_FILE_IDENTITY_HEADER_LABEL_MAP","geo":"GSE97681",
      "soft":{"bytes":len(soft),"sha256":sha(soft),"meta":softmeta},
      "groups":groups,"processed_files":files,"molecular_values_opened":False
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({
      "status":result["status"],
      "group_counts":{k:len(v) for k,v in groups.items()},
      "groups":{k:[{"accession":x["accession"],"title":x["title"],"characteristics":x["characteristics"]} for x in v] for k,v in groups.items()},
      "files":[{"name":x["name"],"bytes":x["compressed_bytes"],"sha256":x["sha256"],"header":x["header"]} for x in files],
      "molecular_values_opened":False
    },indent=2))
    print("BIO_CHI_SHAFFER_FILEMAP_PASS")
if __name__=="__main__": main()
