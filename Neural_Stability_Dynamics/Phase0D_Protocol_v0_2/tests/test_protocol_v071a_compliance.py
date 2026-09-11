import json
from pathlib import Path

import pytest

from src.landscape import make_mapping_record, split_function_limit


ROOT = Path(__file__).resolve().parents[1]


def test_protocol_baseline_names_additive_v071a():
    text = (ROOT / "PROTOCOL_BASELINE.md").read_text(encoding="utf-8")
    assert "v0.7.1 FINAL + General Cross-Project Research Protocol v0.7.1A" in text
    assert "P0-D" in text and "P0-Q" in text
    assert "P1 is closed" in text


def test_coverage_registry_contains_all_four_addendum_roles():
    data = json.loads((ROOT / "registries" / "COVERAGE_ARCHITECTURE.json").read_text(encoding="utf-8"))
    assert set(data["roles"]) == {
        "NOMINAL_FUNCTION",
        "PERTURBED_FUNCTION",
        "BOUNDARY_OR_TRANSITION",
        "RARE_NATURAL_LIMIT",
    }
    assert data["roles"]["RARE_NATURAL_LIMIT"]["status"] == "NOT_APPLICABLE_CURRENT_SYNTHETIC_STAGE"
    assert data["historical_status_firewall"]["p0q1_subspace_dmd"] == "FAILS_P0Q1_UNCHANGED"


def test_independence_registry_is_pathway_specific():
    data = json.loads((ROOT / "registries" / "INDEPENDENCE_PATHWAYS.json").read_text(encoding="utf-8"))
    expected = {
        "data",
        "cohort_system",
        "outcome_label",
        "parameter_tuning",
        "method_estimator",
        "atlas",
        "source_literature",
        "temporal_decisive_evidence",
    }
    assert set(data["pathways"]) == expected


def test_mapping_record_is_claim_specific_and_nonconfirmatory():
    rec = make_mapping_record(
        point_id="nominal-001",
        research_mode="P0-D",
        coverage_role="NOMINAL_FUNCTION",
        location_state="WORKS_HERE",
        claim_object="modal carrier recovery",
        controls={"noise_fraction": 0.1},
        observables={"subspace_similarity": 0.99},
        scope="SUPPORTED_IN_TESTED_REGIME",
    )
    assert rec["confirmatory"] is False
    assert rec["claim_object"] == "modal carrier recovery"
    assert rec["epistemic_status"] == "EXPLORATORY_P0_D"


def test_function_limit_unknown_views_remain_separate():
    records = [
        make_mapping_record(
            point_id="f",
            research_mode="P0-D",
            coverage_role="NOMINAL_FUNCTION",
            location_state="WORKS_HERE",
            claim_object="rank signal",
            controls={},
            observables={},
        ),
        make_mapping_record(
            point_id="l",
            research_mode="P0-D",
            coverage_role="BOUNDARY_OR_TRANSITION",
            location_state="STOPS_WORKING_HERE",
            claim_object="rank signal",
            controls={},
            observables={},
        ),
        make_mapping_record(
            point_id="u",
            research_mode="P0-D",
            coverage_role="BOUNDARY_OR_TRANSITION",
            location_state="NOT_KNOWN_HERE",
            claim_object="modal geometry",
            controls={},
            observables={},
        ),
    ]
    views = split_function_limit(records)
    assert len(views["function_map"]) == 1
    assert len(views["limit_map"]) == 1
    assert len(views["unknown_map"]) == 1


def test_unapproved_scope_cannot_be_silently_added():
    with pytest.raises(ValueError):
        make_mapping_record(
            point_id="bad",
            research_mode="P0-D",
            coverage_role="NOMINAL_FUNCTION",
            location_state="WORKS_HERE",
            claim_object="anything",
            controls={},
            observables={},
            scope="UNIVERSAL",
        )


def test_scientific_contract_preserves_historical_failures_and_p1_hold():
    text = (ROOT / "SCIENTIFIC_CONTRACT.md").read_text(encoding="utf-8")
    assert "Phase 0C v0.2 remains the official prospective FAIL / FAIL / FAIL result" in text
    assert "P1 may begin only after complete MFR-14" in text
    assert "Function Map and Limit Map are coequal" in text
