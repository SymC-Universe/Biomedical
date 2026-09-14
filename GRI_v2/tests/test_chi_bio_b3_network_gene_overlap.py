from __future__ import annotations

from src.probe_chi_bio_b3_network_gene_overlap import (
    CANONICAL_B3_OVERLAP_PROBE,
    DOROTHEA_CONFIDENCE_DENOMINATOR,
    DOROTHEA_LEVELS,
    GSE_SHA256,
    RAW_NAMESPACE_DIAGNOSTIC_STATUS,
    TMIN,
)


def test_b3_raw_namespace_diagnostic_gate_is_outcome_independent_and_predeclared() -> None:
    assert TMIN == 5
    assert DOROTHEA_LEVELS == ("A", "B", "C")
    assert DOROTHEA_CONFIDENCE_DENOMINATOR == {"A": 1.0, "B": 2.0, "C": 3.0}


def test_b3_raw_namespace_diagnostic_is_bound_to_frozen_gse98812_source() -> None:
    assert GSE_SHA256 == "1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5"


def test_b3_raw_namespace_diagnostic_cannot_be_mistaken_for_support_qualification() -> None:
    assert RAW_NAMESPACE_DIAGNOSTIC_STATUS == "DIAGNOSTIC_B3_RAW_IDENTIFIER_NAMESPACE_MISMATCH_EXPECTED"
    assert CANONICAL_B3_OVERLAP_PROBE == "src.probe_chi_bio_b3_network_symbol_mapping"
