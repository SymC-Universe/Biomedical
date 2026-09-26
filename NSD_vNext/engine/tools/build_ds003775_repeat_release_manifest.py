#!/usr/bin/env python3
"""Build an exact release manifest for the frozen ds003775 repeat cohort.

The script reads only the pinned public Git metadata tree and text sidecars. It
resolves git-annex symlink targets to obtain payload size/MD5 identities before
any EDF is downloaded. It also audits scans timestamps, EEG sidecars, and
channel tables for the 42-subject repeat cohort.

This is provenance infrastructure, not signal analysis.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import urllib.request


REPO = "nemarDatasets/on003775"
REF = "v1.0.0"
DATA_BASE = "https://data.nemar.org/on003775/v1.0.0"
ANNEX_RE = re.compile(r"MD5E-s(?P<size>\d+)--(?P<md5>[0-9a-f]{32})\.edf")


def _request_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def _tree() -> dict[str, dict[str, object]]:
    url = f"https://api.github.com/repos/{REPO}/git/trees/{REF}?recursive=1"
    payload = _request_json(url)
    if not isinstance(payload, dict) or payload.get("truncated"):
        raise RuntimeError("pinned Git tree could not be retrieved completely")
    entries = payload.get("tree")
    if not isinstance(entries, list):
        raise RuntimeError("Git tree response has no tree list")
    return {str(item["path"]): item for item in entries if isinstance(item, dict)}


def _blob_text(sha: str) -> str:
    payload = _request_json(f"https://api.github.com/repos/{REPO}/git/blobs/{sha}")
    if not isinstance(payload, dict) or payload.get("encoding") != "base64":
        raise RuntimeError(f"unexpected blob response for {sha}")
    raw = base64.b64decode(str(payload["content"]).replace("\n", ""))
    return raw.decode("utf-8")


def _entry_text(tree: dict[str, dict[str, object]], path: str) -> str:
    entry = tree.get(path)
    if entry is None:
        raise FileNotFoundError(f"pinned tree missing {path}")
    return _blob_text(str(entry["sha"]))


def _annex_identity(pointer: str) -> tuple[int, str]:
    match = ANNEX_RE.search(pointer)
    if match is None:
        raise ValueError(f"could not parse git-annex EDF identity from pointer {pointer!r}")
    return int(match.group("size")), match.group("md5")


def _scans_acq_time(text: str, expected_filename: str) -> str:
    rows = csv.DictReader(io.StringIO(text), delimiter="\t")
    hits = [row for row in rows if row.get("filename") == expected_filename]
    if len(hits) != 1:
        raise ValueError(f"expected exactly one scans.tsv row for {expected_filename}, found {len(hits)}")
    value = str(hits[0].get("acq_time", "")).strip()
    if not value or value.lower() == "n/a":
        raise ValueError(f"missing acquisition time for {expected_filename}")
    return value


def _channels(text: str) -> tuple[str, ...]:
    rows = csv.DictReader(io.StringIO(text), delimiter="\t")
    names = tuple(str(row.get("name", "")).strip() for row in rows)
    if not names or any(not name for name in names):
        raise ValueError("channel table contains missing names")
    if len(set(names)) != len(names):
        raise ValueError("channel table contains duplicate channel names")
    return names


def build(index_path: Path) -> dict[str, object]:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    subjects = [str(value) for value in index["subjects"]]
    if len(subjects) != int(index["repeat_subject_count"]):
        raise ValueError("repeat subject count does not match frozen index")
    if len(set(subjects)) != len(subjects):
        raise ValueError("repeat subject index contains duplicates")

    tree = _tree()
    records: list[dict[str, object]] = []
    reference_channels: tuple[str, ...] | None = None
    reference_sampling: float | None = None
    reference_duration: float | None = None

    for subject in subjects:
        subject_record: dict[str, object] = {"subject_id": subject, "sessions": []}
        for session in ("ses-t1", "ses-t2"):
            stem = f"{subject}_{session}_task-resteyesc"
            eeg_rel = f"{subject}/{session}/eeg/{stem}_eeg.edf"
            scans_rel = f"{subject}/{session}/{subject}_{session}_scans.tsv"
            eeg_json_rel = f"{subject}/{session}/eeg/{stem}_eeg.json"
            channels_rel = f"{subject}/{session}/eeg/{stem}_channels.tsv"

            size_bytes, md5 = _annex_identity(_entry_text(tree, eeg_rel))
            acq_time = _scans_acq_time(_entry_text(tree, scans_rel), f"eeg/{stem}_eeg.edf")
            eeg_json = json.loads(_entry_text(tree, eeg_json_rel))
            sampling = float(eeg_json["SamplingFrequency"])
            duration = float(eeg_json["RecordingDuration"])
            channel_names = _channels(_entry_text(tree, channels_rel))

            if reference_channels is None:
                reference_channels = channel_names
                reference_sampling = sampling
                reference_duration = duration
            else:
                if channel_names != reference_channels:
                    raise ValueError(f"channel order differs for {subject} {session}")
                if sampling != reference_sampling:
                    raise ValueError(f"sampling frequency differs for {subject} {session}")
                if duration != reference_duration:
                    raise ValueError(f"recording duration differs for {subject} {session}")

            subject_record["sessions"].append(
                {
                    "session_id": session,
                    "acquisition_time": acq_time,
                    "relative_path": eeg_rel,
                    "download_url": f"{DATA_BASE}/{eeg_rel}",
                    "expected_size_bytes": size_bytes,
                    "expected_md5": md5,
                }
            )
        records.append(subject_record)

    assert reference_channels is not None
    assert reference_sampling is not None
    assert reference_duration is not None
    body: dict[str, object] = {
        "dataset": "ds003775",
        "manifest_version": "0.1-generated",
        "source_release": {
            "nemar_repo": REPO,
            "nemar_ref": REF,
            "openneuro_doi": "10.18112/openneuro.ds003775.v1.2.1",
        },
        "scope": "exact pinned-release identities for the frozen 42-subject repeat cohort",
        "subject_count": len(records),
        "recording_count": sum(len(item["sessions"]) for item in records),
        "acquisition_contract": {
            "task": "resteyesc",
            "signal_count": len(reference_channels),
            "channel_labels": list(reference_channels),
            "sampling_rate_hz": reference_sampling,
            "recording_duration_seconds": reference_duration,
        },
        "subjects": records,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    body["canonical_body_sha256"] = hashlib.sha256(canonical).hexdigest()
    return body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.index)
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
