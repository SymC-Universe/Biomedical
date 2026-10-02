#!/usr/bin/env python3
"""Audit ds004148 eyes-closed BrainVision header topology across the full dataset.

This is a source/D4 metadata audit only. It resolves VHDR git-annex identities
from the pinned OpenNeuro commit, downloads the exact VHDR payloads from the
declared NEMAR mirror, verifies MD5/size, and records channel topology and
acquisition metadata. It does not download EEG samples or compute signal
features.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

SOURCE_REPOSITORY = "OpenNeuroDatasets/ds004148"
SOURCE_COMMIT = "0c740d838a2c33feeec0b6e514aea323d0e65ca4"
NEMAR_MIRROR = "on004148/v1.0.0"
TASK = "eyesclosed"
SUBJECTS = tuple(f"sub-{index:02d}" for index in range(1, 61))
SESSIONS = ("ses-session1", "ses-session2", "ses-session3")


def _request_bytes(url: str, *, github_api: bool = False) -> bytes:
    headers = {"User-Agent": "SymC-NSD-header-audit/0.1"}
    token = os.environ.get("GITHUB_TOKEN")
    if github_api and token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read()


def _download(url: str, path: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "SymC-NSD-header-audit/0.1"},
    )
    with urllib.request.urlopen(request, timeout=180) as response, path.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def _hash(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_vhdr_annex(source_path: str) -> dict[str, object]:
    encoded = urllib.parse.quote(source_path, safe="/")
    api_url = (
        f"https://api.github.com/repos/{SOURCE_REPOSITORY}/contents/{encoded}"
        f"?ref={SOURCE_COMMIT}"
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

    match = re.search(r"MD5E-s(\d+)--([0-9a-fA-F]{32})\.vhdr", str(target))
    if not match:
        raise ValueError(f"unrecognized VHDR annex target for {source_path}: {target}")

    return {
        "git_annex_target": str(target),
        "expected_size_bytes": int(match.group(1)),
        "expected_md5": match.group(2).lower(),
        "github_api_url": api_url,
    }


def _parse_vhdr(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")

    def grab(name: str) -> str | None:
        match = re.search(
            rf"(?mi)^\s*{re.escape(name)}\s*=\s*(.+?)\s*$",
            text,
        )
        return match.group(1).strip() if match else None

    number_text = grab("NumberOfChannels")
    interval_text = grab("SamplingInterval")
    if number_text is None or interval_text is None:
        raise ValueError("VHDR missing NumberOfChannels or SamplingInterval")

    channels = []
    for match in re.finditer(r"(?mi)^Ch(\d+)=(.*)$", text):
        parts = [part.strip() for part in match.group(2).split(",")]
        channels.append({
            "index": int(match.group(1)),
            "name": parts[0],
            "resolution": (
                float(parts[2]) if len(parts) > 2 and parts[2] else 1.0
            ),
            "unit": parts[3] if len(parts) > 3 else "",
        })

    labels = [str(item["name"]) for item in channels]
    if len(labels) != len(set(labels)):
        raise ValueError("duplicate channel labels in VHDR")

    number = int(number_text)
    if len(channels) != number:
        raise ValueError(
            f"VHDR channel-definition mismatch: NumberOfChannels={number}, "
            f"definitions={len(channels)}"
        )

    sampling_rate = 1_000_000.0 / float(interval_text)

    return {
        "number_of_channels": number,
        "sampling_rate_hz": sampling_rate,
        "binary_format": grab("BinaryFormat"),
        "data_orientation": grab("DataOrientation"),
        "channel_labels": labels,
        "channels": channels,
    }


def _signature(labels: list[str]) -> str:
    return "|".join(labels)


def _intersection(label_lists: list[list[str]]) -> list[str]:
    if not label_lists:
        return []
    common = set(label_lists[0])
    for labels in label_lists[1:]:
        common &= set(labels)
    # Preserve the first record's native order for reproducible output.
    return [label for label in label_lists[0] if label in common]


def _union(label_lists: list[list[str]]) -> list[str]:
    if not label_lists:
        return []
    present = set()
    for labels in label_lists:
        present.update(labels)
    return sorted(present)


def execute(matched_reference_path: Path, output_dir: Path) -> dict[str, object]:
    matched_reference = json.loads(
        matched_reference_path.read_text(encoding="utf-8")
    )
    old_matched = [str(label) for label in matched_reference["channels"]]

    output_dir.mkdir(parents=True, exist_ok=True)
    payload_dir = output_dir / "vhdr_payloads"
    payload_dir.mkdir(exist_ok=True)

    records = []
    failures = []

    for subject in SUBJECTS:
        for session in SESSIONS:
            base = (
                f"{subject}/{session}/eeg/"
                f"{subject}_{session}_task-{TASK}_eeg"
            )
            source_path = base + ".vhdr"
            local_path = payload_dir / f"{subject}__{session}__{TASK}.vhdr"
            try:
                annex = _resolve_vhdr_annex(source_path)
                url = f"https://data.nemar.org/{NEMAR_MIRROR}/{source_path}"
                _download(url, local_path)

                observed_size = local_path.stat().st_size
                observed_md5 = _hash(local_path, "md5")
                if observed_size != int(annex["expected_size_bytes"]):
                    raise ValueError(
                        f"size mismatch {observed_size} != "
                        f"{annex['expected_size_bytes']}"
                    )
                if observed_md5 != str(annex["expected_md5"]):
                    raise ValueError(
                        f"MD5 mismatch {observed_md5} != "
                        f"{annex['expected_md5']}"
                    )

                header = _parse_vhdr(local_path)
                records.append({
                    "subject": subject,
                    "session": session,
                    "task": TASK,
                    "source_path": source_path,
                    "source_identity": {
                        **annex,
                        "observed_size_bytes": observed_size,
                        "observed_md5": observed_md5,
                        "sha256": _hash(local_path, "sha256"),
                        "source_url": url,
                    },
                    "number_of_channels": header["number_of_channels"],
                    "sampling_rate_hz": header["sampling_rate_hz"],
                    "binary_format": header["binary_format"],
                    "data_orientation": header["data_orientation"],
                    "channel_labels": header["channel_labels"],
                    "channel_signature": _signature(
                        header["channel_labels"]
                    ),
                })
            except Exception as exc:
                failures.append({
                    "subject": subject,
                    "session": session,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                })

    expected_records = len(SUBJECTS) * len(SESSIONS)
    if len(records) + len(failures) != expected_records:
        raise RuntimeError("audit accounting mismatch")

    labels_all = [record["channel_labels"] for record in records]
    all_intersection = _intersection(labels_all)
    all_union = _union(labels_all)

    by_session = {}
    for session in SESSIONS:
        subset = [
            record["channel_labels"]
            for record in records
            if record["session"] == session
        ]
        by_session[session] = {
            "record_count": len(subset),
            "intersection": _intersection(subset),
            "union": _union(subset),
        }

    signature_counts = Counter(record["channel_signature"] for record in records)
    signature_examples = {}
    for record in records:
        signature_examples.setdefault(
            record["channel_signature"],
            {
                "number_of_channels": record["number_of_channels"],
                "channel_labels": record["channel_labels"],
                "example_subject": record["subject"],
                "example_session": record["session"],
            },
        )

    variable_channels = []
    presence = {}
    for label in all_union:
        overall = sum(label in record["channel_labels"] for record in records)
        session_counts = {
            session: sum(
                label in record["channel_labels"]
                for record in records
                if record["session"] == session
            )
            for session in SESSIONS
        }
        presence[label] = {
            "overall_present": overall,
            "overall_records": len(records),
            "by_session": session_counts,
        }
        if overall != len(records):
            variable_channels.append(label)

    cpz_matrix = {
        subject: {
            session: next(
                (
                    "CPz" in record["channel_labels"]
                    for record in records
                    if record["subject"] == subject
                    and record["session"] == session
                ),
                None,
            )
            for session in SESSIONS
        }
        for subject in SUBJECTS
    }

    acquisition_anomalies = []
    for record in records:
        anomaly = {}
        if record["sampling_rate_hz"] != 500.0:
            anomaly["sampling_rate_hz"] = record["sampling_rate_hz"]
        if str(record["binary_format"]).upper() != "IEEE_FLOAT_32":
            anomaly["binary_format"] = record["binary_format"]
        if str(record["data_orientation"]).upper() != "MULTIPLEXED":
            anomaly["data_orientation"] = record["data_orientation"]
        if anomaly:
            acquisition_anomalies.append({
                "subject": record["subject"],
                "session": record["session"],
                **anomaly,
            })

    stable_old59 = [label for label in old_matched if label in all_intersection]
    old59_missing_from_stable = [
        label for label in old_matched if label not in all_intersection
    ]

    return {
        "schema": "NSD_DS004148_EYESCLOSED_HEADER_TOPOLOGY_AUDIT_V0_1",
        "status": (
            "HEADER_AUDIT_CLOSED"
            if not failures
            else "HEADER_AUDIT_INCOMPLETE"
        ),
        "source_release": {
            "public_git_repository": SOURCE_REPOSITORY,
            "public_git_commit": SOURCE_COMMIT,
            "nemar_mirror": NEMAR_MIRROR,
        },
        "task": TASK,
        "subject_count": len(SUBJECTS),
        "session_count_per_subject": len(SESSIONS),
        "expected_record_count": expected_records,
        "audited_record_count": len(records),
        "failure_count": len(failures),
        "failures": failures,
        "records": records,
        "unique_channel_signature_count": len(signature_counts),
        "channel_signatures": [
            {
                "signature": signature,
                "record_count": count,
                **signature_examples[signature],
            }
            for signature, count in sorted(
                signature_counts.items(),
                key=lambda item: (-item[1], item[0]),
            )
        ],
        "all_record_intersection": all_intersection,
        "all_record_intersection_count": len(all_intersection),
        "all_record_union": all_union,
        "all_record_union_count": len(all_union),
        "by_session": by_session,
        "variable_channels": variable_channels,
        "channel_presence": presence,
        "cpz_presence_matrix": cpz_matrix,
        "old_matched_reference_channel_count": len(old_matched),
        "stable_intersection_with_old_matched_reference": stable_old59,
        "stable_intersection_with_old_matched_reference_count": len(stable_old59),
        "old_matched_labels_not_dataset_stable": old59_missing_from_stable,
        "acquisition_anomalies": acquisition_anomalies,
        "claim_ceiling": (
            "source/header topology only; no EEG feature, spectral, modal, "
            "chi, capital-Chi, clinical, recovery, or population result"
        ),
    }


def _write_summary(result: dict[str, object], path: Path) -> None:
    lines = [
        "# ds004148 eyes-closed dataset-wide header topology audit",
        "",
        f"Status: {result['status']}",
        f"Audited records: {result['audited_record_count']} / "
        f"{result['expected_record_count']}",
        f"Unique channel signatures: "
        f"{result['unique_channel_signature_count']}",
        f"All-record channel intersection: "
        f"{result['all_record_intersection_count']}",
        f"Old 59-label reference labels stable across all records: "
        f"{result['stable_intersection_with_old_matched_reference_count']}",
        f"Old matched labels not dataset-stable: "
        f"{result['old_matched_labels_not_dataset_stable']}",
        f"Variable channels: {result['variable_channels']}",
        "",
        "## Session intersections",
    ]
    for session, data in result["by_session"].items():
        lines.append(
            f"- {session}: records={data['record_count']}; "
            f"intersection_n={len(data['intersection'])}; "
            f"union_n={len(data['union'])}"
        )

    lines += ["", "## Channel signatures"]
    for signature in result["channel_signatures"]:
        lines.append(
            f"- n={signature['record_count']}; "
            f"channels={signature['number_of_channels']}; "
            f"example={signature['example_subject']} "
            f"{signature['example_session']}"
        )

    if result["failures"]:
        lines += ["", "## Failures"]
        for failure in result["failures"]:
            lines.append(
                f"- {failure['subject']} {failure['session']}: "
                f"{failure['error_type']}: {failure['error']}"
            )

    lines += [
        "",
        "No EEG signal-derived outcome was opened by this audit.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matched-reference", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    result = execute(args.matched_reference, args.output_dir)
    result_path = (
        args.output_dir
        / "ds004148_eyesclosed_header_topology_audit_v0.1.json"
    )
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_summary(result, args.output_dir / "VERIFY_SUMMARY.md")

    failure_types = Counter(item["error_type"] for item in result["failures"])
    print(json.dumps({
        "status": result["status"],
        "audited_record_count": result["audited_record_count"],
        "failure_count": result["failure_count"],
        "failure_types": dict(failure_types),
        "failure_examples": result["failures"][:10],
        "unique_channel_signature_count": result[
            "unique_channel_signature_count"
        ],
        "all_record_intersection_count": result[
            "all_record_intersection_count"
        ],
        "stable_old59_count": result[
            "stable_intersection_with_old_matched_reference_count"
        ],
        "old59_unstable": result[
            "old_matched_labels_not_dataset_stable"
        ],
    }, indent=2, sort_keys=True))

    return 0 if not result["failures"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
