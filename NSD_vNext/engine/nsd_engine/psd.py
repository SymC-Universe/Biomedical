"""Accepted descriptive PSD primitive for NSD T0 qualification.

This module implements Welch power spectral density through SciPy. It is a
native descriptive signal representation only. A PSD peak, bandwidth, or center
frequency returned here does not license a damping rate, modal pole, Q factor,
or chi.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
import scipy
from scipy.signal import welch


@dataclass(frozen=True)
class WelchConfig:
    window_seconds: float = 4.0
    overlap_fraction: float = 0.5
    window: str = "hann"
    detrend: str = "constant"
    scaling: str = "density"

    def __post_init__(self) -> None:
        if not math.isfinite(self.window_seconds) or self.window_seconds <= 0:
            raise ValueError("window_seconds must be finite and > 0")
        if not math.isfinite(self.overlap_fraction) or not 0 <= self.overlap_fraction < 1:
            raise ValueError("overlap_fraction must satisfy 0 <= value < 1")
        if not self.window.strip():
            raise ValueError("window must be non-empty")
        if self.detrend not in {"constant", "linear", "none"}:
            raise ValueError("detrend must be 'constant', 'linear', or 'none'")
        if self.scaling not in {"density", "spectrum"}:
            raise ValueError("scaling must be 'density' or 'spectrum'")


@dataclass(frozen=True)
class PSDResult:
    frequencies_hz: tuple[float, ...]
    power: tuple[float, ...]
    sampling_rate_hz: float
    nperseg: int
    noverlap: int
    segment_count: int
    frequency_resolution_hz: float
    method_name: str
    scipy_version: str
    numpy_version: str
    config: WelchConfig
    fmin_hz: float
    fmax_hz: float

    def __post_init__(self) -> None:
        if not self.frequencies_hz:
            raise ValueError("frequencies_hz must not be empty")
        if len(self.frequencies_hz) != len(self.power):
            raise ValueError("frequencies_hz and power must have equal length")
        if any(not math.isfinite(value) for value in self.frequencies_hz):
            raise ValueError("frequencies_hz must be finite")
        if any(not math.isfinite(value) or value < 0 for value in self.power):
            raise ValueError("power values must be finite and >= 0")
        if any(b <= a for a, b in zip(self.frequencies_hz, self.frequencies_hz[1:])):
            raise ValueError("frequencies_hz must be strictly increasing")
        if self.nperseg <= 0 or self.segment_count <= 0:
            raise ValueError("nperseg and segment_count must be > 0")
        if not 0 <= self.noverlap < self.nperseg:
            raise ValueError("noverlap must satisfy 0 <= noverlap < nperseg")

    @property
    def licenses_dynamical_chi(self) -> bool:
        return False

    @property
    def licenses_damping(self) -> bool:
        return False


def estimate_welch_psd(
    signal: Sequence[float],
    sampling_rate_hz: float,
    *,
    fmin_hz: float = 0.0,
    fmax_hz: float | None = None,
    config: WelchConfig | None = None,
) -> PSDResult:
    """Estimate a one-sided Welch PSD using a fully serialized convention."""
    if not math.isfinite(sampling_rate_hz) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be finite and > 0")
    if not math.isfinite(fmin_hz) or fmin_hz < 0:
        raise ValueError("fmin_hz must be finite and >= 0")

    values = np.asarray(signal, dtype=np.float64)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("signal must be a non-empty one-dimensional sequence")
    if not np.isfinite(values).all():
        raise ValueError("signal contains non-finite samples")

    nyquist = sampling_rate_hz / 2.0
    if fmax_hz is None:
        fmax_hz = nyquist
    if not math.isfinite(fmax_hz) or fmax_hz <= fmin_hz:
        raise ValueError("fmax_hz must be finite and > fmin_hz")
    if fmax_hz > nyquist:
        raise ValueError("fmax_hz cannot exceed Nyquist frequency")

    config = config or WelchConfig()
    nperseg = int(round(config.window_seconds * sampling_rate_hz))
    if nperseg < 2:
        raise ValueError("window_seconds yields fewer than two samples")
    if nperseg > values.size:
        raise ValueError("signal is shorter than one requested Welch window")
    noverlap = int(round(config.overlap_fraction * nperseg))
    if noverlap >= nperseg:
        raise ValueError("overlap produces no forward step")
    step = nperseg - noverlap
    segment_count = 1 + (values.size - nperseg) // step

    detrend: str | bool
    detrend = False if config.detrend == "none" else config.detrend
    frequencies, power = welch(
        values,
        fs=sampling_rate_hz,
        window=config.window,
        nperseg=nperseg,
        noverlap=noverlap,
        nfft=nperseg,
        detrend=detrend,
        return_onesided=True,
        scaling=config.scaling,
        average="mean",
    )

    mask = (frequencies >= fmin_hz) & (frequencies <= fmax_hz)
    clipped_f = frequencies[mask]
    clipped_p = power[mask]
    if clipped_f.size == 0:
        raise ValueError("requested frequency range contains no PSD bins")

    return PSDResult(
        frequencies_hz=tuple(float(value) for value in clipped_f),
        power=tuple(float(value) for value in clipped_p),
        sampling_rate_hz=float(sampling_rate_hz),
        nperseg=nperseg,
        noverlap=noverlap,
        segment_count=int(segment_count),
        frequency_resolution_hz=float(sampling_rate_hz / nperseg),
        method_name="scipy.signal.welch",
        scipy_version=scipy.__version__,
        numpy_version=np.__version__,
        config=config,
        fmin_hz=float(fmin_hz),
        fmax_hz=float(fmax_hz),
    )
