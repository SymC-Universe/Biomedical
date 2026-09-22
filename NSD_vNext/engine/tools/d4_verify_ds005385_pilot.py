#!/usr/bin/env python3
"""Verify one pinned ds005385 EDF payload under the source-declared header caveat.

The ds005385 README explicitly warns that EDF physical min/max specifications
may contain invalid values and should be ignored. Therefore this D4 verifier
checks immutable payload identity and structural EDF fields while intentionally
not validating or using physical calibration ranges.

Passing promotes only the named pilot payload to D4 for header/readability
scope. It does not authorize scientific EEG analysis or physical-unit decoding
from unreliable calibration metadata.
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


EXPECTED_SIZE_BYTES = 23_936_896
EXPECTED_SHA256 = "a9ef4f8bcc7b3fff6568b7a441e14230ec287faa23212713e32f37bf8a8710a7"
EXPECTED_SIGNAL_COUNT_TOTAL = 65
EXPECTED_EEG_CHANNEL_COUNT = 64
EXPECTED_AUXILIARY_LABELS = ("Status",)
EXPECTED_DURATION_SECONDS = 184.0
EXPECTED_SAMPLING_RATE_HZ = 1000.0
EXPECTED_LABELS = (
    "Fp1", "Fp2", "F7", "F3", "Fz", "F4", "F8", "FC5", "FC1", "FC2", "FC6",
    "T7", "C3", "Cz", "C4", "T8", "TP9", "CP5", "CP1", "CP2", "CP6", "TP10",
    "P7", "P3", "Pz", "P4", "P8", "PO9", "O1", "Oz", "O2", "PO10", "AF7",
    "AF3", "AF4", "AF8", "F5", "F1", "F2", "F6", "FT9", "FT7", "FC3", "FC4",
    "FT8", "FT10", "C5", "C1", "C2", "C6", "TP7", "CP3", "CPz", "CP4", "TP8",
    "P5", "P1", "P2", "P6", "PO7", "PO3", "POz", "PO4", "PO8",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path) -> dict[str, object]:
    actual_size = path.stat().st_size
    actual_sha256 = sha256_file(path)

    # Source-authorized provenance exception: parse but do not validate physical
    # min/max fields. No sample-to-physical-unit conversion occurs in D4.
    header = read_edf_header(path, validate_physical_range=False)

    labels = tuple(signal.label for signal in header.signals)
    sampling_rates = tuple(signal.sampling_rate_hz for signal in header.signals)
    unique_sampling_rates = sorted({round(value, 9) for value in sampling_rates})

    physical_ranges = [
        {
            "label": signal.label,
            "physical_dimension": signal.physical_dimension,
            "physical_minimum": signal.physical_minimum,
            "physical_maximum": signal.physical_maximum,
        }
        for signal in header.signals
    ]
    inverted_physical_ranges = sum(
        row["physical_maximum"] <= row["physical_minimum"]
        for row in physical_ranges
    )

    checks = {
        "size_bytes": actual_size == EXPECTED_SIZE_BYTES,
        "annex_sha256": actual_sha256 == EXPECTED_SHA256,
        "signal_count_total": header.signal_count == EXPECTED_SIGNAL_COUNT_TOTAL,
        "eeg_channel_count": len(labels[:EXPECTED_EEG_CHANNEL_COUNT]) == EXPECTED_EEG_CHANNEL_COUNT,
        "eeg_channel_labels": labels[:EXPECTED_EEG_CHANNEL_COUNT] == EXPECTED_LABELS,
        "auxiliary_signal_labels": labels[EXPECTED_EEG_CHANNEL_COUNT:] == EXPECTED_AUXILIARY_LABELS,\n        "recording_duration_seconds":
            header.recording_duration_seconds == EXPECTED_DURATION_SECONDS,
        "sampling_rate_hz": unique_sampling_rates == [EXPECTED_SAMPLING_RATE_HZ],
        "edf_internal_size_consistency":
            header.expected_file_size_bytes == actual_size,
    }

    return {
        "schema": "NSD_DS005385_D4_PILOT_REPORT_V0_1",
        "dataset": "ds005385",
        "source_release":
            "OpenNeuro ds005385 v1.0.3 / NEMAR on005385 v1.0.0",
        "pilot_recording":
            "sub-001/ses-1/task-EyesClosed/acq-pre",
        "path": str(path),
        "actual_size_bytes": actual_size,
        "actual_sha256": actual_sha256,
        "physical_range_policy":
            "SOURCE_DECLARED_UNRELIABLE_DO_NOT_VALIDATE_OR_USE_FOR_SCALING",
        "physical_range_diagnostic": {
            "inverted_or_equal_ranges": int(inverted_physical_ranges),
            "values_retained_for_provenance_only": True,
            "used_for_signal_scaling": False,
        },
        "header": {
            "version": header.version,
            "patient_id": header.patient_id,
            "recording_id": header.recording_id,
            "signal_count_total": header.signal_count,
            "eeg_channel_count_expected_from_bids": EXPECTED_EEG_CHANNEL_COUNT,
            "auxiliary_signal_count": max(0, header.signal_count - EXPECTED_EEG_CHANNEL_COUNT),
            "recording_duration_seconds": header.recording_duration_seconds,
            "unique_sampling_rates_hz": unique_sampling_rates,
            "channel_labels": list(labels),
            "expected_file_size_bytes_from_header":
                header.expected_file_size_bytes,
        },
        "checks": checks,
        "passed": all(checks.values()),
        "claim_ceiling": (
            "D4 payload identity/header/readability only; no physical-unit "
            "decoding, EEG feature, modal inference, chi, diagnosis, or outcome."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("edf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = verify(args.edf)
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
