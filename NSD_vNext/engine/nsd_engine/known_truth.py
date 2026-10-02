"""Known-truth second-order oscillator fixtures for NSD qualification.

These functions generate analytically defined underdamped second-order systems.
They are test fixtures, not estimators and not clinical models.

Convention:
    x'' + 2*zeta*omega0*x' + omega0**2*x = u(t)
where omega0 is the undamped natural angular frequency (rad/s) and zeta is the
classical damping ratio.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


@dataclass(frozen=True)
class DHOTruth:
    natural_frequency_hz: float
    damping_ratio: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.natural_frequency_hz) or self.natural_frequency_hz <= 0:
            raise ValueError("natural_frequency_hz must be finite and > 0")
        if not math.isfinite(self.damping_ratio) or not 0 < self.damping_ratio < 1:
            raise ValueError("damping_ratio must satisfy 0 < zeta < 1 for this underdamped fixture")

    @property
    def omega0_rad_s(self) -> float:
        return 2.0 * math.pi * self.natural_frequency_hz

    @property
    def decay_rate_per_s(self) -> float:
        return self.damping_ratio * self.omega0_rad_s

    @property
    def damped_omega_rad_s(self) -> float:
        return self.omega0_rad_s * math.sqrt(1.0 - self.damping_ratio**2)

    @property
    def damped_frequency_hz(self) -> float:
        return self.damped_omega_rad_s / (2.0 * math.pi)

    @property
    def pole_real_per_s(self) -> float:
        return -self.decay_rate_per_s

    @property
    def pole_imag_rad_s(self) -> float:
        return self.damped_omega_rad_s

    @property
    def resonance_frequency_hz(self) -> float | None:
        """Frequency maximizing |H(iw)| for displacement under harmonic forcing.

        A resonance maximum exists only for zeta < 1/sqrt(2). Importantly, this
        frequency is not generally omega0/(2*pi) and is also distinct from the
        damped free-oscillation frequency.
        """
        if self.damping_ratio >= 1.0 / math.sqrt(2.0):
            return None
        omega_r = self.omega0_rad_s * math.sqrt(1.0 - 2.0 * self.damping_ratio**2)
        return omega_r / (2.0 * math.pi)


def impulse_response(
    truth: DHOTruth,
    duration_seconds: float,
    sampling_rate_hz: float,
    *,
    initial_displacement: float = 0.0,
    initial_velocity: float = 1.0,
) -> tuple[tuple[float, ...], tuple[float, ...]]:
    """Return exact underdamped free response sampled on an evenly spaced grid."""
    if not math.isfinite(duration_seconds) or duration_seconds <= 0:
        raise ValueError("duration_seconds must be finite and > 0")
    if not math.isfinite(sampling_rate_hz) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be finite and > 0")
    if not math.isfinite(initial_displacement) or not math.isfinite(initial_velocity):
        raise ValueError("initial conditions must be finite")

    n = int(math.floor(duration_seconds * sampling_rate_hz)) + 1
    times = tuple(i / sampling_rate_hz for i in range(n))

    alpha = truth.decay_rate_per_s
    omega_d = truth.damped_omega_rad_s
    a = initial_displacement
    b = (initial_velocity + alpha * initial_displacement) / omega_d

    values = tuple(
        math.exp(-alpha * t) * (a * math.cos(omega_d * t) + b * math.sin(omega_d * t))
        for t in times
    )
    return times, values


def transfer_power(
    truth: DHOTruth,
    frequencies_hz: Iterable[float],
) -> tuple[float, ...]:
    """Return unnormalized |H(iw)|^2 for unit forcing of the displacement model."""
    omega0 = truth.omega0_rad_s
    zeta = truth.damping_ratio
    output: list[float] = []
    for frequency_hz in frequencies_hz:
        if not math.isfinite(frequency_hz) or frequency_hz < 0:
            raise ValueError("frequencies_hz must contain finite values >= 0")
        omega = 2.0 * math.pi * frequency_hz
        denominator = (omega0**2 - omega**2) ** 2 + (2.0 * zeta * omega0 * omega) ** 2
        output.append(1.0 / denominator)
    return tuple(output)
