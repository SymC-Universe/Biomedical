#!/usr/bin/env python3
"""Rebuild the 59-label ds003775 reference envelope from frozen subject artifacts.

Input directory must contain the extracted ds003775 repeat subject artifacts
from GitHub Actions run 35337659470. This is a deterministic mechanical
derivation of the exact-label rule frozen before ds004148 outcome inspection.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path

MATCHED_LABELS = (
    "AF3","AF4","AF7","AF8","C1","C2","C3","C4","C5","C6",
    "CP1","CP2","CP3","CP4","CP5","CP6","CPz","Cz",
    "F1","F2","F3","F4","F5","F6","F7","F8",
    "FC1","FC2","FC3","FC4","FC5","FC6","FT7","FT8",
    "Fp1","Fp2","Fpz","Fz","O1","O2","Oz",
    "P1","P2","P3","P4","P5","P6","P7","P8",
    "PO3","PO4","PO7","PO8","POz","Pz","T7","T8","TP7","TP8",
)


def summary(values):
    clean = [float(value) for value in values if value is not None and math.isfinite(float(value))]
    if not clean:
        return {"n": 0, "minimum": None, "median": None, "maximum": None}
    return {
        "n": len(clean),
        "minimum": min(clean),
        "median": statistics.median(clean),
        "maximum": max(clean),
    }


def build(root: Path) -> dict[str, object]:
    subjects = sorted(path for path in root.iterdir() if path.is_dir() and path.name.startswith("ds003775-repeat-sub-"))
    if len(subjects) != 42:
        raise ValueError(f"expected 42 subject artifact directories, found {len(subjects)}")

    pair = {
        "median_channel_log_psd_correlation": [],
        "aperiodic_exponent_absolute_difference_median": [],
        "same_peak_count_fraction": [],
        "same_zero_peak_state_fraction": [],
        "first_peak_nearest_center_difference_median_hz": [],
    }
    recording = {
        "aperiodic_model_disagreement_channel_fraction": [],
        "max_peak_count_channel_fraction": [],
        "zero_peak_channel_fraction": [],
        "width_boundary_hits_per_channel": [],
    }
    subject_ids = []

    for directory in subjects:
        psd_path = next(directory.glob("*_psd.json"))
        spec_path = next(directory.glob("*_specparam.json"))
        psd = json.loads(psd_path.read_text(encoding="utf-8"))
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        subject_id = str(spec["subject_id"])
        subject_ids.append(subject_id)

        correlations = {
            str(item["channel"]): float(item["log_psd_correlation"])
            for item in psd["repeat_comparison"]["channel_correlations"]
        }
        matched_correlations = [correlations[label] for label in MATCHED_LABELS]
        pair["median_channel_log_psd_correlation"].append(statistics.median(matched_correlations))

        sessions = {
            str(session["session_id"]): {str(channel["channel"]): channel for channel in session["channels"]}
            for session in spec["sessions"]
        }
        if len(sessions) != 2:
            raise ValueError(f"{subject_id}: expected exactly two repeat sessions")
        first, second = list(sessions.values())

        exponent_differences = []
        same_peak_count = 0
        same_zero_peak = 0
        peak_center_differences = []

        for label in MATCHED_LABELS:
            a = first[label]["frozen_fixed"]
            b = second[label]["frozen_fixed"]
            ai = list(a["aperiodic_parameter_names"]).index("exponent")
            bi = list(b["aperiodic_parameter_names"]).index("exponent")
            exponent_differences.append(
                abs(float(a["aperiodic_parameters"][ai]) - float(b["aperiodic_parameters"][bi]))
            )
            same_peak_count += int(int(a["peak_count"]) == int(b["peak_count"]))
            same_zero_peak += int(bool(a["zero_peak_state"]) == bool(b["zero_peak_state"]))

            if a["peaks"] and b["peaks"]:
                center = float(a["peaks"][0]["center_frequency_hz"])
                peak_center_differences.append(
                    min(abs(center - float(item["center_frequency_hz"])) for item in b["peaks"])
                )

        pair["aperiodic_exponent_absolute_difference_median"].append(statistics.median(exponent_differences))
        pair["same_peak_count_fraction"].append(same_peak_count / len(MATCHED_LABELS))
        pair["same_zero_peak_state_fraction"].append(same_zero_peak / len(MATCHED_LABELS))
        pair["first_peak_nearest_center_difference_median_hz"].append(
            statistics.median(peak_center_differences) if peak_center_differences else None
        )

        for session in spec["sessions"]:
            channels = {str(item["channel"]): item for item in session["channels"]}
            selected = [channels[label] for label in MATCHED_LABELS]
            count = len(selected)
            recording["aperiodic_model_disagreement_channel_fraction"].append(
                sum(bool(item["model_family_comparison"]["flags"]) for item in selected) / count
            )
            recording["max_peak_count_channel_fraction"].append(
                sum(bool(item["frozen_fixed"]["max_peak_count_reached"]) for item in selected) / count
            )
            recording["zero_peak_channel_fraction"].append(
                sum(bool(item["frozen_fixed"]["zero_peak_state"]) for item in selected) / count
            )
            recording["width_boundary_hits_per_channel"].append(
                sum(int(item["frozen_fixed"]["width_boundary_hit_count"]) for item in selected) / count
            )

    return {
        "schema": "NSD_DS003775_MATCHED_59_REFERENCE_V0_1",
        "status": "POST_RESULT_MECHANICAL_REMEDIATION_OF_PREDECLARED_EXACT_LABEL_RULE",
        "source_workflow_run": 35337659470,
        "source_population_artifact_digest": "sha256:0859c127ca1cac7f2789fb12b7e66b1453f9ec6fb250e20f11eed6e84b9e0bb2",
        "derivation_note": (
            "Derived after the first ds004148 suite exposed an implementation mismatch. "
            "The exact-label-intersection rule itself was frozen before target outcome inspection. "
            "No target-derived threshold or parameter was selected."
        ),
        "channels": list(MATCHED_LABELS),
        "channel_count": len(MATCHED_LABELS),
        "subject_count": len(subject_ids),
        "session_count": 2 * len(subject_ids),
        "pair_metrics": {name: summary(values) for name, values in pair.items()},
        "recording_metrics": {name: summary(values) for name, values in recording.items()},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = build(args.artifact_root)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
