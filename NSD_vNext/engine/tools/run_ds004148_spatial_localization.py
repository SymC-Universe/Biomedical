#!/usr/bin/env python3
"""Run the prospectively frozen ds004148 channel-level spatial/state
localization follow-up.

This is a post-result explanatory P0-D analysis. It reuses the unchanged
descriptive representation and cannot license modal damping, natural frequency,
lowercase chi, capital Chi, clinical inference, recovery, or population claims.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from itertools import combinations
from pathlib import Path

import numpy as np

TOOLS_ROOT = Path(__file__).resolve().parent
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from run_ds004148_descriptive_transfer import _pearson, _recording


TARGET_TASK = "eyesopen"
TARGET_SESSION_A = "ses-session2"
TARGET_SESSION_B = "ses-session3"


def _region(label: str) -> str:
    if label.startswith(("FT", "TP", "T")):
        return "temporal"
    if label.startswith(("Fp", "AF", "FC", "F")):
        return "frontal_anterior"
    if label.startswith(("CP", "C")):
        return "central"
    if label.startswith(("PO", "P", "O")):
        return "posterior"
    raise ValueError(f"unmapped channel region: {label}")


def _hemisphere(label: str) -> str:
    if label.endswith("z"):
        return "midline"
    digits = "".join(ch for ch in label if ch.isdigit())
    if not digits:
        raise ValueError(f"cannot infer hemisphere from channel: {label}")
    return "left" if int(digits[-1]) % 2 else "right"


def _median(values: list[float]) -> float | None:
    clean = [float(v) for v in values if v is not None and math.isfinite(float(v))]
    return float(np.median(clean)) if clean else None


def _channel_pair(
    first: dict[str, object],
    second: dict[str, object],
    labels: list[str],
    reference: dict[str, object],
) -> list[dict[str, object]]:
    first_channels = {str(item["channel"]): item for item in first["channels"]}
    second_channels = {str(item["channel"]): item for item in second["channels"]}
    first_index = {label: i for i, label in enumerate(first["channel_labels"])}
    second_index = {label: i for i, label in enumerate(second["channel_labels"])}
    minimum_peak_n = int(reference["minimum_peak_pair_n_for_channel_threshold"])

    rows = []
    for label in labels:
        a = first_channels[label]
        b = second_channels[label]
        parent = reference["channels"][label]

        correlation = _pearson(
            first["log_psd"][first_index[label]],
            second["log_psd"][second_index[label]],
        )
        exponent_diff = abs(
            float(a["aperiodic_exponent"]) - float(b["aperiodic_exponent"])
        )

        peak_shift = None
        if a["peaks"] and b["peaks"]:
            center = float(a["peaks"][0]["center_frequency_hz"])
            peak_shift = min(
                abs(center - float(item["center_frequency_hz"]))
                for item in b["peaks"]
            )

        peak_ref = parent["first_peak_nearest_center_diff_hz"]
        peak_threshold_admissible = (
            peak_shift is not None
            and int(peak_ref["n"]) >= minimum_peak_n
            and peak_ref["q95"] is not None
        )
        peak_high = (
            bool(peak_shift > float(peak_ref["q95"]))
            if peak_threshold_admissible
            else None
        )
        peak_ratio = (
            float(peak_shift / float(peak_ref["q95"]))
            if peak_threshold_admissible and float(peak_ref["q95"]) > 0
            else None
        )

        exponent_ref = parent["aperiodic_exponent_abs_diff"]
        correlation_ref = parent["log_psd_correlation"]

        rows.append({
            "channel": label,
            "region": _region(label),
            "hemisphere": _hemisphere(label),
            "log_psd_correlation": float(correlation),
            "aperiodic_exponent_abs_diff": float(exponent_diff),
            "first_peak_nearest_center_diff_hz": (
                float(peak_shift) if peak_shift is not None else None
            ),
            "parent_peak_pair_n": int(peak_ref["n"]),
            "parent_peak_shift_q95_hz": peak_ref["q95"],
            "peak_shift_over_q95_ratio": peak_ratio,
            "PEAK_SHIFT_HIGH": peak_high,
            "APERIODIC_DIFF_HIGH": bool(
                exponent_ref["q95"] is not None
                and exponent_diff > float(exponent_ref["q95"])
            ),
            "PSD_CORRELATION_LOW": bool(
                correlation_ref["q05"] is not None
                and correlation < float(correlation_ref["q05"])
            ),
            "MODEL_FAMILY_UNSTABLE": bool(
                a["model_family_disagreement"] or b["model_family_disagreement"]
            ),
            "PEAK_COUNT_CHANGED": int(a["peak_count"]) != int(b["peak_count"]),
            "ZERO_PEAK_STATE_CHANGED": bool(a["zero_peak_state"]) != bool(b["zero_peak_state"]),
            "max_peak_count_reached_any": bool(
                a["max_peak_count_reached"] or b["max_peak_count_reached"]
            ),
            "width_boundary_hits_total": int(a["width_boundary_hit_count"])
            + int(b["width_boundary_hit_count"]),
        })
    return rows


def _group_summary(rows: list[dict[str, object]], key: str) -> dict[str, object]:
    groups: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        groups.setdefault(str(row[key]), []).append(row)

    out = {}
    for group, items in sorted(groups.items()):
        eligible = [row for row in items if row["first_peak_nearest_center_diff_hz"] is not None]
        high = [row for row in items if row["PEAK_SHIFT_HIGH"] is True]
        out[group] = {
            "channel_count": len(items),
            "eligible_peak_shift_channel_count": len(eligible),
            "peak_shift_high_count": len(high),
            "peak_shift_high_fraction_of_eligible": (
                len(high) / len(eligible) if eligible else None
            ),
            "median_peak_shift_hz": _median(
                [row["first_peak_nearest_center_diff_hz"] for row in eligible]
            ),
            "high_shift_channels": [row["channel"] for row in high],
        }
    return out


def _pair_summary(
    first: dict[str, object],
    second: dict[str, object],
    labels: list[str],
    reference: dict[str, object],
) -> dict[str, object]:
    rows = _channel_pair(first, second, labels, reference)
    eligible = [row for row in rows if row["first_peak_nearest_center_diff_hz"] is not None]
    high = [row for row in rows if row["PEAK_SHIFT_HIGH"] is True]

    top = sorted(
        [row for row in rows if row["peak_shift_over_q95_ratio"] is not None],
        key=lambda row: float(row["peak_shift_over_q95_ratio"]),
        reverse=True,
    )[:10]

    overlap = {
        "PEAK_SHIFT_HIGH_count": len(high),
        "APERIODIC_DIFF_HIGH_within_PEAK_SHIFT_HIGH": sum(
            bool(row["APERIODIC_DIFF_HIGH"]) for row in high
        ),
        "PSD_CORRELATION_LOW_within_PEAK_SHIFT_HIGH": sum(
            bool(row["PSD_CORRELATION_LOW"]) for row in high
        ),
        "MODEL_FAMILY_UNSTABLE_within_PEAK_SHIFT_HIGH": sum(
            bool(row["MODEL_FAMILY_UNSTABLE"]) for row in high
        ),
        "PEAK_COUNT_CHANGED_within_PEAK_SHIFT_HIGH": sum(
            bool(row["PEAK_COUNT_CHANGED"]) for row in high
        ),
        "ZERO_PEAK_STATE_CHANGED_within_PEAK_SHIFT_HIGH": sum(
            bool(row["ZERO_PEAK_STATE_CHANGED"]) for row in high
        ),
    }

    regions = _group_summary(rows, "region")
    hemispheres = _group_summary(rows, "hemisphere")

    return {
        "task": first["task"],
        "session_a": first["session"],
        "session_b": second["session"],
        "matched_channel_count": len(rows),
        "eligible_peak_shift_channel_count": len(eligible),
        "peak_shift_high_count": len(high),
        "peak_shift_high_fraction_of_eligible": (
            len(high) / len(eligible) if eligible else None
        ),
        "median_peak_shift_hz": _median(
            [row["first_peak_nearest_center_diff_hz"] for row in eligible]
        ),
        "regions_with_peak_shift_high": [
            region for region, data in regions.items()
            if int(data["peak_shift_high_count"]) > 0
        ],
        "hemispheres_with_peak_shift_high": [
            side for side, data in hemispheres.items()
            if int(data["peak_shift_high_count"]) > 0
        ],
        "regions": regions,
        "hemispheres": hemispheres,
        "cooccurrence": overlap,
        "top10_by_peak_shift_over_parent_q95": [
            {
                "channel": row["channel"],
                "region": row["region"],
                "hemisphere": row["hemisphere"],
                "peak_shift_hz": row["first_peak_nearest_center_diff_hz"],
                "parent_q95_hz": row["parent_peak_shift_q95_hz"],
                "ratio": row["peak_shift_over_q95_ratio"],
                "APERIODIC_DIFF_HIGH": row["APERIODIC_DIFF_HIGH"],
                "PSD_CORRELATION_LOW": row["PSD_CORRELATION_LOW"],
                "MODEL_FAMILY_UNSTABLE": row["MODEL_FAMILY_UNSTABLE"],
                "PEAK_COUNT_CHANGED": row["PEAK_COUNT_CHANGED"],
                "ZERO_PEAK_STATE_CHANGED": row["ZERO_PEAK_STATE_CHANGED"],
            }
            for row in top
        ],
        "channels": rows,
    }


def execute(
    manifest_path: Path,
    reference_path: Path,
    output_dir: Path,
) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    labels = [str(label) for label in reference["matched_channels"]]

    output_dir.mkdir(parents=True, exist_ok=True)
    payload_dir = output_dir / "payloads"
    payload_dir.mkdir(exist_ok=True)

    recordings = [_recording(item, manifest, payload_dir) for item in manifest["recordings"]]
    for recording in recordings:
        available = set(str(label) for label in recording["channel_labels"])
        missing = sorted(set(labels) - available)
        if missing:
            raise ValueError(f"{recording['session']} {recording['task']}: missing matched labels {missing}")

    grouped: dict[str, list[dict[str, object]]] = {}
    for recording in recordings:
        grouped.setdefault(str(recording["task"]), []).append(recording)

    pairs = []
    target = None
    controls = []
    for task, items in sorted(grouped.items()):
        items = sorted(items, key=lambda item: str(item["session"]))
        for first, second in combinations(items, 2):
            summary = _pair_summary(first, second, labels, reference)
            pairs.append(summary)
            is_target = (
                task == TARGET_TASK
                and first["session"] == TARGET_SESSION_A
                and second["session"] == TARGET_SESSION_B
            )
            if is_target:
                target = summary
            else:
                controls.append({
                    "task": summary["task"],
                    "session_a": summary["session_a"],
                    "session_b": summary["session_b"],
                    "eligible_peak_shift_channel_count": summary[
                        "eligible_peak_shift_channel_count"
                    ],
                    "peak_shift_high_count": summary["peak_shift_high_count"],
                    "peak_shift_high_fraction_of_eligible": summary[
                        "peak_shift_high_fraction_of_eligible"
                    ],
                    "median_peak_shift_hz": summary["median_peak_shift_hz"],
                    "regions_with_peak_shift_high": summary[
                        "regions_with_peak_shift_high"
                    ],
                })

    if target is None:
        raise ValueError("frozen target pair was not found")

    result = {
        "schema": "NSD_DS004148_SPATIAL_LOCALIZATION_RESULT_V0_1",
        "status": "P0_D_POSTRESULT_EXPLANATORY_LOCALIZATION",
        "dataset": "ds004148",
        "subject": manifest["subject"],
        "source_manifest": str(manifest_path),
        "parent_reference": {
            "schema": reference["schema"],
            "source_workflow_run": reference["source_workflow_run"],
            "subject_count": reference["subject_count"],
            "matched_channel_count": reference["matched_channel_count"],
        },
        "target_definition": {
            "task": TARGET_TASK,
            "session_a": TARGET_SESSION_A,
            "session_b": TARGET_SESSION_B,
            "selection_status": "selected_after_closed_transfer_result; explanatory, not untouched confirmation",
        },
        "target_pair": target,
        "same_state_controls": controls,
        "all_pairs": pairs,
        "interpretation_firewall": [
            "channel q05/q95 values are empirical descriptive context, not confidence intervals",
            "channels are repeated measurements within one subject",
            "peak centers are descriptive periodic components, not natural frequencies",
            "peak displacement is not modal tracking",
            "repeat-session changes are not recovery or resilience",
            "no modal damping is licensed",
            "no lowercase chi is licensed",
            "no capital Chi empirical neural architecture is licensed",
            "no diagnosis, prognosis, treatment, or population inference is licensed",
        ],
        "licenses_modal_damping": False,
        "licenses_natural_frequency": False,
        "licenses_local_chi": False,
        "licenses_capital_chi": False,
        "licenses_diagnosis": False,
        "licenses_population_inference": False,
    }
    return result


def _write_summary(result: dict[str, object], path: Path) -> None:
    target = result["target_pair"]
    lines = [
        "# ds004148 spatial/state localization verification summary",
        "",
        f"Status: {result['status']}",
        f"Target: {target['task']} {target['session_a']} vs {target['session_b']}",
        f"Matched channels: {target['matched_channel_count']}",
        f"Eligible peak-shift channels: {target['eligible_peak_shift_channel_count']}",
        f"Peak-shift-high channels: {target['peak_shift_high_count']}",
        f"Peak-shift-high fraction: {target['peak_shift_high_fraction_of_eligible']}",
        f"Regions containing high-shift channels: {', '.join(target['regions_with_peak_shift_high']) or 'none'}",
        f"Hemispheres containing high-shift channels: {', '.join(target['hemispheres_with_peak_shift_high']) or 'none'}",
        "",
        "## Co-occurrence within high-shift channels",
    ]
    for key, value in target["cooccurrence"].items():
        lines.append(f"- {key}: {value}")

    lines += ["", "## Top channels by peak-shift / parent-channel q95"]
    for row in target["top10_by_peak_shift_over_parent_q95"]:
        lines.append(
            f"- {row['channel']}: shift={row['peak_shift_hz']}, "
            f"q95={row['parent_q95_hz']}, ratio={row['ratio']}, "
            f"region={row['region']}, hemisphere={row['hemisphere']}, "
            f"aperiodic_high={row['APERIODIC_DIFF_HIGH']}, "
            f"psd_low={row['PSD_CORRELATION_LOW']}, "
            f"model_family_unstable={row['MODEL_FAMILY_UNSTABLE']}"
        )

    lines += [
        "",
        "No modal damping, natural frequency, lowercase chi, capital Chi, clinical, recovery, or population claim is licensed.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--parent-reference", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    result = execute(args.manifest, args.parent_reference, args.output_dir)
    result_path = args.output_dir / "ds004148_spatial_localization_result_v0.1.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_summary(result, args.output_dir / "VERIFY_SUMMARY.md")
    target = result["target_pair"]
    print(json.dumps({
        "status": result["status"],
        "target_peak_shift_high_count": target["peak_shift_high_count"],
        "target_eligible_peak_shift_channel_count": target[
            "eligible_peak_shift_channel_count"
        ],
        "regions_with_peak_shift_high": target["regions_with_peak_shift_high"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
