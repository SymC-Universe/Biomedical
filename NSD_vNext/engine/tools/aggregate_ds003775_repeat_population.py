#!/usr/bin/env python3
"""Aggregate label-blind ds003775 repeat-pair T0 outputs subject-wise.

This deliberately reports population distributions, channel-wise repeatability,
and Limit-Map prevalence. It does not fit a clinical model, define a healthy
boundary, or tune the frozen descriptive parameterizer.
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


def _icc_a1(pairs):
    """Two-way mixed, absolute-agreement, single-measure ICC: ICC(A,1).

    Each pair is one subject measured in the two repeat sessions. This is the
    McGraw-Wong/Shrout-Fleiss absolute-agreement single-measure form:

        (MSR - MSE) /
        (MSR + (k-1)MSE + k(MSC-MSE)/n)

    with k=2 sessions. Negative ICC values are retained rather than clipped.
    """
    rows = []
    for pair in pairs:
        if len(pair) != 2:
            raise ValueError("ICC(A,1) requires exactly two measurements per subject")
        values = [float(pair[0]), float(pair[1])]
        if all(math.isfinite(v) for v in values):
            rows.append(values)
    n = len(rows)
    k = 2
    if n < 2:
        return None

    grand = sum(sum(row) for row in rows) / (n * k)
    row_means = [sum(row) / k for row in rows]
    col_means = [sum(row[j] for row in rows) / n for j in range(k)]

    ss_rows = k * sum((value - grand) ** 2 for value in row_means)
    ss_cols = n * sum((value - grand) ** 2 for value in col_means)
    ss_total = sum((value - grand) ** 2 for row in rows for value in row)
    ss_error = ss_total - ss_rows - ss_cols
    if ss_error < 0 and abs(ss_error) < 1e-12:
        ss_error = 0.0
    if ss_error < 0:
        raise ValueError("negative residual sum of squares in ICC calculation")

    ms_rows = ss_rows / (n - 1)
    ms_cols = ss_cols / (k - 1)
    ms_error = ss_error / ((n - 1) * (k - 1))

    denominator = (
        ms_rows
        + (k - 1) * ms_error
        + (k * (ms_cols - ms_error) / n)
    )
    if not math.isfinite(denominator) or abs(denominator) < 1e-15:
        return None
    value = (ms_rows - ms_error) / denominator
    return float(value) if math.isfinite(value) else None


def _fixed_channel_map(session):
    result = {}
    for row in session.get("channels", []):
        channel = str(row["channel"])
        fixed = row["frozen_fixed"]
        names = list(fixed["aperiodic_parameter_names"])
        params = list(fixed["aperiodic_parameters"])
        if "exponent" not in names:
            raise ValueError(f"channel {channel} has no aperiodic exponent")
        exponent = float(params[names.index("exponent")])
        result[channel] = {
            "aperiodic_exponent": exponent,
            "peak_count": int(fixed["peak_count"]),
            "zero_peak_state": bool(fixed["zero_peak_state"]),
        }
    return result


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
    if len(d4_subjects) != expected_subject_count:
        raise ValueError(
            f"expected {expected_subject_count} D4-verified subjects, found {len(d4_subjects)}"
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

    channel_pairs = {}
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

        sessions = sorted(spec["sessions"], key=lambda item: str(item["session_id"]))
        if len(sessions) != 2:
            raise ValueError(
                f"subject {subject} must have exactly two repeat sessions; found {len(sessions)}"
            )

        fixed_maps = [_fixed_channel_map(session) for session in sessions]
        shared_channels = sorted(set(fixed_maps[0]) & set(fixed_maps[1]))
        for channel in shared_channels:
            first = fixed_maps[0][channel]
            second = fixed_maps[1][channel]
            bucket = channel_pairs.setdefault(
                channel,
                {
                    "aperiodic_exponent": [],
                    "peak_count_equal": [],
                    "zero_peak_equal": [],
                },
            )
            bucket["aperiodic_exponent"].append(
                [first["aperiodic_exponent"], second["aperiodic_exponent"]]
            )
            bucket["peak_count_equal"].append(
                first["peak_count"] == second["peak_count"]
            )
            bucket["zero_peak_equal"].append(
                first["zero_peak_state"] == second["zero_peak_state"]
            )

        session_rows = []
        for session in sessions:
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
            "shared_parameterized_channel_count": len(shared_channels),
            "sessions": session_rows,
        })

    channel_repeatability = []
    for channel in sorted(channel_pairs):
        bucket = channel_pairs[channel]
        exponent_pairs = bucket["aperiodic_exponent"]
        exponent_abs_diffs = [abs(pair[0] - pair[1]) for pair in exponent_pairs]
        peak_equal = bucket["peak_count_equal"]
        zero_equal = bucket["zero_peak_equal"]
        channel_repeatability.append({
            "channel": channel,
            "subject_pair_count": len(exponent_pairs),
            "aperiodic_exponent_icc_a1": _icc_a1(exponent_pairs),
            "aperiodic_exponent_absolute_difference": _summary(exponent_abs_diffs),
            "peak_count_exact_agreement_fraction":
                (sum(peak_equal) / len(peak_equal)) if peak_equal else None,
            "zero_peak_state_exact_agreement_fraction":
                (sum(zero_equal) / len(zero_equal)) if zero_equal else None,
        })

    exponent_iccs = [
        row["aperiodic_exponent_icc_a1"] for row in channel_repeatability
    ]
    finite_iccs = _finite(exponent_iccs)
    peak_agreements = [
        row["peak_count_exact_agreement_fraction"] for row in channel_repeatability
    ]
    zero_agreements = [
        row["zero_peak_state_exact_agreement_fraction"] for row in channel_repeatability
    ]

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
            "channelwise_aperiodic_exponent_icc_a1": {
                **_summary(exponent_iccs),
                "negative_count": sum(value < 0 for value in finite_iccs),
                "nonnegative_count": sum(value >= 0 for value in finite_iccs),
            },
            "channelwise_peak_count_exact_agreement_fraction": _summary(peak_agreements),
            "channelwise_zero_peak_state_exact_agreement_fraction": _summary(zero_agreements),
        },
        "repeatability_method": {
            "continuous": (
                "ICC(A,1): two-way mixed, absolute-agreement, single-measure; "
                "subjects are rows and the two repeat sessions are columns"
            ),
            "categorical": "channel-wise exact agreement fraction across subject pairs",
            "hierarchy_rule": (
                "subjects are the independent repeatability units; channels are summarized "
                "separately and are not treated as independent subjects"
            ),
        },
        "channel_repeatability": channel_repeatability,
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
        "repeatability_method": result["repeatability_method"],
        "interpretation_ceiling": result["interpretation_ceiling"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
