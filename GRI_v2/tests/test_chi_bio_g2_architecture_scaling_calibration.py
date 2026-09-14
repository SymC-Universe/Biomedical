from src.run_chi_bio_g2_architecture_scaling_calibration import run_calibration


def test_architecture_scaling_calibration_is_pre_outcome_only():
    result = run_calibration(replicates=2, seed=31)
    assert result["status"] == "SYNTHETIC_PRE_OUTCOME_ARCHITECTURE_SCALING_ONLY"
    assert result["real_source_files_opened"] is False
    assert result["empirical_model_selected"] is False
    assert result["empirical_threshold_selected"] is False
    assert result["chi_bio_computed"] is False
    assert result["promotion_effect"] == "NONE"


def test_scaling_calibration_contains_both_transition_architectures_and_ranks():
    result = run_calibration(replicates=2, seed=32)
    assert {row["arm_steps"] for row in result["records"]} == {5, 10}
    assert {row["transitions_total"] for row in result["records"]} == {10, 20}
    assert {row["rank"] for row in result["records"]} == {2, 3}


def test_scaling_output_does_not_silently_select_chronic_or_short_term_winner():
    result = run_calibration(replicates=2, seed=33)
    assert "selected_architecture" not in result
    assert "selected_model" not in result
