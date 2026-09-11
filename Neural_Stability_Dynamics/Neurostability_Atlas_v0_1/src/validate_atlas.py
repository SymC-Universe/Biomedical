from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RESEARCH_ROLES = {
    "NOMINAL_FUNCTION",
    "PERTURBED_FUNCTION",
    "BOUNDARY_OR_TRANSITION",
    "RARE_NATURAL_LIMIT",
}

ELIGIBILITY_STATES = {
    "NATIVE_REPORTED",
    "NATIVE_RECONSTRUCTED_FROM_RAW_DATA",
    "NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE",
    "DERIVED_EXACT",
    "DERIVED_MODEL_CONDITIONAL",
    "WITHHELD_INSUFFICIENT_INFORMATION",
    "WITHHELD_ASSUMPTION_NOT_LICENSED",
    "NOT_APPLICABLE",
    "UNRESOLVED",
}

INDEPENDENCE_KEYS = {
    "data",
    "cohort_system",
    "outcome_label",
    "parameter_tuning",
    "method_estimator",
    "atlas_engine",
    "source_literature",
    "temporal_decisive_evidence",
}

INDEPENDENCE_GRADES = {
    "INDEPENDENT",
    "PARTIALLY_INDEPENDENT",
    "NON_INDEPENDENT_FOR_ENGINE_VALIDATION",
    "NOT_APPLICABLE",
    "UNRESOLVED",
}

CHI_STATUSES = {
    "CHI_NATIVE_REPORTED",
    "CHI_DERIVED_LICENSED_SECOND_ORDER",
    "CHI_WITHHELD_NO_SECOND_ORDER_LICENSE",
    "CHI_WITHHELD_INSUFFICIENT_NATIVE_PARAMETERS",
    "CHI_NOT_APPLICABLE",
}

WITHHELD_CHI = {
    "CHI_WITHHELD_NO_SECOND_ORDER_LICENSE",
    "CHI_WITHHELD_INSUFFICIENT_NATIVE_PARAMETERS",
    "CHI_NOT_APPLICABLE",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_coordinate_definitions(data: dict) -> None:
    families = data.get("families")
    if not isinstance(families, dict) or not families:
        raise ValueError("coordinate definitions require non-empty families")
    ids = []
    for family_name, family in families.items():
        coords = family.get("coordinates")
        if not isinstance(coords, list) or not coords:
            raise ValueError(f"coordinate family {family_name} requires coordinates")
        for coord in coords:
            coord_id = coord.get("id")
            if not isinstance(coord_id, str) or not coord_id:
                raise ValueError(f"invalid coordinate id in {family_name}")
            ids.append(coord_id)
    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if duplicates:
        raise ValueError(f"duplicate coordinate ids: {duplicates}")
    if set(data.get("research_roles", [])) != RESEARCH_ROLES:
        raise ValueError("coordinate definitions must preserve all four v0.7.1A roles")
    if set(data.get("eligibility_states", [])) != ELIGIBILITY_STATES:
        raise ValueError("coordinate eligibility states drifted")


def validate_source_queue(data: dict) -> None:
    if data.get("status") != "A1_SOURCE_QUEUE_FROZEN_BEFORE_COORDINATE_POPULATION":
        raise ValueError("source queue must be frozen before coordinate population")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("source queue is empty")
    ids = [x.get("source_id") for x in sources]
    if any(not isinstance(x, str) or not x for x in ids):
        raise ValueError("source_id is required")
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate source_id")
    for source in sources:
        roles = set(source.get("research_roles", []))
        if not roles or not roles <= RESEARCH_ROLES:
            raise ValueError(f"invalid research roles for {source['source_id']}")
        chi_status = source.get("chi_initial_status")
        if chi_status not in WITHHELD_CHI:
            raise ValueError(
                f"initial source queue may not prepopulate chi for {source['source_id']}: {chi_status}"
            )
    balance = data.get("coverage_balance", {})
    for required in ["NOMINAL_FUNCTION", "PERTURBED_FUNCTION", "BOUNDARY_OR_TRANSITION"]:
        if not balance.get(required):
            raise ValueError(f"initial queue lacks required active coverage role {required}")
    if balance.get("RARE_NATURAL_LIMIT") not in ([], None):
        raise ValueError("rare-natural slot was not qualified before initial source freeze")


def validate_entry(entry: dict, coordinate_ids: set[str] | None = None) -> None:
    required = {
        "atlas_entry_id",
        "source_id",
        "research_role",
        "evidence_tier",
        "native_model",
        "context",
        "coordinates",
        "independence",
        "scope",
        "engine_selector_eligible",
        "chi",
    }
    missing = sorted(required - set(entry))
    if missing:
        raise ValueError(f"missing Atlas entry fields: {missing}")
    if entry["research_role"] not in RESEARCH_ROLES:
        raise ValueError("invalid research_role")
    if entry["engine_selector_eligible"] is not False:
        raise ValueError("Atlas values may not be Structural-Engine selector inputs")
    if str(entry["scope"]).upper() == "UNIVERSAL":
        raise ValueError("UNIVERSAL is not an Atlas target scope")

    independence = entry["independence"]
    if set(independence) != INDEPENDENCE_KEYS:
        raise ValueError("Atlas entry must carry all and only the eight independence pathways")
    for key, value in independence.items():
        if not isinstance(value, dict) or value.get("grade") not in INDEPENDENCE_GRADES:
            raise ValueError(f"invalid independence grade for {key}")
        if "reason" not in value:
            raise ValueError(f"independence reason missing for {key}")

    for coord in entry["coordinates"]:
        coord_id = coord.get("coordinate_id")
        if coordinate_ids is not None and coord_id not in coordinate_ids:
            raise ValueError(f"coordinate not declared in ontology: {coord_id}")
        if coord.get("eligibility_status") not in ELIGIBILITY_STATES:
            raise ValueError(f"invalid eligibility status for {coord_id}")
        if "provenance" not in coord or "source_location" not in coord["provenance"]:
            raise ValueError(f"coordinate provenance incomplete for {coord_id}")

    chi = entry["chi"]
    status = chi.get("status")
    if status not in CHI_STATUSES:
        raise ValueError("invalid chi status")
    value = chi.get("value")
    if status in WITHHELD_CHI and value is not None:
        raise ValueError("withheld/not-applicable chi must have null value")
    if status == "CHI_DERIVED_LICENSED_SECOND_ORDER":
        if value is None:
            raise ValueError("licensed derived chi requires value")
        if not chi.get("derivation") or not chi.get("frequency_semantics"):
            raise ValueError("licensed derived chi requires derivation and frequency semantics")
    if status == "CHI_NATIVE_REPORTED" and value is None:
        raise ValueError("native-reported chi requires value")


def declared_coordinate_ids(defs: dict) -> set[str]:
    return {
        coord["id"]
        for family in defs["families"].values()
        for coord in family["coordinates"]
    }


def validate_repository() -> None:
    definitions = load_json(ROOT / "registries" / "COORDINATE_DEFINITIONS.json")
    validate_coordinate_definitions(definitions)
    validate_source_queue(load_json(ROOT / "registries" / "SOURCE_INTAKE_QUEUE.json"))
    ids = declared_coordinate_ids(definitions)
    template = ROOT / "entries" / "TEMPLATE.json"
    if template.exists():
        validate_entry(load_json(template), ids)


if __name__ == "__main__":
    validate_repository()
    print("Neurostability Atlas v0.1 schema/source-intake validation PASS")
