#!/usr/bin/env python3
"""Build the channel-specific ds003775 parent reference used by the
prospectively frozen ds004148 spatial/state localization follow-up.

Input root must contain the 42 extracted subject artifacts from workflow
run 35337659470. The derivation is deterministic and uses no ds004148 values.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

MATCHED_LABELS = (
    "AF3","AF4","AF7","AF8","C1","C2","C3","C4","C5","C6",
    "CP1","CP2","CP3","CP4","CP5","CP6","CPz","Cz",
    "F1","F2","F3","F4","F5","F6","F7","F8",
    "FC1","FC2","FC3","FC4","FC5","FC6","FT7","FT8",
    "Fp1","Fp2","Fpz","Fz","O1","O2","Oz",
    "P1","P2","P3","P4","P5","P6","P7","P8",
    "PO3","PO4","PO7","PO8","POz","Pz","T7","T8","TP7","TP8",
)

SOURCE_WORKFLOW_RUN = 35337659470
SOURCE_POPULATION_ARTIFACT_DIGEST = (
    "sha256:0859c127ca1cac7f2789fb12b7e66b1453f9ec6fb250e20f11eed6e84b9e0bb2"
)


def _summary(values: list[float]) -> dict[str, float | int | None]:
    clean = [float(v) for v in values if math.isfinite(float(v))]
    if not clean:
        return {
            "n": 0,
            "minimum": None,
            "q05": None,
            "median": None,
            "q95": None,
            "maximum": None,
        }
    arr = np.asarray(clean, dtype=float)
    return {
        "n": int(arr.size),
        "minimum": float(np.min(arr)),
        "q05": float(np.quantile(arr, 0.05, method="linear")),
        "median": float(np.quantile(arr, 0.50, method="linear")),
        "q95": float(np.quantile(arr, 0.95, method="linear")),
        "maximum": float(np.max(arr)),
    }


def _find_subject_dirs(root: Path) -> list[Path]:
    direct = sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("ds003775-repeat-sub-"))
    if direct:
        return direct
    nested = sorted(
        p for p in root.rglob("ds003775-repeat-sub-*")
        if p.is_dir()
    )
    return nested


def build(root: Path) -> dict[str, object]:
    subject_dirs = _find_subject_dirs(root)
    if len(subject_dirs) != 42:
        raise ValueError(f"expected 42 subject artifact directories, found {len(subject_dirs)}")

    per_channel: dict[str, dict[str, list[float]]] = {
        label: {
            "log_psd_correlation": [],
            "aperiodic_exponent_abs_diff": [],
            "first_peak_nearest_center_diff_hz": [],
            "peak_count_match": [],
            "zero_peak_match": [],
            "model_family_disagreement": [],
            "max_peak_count_reached": [],
            "width_boundary_hits": [],
        }
        for label in MATCHED_LABELS
    }
    subject_ids: list[str] = []

    for directory in subject_dirs:
        psd_paths = list(directory.glob("*_psd.json"))
        spec_paths = list(directory.glob("*_specparam.json"))
        if len(psd_paths) != 1 or len(spec_paths) != 1:
            raise ValueError(f"{directory}: expected one PSD and one specparam JSON")

        psd = json.loads(psd_paths[0].read_text(encoding="utf-8"))
        spec = json.loads(spec_paths[0].read_text(encoding="utf-8"))
        subject_id = str(spec["subject_id"])
        subject_ids.append(subject_id)

        correlations = {
            str(item["channel"]): float(item["log_psd_correlation"])
            for item in psd["repeat_comparison"]["channel_correlations"]
        }
        sessions = {
            str(session["session_id"]): {
                str(channel["channel"]): channel for channel in session["channels"]
            }
            for session in spec["sessions"]
        }
        if len(sessions) != 2:
            raise ValueError(f"{subject_id}: expected exactly two repeat sessions")
        first, second = list(sessions.values())

        for label in MATCHED_LABELS:
            if label not in first or label not in second or label not in correlations:
                raise ValueError(f"{subject_id}: missing matched channel {label}")

            a = first[label]["frozen_fixed"]
            b = second[label]["frozen_fixed"]
            ai = list(a["aperiodic_parameter_names"]).index("exponent")
            bi = list(b["aperiodic_parameter_names"]).index("exponent")

            record = per_channel[label]
            record["log_psd_correlation"].append(correlations[label])
            record["aperiodic_exponent_abs_diff"].append(
                abs(float(a["aperiodic_parameters"][ai]) - float(b["aperiodic_parameters"][bi]))
            )
            record["peak_count_match"].append(float(int(a["peak_count"] == b["peak_count"])))
            record["zero_peak_match"].append(
                float(int(bool(a["zero_peak_state"]) == bool(b["zero_peak_state"])))
            )

            if a["peaks"] and b["peaks"]:
                center = float(a["peaks"][0]["center_frequency_hz"])
                displacement = min(
                    abs(center - float(peak["center_frequency_hz"]))
                    for peak in b["peaks"]
                )
                record["first_peak_nearest_center_diff_hz"].append(displacement)

            for session_channel in (first[label], second[label]):
                record["model_family_disagreement"].append(
                    float(int(bool(session_channel["model_family_comparison"]["flags"])))
                )
                frozen = session_channel["frozen_fixed"]
                record["max_peak_count_reached"].append(
                    float(int(bool(frozen["max_peak_count_reached"])))
                )
                record["width_boundary_hits"].append(float(frozen["width_boundary_hit_count"]))

    output = {
        "schema": "NSD_DS003775_CHANNEL_LOCALIZATION_REFERENCE_V0_1",
        "status": "PARENT_DERIVATION_FROM_FROZEN_42_SUBJECT_ARTIFACTS",
        "source_workflow_run": SOURCE_WORKFLOW_RUN,
        "source_population_artifact_digest": SOURCE_POPULATION_ARTIFACT_DIGEST,
        "subject_count": len(subject_ids),
        "matched_channel_count": len(MATCHED_LABELS),
        "matched_channels": list(MATCHED_LABELS),
        "quantile_rule": (
            "linear empirical q05/median/q95; descriptive context only, "
            "not confidence intervals or population inference"
        ),
        "minimum_peak_pair_n_for_channel_threshold": 10,
        "channels": {},
    }

    for label in MATCHED_LABELS:
        record = per_channel[label]
        output["channels"][label] = {
            "log_psd_correlation": _summary(record["log_psd_correlation"]),
            "aperiodic_exponent_abs_diff": _summary(record["aperiodic_exponent_abs_diff"]),
            "first_peak_nearest_center_diff_hz": _summary(
                record["first_peak_nearest_center_diff_hz"]
            ),
            "peak_count_match_fraction": float(np.mean(record["peak_count_match"])),
            "zero_peak_match_fraction": float(np.mean(record["zero_peak_match"])),
            "model_family_disagreement_fraction": float(
                np.mean(record["model_family_disagreement"])
            ),
            "max_peak_count_reached_fraction": float(
                np.mean(record["max_peak_count_reached"])
            ),
            "width_boundary_hits": _summary(record["width_boundary_hits"]),
        }

    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_root", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    result = build(args.artifact_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "subject_count": result["subject_count"],
        "matched_channel_count": result["matched_channel_count"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
