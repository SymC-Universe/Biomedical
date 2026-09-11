from __future__ import annotations

from copy import deepcopy


COVERAGE_ROLES = frozenset(
    {
        "NOMINAL_FUNCTION",
        "PERTURBED_FUNCTION",
        "BOUNDARY_OR_TRANSITION",
        "RARE_NATURAL_LIMIT",
    }
)

LOCATION_STATES = frozenset(
    {
        "WORKS_HERE",
        "STOPS_WORKING_HERE",
        "NOT_KNOWN_HERE",
    }
)

P0_MODES = frozenset({"P0-D", "P0-Q"})

SCOPE_LABELS = frozenset(
    {
        "SUPPORTED_IN_TESTED_REGIME",
        "CROSS_REGIME",
        "CROSS_SYSTEM",
        "CROSS_DOMAIN",
        "ROBUST_ACROSS_TESTED_LIMITS",
        "DOMAIN_LIMITED",
        "REGIME_LIMITED",
        "UNRESOLVED_BEYOND_TESTED_RANGE",
        "NOT_YET_ASSIGNED",
    }
)


def make_mapping_record(
    *,
    point_id,
    research_mode,
    coverage_role,
    location_state,
    claim_object,
    controls,
    observables,
    scope="NOT_YET_ASSIGNED",
    epistemic_status=None,
    uncertainty=None,
    identifiability=None,
    open_channel=None,
    notes=None,
):
    """Create one non-adjudicating NSD Function/Limit mapping record.

    This helper deliberately does not decide whether a scientific claim passes.
    It records where a *specific object* appears supported, unsupported, or
    unresolved during P0 mapping/qualification.
    """
    if research_mode not in P0_MODES:
        raise ValueError(f"research_mode must be one of {sorted(P0_MODES)}")
    if coverage_role not in COVERAGE_ROLES:
        raise ValueError(f"coverage_role must be one of {sorted(COVERAGE_ROLES)}")
    if location_state not in LOCATION_STATES:
        raise ValueError(f"location_state must be one of {sorted(LOCATION_STATES)}")
    if scope not in SCOPE_LABELS:
        raise ValueError(f"scope must be one of {sorted(SCOPE_LABELS)}")
    if str(scope).upper() == "UNIVERSAL":
        raise ValueError("UNIVERSAL is not an NSD target scope under protocol v0.7.1A")
    if not str(point_id).strip():
        raise ValueError("point_id is required")
    if not str(claim_object).strip():
        raise ValueError("claim_object is required; mapping states are claim-specific")
    if not isinstance(controls, dict) or not isinstance(observables, dict):
        raise TypeError("controls and observables must be dictionaries")

    if epistemic_status is None:
        epistemic_status = (
            "EXPLORATORY_P0_D" if research_mode == "P0-D" else "QUALIFICATION_P0_Q"
        )

    return {
        "schema": "nsd-function-limit-map-record-v0.7.1A-p0",
        "point_id": str(point_id),
        "research_mode": research_mode,
        "coverage_role": coverage_role,
        "location_state": location_state,
        "claim_object": str(claim_object),
        "scope": scope,
        "epistemic_status": str(epistemic_status),
        "controls": deepcopy(controls),
        "observables": deepcopy(observables),
        "uncertainty": deepcopy(uncertainty),
        "identifiability": deepcopy(identifiability),
        "open_channel": deepcopy(open_channel),
        "notes": None if notes is None else str(notes),
        "confirmatory": False,
    }


def split_function_limit(records):
    """Return Function, Limit and Unknown views without changing records."""
    function_map = []
    limit_map = []
    unknown_map = []
    for record in records:
        state = record.get("location_state")
        if state == "WORKS_HERE":
            function_map.append(record)
        elif state == "STOPS_WORKING_HERE":
            limit_map.append(record)
        elif state == "NOT_KNOWN_HERE":
            unknown_map.append(record)
        else:
            raise ValueError(f"unknown location_state: {state!r}")
    return {
        "function_map": function_map,
        "limit_map": limit_map,
        "unknown_map": unknown_map,
    }
