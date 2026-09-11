import hashlib
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


def _git_blob_sha(path: Path) -> str:
    content = path.read_bytes()
    return hashlib.sha1(f"blob {len(content)}\0".encode("ascii") + content).hexdigest()


def test_coordinate_ontology_and_source_queue_validate():
    defs = load_json(ROOT / "registries" / "COORDINATE_DEFINITIONS.json")
    validate_coordinate_definitions(defs)
    validate_source_queue(load_json(ROOT / "registries" / "SOURCE_INTAKE_QUEUE.json"))


def test_a0_schema_lock_matches_content():
    lock = load_json(ROOT / "registries" / "ATLAS_A0_SCHEMA_LOCK.json")
    assert lock["status"] == "A0_CONTENT_FROZEN_BEFORE_NUMERICAL_COORDINATE_POPULATION"
    for rel, expected in lock["locked_files"].items():
        assert _git_blob_sha(ROOT / rel) == expected


def test_a1_source_lock_matches_content():
    lock = load_json(ROOT / "registries" / "ATLAS_A1_SOURCE_LOCK.json")
    assert lock["status"] == "A1_SOURCE_SELECTION_FROZEN_BEFORE_A2_COORDINATE_RECONSTRUCTION"
    for rel, expected in lock["locked_files"].items():
        assert _git_blob_sha(ROOT / rel) == expected


def test_a2_pilot_is_bound_to_frozen_method_content():
    freeze = load_json(ROOT / "registries" / "A2_SRM_CSD_SVD_PILOT_FREEZE.json")
    assert freeze["status"] == "FROZEN_BEFORE_EEG_VALUE_INSPECTION"
    method = ROOT / freeze["reconstruction"]["method_spec"]
    assert _git_blob_sha(method) == freeze["reconstruction"]["method_spec_git_blob_sha"]
    assert freeze["reconstruction"]["pass_thresholds"] is None
    assert freeze["coordinate_policy"]["chi"] == "CHI_WITHHELD_NO_SECOND_ORDER_LICENSE"


def test_srm_reservoir_is_disjoint_and_complete():
    pilot = load_json(ROOT / "registries" / "A2_SRM_CSD_SVD_PILOT_FREEZE.json")
    reservoir = load_json(ROOT / "registries" / "A2_SRM_REPLICATION_RESERVOIR_FREEZE.json")
    dev = set(reservoir["development_pilot_subjects"])
    hold = set(reservoir["unopened_p0q_reservoir_subjects"])
    full = set(pilot["repeat_session_subjects_lexicographic"])
    assert reservoir["status"] == "UNOPENED_P0_Q_RESERVOIR_FROZEN_BEFORE_A2_PILOT_EEG"
    assert dev.isdisjoint(hold)
    assert dev | hold == full
    assert len(dev) == 8
    assert len(hold) == 34


def test_template_validates_against_declared_coordinates():
    defs = load_json(ROOT / "registries" / "COORDINATE_DEFINITIONS.json")
    validate_entry(_template(), declared_coordinate_ids(defs))


def test_pinned_derivative_is_an_explicit_eligibility_state():
    defs = load_json(ROOT / "registries" / "COORDINATE_DEFINITIONS.json")
    assert "NATIVE_RECONSTRUCTED_FROM_PINNED_DERIVATIVE" in defs["eligibility_states"]


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
