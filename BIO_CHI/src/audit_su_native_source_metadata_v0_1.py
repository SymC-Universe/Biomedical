#!/usr/bin/env python3
from __future__ import annotations
import gzip, hashlib, json, pathlib, urllib.request
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[2]
BIO=ROOT/"BIO_CHI"
CFG=BIO/"config"/"SU2026_NATIVE_METHOD_SOURCE_METADATA_FREEZE_v0_1.json"
SUB=BIO/"config"/"SU2026_SOURCE_SUBSET_v0_1.json"
OUT=BIO/"artifacts"/"generated"
OUT.mkdir(parents=True,exist_ok=True)
OUT_FILE=OUT/"su2026_native_method_source_metadata_v0_1.json"
UA="BioChiReviewerReproducibility/0.1"

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=180) as r: return r.read()

def sha256(b): return hashlib.sha256(b).hexdigest()

def main():
    cfg=json.loads(CFG.read_text(encoding="utf-8"))
    subset=json.loads(SUB.read_text(encoding="utf-8"))
    expected=[x["gsm"] for x in subset["rna_timecourse"]]
    raw=fetch(cfg["family_soft_url"])
    obs=sha256(raw)
    if obs!=cfg["family_soft_sha256"]:
        raise SystemExit(f"SU_SOURCE_SOFT_HASH_MISMATCH expected={cfg['family_soft_sha256']} observed={obs}")
    text=gzip.decompress(raw).decode("utf-8",errors="replace")
    samples={}; current=None
    for line in text.splitlines():
        if line.startswith("^SAMPLE = "):
            current=line.split("=",1)[1].strip()
            samples[current]={
              "title":[],"source_name":[],"characteristics":[],"data_processing":[],
              "relations":[],"supplementary_files":[],"platform_id":[],"library_strategy":[]
            }
        elif line.startswith("^") and not line.startswith("^SAMPLE"):
            current=None
        elif current:
            r=samples[current]
            if line.startswith("!Sample_title = "): r["title"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_source_name_ch1 = "): r["source_name"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_characteristics_ch1 = "): r["characteristics"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_data_processing = "): r["data_processing"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_relation = "): r["relations"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_supplementary_file = "): r["supplementary_files"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_platform_id = "): r["platform_id"].append(line.split("=",1)[1].strip())
            elif line.startswith("!Sample_library_strategy = "): r["library_strategy"].append(line.split("=",1)[1].strip())
    missing=[g for g in expected if g not in samples]
    selected={g:samples[g] for g in expected if g in samples}
    result={
      "schema_version":"0.1",
      "generated_at_utc":datetime.now(timezone.utc).isoformat(),
      "gate":cfg["gate"],
      "family_soft_sha256":obs,
      "expected_gsms":expected,
      "missing_gsms":missing,
      "selected_sample_metadata":selected,
      "expression_values_read":False,
      "surprisal_computed":False,
      "status":"PASS_SU_NATIVE_SOURCE_METADATA" if not missing else "FAIL_MISSING_FROZEN_GSMS"
    }
    OUT_FILE.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
      "output":str(OUT_FILE.relative_to(ROOT)),
      "status":result["status"],
      "expected_count":len(expected),
      "missing":missing,
      "processing_unique":sorted({p for v in selected.values() for p in v["data_processing"]}),
      "supplementary_unique":sorted({p for v in selected.values() for p in v["supplementary_files"]}),
      "expression_values_read":False
    },indent=2))
    if missing: raise SystemExit("BIO_CHI_SU_NATIVE_SOURCE_METADATA_FAIL")
    print("BIO_CHI_SU_NATIVE_SOURCE_METADATA_PASS")

if __name__=="__main__": main()
