from __future__ import annotations

import json
from pathlib import Path


_LEDGER_PATH = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "gri_external_source_gate_ledger_20260911.json"
)


def _ledger():
    with _LEDGER_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _by_id():
    return {row["candidate_id"]: row for row in _ledger()["candidates"]}


def test_source_discovery_has_not_selected_p1_or_opened_gri_outcomes():
    ledger = _ledger()
    assert ledger["scientific_outcomes_opened"] is False
    assert ledger["p1_dataset_selected"] is False
    for candidate in ledger["candidates"]:
        assert candidate["research_mode"] == "P0_D"
        assert candidate["gri_outcome_status"] == "UNOPENED"
        assert candidate["p1_status"] == "NOT_SELECTED_NOT_FROZEN"
        assert candidate["selection_basis"] == "SOURCE_ARCHITECTURE_NOT_GRI_AGREEMENT"


def test_candidate_ids_are_unique():
    rows = _ledger()["candidates"]
    ids = [row["candidate_id"] for row in rows]
    assert len(ids) == len(set(ids))


def test_prostate_identity_gate_remains_exact_and_unopened():
    row = _by_id()["PROSTATE_GSE262522_GSE262524_GSE237995"]
    counts = row["modality_counts"]
    assert counts["methylation_450k"] == 68
    assert counts["methylation_epic"] == 53
    assert counts["methylation_union"] == 121
    assert counts["rna_seq"] == 121
    assert row["identity_gate"] == "PASS"
    assert row["identity_result"] == "EXACT_121_OF_121_GEO_TITLE_BIJECTION"
    assert row["published_shared_probe_count"] == 449636


def test_breast_diagnostic_normalization_is_not_a_production_identity_rule():
    row = _by_id()["BREAST_GSE58999_GSE57968_GSE59000"]
    result = row["identity_result"]
    assert result["raw_title_match"] == "66_OF_72"
    assert result["terminal_b_diagnostic_crosswalk"] == "72_OF_72"
    assert result["production_identity_rule"] == "NOT_YET_ADMITTED"
    assert "PENDING" in row["identity_gate"]


def test_melanoma_pair_structure_preserves_refusal_and_asymmetries():
    row = _by_id()["MELANOMA_GSE65186"]
    counts = row["modality_counts"]
    result = row["identity_result"]
    assert counts["shared_human_patient_states"] == 61
    assert counts["shared_human_patient_ids"] == 19
    assert counts["strict_shared_baseline_plus_post_patients"] == 18
    assert counts["shared_cell_model_states"] == 8
    assert result["strict_pair_refusal_patient"] == "Pt21"
    assert result["methylation_only_states"] == ["Pt14-baseline", "Pt14-DP1"]
    assert result["transcriptome_only_states"] == [
        "Pt19-DDP2",
        "Pt24-baseline",
        "Pt24-DDP1",
    ]


def test_ccell_35_is_not_silently_treated_as_complete_five_modality_intersection():
    row = _by_id()["CGGA_CCELL_4083"]
    counts = row["modality_counts"]
    result = row["identity_result"]
    assert counts["proteomics"] == 35
    assert counts["phosphoproteomics"] == 35
    assert counts["methylation"] == 29
    assert counts["bulk_rna"] == 19
    assert counts["scrna_title_count"] == 18
    assert counts["scrna_description_sample_count"] == 19
    assert result["all_five_modalities_complete_on_35"] is False
    assert result["exact_pairwise_overlap"] == "UNRESOLVED"
    assert result["scrna_source_count_discrepancy"] == "OPEN"


def test_dedicated_audit_references_exist_for_advanced_identity_gates():
    root = Path(__file__).resolve().parents[1]
    for candidate_id in (
        "PROSTATE_GSE262522_GSE262524_GSE237995",
        "BREAST_GSE58999_GSE57968_GSE59000",
        "MELANOMA_GSE65186",
        "CGGA_CCELL_4083",
    ):
        relative = _by_id()[candidate_id]["dedicated_audit"]
        assert relative
        assert (root / relative).is_file(), f"missing dedicated audit: {relative}"
