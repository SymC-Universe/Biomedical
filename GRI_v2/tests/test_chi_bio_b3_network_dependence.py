from __future__ import annotations

from src.probe_chi_bio_b3_network_dependence import (
    CHRONIC_LOTO_TRAIN_ROWS,
    CHRONIC_TRANSITIONS,
    D1_MAX_UNREGULARIZED_RANK_LOTO,
    D2_MAX_UNREGULARIZED_RANK_LOTO,
)


def test_chronic_algebraic_capacity_is_derived_from_frozen_geometry() -> None:
    assert CHRONIC_TRANSITIONS == 20
    assert CHRONIC_LOTO_TRAIN_ROWS == 19
    assert D1_MAX_UNREGULARIZED_RANK_LOTO == 17
    assert D2_MAX_UNREGULARIZED_RANK_LOTO == 8


def test_d2_ceiling_is_row_count_constraint_not_selected_dimension() -> None:
    for rank in range(1, D2_MAX_UNREGULARIZED_RANK_LOTO + 1):
        assert 2 * rank + 2 <= CHRONIC_LOTO_TRAIN_ROWS
    assert 2 * (D2_MAX_UNREGULARIZED_RANK_LOTO + 1) + 2 > CHRONIC_LOTO_TRAIN_ROWS
