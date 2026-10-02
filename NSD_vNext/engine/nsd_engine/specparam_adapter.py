"""Qualification-only adapter for specparam 2.0.0rc7.

The adapter exists to keep a release-candidate third-party API behind a narrow,
version-checked boundary. Its outputs are descriptive spectral parameters only.
They do not license modal poles, damping, Q, natural frequency, or chi.

This module is intentionally not imported from :mod:`nsd_engine.__init__`.
Install the optional ``parameterization_rc7`` dependency when qualifying it.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version as package_version
import math
from typing import Sequence

import numpy as np


REQUIRED_SPECPARAM_VERSION = "2.0.0rc7"


@dataclass(frozen=True)
class SpecparamSettings:
    aperiodic_mode: str = "fixed"
    periodic_mode: str = "gaussian"
    peak_width_limits: tuple[float, float] = (0.5, 12.0)
    max_n_peaks: int = 6
    min_peak_height: float = 0.0
    peak_threshold: float = 2.0
    fmin_hz: float = 1.0
    fmax_hz: float = 45.0

    def __post_init__(self) -> None:
        if self.aperiodic_mode not in {"fixed", "knee"}:
            raise ValueError("aperiodic_mode must be 'fixed' or 'knee'")
        if self.periodic_mode != "gaussian":
            raise ValueError("qualification adapter currently supports gaussian periodic mode only")
        low, high = self.peak_width_limits
        if not (math.isfinite(low) and math.isfinite(high) and 0 < low < high):
            raise ValueError("peak_width_limits must be finite, positive, and increasing")
        if self.max_n_peaks < 0:
            raise ValueError("max_n_peaks must be >= 0")
        if not math.isfinite(self.min_peak_height) or self.min_peak_height < 0:
            raise ValueError("min_peak_height must be finite and >= 0")
        if not math.isfinite(self.peak_threshold) or self.peak_threshold < 0:
            raise ValueError("peak_threshold must be finite and >= 0")
        if not (math.isfinite(self.fmin_hz) and math.isfinite(self.fmax_hz)):
            raise ValueError("frequency bounds must be finite")
        if not 0 < self.fmin_hz < self.fmax_hz:
            raise ValueError("frequency bounds must satisfy 0 < fmin < fmax")


@dataclass(frozen=True)
class DescriptivePeak:
    center_frequency_hz: float
    power_above_aperiodic_log10: float
    bandwidth_hz: float

    def __post_init__(self) -> None:
        if not math.isfinite(self.center_frequency_hz) or self.center_frequency_hz <= 0:
            raise ValueError("center_frequency_hz must be finite and > 0")
        if not math.isfinite(self.power_above_aperiodic_log10):
            raise ValueError("power_above_aperiodic_log10 must be finite")
        if not math.isfinite(self.bandwidth_hz) or self.bandwidth_hz <= 0:
            raise ValueError("bandwidth_hz must be finite and > 0")


@dataclass(frozen=True)
class SpecparamDescriptiveResult:
    package_version: str
    settings: SpecparamSettings
    aperiodic_parameters: tuple[float, ...]
    aperiodic_parameter_names: tuple[str, ...]
    peaks: tuple[DescriptivePeak, ...]
    metrics: tuple[tuple[str, float], ...]
    frequency_resolution_hz: float
    zero_peak_state: bool

    @property
    def licenses_damping(self) -> bool:
        return False

    @property
    def licenses_natural_frequency(self) -> bool:
        return False

    @property
    def licenses_chi(self) -> bool:
        return False

    @property
    def licenses_modal_pole(self) -> bool:
        return False


def installed_specparam_version() -> str:
    try:
        return package_version("specparam")
    except PackageNotFoundError as exc:
        raise RuntimeError(
            "specparam is not installed; install the qualification-only parameterization_rc7 extra"
        ) from exc


def _require_exact_version() -> str:
    installed = installed_specparam_version()
    if installed != REQUIRED_SPECPARAM_VERSION:
        raise RuntimeError(
            f"specparam version mismatch: required {REQUIRED_SPECPARAM_VERSION}, found {installed}"
        )
    return installed


def _normalize_peaks(raw: np.ndarray) -> tuple[DescriptivePeak, ...]:
    array = np.asarray(raw, dtype=float)
    if array.ndim == 1:
        if array.size == 0 or np.isnan(array).all():
            return ()
        if array.size != 3:
            raise ValueError(f"unexpected specparam periodic parameter shape: {array.shape}")
        array = array.reshape(1, 3)
    if array.ndim != 2 or array.shape[1] != 3:
        raise ValueError(f"unexpected specparam periodic parameter shape: {array.shape}")
    rows: list[DescriptivePeak] = []
    for row in array:
        if np.isnan(row).all():
            continue
        if not np.isfinite(row).all():
            raise ValueError("specparam returned partially non-finite periodic parameters")
        rows.append(
            DescriptivePeak(
                center_frequency_hz=float(row[0]),
                power_above_aperiodic_log10=float(row[1]),
                bandwidth_hz=float(row[2]),
            )
        )
    return tuple(rows)


def fit_specparam_descriptive(
    frequencies_hz: Sequence[float],
    power_linear: Sequence[float],
    *,
    settings: SpecparamSettings | None = None,
) -> SpecparamDescriptiveResult:
    """Fit one spectrum with exact-pinned specparam and return a narrow result."""
    installed = _require_exact_version()
    from specparam import SpectralModel

    frequencies = np.asarray(frequencies_hz, dtype=float)
    power = np.asarray(power_linear, dtype=float)
    if frequencies.ndim != 1 or power.ndim != 1 or frequencies.size != power.size:
        raise ValueError("frequencies_hz and power_linear must be equal-length 1D arrays")
    if frequencies.size < 3:
        raise ValueError("at least three spectral bins are required")
    if not np.isfinite(frequencies).all() or not np.isfinite(power).all():
        raise ValueError("spectrum contains non-finite values")
    if np.any(frequencies <= 0) or np.any(power <= 0):
        raise ValueError("frequencies and linear power must be strictly positive")
    if np.any(np.diff(frequencies) <= 0):
        raise ValueError("frequencies must be strictly increasing")

    spacing = np.diff(frequencies)
    resolution = float(np.median(spacing))
    if not np.allclose(spacing, resolution, rtol=1e-6, atol=1e-10):
        raise ValueError("qualification adapter requires an evenly spaced frequency grid")

    settings = settings or SpecparamSettings()
    if settings.fmin_hz < frequencies[0] or settings.fmax_hz > frequencies[-1]:
        raise ValueError("fit frequency range extends beyond supplied spectrum")

    model = SpectralModel(
        aperiodic_mode=settings.aperiodic_mode,
        periodic_mode=settings.periodic_mode,
        peak_width_limits=settings.peak_width_limits,
        max_n_peaks=settings.max_n_peaks,
        min_peak_height=settings.min_peak_height,
        peak_threshold=settings.peak_threshold,
        verbose=False,
    )
    model.fit(frequencies, power, [settings.fmin_hz, settings.fmax_hz])

    aperiodic = np.asarray(model.get_params("aperiodic"), dtype=float).reshape(-1)
    if not np.isfinite(aperiodic).all():
        raise ValueError("specparam returned non-finite aperiodic parameters")
    if settings.aperiodic_mode == "fixed":
        names = ("offset", "exponent")
    else:
        names = ("offset", "knee", "exponent")
    if aperiodic.size != len(names):
        raise ValueError(
            f"unexpected {settings.aperiodic_mode} aperiodic parameter count: {aperiodic.size}"
        )

    periodic = model.get_params("periodic")
    peaks = _normalize_peaks(np.asarray(periodic, dtype=float))

    metrics_dict = dict(model.results.metrics.results)
    metrics: list[tuple[str, float]] = []
    for key, value in sorted(metrics_dict.items()):
        numeric = float(value)
        if not math.isfinite(numeric):
            raise ValueError(f"specparam metric {key!r} is non-finite")
        metrics.append((str(key), numeric))

    return SpecparamDescriptiveResult(
        package_version=installed,
        settings=settings,
        aperiodic_parameters=tuple(float(value) for value in aperiodic),
        aperiodic_parameter_names=names,
        peaks=peaks,
        metrics=tuple(metrics),
        frequency_resolution_hz=resolution,
        zero_peak_state=len(peaks) == 0,
    )
