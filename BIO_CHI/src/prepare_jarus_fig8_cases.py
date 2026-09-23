#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
BASE = BIO / "artifacts" / "generated" / "jarus_matlab_compat" / "source" / "S1_Codes" / "MATLAB files" / "Reduced2023"
OUT = BIO / "artifacts" / "generated" / "jarus_fig8_cases"

EXPECTED_REDUCED_SHA = "b42924cf0b30b8dcb15dac1022f93dd57a535501bd0dcdfa96ed516cb7e25c6c"
EXPECTED_SIM_SHA = "c15c8da4e9dc582880967d1bd58c0c889f5d9d4c56182720b5e04cfa67c5ed4b"

CASES = [
    ("FIG8A_NOMINAL_DAMPED", 9, {}),
    ("FIG8B_LIMIT_CYCLE", 30, {"a2": "0.02", "c5a": "0.00001", "i1a": "0.0001"}),
    ("FIG8C_RELAXATION_OSCILLATION", 30, {"a2": "0.01", "c5a": "0.00001", "i1a": "0.0001"}),
]

ORIGINAL_LINES = {
    "a2": "a2=0.0763;",
    "c5a": "c5a=5.778e-05;",
    "i1a": "i1a=0.000595;",
}

def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

if sha(BASE / "reduced.m") != EXPECTED_REDUCED_SHA:
    raise SystemExit("BIO_CHI_JARUS_FIG8_BASE_REDUCED_HASH_MISMATCH")
if sha(BASE / "simulate_reduced.m") != EXPECTED_SIM_SHA:
    raise SystemExit("BIO_CHI_JARUS_FIG8_BASE_SIM_HASH_MISMATCH")

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

records = []
for case_id, duration_h, overrides in CASES:
    case_dir = OUT / case_id / "source"
    shutil.copytree(BASE, case_dir)
    reduced = case_dir / "reduced.m"
    text = reduced.read_text(encoding="utf-8")
    replacements = []
    for name, value in overrides.items():
        before = ORIGINAL_LINES[name]
        after = f"{name}={value};"
        count = text.count(before)
        if count != 1:
            raise SystemExit(f"BIO_CHI_JARUS_FIG8_PATCH_COUNT_{case_id}_{name}_{count}")
        text = text.replace(before, after, 1)
        replacements.append({"parameter": name, "before": before, "after": after})
    reduced.write_text(text, encoding="utf-8")
    records.append({
        "case_id": case_id,
        "duration_hours": duration_h,
        "source_dir": case_dir.relative_to(ROOT).as_posix(),
        "parameter_overrides": overrides,
        "replacements": replacements,
        "reduced_sha256": sha(reduced),
        "simulate_reduced_sha256": sha(case_dir / "simulate_reduced.m"),
    })

manifest = {
    "schema_version": "0.1",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "audit_type": "prospectively_frozen_figure8_case_preparation",
    "execution_freeze": "BIO_CHI/config/JARUS_FIG8_EXECUTION_FREEZE_v0_1.json",
    "base_reduced_sha256": EXPECTED_REDUCED_SHA,
    "base_simulate_reduced_sha256": EXPECTED_SIM_SHA,
    "published_source_preserved": True,
    "execution_copies_modified_only_by_frozen_parameter_overrides": True,
    "scientific_endpoint_opened": False,
    "chi_bio_constructed": False,
    "cases": records,
}
(OUT / "case_preparation_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps(manifest, indent=2))
print("BIO_CHI_JARUS_FIG8_CASE_PREP_PASS")
