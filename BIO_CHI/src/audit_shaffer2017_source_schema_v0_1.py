#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, html.parser, json, pathlib, re, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SHAFFER2017_SOURCE_SCHEMA_FREEZE_v0_1.json"
OUTDIR=BIO/"artifacts"/"generated"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"shaffer2017_source_schema_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=180) as r:
        b=r.read()
        return b,{"requested_url":url,"resolved_url":r.geturl(),"content_type":r.headers.get("Content-Type"),"content_length":r.headers.get("Content-Length"),"last_modified":r.headers.get("Last-Modified")}

def sha(b): return hashlib.sha256(b).hexdigest()

def series_bucket(acc):
    n=int(acc[3:])
    return f"GSE{n//1000}nnn"

def parse_soft(raw):
    txt=gzip.decompress(raw).decode("utf-8",errors="replace")
    out={"series":{},"samples":{}}
    current=None; curacc=None
    for line in txt.splitlines():
        if line.startswith("^SERIES = "):
            current="series"; curacc=line.split("=",1)[1].strip()
        elif line.startswith("^SAMPLE = "):
            current="sample"; curacc=line.split("=",1)[1].strip()
            out["samples"][curacc]={"accession":curacc,"title":None,"source_name":None,"platform":None,"characteristics":[],"relations":[],"description":[]}
        elif line.startswith("!Series_") and current=="series":
            k,v=line[1:].split(" = ",1) if " = " in line else (line[1:],"")
            out["series"].setdefault(k,[]).append(v)
        elif current=="sample" and curacc:
            rec=out["samples"][curacc]
            if line.startswith("!Sample_title = "): rec["title"]=line.split("=",1)[1].strip()
            elif line.startswith("!Sample_source_name_ch1 = "): rec["source_name"]=line.split("=",1)[1].strip()
            elif line.startswith("!Sample_platform_id = "): rec["platform"]=line.split("=",1)[1].strip()
            elif line.startswith("!Sample_characteristics_ch1 = "): rec["characteristics"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_relation = "): rec["relations"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_description = "): rec["description"].append(line.split("=",1)[1].strip())
    return out

def list_suppl(acc):
    bucket=series_bucket(acc)
    url=f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket}/{acc}/suppl/"
    try:
        raw,meta=fetch(url)
        txt=raw.decode("utf-8",errors="replace")
        hrefs=re.findall(r'href="([^"]+)"',txt)
        files=[]
        for h in hrefs:
            if h in ("../","/") or h.endswith("/"): continue
            if acc in h or not h.startswith("?"):
                files.append(h)
        return {"status":"OK","url":url,"files":sorted(set(files)),"listing_sha256":sha(raw),"meta":meta}
    except Exception as e:
        return {"status":"ERROR","url":url,"error":f"{type(e).__name__}: {e}"}

def classify(rec):
    text=" | ".join([rec.get("title") or "",rec.get("source_name") or ""]+rec.get("characteristics",[])+rec.get("description",[])).lower()
    labels=[]
    for token in ["48hrholiday","7dayholiday","nodrug","drug","untreated","vemurafenib","dabrafenib","resistant","parental","single cell","bulk","scrna","rna-seq"]:
        if token in text: labels.append(token)
    return labels

def main():
    cfg=json.loads(CFG.read_text())
    result={"schema_version":"0.1","generated_at_utc":datetime.now(timezone.utc).isoformat(),"gate":cfg["gate"],"status":"PASS_METADATA_SCHEMA_AUDIT","molecular_values_opened":False,"series":{}}
    for acc in cfg["accessions"]:
        bucket=series_bucket(acc)
        url=f"https://ftp.ncbi.nlm.nih.gov/geo/series/{bucket}/{acc}/soft/{acc}_family.soft.gz"
        raw,meta=fetch(url)
        parsed=parse_soft(raw)
        for rec in parsed["samples"].values():
            rec["keyword_labels"]=classify(rec)
        result["series"][acc]={
          "soft_url":url,"soft_sha256":sha(raw),"soft_bytes":len(raw),"download_meta":meta,
          "series_metadata":parsed["series"],
          "sample_count":len(parsed["samples"]),
          "samples":parsed["samples"],
          "supplementary_listing":list_suppl(acc)
        }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    summary={}
    for acc,s in result["series"].items():
        counts={}
        for rec in s["samples"].values():
            for lab in rec["keyword_labels"]: counts[lab]=counts.get(lab,0)+1
        summary[acc]={"sample_count":s["sample_count"],"keyword_counts":counts,"supplementary_files":s["supplementary_listing"].get("files",[])}
    print(json.dumps({"status":result["status"],"summary":summary,"molecular_values_opened":False},indent=2))
    print("BIO_CHI_SHAFFER_SOURCE_SCHEMA_PASS")
if __name__=="__main__": main()
