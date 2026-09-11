import numpy as np

from src.chi_conglomerate import chi_from_pole_pair, second_order_generator
from src.pole_lineage import (
    advance_two_lineages,
    count_valid_second_order_partitions,
    initial_two_lineages,
)


def _poles(chi_low, chi_high=0.55):
    low = np.linalg.eigvals(second_order_generator(chi_low, 2.0 * np.pi * 2.0))
    high = np.linalg.eigvals(second_order_generator(chi_high, 2.0 * np.pi * 7.0))
    return low, high


def test_initializer_recovers_low_and_high_natural_scale_without_truth_labels():
    low, high = _poles(0.7)
    mixed = np.array([high[1], low[0], high[0], low[1]])
    init = initial_two_lineages(mixed)
    a = chi_from_pole_pair(init["pairs"][0])
    b = chi_from_pole_pair(init["pairs"][1])
    assert np.isclose(a["chi"], 0.7)
    assert np.isclose(b["chi"], 0.55)
    assert a["omega_n"] < b["omega_n"]


def test_continuity_tracks_low_lineage_through_repeated_root_and_real_split():
    low, high = _poles(0.7)
    init = initial_two_lineages(np.array([low[1], high[0], low[0], high[1]]))
    previous = init["pairs"]
    for i, chi in enumerate([0.85, 0.97, 1.0, 1.03, 1.15, 1.3]):
        low, high = _poles(chi)
        orderings = [
            np.array([high[1], low[0], high[0], low[1]]),
            np.array([low[1], high[1], low[0], high[0]]),
        ]
        step = advance_two_lineages(previous, orderings[i % 2])
        tracked = chi_from_pole_pair(step["pairs"][0])
        assert np.isclose(tracked["chi"], chi, atol=1e-10, rtol=1e-10)
        previous = step["pairs"]


def test_static_partition_count_is_one_with_one_complex_anchor():
    low, high = _poles(1.3)
    out = count_valid_second_order_partitions(np.array([low[0], high[0], low[1], high[1]]))
    assert out["count"] == 1
