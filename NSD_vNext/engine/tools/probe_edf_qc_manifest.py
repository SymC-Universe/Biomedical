#!/usr/bin/env python3
"""Run a descriptive, label-blind sample-window integrity probe on EDF manifests.

This is a T0/D4-to-D5 bridge. It verifies that physical samples can be decoded
and summarizes generic integrity metrics. No diagnostic labels, Atlas values,
final scientific QC thresholds, spectral features, or dynamical parameters are
used here.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.edf_samples import read_edf_window
from nsd_engine.qc import evaluate_signal_qc


def probe_manifest(
    manifest_path: Path,
    payload_root: Path,
    *,
    start_seconds: float,
    duration_seconds: float,
) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    labels = [str(value) for value in manifest["expected_channel_labels"]]
    recordings = manifest["recordings"]

    outputs: list[dict[str, object]] = []
    for recording in recordings:
        filename = Path(str(recording["relative_path"])).name
        path = payload_root / filename
        windows = read_edf_window(
            path,
            labels,
            start_seconds=start_seconds,
            duration_seconds=duration_seconds,
        )
        rates = {round(window.sampling_rate_hz, 9) for window in windows}
        if len(rates) != 1:
            raise ValueError("QC probe requires a common sampling rate across requested channels")
        rate = next(iter(rates))
        dimensions = sorted({window.physical_dimension for window in windows})

        channels = {window.label: window.physical_samples for window in windows}
        report = evaluate_signal_qc(channels, rate)
        flat_channels = [item.channel_name for item in report.channels if item.flat]
        max_edge = max(
            (item.edge_fraction or 0.0 for item in report.channels),
            default=0.0,
        )
        finite_ranges = [
            item.amplitude_range
            for item in report.channels
            if item.amplitude_range is not None
        ]

        outputs.append(
            {
                "session_id": recording["session_id"],
                "acquisition_time": recording.get("acquisition_time"),
                "sample_window": {
                    "start_seconds": start_seconds,
                    "requested_duration_seconds": duration_seconds,
                    "actual_duration_seconds": report.signal_qc.duration_seconds,
                    "sampling_rate_hz": rate,
                    "physical_dimensions": dimensions,
                    "channel_count": len(report.channels),
                },
                "descriptive_qc": {
                    "passed_with_no_task_specific_thresholds": report.signal_qc.passed_signal_integrity,
                    "flags": report.signal_qc.flags,
                    "flat_channel_count": len(flat_channels),
                    "flat_channels": flat_channels,
                    "maximum_extreme_occupancy_fraction": max_edge,
                    "minimum_channel_amplitude_range": min(finite_ranges) if finite_ranges else None,
                    "maximum_channel_amplitude_range": max(finite_ranges) if finite_ranges else None,
                    "channels": [
                        {
                            "channel": item.channel_name,
                            "missing_fraction": item.missing_fraction,
                            "minimum": item.minimum,
                            "maximum": item.maximum,
                            "amplitude_range": item.amplitude_range,
                            "flat": item.flat,
                            "edge_fraction": item.edge_fraction,
                        }
                        for item in report.channels
                    ],
                },
            }
        )

    return {
        "dataset": manifest.get("dataset"),
        "subject_id": manifest.get("subject_id"),
        "task": manifest.get("task"),
        "manifest_path": str(manifest_path),
        "probe_scope": "sample decoding and generic descriptive integrity only",
        "recordings": outputs,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("payload_root", type=Path)
    parser.add_argument("--start-seconds", type=float, default=0.0)
    parser.add_argument("--duration-seconds", type=float, default=10.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = probe_manifest(
        args.manifest,
        args.payload_root,
        start_seconds=args.start_seconds,
        duration_seconds=args.duration_seconds,
    )
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
