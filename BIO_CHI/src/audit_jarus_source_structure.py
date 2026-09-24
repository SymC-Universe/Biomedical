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
OUT = BIO / "artifacts" / "generated" / "jarus_source_structure"
OUT.mkdir(parents=True, exist_ok=True)

EXPECTED = {
    "reduced.m": "b42924cf0b30b8dcb15dac1022f93dd57a535501bd0dcdfa96ed516cb7e25c6c",
    "run_simulate_reduced.m": "2acbc191ff2f48bb6f4382a7156b3bf3eaf58122fa06d06c76e3b7a39d51e951",
    "simulate_reduced.m": "c15c8da4e9dc582880967d1bd58c0c889f5d9d4c56182720b5e04cfa67c5ed4b",
}

def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def numbered_noncomment(path: pathlib.Path) -> list[dict]:
    out=[]
    for i,line in enumerate(path.read_text(encoding="utf-8",errors="replace").splitlines(),1):
        s=line.strip()
        if not s or s.startswith("%"):
            continue
        out.append({"line":i,"text":s})
    return out

def structural_subset(path: pathlib.Path) -> list[dict]:
    patterns = [
        r"^function\b", r"\bode23s\b", r"\bsimulate_reduced\b", r"\breduced\(",
        r"\bfigure\b", r"\bsubplot\b", r"\bplot\b", r"\bxlabel\b", r"\bylabel\b",
        r"\btitle\b", r"\blegend\b", r"\bxlim\b", r"\bylim\b", r"\btnf\b",
        r"\btspan\b", r"\bspecies\b", r"\bparams?\b", r"\bparameters?\b",
        r"\ba2\b", r"\bc5a\b", r"\bi1a\b", r"\bTR\b", r"\bNF", r"\bIKK", r"\bA20",
    ]
    rx=re.compile("|".join(patterns),re.IGNORECASE)
    return [x for x in numbered_noncomment(path) if rx.search(x["text"])]

files={}
failures=[]
for name, expected in EXPECTED.items():
    p=BASE/name
    if not p.exists():
        failures.append(f"missing {name}")
        continue
    actual=sha(p)
    if actual != expected:
        failures.append(f"hash mismatch {name}: {actual}")
    files[name]={
        "sha256":actual,
        "line_count":len(p.read_text(encoding="utf-8",errors="replace").splitlines()),
        "structural_lines": numbered_noncomment(p) if name == "run_simulate_reduced.m" else structural_subset(p),
    }

result={
    "schema_version":"0.1",
    "generated_at_utc":datetime.now(timezone.utc).isoformat(),
    "audit_type":"published_source_structure_only",
    "published_source_preserved":True,
    "execution_copy_modified_only_by_frozen_compatibility_repair":True,
    "scientific_endpoint_opened":False,
    "chi_bio_constructed":False,
    "files":files,
    "failures":failures,
    "interpretation_limit":"This audit exposes source control-flow, parameter/input references, and plotting semantics only. It does not classify dynamics or select a scalar/modal representation."
}
out=OUT/"source_structure_v0_1.json"
out.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps(result,indent=2))
if failures:
    raise SystemExit("BIO_CHI_JARUS_SOURCE_STRUCTURE_FAIL")
print("BIO_CHI_JARUS_SOURCE_STRUCTURE_PASS")
