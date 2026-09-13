from __future__ import annotations

from src.probe_chi_bio_b3_network_symbol_mapping import GSE_SHA256, TMIN


def test_b3_symbol_mapping_is_bound_to_frozen_source_and_tmin() -> None:
    assert GSE_SHA256 == "1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5"
    assert TMIN == 5
