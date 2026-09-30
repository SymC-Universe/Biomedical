#!/usr/bin/env python3
"""Validate NSD fresh v0.2 prefreeze scientific-authority contracts.

Mechanical validator only. It does not adjudicate scientific outcomes.
It always binds to Draft-B and the newest versioned lane checkpoints.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTROL = ROOT / "control"


def load(name: str):
    return json.loads((CONTROL / name).read_text(encoding="utf-8"))


def latest_checkpoint(prefix: str) -> tuple[Path, dict]:
    pat = re.compile(rf"^{re.escape(prefix)}_v(\d+)\.(\d+)\.json$")
    found = []
    for path in CONTROL.glob(f"{prefix}_v*.json"):
        m = pat.match(path.name)
        if m:
            found.append(((int(m.group(1)), int(m.group(2))), path))
    if not found:
        raise SystemExit(f"no checkpoint found for {prefix}")
    _, path = max(found, key=lambda x: x[0])
    return path, json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    draft_path = CONTROL / "FRESH_UNTOUCHED_V0_2_DRAFT_B.json"
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    nb1_path, nb1 = latest_checkpoint("LANE_CHECKPOINT_NB1")
    nb23_path, nb23 = latest_checkpoint("LANE_CHECKPOINT_NB23")

    assert draft["execution_authorized"] is False
    assert draft["status"] == "PREFREEZE_DRAFT_B_PENDING_V0_5_REREVIEW_AND_PACKET_APQ"
    assert draft["exposure_firewall"]["v01_scientific_values_used_for_design"] is False

    function_generators = {x["generator"] for x in draft["nb1"]["function_truths"]}
    if "CONTINUOUS_C" not in function_generators:
        raise SystemExit("N-B1 function map lacks native continuous-C truth")

    limit_generators = {x["generator"] for x in draft["nb1"]["limit_truths"]}
    required_limits = {
        "D_NOT_C_POS", "D_NOT_C_NEG", "S_NOT_D_POS", "S_NOT_D_NEG",
        "COLORED_MEMORY", "GENUINE_TWO_MODE", "PIECEWISE_C_REORGANIZATION",
        "AR1_NONOSCILLATORY", "REFERENCE_MIXTURE_TWO_MODE",
    }
    missing = required_limits - limit_generators
    if missing:
        raise SystemExit(f"N-B1 Limit Map missing frozen classes: {sorted(missing)}")

    f_ids = {x["id"] for x in draft["nb1"]["function_truths"]}
    l_ids = {x["id"] for x in draft["nb1"]["limit_truths"]}
    if f_ids & l_ids:
        raise SystemExit("N-B1 Function/Limit identity collision")
    if len(f_ids) != len(l_ids):
        raise SystemExit("N-B1 representative/adversarial case-class balance changed")

    app = draft["nb1"]["applicability_contract"]
    for special in ("U2F8", "U2L8"):
        if special not in app or "R" not in app[special]["required"]:
            raise SystemExit(f"reference-sensitive applicability missing for {special}")

    nb = draft["nb23"]
    if "R(m1)=R(m2)" not in nb["exact_sufficiency_rule"]:
        raise SystemExit("exact sufficiency rule missing equivalence-class contract")
    if "Observation-conditioned" not in nb["recoverability_rule"]:
        raise SystemExit("recoverability firewall missing")
    S = nb["similarity_S"]
    if len(S) != 4 or any(len(row) != 4 for row in S):
        raise SystemExit("similarity transform shape mismatch")
    for key in ("autonomous", "input_driven", "observed", "time_varying"):
        if not nb["target_families"].get(key):
            raise SystemExit(f"empty N-B2/N-B3 target family: {key}")

    firewall = draft["cross_lane_firewall"]
    if firewall["confirmatory_case_identity_overlap_allowed"]:
        raise SystemExit("cross-lane case overlap unexpectedly allowed")
    if firewall["cross_lane_outcome_feedback_before_both_freezes"]:
        raise SystemExit("cross-lane feedback unexpectedly allowed")

    for cp, lane, path in ((nb1, "N-B1", nb1_path), (nb23, "N-B2/N-B3", nb23_path)):
        if cp["lane"] != lane:
            raise SystemExit(f"lane checkpoint mismatch: expected {lane}")
        if cp["state"] != "SCIENTIFIC_GATE":
            raise SystemExit(f"{lane} latest checkpoint {path.name} must remain SCIENTIFIC_GATE before APQ/freeze")
        if cp.get("completed_case_ids"):
            raise SystemExit(f"{lane} opened fresh outcomes before authorization")
        if cp.get("scientific_values_exposed"):
            raise SystemExit(f"{lane} scientific values exposed before authorization")
        if cp.get("execution_authorized"):
            raise SystemExit(f"{lane} execution authorized before packet APQ/freeze")
        if cp.get("final_identity_freeze"):
            raise SystemExit(f"{lane} final identity frozen before packet APQ closure")

    forbidden = re.compile(r"results/long_run_v0_1/(?:nb1|nb2_nb3)/.*\.json")
    for path in (draft_path, nb1_path, nb23_path):
        if forbidden.search(path.read_text(encoding="utf-8")):
            raise SystemExit(f"exposure firewall violation in {path.name}")

    if not (CONTROL / "V0_2_RESULT_LANDING_AUDIT_v0.1.md").exists():
        raise SystemExit("missing prebuilt result-landing audit")

    print(f"NSD fresh v0.2 prefreeze packet contracts PASS using {nb1_path.name} and {nb23_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
