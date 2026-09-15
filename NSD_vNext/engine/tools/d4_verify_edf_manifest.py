#!/usr/bin/env python3
"""Manifest-driven D4 verification for pinned EDF recordings.

The manifest supplies identity expectations established from public release
metadata/annex keys. This tool verifies local downloaded payloads against those
expectations and emits one auditable JSON report. It does not perform signal
analysis or scientific QC beyond file/header identity.
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


def md5_file(path: Path) -> str:
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_recording(
    local_path: Path,
    recording: dict[str, object],
    manifest: dict[str, object],
) -> dict[str, object]:
    header = read_edf_header(local_path)
    actual_size = local_path.stat().st_size
    actual_md5 = md5_file(local_path)
    labels = tuple(signal.label for signal in header.signals)
    rates = sorted({round(signal.sampling_rate_hz, 9) for signal in header.signals})

    expected_labels = tuple(str(value) for value in manifest["expected_channel_labels"])
    expected_rate = float(manifest["expected_sampling_rate_hz"])
    expected_duration = float(manifest["expected_duration_seconds"])
    expected_signal_count = int(manifest["expected_signal_count"])

    checks = {
        "size_bytes": actual_size == int(recording["expected_size_bytes"]),
        "annex_md5": actual_md5 == str(recording["expected_md5"]),
        "signal_count": header.signal_count == expected_signal_count,
        "recording_duration_seconds": header.recording_duration_seconds == expected_duration,
        "sampling_rate_hz": rates == [expected_rate],
        "channel_labels": labels == expected_labels,
        "edf_internal_size_consistency": header.expected_file_size_bytes == actual_size,
    }

    return {
        "session_id": recording["session_id"],
        "acquisition_time": recording.get("acquisition_time"),
        "relative_path": recording["relative_path"],
        "local_path": str(local_path),
        "actual_size_bytes": actual_size,
        "actual_md5": actual_md5,
        "header": {
            "version": header.version,
            "patient_id": header.patient_id,
            "recording_id": header.recording_id,
            "signal_count": header.signal_count,
            "recording_duration_seconds": header.recording_duration_seconds,
            "unique_sampling_rates_hz": rates,
            "channel_labels": labels,
            "expected_file_size_bytes_from_header": header.expected_file_size_bytes,
        },
        "checks": checks,
        "passed": all(checks.values()),
    }


def verify_manifest(manifest_path: Path, payload_root: Path) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    recordings = manifest.get("recordings")
    if not isinstance(recordings, list) or not recordings:
        raise ValueError("manifest must contain a non-empty recordings list")

    results: list[dict[str, object]] = []
    for recording in recordings:
        if not isinstance(recording, dict):
            raise TypeError("every recording manifest item must be an object")
        filename = Path(str(recording["relative_path"])).name
        local_path = payload_root / filename
        if not local_path.is_file():
            raise FileNotFoundError(f"missing downloaded payload: {local_path}")
        results.append(verify_recording(local_path, recording, manifest))

    return {
        "dataset": manifest.get("dataset"),
        "source_release": manifest.get("source_release"),
        "subject_id": manifest.get("subject_id"),
        "task": manifest.get("task"),
        "manifest_path": str(manifest_path),
        "recordings": results,
        "passed": all(bool(item["passed"]) for item in results),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("payload_root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = verify_manifest(args.manifest, args.payload_root)
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
