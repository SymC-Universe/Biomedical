#!/usr/bin/env python3
"""Map Welch-window nuisance sensitivity on a pinned healthy repeat pair.

This is a T0 Limit-Map probe, not a search for the configuration that makes
repeatability look best. The configurations are prespecified at 2, 4, and 8 s
with the same Hann window, 50% overlap, constant detrending, density scaling,
and 1-45 Hz analysis range.

Outputs remain descriptive. No peak fitting, damping, chi, diagnosis, or
reliability claim is licensed by this script.
"""

from __future__ import annotations

import argparse
from itertools import combinations
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


WINDOW_SECONDS = (2.0, 4.0, 8.0)
FMIN_HZ = 1.0
FMAX_HZ = 45.0


def _log_correlation(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        raise ValueError("vectors must have the same shape")
    tiny = np.finfo(float).tiny
    la = np.log10(np.maximum(a, tiny))
    lb = np.log10(np.maximum(b, tiny))
    if np.std(la) == 0 or np.std(lb) == 0:
        return float("nan")
    return float(np.corrcoef(la, lb)[0, 1])


def _summary(values: list[float]) -> dict[str, float | None]:
    finite = np.asarray([value for value in values if math.isfinite(value)], dtype=float)
    if finite.size == 0:
        return {"n": 0, "median": None, "minimum": None, "maximum": None}
    return {
        "n": int(finite.size),
        "median": float(np.median(finite)),
        "minimum": float(np.min(finite)),
        "maximum": float(np.max(finite)),
    }


def _common_bin_indices(frequencies: np.ndarray, common_frequencies: np.ndarray) -> np.ndarray:
    """Return exact indices for frequencies known to share a rational grid."""
    indices: list[int] = []
    for target in common_frequencies:
        hits = np.flatnonzero(np.isclose(frequencies, target, rtol=0.0, atol=1e-10))
        if hits.size != 1:
            raise ValueError(f"expected one exact common PSD bin for {target} Hz, found {hits.size}")
        indices.append(int(hits[0]))
    return np.asarray(indices, dtype=int)


def _session_spectra(path: Path, labels: list[str], duration_seconds: float) -> dict[float, dict[str, object]]:
    physical: dict[str, tuple[float, ...]] = {}
    rate: float | None = None
    for label in labels:
        window = read_edf_channel_window(path, label, start_seconds=0.0, duration_seconds=duration_seconds)
        if rate is None:
            rate = window.sampling_rate_hz
        elif not math.isclose(rate, window.sampling_rate_hz):
            raise ValueError("channels do not share one sampling rate")
        physical[label] = window.physical_samples
    assert rate is not None

    outputs: dict[float, dict[str, object]] = {}
    for seconds in WINDOW_SECONDS:
        config = WelchConfig(
            window_seconds=seconds,
            overlap_fraction=0.5,
            window="hann",
            detrend="constant",
            scaling="density",
        )
        matrix: list[np.ndarray] = []
        frequencies: np.ndarray | None = None
        integrated_power: list[float] = []
        metadata: dict[str, object] | None = None
        for label in labels:
            result = estimate_welch_psd(
                physical[label],
                rate,
                fmin_hz=FMIN_HZ,
                fmax_hz=FMAX_HZ,
                config=config,
            )
            this_f = np.asarray(result.frequencies_hz, dtype=float)
            this_p = np.asarray(result.power, dtype=float)
            if frequencies is None:
                frequencies = this_f
                metadata = {
                    "window_seconds": seconds,
                    "frequency_resolution_hz": result.frequency_resolution_hz,
                    "segment_count": result.segment_count,
                    "nperseg": result.nperseg,
                    "noverlap": result.noverlap,
                    "method": result.method_name,
                    "numpy_version": result.numpy_version,
                    "scipy_version": result.scipy_version,
                }
            elif not np.array_equal(frequencies, this_f):
                raise ValueError("channel frequency grids differ within a configuration")
            matrix.append(this_p)
            integrated_power.append(float(this_p.sum() * result.frequency_resolution_hz))

        assert frequencies is not None
        assert metadata is not None
        array = np.vstack(matrix)
        outputs[seconds] = {
            "frequencies": frequencies,
            "matrix": array,
            "median_psd": np.median(array, axis=0),
            "integrated_power_1_45": np.asarray(integrated_power, dtype=float),
            "metadata": metadata,
        }
    return outputs


def probe(manifest_path: Path, payload_root: Path) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    labels = [str(value) for value in manifest["expected_channel_labels"]]
    duration_seconds = float(manifest["expected_duration_seconds"])
    recordings = manifest["recordings"]
    if len(recordings) != 2:
        raise ValueError("sensitivity probe currently requires exactly two repeat recordings")

    session_data: list[dict[float, dict[str, object]]] = []
    session_ids: list[str] = []
    for recording in recordings:
        path = payload_root / Path(str(recording["relative_path"])).name
        session_data.append(_session_spectra(path, labels, duration_seconds))
        session_ids.append(str(recording["session_id"]))

    per_setting: list[dict[str, object]] = []
    for seconds in WINDOW_SECONDS:
        first = session_data[0][seconds]
        second = session_data[1][seconds]
        matrix_a = first["matrix"]
        matrix_b = second["matrix"]
        assert isinstance(matrix_a, np.ndarray) and isinstance(matrix_b, np.ndarray)

        channel_corrs = [
            _log_correlation(matrix_a[index], matrix_b[index])
            for index in range(len(labels))
        ]
        median_a = first["median_psd"]
        median_b = second["median_psd"]
        assert isinstance(median_a, np.ndarray) and isinstance(median_b, np.ndarray)

        per_setting.append(
            {
                **dict(first["metadata"]),
                "repeat_session_global_median_log_psd_correlation": _log_correlation(median_a, median_b),
                "repeat_session_channel_log_psd_correlation": _summary(channel_corrs),
            }
        )

    # All three grids share exact 0.5-Hz bins from 1 to 45 Hz. Compare on that
    # prespecified common grid rather than interpolating finer configurations.
    common_frequencies = np.arange(FMIN_HZ, FMAX_HZ + 0.25, 0.5, dtype=float)
    within_session_pairs: list[dict[str, object]] = []
    for session_index, session_id in enumerate(session_ids):
        spectra = session_data[session_index]
        for left_seconds, right_seconds in combinations(WINDOW_SECONDS, 2):
            left = spectra[left_seconds]
            right = spectra[right_seconds]
            left_f = left["frequencies"]
            right_f = right["frequencies"]
            left_matrix = left["matrix"]
            right_matrix = right["matrix"]
            assert isinstance(left_f, np.ndarray) and isinstance(right_f, np.ndarray)
            assert isinstance(left_matrix, np.ndarray) and isinstance(right_matrix, np.ndarray)
            left_idx = _common_bin_indices(left_f, common_frequencies)
            right_idx = _common_bin_indices(right_f, common_frequencies)
            correlations = [
                _log_correlation(left_matrix[index, left_idx], right_matrix[index, right_idx])
                for index in range(len(labels))
            ]

            left_power = left["integrated_power_1_45"]
            right_power = right["integrated_power_1_45"]
            assert isinstance(left_power, np.ndarray) and isinstance(right_power, np.ndarray)
            denominator = np.maximum((np.abs(left_power) + np.abs(right_power)) / 2.0, np.finfo(float).tiny)
            relative_difference = np.abs(left_power - right_power) / denominator

            within_session_pairs.append(
                {
                    "session_id": session_id,
                    "window_seconds_a": left_seconds,
                    "window_seconds_b": right_seconds,
                    "common_grid_resolution_hz": 0.5,
                    "channel_log_psd_shape_correlation": _summary(correlations),
                    "channel_integrated_power_symmetric_relative_difference": _summary(
                        [float(value) for value in relative_difference]
                    ),
                }
            )

    return {
        "dataset": manifest.get("dataset"),
        "subject_id": manifest.get("subject_id"),
        "task": manifest.get("task"),
        "scope": "prespecified Welch-window nuisance/Limit-Map probe",
        "selection_rule": "none; 2 s, 4 s, and 8 s are reported together and no configuration is chosen by apparent repeatability",
        "shared_settings": {
            "fmin_hz": FMIN_HZ,
            "fmax_hz": FMAX_HZ,
            "window": "hann",
            "overlap_fraction": 0.5,
            "detrend": "constant",
            "scaling": "density",
            "window_seconds": list(WINDOW_SECONDS),
        },
        "repeat_session_by_window": per_setting,
        "within_session_cross_window": within_session_pairs,
        "interpretation_ceiling": "one-subject descriptive nuisance map; not a parameter-selection result, ICC, population reliability estimate, biological trait claim, modal result, damping result, or diagnostic result",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("payload_root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = probe(args.manifest, args.payload_root)
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
