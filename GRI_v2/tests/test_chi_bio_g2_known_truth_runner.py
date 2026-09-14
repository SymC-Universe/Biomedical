import json
from pathlib import Path

from src.run_chi_bio_g2_known_truth import run_harness


def test_frozen_g2_known_truth_harness_passes_without_real_data():
    config = json.loads(
        Path("config/gri_Chi_bio_g2_known_truth_harness_v0_1.json").read_text(
            encoding="utf-8"
        )
    )
    result = run_harness(config)

    assert result["status"] == "PASS_G2_COMPARATOR_KNOWN_TRUTH_NO_REAL_DATA"
    assert result["required_cases_pass"] is True
    assert result["real_data_used"] is False
    assert result["chi_bio_outcomes_opened"] is False
    assert result["case_results"]["INCONSISTENT_INTERVAL"]["refused"] is True
    assert result["case_results"]["SHARED_OPERATOR"][
        "consistent_exact_operator_exists"
    ] is True
    assert result["case_results"]["SHARED_OPERATOR"][
        "inconsistent_exact_operator_exists"
    ] is False
