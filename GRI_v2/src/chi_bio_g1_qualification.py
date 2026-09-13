from __future__ import annotations

"""Candidate-specific diagnostics for the frozen G1/S1/L3 investigation.

These utilities operate on synthetic or independently supplied candidate
operators. They do not infer a GRI operator from TCGA and do not produce an
admitted biological Chi_bio value.
"""

from dataclasses import dataclass
from typing import Literal

import numpy as np

from src.chi_bio_candidate_math import spectral_abscissa


IntervalDisposition = Literal[
    "BELOW_UNITY_RESOLVED",
    "ABOVE_UNITY_RESOLVED",
    "UNCERTAINTY_SPANS_BOUNDARY",
    "AT_UNITY_WITHIN_TOLERANCE",
]


@dataclass(frozen=True)
class SpectralInterval:
    lower: float
    median: float
    upper: float
    disposition: IntervalDisposition


@dataclass(frozen=True)
class NoisePilotSummary:
    truth_value: float
    sigma: float
    replicates: int
    seed: int
    median_estimate: float
    median_error: float
    lower_2p5: float
    upper_97p5: float
    truth_covered: bool
    unity_disposition: IntervalDisposition
    fraction_at_or_above_unity: float


def _real_square_finite(matrix: np.ndarray, name: str = "matrix") -> np.ndarray:
    arr = np.asarray(matrix, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
        raise ValueError(f"{name} must be a nonempty square 2D array")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr


def continuous_time_numerical_abscissa(jacobian: np.ndarray) -> float:
    """Largest eigenvalue of (J+J.T)/2 for a real continuous-time Jacobian.

    A positive value exposes an instantaneous Euclidean growth direction even
    when the spectral abscissa is negative. This is a companion warning, not a
    replacement for asymptotic spectral stability.
    """

    j = _real_square_finite(jacobian, "jacobian")
    hermitian_part = 0.5 * (j + j.T)
    return float(np.max(np.linalg.eigvalsh(hermitian_part)))


def leading_realpart_gap(matrix: np.ndarray) -> float:
    """Gap between the largest and second-largest eigenvalue real parts."""

    arr = _real_square_finite(matrix)
    if arr.shape[0] < 2:
        return float("inf")
    realparts = np.sort(np.real(np.linalg.eigvals(arr)))[::-1]
    return float(realparts[0] - realparts[1])


def dominant_mode_status(matrix: np.ndarray, *, gap_tolerance: float = 1e-6) -> str:
    if gap_tolerance < 0 or not np.isfinite(gap_tolerance):
        raise ValueError("gap_tolerance must be finite and nonnegative")
    gap = leading_realpart_gap(matrix)
    if gap <= gap_tolerance:
        return "DOMINANT_SUBSPACE_NEAR_DEGENERATE"
    return "DOMINANT_MODE_SEPARATED"


def interval_relative_to_unity(
    values: np.ndarray, *, boundary_tolerance: float = 1e-8
) -> SpectralInterval:
    vals = np.asarray(values, dtype=float).reshape(-1)
    if vals.size == 0 or not np.all(np.isfinite(vals)):
        raise ValueError("values must be a nonempty finite vector")
    if boundary_tolerance < 0 or not np.isfinite(boundary_tolerance):
        raise ValueError("boundary_tolerance must be finite and nonnegative")

    lower, median, upper = np.quantile(vals, [0.025, 0.5, 0.975])
    lower = float(lower)
    median = float(median)
    upper = float(upper)

    if lower <= 1.0 + boundary_tolerance and upper >= 1.0 - boundary_tolerance:
        if (
            abs(lower - 1.0) <= boundary_tolerance
            and abs(median - 1.0) <= boundary_tolerance
            and abs(upper - 1.0) <= boundary_tolerance
        ):
            disposition: IntervalDisposition = "AT_UNITY_WITHIN_TOLERANCE"
        else:
            disposition = "UNCERTAINTY_SPANS_BOUNDARY"
    elif upper < 1.0 - boundary_tolerance:
        disposition = "BELOW_UNITY_RESOLVED"
    elif lower > 1.0 + boundary_tolerance:
        disposition = "ABOVE_UNITY_RESOLVED"
    else:
        disposition = "UNCERTAINTY_SPANS_BOUNDARY"

    return SpectralInterval(lower=lower, median=median, upper=upper, disposition=disposition)


def g1a_entrywise_noise_pilot(
    truth_matrix_m: np.ndarray,
    *,
    sigma: float,
    replicates: int,
    seed: int,
    boundary_tolerance: float = 1e-8,
) -> NoisePilotSummary:
    """Run a deterministic synthetic perturbation pilot around a G1A truth M."""

    m = _real_square_finite(truth_matrix_m, "truth_matrix_m")
    if not np.isfinite(sigma) or sigma < 0:
        raise ValueError("sigma must be finite and nonnegative")
    if replicates < 2:
        raise ValueError("replicates must be >= 2")

    rng = np.random.default_rng(seed)
    estimates = np.empty(replicates, dtype=float)
    for i in range(replicates):
        noisy = m + rng.normal(loc=0.0, scale=sigma, size=m.shape)
        estimates[i] = spectral_abscissa(noisy)

    truth = spectral_abscissa(m)
    interval = interval_relative_to_unity(estimates, boundary_tolerance=boundary_tolerance)
    return NoisePilotSummary(
        truth_value=float(truth),
        sigma=float(sigma),
        replicates=int(replicates),
        seed=int(seed),
        median_estimate=interval.median,
        median_error=float(interval.median - truth),
        lower_2p5=interval.lower,
        upper_97p5=interval.upper,
        truth_covered=bool(interval.lower <= truth <= interval.upper),
        unity_disposition=interval.disposition,
        fraction_at_or_above_unity=float(np.mean(estimates >= 1.0 - boundary_tolerance)),
    )
