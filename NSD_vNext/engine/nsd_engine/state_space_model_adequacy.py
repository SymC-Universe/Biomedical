"""Qualification-stage native state-space model competition for NSD.

This module implements the next P0-Q modal-adequacy layer after the narrow
M2 covariance route demonstrated that mechanical single-oscillator fits can
admit nonoscillatory, multimode, nonstationary, and colored-noise adversaries.

The candidate families are deliberately native and explicit:

A0: one nonoscillatory latent AR(1)/relaxation state + white observation noise.
A1: one two-dimensional damped-rotation latent oscillator + white observation noise.
A2: two independent two-dimensional damped-rotation latent oscillators observed
    through one scalar channel + white observation noise.

All three candidates are evaluated with the exact Gaussian innovations
likelihood from a Kalman filter. BIC/AIC values therefore refer to the sample
likelihood, unlike the earlier covariance-lag pseudo-BIC diagnostics.

This remains qualification code. A best-scoring candidate is not automatically
an admitted biological mode, damping ratio, or chi. Admission/refusal rules
must be frozen only after known-truth operating-region, residual, stationarity,
identifiability, and held-out qualification.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math
from typing import Sequence

import numpy as np
from scipy.linalg import solve_discrete_lyapunov
from scipy.optimize import minimize


class StateSpaceFamily(str, Enum):
    A0_RELAXATION = "A0_RELAXATION"
    A1_SINGLE_OSCILLATOR = "A1_SINGLE_OSCILLATOR"
    A2_TWO_OSCILLATORS = "A2_TWO_OSCILLATORS"


@dataclass(frozen=True)
class StateSpaceMode:
    frequency_hz: float
    rho: float
    decay_rate_per_s: float
    natural_frequency_hz: float
    damping_ratio: float
    process_variance: float

    def __post_init__(self) -> None:
        values = (
            self.frequency_hz,
            self.rho,
            self.decay_rate_per_s,
            self.natural_frequency_hz,
            self.damping_ratio,
            self.process_variance,
        )
        if any(not math.isfinite(v) for v in values):
            raise ValueError("mode fields must be finite")
        if self.frequency_hz <= 0 or self.natural_frequency_hz <= 0:
            raise ValueError("mode frequencies must be > 0")
        if not 0 < self.rho < 1:
            raise ValueError("rho must satisfy 0 < rho < 1")
        if not 0 < self.damping_ratio < 1:
            raise ValueError("damping_ratio must satisfy 0 < zeta < 1")
        if self.process_variance <= 0:
            raise ValueError("process_variance must be > 0")


@dataclass(frozen=True)
class StateSpaceCandidateFit:
    family: StateSpaceFamily
    converged: bool
    sample_count: int
    parameter_count: int
    negative_log_likelihood: float
    bic: float
    aic: float
    heldout_negative_log_likelihood_per_sample: float | None
    observation_noise_variance: float
    relaxation_phi: float | None
    process_variances: tuple[float, ...]
    modes: tuple[StateSpaceMode, ...]
    optimizer_message: str
    optimizer_iterations: int | None

    def __post_init__(self) -> None:
        if self.sample_count < 4:
            raise ValueError("sample_count must be >= 4")
        for value in (
            self.negative_log_likelihood,
            self.bic,
            self.aic,
            self.observation_noise_variance,
        ):
            if not math.isfinite(value):
                raise ValueError("fit summary must be finite")
        if self.observation_noise_variance <= 0:
            raise ValueError("observation_noise_variance must be > 0")
        if self.heldout_negative_log_likelihood_per_sample is not None and not math.isfinite(
            self.heldout_negative_log_likelihood_per_sample
        ):
            raise ValueError("heldout likelihood must be finite when present")


def _standardize(signal: Sequence[float]) -> np.ndarray:
    values = np.asarray(signal, dtype=np.float64)
    if values.ndim != 1 or values.size < 4:
        raise ValueError("signal must be a one-dimensional sequence with at least four samples")
    if not np.isfinite(values).all():
        raise ValueError("signal must contain only finite samples")
    centered = values - float(np.mean(values))
    scale = float(np.std(centered))
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("signal variance must be finite and > 0")
    return centered / scale


def _rotation_transition(rho: float, theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return rho * np.asarray([[c, -s], [s, c]], dtype=np.float64)


def _stationary_covariance(a: np.ndarray, q: np.ndarray) -> np.ndarray:
    try:
        p = solve_discrete_lyapunov(a, q)
    except Exception as exc:
        raise ValueError("stationary covariance could not be solved") from exc
    p = 0.5 * (p + p.T)
    if not np.isfinite(p).all():
        raise ValueError("stationary covariance is non-finite")
    eig = np.linalg.eigvalsh(p)
    if float(np.min(eig)) <= 0:
        raise ValueError("stationary covariance is not positive definite")
    return p


def kalman_innovations_nll(
    signal: Sequence[float],
    transition: np.ndarray,
    process_covariance: np.ndarray,
    observation: np.ndarray,
    observation_noise_variance: float,
) -> float:
    """Return exact scalar-observation Gaussian innovations negative log likelihood."""
    y = np.asarray(signal, dtype=np.float64)
    if y.ndim != 1 or y.size < 2 or not np.isfinite(y).all():
        raise ValueError("signal must be finite one-dimensional data")
    a = np.asarray(transition, dtype=np.float64)
    q = np.asarray(process_covariance, dtype=np.float64)
    h = np.asarray(observation, dtype=np.float64).reshape(1, -1)
    n_state = a.shape[0]
    if a.shape != (n_state, n_state) or q.shape != a.shape or h.shape[1] != n_state:
        raise ValueError("state-space matrix dimensions are inconsistent")
    if not math.isfinite(observation_noise_variance) or observation_noise_variance <= 0:
        raise ValueError("observation_noise_variance must be finite and > 0")
    if float(np.max(np.abs(np.linalg.eigvals(a)))) >= 1:
        raise ValueError("transition must be asymptotically stable")

    p = _stationary_covariance(a, q)
    m = np.zeros(n_state, dtype=np.float64)
    nll = 0.0
    log_2pi = math.log(2.0 * math.pi)

    for value in y:
        hp = h @ p
        innovation_variance = float(hp @ h.T) + observation_noise_variance
        if not math.isfinite(innovation_variance) or innovation_variance <= 1e-12:
            return float("inf")
        innovation = float(value - (h @ m)[0])
        nll += 0.5 * (
            log_2pi
            + math.log(innovation_variance)
            + innovation * innovation / innovation_variance
        )

        gain = (p @ h.T)[:, 0] / innovation_variance
        m_post = m + gain * innovation
        p_post = p - np.outer(gain, hp[0])
        p_post = 0.5 * (p_post + p_post.T)

        m = a @ m_post
        p = a @ p_post @ a.T + q
        p = 0.5 * (p + p.T)

    return float(nll)


def _fft_candidates(values: np.ndarray, fs: float, fmin: float, fmax: float) -> list[float]:
    power = np.abs(np.fft.rfft(values)) ** 2
    freq = np.fft.rfftfreq(values.size, d=1.0 / fs)
    mask = (freq >= fmin) & (freq <= fmax)
    freq = freq[mask]
    power = power[mask]
    if freq.size == 0:
        return [0.5 * (fmin + fmax)]
    order = np.argsort(power)[::-1]
    chosen: list[float] = []
    minimum_separation = max(0.5, 2.0 * fs / values.size)
    for index in order:
        candidate = float(freq[int(index)])
        if all(abs(candidate - old) >= minimum_separation for old in chosen):
            chosen.append(candidate)
        if len(chosen) >= 5:
            break
    return chosen or [0.5 * (fmin + fmax)]


def _physical_model(
    family: StateSpaceFamily,
    parameters: np.ndarray,
    fs: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float | None, tuple[StateSpaceMode, ...], tuple[float, ...]]:
    if family is StateSpaceFamily.A0_RELAXATION:
        phi, log_q, log_r = (float(v) for v in parameters)
        q0 = math.exp(log_q)
        r = math.exp(log_r)
        a = np.asarray([[phi]], dtype=np.float64)
        q = np.asarray([[q0]], dtype=np.float64)
        h = np.asarray([1.0], dtype=np.float64)
        return a, q, h, r, phi, (), (q0,)

    if family is StateSpaceFamily.A1_SINGLE_OSCILLATOR:
        rho, theta, log_q, log_r = (float(v) for v in parameters)
        q0 = math.exp(log_q)
        r = math.exp(log_r)
        a = _rotation_transition(rho, theta)
        q = np.eye(2, dtype=np.float64) * q0
        h = np.asarray([1.0, 0.0], dtype=np.float64)
        mode = _mode_from_discrete(rho, theta, q0, fs)
        return a, q, h, r, None, (mode,), (q0,)

    if family is StateSpaceFamily.A2_TWO_OSCILLATORS:
        rho1, theta1, log_q1, rho2, theta2, log_q2, log_r = (
            float(v) for v in parameters
        )
        q1 = math.exp(log_q1)
        q2 = math.exp(log_q2)
        r = math.exp(log_r)
        a = np.zeros((4, 4), dtype=np.float64)
        a[:2, :2] = _rotation_transition(rho1, theta1)
        a[2:, 2:] = _rotation_transition(rho2, theta2)
        q = np.diag([q1, q1, q2, q2]).astype(np.float64)
        h = np.asarray([1.0, 0.0, 1.0, 0.0], dtype=np.float64)
        modes = sorted(
            (
                _mode_from_discrete(rho1, theta1, q1, fs),
                _mode_from_discrete(rho2, theta2, q2, fs),
            ),
            key=lambda item: item.frequency_hz,
        )
        return a, q, h, r, None, tuple(modes), (q1, q2)

    raise ValueError(f"unsupported model family: {family}")


def _mode_from_discrete(rho: float, theta: float, q: float, fs: float) -> StateSpaceMode:
    decay = -math.log(rho) * fs
    damped_omega = theta * fs
    natural_omega = math.hypot(decay, damped_omega)
    zeta = decay / natural_omega
    return StateSpaceMode(
        frequency_hz=damped_omega / (2.0 * math.pi),
        rho=rho,
        decay_rate_per_s=decay,
        natural_frequency_hz=natural_omega / (2.0 * math.pi),
        damping_ratio=zeta,
        process_variance=q,
    )


def _bounds_and_starts(
    family: StateSpaceFamily,
    values: np.ndarray,
    fs: float,
    fmin_hz: float,
    fmax_hz: float,
) -> tuple[list[tuple[float, float]], list[np.ndarray]]:
    log_low = math.log(1e-6)
    log_high = math.log(10.0)
    theta_min = 2.0 * math.pi * fmin_hz / fs
    theta_max = 2.0 * math.pi * fmax_hz / fs
    candidates = _fft_candidates(values, fs, fmin_hz, fmax_hz)

    if family is StateSpaceFamily.A0_RELAXATION:
        bounds = [(1e-4, 0.9999), (log_low, log_high), (log_low, log_high)]
        starts = [
            np.asarray([phi, math.log(0.10), math.log(0.20)], dtype=np.float64)
            for phi in (0.40, 0.80, 0.97)
        ]
        return bounds, starts

    if family is StateSpaceFamily.A1_SINGLE_OSCILLATOR:
        bounds = [
            (0.05, 0.9999),
            (theta_min, theta_max),
            (log_low, log_high),
            (log_low, log_high),
        ]
        starts: list[np.ndarray] = []
        for frequency in candidates[:3]:
            theta = 2.0 * math.pi * frequency / fs
            for rho in (0.85, 0.97):
                starts.append(
                    np.asarray(
                        [rho, theta, math.log(0.08), math.log(0.20)],
                        dtype=np.float64,
                    )
                )
        return bounds, starts

    if family is StateSpaceFamily.A2_TWO_OSCILLATORS:
        bounds = [
            (0.05, 0.9999),
            (theta_min, theta_max),
            (log_low, log_high),
            (0.05, 0.9999),
            (theta_min, theta_max),
            (log_low, log_high),
            (log_low, log_high),
        ]
        pairs: list[tuple[float, float]] = []
        for first in candidates:
            for second in candidates:
                if second <= first:
                    continue
                if abs(second - first) < max(0.75, 2.0 * fs / values.size):
                    continue
                pair = (float(first), float(second))
                if pair not in pairs:
                    pairs.append(pair)
        primary = candidates[0]
        fallbacks = [
            (max(fmin_hz + 0.5, primary * 0.8), min(fmax_hz - 0.5, primary * 1.2)),
            (max(fmin_hz + 0.5, primary), min(fmax_hz - 0.5, primary + 8.0)),
            (max(fmin_hz + 0.5, 8.0), min(fmax_hz - 0.5, 20.0)),
        ]
        for pair in fallbacks:
            a, b = sorted(pair)
            if b - a >= 0.75 and (a, b) not in pairs:
                pairs.append((a, b))

        starts = []
        for first, second in pairs[:6]:
            starts.append(
                np.asarray(
                    [
                        0.94,
                        2.0 * math.pi * first / fs,
                        math.log(0.04),
                        0.94,
                        2.0 * math.pi * second / fs,
                        math.log(0.04),
                        math.log(0.15),
                    ],
                    dtype=np.float64,
                )
            )
        return bounds, starts

    raise ValueError(f"unsupported model family: {family}")


def _fit_fixed_values(
    values: np.ndarray,
    fs: float,
    family: StateSpaceFamily,
    *,
    fmin_hz: float,
    fmax_hz: float,
    maxiter: int,
) -> tuple[object, np.ndarray]:
    bounds, starts = _bounds_and_starts(family, values, fs, fmin_hz, fmax_hz)

    def objective(parameters: np.ndarray) -> float:
        try:
            a, q, h, r, _, _, _ = _physical_model(family, parameters, fs)
            return kalman_innovations_nll(values, a, q, h, r)
        except (ValueError, FloatingPointError, OverflowError):
            return 1e30

    best = None
    best_x = None
    for start in starts:
        fit = minimize(
            objective,
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": int(maxiter), "ftol": 1e-9, "gtol": 1e-6},
        )
        if not math.isfinite(float(fit.fun)):
            continue
        if best is None or float(fit.fun) < float(best.fun):
            best = fit
            best_x = np.asarray(fit.x, dtype=np.float64)

    if best is None or best_x is None:
        raise RuntimeError(f"{family.value} optimization produced no finite result")
    return best, best_x


def fit_state_space_candidate(
    signal: Sequence[float],
    sampling_rate_hz: float,
    family: StateSpaceFamily,
    *,
    fmin_hz: float = 1.0,
    fmax_hz: float = 40.0,
    heldout_fraction: float = 0.30,
    maxiter: int = 160,
) -> StateSpaceCandidateFit:
    """Fit one candidate family using training likelihood and fixed-parameter holdout."""
    if not math.isfinite(sampling_rate_hz) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be finite and > 0")
    nyquist = sampling_rate_hz / 2.0
    if not (0 < fmin_hz < fmax_hz < nyquist):
        raise ValueError("frequency bounds must satisfy 0 < fmin < fmax < Nyquist")
    if not 0 <= heldout_fraction < 0.5:
        raise ValueError("heldout_fraction must satisfy 0 <= value < 0.5")
    if maxiter < 1:
        raise ValueError("maxiter must be >= 1")

    values = _standardize(signal)
    if heldout_fraction > 0:
        split = int(math.floor(values.size * (1.0 - heldout_fraction)))
        if split < 64 or values.size - split < 32:
            raise ValueError("signal is too short for requested train/holdout split")
        train = values[:split]
        test = values[split:]
    else:
        train = values
        test = np.empty(0, dtype=np.float64)

    fit, parameters = _fit_fixed_values(
        train,
        sampling_rate_hz,
        family,
        fmin_hz=fmin_hz,
        fmax_hz=fmax_hz,
        maxiter=maxiter,
    )
    a, q, h, r, phi, modes, process_variances = _physical_model(
        family, parameters, sampling_rate_hz
    )
    nll = kalman_innovations_nll(train, a, q, h, r)
    k = int(parameters.size)
    n = int(train.size)
    bic = 2.0 * nll + k * math.log(n)
    aic = 2.0 * nll + 2.0 * k
    heldout = None
    if test.size:
        heldout = kalman_innovations_nll(test, a, q, h, r) / float(test.size)

    return StateSpaceCandidateFit(
        family=family,
        converged=bool(fit.success),
        sample_count=n,
        parameter_count=k,
        negative_log_likelihood=float(nll),
        bic=float(bic),
        aic=float(aic),
        heldout_negative_log_likelihood_per_sample=(
            float(heldout) if heldout is not None else None
        ),
        observation_noise_variance=float(r),
        relaxation_phi=float(phi) if phi is not None else None,
        process_variances=tuple(float(v) for v in process_variances),
        modes=tuple(modes),
        optimizer_message=str(fit.message),
        optimizer_iterations=(int(fit.nit) if getattr(fit, "nit", None) is not None else None),
    )


def fit_model_set(
    signal: Sequence[float],
    sampling_rate_hz: float,
    *,
    fmin_hz: float = 1.0,
    fmax_hz: float = 40.0,
    heldout_fraction: float = 0.30,
    maxiter: int = 160,
) -> dict[StateSpaceFamily, StateSpaceCandidateFit]:
    """Fit A0/A1/A2 without converting the winner into an admission decision."""
    return {
        family: fit_state_space_candidate(
            signal,
            sampling_rate_hz,
            family,
            fmin_hz=fmin_hz,
            fmax_hz=fmax_hz,
            heldout_fraction=heldout_fraction,
            maxiter=maxiter,
        )
        for family in (
            StateSpaceFamily.A0_RELAXATION,
            StateSpaceFamily.A1_SINGLE_OSCILLATOR,
            StateSpaceFamily.A2_TWO_OSCILLATORS,
        )
    }


def rank_model_set(
    fits: dict[StateSpaceFamily, StateSpaceCandidateFit],
) -> dict[str, object]:
    """Return descriptive model rankings only; this is not an admission policy."""
    required = set(StateSpaceFamily)
    if set(fits) != required:
        raise ValueError("fits must contain exactly A0, A1, and A2")
    bic_order = sorted(fits.values(), key=lambda item: item.bic)
    heldout_available = all(
        item.heldout_negative_log_likelihood_per_sample is not None for item in fits.values()
    )
    heldout_order = (
        sorted(
            fits.values(),
            key=lambda item: float(item.heldout_negative_log_likelihood_per_sample),
        )
        if heldout_available
        else []
    )
    return {
        "bic_order": [item.family.value for item in bic_order],
        "bic_delta_from_best": {
            item.family.value: float(item.bic - bic_order[0].bic) for item in bic_order
        },
        "heldout_order": [item.family.value for item in heldout_order],
        "heldout_delta_nll_per_sample_from_best": (
            {
                item.family.value: float(
                    item.heldout_negative_log_likelihood_per_sample
                    - heldout_order[0].heldout_negative_log_likelihood_per_sample
                )
                for item in heldout_order
            }
            if heldout_order
            else {}
        ),
        "interpretation": (
            "Rankings are P0-Q diagnostics. A winning family is not an admitted "
            "biological mode, damping ratio, or chi until operating-region and "
            "refusal rules are separately qualified and frozen."
        ),
    }
