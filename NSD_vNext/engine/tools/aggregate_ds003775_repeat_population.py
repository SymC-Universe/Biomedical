#!/usr/bin/env python3
"""Aggregate label-blind ds003775 repeat-pair T0 outputs subject-wise.

This deliberately reports population distributions and Limit-Map prevalence.
It does not fit a clinical model, define a healthy boundary, or tune the frozen
descriptive parameterizer.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import median


def _finite(values):
    return [float(v) for v in values if v is not None and math.isfinite(float(v))]


def _summary(values):
    vals = sorted(_finite(values))
    if not vals:
        return {"n": 0, "median": None, "minimum": None, "maximum": None}
    return {
        "n": len(vals),
        "median": median(vals),
        "minimum": vals[0],
        "maximum": vals[-1],
    }


def _load_many(root: Path, suffix: str):
    out = []
    for path in sorted(root.rglob(f"*{suffix}")):
        data = json.loads(path.read_text(encoding="utf-8"))
        out.append((path, data))
    return out


def aggregate(root: Path, expected_subject_count: int) -> dict[str, object]:
    spec_reports = _load_many(root, "_specparam.json")
    psd_reports = _load_many(root, "_psd.json")
    d4_reports = _load_many(root, "_d4.json")

    spec_by_subject = {str(d["subject_id"]): d for _, d in spec_reports}
    psd_by_subject = {str(d["subject_id"]): d for _, d in psd_reports}
    d4_subjects = {
        str(d.get("subject_id") or d.get("manifest_subject_id") or "")
        for _, d in d4_reports
    }
    d4_subjects.discard("")

    common = sorted(set(spec_by_subject) & set(psd_by_subject))
    if len(common) != expected_subject_count:
        raise ValueError(
            f"expected {expected_subject_count} complete specparam+PSD subjects, found {len(common)}"
        )

    exponent_median_diff = []
    same_peak_fraction = []
    same_zero_fraction = []
    peak_center_median_diff = []
    psd_global_corr = []
    psd_channel_median_corr = []
    psd_channel_min_corr = []

    disagreement_fractions = []
    max_peak_saturation_fractions = []
    zero_peak_fractions = []
    width_boundary_hits_per_channel = []

    subjects = []
    for subject in common:
        spec = spec_by_subject[subject]
        psd = psd_by_subject[subject]
        repeat = spec["repeat_summary"]

        exponent_median_diff.append(
            repeat["aperiodic_exponent_absolute_difference"]["median"]
        )
        same_peak_fraction.append(repeat["same_peak_count_fraction"])
        same_zero_fraction.append(repeat["same_zero_peak_state_fraction"])
        peak_center_median_diff.append(
            repeat["first_listed_peak_nearest_center_difference_hz"]["median"]
        )

        pc = psd["repeat_comparison"]
        psd_global_corr.append(pc["global_median_psd_correlation"])
        psd_channel_median_corr.append(pc["channel_correlation_median"])
        psd_channel_min_corr.append(pc["channel_correlation_minimum"])

        session_rows = []
        for session in spec["sessions"]:
            summary = session["summary"]
            channel_count = int(summary["channel_count"])
            disagreement_fractions.append(
                float(summary["aperiodic_model_disagreement_channel_fraction"])
            )
            max_peak_saturation_fractions.append(
                int(summary["fixed_max_peak_count_channel_count"]) / channel_count
            )
            zero_peak_fractions.append(
                float(summary["fixed_zero_peak_channel_fraction"])
            )
            width_boundary_hits_per_channel.append(
                int(summary["fixed_total_width_boundary_hits"]) / channel_count
            )
            session_rows.append({
                "session_id": session["session_id"],
                "aperiodic_model_disagreement_fraction":
                    summary["aperiodic_model_disagreement_channel_fraction"],
                "max_peak_count_channel_fraction":
                    int(summary["fixed_max_peak_count_channel_count"]) / channel_count,
                "zero_peak_channel_fraction":
                    summary["fixed_zero_peak_channel_fraction"],
                "width_boundary_hits_per_channel":
                    int(summary["fixed_total_width_boundary_hits"]) / channel_count,
            })

        subjects.append({
            "subject_id": subject,
            "exponent_absolute_difference_median":
                repeat["aperiodic_exponent_absolute_difference"]["median"],
            "same_peak_count_fraction": repeat["same_peak_count_fraction"],
            "same_zero_peak_state_fraction": repeat["same_zero_peak_state_fraction"],
            "first_peak_nearest_center_difference_median_hz":
                repeat["first_listed_peak_nearest_center_difference_hz"]["median"],
            "global_median_log_psd_correlation": pc["global_median_psd_correlation"],
            "median_channel_log_psd_correlation": pc["channel_correlation_median"],
            "minimum_channel_log_psd_correlation": pc["channel_correlation_minimum"],
            "sessions": session_rows,
        })

    return {
        "dataset": "ds003775",
        "scope": "T0 label-blind 42-repeat-subject descriptive population Limit Map",
        "subject_count": len(common),
        "d4_report_count": len(d4_reports),
        "d4_subject_count_recoverable_from_reports": len(d4_subjects),
        "population": {
            "aperiodic_exponent_absolute_difference_subject_median": _summary(exponent_median_diff),
            "same_peak_count_fraction_per_subject": _summary(same_peak_fraction),
            "same_zero_peak_state_fraction_per_subject": _summary(same_zero_fraction),
            "first_peak_nearest_center_difference_subject_median_hz": _summary(peak_center_median_diff),
            "global_median_log_psd_correlation": _summary(psd_global_corr),
            "median_channel_log_psd_correlation": _summary(psd_channel_median_corr),
            "minimum_channel_log_psd_correlation": _summary(psd_channel_min_corr),
            "aperiodic_model_disagreement_fraction_per_session": _summary(disagreement_fractions),
            "max_peak_count_channel_fraction_per_session": _summary(max_peak_saturation_fractions),
            "zero_peak_channel_fraction_per_session": _summary(zero_peak_fractions),
            "width_boundary_hits_per_channel_per_session": _summary(width_boundary_hits_per_channel),
        },
        "subjects": subjects,
        "interpretation_ceiling": (
            "descriptive repeat population map only; no trait biomarker, damping, chi, "
            "diagnostic, prognostic, or healthy-boundary claim"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact_root", type=Path)
    parser.add_argument("--expected-subject-count", type=int, default=42)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = aggregate(args.artifact_root, args.expected_subject_count)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "subject_count": result["subject_count"],
        "population": result["population"],
        "interpretation_ceiling": result["interpretation_ceiling"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
