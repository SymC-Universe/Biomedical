from __future__ import annotations

from src.probe_chi_bio_b3_network_gene_overlap import (
    DOROTHEA_CONFIDENCE_DENOMINATOR,
    DOROTHEA_LEVELS,
    GSE_SHA256,
    TMIN,
)


def test_b3_overlap_gate_is_outcome_independent_and_predeclared() -> None:
    assert TMIN == 5
    assert DOROTHEA_LEVELS == ("A", "B", "C")
    assert DOROTHEA_CONFIDENCE_DENOMINATOR == {"A": 1.0, "B": 2.0, "C": 3.0}


def test_b3_overlap_probe_is_bound_to_frozen_gse98812_source() -> None:
    assert GSE_SHA256 == "1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5"
