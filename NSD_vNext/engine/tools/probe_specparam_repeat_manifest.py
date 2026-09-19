#!/usr/bin/env python3
"""Run the frozen descriptive parameterization candidate on one healthy repeat pair.

This script is intentionally downstream of known-truth qualification and upstream
of any clinical labels. It uses the frozen 5-35 Hz fixed-mode candidate and
reports descriptive periodic/aperiodic outputs plus warning diagnostics. A
second knee fit is computed only as a sensitivity diagnostic; it cannot silently
replace or retune the frozen candidate.
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
from nsd_engine.specparam_adapter import SpecparamSettings, fit_specparam_descriptive
from nsd_engine.spectral_parameterization_qc import (
    compare_aperiodic_models,
    diagnose_parameterization,
)


WELCH = WelchConfig(
    window_seconds=4.0,
    overlap_fraction=0.5,
    window="hann",
    detrend="constant",
    scaling="density",
)
FROZEN_FIXED = SpecparamSettings(
    aperiodic_mode="fixed",
    periodic_mode="gaussian",
    peak_width_limits=(0.5, 12.0),
    max_n_peaks=3,
    min_peak_height=0.20,
    peak_threshold=3.0,
    fmin_hz=5.0,
    fmax_hz=35.0,
)
SENSITIVITY_KNEE = SpecparamSettings(
    aperiodic_mode="knee",
    periodic_mode="gaussian",
    peak_width_limits=(0.5, 12.0),
    max_n_peaks=3,
    min_peak_height=0.20,
    peak_threshold=3.0,
    fmin_hz=5.0,
    fmax_hz=35.0,
)


def _param_payload(result) -> dict[str, object]:
    diagnostics = diagnose_parameterization(result)
    return {
        "aperiodic_parameter_names": list(result.aperiodic_parameter_names),
        "aperiodic_parameters": list(result.aperiodic_parameters),
        "peaks": [
            {
                "center_frequency_hz": peak.center_frequency_hz,
                "power_above_aperiodic_log10": peak.power_above_aperiodic_log10,
                "descriptive_bandwidth_hz": peak.bandwidth_hz,
            }
            for peak in result.peaks
        ],
        "peak_count": len(result.peaks),
        "zero_peak_state": result.zero_peak_state,
        "metrics": dict(result.metrics),
        "warning_flags": [flag.value for flag in diagnostics.flags],
        "width_boundary_hit_count": (
            diagnostics.lower_width_limit_hit_count + diagnostics.upper_width_limit_hit_count
        ),
        "max_peak_count_reached": diagnostics.max_peak_count_reached,
        "licenses_damping": False,
        "licenses_natural_frequency": False,
        "licenses_chi": False,
        "licenses_modal_pole": False,
    }


def _session(path: Path, labels: list[str], duration_seconds: float) -> dict[str, object]:
    channels: list[dict[str, object]] = []
    for label in labels:
        window = read_edf_channel_window(
            path,
            label,
            start_seconds=0.0,
            duration_seconds=duration_seconds,
        )
        psd = estimate_welch_psd(
            window.physical_samples,
            window.sampling_rate_hz,
            fmin_hz=1.0,
            fmax_hz=45.0,
            config=WELCH,
        )
        fixed = fit_specparam_descriptive(
            psd.frequencies_hz,
            psd.power,
            settings=FROZEN_FIXED,
        )
        knee = fit_specparam_descriptive(
            psd.frequencies_hz,
            psd.power,
            settings=SENSITIVITY_KNEE,
        )
        comparison = compare_aperiodic_models(fixed, knee, center_tolerance_hz=1.0)
        channels.append(
            {
                "channel": label,
                "frozen_fixed": _param_payload(fixed),
                "knee_sensitivity": _param_payload(knee),
                "model_family_comparison": {
                    "fixed_peak_count": comparison.first_peak_count,
                    "knee_peak_count": comparison.second_peak_count,
                    "matched_peak_count": comparison.matched_peak_count,
                    "unmatched_fixed_peak_count": comparison.unmatched_first_peak_count,
                    "unmatched_knee_peak_count": comparison.unmatched_second_peak_count,
                    "flags": [flag.value for flag in comparison.flags],
                },
            }
        )

    fixed_zero = sum(item["frozen_fixed"]["zero_peak_state"] for item in channels)
    fixed_boundary = sum(item["frozen_fixed"]["width_boundary_hit_count"] for item in channels)
    fixed_max = sum(item["frozen_fixed"]["max_peak_count_reached"] for item in channels)
    disagreement = sum(bool(item["model_family_comparison"]["flags"]) for item in channels)
    fixed_peak_counts = [int(item["frozen_fixed"]["peak_count"]) for item in channels]

    return {
        "summary": {
            "channel_count": len(channels),
            "fixed_zero_peak_channel_count": int(fixed_zero),
            "fixed_zero_peak_channel_fraction": float(fixed_zero / len(channels)),
            "fixed_total_width_boundary_hits": int(fixed_boundary),
            "fixed_max_peak_count_channel_count": int(fixed_max),
            "fixed_mean_peak_count": float(np.mean(fixed_peak_counts)),
            "aperiodic_model_disagreement_channel_count": int(disagreement),
            "aperiodic_model_disagreement_channel_fraction": float(disagreement / len(channels)),
        },
        "channels": channels,
    }


def _fixed_repeat_summary(first: dict[str, object], second: dict[str, object]) -> dict[str, object]:
    first_by_channel = {item["channel"]: item for item in first["channels"]}
    second_by_channel = {item["channel"]: item for item in second["channels"]}
    shared = sorted(set(first_by_channel) & set(second_by_channel))

    exponent_differences: list[float] = []
    peak_count_equal = 0
    zero_peak_state_equal = 0
    first_peak_matches: list[float] = []

    for label in shared:
        a = first_by_channel[label]["frozen_fixed"]
        b = second_by_channel[label]["frozen_fixed"]
        names_a = list(a["aperiodic_parameter_names"])
        names_b = list(b["aperiodic_parameter_names"])
        if names_a == names_b and "exponent" in names_a:
            index = names_a.index("exponent")
            exponent_differences.append(
                abs(float(a["aperiodic_parameters"][index]) - float(b["aperiodic_parameters"][index]))
            )
        if int(a["peak_count"]) == int(b["peak_count"]):
            peak_count_equal += 1
        if bool(a["zero_peak_state"]) == bool(b["zero_peak_state"]):
            zero_peak_state_equal += 1

        peaks_a = list(a["peaks"])
        peaks_b = list(b["peaks"])
        if peaks_a and peaks_b:
            # Descriptive only: nearest-center difference for the strongest
            # available first listed component, not mode tracking.
            cf_a = float(peaks_a[0]["center_frequency_hz"])
            nearest = min(abs(cf_a - float(peak["center_frequency_hz"])) for peak in peaks_b)
            first_peak_matches.append(nearest)

    def summary(values: list[float]) -> dict[str, float | int | None]:
        if not values:
            return {"n": 0, "median": None, "minimum": None, "maximum": None}
        array = np.asarray(values, dtype=float)
        return {
            "n": int(array.size),
            "median": float(np.median(array)),
            "minimum": float(np.min(array)),
            "maximum": float(np.max(array)),
        }

    return {
        "shared_channel_count": len(shared),
        "aperiodic_exponent_absolute_difference": summary(exponent_differences),
        "same_peak_count_fraction": peak_count_equal / len(shared),
        "same_zero_peak_state_fraction": zero_peak_state_equal / len(shared),
        "first_listed_peak_nearest_center_difference_hz": summary(first_peak_matches),
        "interpretation_ceiling": "single-subject descriptive repeat comparison; no ICC, trait, mode tracking, damping, chi, diagnostic, or prognostic claim",
    }


def probe(manifest_path: Path, payload_root: Path) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    labels = [str(value) for value in manifest["expected_channel_labels"]]
    duration = float(manifest["expected_duration_seconds"])
    recordings = manifest["recordings"]
    if len(recordings) != 2:
        raise ValueError("healthy repeat pilot currently requires exactly two recordings")

    outputs: list[dict[str, object]] = []
    for recording in recordings:
        path = payload_root / Path(str(recording["relative_path"])).name
        session = _session(path, labels, duration)
        session["session_id"] = recording["session_id"]
        session["acquisition_time"] = recording.get("acquisition_time")
        outputs.append(session)

    return {
        "dataset": manifest.get("dataset"),
        "subject_id": manifest.get("subject_id"),
        "task": manifest.get("task"),
        "scope": "first label-blind healthy repeat pilot of known-truth-qualified descriptive parameterization candidate",
        "frozen_candidate": {
            "welch": {
                "window_seconds": WELCH.window_seconds,
                "overlap_fraction": WELCH.overlap_fraction,
                "window": WELCH.window,
                "detrend": WELCH.detrend,
                "scaling": WELCH.scaling,
                "source_psd_range_hz": [1.0, 45.0],
            },
            "specparam": FROZEN_FIXED.__dict__,
        },
        "sessions": outputs,
        "repeat_summary": _fixed_repeat_summary(outputs[0], outputs[1]),
        "interpretation_firewall": [
            "descriptive peak center is not automatically omega_0",
            "descriptive bandwidth is not damping",
            "descriptive peak is not an identified dynamical mode",
            "no chi is licensed at this layer",
            "no clinical label was used to construct or select this candidate",
        ],
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
