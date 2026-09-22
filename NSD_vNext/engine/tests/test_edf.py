from pathlib import Path

import pytest

from nsd_engine.edf import EDFHeaderError, read_edf_header


def _field(value: object, width: int) -> bytes:
    text = str(value).encode("ascii")
    if len(text) > width:
        raise ValueError("fixture field too long")
    return text + b" " * (width - len(text))


def _write_synthetic_edf(path: Path) -> None:
    signal_count = 2
    record_count = 2
    record_duration = 1
    samples_per_record = [4, 4]
    header_bytes = 256 + 256 * signal_count

    fixed = b"".join(
        [
            _field("0", 8),
            _field("synthetic-patient", 80),
            _field("synthetic-recording", 80),
            _field("01.01.26", 8),
            _field("12.00.00", 8),
            _field(header_bytes, 8),
            _field("", 44),
            _field(record_count, 8),
            _field(record_duration, 8),
            _field(signal_count, 4),
        ]
    )
    assert len(fixed) == 256

    signal_header = b"".join(
        [
            b"".join(_field(value, 16) for value in ("C3", "C4")),
            b"".join(_field("", 80) for _ in range(signal_count)),
            b"".join(_field("uV", 8) for _ in range(signal_count)),
            b"".join(_field(-100, 8) for _ in range(signal_count)),
            b"".join(_field(100, 8) for _ in range(signal_count)),
            b"".join(_field(-32768, 8) for _ in range(signal_count)),
            b"".join(_field(32767, 8) for _ in range(signal_count)),
            b"".join(_field("", 80) for _ in range(signal_count)),
            b"".join(_field(value, 8) for value in samples_per_record),
            b"".join(_field("", 32) for _ in range(signal_count)),
        ]
    )
    assert len(signal_header) == 256 * signal_count

    payload_samples = record_count * sum(samples_per_record)
    payload = b"\x00\x00" * payload_samples
    path.write_bytes(fixed + signal_header + payload)


def test_read_edf_header_recovers_d4_identity_metrics(tmp_path):
    path = tmp_path / "fixture.edf"
    _write_synthetic_edf(path)

    header = read_edf_header(path)

    assert header.signal_count == 2
    assert header.header_bytes == 768
    assert header.recording_duration_seconds == pytest.approx(2.0)
    assert [signal.label for signal in header.signals] == ["C3", "C4"]
    assert [signal.sampling_rate_hz for signal in header.signals] == pytest.approx([4.0, 4.0])
    assert header.expected_file_size_bytes == path.stat().st_size == 800


def test_read_edf_header_refuses_truncated_file(tmp_path):
    path = tmp_path / "truncated.edf"
    path.write_bytes(b"0" * 100)

    with pytest.raises(EDFHeaderError, match="truncated EDF"):
        read_edf_header(path)


def test_read_edf_header_refuses_declared_header_size_mismatch(tmp_path):
    path = tmp_path / "fixture.edf"
    _write_synthetic_edf(path)
    data = bytearray(path.read_bytes())
    data[184:192] = _field(999, 8)
    path.write_bytes(bytes(data))

    with pytest.raises(EDFHeaderError, match="header_bytes mismatch"):
        read_edf_header(path)


def test_source_declared_invalid_physical_range_can_be_ignored_for_d4_header_audit(tmp_path):
    path = tmp_path / "invalid-physical-range.edf"
    _write_synthetic_edf(path)
    data = bytearray(path.read_bytes())

    signal_count = 2
    physical_min_start = 256 + 16 * signal_count + 80 * signal_count + 8 * signal_count
    physical_max_start = physical_min_start + 8 * signal_count

    data[physical_min_start : physical_min_start + 8] = _field(100, 8)
    data[physical_max_start : physical_max_start + 8] = _field(-100, 8)
    path.write_bytes(bytes(data))

    with pytest.raises(EDFHeaderError, match="physical range invalid"):
        read_edf_header(path)

    header = read_edf_header(path, validate_physical_range=False)
    assert header.signal_count == 2
    assert header.expected_file_size_bytes == path.stat().st_size
    assert header.signals[0].physical_minimum == pytest.approx(100.0)
    assert header.signals[0].physical_maximum == pytest.approx(-100.0)
