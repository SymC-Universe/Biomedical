from __future__ import annotations

"""Validation contract for the next GRI Chi_bio science freeze.

The template can exist indefinitely without authorization. A record becomes an
execution-bearing freeze only after A/B/C are explicitly selected and all
required prospective details are present. This contract never chooses among the
scientific options.
"""

from collections.abc import Mapping
from typing import Any


class NextScienceDecisionContractError(ValueError):
    pass


A_OPTIONS = frozenset(
    {
        "A1_PRIMARY_R2_SENSITIVITY_R3",
        "A2_PRIMARY_R3_SENSITIVITY_R2",
        "A3_ROBUSTNESS_REQUIRED_R2_R3",
        "A4_OTHER_PROSPECTIVELY_JUSTIFIED",
    }
)
B_OPTIONS = frozenset(
    {
        "B1_FIXED_SIGNED_REGULON_TF_ACTIVITY",
        "B2_FIXED_MODULE_EXPRESSION",
        "B3_EXTERNALLY_SOURCED_REGULON_LOW_DIMENSION_HYBRID",
        "B4_OTHER_PROSPECTIVELY_JUSTIFIED",
    }
)
C_OPTIONS = frozenset(
    {
        "C1_EFFECTIVE_COMMON_RESTORATION_WITH_INDEPENDENT_SUPPORT",
        "C2_STATE_SPECIFIC_RESTORATION_WITH_SEPARATE_EXACT_NORMALIZATION",
        "C3_WITHHOLD_NORMALIZED_G1_UNTIL_RESTORATION_RESOLVED",
        "C4_OTHER_PROSPECTIVELY_JUSTIFIED",
    }
)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise NextScienceDecisionContractError(f"{name} must be a mapping")
    return value


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_false(record: Mapping[str, Any], key: str) -> None:
    if record.get(key) is not False:
        raise NextScienceDecisionContractError(f"{key} must be explicitly false")


def validate_next_science_freeze(record: Mapping[str, Any]) -> None:
    if not isinstance(record, Mapping):
        raise NextScienceDecisionContractError("record must be a mapping")
    if record.get("status") != "FROZEN_SCIENTIFIC_DECISIONS":
        raise NextScienceDecisionContractError(
            "status must be FROZEN_SCIENTIFIC_DECISIONS; templates are not executable"
        )
    if not _nonempty(record.get("scientific_approval_reference")):
        raise NextScienceDecisionContractError("scientific_approval_reference is required")
    if not _nonempty(record.get("freeze_timestamp")):
        raise NextScienceDecisionContractError("freeze_timestamp is required")
    _require_false(record, "chi_bio_outcomes_opened_before_freeze")

    a = _mapping(record.get("decision_A_first_G2_rank_design"), "decision_A_first_G2_rank_design")
    b = _mapping(record.get("decision_B_first_G1_state_basis"), "decision_B_first_G1_state_basis")
    c = _mapping(record.get("decision_C_G1_restoration_strategy"), "decision_C_G1_restoration_strategy")

    a_opt = a.get("selected_option")
    if a_opt not in A_OPTIONS:
        raise NextScienceDecisionContractError(f"invalid A selected_option: {a_opt!r}")
    _require_false(a, "treated_states_used_to_select")
    _require_false(a, "proliferation_used_to_select")
    _require_false(a, "distance_to_unity_used_to_select")

    if a_opt == "A1_PRIMARY_R2_SENSITIVITY_R3":
        if a.get("primary_rank") != 2 or a.get("sensitivity_rank") != 3:
            raise NextScienceDecisionContractError("A1 requires primary_rank=2 and sensitivity_rank=3")
    elif a_opt == "A2_PRIMARY_R3_SENSITIVITY_R2":
        if a.get("primary_rank") != 3 or a.get("sensitivity_rank") != 2:
            raise NextScienceDecisionContractError("A2 requires primary_rank=3 and sensitivity_rank=2")
    elif a_opt == "A3_ROBUSTNESS_REQUIRED_R2_R3":
        if not _nonempty(a.get("robustness_rule")):
            raise NextScienceDecisionContractError("A3 requires a frozen robustness_rule")
        if a.get("primary_rank") is not None or a.get("sensitivity_rank") is not None:
            raise NextScienceDecisionContractError("A3 must not designate a primary or sensitivity winner")
    else:
        if not _nonempty(a.get("robustness_rule")):
            raise NextScienceDecisionContractError("A4 requires a prospectively justified custom rule")

    b_opt = b.get("selected_option")
    if b_opt not in B_OPTIONS:
        raise NextScienceDecisionContractError(f"invalid B selected_option: {b_opt!r}")
    _require_false(b, "scc25_or_tcga_candidate_values_used_to_select")
    for key in (
        "source_identity_and_version",
        "state_coordinate_semantics",
        "subset_or_dimension_rule",
        "transport_rule",
    ):
        if not _nonempty(b.get(key)):
            raise NextScienceDecisionContractError(f"B requires {key}")
    if b_opt == "B3_EXTERNALLY_SOURCED_REGULON_LOW_DIMENSION_HYBRID" and not _nonempty(
        b.get("representation_sensitivity_source")
    ):
        raise NextScienceDecisionContractError(
            "B3 requires an independent representation_sensitivity_source"
        )

    c_opt = c.get("selected_option")
    if c_opt not in C_OPTIONS:
        raise NextScienceDecisionContractError(f"invalid C selected_option: {c_opt!r}")
    if c.get("restoration_not_tuned_to_unity") is not True:
        raise NextScienceDecisionContractError("restoration_not_tuned_to_unity must be true")

    if c_opt in {
        "C1_EFFECTIVE_COMMON_RESTORATION_WITH_INDEPENDENT_SUPPORT",
        "C2_STATE_SPECIFIC_RESTORATION_WITH_SEPARATE_EXACT_NORMALIZATION",
    }:
        if not _nonempty(c.get("independent_restoration_source_or_experiment")):
            raise NextScienceDecisionContractError(
                "C1/C2 require an independent restoration source or experiment"
            )
        if not _nonempty(c.get("normalization_derivation_id")):
            raise NextScienceDecisionContractError("C1/C2 require normalization_derivation_id")
    elif c_opt == "C3_WITHHOLD_NORMALIZED_G1_UNTIL_RESTORATION_RESOLVED":
        if c.get("normalization_derivation_id") not in (None, ""):
            raise NextScienceDecisionContractError(
                "C3 must not smuggle in a normalization derivation"
            )
    else:
        if not _nonempty(c.get("normalization_derivation_id")):
            raise NextScienceDecisionContractError("C4 requires a prospectively justified derivation id")


def template_is_nonexecuting(record: Mapping[str, Any]) -> bool:
    """Return True only for the intentionally unset non-authorizing template."""
    if not isinstance(record, Mapping) or record.get("status") != "TEMPLATE_NOT_A_FREEZE":
        return False
    try:
        a = _mapping(record.get("decision_A_first_G2_rank_design"), "A")
        b = _mapping(record.get("decision_B_first_G1_state_basis"), "B")
        c = _mapping(record.get("decision_C_G1_restoration_strategy"), "C")
    except NextScienceDecisionContractError:
        return False
    return (
        record.get("scientific_approval_reference") is None
        and record.get("freeze_timestamp") is None
        and a.get("selected_option") is None
        and b.get("selected_option") is None
        and c.get("selected_option") is None
    )
