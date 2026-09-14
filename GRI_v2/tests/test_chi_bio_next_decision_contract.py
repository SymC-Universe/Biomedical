import json
from pathlib import Path

import pytest

from src.chi_bio_next_decision_contract import (
    NextScienceDecisionContractError,
    template_is_nonexecuting,
    validate_next_science_freeze,
)


def _template():
    root = Path(__file__).resolve().parents[1]
    return json.loads(
        (root / "config" / "gri_Chi_bio_next_science_decisions_TEMPLATE_v0_1.json").read_text(
            encoding="utf-8"
        )
    )


def _approved_base():
    record = _template()
    record["status"] = "FROZEN_SCIENTIFIC_DECISIONS"
    record["scientific_approval_reference"] = "TEST_ONLY_EXPLICIT_APPROVAL"
    record["freeze_timestamp"] = "2099-01-01T00:00:00Z"
    return record


def test_template_is_explicitly_nonexecuting():
    record = _template()
    assert template_is_nonexecuting(record) is True
    with pytest.raises(NextScienceDecisionContractError, match="templates are not executable"):
        validate_next_science_freeze(record)


def test_valid_a3_b3_c3_freeze_passes_without_assigning_g1_value():
    record = _approved_base()
    a = record["decision_A_first_G2_rank_design"]
    a.update(
        {
            "selected_option": "A3_ROBUSTNESS_REQUIRED_R2_R3",
            "primary_rank": None,
            "sensitivity_rank": None,
            "robustness_rule": "Material conclusions must agree across r=2 and r=3 or refuse transfer.",
        }
    )
    b = record["decision_B_first_G1_state_basis"]
    b.update(
        {
            "selected_option": "B3_EXTERNALLY_SOURCED_REGULON_LOW_DIMENSION_HYBRID",
            "source_identity_and_version": "TEST_FIXED_SIGNED_REGULON_SOURCE",
            "state_coordinate_semantics": "fixed regulator activity coordinates",
            "subset_or_dimension_rule": "TEST_OUTCOME_BLIND_RULE",
            "transport_rule": "same frozen coordinates across sources or refuse",
            "representation_sensitivity_source": "TEST_INDEPENDENT_COMPARATOR",
        }
    )
    c = record["decision_C_G1_restoration_strategy"]
    c.update(
        {
            "selected_option": "C3_WITHHOLD_NORMALIZED_G1_UNTIL_RESTORATION_RESOLVED",
            "normalization_derivation_id": None,
        }
    )
    validate_next_science_freeze(record)


def test_a1_and_a2_rank_roles_cannot_be_swapped_after_selection():
    for option, primary, sensitivity in (
        ("A1_PRIMARY_R2_SENSITIVITY_R3", 3, 2),
        ("A2_PRIMARY_R3_SENSITIVITY_R2", 2, 3),
    ):
        record = _approved_base()
        record["decision_A_first_G2_rank_design"].update(
            {"selected_option": option, "primary_rank": primary, "sensitivity_rank": sensitivity}
        )
        record["decision_B_first_G1_state_basis"].update(
            {
                "selected_option": "B1_FIXED_SIGNED_REGULON_TF_ACTIVITY",
                "source_identity_and_version": "TEST",
                "state_coordinate_semantics": "TEST",
                "subset_or_dimension_rule": "TEST",
                "transport_rule": "TEST",
            }
        )
        record["decision_C_G1_restoration_strategy"].update(
            {"selected_option": "C3_WITHHOLD_NORMALIZED_G1_UNTIL_RESTORATION_RESOLVED"}
        )
        with pytest.raises(NextScienceDecisionContractError):
            validate_next_science_freeze(record)


def test_c1_cannot_proceed_without_independent_restoration_support():
    record = _approved_base()
    record["decision_A_first_G2_rank_design"].update(
        {"selected_option": "A1_PRIMARY_R2_SENSITIVITY_R3", "primary_rank": 2, "sensitivity_rank": 3}
    )
    record["decision_B_first_G1_state_basis"].update(
        {
            "selected_option": "B1_FIXED_SIGNED_REGULON_TF_ACTIVITY",
            "source_identity_and_version": "TEST",
            "state_coordinate_semantics": "TEST",
            "subset_or_dimension_rule": "TEST",
            "transport_rule": "TEST",
        }
    )
    record["decision_C_G1_restoration_strategy"].update(
        {
            "selected_option": "C1_EFFECTIVE_COMMON_RESTORATION_WITH_INDEPENDENT_SUPPORT",
            "independent_restoration_source_or_experiment": None,
            "normalization_derivation_id": None,
        }
    )
    with pytest.raises(NextScienceDecisionContractError, match="independent restoration"):
        validate_next_science_freeze(record)


def test_forbidden_postoutcome_flags_fail():
    record = _approved_base()
    record["decision_A_first_G2_rank_design"].update(
        {"selected_option": "A1_PRIMARY_R2_SENSITIVITY_R3", "primary_rank": 2, "sensitivity_rank": 3, "distance_to_unity_used_to_select": True}
    )
    with pytest.raises(NextScienceDecisionContractError, match="must be explicitly false"):
        validate_next_science_freeze(record)
