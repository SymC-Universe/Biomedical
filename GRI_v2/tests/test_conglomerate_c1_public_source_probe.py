from pathlib import Path

from src.probe_conglomerate_c1_public_sources import parse_content_range


def test_parse_content_range_total():
    assert parse_content_range("bytes 0-0/1882540959") == 1882540959
    assert parse_content_range("bytes 0-0/5022150019") == 5022150019


def test_parse_content_range_unknown_or_invalid():
    assert parse_content_range(None) is None
    assert parse_content_range("bytes 0-0/*") is None
    assert parse_content_range("invalid") is None


def test_c1_source_registry_exists_and_is_outcome_blind():
    repo_root = Path(__file__).resolve().parents[2]
    path = repo_root / "GRI_v2/config/gri_conglomerate_c1_source_registry_20260918.json"
    assert path.is_file()

    import json

    cfg = json.loads(path.read_text(encoding="utf-8"))
    assert cfg["rules"]["no_biological_outcome_access"] is True
    assert cfg["rules"]["no_model_fit"] is True
    assert cfg["rules"]["no_cross_block_aggregation"] is True
    assert len(cfg["sources"]) == 7
    assert {s["id"] for s in cfg["sources"]} == {
        "RNA_PANCAN_FINAL",
        "ABSOLUTE_PURITY",
        "LEUKOCYTE_FRACTION",
        "ANEUPLOIDY_LOH",
        "CNV_BURDEN",
        "RPPA_FINAL",
        "METHYLATION_MERGED_27K_450K",
    }
