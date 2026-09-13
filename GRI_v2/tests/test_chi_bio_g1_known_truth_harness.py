import json
from pathlib import Path

from src.run_chi_bio_g1_known_truth import run_harness


def test_frozen_g1_known_truth_harness_passes_without_real_data():
    root = Path(__file__).resolve().parents[1]
    config_path = root / "config" / "gri_Chi_bio_g1_known_truth_harness_v0_1.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    result = run_harness(config)

    assert result["status"] == "PASS_EXACT_AND_FAILURE_CASES_NO_REAL_DATA"
    assert result["required_exact_cases_pass"] is True
    assert result["real_cancer_values_used"] is False
    assert result["atlas_or_unity_placement_used_for_selection"] is False
    assert result["promotion_consequence"] == (
        "CB9_SYNTHETIC_MATH_COMPONENT_SUPPORTED_ONLY; CANDIDATE_LOCK_NOT_EARNED"
    )

    noise_rows = result["case_results"]["G1_NOISE_PILOT"]
    assert len(noise_rows) == len(config["noise_and_uncertainty_pilot"]["entrywise_gaussian_sigma_grid"])
    assert all(row["replicates"] == 200 for row in noise_rows)
    assert all(row["seed"] == 20260912 for row in noise_rows)


def test_harness_keeps_naive_heterogeneous_unity_generalization_rejected():
    root = Path(__file__).resolve().parents[1]
    config = json.loads(
        (root / "config" / "gri_Chi_bio_g1_known_truth_harness_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    result = run_harness(config)

    rows = result["case_results"]["G1C_DIRECTED_HETEROGENEOUS_COUNTEREXAMPLES"]
    assert len(rows) == 2
    assert all(row["pass"] for row in rows)
    assert all(
        row["exact_unity_route"] == "NO_EXACT_UNITY_ROUTE_FROM_NAIVE_NORMALIZATION"
        for row in rows
    )
