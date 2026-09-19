"""Auditable data contracts for the NSD vNext Structural Engine.

Scientific estimators are deliberately absent from this module. The purpose of
this scaffold is to make provenance, refusals, mode lineage, and scalar
admission machine-readable before any clinical analysis is implemented.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import math
from typing import Any, Mapping, Optional


class RefusalCode(str, Enum):
    META_AMBIGUOUS = "REF_META_AMBIGUOUS"
    SIGNAL_INSUFFICIENT = "REF_SIGNAL_INSUFFICIENT"
    SPECTRAL_POOR_FIT = "REF_SPECTRAL_POOR_FIT"
    NO_PEAK = "REF_NO_PEAK"
    MODE_NONIDENTIFIABLE = "REF_MODE_NONIDENTIFIABLE"
    MODEL_DISAGREEMENT = "REF_MODEL_DISAGREEMENT"
    WIDTH_NOT_DAMPING = "REF_WIDTH_NOT_DAMPING"
    FREQ_NOT_OMEGA0 = "REF_FREQ_NOT_OMEGA0"
    BROADENING_UNRESOLVED = "REF_BROADENING_UNRESOLVED"
    UNCERTAINTY_TOO_LARGE = "REF_UNCERTAINTY_TOO_LARGE"
    OUT_OF_DOMAIN = "REF_OUT_OF_DOMAIN"


def _require_nonempty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_finite_positive(value: float, field_name: str, *, allow_zero: bool = False) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{field_name} must be finite")
    if allow_zero:
        if value < 0:
            raise ValueError(f"{field_name} must be >= 0")
    elif value <= 0:
        raise ValueError(f"{field_name} must be > 0")


def canonical_config_hash(config: Mapping[str, Any]) -> str:
    """Return a stable SHA-256 over a JSON-serializable configuration mapping."""
    payload = json.dumps(config, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ProvenanceRecord:
    subject_id: str
    session_id: str
    recording_condition: str
    source_dataset: str
    sampling_rate_hz: float
    engine_version: str
    config_hash: str
    run_id: str

    def __post_init__(self) -> None:
        for name in (
            "subject_id",
            "session_id",
            "recording_condition",
            "source_dataset",
            "engine_version",
            "config_hash",
            "run_id",
        ):
            _require_nonempty(getattr(self, name), name)
        _require_finite_positive(self.sampling_rate_hz, "sampling_rate_hz")
        if len(self.config_hash) != 64 or any(c not in "0123456789abcdef" for c in self.config_hash.lower()):
            raise ValueError("config_hash must be a 64-character hexadecimal SHA-256 string")


@dataclass(frozen=True)
class SignalQC:
    duration_seconds: float
    usable_duration_seconds: float
    passed_signal_integrity: bool
    flags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_finite_positive(self.duration_seconds, "duration_seconds")
        _require_finite_positive(self.usable_duration_seconds, "usable_duration_seconds", allow_zero=True)
        if self.usable_duration_seconds > self.duration_seconds:
            raise ValueError("usable_duration_seconds cannot exceed duration_seconds")
        for flag in self.flags:
            _require_nonempty(flag, "SignalQC.flags item")


@dataclass(frozen=True)
class SpectralPeak:
    peak_id: str
    center_frequency_hz: float
    power: float
    bandwidth_hz: float
    model_family: str

    def __post_init__(self) -> None:
        _require_nonempty(self.peak_id, "peak_id")
        _require_finite_positive(self.center_frequency_hz, "center_frequency_hz")
        if not math.isfinite(self.power):
            raise ValueError("power must be finite")
        _require_finite_positive(self.bandwidth_hz, "bandwidth_hz")
        _require_nonempty(self.model_family, "model_family")


@dataclass(frozen=True)
class SpectralState:
    aperiodic_exponent: Optional[float]
    aperiodic_offset: Optional[float]
    peaks: tuple[SpectralPeak, ...] = ()
    fit_quality: Mapping[str, float] = field(default_factory=dict)
    fit_model: str = "unspecified"

    def __post_init__(self) -> None:
        if self.aperiodic_exponent is not None and not math.isfinite(self.aperiodic_exponent):
            raise ValueError("aperiodic_exponent must be finite when present")
        if self.aperiodic_offset is not None and not math.isfinite(self.aperiodic_offset):
            raise ValueError("aperiodic_offset must be finite when present")
        _require_nonempty(self.fit_model, "fit_model")
        ids = [peak.peak_id for peak in self.peaks]
        if len(ids) != len(set(ids)):
            raise ValueError("SpectralState peak_id values must be unique")
        for name, value in self.fit_quality.items():
            _require_nonempty(str(name), "fit_quality key")
            if not math.isfinite(float(value)):
                raise ValueError(f"fit_quality[{name!r}] must be finite")


@dataclass(frozen=True)
class CandidateMode:
    mode_id: str
    source_method: str
    frequency_hz: Optional[float] = None
    decay_rate_per_s: Optional[float] = None
    pole_real_per_s: Optional[float] = None
    pole_imag_rad_s: Optional[float] = None
    identifiable: bool = False
    diagnostics: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_nonempty(self.mode_id, "mode_id")
        _require_nonempty(self.source_method, "source_method")
        for name in ("frequency_hz", "decay_rate_per_s", "pole_real_per_s", "pole_imag_rad_s"):
            value = getattr(self, name)
            if value is not None and not math.isfinite(value):
                raise ValueError(f"{name} must be finite when present")
        if self.frequency_hz is not None and self.frequency_hz <= 0:
            raise ValueError("frequency_hz must be > 0 when present")


@dataclass(frozen=True)
class LicensedScalar:
    name: str
    value: float
    uncertainty: Optional[float]
    source_mode_id: str
    derivation: str
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_nonempty(self.name, "LicensedScalar.name")
        _require_nonempty(self.source_mode_id, "LicensedScalar.source_mode_id")
        _require_nonempty(self.derivation, "LicensedScalar.derivation")
        if not math.isfinite(self.value):
            raise ValueError("LicensedScalar.value must be finite")
        if self.uncertainty is not None:
            _require_finite_positive(self.uncertainty, "LicensedScalar.uncertainty", allow_zero=True)
        if self.name.lower() in {"whole_brain_chi", "global_chi", "whole_head_chi"}:
            raise ValueError("A whole-system chi is prohibited by the NSD vNext contract")
        if "chi" in self.name.lower() and not self.source_mode_id.strip():
            raise ValueError("Any chi-like licensed scalar must have explicit source_mode_id lineage")
        for dependency in self.dependencies:
            _require_nonempty(dependency, "LicensedScalar.dependencies item")


@dataclass(frozen=True)
class ScalarRefusal:
    requested_scalar: str
    code: RefusalCode
    detail: str
    source_mode_id: Optional[str] = None

    def __post_init__(self) -> None:
        _require_nonempty(self.requested_scalar, "ScalarRefusal.requested_scalar")
        _require_nonempty(self.detail, "ScalarRefusal.detail")
        if self.source_mode_id is not None:
            _require_nonempty(self.source_mode_id, "ScalarRefusal.source_mode_id")


@dataclass(frozen=True)
class EngineResult:
    provenance: ProvenanceRecord
    signal_qc: SignalQC
    spectral_state: SpectralState
    candidate_modes: tuple[CandidateMode, ...] = ()
    licensed_scalars: tuple[LicensedScalar, ...] = ()
    scalar_refusals: tuple[ScalarRefusal, ...] = ()
    spatial_state: Mapping[str, Any] = field(default_factory=dict)
    conglomerate_state: Mapping[str, Any] = field(default_factory=dict)
    open_channel: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        mode_ids = [mode.mode_id for mode in self.candidate_modes]
        if len(mode_ids) != len(set(mode_ids)):
            raise ValueError("candidate mode_id values must be unique")
        known_modes = set(mode_ids)
        for scalar in self.licensed_scalars:
            if scalar.source_mode_id not in known_modes:
                raise ValueError(
                    f"Licensed scalar {scalar.name!r} references unknown mode {scalar.source_mode_id!r}"
                )
        for refusal in self.scalar_refusals:
            if refusal.source_mode_id is not None and refusal.source_mode_id not in known_modes:
                raise ValueError(
                    f"Scalar refusal {refusal.requested_scalar!r} references unknown mode "
                    f"{refusal.source_mode_id!r}"
                )

    def scalar_names(self) -> tuple[str, ...]:
        return tuple(scalar.name for scalar in self.licensed_scalars)

    def refusal_codes(self) -> tuple[RefusalCode, ...]:
        return tuple(refusal.code for refusal in self.scalar_refusals)
