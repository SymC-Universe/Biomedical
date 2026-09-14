from src.run_chi_bio_g2_model_comparison_calibration import run_calibration


def test_model_comparison_calibration_is_pre_outcome_only():
    result = run_calibration(replicates=4, seed=11)
    assert result["status"] == "SYNTHETIC_PRE_OUTCOME_MODEL_COMPARISON_ONLY"
    assert result["real_source_files_opened"] is False
    assert result["empirical_model_selected"] is False
    assert result["empirical_threshold_selected"] is False
    assert result["chi_bio_computed"] is False
    assert result["promotion_effect"] == "NONE"
    assert {row["rank"] for row in result["records"]} == {2, 3}


def test_calibration_contains_shared_and_reorganization_truths():
    result = run_calibration(replicates=2, seed=12)
    scenarios = {row["scenario"] for row in result["records"]}
    assert "SHARED_OPERATOR" in scenarios
    assert "REORGANIZED_STABLE" in scenarios
    assert "REORGANIZED_ABOVE_UNIT_CIRCLE" in scenarios
    assert "REORGANIZED_NONNORMAL_STABLE" in scenarios


def test_noiseless_shared_truth_d1_leave_one_out_is_identifiable_in_some_fixtures():
    result = run_calibration(replicates=8, seed=13)
    rows = [
        row
        for row in result["records"]
        if row["scenario"] == "SHARED_OPERATOR" and row["noise_sd"] == 0.0
    ]
    assert rows
    assert all(row["d1_all_loto_identifiable_fraction"] > 0.0 for row in rows)


def test_output_does_not_convert_predictive_comparison_into_model_promotion():
    result = run_calibration(replicates=2, seed=14)
    assert "selected_model" not in result
    assert "p_value" not in result
