"""Mechanical contracts for the qualification-only C1Q-RS search route."""

from __future__ import annotations

import math

import numpy as np

from nsd_engine.continuous_lineage_candidate import (
    _initial_starts,
    _nll,
    _select_legacy_optimized_starts,
    fit_continuous_lineage_candidate,
)
from nsd_engine.continuous_lineage_candidate_rs import (
    fit_continuous_lineage_candidate_rs,
)


def _signal(fs: float = 128.0, n: int = 2048) -> np.ndarray:
    rng = np.random.default_rng(20260927)
    t = np.arange(n, dtype=float) / fs
    return (
        0.8 * np.sin(2.0 * np.pi * 9.0 * t)
        + 0.25 * np.sin(2.0 * np.pi * 17.0 * t + 0.4)
        + rng.normal(0.0, 0.45, size=n)
    )


def _historical_inline_selection(
    standardized: np.ndarray,
    fs: float,
    fmin: float,
    fmax: float,
    burn: int,
    maximum: int,
):
    candidates = _initial_starts(standardized, fs, fmin, fmax)
    scored = []
    for start in candidates:
        value = _nll(standardized, start, fs, fmin, fmax, burn)
        if math.isfinite(value) and value < 1e90:
            scored.append((value, start))
    scored.sort(key=lambda item: item[0])
    starts = [x for _, x in scored[:maximum]]
    if not starts:
        starts = candidates[:maximum]
    next_ranked = (
        scored[maximum][1]
        if scored and len(scored) > maximum
        else (
            candidates[maximum]
            if not scored and len(candidates) > maximum
            else None
        )
    )
    return starts, next_ranked


def test_shared_legacy_selection_matches_historical_inline_algorithm():
    signal = _signal()
    standardized = (signal - np.mean(signal)) / np.std(signal)
    fs = 128.0
    fmin = 1.0
    fmax = 45.0
    burn = 128
    maximum = 7

    expected, expected_next = _historical_inline_selection(
        standardized, fs, fmin, fmax, burn, maximum
    )
    actual = _select_legacy_optimized_starts(
        standardized, fs, fmin, fmax, burn, maximum
    )

    assert len(actual["selected"]) == len(expected)
    for got, want in zip(actual["selected"], expected):
        np.testing.assert_array_equal(got, want)

    if expected_next is None:
        assert actual["next_ranked"] is None
    else:
        np.testing.assert_array_equal(actual["next_ranked"], expected_next)


def test_rs_contains_legacy_search_and_preserves_parameter_count():
    signal = _signal()
    legacy = fit_continuous_lineage_candidate(
        signal,
        128.0,
        optimizer_maxiter=8,
        max_optimized_starts=4,
    )
    rs = fit_continuous_lineage_candidate_rs(
        signal,
        128.0,
        optimizer_maxiter=8,
        max_optimized_starts=4,
    )

    assert legacy.parameter_count == 4
    assert rs.parameter_count == 4
    assert rs.legacy_attempted_start_count == legacy.attempted_start_count
    assert abs(
        rs.legacy_best_negative_log_likelihood
        - legacy.negative_log_likelihood
    ) <= 1e-8 * max(1.0, abs(legacy.negative_log_likelihood))
    assert rs.negative_log_likelihood <= (
        legacy.negative_log_likelihood
        + 1e-8 * max(1.0, abs(legacy.negative_log_likelihood))
    )
    assert rs.attempted_start_count in {
        rs.legacy_attempted_start_count,
        rs.legacy_attempted_start_count + 1,
    }


def test_rs_bic_uses_same_four_parameter_penalty():
    signal = _signal()
    rs = fit_continuous_lineage_candidate_rs(
        signal,
        128.0,
        optimizer_maxiter=5,
        max_optimized_starts=3,
    )
    expected = (
        2.0 * rs.negative_log_likelihood
        + 4.0 * math.log(rs.effective_sample_count)
    )
    assert abs(rs.bic - expected) <= 1e-10 * max(1.0, abs(expected))
