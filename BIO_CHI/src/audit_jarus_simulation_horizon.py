#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import re
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"
BASE = BIO / "artifacts" / "generated" / "jarus_matlab_compat" / "source" / "S1_Codes" / "MATLAB files" / "Reduced2023"
OUT = BIO / "artifacts" / "generated" / "jarus_simulation_horizon"
OUT.mkdir(parents=True, exist_ok=True)

SIM = BASE / "simulate_reduced.m"
EXPECTED_SHA = "c15c8da4e9dc582880967d1bd58c0c889f5d9d4c56182720b5e04cfa67c5ed4b"

def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

if not SIM.exists():
    raise SystemExit("BIO_CHI_JARUS_SIM_HORIZON_SOURCE_MISSING")
if sha(SIM) != EXPECTED_SHA:
    raise SystemExit("BIO_CHI_JARUS_SIM_HORIZON_HASH_MISMATCH")

lines = SIM.read_text(encoding="utf-8", errors="replace").splitlines()
rx = re.compile(
    r"function\s+simulate_reduced|t_equil|t_tnf|pulse_begin|pulse_end|rest_end|plot_tspan|timepoints|steps|dur_tnf|24\s*\*\s*3600|24\*3600|ode23s",
    re.IGNORECASE,
)
selected = []
for i, line in enumerate(lines, 1):
    if rx.search(line):
        selected.append({"line": i, "text": line.rstrip()})

result = {
    "schema_version": "0.1",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "audit_type": "published_simulation_horizon_control_flow",
    "simulate_reduced_sha256": sha(SIM),
    "scientific_endpoint_opened": False,
    "trajectory_values_opened": False,
    "chi_bio_constructed": False,
    "selected_source_lines": selected,
    "interpretation_limit": "Source-control-flow audit only. It exists to determine whether the supplied simulator has a fixed plotting/integration horizon that can mechanically invalidate long Figure 8 executions."
}
path = OUT / "simulation_horizon_v0_1.json"
path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
print("BIO_CHI_JARUS_SIM_HORIZON_AUDIT_PASS")
