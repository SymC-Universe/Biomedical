"""Physical-coordinate helpers for qualification-only C1Q uncertainty work.

This module does not define a new likelihood. It maps physical coordinates
(A, natural frequency, chi, g) onto the exact existing C1Q raw coordinates and
delegates likelihood evaluation to the canonical C1Q implementation.

No production promotion, threshold, or real-EEG admission is defined here.
"""

from __future__ import annotations

import math
import numpy as np

from .continuous_lineage_candidate import _build_candidate, _nll
from .state_space_adequacy import (
    _raw_fraction,
    _raw_frequency,
    _raw_rho,
)


def physical_to_c1q_raw(
    *,
    A: float,
    natural_frequency_hz: float,
    chi: float,
    g: float,
    sampling_rate_hz: float,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
) -> np.ndarray:
    if not 0.0 < A < 1.0:
        raise ValueError("A must lie in (0,1)")
    if not 0.0 < chi < 1.0:
        raise ValueError("chi must lie in (0,1) for this underdamped wrapper")
    if not -1.0 < g < 1.0:
        raise ValueError("g must lie in (-1,1)")
    if natural_frequency_hz <= 0.0:
        raise ValueError("natural_frequency_hz must be positive")

    omega_n = 2.0 * math.pi * natural_frequency_hz
    alpha = chi * omega_n
    nu = omega_n * math.sqrt(1.0 - chi * chi)
    rho = math.exp(-alpha / sampling_rate_hz)
    damped_frequency_hz = nu / (2.0 * math.pi)

    raw = np.asarray(
        [
            _raw_fraction(A),
            _raw_rho(rho),
            _raw_frequency(damped_frequency_hz, fmin_hz, fmax_hz),
            float(np.arctanh(g)),
        ],
        dtype=np.float64,
    )
    if not np.isfinite(raw).all():
        raise ValueError("physical coordinates do not map to finite raw coordinates")
    if np.any(raw < -8.0) or np.any(raw > 8.0):
        raise ValueError("physical coordinates lie outside current C1Q raw box")
    return raw


def physical_candidate(
    *,
    A: float,
    natural_frequency_hz: float,
    chi: float,
    g: float,
    sampling_rate_hz: float,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
):
    raw = physical_to_c1q_raw(
        A=A,
        natural_frequency_hz=natural_frequency_hz,
        chi=chi,
        g=g,
        sampling_rate_hz=sampling_rate_hz,
        fmin_hz=fmin_hz,
        fmax_hz=fmax_hz,
    )
    return _build_candidate(raw, sampling_rate_hz, fmin_hz, fmax_hz)


def physical_nll(
    standardized: np.ndarray,
    *,
    A: float,
    natural_frequency_hz: float,
    chi: float,
    g: float,
    sampling_rate_hz: float,
    burn_in_samples: int = 128,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
) -> float:
    raw = physical_to_c1q_raw(
        A=A,
        natural_frequency_hz=natural_frequency_hz,
        chi=chi,
        g=g,
        sampling_rate_hz=sampling_rate_hz,
        fmin_hz=fmin_hz,
        fmax_hz=fmax_hz,
    )
    return _nll(
        np.asarray(standardized, dtype=np.float64),
        raw,
        sampling_rate_hz,
        fmin_hz,
        fmax_hz,
        burn_in_samples,
    )
