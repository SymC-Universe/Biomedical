from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from src.probe_stage_b2_sources import download, probe_data_endpoint, scan

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "config" / "stage_b2_source_plan.json"

EXPECTED = {
    "aneuploidy_loh": "4e115fd7408a06b002f34678fa46df0b05aa20ac71db57acf535238f37aa64c8",
    "cnv_burden": "4b63eefb164866a3c49c50c04ee423d3ad1c25540f7cf39e08d997b454a189d0",
    "rppa_final": "06246573836865589134bd9424189f81b0d9fb436fcbf5e72024225442c400de",
    "methylation_merged_27k_450k": "5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77",
}

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def run(out_path: Path, download_dir: Path) -> dict:
    plan=json.loads(PLAN.read_text())
    records=[]
    for src in plan["sources"]:
        url=f"https://api.gdc.cancer.gov/data/{src['gdc_uuid']}"
        meta=probe_data_endpoint(url)
        rec={
            "id":src["id"],
            "role":src["role"],
            "file_name":src["file_name"],
            "gdc_uuid":src["gdc_uuid"],
            "metadata":meta,
            "expected_sha256":EXPECTED.get(src["id"]),
        }
        if src["download_now"]:
            p=download_dir/src["file_name"]
            download(url,p)
            got=sha256_file(p)
            rec["downloaded_bytes"]=p.stat().st_size
            rec["sha256"]=got
            rec["hash_match"]=(EXPECTED.get(src["id"]) == got)
            rec["scan"]=scan(p)
        else:
            rec["hash_match"]=None
            rec["download_status"]="METADATA_ONLY"
        records.append(rec)

    small=[r for r in records if r.get("sha256")]
    all_small_ok=all(r["hash_match"] for r in small)
    methyl=next(r for r in records if r["id"]=="methylation_merged_27k_450k")
    result={
        "schema":"GRI_CHI_BIO_CONGLOMERATE_V01_MATERIALIZATION_PREFLIGHT",
        "status":"PASS" if all_small_ok else "FAIL",
        "no_biological_outcomes_opened":True,
        "no_conglomerate_weights_selected":True,
        "no_scalar_chi_created":True,
        "small_source_hashes_pass":all_small_ok,
        "sources":records,
        "materialization_plan":{
            "G":"REMOTE_READY_SMALL_SOURCE",
            "P":"REMOTE_READY_SMALL_SOURCE",
            "S":"REMOTE_SOURCE_VERIFIED_METADATA_ONLY_LARGE_5GB",
            "R":"SOURCE_IDENTITY_HASH_KNOWN_BUT_REMOTE_FETCH_ROUTE_NOT_YET_BOUND",
            "E":"RECONSTRUCT_FROM_FROZEN_PURITY_LEUKOCYTE_SOURCES_OR_RECOVER_MILESTONE_VALUES",
            "M":"DERIVE_FROM_FROZEN_R_S_CARRIERS_AFTER_MATERIALIZATION",
            "T":"SYSTEM_SPECIFIC_EXISTING_SCC25_ARTIFACTS_KEEP_SEPARATE",
            "Q":"EXISTING_INTERNAL_CONFIDENCE_AND_PROVENANCE_METADATA_READY"
        },
        "methylation_remote_size_bytes":methyl.get("metadata",{}).get("content_length"),
        "next":"bind an exact remote source route for the frozen 1.882GB RNA matrix, then stage R/S materialization without opening clinical outcomes"
    }
    out_path.parent.mkdir(parents=True,exist_ok=True)
    out_path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    return result

if __name__=="__main__":
    out=ROOT/"conglomerate_v01_outputs"/"materialization_preflight.json"
    with tempfile.TemporaryDirectory() as td:
        result=run(out,Path(td))
    if result["status"]!="PASS":
        raise SystemExit(2)
