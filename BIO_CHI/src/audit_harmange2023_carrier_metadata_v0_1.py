#!/usr/bin/env python3
from __future__ import annotations
import csv,gzip,hashlib,io,json,pathlib,urllib.request
from collections import Counter,defaultdict
from datetime import datetime,timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"HARMANGE2023_CARRIER_METADATA_FREEZE_v0_1.json"
OUTDIR=BIO/"artifacts"/"generated"; OUTDIR.mkdir(parents=True,exist_ok=True)
OUT=OUTDIR/"harmange2023_carrier_metadata_v0_1.json"
URL="https://ftp.ncbi.nlm.nih.gov/geo/series/GSE237nnn/GSE237228/suppl/GSE237228_10x_exp3_metadata.tsv.gz"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
 req=urllib.request.Request(url,headers={"User-Agent":UA})
 with urllib.request.urlopen(req,timeout=180) as r:return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()

def clean(v):
 if v is None:return ""
 return str(v).strip()

def main():
 cfg=json.loads(CFG.read_text())
 raw=fetch(URL)
 if sha(raw)!=cfg["metadata_sha256"]:raise SystemExit("metadata SHA mismatch")
 with gzip.GzipFile(fileobj=io.BytesIO(raw),mode="rb") as gz:
  txt=io.TextIOWrapper(gz,encoding="utf-8",errors="replace",newline="")
  rd=csv.DictReader(txt,delimiter="\t")
  fields=rd.fieldnames or []
  for req in [cfg["qualification_rule"]["carrier_field"],cfg["qualification_rule"]["condition_field"]]:
   if req not in fields:raise SystemExit(f"missing required field {req}; fields={fields}")
  sample_field=next((x for x in ["sample_id","sample","orig.ident","Sample","sampleID"] if x in fields),None)
  condition_counts=Counter(); sample_counts=Counter(); lineage_counts=Counter(); lineage_conditions=defaultdict(set); lineage_samples=defaultdict(set)
  rows=0; nonempty_lineage_rows=0; empty_lineage_rows=0; empty_condition_rows=0
  for row in rd:
   rows+=1
   lin=clean(row.get(cfg["qualification_rule"]["carrier_field"]))
   cond=clean(row.get(cfg["qualification_rule"]["condition_field"]))
   samp=clean(row.get(sample_field)) if sample_field else ""
   if cond:condition_counts[cond]+=1
   else:empty_condition_rows+=1
   if samp:sample_counts[samp]+=1
   if lin and lin.lower() not in {"na","nan","none","0"}:
    nonempty_lineage_rows+=1
    lineage_counts[lin]+=1
    if cond:lineage_conditions[lin].add(cond)
    if samp:lineage_samples[lin].add(samp)
   else:empty_lineage_rows+=1
 spanning={lin:sorted(v) for lin,v in lineage_conditions.items() if len(v)>=2}
 n_lineages=len(lineage_counts); n_spanning=len(spanning)
 carrier_defined=n_lineages>=100 and n_spanning>=20
 continuity_defined=len(condition_counts)>=2 and n_spanning>=20
 result={
  "schema_version":"0.1","generated_at_utc":datetime.now(timezone.utc).isoformat(),
  "status":"PASS_CARRIER_METADATA_AUDIT",
  "metadata_sha256":sha(raw),"metadata_bytes":len(raw),"rows":rows,"fields":fields,"sample_field":sample_field,
  "condition_counts":dict(sorted(condition_counts.items())),
  "sample_counts":dict(sorted(sample_counts.items())),
  "lineage":{"nonempty_rows":nonempty_lineage_rows,"empty_rows":empty_lineage_rows,"unique_lineages":n_lineages,
             "lineages_spanning_2plus_conditions":n_spanning,
             "spanning_condition_sets":dict(Counter(tuple(v) for v in spanning.values())),
             "top_lineages_by_cell_count":lineage_counts.most_common(20)},
  "qualification":{"carrier_defined":carrier_defined,"continuity_defined":continuity_defined,"causal_inheritance":"NOT_ESTABLISHED"},
  "expression_values_opened":False
 }
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps(result,indent=2))
 print("BIO_CHI_HARMANGE_CARRIER_METADATA_DONE")
if __name__=="__main__":main()
