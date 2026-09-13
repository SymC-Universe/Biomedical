import pytest

from src.chi_bio_contract import ChiBioContractError, validate_chi_bio_record


REFUSALS = [
    "NO_COHERENT_CHI_BIO",
    "NOT_IDENTIFIABLE",
    "OUT_OF_VALIDITY_REGIME",
    "UNCERTAINTY_SPANS_BOUNDARY",
    "REPRESENTATION_DEPENDENT_NO_TRANSFER",
    "INSUFFICIENT_TEMPORAL_INFORMATION_FOR_DYNAMIC_INTERPRETATION",
]


def base_record():
    return {
        "notation": "Chi_bio",
        "candidate_id": "control",
        "promotion_state": "NOT_ADMITTED",
        "passed_gates": [],
        "formula_or_mapping": None,
        "direct_alias_of": None,
        "construction_used_atlas_positions": False,
        "construction_used_downstream_outcome": False,
        "formula_selected_by_closeness_to_one": False,
        "posthoc_rescaling_created_unity": False,
        "disagreeing_cancers_or_modes_suppressed": False,
        "scalar_view": {"status": "AVAILABLE", "inputs": []},
        "modal_vector_view": {"status": "AVAILABLE", "inputs": []},
        "conglomerate_system_view": {"status": "AVAILABLE", "inputs": []},
        "uncertainty": {"status": "UNRESOLVED"},
        "refusal": {"supported_states": REFUSALS},
        "Chi_bio_value": None,
        "unity_boundary_status": "NOT_TESTED",
        "biological_regime_label": None,
        "external_p1_freeze_id": None,
        "decisive_external_evidence_unopened_at_freeze": None,
        "unity_basis": None,
        "independent_boundary_test_id": None,
    }


def test_control_record_passes():
    validate_chi_bio_record(base_record())


def test_direct_h2_alias_fails():
    r = base_record()
    r["direct_alias_of"] = "H2"
    with pytest.raises(ChiBioContractError):
        validate_chi_bio_record(r)


def test_posthoc_unity_fails():
    r = base_record()
    r["posthoc_rescaling_created_unity"] = True
    with pytest.raises(ChiBioContractError):
        validate_chi_bio_record(r)


def test_value_before_qualification_fails():
    r = base_record()
    r["Chi_bio_value"] = 1.02
    with pytest.raises(ChiBioContractError):
        validate_chi_bio_record(r)


def test_candidate_lock_requires_all_nine_gates():
    r = base_record()
    r["promotion_state"] = "CANDIDATE_LOCKED"
    r["formula_or_mapping"] = "frozen mapping"
    r["passed_gates"] = [f"CB{i}" for i in range(1, 9)]
    with pytest.raises(ChiBioContractError):
        validate_chi_bio_record(r)


def test_candidate_lock_passes_with_cb1_through_cb9():
    r = base_record()
    r["promotion_state"] = "CANDIDATE_LOCKED"
    r["formula_or_mapping"] = "frozen mapping"
    r["passed_gates"] = [f"CB{i}" for i in range(1, 10)]
    validate_chi_bio_record(r)


def test_unity_admission_requires_final_state():
    r = base_record()
    r["promotion_state"] = "INTERNALLY_QUALIFIED_P0Q"
    r["formula_or_mapping"] = "frozen mapping"
    r["passed_gates"] = [f"CB{i}" for i in range(1, 12)]
    r["unity_boundary_status"] = "ADMITTED"
    with pytest.raises(ChiBioContractError):
        validate_chi_bio_record(r)
