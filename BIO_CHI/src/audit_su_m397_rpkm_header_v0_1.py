#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, io, json, pathlib, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SU2026_M397_RPKM_HEADER_FREEZE_v0_1.json"
PIN=BIO/"config"/"SU2026_M397_RPKM_SOURCE_FREEZE_V01_RESULT_PIN.json"
OUT=BIO/"artifacts"/"generated"
OUT.mkdir(parents=True,exist_ok=True)
OUT_FILE=OUT/"su2026_m397_rpkm_header_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def main():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    pin=json.loads(PIN.read_text(encoding="utf-8"))
    req=urllib.request.Request(
      "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE134nnn/GSE134459/suppl/GSE134459_Reversible_RPKM_values.txt.gz",
      headers={"User-Agent":UA}
    )
    with urllib.request.urlopen(req,timeout=180) as r:
        raw=r.read()
    obs=hashlib.sha256(raw).hexdigest()
    if obs!=cfg["expected_sha256"] or obs!=pin["sha256"]:
        raise SystemExit(f"SU_RPKM_HEADER_HASH_MISMATCH {obs}")
    with gzip.GzipFile(fileobj=io.BytesIO(raw),mode="rb") as gz:
        header_bytes=gz.readline()
    header=header_bytes.decode("utf-8-sig",errors="replace").rstrip("\r\n")
    delimiter="\t" if "\t" in header else ("," if "," in header else None)
    columns=header.split(delimiter) if delimiter else [header]
    result={
      "schema_version":"0.1",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],
      "source_sha256":obs,
      "header":header,
      "delimiter":delimiter,
      "column_count":len(columns),
      "columns":columns,
      "data_lines_read":0,
      "rpkm_values_read":False,
      "scientific_values_interpreted":False,
      "status":"PASS_HEADER_ONLY_SCHEMA_CAPTURE" if header and delimiter else "FAIL_HEADER_SCHEMA_CAPTURE"
    }
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
    if result["status"]!="PASS_HEADER_ONLY_SCHEMA_CAPTURE":
        raise SystemExit("BIO_CHI_SU_RPKM_HEADER_FAIL")
    print("BIO_CHI_SU_RPKM_HEADER_PASS")
if __name__=="__main__": main()
