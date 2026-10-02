from pathlib import Path
import struct

import pytest

from nsd_engine.edf_samples import digital_to_physical, read_edf_channel_window, read_edf_window
from nsd_engine.edf import read_edf_header


def _field(value: object, width: int) -> bytes:
    text = str(value).encode("ascii")
    if len(text) > width:
        raise ValueError("fixture field too long")
    return text + b" " * (width - len(text))


def _write_sample_edf(path: Path) -> None:
    signal_count = 2
    record_count = 2
    duration = 1
    spr = 4
    header_bytes = 256 + 256 * signal_count

    fixed = b"".join(
        [
            _field("0", 8),
            _field("patient", 80),
            _field("recording", 80),
            _field("01.01.26", 8),
            _field("12.00.00", 8),
            _field(header_bytes, 8),
            _field("", 44),
            _field(record_count, 8),
            _field(duration, 8),
            _field(signal_count, 4),
        ]
    )
    signal_header = b"".join(
        [
            b"".join(_field(v, 16) for v in ("C3", "C4")),
            b"".join(_field("", 80) for _ in range(signal_count)),
            b"".join(_field("uV", 8) for _ in range(signal_count)),
            b"".join(_field(-100, 8) for _ in range(signal_count)),
            b"".join(_field(100, 8) for _ in range(signal_count)),
            b"".join(_field(-1000, 8) for _ in range(signal_count)),
            b"".join(_field(1000, 8) for _ in range(signal_count)),
            b"".join(_field("", 80) for _ in range(signal_count)),
            b"".join(_field(spr, 8) for _ in range(signal_count)),
            b"".join(_field("", 32) for _ in range(signal_count)),
        ]
    )

    records = [
        ((-1000, 0, 1000, 500), (1000, 0, -1000, -500)),
        ((250, 500, 750, 1000), (-250, -500, -750, -1000)),
    ]
    payload = bytearray()
    for c3, c4 in records:
        payload.extend(struct.pack("<4h", *c3))
        payload.extend(struct.pack("<4h", *c4))

    path.write_bytes(fixed + signal_header + bytes(payload))


def test_digital_to_physical_uses_edf_calibration(tmp_path):
    path = tmp_path / "sample.edf"
    _write_sample_edf(path)
    header = read_edf_header(path)
    signal = header.signals[0]

    assert digital_to_physical(signal, -1000) == pytest.approx(-100.0)
    assert digital_to_physical(signal, 0) == pytest.approx(0.0)
    assert digital_to_physical(signal, 1000) == pytest.approx(100.0)


def test_read_channel_window_crosses_data_record_boundary(tmp_path):
    path = tmp_path / "sample.edf"
    _write_sample_edf(path)

    result = read_edf_channel_window(path, "C3", start_seconds=0.5, duration_seconds=1.0)

    assert result.sampling_rate_hz == pytest.approx(4.0)
    assert result.start_seconds == pytest.approx(0.5)
    assert result.duration_seconds == pytest.approx(1.0)
    assert result.digital_samples == (1000, 500, 250, 500)
    assert result.physical_samples == pytest.approx((100.0, 50.0, 25.0, 50.0))
    assert result.physical_dimension == "uV"


def test_read_multiple_channels_preserves_requested_order(tmp_path):
    path = tmp_path / "sample.edf"
    _write_sample_edf(path)

    windows = read_edf_window(path, ["C4", "C3"], start_seconds=0.0, duration_seconds=0.5)
    assert [item.label for item in windows] == ["C4", "C3"]
    assert windows[0].digital_samples == (1000, 0)
    assert windows[1].digital_samples == (-1000, 0)


def test_read_unknown_channel_refuses(tmp_path):
    path = tmp_path / "sample.edf"
    _write_sample_edf(path)

    with pytest.raises(KeyError, match="channel label not found"):
        read_edf_channel_window(path, "NOPE", duration_seconds=1.0)


def test_read_window_clips_cleanly_at_recording_end(tmp_path):
    path = tmp_path / "sample.edf"
    _write_sample_edf(path)

    result = read_edf_channel_window(path, "C3", start_seconds=1.5, duration_seconds=2.0)
    assert result.digital_samples == (750, 1000)
    assert result.duration_seconds == pytest.approx(0.5)
