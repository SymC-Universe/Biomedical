import json
from pathlib import Path

from src.run_chi_bio_g1_known_truth import run_harness


def test_frozen_g1_known_truth_harness_passes_exact_cases():
    cfg = json.loads(
        Path("config/gri_Chi_bio_g1_known_truth_harness_v0_1.json").read_text(encoding="utf-8")
    )
    result = run_harness(cfg)

    assert result["status"] == "PASS_EXACT_AND_FAILURE_CASES_NO_REAL_DATA"
    assert result["required_exact_cases_pass"] is True
    assert result["real_cancer_values_used"] is False
    assert result["atlas_or_unity_placement_used_for_selection"] is False
    assert result["promotion_consequence"] == (
        "CB9_SYNTHETIC_MATH_COMPONENT_SUPPORTED_ONLY; CANDIDATE_LOCK_NOT_EARNED"
    )

    false_safe, false_unsafe = result["case_results"][
        "G1C_DIRECTED_HETEROGENEOUS_COUNTEREXAMPLES"
    ]
    assert false_safe["pass"] is True
    assert false_unsafe["pass"] is True
