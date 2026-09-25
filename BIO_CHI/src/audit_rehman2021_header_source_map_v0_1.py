#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, io, json, pathlib, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"REHMAN2021_HEADER_SOURCE_MAP_FREEZE_v0_1.json"
OUTDIR=BIO/"artifacts"/"generated"
OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"rehman2021_header_source_map_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def get(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=180) as r:
        return r.read(),{"resolved_url":r.geturl(),"content_type":r.headers.get("Content-Type"),"content_length":r.headers.get("Content-Length")}
def sha(b): return hashlib.sha256(b).hexdigest()

def parse_soft(raw):
    txt=gzip.decompress(raw).decode("utf-8",errors="replace")
    samples={}
    cur=None
    for line in txt.splitlines():
        if line.startswith("^SAMPLE = "):
            cur=line.split("=",1)[1].strip()
            samples[cur]={"accession":cur,"title":None,"characteristics":[]}
        elif cur and line.startswith("!Sample_title = "):
            samples[cur]["title"]=line.split("=",1)[1].strip()
        elif cur and line.startswith("!Sample_characteristics_ch1 = "):
            samples[cur]["characteristics"].append(line.split("=",1)[1].strip())
    return samples

def main():
    cfg=json.loads(CFG.read_text())
    counts,cmeta=get(cfg["counts_url"])
    soft,smeta=get(cfg["soft_url"])
    if sha(counts)!=cfg["counts_sha256"]: raise SystemExit("counts sha mismatch")
    if sha(soft)!=cfg["soft_sha256"]: raise SystemExit("soft sha mismatch")
    with gzip.GzipFile(fileobj=io.BytesIO(counts),mode="rb") as gz:
        header=gz.readline().decode("utf-8",errors="replace").rstrip("\n\r")
    cols=header.split("\t")
    samples=parse_soft(soft)
    title_to_acc={}
    duplicate_titles={}
    for acc,rec in samples.items():
        t=rec["title"]
        if t in title_to_acc: duplicate_titles.setdefault(t,[title_to_acc[t]]).append(acc)
        else: title_to_acc[t]=acc
    mapped=[]
    unmapped=[]
    for i,c in enumerate(cols):
        key=c.strip()
        acc=None
        if key in samples: acc=key
        elif key in title_to_acc and key not in duplicate_titles: acc=title_to_acc[key]
        else:
            # tolerate common filename/header suffixes by exact title containment only if unique
            hits=[a for t,a in title_to_acc.items() if t and (key==t or key.startswith(t+"_") or t.startswith(key+"_"))]
            if len(set(hits))==1: acc=hits[0]
        if acc:
            mapped.append({"column_index_1based":i+1,"header":key,"accession":acc,"title":samples[acc]["title"],"characteristics":samples[acc]["characteristics"]})
        else:
            unmapped.append({"column_index_1based":i+1,"header":key})
    # source-label candidate sets, metadata only
    by_acc={x["accession"]:x for x in mapped}
    sets={
      "saline_8w":["GSM4315308","GSM4315309","GSM4315310"],
      "barcoded_dmso_8w":["GSM4315311","GSM4315312","GSM4315313"],
      "nonbarcoded_ctrl":["GSM4315329","GSM4315330","GSM4315331","GSM4315332"],
      "cpt11_regrowth":["GSM4315317","GSM4315318","GSM4315319"],
      "cpt11_resistant_7mo":["GSM4315323","GSM4315324","GSM4315325"],
      "cpt11_8w":["GSM4315326","GSM4315327","GSM4315328"]
    }
    set_meta={k:[by_acc[a] for a in v if a in by_acc] for k,v in sets.items()}
    result={
      "schema_version":"0.1","generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],"status":"PASS_HEADER_SOURCE_MAP",
      "counts":{"sha256":sha(counts),"compressed_bytes":len(counts),"header_column_count":len(cols),"header":cols,"data_rows_read":0,"meta":cmeta},
      "soft":{"sha256":sha(soft),"compressed_bytes":len(soft),"sample_count":len(samples),"meta":smeta},
      "mapped_columns":mapped,"unmapped_columns":unmapped,"source_sets":set_meta,
      "molecular_values_opened":False
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({
      "status":result["status"],"header_column_count":len(cols),"mapped_count":len(mapped),"unmapped":unmapped,
      "source_sets":{k:[{"acc":x["accession"],"title":x["title"],"characteristics":x["characteristics"]} for x in v] for k,v in set_meta.items()},
      "molecular_values_opened":False
    },indent=2))
    print("BIO_CHI_REHMAN_HEADER_SOURCE_MAP_PASS")
if __name__=="__main__": main()
