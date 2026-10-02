"""Label-blind signal-integrity metrics for the NSD Structural Engine.

The module deliberately separates *measurement* from *admission thresholds*.
It computes generic channel-level integrity quantities and applies only thresholds
that are explicitly supplied by the caller. There is no universal EEG-quality
cutoff hidden in this module.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping, Sequence

from .schema import SignalQC


@dataclass(frozen=True)
class QCThresholds:
    """Frozen task-specific thresholds for generic signal-integrity checks.

    ``None`` means that the corresponding metric is reported but does not by
    itself fail the recording. This prevents a convenience default from becoming
    an undocumented scientific threshold.
    """

    min_channel_count: int | None = None
    max_missing_fraction_per_channel: float | None = None
    max_flat_channels: int | None = None
    max_edge_fraction_per_channel: float | None = None
    flat_tolerance: float = 0.0

    def __post_init__(self) -> None:
        if self.min_channel_count is not None and self.min_channel_count <= 0:
            raise ValueError("min_channel_count must be > 0 when supplied")
        if self.max_flat_channels is not None and self.max_flat_channels < 0:
            raise ValueError("max_flat_channels must be >= 0 when supplied")
        for name in ("max_missing_fraction_per_channel", "max_edge_fraction_per_channel"):
            value = getattr(self, name)
            if value is not None and (not math.isfinite(value) or not 0.0 <= value <= 1.0):
                raise ValueError(f"{name} must lie in [0, 1] when supplied")
        if not math.isfinite(self.flat_tolerance) or self.flat_tolerance < 0:
            raise ValueError("flat_tolerance must be finite and >= 0")


@dataclass(frozen=True)
class ChannelQC:
    channel_name: str
    sample_count: int
    finite_sample_count: int
    missing_fraction: float
    minimum: float | None
    maximum: float | None
    amplitude_range: float | None
    flat: bool
    edge_fraction: float | None

    def __post_init__(self) -> None:
        if not self.channel_name.strip():
            raise ValueError("channel_name must be non-empty")
        if self.sample_count <= 0:
            raise ValueError("sample_count must be > 0")
        if not 0 <= self.finite_sample_count <= self.sample_count:
            raise ValueError("finite_sample_count must lie within sample_count")
        if not 0.0 <= self.missing_fraction <= 1.0:
            raise ValueError("missing_fraction must lie in [0, 1]")
        if self.edge_fraction is not None and not 0.0 <= self.edge_fraction <= 1.0:
            raise ValueError("edge_fraction must lie in [0, 1] when present")


@dataclass(frozen=True)
class SignalQCReport:
    signal_qc: SignalQC
    channels: tuple[ChannelQC, ...]
    sampling_rate_hz: float
    sample_count: int
    thresholds: QCThresholds

    def __post_init__(self) -> None:
        if not math.isfinite(self.sampling_rate_hz) or self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz must be finite and > 0")
        if self.sample_count <= 0:
            raise ValueError("sample_count must be > 0")
        if not self.channels:
            raise ValueError("at least one channel is required")


def _channel_qc(name: str, values: Sequence[float], flat_tolerance: float) -> ChannelQC:
    if not name.strip():
        raise ValueError("channel names must be non-empty")
    if not values:
        raise ValueError(f"channel {name!r} has no samples")

    finite = [float(value) for value in values if math.isfinite(float(value))]
    sample_count = len(values)
    finite_count = len(finite)
    missing_fraction = (sample_count - finite_count) / sample_count

    if not finite:
        return ChannelQC(
            channel_name=name,
            sample_count=sample_count,
            finite_sample_count=0,
            missing_fraction=1.0,
            minimum=None,
            maximum=None,
            amplitude_range=None,
            flat=False,
            edge_fraction=None,
        )

    minimum = min(finite)
    maximum = max(finite)
    amplitude_range = maximum - minimum
    flat = amplitude_range <= flat_tolerance

    # Repeated occupancy at the observed numerical extremes is a generic
    # clipping/saturation *indicator*, not proof of hardware clipping. The
    # task-specific threshold, if any, is supplied explicitly above.
    if flat:
        edge_fraction = 1.0
    else:
        edge_count = sum(value == minimum or value == maximum for value in finite)
        edge_fraction = edge_count / finite_count

    return ChannelQC(
        channel_name=name,
        sample_count=sample_count,
        finite_sample_count=finite_count,
        missing_fraction=missing_fraction,
        minimum=minimum,
        maximum=maximum,
        amplitude_range=amplitude_range,
        flat=flat,
        edge_fraction=edge_fraction,
    )


def evaluate_signal_qc(
    channels: Mapping[str, Sequence[float]],
    sampling_rate_hz: float,
    *,
    thresholds: QCThresholds | None = None,
) -> SignalQCReport:
    """Measure generic multi-channel signal integrity without clinical labels.

    All channels must contain the same number of samples. The returned usable
    duration is conservative: total duration multiplied by the *minimum* finite
    fraction across channels. This is a bookkeeping quantity, not a claim that
    every missing sample occurs at the same time across channels.
    """
    if not math.isfinite(sampling_rate_hz) or sampling_rate_hz <= 0:
        raise ValueError("sampling_rate_hz must be finite and > 0")
    if not channels:
        raise ValueError("at least one channel is required")

    thresholds = thresholds or QCThresholds()
    lengths = {len(values) for values in channels.values()}
    if 0 in lengths:
        raise ValueError("channels must contain at least one sample")
    if len(lengths) != 1:
        raise ValueError("all channels must have the same sample count")
    sample_count = next(iter(lengths))

    channel_results = tuple(
        _channel_qc(name, values, thresholds.flat_tolerance)
        for name, values in sorted(channels.items())
    )

    duration_seconds = sample_count / sampling_rate_hz
    minimum_finite_fraction = min(1.0 - item.missing_fraction for item in channel_results)
    usable_duration_seconds = duration_seconds * minimum_finite_fraction

    flags: list[str] = []
    if any(item.finite_sample_count == 0 for item in channel_results):
        flags.append("QC_CHANNEL_NO_FINITE_DATA")

    flat_count = sum(item.flat for item in channel_results)
    if thresholds.min_channel_count is not None and len(channel_results) < thresholds.min_channel_count:
        flags.append("QC_TOO_FEW_CHANNELS")
    if thresholds.max_flat_channels is not None and flat_count > thresholds.max_flat_channels:
        flags.append("QC_TOO_MANY_FLAT_CHANNELS")
    if thresholds.max_missing_fraction_per_channel is not None and any(
        item.missing_fraction > thresholds.max_missing_fraction_per_channel
        for item in channel_results
    ):
        flags.append("QC_EXCESS_MISSINGNESS")
    if thresholds.max_edge_fraction_per_channel is not None and any(
        item.edge_fraction is not None
        and item.edge_fraction > thresholds.max_edge_fraction_per_channel
        for item in channel_results
    ):
        flags.append("QC_EXCESS_EXTREME_OCCUPANCY")

    signal_qc = SignalQC(
        duration_seconds=duration_seconds,
        usable_duration_seconds=usable_duration_seconds,
        passed_signal_integrity=not flags,
        flags=tuple(flags),
    )
    return SignalQCReport(
        signal_qc=signal_qc,
        channels=channel_results,
        sampling_rate_hz=sampling_rate_hz,
        sample_count=sample_count,
        thresholds=thresholds,
    )
