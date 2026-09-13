import json
from pathlib import Path

import pytest

from src.chi_bio_empirical_freeze_contract import EmpiricalFreezeContractError
from src.preflight_chi_bio_first_empirical_g2 import run_preflight, validate_source_manifests


TEMPLATE = Path("config/gri_Chi_bio_first_empirical_g2_r1_freeze_TEMPLATE_v0_1.json")


def _valid_freeze(tmp_path: Path) -> Path:
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    data.update(
        {
            "status": "TEST_VALIDATED_ONLY",
            "freeze_id": "TEST_VALID_FREEZE",
            "scientific_approval_reference": "unit-test fixture only",
            "freeze_timestamp": "2099-01-01T00:00:00Z",
            "frozen_before_real_candidate_values": True,
            "primary_rank": 2,
            "sensitivity_ranks": [3],
            "normalization_rule": "test fixture",
            "feature_universe_rule": "test fixture",
            "day0_initialization_rule": "test fixture",
            "conditioning_refusal_rule": "test fixture",
            "model_adequacy_refusal_rule": "test fixture",
            "uncertainty_rule": "test fixture",
            "transport_rule": "test fixture",
        }
    )
    path = tmp_path / "freeze.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_incomplete_template_refuses_before_source_open():
    with pytest.raises(EmpiricalFreezeContractError):
        run_preflight(TEMPLATE, source_root=Path("THIS_PATH_MUST_NEVER_BE_TOUCHED"))


def test_frozen_source_manifests_pass_against_repeated_machine_provenance():
    result = validate_source_manifests()
    assert result["status"] == "PASS_FROZEN_SOURCE_MANIFESTS_AND_PROVENANCE_LOCK"
    assert result["real_molecular_files_opened"] is False
    assert result["short_term_scc25_states"] == 11
    assert result["chronic_main_scc25_states"] == 22
    assert result["chronic_source_container_samples"] == 36
    assert result["chronic_source_projection_sha256"] == "fa8772da77054785ff2fb384d336ff6821ed32e65172708a92a975ba1321e70b"


def test_valid_freeze_can_pass_manifest_only_preflight_without_analysis(tmp_path):
    result = run_preflight(_valid_freeze(tmp_path))
    assert result["status"] == "PASS_EMPIRICAL_EXECUTION_PREFLIGHT_NO_ANALYSIS_RUN"
    assert result["state_reduction_run"] is False
    assert result["transition_model_fit"] is False
    assert result["chi_bio_value_computed"] is False
    assert result["local_source_validation"] is None


def test_local_source_validation_only_occurs_after_freeze_and_fails_missing_files(tmp_path):
    freeze = _valid_freeze(tmp_path)
    empty_source_root = tmp_path / "sources"
    empty_source_root.mkdir()
    with pytest.raises(RuntimeError, match="missing or hash-mismatched"):
        run_preflight(freeze, source_root=empty_source_root)
