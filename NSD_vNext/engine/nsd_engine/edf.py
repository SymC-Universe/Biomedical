"""Minimal EDF/EDF+ header inspection for dataset D4 verification.

This is not an EEG-analysis reader. It reads only the standardized EDF header
needed to verify file identity, channel count, duration, and per-channel sample
rates before a scientific pipeline is allowed to consume the payload.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import BinaryIO


class EDFHeaderError(ValueError):
    pass


def _decode(field: bytes) -> str:
    return field.decode("ascii", errors="strict").strip()


def _parse_int(field: bytes, name: str) -> int:
    text = _decode(field)
    try:
        return int(text)
    except ValueError as exc:
        raise EDFHeaderError(f"invalid integer field {name}: {text!r}") from exc


def _parse_float(field: bytes, name: str) -> float:
    text = _decode(field)
    try:
        value = float(text)
    except ValueError as exc:
        raise EDFHeaderError(f"invalid float field {name}: {text!r}") from exc
    if not math.isfinite(value):
        raise EDFHeaderError(f"non-finite float field {name}: {text!r}")
    return value


@dataclass(frozen=True)
class EDFSignalHeader:
    label: str
    physical_dimension: str
    physical_minimum: float
    physical_maximum: float
    digital_minimum: int
    digital_maximum: int
    samples_per_record: int
    sampling_rate_hz: float


@dataclass(frozen=True)
class EDFHeader:
    version: str
    patient_id: str
    recording_id: str
    start_date: str
    start_time: str
    header_bytes: int
    reserved: str
    data_record_count: int
    data_record_duration_seconds: float
    signal_count: int
    signals: tuple[EDFSignalHeader, ...]

    @property
    def recording_duration_seconds(self) -> float | None:
        if self.data_record_count < 0:
            return None
        return self.data_record_count * self.data_record_duration_seconds

    @property
    def expected_file_size_bytes(self) -> int | None:
        """Expected EDF size for ordinary 16-bit data records.

        EDF stores each sample as a two-byte integer. For files that declare an
        unknown number of records (-1), exact payload size is intentionally not
        inferred.
        """
        if self.data_record_count < 0:
            return None
        samples_per_record = sum(signal.samples_per_record for signal in self.signals)
        return self.header_bytes + self.data_record_count * samples_per_record * 2


def _read_exact(handle: BinaryIO, count: int, name: str) -> bytes:
    data = handle.read(count)
    if len(data) != count:
        raise EDFHeaderError(f"truncated EDF while reading {name}: expected {count}, got {len(data)}")
    return data


def _split_signal_fields(block: bytes, width: int, signal_count: int) -> tuple[bytes, ...]:
    expected = width * signal_count
    if len(block) != expected:
        raise EDFHeaderError("internal signal-field block length mismatch")
    return tuple(block[i * width : (i + 1) * width] for i in range(signal_count))


def read_edf_header(path: str | Path) -> EDFHeader:
    path = Path(path)
    with path.open("rb") as handle:
        fixed = _read_exact(handle, 256, "fixed header")

        version = _decode(fixed[0:8])
        patient_id = _decode(fixed[8:88])
        recording_id = _decode(fixed[88:168])
        start_date = _decode(fixed[168:176])
        start_time = _decode(fixed[176:184])
        header_bytes = _parse_int(fixed[184:192], "header_bytes")
        reserved = _decode(fixed[192:236])
        data_record_count = _parse_int(fixed[236:244], "data_record_count")
        data_record_duration = _parse_float(fixed[244:252], "data_record_duration_seconds")
        signal_count = _parse_int(fixed[252:256], "signal_count")

        if signal_count <= 0:
            raise EDFHeaderError("signal_count must be > 0")
        if data_record_duration <= 0:
            raise EDFHeaderError("data_record_duration_seconds must be > 0")
        expected_header_bytes = 256 + 256 * signal_count
        if header_bytes != expected_header_bytes:
            raise EDFHeaderError(
                f"header_bytes mismatch: declared {header_bytes}, expected {expected_header_bytes} for {signal_count} signals"
            )

        labels = _split_signal_fields(_read_exact(handle, 16 * signal_count, "signal labels"), 16, signal_count)
        _read_exact(handle, 80 * signal_count, "transducer types")
        physical_dimensions = _split_signal_fields(
            _read_exact(handle, 8 * signal_count, "physical dimensions"), 8, signal_count
        )
        physical_minima = _split_signal_fields(
            _read_exact(handle, 8 * signal_count, "physical minima"), 8, signal_count
        )
        physical_maxima = _split_signal_fields(
            _read_exact(handle, 8 * signal_count, "physical maxima"), 8, signal_count
        )
        digital_minima = _split_signal_fields(
            _read_exact(handle, 8 * signal_count, "digital minima"), 8, signal_count
        )
        digital_maxima = _split_signal_fields(
            _read_exact(handle, 8 * signal_count, "digital maxima"), 8, signal_count
        )
        _read_exact(handle, 80 * signal_count, "prefiltering")
        samples_per_record_fields = _split_signal_fields(
            _read_exact(handle, 8 * signal_count, "samples per record"), 8, signal_count
        )
        _read_exact(handle, 32 * signal_count, "signal reserved fields")

    signals: list[EDFSignalHeader] = []
    for index in range(signal_count):
        samples_per_record = _parse_int(samples_per_record_fields[index], f"samples_per_record[{index}]")
        if samples_per_record <= 0:
            raise EDFHeaderError(f"samples_per_record[{index}] must be > 0")
        physical_minimum = _parse_float(physical_minima[index], f"physical_minimum[{index}]")
        physical_maximum = _parse_float(physical_maxima[index], f"physical_maximum[{index}]")
        digital_minimum = _parse_int(digital_minima[index], f"digital_minimum[{index}]")
        digital_maximum = _parse_int(digital_maxima[index], f"digital_maximum[{index}]")
        if physical_maximum <= physical_minimum:
            raise EDFHeaderError(f"physical range invalid for signal {index}")
        if digital_maximum <= digital_minimum:
            raise EDFHeaderError(f"digital range invalid for signal {index}")

        signals.append(
            EDFSignalHeader(
                label=_decode(labels[index]),
                physical_dimension=_decode(physical_dimensions[index]),
                physical_minimum=physical_minimum,
                physical_maximum=physical_maximum,
                digital_minimum=digital_minimum,
                digital_maximum=digital_maximum,
                samples_per_record=samples_per_record,
                sampling_rate_hz=samples_per_record / data_record_duration,
            )
        )

    return EDFHeader(
        version=version,
        patient_id=patient_id,
        recording_id=recording_id,
        start_date=start_date,
        start_time=start_time,
        header_bytes=header_bytes,
        reserved=reserved,
        data_record_count=data_record_count,
        data_record_duration_seconds=data_record_duration,
        signal_count=signal_count,
        signals=tuple(signals),
    )
