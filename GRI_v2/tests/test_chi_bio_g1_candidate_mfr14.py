import json
from pathlib import Path


def test_g1_candidate_mfr14_is_complete_for_synthetic_stage_only():
    data = json.loads(
        Path("config/gri_Chi_bio_g1_candidate_mfr14_v0_1.json").read_text(encoding="utf-8")
    )

    for i in range(1, 15):
        key_prefix = f"MFR_{i:02d}_"
        assert any(key.startswith(key_prefix) for key in data), key_prefix

    guard = data["completion_guard"]
    assert guard["complete_for_synthetic_stage"] is True
    assert guard["candidate_lock_earned"] is False
    assert guard["p1_freeze"] is False
    assert guard["real_Chi_bio_values_allowed"] is False

    assert data["MFR_12_freeze_identity_untouched_test"][
        "decisive_synthetic_evidence_unopened_at_freeze"
    ] is True
    assert data["MFR_12_freeze_identity_untouched_test"]["real_data_used"] is False
    assert data["MFR_12_freeze_identity_untouched_test"]["atlas_used"] is False
