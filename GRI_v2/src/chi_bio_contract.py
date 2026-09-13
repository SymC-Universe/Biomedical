from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class ChiBioContractError(ValueError):
    pass


GATES = tuple(f"CB{i}" for i in range(1, 15))
GATE_SET = frozenset(GATES)
PROMOTION_STATES = {
    "NOT_ADMITTED": frozenset(),
    "CANDIDATE_LOCKED": frozenset(f"CB{i}" for i in range(1, 10)),
    "INTERNALLY_QUALIFIED_P0Q": frozenset(f"CB{i}" for i in range(1, 12)),
    "EXTERNALLY_ADMITTED_P1": frozenset(f"CB{i}" for i in range(1, 14)),
    "UNITY_BOUNDARY_ADMITTED": frozenset(f"CB{i}" for i in range(1, 15)),
}
VALUE_ALLOWED_STATES = frozenset({
    "INTERNALLY_QUALIFIED_P0Q",
    "EXTERNALLY_ADMITTED_P1",
    "UNITY_BOUNDARY_ADMITTED",
})
PROHIBITED_DIRECT_ALIASES = frozenset({
    "CV/2", "CV2", "CV_OVER_2", "S_SPEC", "H2", "H3A", "H3B", "GLOBAL_CKA"
})
REQUIRED_REFUSALS = frozenset({
    "NO_COHERENT_CHI_BIO",
    "NOT_IDENTIFIABLE",
    "OUT_OF_VALIDITY_REGIME",
    "UNCERTAINTY_SPANS_BOUNDARY",
    "REPRESENTATION_DEPENDENT_NO_TRANSFER",
    "INSUFFICIENT_TEMPORAL_INFORMATION_FOR_DYNAMIC_INTERPRETATION",
})


def _nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    try:
        return len(value) > 0
    except TypeError:
        return bool(value)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ChiBioContractError(f"{name} must be a mapping")
    return value


def validate_chi_bio_record(record: Mapping[str, Any]) -> None:
    if not isinstance(record, Mapping):
        raise ChiBioContractError("record must be a mapping")
    if record.get("notation") != "Chi_bio":
        raise ChiBioContractError("notation must be exactly Chi_bio")
    if not _nonempty(record.get("candidate_id")):
        raise ChiBioContractError("candidate_id is required")

    state = record.get("promotion_state")
    if state not in PROMOTION_STATES:
        raise ChiBioContractError(f"invalid promotion_state: {state!r}")

    passed = frozenset(str(x) for x in record.get("passed_gates", []))
    unknown = passed - GATE_SET
    if unknown:
        raise ChiBioContractError("unknown gate(s): " + ", ".join(sorted(unknown)))
    missing = PROMOTION_STATES[state] - passed
    if missing:
        raise ChiBioContractError("missing gate(s): " + ", ".join(sorted(missing)))

    alias = str(record.get("direct_alias_of") or "").strip().upper()
    if alias in PROHIBITED_DIRECT_ALIASES:
        raise ChiBioContractError("direct alias is prohibited for Chi_bio")

    for key in (
        "construction_used_atlas_positions",
        "construction_used_downstream_outcome",
        "formula_selected_by_closeness_to_one",
        "posthoc_rescaling_created_unity",
        "disagreeing_cancers_or_modes_suppressed",
    ):
        if record.get(key) is True:
            raise ChiBioContractError(f"prohibited construction flag set: {key}")

    for key in ("scalar_view", "modal_vector_view", "conglomerate_system_view"):
        view = _mapping(record.get(key), key)
        if "status" not in view or "inputs" not in view:
            raise ChiBioContractError(f"{key} requires status and inputs")

    refusal = _mapping(record.get("refusal"), "refusal")
    supported = frozenset(str(x) for x in refusal.get("supported_states", []))
    missing_refusals = REQUIRED_REFUSALS - supported
    if missing_refusals:
        raise ChiBioContractError("missing refusal state(s): " + ", ".join(sorted(missing_refusals)))

    _mapping(record.get("uncertainty"), "uncertainty")

    if state != "NOT_ADMITTED" and not _nonempty(record.get("formula_or_mapping")):
        raise ChiBioContractError("locked or admitted state requires formula_or_mapping")

    if record.get("Chi_bio_value") is not None and state not in VALUE_ALLOWED_STATES:
        raise ChiBioContractError("Chi_bio_value is not allowed in this promotion state")

    unity_status = record.get("unity_boundary_status")
    allowed_unity = {"NOT_TESTED", "CANDIDATE_REFERENCE_ONLY", "UNRESOLVED", "REJECTED_OR_DIFFERENT_BOUNDARY", "ADMITTED"}
    if unity_status not in allowed_unity:
        raise ChiBioContractError("invalid unity_boundary_status")

    if state != "UNITY_BOUNDARY_ADMITTED" and record.get("biological_regime_label") is not None:
        raise ChiBioContractError("biological_regime_label requires unity-boundary admission")

    if state in {"EXTERNALLY_ADMITTED_P1", "UNITY_BOUNDARY_ADMITTED"}:
        if not _nonempty(record.get("external_p1_freeze_id")):
            raise ChiBioContractError("external admission requires external_p1_freeze_id")
        if record.get("decisive_external_evidence_unopened_at_freeze") is not True:
            raise ChiBioContractError("external admission requires unopened decisive evidence at freeze")

    if unity_status == "ADMITTED":
        if state != "UNITY_BOUNDARY_ADMITTED":
            raise ChiBioContractError("unity cannot be admitted before UNITY_BOUNDARY_ADMITTED")
        if "CB14" not in passed:
            raise ChiBioContractError("unity admission requires CB14")
        if not _nonempty(record.get("unity_basis")):
            raise ChiBioContractError("unity admission requires unity_basis")
        if not _nonempty(record.get("independent_boundary_test_id")):
            raise ChiBioContractError("unity admission requires independent_boundary_test_id")
    elif state == "UNITY_BOUNDARY_ADMITTED":
        raise ChiBioContractError("UNITY_BOUNDARY_ADMITTED requires unity_boundary_status ADMITTED")


def required_gates_for_state(state: str) -> tuple[str, ...]:
    if state not in PROMOTION_STATES:
        raise ChiBioContractError(f"invalid promotion_state: {state!r}")
    return tuple(sorted(PROMOTION_STATES[state], key=lambda x: int(x[2:])))
