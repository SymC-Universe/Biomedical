#!/usr/bin/env python3
"""Verify one pinned ds003775 EDF payload against public BIDS/NEMAR metadata.

This script is intentionally dataset-specific and lives under tools rather than
inside the generic Engine API. Passing it promotes only the named pilot file,
not the full dataset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.edf import read_edf_header


EXPECTED_SIZE_BYTES = 31_473_920
EXPECTED_MD5 = "a4aa13370458a970886967bd6dc6d672"
EXPECTED_SIGNAL_COUNT = 64
EXPECTED_DURATION_SECONDS = 240.0
EXPECTED_SAMPLING_RATE_HZ = 1024.0
EXPECTED_LABELS = (
    "Fp1", "AF7", "AF3", "F1", "F3", "F5", "F7", "FT7", "FC5", "FC3", "FC1",
    "C1", "C3", "C5", "T7", "TP7", "CP5", "CP3", "CP1", "P1", "P3", "P5", "P7",
    "P9", "PO7", "PO3", "O1", "Iz", "Oz", "POz", "Pz", "CPz", "Fpz", "Fp2", "AF8",
    "AF4", "AFz", "Fz", "F2", "F4", "F6", "F8", "FT8", "FC6", "FC4", "FC2", "FCz",
    "Cz", "C2", "C4", "C6", "T8", "TP8", "CP6", "CP4", "CP2", "P2", "P4", "P6", "P8",
    "P10", "PO8", "PO4", "O2",
)


def md5_file(path: Path) -> str:
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path) -> dict[str, object]:
    actual_size = path.stat().st_size
    actual_md5 = md5_file(path)
    header = read_edf_header(path)

    labels = tuple(signal.label for signal in header.signals)
    sampling_rates = tuple(signal.sampling_rate_hz for signal in header.signals)
    unique_sampling_rates = sorted({round(value, 9) for value in sampling_rates})

    checks = {
        "size_bytes": actual_size == EXPECTED_SIZE_BYTES,
        "annex_md5": actual_md5 == EXPECTED_MD5,
        "signal_count": header.signal_count == EXPECTED_SIGNAL_COUNT,
        "recording_duration_seconds": header.recording_duration_seconds == EXPECTED_DURATION_SECONDS,
        "sampling_rate_hz": unique_sampling_rates == [EXPECTED_SAMPLING_RATE_HZ],
        "channel_labels": labels == EXPECTED_LABELS,
        "edf_internal_size_consistency": header.expected_file_size_bytes == actual_size,
    }

    result = {
        "dataset": "ds003775",
        "source_release": "OpenNeuro v1.2.1 / NEMAR on003775 v1.0.0",
        "pilot_recording": "sub-001/ses-t1/task-resteyesc",
        "path": str(path),
        "actual_size_bytes": actual_size,
        "actual_md5": actual_md5,
        "header": {
            "version": header.version,
            "patient_id": header.patient_id,
            "recording_id": header.recording_id,
            "signal_count": header.signal_count,
            "recording_duration_seconds": header.recording_duration_seconds,
            "unique_sampling_rates_hz": unique_sampling_rates,
            "channel_labels": labels,
            "expected_file_size_bytes_from_header": header.expected_file_size_bytes,
        },
        "checks": checks,
        "passed": all(checks.values()),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("edf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = verify(args.edf)
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
