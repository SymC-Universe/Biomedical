from __future__ import annotations

"""Protocol-neutral validation helpers for the GRI v0.7.1/v0.7.1A migration.

This module does not implement the scientific GRI Engine and does not alter any
frozen Stage C1 or legacy predictive P0 calculation. It validates control-plane
output semantics that are required regardless of the final supported scientific
scope.
"""

from collections.abc import Mapping
from typing import Any


class ProtocolContractError(ValueError):
    """Raised when a draft GRI output violates the active protocol contract."""


RESEARCH_MODES = frozenset({"P0_D", "P0_Q", "P1", "P2"})
FUNCTION_STATES = frozenset({"WORKS_HERE", "NOT_KNOWN_HERE"})
LIMIT_STATES = frozenset({"STOPS_WORKING_HERE", "NOT_KNOWN_HERE"})
RESEARCH_ROLES = frozenset(
    {
        "NOMINAL_FUNCTION",
        "PERTURBED_FUNCTION",
        "BOUNDARY_OR_TRANSITION",
        "RARE_NATURAL_LIMIT",
        "NOT_AVAILABLE",
        "NOT_APPLICABLE",
        "UNRESOLVED",
    }
)
INDEPENDENCE_GRADES = frozenset(
    {
        "INDEPENDENT",
        "PARTIALLY_INDEPENDENT",
        "NON_INDEPENDENT",
        "NON_INDEPENDENT_FOR_ENGINE_VALIDATION",
        "NOT_APPLICABLE",
        "UNRESOLVED",
    }
)

REQUIRED_TOP_LEVEL_GROUPS = (
    "research_mode",
    "measurement_status",
    "system_model",
    "engine",
    "atlas",
    "scalar_output",
    "modal_output",
    "conglomerate_output",
    "cross_component_output",
    "function_map_output",
    "limit_map_output",
    "reduction_adequacy",
    "classification",
    "refusal",
    "prediction",
    "independence",
    "uncertainty",
    "epistemic_status",
    "claim_ceiling",
    "provenance",
)

_REQUIRED_MAP_SCOPE_FIELDS = ("scope_id", "component_or_claim", "research_role")

_PROHIBITED_RARE_SELECTION_BASES = frozenset(
    {
        "CLOSENESS_TO_PREDICTED_CHI",
        "FAVORABLE_ENGINE_RESIDUAL",
        "UNFAVORABLE_ENGINE_RESIDUAL_ALONE",
        "AGREEMENT_WITH_PROPOSED_ARCHITECTURE",
        "VISUAL_SIMILARITY_TO_EXPECTED_RESULT",
        "ENGINE_OUTPUT_ONLY",
    }
)

_CONFIRMATORY_EMPIRICAL_OUTCOMES = frozenset(
    {
        "EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST",
        "EMPIRICAL_CLAIM_FALSIFIED",
    }
)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ProtocolContractError(f"{name} must be a mapping")
    return value


def _nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    try:
        return len(value) > 0
    except TypeError:
        return bool(value)


def _validate_map_scope(value: Mapping[str, Any], name: str) -> None:
    missing = [key for key in _REQUIRED_MAP_SCOPE_FIELDS if not _nonempty(value.get(key))]
    if missing:
        raise ProtocolContractError(
            f"{name} missing required scope field(s): " + ", ".join(missing)
        )
    role = value["research_role"]
    if role not in RESEARCH_ROLES:
        raise ProtocolContractError(f"invalid research role in {name}: {role!r}")


