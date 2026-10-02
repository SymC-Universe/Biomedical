"""Dependency-light EDF sample access for D4/D5 qualification.

The reader is intentionally small and transparent. It supports ordinary EDF
16-bit data records, uses the parsed header from :mod:`nsd_engine.edf`, and can
read a bounded time window from selected channels without loading the entire
recording.

It is not a replacement for a mature neurophysiology library. Its purpose is to
make byte-to-sample identity and EDF digital-to-physical scaling independently
auditable before higher-level estimators are introduced.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import struct
from typing import Sequence

from .edf import EDFHeader, EDFHeaderError, EDFSignalHeader, read_edf_header


@dataclass(frozen=True)
class EDFChannelWindow:
    label: str
    sampling_rate_hz: float
    start_seconds: float
    duration_seconds: float
    physical_dimension: str
    digital_samples: tuple[int, ...]
    physical_samples: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("label must be non-empty")
        if not math.isfinite(self.sampling_rate_hz) or self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz must be finite and > 0")
        if not math.isfinite(self.start_seconds) or self.start_seconds < 0:
            raise ValueError("start_seconds must be finite and >= 0")
        if not math.isfinite(self.duration_seconds) or self.duration_seconds <= 0:
            raise ValueError("duration_seconds must be finite and > 0")
        if len(self.digital_samples) != len(self.physical_samples):
            raise ValueError("digital_samples and physical_samples must have equal length")


def digital_to_physical(signal: EDFSignalHeader, digital_value: int) -> float:
    """Apply the EDF linear digital-to-physical calibration exactly."""
    digital_span = signal.digital_maximum - signal.digital_minimum
    physical_span = signal.physical_maximum - signal.physical_minimum
    if digital_span <= 0:
        raise EDFHeaderError("invalid EDF digital span")
    return (
        (digital_value - signal.digital_minimum) * physical_span / digital_span
        + signal.physical_minimum
    )


def _record_layout(header: EDFHeader) -> tuple[int, tuple[int, ...]]:
    offsets: list[int] = []
    cursor = 0
    for signal in header.signals:
        offsets.append(cursor)
        cursor += signal.samples_per_record * 2
    return cursor, tuple(offsets)


def _channel_index(header: EDFHeader, label: str) -> int:
    matches = [index for index, signal in enumerate(header.signals) if signal.label == label]
    if not matches:
        raise KeyError(f"EDF channel label not found: {label!r}")
    if len(matches) > 1:
        raise EDFHeaderError(f"EDF channel label is not unique: {label!r}")
    return matches[0]


def read_edf_channel_window(
    path: str | Path,
    label: str,
    *,
    start_seconds: float = 0.0,
    duration_seconds: float,
    header: EDFHeader | None = None,
) -> EDFChannelWindow:
    """Read one bounded EDF channel window in digital and physical units.

    The requested interval is converted to sample indices using floor for the
    starting sample and ceiling for the exclusive ending sample. The returned
    duration is the actual number of returned samples divided by the channel
    sampling rate.
    """
    if not math.isfinite(start_seconds) or start_seconds < 0:
        raise ValueError("start_seconds must be finite and >= 0")
    if not math.isfinite(duration_seconds) or duration_seconds <= 0:
        raise ValueError("duration_seconds must be finite and > 0")

    path = Path(path)
    header = header or read_edf_header(path)
    index = _channel_index(header, label)
    signal = header.signals[index]
    rate = signal.sampling_rate_hz

    start_sample = int(math.floor(start_seconds * rate))
    end_sample = int(math.ceil((start_seconds + duration_seconds) * rate))

    if header.data_record_count < 0:
        raise EDFHeaderError("sample-window reading requires known EDF data_record_count")
    total_samples = header.data_record_count * signal.samples_per_record
    if start_sample >= total_samples:
        raise ValueError("start_seconds is outside the recording")
    end_sample = min(end_sample, total_samples)
    if end_sample <= start_sample:
        raise ValueError("requested window contains no samples")

    record_bytes, channel_offsets = _record_layout(header)
    channel_offset = channel_offsets[index]
    samples_per_record = signal.samples_per_record
    first_record = start_sample // samples_per_record
    last_record = (end_sample - 1) // samples_per_record

    digital: list[int] = []
    with path.open("rb") as handle:
        for record_index in range(first_record, last_record + 1):
            file_offset = header.header_bytes + record_index * record_bytes + channel_offset
            handle.seek(file_offset)
            raw = handle.read(samples_per_record * 2)
            expected = samples_per_record * 2
            if len(raw) != expected:
                raise EDFHeaderError(
                    f"truncated EDF data record {record_index} channel {label!r}: "
                    f"expected {expected} bytes, got {len(raw)}"
                )
            record_values = struct.unpack(f"<{samples_per_record}h", raw)

            record_start_sample = record_index * samples_per_record
            left = max(start_sample, record_start_sample) - record_start_sample
            right = min(end_sample, record_start_sample + samples_per_record) - record_start_sample
            digital.extend(record_values[left:right])

    physical = tuple(digital_to_physical(signal, value) for value in digital)
    actual_duration = len(digital) / rate
    return EDFChannelWindow(
        label=label,
        sampling_rate_hz=rate,
        start_seconds=start_sample / rate,
        duration_seconds=actual_duration,
        physical_dimension=signal.physical_dimension,
        digital_samples=tuple(digital),
        physical_samples=physical,
    )


def read_edf_window(
    path: str | Path,
    labels: Sequence[str],
    *,
    start_seconds: float = 0.0,
    duration_seconds: float,
) -> tuple[EDFChannelWindow, ...]:
    """Read the same bounded interval from a declared channel list."""
    if not labels:
        raise ValueError("labels must not be empty")
    if len(set(labels)) != len(labels):
        raise ValueError("labels must be unique")
    header = read_edf_header(path)
    return tuple(
        read_edf_channel_window(
            path,
            label,
            start_seconds=start_seconds,
            duration_seconds=duration_seconds,
            header=header,
        )
        for label in labels
    )
