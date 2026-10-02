#!/usr/bin/env python3
"""Extract one frozen ds003775 repeat subject from the exact release manifest.

The full release manifest is generated from the pinned public Git/NEMAR release.
This helper converts one nested subject record into the pair-manifest contract
already consumed by the D4, PSD, and descriptive-parameterization tools.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def extract(release_manifest_path: Path, subject_id: str) -> dict[str, object]:
    release = json.loads(release_manifest_path.read_text(encoding="utf-8"))
    if release.get("dataset") != "ds003775":
        raise ValueError("release manifest is not ds003775")

    matches = [
        item for item in release.get("subjects", [])
        if str(item.get("subject_id")) == subject_id
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one record for {subject_id}, found {len(matches)}")

    contract = dict(release["acquisition_contract"])
    sessions = list(matches[0]["sessions"])
    if {str(item.get("session_id")) for item in sessions} != {"ses-t1", "ses-t2"}:
        raise ValueError(f"{subject_id} does not contain exactly ses-t1 and ses-t2")

    return {
        "dataset": "ds003775",
        "manifest_version": "0.1-extracted-from-exact-release",
        "source_release": release["source_release"],
        "release_manifest_sha256": release.get("canonical_body_sha256"),
        "subject_id": subject_id,
        "task": contract["task"],
        "expected_signal_count": int(contract["signal_count"]),
        "expected_duration_seconds": float(contract["recording_duration_seconds"]),
        "expected_sampling_rate_hz": float(contract["sampling_rate_hz"]),
        "expected_channel_labels": list(contract["channel_labels"]),
        "recordings": sessions,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("release_manifest", type=Path)
    parser.add_argument("subject_id")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = extract(args.release_manifest, args.subject_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "subject_id": result["subject_id"],
        "recording_count": len(result["recordings"]),
        "release_manifest_sha256": result["release_manifest_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
