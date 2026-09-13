import pytest

from src.validate_chi_bio_geo_source_probe import _gene_identity_status


def test_gene_identity_exact_match_passes_without_rewrite():
    result = _gene_identity_status(["TP53", "MIR1302-2HG"], ["TP53", "MIR1302-2HG"])
    assert result == {"status": "EXACT_ORDER_MATCH", "case_only_differences": 0}


def test_gene_identity_case_only_match_is_visible_not_rewritten():
    result = _gene_identity_status(
        ["TP53", "LOC100133331", "LINC00115"],
        ["TP53", "LOC100133331", "Linc00115"],
    )
    assert result["status"] == "CASE_ONLY_ORDER_MATCH"
    assert result["case_only_differences"] == 1
    assert result["case_only_preview"][0]["expression"] == "LINC00115"
    assert result["case_only_preview"][0]["feature"] == "Linc00115"


def test_gene_identity_difference_beyond_case_fails():
    with pytest.raises(RuntimeError, match="beyond capitalization"):
        _gene_identity_status(["TP53", "GENE_A"], ["TP53", "GENE_B"])


def test_gene_identity_row_count_difference_fails():
    with pytest.raises(RuntimeError, match="row counts differ"):
        _gene_identity_status(["TP53"], ["TP53", "MYC"])
