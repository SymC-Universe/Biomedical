"""Qualification-stage AR(2) output-only modal estimator.

This module supplies one explicit native dynamical route for T0 known-truth
qualification. It does not claim that arbitrary EEG is an AR(2) oscillator.
Instead, it asks whether an identified second-order discrete mode can recover
continuous-time pole quantities when the generating assumptions are true, and
refuse when they are not.

Recurrence convention
---------------------
    x[t] = a1 * x[t-1] + a2 * x[t-2] + e[t]

The discrete poles are roots of
    z^2 - a1 z - a2 = 0.

For a stable complex-conjugate pole z and sample interval dt, the continuous
pole is s = log(z) / dt = -alpha +/- i * omega_d. Then
    omega_n = sqrt(alpha^2 + omega_d^2)
    zeta = alpha / omega_n.

The returned damping ratio is therefore licensed only by this fitted model and
its qualification status. It is not a whole-system neural stability score.
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
from typing import Sequence

import numpy as np

from .schema import RefusalCode


@dataclass(frozen=True)
class AR2ModalResult:
    admitted: bool
    refusal_code: RefusalCode | None
    reason: str | None
    sample_count: int
    sampling_rate_hz: float
    a1: float | None = None
    a2: float | None = None
    residual_variance: float | None = None
    design_condition_number: float | None = None
    discrete_poles: tuple[complex, complex] | None = None
    continuous_poles_per_s: tuple[complex, complex] | None = None
    damped_frequency_hz: float | None = None
    natural_frequency_hz: float | None = None
    decay_rate_per_s: float | None = None
    damping_ratio: float | None = None

    def __post_init__(self) -> None:
        if self.sample_count < 3:
            raise ValueError("sample_count must be >= 3")
        if not math.isfinite(self.sampling_rate_hz) or self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz must be finite and > 0")
        if self.admitted:
            if self.refusal_code is not None or self.reason is not None:
                raise ValueError("admitted result cannot contain a refusal")
            required = (
                self.a1,
                self.a2,
                self.residual_variance,
                self.design_condition_number,
                self.discrete_poles,
                self.continuous_poles_per_s,
                self.damped_frequency_hz,
                self.natural_frequency_hz,
                self.decay_rate_per_s,
                self.damping_ratio,
            )
            if any(value is None for value in required):
                raise ValueError("admitted AR2 modal result is incomplete")
        else:
            if self.refusal_code is None or not self.reason:
                raise ValueError("refused result requires refusal_code and reason")


@dataclass(frozen=True)
class AR2Truth:
    natural_frequency_hz: float
    damping_ratio: float
    sampling_rate_hz: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.natural_frequency_hz) or self.natural_frequency_hz <= 0:
            raise ValueError("natural_frequency_hz must be finite and > 0")
        if not math.isfinite(self.damping_ratio) or not 0 < self.damping_ratio < 1:
            raise ValueError("AR2 oscillatory truth requires 0 < damping_ratio < 1")
        if not math.isfinite(self.sampling_rate_hz) or self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz must be finite and > 0")
        if self.natural_frequency_hz >= self.sampling_rate_hz / 2:
            raise ValueError("natural frequency must lie below Nyquist")

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
    def discrete_radius(self) -> float:
        dt = 1.0 / self.sampling_rate_hz
        return math.exp(-self.decay_rate_per_s * dt)

    @property
    def discrete_angle_rad(self) -> float:
        return self.damped_omega_rad_s / self.sampling_rate_hz

    @property
    def ar_coefficients(self) -> tuple[float, float]:
        radius = self.discrete_radius
        angle = self.discrete_angle_rad
        return (2.0 * radius * math.cos(angle), -(radius**2))


def simulate_ar2_truth(
    truth: AR2Truth,
    *,
    seconds: float,
    innovation_sd: float = 1.0,
    measurement_noise_sd: float = 0.0,
    seed: int = 0,
    burn_in_seconds: float = 5.0,
) -> np.ndarray:
    """Generate stationary AR(2) known truth with optional measurement noise."""
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("seconds must be finite and > 0")
    if not math.isfinite(innovation_sd) or innovation_sd <= 0:
        raise ValueError("innovation_sd must be finite and > 0")
    if not math.isfinite(measurement_noise_sd) or measurement_noise_sd < 0:
        raise ValueError("measurement_noise_sd must be finite and >= 0")
    if not math.isfinite(burn_in_seconds) or burn_in_seconds < 0:
        raise ValueError("burn_in_seconds must be finite and >= 0")

    fs = truth.sampling_rate_hz
    target_n = int(round(seconds * fs))
    burn_n = int(round(burn_in_seconds * fs))
    total_n = target_n + burn_n
    if target_n < 3:
        raise ValueError("requested duration yields fewer than three samples")

    rng = np.random.default_rng(seed)
    innovations = rng.normal(0.0, innovation_sd, size=total_n)
    values = np.zeros(total_n, dtype=np.float64)
    a1, a2 = truth.ar_coefficients
    for index in range(2, total_n):
        values[index] = a1 * values[index - 1] + a2 * values[index - 2] + innovations[index]

    observed = values[burn_n:].copy()
    if measurement_noise_sd > 0:
        observed += rng.normal(0.0, measurement_noise_sd, size=target_n)
    return observed


def _refuse(sample_count: int, fs: float, code: RefusalCode, reason: str) -> AR2ModalResult:
    return AR2ModalResult(
        admitted=False,
        refusal_code=code,
        reason=reason,
        sample_count=sample_count,
        sampling_rate_hz=fs,
    )


def fit_ar2_modal(
    signal: Sequence[float],
    sampling_rate_hz: float,
    *,
    min_samples: int = 256,
    complex_imag_tolerance: float = 1e-8,
    max_design_condition_number: float = 1e8,
) -> AR2ModalResult:
    """Fit one AR(2) mode and admit only a stable complex-conjugate pole pair."""
    if not math.isfinite(sampling_rate_hz) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be finite and > 0")
    if min_samples < 3:
        raise ValueError("min_samples must be >= 3")
    if not math.isfinite(complex_imag_tolerance) or complex_imag_tolerance < 0:
        raise ValueError("complex_imag_tolerance must be finite and >= 0")
    if not math.isfinite(max_design_condition_number) or max_design_condition_number <= 1:
        raise ValueError("max_design_condition_number must be finite and > 1")

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
    if float(np.std(centered)) == 0.0:
        return _refuse(values.size, sampling_rate_hz, RefusalCode.MODE_NONIDENTIFIABLE, "zero-variance signal")

    y = centered[2:]
    design = np.column_stack((centered[1:-1], centered[:-2]))
    condition = float(np.linalg.cond(design))
    if not math.isfinite(condition) or condition > max_design_condition_number:
        return _refuse(
            values.size,
            sampling_rate_hz,
            RefusalCode.MODE_NONIDENTIFIABLE,
            f"AR2 design condition number {condition!r} exceeds limit",
        )

    coefficients, _, rank, _ = np.linalg.lstsq(design, y, rcond=None)
    if rank < 2:
        return _refuse(values.size, sampling_rate_hz, RefusalCode.MODE_NONIDENTIFIABLE, "rank-deficient AR2 fit")
    a1, a2 = (float(coefficients[0]), float(coefficients[1]))
    residual = y - design @ coefficients
    residual_variance = float(np.mean(residual**2))

    discriminant = complex(a1 * a1 + 4.0 * a2, 0.0)
    root_disc = cmath.sqrt(discriminant)
    poles = ((a1 + root_disc) / 2.0, (a1 - root_disc) / 2.0)

    if any(abs(pole) == 0.0 for pole in poles):
        return _refuse(values.size, sampling_rate_hz, RefusalCode.MODE_NONIDENTIFIABLE, "zero discrete pole")
    if any(abs(pole) >= 1.0 for pole in poles):
        return _refuse(
            values.size,
            sampling_rate_hz,
            RefusalCode.OUT_OF_DOMAIN,
            "AR2 fitted pole is not inside the unit circle",
        )
    if max(abs(pole.imag) for pole in poles) <= complex_imag_tolerance:
        return _refuse(
            values.size,
            sampling_rate_hz,
            RefusalCode.MODE_NONIDENTIFIABLE,
            "AR2 fitted poles are real/non-oscillatory",
        )

    dt = 1.0 / sampling_rate_hz
    continuous = tuple(cmath.log(pole) / dt for pole in poles)
    representative = max(continuous, key=lambda value: value.imag)
    if representative.real >= 0:
        return _refuse(
            values.size,
            sampling_rate_hz,
            RefusalCode.OUT_OF_DOMAIN,
            "continuous-time pole is not decaying",
        )

    decay_rate = -representative.real
    damped_omega = abs(representative.imag)
    natural_omega = math.hypot(decay_rate, damped_omega)
    if natural_omega <= 0:
        return _refuse(values.size, sampling_rate_hz, RefusalCode.MODE_NONIDENTIFIABLE, "zero natural frequency")
    zeta = decay_rate / natural_omega
    if not 0 < zeta < 1:
        return _refuse(
            values.size,
            sampling_rate_hz,
            RefusalCode.OUT_OF_DOMAIN,
            f"derived damping ratio {zeta} is outside oscillatory AR2 domain",
        )

    return AR2ModalResult(
        admitted=True,
        refusal_code=None,
        reason=None,
        sample_count=values.size,
        sampling_rate_hz=sampling_rate_hz,
        a1=a1,
        a2=a2,
        residual_variance=residual_variance,
        design_condition_number=condition,
        discrete_poles=poles,
        continuous_poles_per_s=continuous,
        damped_frequency_hz=damped_omega / (2.0 * math.pi),
        natural_frequency_hz=natural_omega / (2.0 * math.pi),
        decay_rate_per_s=decay_rate,
        damping_ratio=zeta,
    )
