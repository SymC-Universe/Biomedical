"""Observation-noise-aware latent oscillator covariance estimator.

This is the second T0 modal route. It uses a native linear stochastic oscillator
whose latent 2D state follows a damped rotation and whose scalar observation has
additive white measurement noise:

    x[t+1] = rho * R(theta) * x[t] + w[t]
    y[t]   = [1, 0] x[t] + v[t]

With isotropic stationary process noise, the normalized observation covariance
for non-zero lags is

    C_y[k] / C_y[0] = b * rho**k * cos(k * theta),  k >= 1,

where b is the fraction of zero-lag variance attributable to the latent state.
White observation noise changes the zero-lag variance but not the non-zero-lag
covariance, so the model can separate a latent oscillatory pole from additive
measurement noise under its stated assumptions.

The estimator is deliberately narrow. It is a known-truth candidate for modal
qualification, not a claim that arbitrary EEG follows this model.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from scipy.optimize import least_squares

from .schema import RefusalCode


@dataclass(frozen=True)
class LatentOscillatorTruth:
    natural_frequency_hz: float
    damping_ratio: float
    sampling_rate_hz: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.natural_frequency_hz) or self.natural_frequency_hz <= 0:
            raise ValueError("natural_frequency_hz must be finite and > 0")
        if not math.isfinite(self.damping_ratio) or not 0 < self.damping_ratio < 1:
            raise ValueError("damping_ratio must satisfy 0 < zeta < 1")
        if not math.isfinite(self.sampling_rate_hz) or self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz must be finite and > 0")
        if self.damped_frequency_hz >= self.sampling_rate_hz / 2:
            raise ValueError("damped frequency must lie below Nyquist")

    @property
    def omega_n_rad_s(self) -> float:
        return 2.0 * math.pi * self.natural_frequency_hz

    @property
    def decay_rate_per_s(self) -> float:
        return self.damping_ratio * self.omega_n_rad_s

    @property
    def damped_omega_rad_s(self) -> float:
        return self.omega_n_rad_s * math.sqrt(1.0 - self.damping_ratio**2)

    @property
    def damped_frequency_hz(self) -> float:
        return self.damped_omega_rad_s / (2.0 * math.pi)

    @property
    def rho(self) -> float:
        return math.exp(-self.decay_rate_per_s / self.sampling_rate_hz)

    @property
    def theta_rad_per_sample(self) -> float:
        return self.damped_omega_rad_s / self.sampling_rate_hz


@dataclass(frozen=True)
class LatentOscillatorEstimate:
    admitted: bool
    refusal_code: RefusalCode | None
    reason: str | None
    sample_count: int
    sampling_rate_hz: float
    latent_variance_fraction: float | None = None
    rho: float | None = None
    theta_rad_per_sample: float | None = None
    decay_rate_per_s: float | None = None
    damped_frequency_hz: float | None = None
    natural_frequency_hz: float | None = None
    damping_ratio: float | None = None
    observation_noise_to_latent_variance_ratio: float | None = None
    autocorrelation_r_squared: float | None = None
    fitted_lag_count: int | None = None
    optimizer_cost: float | None = None

    def __post_init__(self) -> None:
        if self.sample_count < 3:
            raise ValueError("sample_count must be >= 3")
        if not math.isfinite(self.sampling_rate_hz) or self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz must be finite and > 0")
        if self.admitted:
            if self.refusal_code is not None or self.reason is not None:
                raise ValueError("admitted result cannot contain refusal fields")
            required = (
                self.latent_variance_fraction,
                self.rho,
                self.theta_rad_per_sample,
                self.decay_rate_per_s,
                self.damped_frequency_hz,
                self.natural_frequency_hz,
                self.damping_ratio,
                self.observation_noise_to_latent_variance_ratio,
                self.autocorrelation_r_squared,
                self.fitted_lag_count,
                self.optimizer_cost,
            )
            if any(value is None for value in required):
                raise ValueError("admitted latent oscillator result is incomplete")
        else:
            if self.refusal_code is None or not self.reason:
                raise ValueError("refused result requires refusal_code and reason")


def simulate_latent_oscillator(
    truth: LatentOscillatorTruth,
    *,
    seconds: float,
    measurement_noise_to_latent_sd: float = 0.0,
    seed: int = 0,
    burn_in_seconds: float = 5.0,
) -> np.ndarray:
    """Simulate stationary unit-variance latent oscillator plus observation noise."""
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("seconds must be finite and > 0")
    if not math.isfinite(measurement_noise_to_latent_sd) or measurement_noise_to_latent_sd < 0:
        raise ValueError("measurement_noise_to_latent_sd must be finite and >= 0")
    if not math.isfinite(burn_in_seconds) or burn_in_seconds < 0:
        raise ValueError("burn_in_seconds must be finite and >= 0")

    fs = truth.sampling_rate_hz
    target_n = int(round(seconds * fs))
    burn_n = int(round(burn_in_seconds * fs))
    total_n = target_n + burn_n
    if target_n < 3:
        raise ValueError("requested duration yields fewer than three samples")

    rho = truth.rho
    theta = truth.theta_rad_per_sample
    rotation = np.array(
        [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]],
        dtype=np.float64,
    )
    transition = rho * rotation
    # q = 1-rho^2 gives stationary covariance I for isotropic Q=qI.
    process_sd = math.sqrt(max(0.0, 1.0 - rho * rho))

    rng = np.random.default_rng(seed)
    state = rng.normal(0.0, 1.0, size=2)
    latent = np.empty(total_n, dtype=np.float64)
    for index in range(total_n):
        latent[index] = state[0]
        state = transition @ state + rng.normal(0.0, process_sd, size=2)

    observed = latent[burn_n:].copy()
    if measurement_noise_to_latent_sd > 0:
        observed += rng.normal(
            0.0,
            measurement_noise_to_latent_sd,
            size=target_n,
        )
    return observed


def _refuse(sample_count: int, fs: float, code: RefusalCode, reason: str) -> LatentOscillatorEstimate:
    return LatentOscillatorEstimate(
        admitted=False,
        refusal_code=code,
        reason=reason,
        sample_count=sample_count,
        sampling_rate_hz=fs,
    )


def _initial_frequency_hz(values: np.ndarray, fs: float, fmin: float, fmax: float) -> float:
    centered = values - np.mean(values)
    spectrum = np.abs(np.fft.rfft(centered)) ** 2
    frequencies = np.fft.rfftfreq(centered.size, d=1.0 / fs)
    mask = (frequencies >= fmin) & (frequencies <= fmax)
    if not np.any(mask):
        return 0.5 * (fmin + fmax)
    local = spectrum[mask]
    if not np.isfinite(local).all() or np.max(local) <= 0:
        return 0.5 * (fmin + fmax)
    return float(frequencies[mask][int(np.argmax(local))])


def fit_latent_oscillator_covariance(
    signal: Sequence[float],
    sampling_rate_hz: float,
    *,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
    max_lag_seconds: float = 1.0,
    min_samples: int = 512,
) -> LatentOscillatorEstimate:
    """Fit the non-zero-lag covariance of one latent damped oscillator."""
    if not math.isfinite(sampling_rate_hz) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be finite and > 0")
    nyquist = sampling_rate_hz / 2.0
    if not (math.isfinite(fmin_hz) and math.isfinite(fmax_hz) and 0 < fmin_hz < fmax_hz < nyquist):
        raise ValueError("frequency bounds must satisfy 0 < fmin < fmax < Nyquist")
    if not math.isfinite(max_lag_seconds) or max_lag_seconds <= 0:
        raise ValueError("max_lag_seconds must be finite and > 0")
    if min_samples < 3:
        raise ValueError("min_samples must be >= 3")

    values = np.asarray(signal, dtype=np.float64)
    if values.ndim != 1 or values.size < 3:
        raise ValueError("signal must be a one-dimensional sequence with at least three samples")
    if not np.isfinite(values).all():
        return _refuse(values.size, sampling_rate_hz, RefusalCode.SIGNAL_INSUFFICIENT, "non-finite samples")
    if values.size < min_samples:
        return _refuse(
            values.size,
            sampling_rate_hz,
            RefusalCode.SIGNAL_INSUFFICIENT,
            f"requires at least {min_samples} samples",
        )

    centered = values - float(np.mean(values))
    variance = float(np.mean(centered**2))
    if variance <= 0 or not math.isfinite(variance):
        return _refuse(values.size, sampling_rate_hz, RefusalCode.MODE_NONIDENTIFIABLE, "zero/non-finite variance")

    max_lag = min(int(round(max_lag_seconds * sampling_rate_hz)), values.size // 8)
    if max_lag < 3:
        return _refuse(values.size, sampling_rate_hz, RefusalCode.SIGNAL_INSUFFICIENT, "too few usable covariance lags")
    lags = np.arange(1, max_lag + 1, dtype=np.float64)
    correlations = np.asarray(
        [
            float(np.dot(centered[:-lag], centered[lag:]) / (values.size - lag) / variance)
            for lag in range(1, max_lag + 1)
        ],
        dtype=np.float64,
    )
    if not np.isfinite(correlations).all():
        return _refuse(values.size, sampling_rate_hz, RefusalCode.MODE_NONIDENTIFIABLE, "non-finite covariance sequence")

    theta_min = 2.0 * math.pi * fmin_hz / sampling_rate_hz
    theta_max = 2.0 * math.pi * fmax_hz / sampling_rate_hz
    peak_frequency = _initial_frequency_hz(centered, sampling_rate_hz, fmin_hz, fmax_hz)
    theta_peak = 2.0 * math.pi * peak_frequency / sampling_rate_hz

    def residual(parameters: np.ndarray) -> np.ndarray:
        b, rho, theta = parameters
        predicted = b * (rho**lags) * np.cos(lags * theta)
        return predicted - correlations

    starts: list[tuple[float, float, float]] = []
    for b0 in (0.25, 0.5, 0.85, 0.98):
        for rho0 in (0.50, 0.70, 0.85, 0.95, 0.99):
            for multiplier in (0.8, 1.0, 1.2):
                theta0 = min(theta_max * 0.999, max(theta_min * 1.001, theta_peak * multiplier))
                starts.append((b0, rho0, theta0))

    best = None
    for start in starts:
        fit = least_squares(
            residual,
            x0=np.asarray(start, dtype=np.float64),
            bounds=(
                np.asarray([1e-4, 1e-4, theta_min], dtype=np.float64),
                np.asarray([0.999999, 0.999999, theta_max], dtype=np.float64),
            ),
            method="trf",
            loss="soft_l1",
            f_scale=0.05,
            max_nfev=3000,
        )
        if best is None or fit.cost < best.cost:
            best = fit

    if best is None or not best.success or not np.isfinite(best.x).all():
        return _refuse(values.size, sampling_rate_hz, RefusalCode.MODE_NONIDENTIFIABLE, "covariance optimizer failed")

    b, rho, theta = (float(value) for value in best.x)
    predicted = b * (rho**lags) * np.cos(lags * theta)
    ss_res = float(np.sum((correlations - predicted) ** 2))
    ss_tot = float(np.sum((correlations - np.mean(correlations)) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    decay_rate = -math.log(rho) * sampling_rate_hz
    damped_omega = theta * sampling_rate_hz
    natural_omega = math.hypot(decay_rate, damped_omega)
    if natural_omega <= 0:
        return _refuse(values.size, sampling_rate_hz, RefusalCode.MODE_NONIDENTIFIABLE, "zero natural frequency")
    zeta = decay_rate / natural_omega
    if not 0 < zeta < 1:
        return _refuse(
            values.size,
            sampling_rate_hz,
            RefusalCode.OUT_OF_DOMAIN,
            f"derived damping ratio {zeta} outside oscillatory domain",
        )

    noise_to_latent_variance = (1.0 - b) / b
    return LatentOscillatorEstimate(
        admitted=True,
        refusal_code=None,
        reason=None,
        sample_count=values.size,
        sampling_rate_hz=sampling_rate_hz,
        latent_variance_fraction=b,
        rho=rho,
        theta_rad_per_sample=theta,
        decay_rate_per_s=decay_rate,
        damped_frequency_hz=damped_omega / (2.0 * math.pi),
        natural_frequency_hz=natural_omega / (2.0 * math.pi),
        damping_ratio=zeta,
        observation_noise_to_latent_variance_ratio=noise_to_latent_variance,
        autocorrelation_r_squared=r_squared,
        fitted_lag_count=max_lag,
        optimizer_cost=float(best.cost),
    )