def validate_v071a_output(record: Mapping[str, Any]) -> None:
    """Validate protocol semantics for a draft GRI Engine/Tool output.

    The validator is intentionally conservative. It guards only requirements
    already fixed by the active cross-project protocol and current GRI claim
    ceiling. Scientific thresholds and future System Model capability are not
    defined here.
    """

    if not isinstance(record, Mapping):
        raise ProtocolContractError("record must be a mapping")

    missing = [key for key in REQUIRED_TOP_LEVEL_GROUPS if key not in record]
    if missing:
        raise ProtocolContractError(
            "missing required top-level group(s): " + ", ".join(missing)
        )

    mode = record["research_mode"]
    if mode not in RESEARCH_MODES:
        raise ProtocolContractError(f"unsupported research_mode: {mode!r}")

    function_map = _mapping(record["function_map_output"], "function_map_output")
    _validate_map_scope(function_map, "function_map_output")
    function_state = function_map.get("summary_state")
    if function_state not in FUNCTION_STATES:
        raise ProtocolContractError(
            f"invalid function-map summary_state: {function_state!r}"
        )

    limit_map = _mapping(record["limit_map_output"], "limit_map_output")
    _validate_map_scope(limit_map, "limit_map_output")
    limit_state = limit_map.get("summary_state")
    if limit_state not in LIMIT_STATES:
        raise ProtocolContractError(
            f"invalid limit-map summary_state: {limit_state!r}"
        )

    # Current GRI has not admitted a biological chi. A future version may only
    # change this by changing the scientifically frozen System Model, not by
    # silently populating an output field.
    classification = _mapping(record["classification"], "classification")
    chi_status = classification.get("biological_chi_status", "NOT_ADMITTED")
    if chi_status != "NOT_ADMITTED":
        raise ProtocolContractError(
            "biological chi is not admitted in the current GRI System Model"
        )
    scalar = _mapping(record["scalar_output"], "scalar_output")
    if scalar.get("biological_chi") is not None:
        raise ProtocolContractError(
            "biological_chi must be null while biological chi is NOT_ADMITTED"
        )

    # v0.7.1A rare-natural-testbed admission must be based on domain-native
    # rarity, not on the model output that is being challenged.
    rare_status = classification.get("rare_natural_testbed_status", "NOT_ADMITTED")
    if rare_status not in {"NOT_ADMITTED", "ADMITTED"}:
        raise ProtocolContractError(
            "rare_natural_testbed_status must be NOT_ADMITTED or ADMITTED"
        )
    if rare_status == "ADMITTED":
        rare = _mapping(
            classification.get("rare_natural_testbed"),
            "classification.rare_natural_testbed",
        )
        if not _nonempty(rare.get("domain_native_rarity_evidence")):
            raise ProtocolContractError(
                "RARE_NATURAL_TESTBED requires domain-native rarity evidence"
            )
        if rare.get("authenticity_and_confounding_gate_passed") is not True:
            raise ProtocolContractError(
                "RARE_NATURAL_TESTBED requires an authenticity/confounding gate"
            )
        basis = str(rare.get("selection_basis", "")).strip().upper()
        if not basis or basis in _PROHIBITED_RARE_SELECTION_BASES:
            raise ProtocolContractError(
                "RARE_NATURAL_TESTBED cannot be selected from Engine agreement/output"
            )
        if mode == "P1" and rare.get("selection_independent_of_engine_result") is not True:
            raise ProtocolContractError(
                "P1 rare-natural-testbed selection must be independent of Engine result"
            )

    # Atlas overlap may be shown descriptively, but it cannot be represented as
    # independent Engine validation when the reference family is non-independent.
    atlas = _mapping(record["atlas"], "atlas")
    atlas_grade = atlas.get("independence_grade")
    if atlas_grade is not None and atlas_grade not in INDEPENDENCE_GRADES:
        raise ProtocolContractError(f"invalid Atlas independence grade: {atlas_grade!r}")
    if (
        atlas.get("used_as_independent_engine_validation") is True
        and atlas_grade == "NON_INDEPENDENT_FOR_ENGINE_VALIDATION"
    ):
        raise ProtocolContractError(
            "non-independent Atlas evidence cannot validate the Engine independently"
        )

    independence = _mapping(record["independence"], "independence")
    for key, value in independence.items():
        if key.endswith("_independence") and value not in INDEPENDENCE_GRADES:
            raise ProtocolContractError(
                f"invalid pathway-specific independence grade for {key}: {value!r}"
            )

    prediction = _mapping(record["prediction"], "prediction")
    prediction_class = prediction.get("prediction_class")
    outcome_namespace = prediction.get("outcome_namespace")
    outcome = prediction.get("outcome")

    if prediction_class not in {None, "S", "M"}:
        raise ProtocolContractError(
            f"prediction_class must be S, M, or null; got {prediction_class!r}"
        )

    if prediction_class == "M" and outcome_namespace == "EMPIRICAL":
        raise ProtocolContractError(
            "method-validity prediction cannot use the empirical outcome namespace"
        )
    if (
        outcome_namespace == "METHOD_SCOPE"
        and isinstance(outcome, str)
        and outcome.startswith("EMPIRICAL_")
    ):
        raise ProtocolContractError(
            "method-scope outcome cannot be encoded as an empirical confirmation"
        )

    # P0-D and P0-Q may discover or qualify real empirical structure, but their
    # own result cannot be labeled as a frozen confirmatory survival/falsification
    # outcome. Such promotion requires a separately frozen P1 test.
    if mode in {"P0_D", "P0_Q"} and outcome in _CONFIRMATORY_EMPIRICAL_OUTCOMES:
        raise ProtocolContractError(
            "P0-D/P0-Q output cannot carry a confirmatory empirical outcome label"
        )

    # P1 status is only licensed after a complete, verifiably frozen MFR-14 with
    # decisive evidence untouched at freeze time.
    if mode == "P1":
        if prediction.get("mfr14_complete") is not True:
            raise ProtocolContractError("P1 requires complete MFR-14")
        if not _nonempty(prediction.get("freeze_id")):
            raise ProtocolContractError("P1 requires a verifiable freeze_id")
        if prediction.get("decisive_evidence_unopened_at_freeze") is not True:
            raise ProtocolContractError(
                "P1 requires decisive evidence to be unopened at freeze"
            )


def protocol_contract_version() -> str:
    """Return the protocol-control contract implemented by this helper."""

    return "GRI-v0.7.1+v0.7.1A-control-draft-20260910.2"
