#!/usr/bin/env python3
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
C=ROOT/"control"

def load(name):
    return json.loads((C/name).read_text())

def latest(prefix):
    found=[]
    rx=re.compile(rf"^{prefix}_v(\d+)\.(\d+)\.json$")
    for p in C.glob(f"{prefix}_v*.json"):
        m=rx.match(p.name)
        if m: found.append(((int(m.group(1)),int(m.group(2))),p))
    _,p=max(found,key=lambda x:x[0])
    return p,json.loads(p.read_text())

freeze=load("V0_2_FINAL_SCIENTIFIC_FREEZE_v0.1.json")
if freeze["execution_authorized"] or freeze["scientific_outcomes_opened"]:
    raise SystemExit("freeze authority violation")
for lane in ("nb1","nb23","integrated"):
    if freeze["apq_closure"][lane]["unresolved_blocker_material"] != 0:
        raise SystemExit(f"unresolved APQ in {lane}")

p1,c1=latest("LANE_CHECKPOINT_NB1")
p2,c2=latest("LANE_CHECKPOINT_NB23")
for cp,name in ((c1,"N-B1"),(c2,"N-B2/N-B3")):
    if cp["lane"] != name or cp["state"] not in {"SCIENTIFIC_GATE","ADVANCED_CHECKPOINT","EXTERNAL_BLOCK","USER_ACTION_REQUIRED"}:
        raise SystemExit(f"bad latest lane checkpoint {name}")
    if not cp["final_identity_freeze"]:
        raise SystemExit(f"{name} does not bind final scientific freeze")
    if cp["execution_authorized"] or cp["scientific_values_exposed"] or cp["completed_case_ids"]:
        raise SystemExit(f"{name} opened execution/outcomes before preflight")

print(f"NSD v0.2 post-freeze authority PASS using {p1.name} and {p2.name}")
