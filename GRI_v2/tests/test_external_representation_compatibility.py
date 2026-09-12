from __future__ import annotations

import json
from pathlib import Path


_ROOT = Path(__file__).resolve().parents[1]
_COMPAT_PATH = _ROOT / "config" / "gri_external_representation_compatibility_20260911.json"
_SOURCE_LEDGER_PATH = _ROOT / "config" / "gri_external_source_gate_ledger_20260911.json"


def _load(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_representation_triage_cannot_be_p1_ready_by_source_discovery_alone():
    data = _load(_COMPAT_PATH)
    assert data["status"] == "P0_D_REPRESENTATION_TRIAGE"
    for row in data["sources"]:
        assert row["direct_p1_ready"] is False
        assert row["reason_not_direct_p1_ready"]


def test_representation_sources_are_known_source_gate_candidates():
    compatibility = _load(_COMPAT_PATH)
    source_ledger = _load(_SOURCE_LEDGER_PATH)
    candidate_ids = {row["candidate_id"] for row in source_ledger["candidates"]}
    for row in compatibility["sources"]:
        assert row["candidate_id"] in candidate_ids


def test_single_nucleus_nomura_source_cannot_silently_claim_bulk_compatibility():
    rows = {row["candidate_id"]: row for row in _load(_COMPAT_PATH)["sources"]}
    row = rows["IDH_GLIOMA_NOMURA_2026_DUAL_CAPTURE"]
    assert row["measurement_match"] == "REPRESENTATION_CHANGING"
    assert "SINGLE_NUCLEUS" in row["required_adapter_class"]


def test_care_source_preserves_unresolved_bulk_methylation_path():
    rows = {row["candidate_id"]: row for row in _load(_COMPAT_PATH)["sources"]}
    row = rows["CARE_IDH_MUT_2026"]
    assert "UNRESOLVED" in row["methylation_match"]
    assert row["measurement_match"] == "MULTI_LAYER_REPRESENTATION_CHANGING"


def test_crc_rrbs_is_not_treated_as_array_methylation():
    rows = {row["candidate_id"]: row for row in _load(_COMPAT_PATH)["sources"]}
    row = rows["CRC_GSE213402"]
    assert row["methylation_match"] == "RRBS_NOT_ARRAY"
    assert "RRBS" in row["required_adapter_class"]


def test_protocol_firewalls_are_explicit():
    rules = _load(_COMPAT_PATH)["rules"]
    assert rules["DIRECT_COMPATIBLE_DOES_NOT_MEAN_VALIDATED"] is True
    assert rules["ADAPTER_REQUIRED_IS_P0_D_OR_P0_Q_NOT_P1_CONFIRMATION_OF_ITSELF"] is True
    assert rules["NO_BIOLOGICAL_CHI_IN_ANY_EXTERNAL_ADAPTER"] is True
    assert rules["PATIENT_TIMEPOINT_HIERARCHY_MUST_BE_PRESERVED"] is True
    assert rules["NO_OUTCOME_DEPENDENT_SOURCE_OR_REPRESENTATION_SELECTION"] is True
