from __future__ import annotations

from src.probe_chi_bio_gse98812_gene_namespace import GSE_SHA256, EXPECTED_GENE_ROWS


def test_namespace_probe_is_bound_to_frozen_source_without_expression_design() -> None:
    assert GSE_SHA256 == "1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5"
    assert EXPECTED_GENE_ROWS == 20_531
