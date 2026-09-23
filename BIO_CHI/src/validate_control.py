#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BIO = ROOT / "BIO_CHI"

REQUIRED = [
    BIO / "README.md",
    BIO / "control" / "AUTORUN_CHECKPOINT.md",
    BIO / "control" / "WORK_QUEUE.json",
    BIO / "reviewer" / "README.md",
    BIO / "reviewer" / "MANUSCRIPT_PRIVACY_FIREWALL.md",
    BIO / "artifacts" / "DATASET_ELIGIBILITY_MATRIX_v0_1.md",
    BIO / "config" / "P0D_TESTBED_REGISTRY_v0_1.json",
]

ALLOWED_QUEUE_STATUS_PREFIXES = {
    "complete",
    "active",
    "pending",
    "not_open",
}

def fail(msg: str) -> None:
    print(f"BIO_CHI_CONTROL_FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)

for path in REQUIRED:
    if not path.exists():
        fail(f"missing required control file: {path.relative_to(ROOT)}")

with (BIO / "control" / "WORK_QUEUE.json").open(encoding="utf-8") as fh:
    queue = json.load(fh)

with (BIO / "config" / "P0D_TESTBED_REGISTRY_v0_1.json").open(encoding="utf-8") as fh:
    registry = json.load(fh)

n = queue.get("nomenclature", {})
expected = {
    "chi": "program-wide scalar stability class/symbol",
    "chi_bio": "biological scalar instance/sublabel of chi if licensed",
    "Chi_bio": "biological modal/vector representation",
    "Bio_Chi": "biological conglomerate/system stability architecture",
}
if n != expected:
    fail(f"nomenclature drift: {n!r}")

policy = queue.get("continuation_policy", {})
if policy.get("resume_from_checkpoint") is not True:
    fail("resume_from_checkpoint must remain true")
if policy.get("mechanical_blockers_are_stop_conditions") is not False:
    fail("mechanical blockers must not be stop conditions")
if policy.get("scientific_decision_required_for_stop") is not True:
    fail("scientific_decision_required_for_stop must remain true")
if policy.get("manuscript_private") is not True:
    fail("working manuscript privacy flag must remain true")

ids = []
for item in queue.get("queue", []):
    qid = item.get("id")
    status = str(item.get("status", ""))
    if not qid:
        fail("queue item missing id")
    if not any(status.startswith(prefix) for prefix in ALLOWED_QUEUE_STATUS_PREFIXES):
        fail(f"unrecognized queue status for {qid}: {status}")
    ids.append(qid)

if len(ids) != len(set(ids)):
    fail("duplicate queue ids")

testbed_ids = [x.get("id") for x in registry.get("testbeds", [])]
if None in testbed_ids or len(testbed_ids) != len(set(testbed_ids)):
    fail("testbed ids must be present and unique")

# Public-repository manuscript firewall.
for path in BIO.rglob("*"):
    if not path.is_file():
        continue
    rel = path.relative_to(BIO).as_posix().lower()
    if rel.startswith("release/approved/"):
        continue
    name = path.name.lower()
    forbidden = (
        name.endswith(".docx")
        or name.endswith(".odt")
        or (name.endswith(".tex") and ("manuscript" in name or "working" in name or "draft" in name))
        or "working_manuscript" in name
    )
    if forbidden:
        fail(f"working-manuscript-like file found in public BIO_CHI tree: {rel}")

checkpoint = (BIO / "control" / "AUTORUN_CHECKPOINT.md").read_text(encoding="utf-8")
for token in ["Mechanical continuation authority", "Scientific stop conditions", "Current execution queue"]:
    if token not in checkpoint:
        fail(f"checkpoint missing section: {token}")

print("BIO_CHI_CONTROL_PASS")
