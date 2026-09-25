#!/usr/bin/env python3
"""Execute the prospectively frozen ds004148 descriptive transfer pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import urllib.request
from itertools import combinations
from pathlib import Path

import numpy as np

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.psd import WelchConfig, estimate_welch_psd
from nsd_engine.specparam_adapter import SpecparamSettings, fit_specparam_descriptive
from nsd_engine.spectral_parameterization_qc import compare_aperiodic_models, diagnose_parameterization

WELCH = WelchConfig(window_seconds=4.0, overlap_fraction=0.5, window="hann", detrend="constant", scaling="density")
FROZEN_FIXED = SpecparamSettings(
    aperiodic_mode="fixed", periodic_mode="gaussian", peak_width_limits=(0.5, 12.0),
    max_n_peaks=3, min_peak_height=0.20, peak_threshold=3.0, fmin_hz=5.0, fmax_hz=35.0,
)
SENSITIVITY_KNEE = SpecparamSettings(
    aperiodic_mode="knee", periodic_mode="gaussian", peak_width_limits=(0.5, 12.0),
    max_n_peaks=3, min_peak_height=0.20, peak_threshold=3.0, fmin_hz=5.0, fmax_hz=35.0,
)

PAIR_METRIC_TO_REFERENCE = {
    "global_median_log_psd_correlation": "global_median_log_psd_correlation",
    "median_channel_log_psd_correlation": "median_channel_log_psd_correlation",
    "aperiodic_exponent_absolute_difference_median": "aperiodic_exponent_absolute_difference_subject_median",
    "same_peak_count_fraction": "same_peak_count_fraction_per_subject",
    "same_zero_peak_state_fraction": "same_zero_peak_state_fraction_per_subject",
    "first_peak_nearest_center_difference_median_hz": "first_peak_nearest_center_difference_subject_median_hz",
}
RECORDING_METRIC_TO_REFERENCE = {
    "aperiodic_model_disagreement_channel_fraction": "aperiodic_model_disagreement_fraction_per_session",
    "max_peak_count_channel_fraction": "max_peak_count_channel_fraction_per_session",
    "zero_peak_channel_fraction": "zero_peak_channel_fraction_per_session",
    "width_boundary_hits_per_channel": "width_boundary_hits_per_channel_per_session",
}


def _hash(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _download(url: str, path: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "SymC-NSD-transfer/0.1"})
    with urllib.request.urlopen(request, timeout=180) as response, path.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def _parse_vhdr(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")

    def grab(name: str) -> str | None:
        match = re.search(rf"(?mi)^\s*{re.escape(name)}\s*=\s*(.+?)\s*$", text)
        return match.group(1).strip() if match else None

    channels = []
    for match in re.finditer(r"(?mi)^Ch(\d+)=(.*)$", text):
        parts = [part.strip() for part in match.group(2).split(",")]
        channels.append({
            "index": int(match.group(1)),
            "name": parts[0],
            "resolution": float(parts[2]) if len(parts) > 2 and parts[2] else 1.0,
            "unit": parts[3] if len(parts) > 3 else "",
        })

    interval = float(grab("SamplingInterval"))
    return {
        "number_of_channels": int(grab("NumberOfChannels")),
        "sampling_rate_hz": 1_000_000.0 / interval,
        "binary_format": str(grab("BinaryFormat")),
        "data_orientation": str(grab("DataOrientation")),
        "channels": channels,
    }


def _read_brainvision(eeg_path: Path, header: dict[str, object]) -> tuple[list[str], np.ndarray]:
    if str(header["binary_format"]).upper() != "IEEE_FLOAT_32":
        raise ValueError("frozen transfer requires IEEE_FLOAT_32")
    if str(header["data_orientation"]).upper() != "MULTIPLEXED":
        raise ValueError("frozen transfer requires MULTIPLEXED")

    channels = list(header["channels"])
    count = int(header["number_of_channels"])
    if len(channels) != count:
        raise ValueError("channel definition count mismatch")

    labels = [str(channel["name"]) for channel in channels]
    if len(labels) != len(set(labels)):
        raise ValueError("duplicate raw channel labels")

    raw = np.fromfile(eeg_path, dtype="<f4")
    if raw.size % count:
        raise ValueError("raw sample count not divisible by channel count")
    data = raw.reshape(-1, count).T.astype(np.float64, copy=False)
    resolution = np.asarray([float(channel["resolution"]) for channel in channels], dtype=float)
    data = data * resolution[:, None]
    if not np.isfinite(data).all():
        raise ValueError("decoded signal contains non-finite values")
    return labels, data


def _fit_channel(signal: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
    psd = estimate_welch_psd(signal, 500.0, fmin_hz=1.0, fmax_hz=45.0, config=WELCH)
    power = np.asarray(psd.power, dtype=float)
    if np.any(power <= 0):
        raise ValueError("Welch power contains non-positive values")

    fixed = fit_specparam_descriptive(psd.frequencies_hz, psd.power, settings=FROZEN_FIXED)
    knee = fit_specparam_descriptive(psd.frequencies_hz, psd.power, settings=SENSITIVITY_KNEE)
    diagnostics = diagnose_parameterization(fixed)
    comparison = compare_aperiodic_models(fixed, knee, center_tolerance_hz=1.0)

    names = list(fixed.aperiodic_parameter_names)
    exponent = float(fixed.aperiodic_parameters[names.index("exponent")])
    return np.log10(power), {
        "aperiodic_exponent": exponent,
        "peak_count": len(fixed.peaks),
        "zero_peak_state": bool(fixed.zero_peak_state),
        "peaks": [{"center_frequency_hz": float(peak.center_frequency_hz)} for peak in fixed.peaks],
        "model_family_disagreement": bool(comparison.flags),
        "width_boundary_hit_count": int(
            diagnostics.lower_width_limit_hit_count + diagnostics.upper_width_limit_hit_count
        ),
        "max_peak_count_reached": bool(diagnostics.max_peak_count_reached),
        "warning_flags": [flag.value for flag in diagnostics.flags],
    }


def _recording(recording: dict[str, object], manifest: dict[str, object], root: Path) -> dict[str, object]:
    base_name = str(recording["base"]).split("/")[-1]
    local: dict[str, Path] = {}
    identities = {}

    for ext, spec in dict(recording["files"]).items():
        path = root / f"{recording['session']}__{base_name}.{ext}"
        url = f"https://data.nemar.org/{manifest['source_release']['nemar_mirror']}/{recording['base']}.{ext}"
        _download(url, path)
        observed_md5 = _hash(path, "md5")
        identities[ext] = {
            "url": url,
            "size_bytes": path.stat().st_size,
            "md5": observed_md5,
            "sha256": _hash(path, "sha256"),
            "size_match": path.stat().st_size == int(spec["size_bytes"]),
            "md5_match": observed_md5 == str(spec["md5"]),
        }
        local[ext] = path

    if not all(item["size_match"] and item["md5_match"] for item in identities.values()):
        raise ValueError("frozen source identity mismatch")

    header = _parse_vhdr(local["vhdr"])
    if int(header["number_of_channels"]) != 61:
        raise ValueError("raw channel count mismatch")
    if float(header["sampling_rate_hz"]) != 500.0:
        raise ValueError("sampling rate mismatch")

    labels, data = _read_brainvision(local["eeg"], header)
    if data.shape != (61, 150000):
        raise ValueError(f"unexpected decoded shape {data.shape}")

    channels = []
    log_psd = []
    for label, signal in zip(labels, data):
        log_power, fitted = _fit_channel(signal)
        log_psd.append(log_power)
        channels.append({"channel": label, **fitted})

    disagreement = sum(bool(item["model_family_disagreement"]) for item in channels)
    zero_peak = sum(bool(item["zero_peak_state"]) for item in channels)
    max_peak = sum(bool(item["max_peak_count_reached"]) for item in channels)
    width_hits = sum(int(item["width_boundary_hit_count"]) for item in channels)

    return {
        "session": recording["session"],
        "task": recording["task"],
        "source_identity": identities,
        "channel_labels": labels,
        "channels": channels,
        "log_psd": np.asarray(log_psd, dtype=float),
        "summary": {
            "aperiodic_model_disagreement_channel_fraction": disagreement / len(channels),
            "zero_peak_channel_fraction": zero_peak / len(channels),
            "max_peak_count_channel_fraction": max_peak / len(channels),
            "width_boundary_hits_per_channel": width_hits / len(channels),
        },
    }


def _pearson(first: np.ndarray, second: np.ndarray) -> float:
    if first.size != second.size:
        raise ValueError("PSD vector size mismatch")
    if np.std(first) == 0 or np.std(second) == 0:
        return float("nan")
    return float(np.corrcoef(first, second)[0, 1])


def _pair(first: dict[str, object], second: dict[str, object]) -> dict[str, object]:
    first_channels = {str(item["channel"]): item for item in first["channels"]}
    second_channels = {str(item["channel"]): item for item in second["channels"]}
    shared = sorted(set(first_channels) & set(second_channels))
    if not shared:
        raise ValueError("no shared channels")

    first_index = {label: i for i, label in enumerate(first["channel_labels"])}
    second_index = {label: i for i, label in enumerate(second["channel_labels"])}
    correlations = []
    exponent_differences = []
    peak_count_equal = 0
    zero_peak_equal = 0
    peak_center_differences = []

    for label in shared:
        corr = _pearson(first["log_psd"][first_index[label]], second["log_psd"][second_index[label]])
        if math.isfinite(corr):
            correlations.append(corr)

        a = first_channels[label]
        b = second_channels[label]
        exponent_differences.append(abs(float(a["aperiodic_exponent"]) - float(b["aperiodic_exponent"])))
        peak_count_equal += int(int(a["peak_count"]) == int(b["peak_count"]))
        zero_peak_equal += int(bool(a["zero_peak_state"]) == bool(b["zero_peak_state"]))

        if a["peaks"] and b["peaks"]:
            center = float(a["peaks"][0]["center_frequency_hz"])
            peak_center_differences.append(
                min(abs(center - float(peak["center_frequency_hz"])) for peak in b["peaks"])
            )

    if not correlations:
        raise ValueError("no finite PSD correlations")

    global_first = np.median(first["log_psd"], axis=0)
    global_second = np.median(second["log_psd"], axis=0)

    return {
        "task": first["task"],
        "session_a": first["session"],
        "session_b": second["session"],
        "shared_channel_count": len(shared),
        "global_median_log_psd_correlation": _pearson(global_first, global_second),
        "median_channel_log_psd_correlation": float(np.median(correlations)),
        "aperiodic_exponent_absolute_difference_median": float(np.median(exponent_differences)),
        "same_peak_count_fraction": peak_count_equal / len(shared),
        "same_zero_peak_state_fraction": zero_peak_equal / len(shared),
        "first_peak_nearest_center_difference_median_hz": (
            float(np.median(peak_center_differences)) if peak_center_differences else None
        ),
    }


def _summary(values: list[float | None]) -> dict[str, float | int | None]:
    clean = [float(value) for value in values if value is not None and math.isfinite(float(value))]
    if not clean:
        return {"n": 0, "minimum": None, "median": None, "maximum": None}
    array = np.asarray(clean, dtype=float)
    return {
        "n": int(array.size),
        "minimum": float(np.min(array)),
        "median": float(np.median(array)),
        "maximum": float(np.max(array)),
    }


def _label(value: float | None, reference: dict[str, object]) -> str:
    if value is None or not math.isfinite(float(value)):
        return "REFUSED_OR_NOT_AVAILABLE"
    low = float(reference["minimum"])
    high = float(reference["maximum"])
    return "WITHIN_PREVIOUS_ENVELOPE" if low <= float(value) <= high else "OUTSIDE_PREVIOUS_ENVELOPE"


def execute(manifest_path: Path, atlas_path: Path, output_dir: Path) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    atlas = json.loads(atlas_path.read_text(encoding="utf-8"))

    output_dir.mkdir(parents=True, exist_ok=True)
    payload_dir = output_dir / "payloads"
    payload_dir.mkdir(exist_ok=True)

    recordings = [_recording(item, manifest, payload_dir) for item in manifest["recordings"]]
    grouped: dict[str, list[dict[str, object]]] = {}
    for recording in recordings:
        grouped.setdefault(str(recording["task"]), []).append(recording)

    states = {}
    population = atlas["population"]
    for task, items in sorted(grouped.items()):
        items = sorted(items, key=lambda item: str(item["session"]))
        pairs = [_pair(first, second) for first, second in combinations(items, 2)]

        pair_summaries = {}
        reference_comparison = {}
        for metric, reference_key in PAIR_METRIC_TO_REFERENCE.items():
            summary = _summary([pair.get(metric) for pair in pairs])
            pair_summaries[metric] = summary
            reference = population[reference_key]
            reference_comparison[metric] = {
                "state_median": summary["median"],
                "ds003775_reference": reference,
                "label": _label(summary["median"], reference),
            }

        recording_summaries = {}
        for metric, reference_key in RECORDING_METRIC_TO_REFERENCE.items():
            summary = _summary([float(item["summary"][metric]) for item in items])
            recording_summaries[metric] = summary
            reference = population[reference_key]
            reference_comparison[metric] = {
                "state_median": summary["median"],
                "ds003775_reference": reference,
                "label": _label(summary["median"], reference),
            }

        states[task] = {
            "recording_count": len(items),
            "pair_count": len(pairs),
            "pairwise": pairs,
            "pair_metric_summaries": pair_summaries,
            "recording_metric_summaries": recording_summaries,
            "reference_comparison": reference_comparison,
        }

    reference_channels = {str(item["channel"]) for item in atlas["channel_repeatability"]}
    target_channels = set(recordings[0]["channel_labels"])
    exact_intersection = sorted(reference_channels & target_channels)

    return {
        "schema": "NSD_DS004148_DESCRIPTIVE_TRANSFER_RESULT_V0_1",
        "status": "P0_Q_INDEPENDENT_LABEL_BLIND_DESCRIPTIVE_TRANSFER",
        "dataset": "ds004148",
        "subject": manifest["subject"],
        "source_release": manifest["source_release"],
        "source_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "reference_atlas": {
            "atlas_data_id": atlas["atlas_data_id"],
            "source_workflow_run": atlas["source_workflow_run"],
            "source_artifact_digest": atlas["source_artifact_digest"],
            "file_sha256": hashlib.sha256(atlas_path.read_bytes()).hexdigest(),
        },
        "frozen_representation": {
            "welch": WELCH.__dict__,
            "specparam_fixed": FROZEN_FIXED.__dict__,
            "specparam_knee_sensitivity": SENSITIVITY_KNEE.__dict__,
        },
        "recording_count": len(recordings),
        "channel_semantics": {
            "ds004148_raw_channel_count": len(target_channels),
            "ds003775_reference_channel_count": len(reference_channels),
            "exact_label_intersection_count": len(exact_intersection),
            "exact_label_intersection": exact_intersection,
            "no_synthetic_channel_mapping": True,
        },
        "recordings": [
            {
                "session": item["session"],
                "task": item["task"],
                "channel_count": len(item["channel_labels"]),
                "summary": item["summary"],
                "source_identity": item["source_identity"],
            }
            for item in recordings
        ],
        "states": states,
        "interpretation_firewall": [
            "descriptive transfer labels are not tuned pass/fail thresholds",
            "outside previous envelope is a Limit Map observation, not automatic failure",
            "one subject does not support population generalization",
            "channels are repeated measurements, not independent participants",
            "descriptive bandwidth does not license damping",
            "descriptive peak center does not license natural frequency",
            "no local chi is licensed",
            "no capital Chi empirical neural-architecture claim is licensed",
            "no whole-system scalar is computed",
            "repeat-session similarity is not recovery or resilience",
            "no clinical label entered feature construction or interpretation",
        ],
        "licenses_modal_damping": False,
        "licenses_local_chi": False,
        "licenses_capital_chi": False,
        "licenses_diagnosis": False,
        "licenses_population_inference": False,
    }


def _write_summary(result: dict[str, object], path: Path) -> None:
    lines = [
        "# ds004148 descriptive transfer verification summary",
        "",
        f"Status: {result['status']}",
        f"Recordings: {result['recording_count']}",
        f"Exact channel-label intersection with ds003775 reference: {result['channel_semantics']['exact_label_intersection_count']}",
        "",
    ]
    for task, state in result["states"].items():
        lines.append(f"## {task}")
        for metric, comparison in state["reference_comparison"].items():
            reference = comparison["ds003775_reference"]
            lines.append(
                f"- {metric}: median={comparison['state_median']}; "
                f"label={comparison['label']}; reference_min={reference['minimum']}; "
                f"reference_max={reference['maximum']}"
            )
        lines.append("")
    lines.append(
        "No modal damping, local chi, capital Chi, whole-system scalar, diagnosis, "
        "recovery, or population inference is licensed by this pilot."
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--atlas", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    result = execute(args.manifest, args.atlas, args.output_dir)
    result_path = args.output_dir / "ds004148_descriptive_transfer_result_v0.1.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_summary(result, args.output_dir / "VERIFY_SUMMARY.md")
    print(json.dumps({
        "status": result["status"],
        "recording_count": result["recording_count"],
        "states": {
            task: {
                metric: comparison["label"]
                for metric, comparison in state["reference_comparison"].items()
            }
            for task, state in result["states"].items()
        },
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
