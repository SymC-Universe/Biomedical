import json
from pathlib import Path


def test_scc25_state_reduction_registry_preserves_science_boundary():
    data = json.loads(
        Path("config/gri_Chi_bio_scc25_state_reduction_candidates_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    assert data["chi_bio_outcomes_opened"] is False
    assert data["selected_reduction_id"] is None
    ids = [x["id"] for x in data["candidates"]]
    assert len(ids) == len(set(ids)) == 6
    assert data["review_order"]["G2"][0] == "R1_CONTROL_ONLY_UNSUPERVISED"
    assert data["review_order"]["G1"][0] == "R4_MECHANISTIC_REGULON_STATE"
    assert "unity crossing" in data["selection_rule"]
