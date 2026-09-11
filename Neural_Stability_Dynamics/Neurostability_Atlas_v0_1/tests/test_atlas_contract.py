from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from src.validate_atlas import (
    declared_coordinate_ids,
    load_json,
    validate_coordinate_definitions,
    validate_entry,
    validate_source_queue,
)


def _template():
    return load_json(ROOT / "entries" / "TEMPLATE.json")


def test_coordinate_ontology_and_source_queue_validate():
    defs = load_json(ROOT / "registries" / "COORDINATE_DEFINITIONS.json")
    validate_coordinate_definitions(defs)
    validate_source_queue(load_json(ROOT / "registries" / "SOURCE_INTAKE_QUEUE.json"))


def test_template_validates_against_declared_coordinates():
    defs = load_json(ROOT / "registries" / "COORDINATE_DEFINITIONS.json")
    validate_entry(_template(), declared_coordinate_ids(defs))


def test_atlas_entry_can_never_be_selector_eligible():
    entry = _template()
    entry["engine_selector_eligible"] = True
    with pytest.raises(ValueError):
        validate_entry(entry)


def test_unlicensed_chi_cannot_have_value():
    entry = _template()
    entry["chi"]["value"] = 1.0
    with pytest.raises(ValueError):
        validate_entry(entry)


def test_derived_chi_requires_derivation_and_frequency_semantics():
    entry = _template()
    entry["chi"] = {
        "status": "CHI_DERIVED_LICENSED_SECOND_ORDER",
        "value": 0.8,
        "derivation": None,
        "frequency_semantics": None,
        "uncertainty": None,
    }
    with pytest.raises(ValueError):
        validate_entry(entry)


def test_missing_independence_pathway_is_rejected():
    entry = _template()
    del entry["independence"]["outcome_label"]
    with pytest.raises(ValueError):
        validate_entry(entry)


def test_universal_scope_is_rejected():
    entry = _template()
    entry["scope"] = "UNIVERSAL"
    with pytest.raises(ValueError):
        validate_entry(entry)


def test_undeclared_coordinate_is_rejected():
    defs = load_json(ROOT / "registries" / "COORDINATE_DEFINITIONS.json")
    entry = _template()
    entry["coordinates"][0]["coordinate_id"] = "magic_neural_stability_number"
    with pytest.raises(ValueError):
        validate_entry(entry, declared_coordinate_ids(defs))


def test_rare_natural_role_is_not_manufactured_in_initial_queue():
    queue = load_json(ROOT / "registries" / "SOURCE_INTAKE_QUEUE.json")
    assert queue["coverage_balance"]["RARE_NATURAL_LIMIT"] == []
    assert queue["rare_natural_limit_status"] == "NOT_YET_QUALIFIED_DO_NOT_MANUFACTURE"
