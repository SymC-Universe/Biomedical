#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, io, json, pathlib, urllib.request, zipfile
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"BLUM2019_FIG2_NATIVE_MEAN_INPUT_MAPPING_FREEZE_v0_1.json"
PIN=BIO/"config"/"BLUM2019_MENDELEY_SOURCE_FREEZE_V02_RESULT_PIN.json"
OUT=BIO/"artifacts"/"generated"
OUT.mkdir(parents=True,exist_ok=True)
OUT_FILE=OUT/"blum2019_fig2_native_mean_input_mapping_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def sha256(b): return hashlib.sha256(b).hexdigest()
def firstline(b): return b.decode("utf-8-sig",errors="replace").splitlines()[0] if b else ""

def main():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    pin=json.loads(PIN.read_text(encoding="utf-8"))
    req=urllib.request.Request(pin["selected_file"]["download_url"],headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=180) as r: raw=r.read()
    obs=sha256(raw)
    if obs!=cfg["source_sha256"]: raise SystemExit(f"BLUM_FIG2_SOURCE_HASH_MISMATCH {obs}")
    recs=[]; readme=None
    with zipfile.ZipFile(io.BytesIO(raw),"r") as zf:
        names=set(zf.namelist())
        missing=[p for p in cfg["allowed_members"] if p not in names]
        if missing: raise SystemExit(f"BLUM_FIG2_MISSING {missing}")
        for p in cfg["allowed_members"]:
            payload=zf.read(p)
            rec={"path":p,"size_bytes":len(payload),"sha256":sha256(payload)}
            if p.endswith("README.txt"):
                readme=payload.decode("utf-8",errors="replace")
                rec["inspection"]="FULL_README"
                rec["text"]=readme
            elif p.endswith(".csv.gz"):
                with gzip.GzipFile(fileobj=io.BytesIO(payload),mode="rb") as gz:
                    h=gz.readline()
                rec["inspection"]="HEADER_ONLY_GZIP"
                rec["header"]=firstline(h)
            elif p.endswith(".csv"):
                h=payload.splitlines()[0] if payload else b""
                rec["inspection"]="HEADER_ONLY"
                rec["header"]=firstline(h)
            recs.append(rec)
    result={
      "schema_version":"0.1","generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],"archive_sha256":obs,"records":recs,
      "data_rows_read":False,"metric_computed":False,"scientific_values_interpreted":False,
      "status":"PASS_FIG2_NATIVE_INPUT_MAPPING"
    }
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "output":str(OUT_FILE.relative_to(ROOT)),"status":result["status"],
      "headers":{r["path"]:r.get("header") for r in recs if "header" in r},
      "readme":readme,"data_rows_read":False
    },indent=2))
    print("BIO_CHI_BLUM_FIG2_NATIVE_INPUT_MAPPING_PASS")
if __name__=="__main__": main()
