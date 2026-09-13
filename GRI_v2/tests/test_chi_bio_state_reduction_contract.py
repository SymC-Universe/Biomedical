import pytest

from src.chi_bio_state_reduction_contract import (
    StateReductionContractError,
    validate_state_reduction_record,
)


def base_record():
    return {
        "reduction_id": "control_basis_v0",
        "method_class": "CONTROL_ONLY_UNSUPERVISED_BASIS",
        "state_dimension": 4,
        "formal_rank_ceiling": 9,
        "basis_fit_source_role": "PBS_CONTROL_ONLY",
        "dimension_rule": "frozen before Chi; example only",
        "transport_rule": "fit on control source role then project treated states without refitting",
        "failure_or_refusal_rule": "refuse if representation is unstable or nontransportable",
        "dimension_selected_after_chi_outcomes": False,
        "basis_selected_after_chi_outcomes": False,
        "uses_proliferation_to_fit_or_select": False,
        "uses_resistant_clones_to_fit_or_select": False,
        "selection_signals": ["RNA_MEASUREMENT_GEOMETRY"],
        "frozen_before_real_chi_values": True,
        "external_basis_identity": None,
        "module_definition_identity": None,
    }


def test_valid_control_only_reduction_record_passes():
    validate_state_reduction_record(base_record())


def test_dimension_above_rank_ceiling_fails():
    r = base_record()
    r["state_dimension"] = 10
    with pytest.raises(StateReductionContractError, match="exceeds"):
        validate_state_reduction_record(r)


def test_proliferation_selected_basis_fails():
    r = base_record()
    r["uses_proliferation_to_fit_or_select"] = True
    with pytest.raises(StateReductionContractError, match="proliferation"):
        validate_state_reduction_record(r)


def test_unity_selected_dimension_fails():
    r = base_record()
    r["selection_signals"] = ["DISTANCE_TO_UNITY"]
    with pytest.raises(StateReductionContractError, match="DISTANCE_TO_UNITY"):
        validate_state_reduction_record(r)


def test_control_only_basis_must_really_fit_control_only():
    r = base_record()
    r["basis_fit_source_role"] = "BOTH_ARMS"
    with pytest.raises(StateReductionContractError, match="PBS_CONTROL_ONLY"):
        validate_state_reduction_record(r)


def test_external_basis_requires_identity():
    r = base_record()
    r["method_class"] = "EXTERNAL_FIXED_BASIS"
    r["basis_fit_source_role"] = "EXTERNAL_REFERENCE"
    with pytest.raises(StateReductionContractError, match="external_basis_identity"):
        validate_state_reduction_record(r)


def test_predeclared_modules_require_definition_identity():
    r = base_record()
    r["method_class"] = "PREDECLARED_BIOLOGICAL_MODULES"
    r["basis_fit_source_role"] = "NO_DATA_FIT"
    with pytest.raises(StateReductionContractError, match="module_definition_identity"):
        validate_state_reduction_record(r)


def test_unfrozen_reduction_fails():
    r = base_record()
    r["frozen_before_real_chi_values"] = False
    with pytest.raises(StateReductionContractError, match="frozen before real"):
        validate_state_reduction_record(r)
