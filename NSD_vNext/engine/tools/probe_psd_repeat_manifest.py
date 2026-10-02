#!/usr/bin/env python3
"""Run a label-blind descriptive Welch-PSD repeat-session pilot.

This T0 tool intentionally stays below modal/dynamical interpretation. It reads
pinned EDF payloads, computes a conventional Welch PSD for every declared EEG
channel, and describes repeat-session similarity. It does not fit peaks, infer
damping, compute chi, classify a subject, or define a healthy range.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.edf_samples import read_edf_channel_window
from nsd_engine.psd import WelchConfig, estimate_welch_psd


BANDS_HZ = {
    "delta_1_4": (1.0, 4.0),
    "theta_4_8": (4.0, 8.0),
    "alpha_8_13": (8.0, 13.0),
    "beta_13_30": (13.0, 30.0),
    "low_gamma_30_45": (30.0, 45.0),
}


def _band_power(frequencies: np.ndarray, power: np.ndarray, low: float, high: float, df: float) -> float:
    # Half-open intervals avoid double-counting boundary bins, except 45 Hz is
    # retained in the final declared band.
    if math.isclose(high, 45.0):
        mask = (frequencies >= low) & (frequencies <= high)
    else:
        mask = (frequencies >= low) & (frequencies < high)
    return float(power[mask].sum() * df)


def _safe_log_correlation(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        raise ValueError("PSD vectors must have equal shape")
    tiny = np.finfo(float).tiny
    la = np.log10(np.maximum(a, tiny))
    lb = np.log10(np.maximum(b, tiny))
    if np.std(la) == 0 or np.std(lb) == 0:
        return float("nan")
    return float(np.corrcoef(la, lb)[0, 1])


def _recording_psd(path: Path, labels: list[str], duration_seconds: float) -> dict[str, object]:
    config = WelchConfig(window_seconds=4.0, overlap_fraction=0.5, window="hann", detrend="constant", scaling="density")
    channel_outputs: list[dict[str, object]] = []
    psd_matrix: list[np.ndarray] = []
    common_frequencies: np.ndarray | None = None
    versions: dict[str, str] | None = None
    df: float | None = None
    segment_count: int | None = None

    for label in labels:
        window = read_edf_channel_window(
            path,
            label,
            start_seconds=0.0,
            duration_seconds=duration_seconds,
        )
        result = estimate_welch_psd(
            window.physical_samples,
            window.sampling_rate_hz,
            fmin_hz=1.0,
            fmax_hz=45.0,
            config=config,
        )
        frequencies = np.asarray(result.frequencies_hz, dtype=float)
        power = np.asarray(result.power, dtype=float)
        if common_frequencies is None:
            common_frequencies = frequencies
            df = result.frequency_resolution_hz
            segment_count = result.segment_count
            versions = {"numpy": result.numpy_version, "scipy": result.scipy_version}
        elif not np.array_equal(common_frequencies, frequencies):
            raise ValueError("channel PSD frequency grids differ unexpectedly")

        dominant_index = int(np.argmax(power))
        bands = {
            name: _band_power(frequencies, power, low, high, result.frequency_resolution_hz)
            for name, (low, high) in BANDS_HZ.items()
        }
        total_1_45 = float(power.sum() * result.frequency_resolution_hz)
        relative_bands = {
            name: (value / total_1_45 if total_1_45 > 0 else None)
            for name, value in bands.items()
        }
        channel_outputs.append(
            {
                "channel": label,
                "dominant_descriptive_bin_hz_1_45": float(frequencies[dominant_index]),
                "integrated_power_1_45": total_1_45,
                "band_power": bands,
                "relative_band_power": relative_bands,
                "licenses_peak": False,
                "licenses_damping": False,
                "licenses_chi": False,
            }
        )
        psd_matrix.append(power)

    assert common_frequencies is not None
    assert df is not None
    assert segment_count is not None
    assert versions is not None
    matrix = np.vstack(psd_matrix)
    median_psd = np.median(matrix, axis=0)

    return {
        "method": "scipy.signal.welch",
        "versions": versions,
        "config": {
            "fmin_hz": 1.0,
            "fmax_hz": 45.0,
            "window_seconds": config.window_seconds,
            "overlap_fraction": config.overlap_fraction,
            "window": config.window,
            "detrend": config.detrend,
            "scaling": config.scaling,
            "frequency_resolution_hz": df,
            "segment_count": segment_count,
        },
        "frequency_bins_hz": [float(value) for value in common_frequencies],
        "median_psd_across_channels": [float(value) for value in median_psd],
        "channels": channel_outputs,
        "_psd_matrix": matrix,
        "_median_psd": median_psd,
    }


def probe_repeat(manifest_path: Path, payload_root: Path) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    labels = [str(value) for value in manifest["expected_channel_labels"]]
    duration_seconds = float(manifest["expected_duration_seconds"])
    recordings = manifest["recordings"]
    if len(recordings) != 2:
        raise ValueError("repeat PSD pilot currently requires exactly two recordings")

    session_results: list[dict[str, object]] = []
    internal_psd: list[np.ndarray] = []
    internal_medians: list[np.ndarray] = []
    for recording in recordings:
        path = payload_root / Path(str(recording["relative_path"])).name
        result = _recording_psd(path, labels, duration_seconds)
        internal_psd.append(result.pop("_psd_matrix"))
        internal_medians.append(result.pop("_median_psd"))
        result["session_id"] = recording["session_id"]
        result["acquisition_time"] = recording.get("acquisition_time")
        session_results.append(result)

    channel_correlations = [
        _safe_log_correlation(internal_psd[0][idx], internal_psd[1][idx])
        for idx in range(len(labels))
    ]
    finite_correlations = [value for value in channel_correlations if math.isfinite(value)]
    if not finite_correlations:
        raise ValueError("no finite repeat-session channel PSD correlations")

    comparison = {
        "metric": "Pearson correlation of log10 Welch PSD across 1-45 Hz bins",
        "global_median_psd_correlation": _safe_log_correlation(internal_medians[0], internal_medians[1]),
        "channel_correlation_median": float(np.median(finite_correlations)),
        "channel_correlation_minimum": float(np.min(finite_correlations)),
        "channel_correlation_maximum": float(np.max(finite_correlations)),
        "channel_correlations": [
            {"channel": label, "log_psd_correlation": value}
            for label, value in zip(labels, channel_correlations)
        ],
        "interpretation_ceiling": "single-subject descriptive repeat pilot; not an ICC, trait estimate, clinical effect, or reliability claim",
    }

    return {
        "dataset": manifest.get("dataset"),
        "source_release": manifest.get("source_release"),
        "subject_id": manifest.get("subject_id"),
        "task": manifest.get("task"),
        "analysis_scope": "T0 label-blind descriptive spectral qualification",
        "dynamical_interpretation": "prohibited at this stage",
        "sessions": session_results,
        "repeat_comparison": comparison,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("payload_root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = probe_repeat(args.manifest, args.payload_root)
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
