"""Descriptive spectral interface for NSD vNext.

This layer may estimate aperiodic and periodic spectral features. It is
intentionally incapable of licensing damping or chi. Dynamical interpretation
belongs to a separately qualified modal/generative layer and the admission gate.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any, Mapping, Protocol, Sequence, runtime_checkable

from .schema import SpectralState


@dataclass(frozen=True)
class SpectralConfig:
    fmin_hz: float
    fmax_hz: float
    psd_method: str
    window_seconds: float | None = None
    overlap_fraction: float | None = None
    aperiodic_model: str = "fixed"
    periodic_model: str = "descriptive"

    def __post_init__(self) -> None:
        if not math.isfinite(self.fmin_hz) or self.fmin_hz < 0:
            raise ValueError("fmin_hz must be finite and >= 0")
        if not math.isfinite(self.fmax_hz) or self.fmax_hz <= self.fmin_hz:
            raise ValueError("fmax_hz must be finite and > fmin_hz")
        if not self.psd_method.strip():
            raise ValueError("psd_method must be non-empty")
        if not self.aperiodic_model.strip():
            raise ValueError("aperiodic_model must be non-empty")
        if not self.periodic_model.strip():
            raise ValueError("periodic_model must be non-empty")
        if self.window_seconds is not None and (
            not math.isfinite(self.window_seconds) or self.window_seconds <= 0
        ):
            raise ValueError("window_seconds must be finite and > 0 when present")
        if self.overlap_fraction is not None and (
            not math.isfinite(self.overlap_fraction)
            or not 0 <= self.overlap_fraction < 1
        ):
            raise ValueError("overlap_fraction must satisfy 0 <= value < 1")


@dataclass(frozen=True)
class DescriptiveSpectralEstimate:
    method_name: str
    method_version: str
    config: SpectralConfig
    state: SpectralState
    diagnostics: Mapping[str, Any]

    def __post_init__(self) -> None:
        if not self.method_name.strip():
            raise ValueError("method_name must be non-empty")
        if not self.method_version.strip():
            raise ValueError("method_version must be non-empty")

    @property
    def licenses_dynamical_chi(self) -> bool:
        """Descriptive spectral output never licenses a dynamical chi by itself."""
        return False


@runtime_checkable
class DescriptiveSpectralEstimator(Protocol):
    name: str
    version: str

    def estimate(
        self,
        signal: Sequence[float],
        sampling_rate_hz: float,
        config: SpectralConfig,
    ) -> DescriptiveSpectralEstimate:
        ...
