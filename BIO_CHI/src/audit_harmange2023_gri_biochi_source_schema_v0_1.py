#!/usr/bin/env python3
import gzip, hashlib, json, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
cfg=json.loads((ROOT/"config"/"HARMANGE2023_GRI_BIOCHI_BRIDGE_SOURCE_FREEZE_v0_1.json").read_text())
outdir=ROOT/"artifacts"/"generated"
outdir.mkdir(parents=True, exist_ok=True)

def download(url, dest):
    h=hashlib.sha256()
    size=0
    with urllib.request.urlopen(url, timeout=120) as r, open(dest,"wb") as f:
        while True:
            chunk=r.read(1024*1024)
            if not chunk: break
            f.write(chunk); h.update(chunk); size += len(chunk)
    return {"sha256":h.hexdigest(),"size_bytes":size}

meta_tmp=outdir/"_harmange_metadata.tsv.gz"
bar_tmp=outdir/"_harmange_barcodes.tsv.gz"
meta_info=download(cfg["source"]["processed_metadata_url"],meta_tmp)
bar_info=download(cfg["source"]["processed_barcodes_url"],bar_tmp)

with gzip.open(meta_tmp,"rt",encoding="utf-8",errors="replace") as f:
    header=f.readline().rstrip("\n\r").split("\t")
    row_count=sum(1 for _ in f)
with gzip.open(bar_tmp,"rt",encoding="utf-8",errors="replace") as f:
    barcode_header_or_first=f.readline().rstrip("\n\r")
    barcode_row_count=1+sum(1 for _ in f)

lower=[x.lower() for x in header]
lineage_fields=[header[i] for i,x in enumerate(lower) if any(k in x for k in ["lineage","barcode","clone"])]
condition_fields=[header[i] for i,x in enumerate(lower) if any(k in x for k in ["condition","treatment","tgfb","pi3k","sample"])]
state_fields=[header[i] for i,x in enumerate(lower) if any(k in x for k in ["primed","cluster","state","egfr","ngfr","sox10"])]

required_design={
  "has_lineage_or_barcode_field": bool(lineage_fields),
  "has_condition_or_sample_field": bool(condition_fields),
  "metadata_rows_positive": row_count>0,
  "barcode_rows_positive": barcode_row_count>0
}
status="PASS_SOURCE_CARRIER_SCHEMA" if all(required_design.values()) else "FAIL_SOURCE_CARRIER_SCHEMA"

result={
 "schema_version":"0.1",
 "project":"GRI Bio Chi Bridge",
 "gate":"Harmange 2023 source/carrier schema audit",
 "freeze":"BIO_CHI/config/HARMANGE2023_GRI_BIOCHI_BRIDGE_SOURCE_FREEZE_v0_1.json",
 "status":status,
 "metadata":{"sha256":meta_info["sha256"],"size_bytes":meta_info["size_bytes"],"rows_excluding_header":row_count,"columns":len(header),"header":header},
 "barcodes":{"sha256":bar_info["sha256"],"size_bytes":bar_info["size_bytes"],"rows":barcode_row_count,"first_record_shape_only":len(barcode_header_or_first)},
 "field_groups":{"lineage_fields":lineage_fields,"condition_fields":condition_fields,"state_fields":state_fields},
 "design_checks":required_design,
 "molecular_values_opened":false,
 "target_outcomes_computed":false,
 "next_action":"freeze exact lineage-to-cell and condition mapping using metadata identifiers only" if status.startswith("PASS") else "refuse Harmange bridge carrier and move to frozen Shaffer backup"
}
(outdir/"harmange2023_gri_biochi_source_schema_v0_1.json").write_text(json.dumps(result,indent=2)+"\n")

md=[
"# Harmange 2023 GRI ↔ Bio Chi source/carrier schema audit","",
f"**Status:** {status}","",
f"- metadata rows: {row_count}",
f"- metadata columns: {len(header)}",
f"- lineage/barcode-like fields: {', '.join(lineage_fields) if lineage_fields else 'none'}",
f"- condition/sample-like fields: {', '.join(condition_fields) if condition_fields else 'none'}",
f"- state-like fields: {', '.join(state_fields) if state_fields else 'none'}",
f"- molecular values opened: no",
f"- target outcomes computed: no","",
"## Next gate","",
result["next_action"],""
]
(outdir/"HARMANGE2023_GRI_BIOCHI_SOURCE_SCHEMA_V0_1_AUDIT.md").write_text("\n".join(md))
meta_tmp.unlink(missing_ok=True)
bar_tmp.unlink(missing_ok=True)
print(json.dumps(result,indent=2))
