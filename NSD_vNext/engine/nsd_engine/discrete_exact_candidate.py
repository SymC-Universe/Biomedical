"""Qualification-only one-mode discrete exact-image D candidate.

D1Q spans the underdamped discrete exact white-Q image in regular covariance
coordinates. It is a control model for C1Q family-scope qualification and is
not part of production A0/A1/A2.

Parameters:
    A      standardized latent fraction
    rho    discrete pole radius
    f_d    damped frequency
    h      H / (A sinh L), constrained to (-1,1)

where L=-log(rho). The exact D boundary is |h|<=1. The implied continuous
coordinate

    g = (H/A) * theta / (L sin theta)

is reported without constraining |g|<=1. Thus D1Q can expose a one-mode
solution that is valid in discrete time but outside the prospective
continuous-lineage C family.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from scipy.linalg import solve_discrete_are
from scipy.optimize import minimize
from scipy.signal import lfilter, ss2tf

from .state_space_adequacy import (
    _frequency_from_raw,
    _fraction_from_raw,
    _raw_fraction,
    _raw_frequency,
    _raw_rho,
    _rho_from_raw,
    _spectral_seed_frequencies,
)


@dataclass(frozen=True)
class DiscreteExactCandidateFit:
    success: bool
    sample_count: int
    effective_sample_count: int
    burn_in_samples: int
    parameter_count: int
    negative_log_likelihood: float
    bic: float
    parameters: dict[str, float]
    raw_parameters: tuple[float, ...]
    attempted_start_count: int
    converged_start_count: int
    optimizer_message: str


def _h_from_raw(value: float) -> float:
    return math.tanh(float(value))


def _build_candidate(
    raw: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
):
    A = _fraction_from_raw(float(raw[0]))
    rho = _rho_from_raw(float(raw[1]))
    damped_frequency_hz = _frequency_from_raw(
        float(raw[2]), fmin_hz, fmax_hz
    )
    h = _h_from_raw(float(raw[3]))

    L = -math.log(rho)
    theta = 2.0 * math.pi * damped_frequency_hz / sampling_rate_hz
    xi = math.cos(theta)
    sin_theta = math.sin(theta)
    H_D = A * math.sinh(L)
    H = h * H_D

    transition = rho * np.asarray(
        [[xi, -1.0], [1.0 - xi * xi, xi]],
        dtype=np.float64,
    )
    D = A * (
        (1.0 + rho**4) - 2.0 * rho * rho * xi * xi
    ) / (2.0 * rho * rho)
    stationary_cov = np.asarray(
        [[A, -H], [-H, D]],
        dtype=np.float64,
    )
    process_cov = stationary_cov - transition @ stationary_cov @ transition.T
    process_cov = 0.5 * (process_cov + process_cov.T)
    observation = np.asarray([1.0, 0.0], dtype=np.float64)
    observation_variance = 1.0 - A

    min_q = float(np.min(np.linalg.eigvalsh(process_cov)))
    if min_q < -1e-8:
        raise ValueError("D1Q process covariance is not PSD")
    if min_q < 0.0:
        values, vectors = np.linalg.eigh(process_cov)
        process_cov = vectors @ np.diag(np.clip(values, 0.0, None)) @ vectors.T

    if abs(sin_theta) <= 1e-14:
        implied_g = float("nan")
    else:
        implied_g = (H / A) * theta / (L * sin_theta)
    chi = L / math.sqrt(L * L + theta * theta)
    natural_frequency_hz = (
        math.sqrt((L * sampling_rate_hz) ** 2
                  + (theta * sampling_rate_hz) ** 2)
        / (2.0 * math.pi)
    )

    parameters = {
        "latent_fraction": float(A),
        "rho": float(rho),
        "h": float(h),
        "H": float(H),
        "implied_continuous_g": float(implied_g),
        "continuous_embeddable_by_point": float(
            math.isfinite(implied_g) and abs(implied_g) <= 1.0
        ),
        "decay_rate_per_s": float(L * sampling_rate_hz),
        "damped_frequency_hz": float(damped_frequency_hz),
        "natural_frequency_hz": float(natural_frequency_hz),
        "damping_ratio": float(chi),
    }
    return (
        transition,
        process_cov,
        observation,
        observation_variance,
        stationary_cov,
        parameters,
    )


def _steady_state(raw, sampling_rate_hz, fmin_hz, fmax_hz):
    try:
        transition, process_cov, observation, observation_variance, _, parameters = (
            _build_candidate(raw, sampling_rate_hz, fmin_hz, fmax_hz)
        )
        predicted_cov = solve_discrete_are(
            transition.T,
            observation.reshape(-1, 1),
            process_cov,
            np.asarray([[observation_variance]], dtype=np.float64),
        )
    except Exception:
        return None

    innovation_variance = float(
        observation @ predicted_cov @ observation + observation_variance
    )
    if not math.isfinite(innovation_variance) or innovation_variance <= 1e-12:
        return None

    gain = (predicted_cov @ observation) / innovation_variance
    predictor_transition = transition @ (
        np.eye(transition.shape[0]) - np.outer(gain, observation)
    )
    predictor_input = (transition @ gain).reshape(-1, 1)
    numerator, denominator = ss2tf(
        predictor_transition,
        predictor_input,
        observation.reshape(1, -1),
        np.asarray([[0.0]], dtype=np.float64),
    )
    numerator = np.asarray(numerator[0], dtype=np.float64)
    denominator = np.asarray(denominator, dtype=np.float64)
    if not np.isfinite(numerator).all() or not np.isfinite(denominator).all():
        return None
    return numerator, denominator, innovation_variance, parameters


def _nll(
    standardized: np.ndarray,
    raw: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
    burn_in_samples: int,
) -> float:
    steady = _steady_state(raw, sampling_rate_hz, fmin_hz, fmax_hz)
    if steady is None:
        return 1e100
    numerator, denominator, innovation_variance, _ = steady
    prediction = lfilter(numerator, denominator, standardized)
    innovation = standardized - prediction
    used = innovation[burn_in_samples:]
    if used.size < 3 or not np.isfinite(used).all():
        return 1e100
    return float(
        0.5 * used.size
        * (math.log(2.0 * math.pi) + math.log(innovation_variance))
        + 0.5 * np.dot(used, used) / innovation_variance
    )


def _initial_starts(
    standardized: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
):
    frequencies = _spectral_seed_frequencies(
        standardized,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
        maximum=10,
    )
    profiles = (
        (0.80, 0.94),
        (0.80, 0.88),
        (0.60, 0.94),
    )
    h_starts = (0.0, -0.7, 0.7)
    starts = []
    for frequency in frequencies[:8]:
        for A, rho in profiles:
            for h in h_starts:
                starts.append(
                    np.asarray(
                        [
                            _raw_fraction(A),
                            _raw_rho(rho),
                            _raw_frequency(frequency, fmin_hz, fmax_hz),
                            np.arctanh(np.clip(h, -0.999999, 0.999999)),
                        ],
                        dtype=np.float64,
                    )
                )
    return starts


def fit_discrete_exact_candidate(
    signal: Sequence[float],
    sampling_rate_hz: float,
    *,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
    min_samples: int = 1024,
    burn_in_samples: int = 128,
    optimizer_maxiter: int = 80,
    max_optimized_starts: int = 18,
) -> DiscreteExactCandidateFit:
    values = np.asarray(signal, dtype=np.float64)
    if values.ndim != 1:
        raise ValueError("signal must be one-dimensional")
    if values.size < min_samples:
        raise ValueError(f"signal requires at least {min_samples} samples")
    if not np.isfinite(values).all():
        raise ValueError("signal contains non-finite samples")
    if not 0.0 < fmin_hz < fmax_hz < sampling_rate_hz / 2.0:
        raise ValueError("frequency bounds must satisfy 0 < fmin < fmax < Nyquist")
    if not 0 <= burn_in_samples < values.size - 3:
        raise ValueError("burn_in_samples leaves too few likelihood samples")

    mean = float(np.mean(values))
    sd = float(np.std(values))
    if not math.isfinite(sd) or sd <= 0.0:
        raise ValueError("signal has zero or non-finite standard deviation")
    standardized = (values - mean) / sd

    candidates = _initial_starts(
        standardized, sampling_rate_hz, fmin_hz, fmax_hz
    )
    scored = []
    for start in candidates:
        value = _nll(
            standardized,
            start,
            sampling_rate_hz,
            fmin_hz,
            fmax_hz,
            burn_in_samples,
        )
        if math.isfinite(value) and value < 1e90:
            scored.append((value, start))
    scored.sort(key=lambda item: item[0])
    starts = [x for _, x in scored[:max_optimized_starts]]
    if not starts:
        starts = candidates[:max_optimized_starts]

    solutions = []
    for start in starts:
        result = minimize(
            lambda raw: _nll(
                standardized,
                raw,
                sampling_rate_hz,
                fmin_hz,
                fmax_hz,
                burn_in_samples,
            ),
            start,
            method="L-BFGS-B",
            bounds=[(-8.0, 8.0)] * 4,
            options={"maxiter": optimizer_maxiter, "ftol": 1e-8, "maxls": 30},
        )
        if math.isfinite(float(result.fun)):
            solutions.append(result)

    if not solutions:
        raise RuntimeError("D1Q produced no finite solution")
    best = min(solutions, key=lambda item: float(item.fun))
    steady = _steady_state(
        np.asarray(best.x, dtype=np.float64),
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )
    if steady is None:
        raise RuntimeError("best D1Q solution is invalid")
    _, _, _, parameters = steady

    effective_n = int(values.size - burn_in_samples)
    nll = float(best.fun)
    parameter_count = 4
    bic = float(2.0 * nll + parameter_count * math.log(effective_n))
    return DiscreteExactCandidateFit(
        success=bool(best.success),
        sample_count=int(values.size),
        effective_sample_count=effective_n,
        burn_in_samples=int(burn_in_samples),
        parameter_count=parameter_count,
        negative_log_likelihood=nll,
        bic=bic,
        parameters={k: float(v) for k, v in parameters.items()},
        raw_parameters=tuple(float(v) for v in best.x),
        attempted_start_count=len(starts),
        converged_start_count=sum(1 for x in solutions if bool(x.success)),
        optimizer_message=str(best.message),
    )
