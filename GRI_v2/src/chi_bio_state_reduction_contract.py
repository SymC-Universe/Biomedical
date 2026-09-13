from __future__ import annotations

"""Pre-outcome contract for Chi_bio empirical state reductions.

A reduction can be scientifically proposed without being admitted. This module
prevents a future SCC25/TCGA adapter from silently choosing its dimension or
basis using Chi_bio placement, unity crossing, proliferation/resistance labels,
or other downstream outcomes.
"""

from collections.abc import Mapping
from typing import Any


class StateReductionContractError(ValueError):
    pass


ALLOWED_METHOD_CLASSES = frozenset(
    {
        "EXTERNAL_FIXED_BASIS",
        "PREDECLARED_BIOLOGICAL_MODULES",
        "CONTROL_ONLY_UNSUPERVISED_BASIS",
        "OUTCOME_BLIND_UNSUPERVISED_BASIS",
        "MECHANISTIC_FIXED_BASIS",
    }
)

FORBIDDEN_SELECTION_SIGNALS = frozenset(
    {
        "CHI_BIO_VALUE",
        "DISTANCE_TO_UNITY",
        "UNITY_CROSSING_WEEK",
        "PROLIFERATION_RESPONSE",
        "RESISTANT_CLONE_LABEL",
        "SURVIVAL_OR_CLINICAL_OUTCOME",
        "ATLAS_PLACEMENT",
        "FAVORED_CANCER_ORDERING",
    }
)


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_state_reduction_record(record: Mapping[str, Any]) -> None:
    if not isinstance(record, Mapping):
        raise StateReductionContractError("record must be a mapping")

    if not _nonempty(record.get("reduction_id")):
        raise StateReductionContractError("reduction_id is required")

    method_class = record.get("method_class")
    if method_class not in ALLOWED_METHOD_CLASSES:
        raise StateReductionContractError(f"invalid method_class: {method_class!r}")

    dimension = record.get("state_dimension")
    if not isinstance(dimension, int) or isinstance(dimension, bool) or dimension <= 0:
        raise StateReductionContractError("state_dimension must be a positive integer")

    ceiling = record.get("formal_rank_ceiling")
    if ceiling is not None:
        if not isinstance(ceiling, int) or isinstance(ceiling, bool) or ceiling <= 0:
            raise StateReductionContractError("formal_rank_ceiling must be a positive integer or null")
        if dimension > ceiling:
            raise StateReductionContractError("state_dimension exceeds the declared formal rank ceiling")

    if record.get("dimension_selected_after_chi_outcomes") is True:
        raise StateReductionContractError("dimension may not be selected after Chi_bio outcomes")
    if record.get("basis_selected_after_chi_outcomes") is True:
        raise StateReductionContractError("basis may not be selected after Chi_bio outcomes")
    if record.get("uses_proliferation_to_fit_or_select") is True:
        raise StateReductionContractError("proliferation may not fit/select the state reduction")
    if record.get("uses_resistant_clones_to_fit_or_select") is True:
        raise StateReductionContractError("stable resistant clones may not fit/select the main trajectory reduction")

    signals = frozenset(str(x) for x in record.get("selection_signals", []))
    forbidden = signals & FORBIDDEN_SELECTION_SIGNALS
    if forbidden:
        raise StateReductionContractError(
            "forbidden selection signal(s): " + ", ".join(sorted(forbidden))
        )

    fit_role = record.get("basis_fit_source_role")
    if not _nonempty(fit_role):
        raise StateReductionContractError("basis_fit_source_role is required")

    if not _nonempty(record.get("dimension_rule")):
        raise StateReductionContractError("dimension_rule is required")
    if not _nonempty(record.get("transport_rule")):
        raise StateReductionContractError("transport_rule is required")
    if not _nonempty(record.get("failure_or_refusal_rule")):
        raise StateReductionContractError("failure_or_refusal_rule is required")

    if record.get("frozen_before_real_chi_values") is not True:
        raise StateReductionContractError("reduction must be frozen before real Chi_bio values")

    if method_class == "CONTROL_ONLY_UNSUPERVISED_BASIS":
        if record.get("basis_fit_source_role") != "PBS_CONTROL_ONLY":
            raise StateReductionContractError(
                "CONTROL_ONLY_UNSUPERVISED_BASIS requires basis_fit_source_role PBS_CONTROL_ONLY"
            )

    if method_class == "EXTERNAL_FIXED_BASIS":
        if not _nonempty(record.get("external_basis_identity")):
            raise StateReductionContractError("external fixed basis requires external_basis_identity")

    if method_class == "PREDECLARED_BIOLOGICAL_MODULES":
        if not _nonempty(record.get("module_definition_identity")):
            raise StateReductionContractError("predeclared modules require module_definition_identity")
