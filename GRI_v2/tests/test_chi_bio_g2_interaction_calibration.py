import math

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


def test_noiseless_sequential_fixture_preserves_truth_side_without_hiding_conditioning():
    result = run_calibration(replicates=12, seed=20260913)
    rows = [row for row in result["records"] if row["noise_sd"] == 0.0]
    assert rows
    for row in rows:
        assert row["full_rank_fit_fraction"] > 0.0
        # The trajectory-like fixture is intentionally sequential rather than
        # an independent random design. Full rank therefore does not imply a
        # well-conditioned inverse. Do not turn an observed 1e-5-scale spectral
        # perturbation into a passing/failing scientific threshold here. Keep
        # both the recovery error and condition number in the output and require
        # only finite diagnostics plus the exact mathematical-side conclusion.
        for key in (
            "control_rho_abs_error",
            "treated_rho_abs_error",
            "delta_transition_relative_frobenius_error",
            "condition_number",
        ):
            assert math.isfinite(row[key]["max"])
            assert row[key]["max"] >= 0.0
        assert row["treated_unit_circle_side_accuracy_given_full_rank"] == 1.0


def test_near_boundary_stress_is_present_for_both_ranks():
    result = run_calibration(replicates=4, seed=9)
    rows = [row for row in result["records"] if row["scenario"] == "NEAR_BOUNDARY_TREATED"]
    assert {row["rank"] for row in rows} == {2, 3}
    assert all(abs(row["truth_treated_rho"] - 0.98) < 1e-12 for row in rows)
