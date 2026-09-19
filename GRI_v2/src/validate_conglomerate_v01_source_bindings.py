from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "config" / "chi_bio_conglomerate_v01_source_bindings.json"

REQUIRED_BLOCKS = {"R","S","E","G","P","M","T","Q"}

def validate():
    data=json.loads(BINDING.read_text())
    assert data["schema"]=="GRI_CHI_BIO_CONGLOMERATE_V01_SOURCE_BINDINGS"
    assert set(data["blocks"])==REQUIRED_BLOCKS
    fw=data["global_firewalls"]
    assert fw["scalar_required"] is False
    assert fw["damped_oscillator_required"] is False
    assert fw["unity_boundary_required"] is False
    assert fw["clinical_endpoint_used_to_construct_carrier"] is False
    assert fw["tcga_final_holdout_is_external_for_new_conglomerate_version"] is False
    missing=[]
    for block,spec in data["blocks"].items():
        for rel in spec.get("sources",[]):
            p=ROOT.parent / rel if rel.startswith("GRI_v2/") else ROOT / rel
            if not p.exists():
                missing.append((block,rel))
    if missing:
        raise AssertionError(f"missing bound source files: {missing}")
    return data

if __name__=="__main__":
    d=validate()
    out=ROOT / "conglomerate_v01_outputs"
    out.mkdir(exist_ok=True)
    (out/"source_binding_validation.json").write_text(json.dumps({
        "status":"PASS",
        "schema":d["schema"],
        "blocks":sorted(d["blocks"]),
        "source_file_validation":"PASS",
        "scalar_required":False,
        "damped_oscillator_required":False,
        "unity_boundary_required":False
    },indent=2)+"\n")
