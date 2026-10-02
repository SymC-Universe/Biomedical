"""Diagnostics for descriptive periodic/aperiodic parameterization.

These diagnostics expose failure-warning structure without silently turning any
one warning into a universal admission threshold. Hard admission/refusal rules
are frozen separately after known-truth calibration.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math

from .specparam_adapter import SpecparamDescriptiveResult


class ParameterizationFlag(str, Enum):
    PEAK_AT_LOWER_WIDTH_LIMIT = "PARAM_PEAK_AT_LOWER_WIDTH_LIMIT"
    PEAK_AT_UPPER_WIDTH_LIMIT = "PARAM_PEAK_AT_UPPER_WIDTH_LIMIT"
    MAX_PEAK_COUNT_REACHED = "PARAM_MAX_PEAK_COUNT_REACHED"
    APERIODIC_MODEL_PEAK_COUNT_DISAGREEMENT = "PARAM_APERIODIC_MODEL_PEAK_COUNT_DISAGREEMENT"
    APERIODIC_MODEL_PEAK_LOCATION_DISAGREEMENT = "PARAM_APERIODIC_MODEL_PEAK_LOCATION_DISAGREEMENT"


@dataclass(frozen=True)
class ParameterizationDiagnostics:
    flags: tuple[ParameterizationFlag, ...]
    lower_width_limit_hit_count: int
    upper_width_limit_hit_count: int
    max_peak_count_reached: bool

    @property
    def has_boundary_hit(self) -> bool:
        return self.lower_width_limit_hit_count > 0 or self.upper_width_limit_hit_count > 0


@dataclass(frozen=True)
class AperiodicModelComparison:
    first_mode: str
    second_mode: str
    first_peak_count: int
    second_peak_count: int
    matched_peak_count: int
    unmatched_first_peak_count: int
    unmatched_second_peak_count: int
    flags: tuple[ParameterizationFlag, ...]


def diagnose_parameterization(
    result: SpecparamDescriptiveResult,
    *,
    width_boundary_tolerance_hz: float = 0.02,
) -> ParameterizationDiagnostics:
    """Expose descriptive fit warnings without assigning biological meaning."""
    if not math.isfinite(width_boundary_tolerance_hz) or width_boundary_tolerance_hz < 0:
        raise ValueError("width_boundary_tolerance_hz must be finite and >= 0")

    lower, upper = result.settings.peak_width_limits
    lower_hits = sum(
        math.isclose(peak.bandwidth_hz, lower, rel_tol=0.0, abs_tol=width_boundary_tolerance_hz)
        for peak in result.peaks
    )
    upper_hits = sum(
        math.isclose(peak.bandwidth_hz, upper, rel_tol=0.0, abs_tol=width_boundary_tolerance_hz)
        for peak in result.peaks
    )
    max_count = result.settings.max_n_peaks > 0 and len(result.peaks) >= result.settings.max_n_peaks

    flags: list[ParameterizationFlag] = []
    if lower_hits:
        flags.append(ParameterizationFlag.PEAK_AT_LOWER_WIDTH_LIMIT)
    if upper_hits:
        flags.append(ParameterizationFlag.PEAK_AT_UPPER_WIDTH_LIMIT)
    if max_count:
        flags.append(ParameterizationFlag.MAX_PEAK_COUNT_REACHED)

    return ParameterizationDiagnostics(
        flags=tuple(flags),
        lower_width_limit_hit_count=lower_hits,
        upper_width_limit_hit_count=upper_hits,
        max_peak_count_reached=max_count,
    )


def compare_aperiodic_models(
    first: SpecparamDescriptiveResult,
    second: SpecparamDescriptiveResult,
    *,
    center_tolerance_hz: float = 1.0,
) -> AperiodicModelComparison:
    """Compare descriptive peak structure across two aperiodic model families.

    Peak matching is center-frequency-only on purpose. Width is already model
    dependent and is not used here to manufacture stronger equivalence.
    """
    if not math.isfinite(center_tolerance_hz) or center_tolerance_hz < 0:
        raise ValueError("center_tolerance_hz must be finite and >= 0")
    if first.settings.fmin_hz != second.settings.fmin_hz or first.settings.fmax_hz != second.settings.fmax_hz:
        raise ValueError("aperiodic model comparison requires the same frequency range")

    remaining_second = set(range(len(second.peaks)))
    matched = 0
    for first_peak in first.peaks:
        candidates = [
            index
            for index in remaining_second
            if abs(first_peak.center_frequency_hz - second.peaks[index].center_frequency_hz)
            <= center_tolerance_hz
        ]
        if not candidates:
            continue
        best = min(
            candidates,
            key=lambda index: abs(first_peak.center_frequency_hz - second.peaks[index].center_frequency_hz),
        )
        remaining_second.remove(best)
        matched += 1

    unmatched_first = len(first.peaks) - matched
    unmatched_second = len(second.peaks) - matched
    flags: list[ParameterizationFlag] = []
    if len(first.peaks) != len(second.peaks):
        flags.append(ParameterizationFlag.APERIODIC_MODEL_PEAK_COUNT_DISAGREEMENT)
    if unmatched_first or unmatched_second:
        flags.append(ParameterizationFlag.APERIODIC_MODEL_PEAK_LOCATION_DISAGREEMENT)

    return AperiodicModelComparison(
        first_mode=first.settings.aperiodic_mode,
        second_mode=second.settings.aperiodic_mode,
        first_peak_count=len(first.peaks),
        second_peak_count=len(second.peaks),
        matched_peak_count=matched,
        unmatched_first_peak_count=unmatched_first,
        unmatched_second_peak_count=unmatched_second,
        flags=tuple(flags),
    )
