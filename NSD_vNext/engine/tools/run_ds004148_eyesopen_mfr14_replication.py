#!/usr/bin/env python3
"""Run the prospectively frozen 14-subject untouched ds004148 eyes-open
replication.

The independent unit is subject. Channel-level flags are descriptive inputs to
subject-level summaries and never manufacture sample size.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

TOOLS_ROOT = Path(__file__).resolve().parent
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from run_ds004148_descriptive_transfer import (
    _fit_channel,
    _hash,
    _parse_vhdr,
    _read_brainvision,
)
from run_ds004148_spatial_localization import _pair_summary


def _request_bytes(url: str, *, github_api: bool = False) -> bytes:
    headers = {"User-Agent": "SymC-NSD-MFR14/0.1"}
    token = os.environ.get("GITHUB_TOKEN")
    if github_api and token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def _download(url: str, path: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "SymC-NSD-MFR14/0.1"})
    with urllib.request.urlopen(request, timeout=300) as response, path.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def _resolve_annex_identity(
    repository: str,
    commit: str,
    source_path: str,
    extension: str,
) -> dict[str, object]:
    encoded = urllib.parse.quote(source_path, safe="/")
    api_url = (
        f"https://api.github.com/repos/{repository}/contents/{encoded}"
        f"?ref={commit}"
    )
    body = _request_bytes(api_url, github_api=True)
    payload = json.loads(body.decode("utf-8"))

    target = None
    if isinstance(payload, dict):
        target = payload.get("target")
        if target is None and payload.get("content"):
            target = base64.b64decode(payload["content"]).decode("utf-8").strip()
    elif isinstance(payload, str):
        target = payload

    if not target:
        raise ValueError(f"could not resolve git-annex target for {source_path}")

    match = re.search(
        rf"MD5E-s(\d+)--([0-9a-fA-F]{{32}})\.{re.escape(extension)}",
        str(target),
    )
    if not match:
        raise ValueError(
            f"unrecognized git-annex target for {source_path}: {target}"
        )

    return {
        "git_annex_target": str(target),
        "expected_size_bytes": int(match.group(1)),
        "expected_md5": match.group(2).lower(),
        "github_api_url": api_url,
    }


def _recording(
    subject: str,
    session: str,
    task: str,
    source_release: dict[str, str],
    root: Path,
) -> dict[str, object]:
    commit = source_release["public_git_commit"]
    repository = source_release["public_git_repository"]
    mirror = source_release["nemar_mirror"]
    base = f"{subject}/{session}/eeg/{subject}_{session}_task-{task}_eeg"

    nemar_base = f"https://data.nemar.org/{mirror}/{base}"

    local_paths = {
        "vhdr": root / f"{subject}__{session}__{task}.vhdr",
        "vmrk": root / f"{subject}__{session}__{task}.vmrk",
        "eeg": root / f"{subject}__{session}__{task}.eeg",
    }
    identities = {}

    for extension in ("vhdr", "vmrk", "eeg"):
        source_path = base + "." + extension
        annex = _resolve_annex_identity(
            repository,
            commit,
            source_path,
            extension,
        )
        _download(nemar_base + "." + extension, local_paths[extension])

        observed_size = local_paths[extension].stat().st_size
        observed_md5 = _hash(local_paths[extension], "md5")
        if observed_size != int(annex["expected_size_bytes"]):
            raise ValueError(
                f"{subject} {session} {extension}: size mismatch "
                f"{observed_size} != {annex['expected_size_bytes']}"
            )
        if observed_md5 != str(annex["expected_md5"]):
            raise ValueError(
                f"{subject} {session} {extension}: MD5 mismatch "
                f"{observed_md5} != {annex['expected_md5']}"
            )

        identities[extension] = {
            **annex,
            "observed_size_bytes": observed_size,
            "observed_md5": observed_md5,
            "sha256": _hash(local_paths[extension], "sha256"),
        }

    vhdr_path = local_paths["vhdr"]
    vmrk_path = local_paths["vmrk"]
    eeg_path = local_paths["eeg"]

    header = _parse_vhdr(vhdr_path)
    if int(header["number_of_channels"]) != 61:
        raise ValueError(f"{subject} {session}: raw channel count != 61")
    if float(header["sampling_rate_hz"]) != 500.0:
        raise ValueError(f"{subject} {session}: sampling rate != 500 Hz")
    if str(header["binary_format"]).upper() != "IEEE_FLOAT_32":
        raise ValueError(f"{subject} {session}: binary format mismatch")
    if str(header["data_orientation"]).upper() != "MULTIPLEXED":
        raise ValueError(f"{subject} {session}: orientation mismatch")

    labels, data = _read_brainvision(eeg_path, header)
    if data.shape != (61, 150000):
        raise ValueError(f"{subject} {session}: decoded shape {data.shape}")

    channels = []
    log_psd = []
    for label, signal in zip(labels, data):
        log_power, fitted = _fit_channel(signal)
        log_psd.append(log_power)
        channels.append({"channel": label, **fitted})

    return {
        "subject": subject,
        "session": session,
        "task": task,
        "channel_labels": labels,
        "channels": channels,
        "log_psd": np.asarray(log_psd, dtype=float),
        "source_identity": {
            "base": base,
            "files": identities,
            "d4_pass": True,
        },
    }


def _pair_compact(pair: dict[str, object]) -> dict[str, object]:
    high = int(pair["peak_shift_high_count"])
    unstable = int(
        pair["cooccurrence"]["MODEL_FAMILY_UNSTABLE_within_PEAK_SHIFT_HIGH"]
    )
    return {
        "session_a": pair["session_a"],
        "session_b": pair["session_b"],
        "eligible_peak_shift_channel_count": pair[
            "eligible_peak_shift_channel_count"
        ],
        "peak_shift_high_count": high,
        "peak_shift_high_fraction_of_eligible": pair[
            "peak_shift_high_fraction_of_eligible"
        ],
        "median_peak_shift_hz": pair["median_peak_shift_hz"],
        "model_family_unstable_within_high_count": unstable,
        "model_family_unstable_within_high_fraction": (
            unstable / high if high else None
        ),
        "regions_with_peak_shift_high": pair["regions_with_peak_shift_high"],
    }


def _summary(values: list[float]) -> dict[str, float | int | None]:
    clean = [float(v) for v in values if v is not None and math.isfinite(float(v))]
    if not clean:
        return {"n": 0, "minimum": None, "median": None, "maximum": None}
    arr = np.asarray(clean, dtype=float)
    return {
        "n": int(arr.size),
        "minimum": float(np.min(arr)),
        "median": float(np.median(arr)),
        "maximum": float(np.max(arr)),
    }


def _sign_test(deltas: list[float]) -> dict[str, object]:
    positive = sum(delta > 0 for delta in deltas)
    negative = sum(delta < 0 for delta in deltas)
    tied = sum(delta == 0 for delta in deltas)
    non_tied = positive + negative
    p_value = (
        float(binomtest(positive, non_tied, 0.5, alternative="two-sided").pvalue)
        if non_tied
        else 1.0
    )
    return {
        "positive": positive,
        "negative": negative,
        "tied": tied,
        "non_tied": non_tied,
        "two_sided_exact_sign_test_p": p_value,
    }


def _holm_two(raw: dict[str, float]) -> dict[str, float]:
    ordered = sorted(raw.items(), key=lambda item: item[1])
    adjusted = {}
    running = 0.0
    m = len(ordered)
    for index, (name, p_value) in enumerate(ordered):
        candidate = min(1.0, (m - index) * float(p_value))
        running = max(running, candidate)
        adjusted[name] = running
    return adjusted


def execute(
    cohort_manifest_path: Path,
    parent_reference_path: Path,
    output_dir: Path,
) -> dict[str, object]:
    cohort = json.loads(cohort_manifest_path.read_text(encoding="utf-8"))
    reference = json.loads(parent_reference_path.read_text(encoding="utf-8"))
    labels = [str(label) for label in reference["matched_channels"]]

    output_dir.mkdir(parents=True, exist_ok=True)
    payload_dir = output_dir / "payloads"
    payload_dir.mkdir(exist_ok=True)

    subject_results = []
    failures = []

    for subject in cohort["subjects"]:
        try:
            recordings = {}
            for session in cohort["sessions"]:
                recordings[session] = _recording(
                    subject,
                    session,
                    cohort["task"],
                    cohort["source_release"],
                    payload_dir,
                )
                available = set(recordings[session]["channel_labels"])
                missing = sorted(set(labels) - available)
                if missing:
                    raise ValueError(
                        f"{subject} {session}: missing matched labels {missing}"
                    )

            p12 = _pair_summary(
                recordings["ses-session1"],
                recordings["ses-session2"],
                labels,
                reference,
            )
            p13 = _pair_summary(
                recordings["ses-session1"],
                recordings["ses-session3"],
                labels,
                reference,
            )
            p23 = _pair_summary(
                recordings["ses-session2"],
                recordings["ses-session3"],
                labels,
                reference,
            )

            c12 = _pair_compact(p12)
            c13 = _pair_compact(p13)
            c23 = _pair_compact(p23)

            f12 = float(c12["peak_shift_high_fraction_of_eligible"])
            f13 = float(c13["peak_shift_high_fraction_of_eligible"])
            f23 = float(c23["peak_shift_high_fraction_of_eligible"])

            m12 = float(c12["median_peak_shift_hz"])
            m13 = float(c13["median_peak_shift_hz"])
            m23 = float(c23["median_peak_shift_hz"])

            subject_results.append({
                "subject": subject,
                "source_identity": {
                    session: recordings[session]["source_identity"]
                    for session in cohort["sessions"]
                },
                "pairs": {
                    "session1_session2": c12,
                    "session1_session3": c13,
                    "session2_session3": c23,
                },
                "paired_deltas": {
                    "high_fraction_13_minus_12": f13 - f12,
                    "high_fraction_23_minus_12": f23 - f12,
                    "median_peak_shift_13_minus_12_hz": m13 - m12,
                    "median_peak_shift_23_minus_12_hz": m23 - m12,
                },
            })
        except Exception as exc:
            failures.append({
                "subject": subject,
                "error_type": type(exc).__name__,
                "error": str(exc),
            })

    if failures:
        status = "MFR14_INCOMPLETE_SOURCE_OR_D4_FAILURE"
    else:
        status = "P0_Q_MFR14_UNTOUCHED_EYESOPEN_REPLICATION"

    result = {
        "schema": "NSD_DS004148_EYESOPEN_MFR14_REPLICATION_RESULT_V0_1",
        "status": status,
        "cohort_manifest": str(cohort_manifest_path),
        "parent_reference": {
            "schema": reference["schema"],
            "source_workflow_run": reference["source_workflow_run"],
            "subject_count": reference["subject_count"],
            "matched_channel_count": reference["matched_channel_count"],
        },
        "requested_subject_count": len(cohort["subjects"]),
        "completed_subject_count": len(subject_results),
        "failures": failures,
        "subjects": subject_results,
        "interpretation_firewall": [
            "subject is the independent unit",
            "channels do not create inferential sample size",
            "channel q05/q95 values are descriptive parent context",
            "peak centers are descriptive components, not natural frequencies",
            "no modal damping is licensed",
            "no lowercase chi is licensed",
            "no capital Chi empirical neural architecture is licensed",
            "no diagnosis, prognosis, treatment, recovery, or broad population inference is licensed",
        ],
        "licenses_modal_damping": False,
        "licenses_natural_frequency": False,
        "licenses_local_chi": False,
        "licenses_capital_chi": False,
        "licenses_diagnosis": False,
        "licenses_population_inference": False,
    }

    if not failures:
        pair_names = (
            "session1_session2",
            "session1_session3",
            "session2_session3",
        )
        aggregate = {}
        for pair_name in pair_names:
            aggregate[pair_name] = {
                "peak_shift_high_fraction_of_eligible": _summary([
                    subject["pairs"][pair_name][
                        "peak_shift_high_fraction_of_eligible"
                    ]
                    for subject in subject_results
                ]),
                "median_peak_shift_hz": _summary([
                    subject["pairs"][pair_name]["median_peak_shift_hz"]
                    for subject in subject_results
                ]),
                "model_family_unstable_within_high_fraction": _summary([
                    subject["pairs"][pair_name][
                        "model_family_unstable_within_high_fraction"
                    ]
                    for subject in subject_results
                    if subject["pairs"][pair_name][
                        "model_family_unstable_within_high_fraction"
                    ] is not None
                ]),
            }

        delta13 = [
            float(subject["paired_deltas"]["high_fraction_13_minus_12"])
            for subject in subject_results
        ]
        delta23 = [
            float(subject["paired_deltas"]["high_fraction_23_minus_12"])
            for subject in subject_results
        ]
        median13 = [
            float(subject["paired_deltas"]["median_peak_shift_13_minus_12_hz"])
            for subject in subject_results
        ]
        median23 = [
            float(subject["paired_deltas"]["median_peak_shift_23_minus_12_hz"])
            for subject in subject_results
        ]

        test13 = _sign_test(delta13)
        test23 = _sign_test(delta23)
        holm = _holm_two({
            "high_fraction_13_minus_12": test13["two_sided_exact_sign_test_p"],
            "high_fraction_23_minus_12": test23["two_sided_exact_sign_test_p"],
        })
        test13["holm_adjusted_p"] = holm["high_fraction_13_minus_12"]
        test23["holm_adjusted_p"] = holm["high_fraction_23_minus_12"]

        result["aggregate"] = aggregate
        result["paired_contrasts"] = {
            "high_fraction_13_minus_12": {
                "distribution": _summary(delta13),
                "sign_test": test13,
            },
            "high_fraction_23_minus_12": {
                "distribution": _summary(delta23),
                "sign_test": test23,
            },
            "median_peak_shift_13_minus_12_hz": {
                "distribution": _summary(median13),
            },
            "median_peak_shift_23_minus_12_hz": {
                "distribution": _summary(median23),
            },
        }

    return result


def _write_summary(result: dict[str, object], path: Path) -> None:
    lines = [
        "# ds004148 eyes-open MFR-14 replication verification summary",
        "",
        f"Status: {result['status']}",
        f"Completed subjects: {result['completed_subject_count']} / {result['requested_subject_count']}",
    ]
    if result["failures"]:
        lines += ["", "## Failures"]
        for failure in result["failures"]:
            lines.append(
                f"- {failure['subject']}: {failure['error_type']}: {failure['error']}"
            )
    else:
        lines += ["", "## Aggregate high-shift fractions"]
        for pair_name, data in result["aggregate"].items():
            summary = data["peak_shift_high_fraction_of_eligible"]
            lines.append(
                f"- {pair_name}: median={summary['median']}; "
                f"min={summary['minimum']}; max={summary['maximum']}"
            )
        lines += ["", "## Predeclared paired contrasts"]
        for name in (
            "high_fraction_13_minus_12",
            "high_fraction_23_minus_12",
        ):
            contrast = result["paired_contrasts"][name]
            test = contrast["sign_test"]
            lines.append(
                f"- {name}: median_delta={contrast['distribution']['median']}; "
                f"positive={test['positive']}; negative={test['negative']}; "
                f"tied={test['tied']}; exact_p={test['two_sided_exact_sign_test_p']}; "
                f"holm_p={test['holm_adjusted_p']}"
            )

    lines += [
        "",
        "No modal damping, natural frequency, lowercase chi, capital Chi, clinical, recovery, or broad population claim is licensed.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort-manifest", required=True, type=Path)
    parser.add_argument("--parent-reference", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    result = execute(args.cohort_manifest, args.parent_reference, args.output_dir)
    result_path = args.output_dir / "ds004148_eyesopen_mfr14_replication_result_v0.1.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_summary(result, args.output_dir / "VERIFY_SUMMARY.md")

    print(json.dumps({
        "status": result["status"],
        "completed_subject_count": result["completed_subject_count"],
        "failure_count": len(result["failures"]),
        "paired_contrasts": result.get("paired_contrasts"),
    }, indent=2, sort_keys=True))

    return 0 if not result["failures"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
