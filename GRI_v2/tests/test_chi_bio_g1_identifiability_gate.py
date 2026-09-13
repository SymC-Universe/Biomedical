import json
from pathlib import Path


EXPECTED_STAGE_IDS = [
    "IG1_REPRESENTATION_IDENTITY",
    "IG2_PARAMETER_COUNT_AND_RANK",
    "IG3_SYNTHETIC_RECOVERY_MATCHED_GEOMETRY",
    "IG4_RESAMPLING_STABILITY",
    "IG5_NONNORMALITY_AND_COMPRESSION_LOSS",
    "IG6_LOCAL_EMBEDDED_SEPARATION",
    "IG7_G2_COMPETITOR",
    "IG8_G4_STOCHASTIC_ALTERNATIVE",
    "IG9_BOUNDARY_UNCERTAINTY",
]


def _load_gate():
    root = Path(__file__).resolve().parents[1]
    return json.loads(
        (root / "config" / "gri_Chi_bio_G1_identifiability_gate_v0_1.json").read_text(
            encoding="utf-8"
        )
    )


def test_identifiability_gate_is_preoutcome_and_complete():
    gate = _load_gate()

    assert gate["status"] == "FROZEN_PREOUTCOME_GATE_SPEC"
    assert gate["candidate_family"] == "G1_S1_L3"
    assert gate["real_cancer_Chi_bio_values_may_select_gate"] is False
    assert gate["atlas_or_unity_placement_may_select_gate"] is False
    assert [stage["id"] for stage in gate["stages"]] == EXPECTED_STAGE_IDS
    assert all(stage["question"] for stage in gate["stages"])
    assert all(stage["required_evidence"] for stage in gate["stages"])
    assert all(stage["failure"] for stage in gate["stages"])


def test_identifiability_gate_preserves_material_competitors_and_refusal():
    gate = _load_gate()
    by_id = {stage["id"]: stage for stage in gate["stages"]}

    assert by_id["IG7_G2_COMPETITOR"]["failure"] == "NARROW_G1_OR_ELEVATE_G2"
    assert by_id["IG8_G4_STOCHASTIC_ALTERNATIVE"]["failure"] == (
        "NO_SINGLE_DETERMINISTIC_CHI_OR_ELEVATE_G4"
    )
    assert by_id["IG9_BOUNDARY_UNCERTAINTY"]["failure"] == "UNCERTAINTY_SPANS_BOUNDARY"
    assert "Do not tune" in gate["failure_rule"]
