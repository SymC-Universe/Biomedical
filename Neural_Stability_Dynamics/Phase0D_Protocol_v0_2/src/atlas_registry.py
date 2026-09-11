from __future__ import annotations


ALLOWED_EVIDENCE_TIERS = {
    "DIRECT_NUMERIC_NATIVE",
    "REPRODUCED_FROM_SOURCE_DATA",
    "DERIVED_LICENSED",
    "SNIPPET_OR_PARTIAL",
    "BLOCKED_SOURCE",
    "INELIGIBLE",
}
ALLOWED_ROLES = {
    "NOMINAL_FUNCTION",
    "PERTURBED_FUNCTION",
    "BOUNDARY_OR_TRANSITION",
    "RARE_NATURAL_LIMIT",
}
ALLOWED_MAP_STATES = {"WORKS_HERE", "STOPS_WORKING_HERE", "NOT_KNOWN_HERE"}
INDEPENDENCE_KEYS = {
    "data",
    "cohort_system",
    "outcome_label",
    "parameter_tuning",
    "method_estimator",
    "atlas",
    "source_literature",
    "temporal_decisive_evidence",
}


def validate_atlas_entry(entry):
    """Fail-closed structural validation for Neurostability Atlas intake.

    This validator checks provenance/ontology completeness only. It does not
    decide whether a numerical coordinate is scientifically correct.
    """
    required = {
        "source_id",
        "coordinate_family",
        "coordinate_name",
        "native_or_derived",
        "value_or_object",
        "units",
        "estimator_method",
        "evidence_tier",
        "research_role",
        "function_limit_state",
        "independence_pathways",
        "scope_ceiling",
    }
    missing = sorted(required - set(entry))
    if missing:
        raise ValueError(f"missing Atlas entry fields: {missing}")
    if entry["evidence_tier"] not in ALLOWED_EVIDENCE_TIERS:
        raise ValueError("invalid evidence tier")
    if entry["research_role"] not in ALLOWED_ROLES:
        raise ValueError("invalid research role")
    if entry["function_limit_state"] not in ALLOWED_MAP_STATES:
        raise ValueError("invalid Function/Limit state")
    pathways = entry["independence_pathways"]
    if not isinstance(pathways, dict) or set(pathways) != INDEPENDENCE_KEYS:
        raise ValueError("Atlas independence must be recorded pathway-specifically")

    name = str(entry["coordinate_name"]).lower()
    if name in {"chi", "χ"}:
        admission = entry.get("chi_admission")
        if not isinstance(admission, dict) or admission.get("status") != "LICENSED":
            raise ValueError("chi is withheld unless an explicit licensed admission record is attached")
        if not admission.get("derivation"):
            raise ValueError("licensed chi requires an explicit derivation")
        if not admission.get("native_inputs_retained", False):
            raise ValueError("licensed chi requires underlying native inputs to be retained")

    if str(entry["native_or_derived"]).upper() == "DERIVED":
        if not entry.get("derivation_record_if_any"):
            raise ValueError("derived Atlas coordinates require a derivation record")

    return True
