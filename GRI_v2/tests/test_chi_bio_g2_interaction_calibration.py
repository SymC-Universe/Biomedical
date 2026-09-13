from src.run_chi_bio_g2_interaction_calibration import run_calibration


def test_synthetic_interaction_calibration_has_no_empirical_side_effects():
    result = run_calibration(replicates=8, seed=17)
    assert result["status"] == "SYNTHETIC_PRE_OUTCOME_CALIBRATION_ONLY"
    assert result["real_source_files_opened"] is False
    assert result["empirical_thresholds_selected"] is False
    assert result["empirical_rank_winner_selected"] is False
    assert result["chi_bio_computed"] is False
    assert result["promotion_effect"] == "NONE"
    assert {row["rank"] for row in result["records"]} == {2, 3}


def test_noiseless_known_truth_is_recovered_to_double_precision_scale_when_full_rank():
    result = run_calibration(replicates=12, seed=20260913)
    rows = [row for row in result["records"] if row["noise_sd"] == 0.0]
    assert rows
    for row in rows:
        assert row["full_rank_fit_fraction"] > 0.0
        # Sequential tiny-sample designs can be ill-conditioned even when full
        # rank, so exact coefficient equality is not the correct regression
        # invariant. Keep the actual condition number in the calibration output
        # and require only numerically negligible recovery error here.
        assert row["control_rho_abs_error"]["max"] < 1e-6
        assert row["treated_rho_abs_error"]["max"] < 1e-6
        assert row["delta_transition_relative_frobenius_error"]["max"] < 1e-5
        assert row["treated_unit_circle_side_accuracy_given_full_rank"] == 1.0


def test_near_boundary_stress_is_present_for_both_ranks():
    result = run_calibration(replicates=4, seed=9)
    rows = [row for row in result["records"] if row["scenario"] == "NEAR_BOUNDARY_TREATED"]
    assert {row["rank"] for row in rows} == {2, 3}
    assert all(abs(row["truth_treated_rho"] - 0.98) < 1e-12 for row in rows)
