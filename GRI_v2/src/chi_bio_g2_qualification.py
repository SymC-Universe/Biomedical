from __future__ import annotations

"""Synthetic qualification helpers for the approved G2 temporal comparator.

These functions do not fit SCC25 or TCGA. They expose exact unit-circle,
sampling-interval, non-normality, rank, and time-variation failure modes before
any outcome-bearing temporal analysis.
"""

from dataclasses import dataclass

import numpy as np

from src.chi_bio_candidate_math import spectral_radius
from src.chi_bio_identifiability import g2_reference_interval_value


@dataclass(frozen=True)
class G2NoisePilotSummary:
    truth_value: float
    sigma: float
    replicates: int
    seed: int
    median_estimate: float
    lower_2p5: float
    upper_97p5: float
    truth_covered: bool
    fraction_at_or_above_unity: float
    unity_disposition: str


def _square_finite(matrix: np.ndarray, name: str = "matrix") -> np.ndarray:
    arr = np.asarray(matrix, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
        raise ValueError(f"{name} must be a nonempty square 2D array")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr


def largest_singular_value(matrix: np.ndarray) -> float:
    arr = _square_finite(matrix)
    return float(np.linalg.svd(arr, compute_uv=False)[0])


def g2_interval_disposition(values: np.ndarray, *, boundary_tolerance: float = 1e-8) -> str:
    vals = np.asarray(values, dtype=float).reshape(-1)
    if vals.size == 0 or not np.all(np.isfinite(vals)):
        raise ValueError("values must be a nonempty finite vector")
    if boundary_tolerance < 0 or not np.isfinite(boundary_tolerance):
        raise ValueError("boundary_tolerance must be finite and nonnegative")
    lo, hi = np.quantile(vals, [0.025, 0.975])
    if lo <= 1.0 + boundary_tolerance and hi >= 1.0 - boundary_tolerance:
        return "UNCERTAINTY_SPANS_BOUNDARY"
    if hi < 1.0 - boundary_tolerance:
        return "BELOW_UNITY_RESOLVED"
    if lo > 1.0 + boundary_tolerance:
        return "ABOVE_UNITY_RESOLVED"
    return "UNCERTAINTY_SPANS_BOUNDARY"


def g2_entrywise_noise_pilot(
    truth_transition: np.ndarray,
    *,
    sigma: float,
    replicates: int,
    seed: int,
    boundary_tolerance: float = 1e-8,
) -> G2NoisePilotSummary:
    t = _square_finite(truth_transition, "truth_transition")
    if not np.isfinite(sigma) or sigma < 0:
        raise ValueError("sigma must be finite and nonnegative")
    if replicates < 2:
        raise ValueError("replicates must be >= 2")
    rng = np.random.default_rng(seed)
    estimates = np.empty(replicates, dtype=float)
    for i in range(replicates):
        estimates[i] = spectral_radius(t + rng.normal(0.0, sigma, size=t.shape))
    truth = spectral_radius(t)
    lo, med, hi = np.quantile(estimates, [0.025, 0.5, 0.975])
    return G2NoisePilotSummary(
        truth_value=float(truth),
        sigma=float(sigma),
        replicates=int(replicates),
        seed=int(seed),
        median_estimate=float(med),
        lower_2p5=float(lo),
        upper_97p5=float(hi),
        truth_covered=bool(lo <= truth <= hi),
        fraction_at_or_above_unity=float(np.mean(estimates >= 1.0 - boundary_tolerance)),
        unity_disposition=g2_interval_disposition(estimates, boundary_tolerance=boundary_tolerance),
    )


def sampling_interval_consistency(
    radii: list[float] | tuple[float, ...],
    intervals: list[float] | tuple[float, ...],
    *,
    reference_interval: float = 1.0,
    tolerance: float = 1e-8,
) -> tuple[float, ...]:
    """Return reference-interval values and require semigroup consistency.

    The check is deliberately strict for synthetic known-truth cases. Real data
    would require uncertainty-aware model checking, not this deterministic rule.
    """

    if len(radii) != len(intervals) or len(radii) < 2:
        raise ValueError("radii and intervals must have equal length >= 2")
    values = tuple(
        g2_reference_interval_value(r, observed_interval=d, reference_interval=reference_interval)
        for r, d in zip(radii, intervals)
    )
    if max(values) - min(values) > tolerance:
        raise ValueError("transition radii are inconsistent with a single semigroup rate")
    return values


def one_step_operator_residual(
    x_now: np.ndarray, x_next: np.ndarray, transition: np.ndarray
) -> float:
    x0 = np.asarray(x_now, dtype=float).reshape(-1)
    x1 = np.asarray(x_next, dtype=float).reshape(-1)
    t = _square_finite(transition, "transition")
    if x0.size != t.shape[0] or x1.size != t.shape[0]:
        raise ValueError("state vectors must match transition dimension")
    return float(np.linalg.norm(x1 - t @ x0))


def exact_shared_transition_exists(
    x_now: np.ndarray,
    x_next: np.ndarray,
    *,
    residual_tolerance: float = 1e-10,
) -> bool:
    """Test whether one least-squares T reproduces all supplied transitions exactly.

    Inputs are shaped (n_transitions, state_dimension). The function is for
    synthetic failure tests only; passing it is not sufficient for empirical
    identifiability or validation.
    """

    x0 = np.asarray(x_now, dtype=float)
    x1 = np.asarray(x_next, dtype=float)
    if x0.ndim != 2 or x1.ndim != 2 or x0.shape != x1.shape or x0.shape[0] < 1:
        raise ValueError("x_now and x_next must be equal nonempty 2D arrays")
    if residual_tolerance < 0 or not np.isfinite(residual_tolerance):
        raise ValueError("residual_tolerance must be finite and nonnegative")
    # Row-state convention: X_next ~= X_now @ T.T
    coef, *_ = np.linalg.lstsq(x0, x1, rcond=None)
    fitted = x0 @ coef
    residual = np.linalg.norm(x1 - fitted)
    return bool(residual <= residual_tolerance)
