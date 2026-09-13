import json
from pathlib import Path


def test_next_science_decision_template_authorizes_nothing_by_default():
    root = Path(__file__).resolve().parents[1]
    data = json.loads(
        (root / "config" / "gri_Chi_bio_next_science_decisions_TEMPLATE_v0_1.json").read_text(
            encoding="utf-8"
        )
    )

    assert data["status"] == "TEMPLATE_NOT_A_FREEZE"
    assert data["scientific_approval_reference"] is None
    assert data["freeze_timestamp"] is None
    assert data["chi_bio_outcomes_opened_before_freeze"] is False

    assert data["decision_A_first_G2_rank_design"]["selected_option"] is None
    assert data["decision_B_first_G1_state_basis"]["selected_option"] is None
    assert data["decision_C_G1_restoration_strategy"]["selected_option"] is None

    assert data["decision_A_first_G2_rank_design"]["distance_to_unity_used_to_select"] is False
    assert data["decision_B_first_G1_state_basis"]["scc25_or_tcga_candidate_values_used_to_select"] is False
    assert data["decision_C_G1_restoration_strategy"]["restoration_not_tuned_to_unity"] is True
