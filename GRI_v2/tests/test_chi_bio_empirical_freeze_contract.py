import pytest

from src.chi_bio_empirical_freeze_contract import (
    EmpiricalFreezeContractError,
    validate_empirical_freeze,
)


REFUSALS = [
    "REFUSE_RANK_DEFICIENT_DESIGN",
    "REFUSE_ILL_CONDITIONED_DESIGN",
    "REFUSE_UNSTABLE_OR_NONTRANSPORTABLE_BASIS",
    "REFUSE_SOURCE_IDENTITY_MISMATCH",
    "REFUSE_UNCERTAINTY_SPANS_BOUNDARY",
    "REFUSE_REPRESENTATION_DEPENDENT_NO_TRANSFER",
]


def base_record():
    return {
        "freeze_id": "TEST_FREEZE",
        "scientific_approval_reference": "explicit-user-review-placeholder",
        "freeze_timestamp": "2099-01-01T00:00:00Z",
        "chi_bio_outcomes_opened_before_freeze": False,
        "frozen_before_real_candidate_values": True,
        "primary_reduction_id": "R1_CONTROL_ONLY_UNSUPERVISED",
        "rank_design": "PRIMARY_PLUS_SENSITIVITY",
        "primary_rank": 2,
        "sensitivity_ranks": [3],
        "basis_scope": "PBS_CONTROL_ONLY_PER_SOURCE",
        "basis_fit_uses_treated_states": False,
        "primary_transition_model": "SHARED_T_PLUS_TREATMENT_INPUT_PLUS_INTERCEPT",
        "normalization_rule": "frozen placeholder",
        "feature_universe_rule": "frozen placeholder",
        "day0_initialization_rule": "frozen placeholder",
        "conditioning_refusal_rule": "frozen placeholder",
        "model_adequacy_refusal_rule": "frozen placeholder",
        "uncertainty_rule": "frozen placeholder",
        "transport_rule": "frozen placeholder",
        "selection_inputs": ["PBS_CONTROL_RNA_ONLY"],
        "supported_refusals": REFUSALS,
        "proliferation_reserved_for_postconstruction_test": True,
        "atac_reserved_for_postconstruction_relational_test": True,
        "scrna_reserved_for_postconstruction_carrier_test": True,
        "biological_unity_boundary_admitted": False,
    }


def a3_record():
    r = base_record()
    r["rank_design"] = "A3_ROBUSTNESS_REQUIRED_R2_R3"
    r["primary_rank"] = None
    r["sensitivity_ranks"] = []
    r["robustness_ranks"] = [2, 3]
    r["rank_robustness_rule"] = (
        "Evaluate all frozen material conclusions under r=2 and r=3; disagreement returns "
        "REPRESENTATION_DEPENDENT_NO_TRANSFER."
    )
    r["material_conclusion_schema"] = "frozen outcome-independent conclusion schema placeholder"
    return r


def test_complete_prospective_empirical_freeze_record_passes():
    validate_empirical_freeze(base_record())


def test_complete_a3_empirical_freeze_record_passes():
    validate_empirical_freeze(a3_record())


def test_missing_science_approval_fails():
    r = base_record()
    r["scientific_approval_reference"] = ""
    with pytest.raises(EmpiricalFreezeContractError, match="scientific_approval_reference"):
        validate_empirical_freeze(r)


def test_rank_must_be_prospectively_frozen_to_allowed_pilot_rank():
    r = base_record()
    r["primary_rank"] = 4
    with pytest.raises(EmpiricalFreezeContractError, match="2 or 3"):
        validate_empirical_freeze(r)


def test_primary_rank_cannot_double_as_sensitivity_rank():
    r = base_record()
    r["sensitivity_ranks"] = [2, 3]
    with pytest.raises(EmpiricalFreezeContractError, match="also be listed"):
        validate_empirical_freeze(r)


def test_a3_cannot_privilege_primary_rank():
    r = a3_record()
    r["primary_rank"] = 2
    with pytest.raises(EmpiricalFreezeContractError, match="may not designate"):
        validate_empirical_freeze(r)


def test_a3_requires_both_ranks_in_fixed_order():
    r = a3_record()
    r["robustness_ranks"] = [3, 2]
    with pytest.raises(EmpiricalFreezeContractError, match="robustness_ranks"):
        validate_empirical_freeze(r)


def test_a3_requires_material_conclusion_schema():
    r = a3_record()
    r["material_conclusion_schema"] = ""
    with pytest.raises(EmpiricalFreezeContractError, match="material_conclusion_schema"):
        validate_empirical_freeze(r)


def test_control_only_basis_cannot_use_treated_states():
    r = base_record()
    r["basis_fit_uses_treated_states"] = True
    with pytest.raises(EmpiricalFreezeContractError, match="exclude treated"):
        validate_empirical_freeze(r)


def test_unity_selected_design_fails():
    r = base_record()
    r["selection_inputs"] = ["DISTANCE_TO_UNITY"]
    with pytest.raises(EmpiricalFreezeContractError, match="DISTANCE_TO_UNITY"):
        validate_empirical_freeze(r)


def test_missing_refusal_fails():
    r = base_record()
    r["supported_refusals"] = REFUSALS[:-1]
    with pytest.raises(EmpiricalFreezeContractError, match="REFUSE_REPRESENTATION_DEPENDENT_NO_TRANSFER"):
        validate_empirical_freeze(r)


def test_cross_modal_and_phenotype_endpoints_must_remain_reserved():
    for key in (
        "proliferation_reserved_for_postconstruction_test",
        "atac_reserved_for_postconstruction_relational_test",
        "scrna_reserved_for_postconstruction_carrier_test",
    ):
        r = base_record()
        r[key] = False
        with pytest.raises(EmpiricalFreezeContractError):
            validate_empirical_freeze(r)


def test_biological_unity_cannot_be_pre_admitted():
    r = base_record()
    r["biological_unity_boundary_admitted"] = True
    with pytest.raises(EmpiricalFreezeContractError, match="unadmitted"):
        validate_empirical_freeze(r)
