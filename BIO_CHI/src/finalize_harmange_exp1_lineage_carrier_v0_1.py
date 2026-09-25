#!/usr/bin/env python3
import hashlib, json, pathlib, sys

if len(sys.argv) != 5:
    raise SystemExit("usage: finalize_harmange_exp1_lineage_carrier_v0_1.py <rds> <result_json> <lineage_csv> <expected_bytes>")
rds=pathlib.Path(sys.argv[1]); result=pathlib.Path(sys.argv[2]); csvp=pathlib.Path(sys.argv[3]); expected=int(sys.argv[4])
if rds.stat().st_size != expected:
    raise SystemExit(f"RDS byte-size mismatch {rds.stat().st_size} != {expected}")
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(8*1024*1024),b""): h.update(c)
    return h.hexdigest()
d=json.loads(result.read_text())
d["source_rds_bytes"]=rds.stat().st_size
d["source_rds_sha256"]=sha(rds)
d["lineage_table_sha256"]=sha(csvp)
result.write_text(json.dumps(d,indent=2)+"\n")
print(json.dumps({
    "status":d["status"],
    "source_rds_bytes":d["source_rds_bytes"],
    "source_rds_sha256":d["source_rds_sha256"],
    "retained_cell_count":d["retained_cell_count"],
    "unique_lineage_count":d["unique_lineage_count"],
    "lineage_size":d["lineage_size"],
    "startID_cell_counts":d["startID_cell_counts"],
    "startID_lineage_counts":d["startID_lineage_counts"],
    "qualification_checks":d["qualification_checks"],
    "carrier_defined":d["carrier_defined"]
},indent=2))
print("BIO_CHI_HARMANGE_EXP1_CARRIER_QUALIFICATION_FINALIZED")
