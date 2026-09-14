from pathlib import Path

import pytest

from src.preflight_chi_bio_regulon_source_export import inventory_export


def test_inventory_export_is_provenance_only(tmp_path: Path):
    path = tmp_path / "collectri.tsv"
    path.write_text(
        "source\ttarget\tweight\nTF1\tG1\t1\nTF2\tG2\t-1\n",
        encoding="utf-8",
    )
    result = inventory_export(
        path,
        source_id="COLLECTRI_CANDIDATE",
        expected_columns=("source", "target", "weight"),
    )

    assert result["status"] == "PASS_SOURCE_EXPORT_PROVENANCE_ONLY"
    assert result["interaction_row_count"] == 2
    assert len(result["sha256"]) == 64
    for key in (
        "tf_activity_scored",
        "state_coordinates_computed",
        "state_dimension_selected",
        "operator_fit",
        "g1_computed",
        "g2_computed",
        "chi_bio_computed",
    ):
        assert result[key] is False
    assert result["promotion_effect"] == "NONE"


def test_inventory_rejects_unknown_source(tmp_path: Path):
    path = tmp_path / "x.csv"
    path.write_text("a,b\n1,2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unrecognized source_id"):
        inventory_export(path, source_id="UNAPPROVED_SOURCE")


def test_inventory_rejects_missing_expected_semantic_columns(tmp_path: Path):
    path = tmp_path / "dorothea.tsv"
    path.write_text("source\ttarget\nTF1\tG1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing expected column"):
        inventory_export(
            path,
            source_id="DOROTHEA_CANDIDATE",
            expected_columns=("source", "target", "confidence"),
        )


def test_inventory_rejects_malformed_row_width(tmp_path: Path):
    path = tmp_path / "bad.tsv"
    path.write_text("source\ttarget\tweight\nTF1\tG1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="wrong field count"):
        inventory_export(path, source_id="COLLECTRI_CANDIDATE")
