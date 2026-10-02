"""Qualification-only one-mode continuous-lineage C candidate.

This module is not part of the production A0/A1/A2 family. It exists only to
test whether adding the single covariance-phase / continuous-lineage nuisance
coordinate g removes false model-order pressure for valid one-mode C truths.

Underdamped parameterization:
    A in (0,1)
    rho in (0,1)
    f_d in (fmin,fmax)
    g in (-1,1)

with
    alpha = -log(rho) * fs
    nu = 2*pi*f_d
    G = g*A*alpha
    K = [[-alpha,-1],[nu^2,-alpha]]
    D* = A*(2*alpha^2 + nu^2)
    P = [[A,-G],[-G,D*]]
    Qc = -(K P + P K^T)
    F = expm(K/fs)
    Qd = P - F P F^T
    R = 1-A.

For |g|<=1 this is inside the continuous-time embeddable C family. The scalar
output uses observation [1,0]. The fitted chi is alpha/sqrt(alpha^2+nu^2).

No real EEG admission, production promotion, or threshold is defined here.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from scipy.linalg import expm, solve_discrete_are
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
class ContinuousLineageCandidateFit:
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


def _g_from_raw(value: float) -> float:
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
    g = _g_from_raw(float(raw[3]))

    alpha = -math.log(rho) * sampling_rate_hz
    nu = 2.0 * math.pi * damped_frequency_hz
    G = g * A * alpha
    D = A * (2.0 * alpha * alpha + nu * nu)

    K = np.asarray(
        [[-alpha, -1.0], [nu * nu, -alpha]],
        dtype=np.float64,
    )
    P = np.asarray([[A, -G], [-G, D]], dtype=np.float64)
    transition = expm(K / sampling_rate_hz)
    process_cov = P - transition @ P @ transition.T
    process_cov = 0.5 * (process_cov + process_cov.T)
    observation = np.asarray([1.0, 0.0], dtype=np.float64)
    observation_variance = 1.0 - A

    min_q = float(np.min(np.linalg.eigvalsh(process_cov)))
    if min_q < -1e-8:
        raise ValueError("candidate discrete process covariance is not PSD")
    if min_q < 0.0:
        values, vectors = np.linalg.eigh(process_cov)
        process_cov = vectors @ np.diag(np.clip(values, 0.0, None)) @ vectors.T

    natural_omega = math.hypot(alpha, nu)
    theta = nu / sampling_rate_hz
    H = G * math.sin(theta) / nu
    parameters = {
        "latent_fraction": float(A),
        "rho": float(rho),
        "g": float(g),
        "H": float(H),
        "decay_rate_per_s": float(alpha),
        "damped_frequency_hz": float(damped_frequency_hz),
        "natural_frequency_hz": float(natural_omega / (2.0 * math.pi)),
        "damping_ratio": float(alpha / natural_omega),
    }
    return transition, process_cov, observation, observation_variance, parameters


def _steady_state(raw, sampling_rate_hz, fmin_hz, fmax_hz):
    try:
        transition, process_cov, observation, observation_variance, parameters = (
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
        0.5 * used.size * (
            math.log(2.0 * math.pi) + math.log(innovation_variance)
        )
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
    g_starts = (0.0, -0.6, 0.6)
    starts = []
    for frequency in frequencies[:8]:
        for A, rho in profiles:
            for g in g_starts:
                raw_g = np.arctanh(np.clip(g, -0.999999, 0.999999))
                starts.append(
                    np.asarray(
                        [
                            _raw_fraction(A),
                            _raw_rho(rho),
                            _raw_frequency(frequency, fmin_hz, fmax_hz),
                            raw_g,
                        ],
                        dtype=np.float64,
                    )
                )
    return starts


def _select_legacy_optimized_starts(
    standardized: np.ndarray,
    sampling_rate_hz: float,
    fmin_hz: float,
    fmax_hz: float,
    burn_in_samples: int,
    max_optimized_starts: int,
):
    """Return the exact legacy C1Q start ranking used before C1Q-RS.

    This helper is a mechanical factoring of the historical inline selection
    logic. It does not change start generation, scoring, ranking, fallback, or
    optimizer settings. C1Q-RS uses it so the augmented route contains rather
    than reimplements the legacy optimized-start set.
    """
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
    if scored:
        selected = [x for _, x in scored[:max_optimized_starts]]
        next_ranked = (
            scored[max_optimized_starts][1]
            if len(scored) > max_optimized_starts
            else None
        )
    else:
        selected = candidates[:max_optimized_starts]
        next_ranked = (
            candidates[max_optimized_starts]
            if len(candidates) > max_optimized_starts
            else None
        )
    return {
        "candidates": candidates,
        "scored": scored,
        "selected": selected,
        "next_ranked": next_ranked,
    }


def fit_continuous_lineage_candidate(
    signal: Sequence[float],
    sampling_rate_hz: float,
    *,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
    min_samples: int = 1024,
    burn_in_samples: int = 128,
    optimizer_maxiter: int = 80,
    max_optimized_starts: int = 18,
) -> ContinuousLineageCandidateFit:
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

    selection = _select_legacy_optimized_starts(
        standardized,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
        burn_in_samples,
        max_optimized_starts,
    )
    starts = selection["selected"]

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
        raise RuntimeError("continuous-lineage candidate produced no finite solution")
    best = min(solutions, key=lambda item: float(item.fun))
    steady = _steady_state(
        np.asarray(best.x, dtype=np.float64),
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
    )
    if steady is None:
        raise RuntimeError("best continuous-lineage candidate is invalid")
    _, _, _, parameters = steady

    effective_n = int(values.size - burn_in_samples)
    nll = float(best.fun)
    parameter_count = 4
    bic = float(2.0 * nll + parameter_count * math.log(effective_n))
    return ContinuousLineageCandidateFit(
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
