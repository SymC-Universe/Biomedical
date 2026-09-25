#!/usr/bin/env python3
import csv,gzip,hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/"config"/"HARMANGE2023_GRI_BIOCHI_BRIDGE_SOURCE_FREEZE_v0_1.json").read_text())
out=ROOT/"artifacts"/"generated"; out.mkdir(parents=True,exist_ok=True)

def dl(url,p):
    h=hashlib.sha256(); n=0
    with urllib.request.urlopen(url,timeout=120) as r, open(p,"wb") as f:
        while True:
            b=r.read(1024*1024)
            if not b: break
            f.write(b); h.update(b); n+=len(b)
    return h.hexdigest(),n

p=out/"_genes.tsv.gz"
sha,size=dl(cfg["source"]["processed_genes_url"],p)
rows=[]
widths={}
with gzip.open(p,"rt",encoding="utf-8",errors="replace") as f:
    for i,line in enumerate(f):
        cols=line.rstrip("\n\r").split("\t")
        widths[len(cols)]=widths.get(len(cols),0)+1
        if i<8:
            rows.append({"index":i+1,"cols":cols})
        last={"index":i+1,"cols":cols}
        total=i+1
# second pass for last 8 only, small enough
last_rows=[]
with gzip.open(p,"rt",encoding="utf-8",errors="replace") as f:
    all_lines=f.readlines()
for j,line in enumerate(all_lines[-8:], start=total-7):
    last_rows.append({"index":j,"cols":line.rstrip("\n\r").split("\t")})

tokens=("custom","lineage","barcode","feature barcode","antibody")
matching=[]
for i,line in enumerate(all_lines, start=1):
    low=line.lower()
    if any(t in low for t in tokens):
        matching.append({"index":i,"cols":line.rstrip("\n\r").split("\t")})
        if len(matching)>=50: break

res={
 "schema_version":"0.1",
 "gate":"Harmange experiment-3 GEO feature schema",
 "status":"PASS_FEATURE_SCHEMA_READ",
 "genes_sha256":sha,
 "genes_size_bytes":size,
 "feature_rows":total,
 "column_width_counts":widths,
 "first_rows":rows,
 "last_rows":last_rows,
 "keyword_matching_rows":matching,
 "molecular_values_opened":False,
 "target_outcomes_computed":False
}
(out/"harmange2023_feature_schema_v0_1.json").write_text(json.dumps(res,indent=2)+"\n")
print(json.dumps(res,indent=2))
p.unlink(missing_ok=True)
