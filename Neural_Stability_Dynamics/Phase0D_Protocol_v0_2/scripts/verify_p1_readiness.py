from __future__ import annotations
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
ready = root / "P1_READY.json"
if not ready.exists():
    print("P1 HOLD: P1_READY.json is absent. No confirmatory execution is authorized.")
    raise SystemExit(3)
obj = json.loads(ready.read_text(encoding="utf-8"))
required = ["mfr14_complete","comparator_route_frozen","uncertainty_rule_frozen","model_adequacy_rule_frozen","multiplicity_registered","evidence_independence_audited","known_bad_tests_pass","freeze_manifest_committed","untouched_design_frozen"]
missing = [k for k in required if obj.get(k) is not True]
if missing:
    print("P1 HOLD: readiness fields not satisfied:")
    for k in missing: print(k)
    raise SystemExit(3)
print("P1 READINESS RECORD COMPLETE")
