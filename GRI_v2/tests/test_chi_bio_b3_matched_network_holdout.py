from __future__ import annotations

import json
from pathlib import Path

from src.run_chi_bio_b3_matched_network_holdout import _validate_config


def test_b3_holdout_freeze_is_real_data_closed_and_unseen_seeded() -> None:
    config = json.loads(
        Path("config/gri_Chi_bio_B3_matched_network_holdout_20260913_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    _validate_config(config)
    assert config["pilot_seed_reused"] is False
    assert config["real_expression_opened_before_holdout"] is False
    assert config["real_tf_activity_scored_before_holdout"] is False
    assert config["normalized_g1_authorized"] is False
    assert config["candidate_dimensions"] == [2, 3, 4, 5]


def test_b3_holdout_requires_cross_network_state_and_dynamic_recovery() -> None:
    config = json.loads(
        Path("config/gri_Chi_bio_B3_matched_network_holdout_20260913_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    gate = config["primary_noise_pass_gate_per_seed_per_network"]
    assert config["network_representations"] == [
        "COLLECTRI_PRIMARY",
        "DOROTHEA_ABC_SENSITIVITY",
    ]
    assert gate["latent_subspace_maximum_principal_angle_degrees_max"] == 45.0
    assert gate["transition_relative_rho_error_max"] == 0.10
    assert gate["transition_loto_must_strictly_beat_persistence_baseline"] is True
    assert (
        gate["transition_loto_must_strictly_beat_arm_specific_loto_mean_next_state_baseline"]
        is True
    )
