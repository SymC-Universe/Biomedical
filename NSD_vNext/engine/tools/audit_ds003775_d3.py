#!/usr/bin/env python3
"""Close the ds003775 D3 metadata/join gate against the pinned public release.

This audit is intentionally metadata-only. It verifies participant-to-BIDS
subject identity, reviewed metadata-role completeness, participant-table
missingness, and the structural-engine visibility firewall. It does not inspect
EEG samples and therefore cannot promote D4 or D5.
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
SUBJECT_RE = re.compile(r"^(sub-[^/]+)(?:/|$)")
MISSING = {"", "n/a", "na", "nan", "none", "null"}
ENGINE_VISIBLE = {"identity", "acquisition", "recording_state"}


def _request_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def _tree() -> dict[str, dict[str, object]]:
    payload = _request_json(
        f"https://api.github.com/repos/{REPO}/git/trees/{REF}?recursive=1"
    )
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


def _normalized(value: object) -> str | None:
    text = "" if value is None else str(value).strip()
    return None if text.lower() in MISSING else text


def build(manifest_path: Path) -> dict[str, object]:
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    roles = dict(manifest["roles"])

    tree = _tree()
    participant_entry = tree.get("participants.tsv")
    if participant_entry is None:
        raise FileNotFoundError("pinned tree missing participants.tsv")
    participant_text = _blob_text(str(participant_entry["sha"]))

    reader = csv.DictReader(io.StringIO(participant_text), delimiter="\t")
    header = tuple(reader.fieldnames or ())
    rows = list(reader)
    participant_ids = [str(row.get("participant_id", "")).strip() for row in rows]

    bids_subjects = sorted(
        {
            match.group(1)
            for path in tree
            for match in [SUBJECT_RE.match(path)]
            if match is not None
        }
    )

    duplicate_ids = sorted(
        {value for value in participant_ids if participant_ids.count(value) > 1}
    )
    participant_set = set(participant_ids)
    bids_set = set(bids_subjects)
    participant_only = sorted(participant_set - bids_set)
    bids_only = sorted(bids_set - participant_set)

    missingness: dict[str, dict[str, float | int]] = {}
    for column in header:
        missing_count = sum(_normalized(row.get(column)) is None for row in rows)
        missingness[column] = {
            "missing_count": missing_count,
            "row_count": len(rows),
            "missing_fraction": (missing_count / len(rows)) if rows else 0.0,
        }

    manifest_columns = set(roles)
    header_set = set(header)
    unreviewed_columns = sorted(header_set - manifest_columns)
    manifest_only_columns = sorted(manifest_columns - header_set)

    engine_visible_participant_columns = [
        column for column in header if roles.get(column) in ENGINE_VISIBLE
    ]
    expected_engine_columns = list(manifest["structural_engine_participant_columns"])

    join_contract = dict(manifest["join_contract"])
    pass_conditions = {
        "participant_count_matches_bids_subject_count": len(rows) == len(bids_subjects),
        "no_duplicate_participant_ids": not duplicate_ids,
        "no_participant_only_ids": not participant_only,
        "no_bids_only_ids": not bids_only,
        "all_participant_columns_reviewed": not unreviewed_columns,
        "manifest_has_no_stale_columns": not manifest_only_columns,
        "engine_visibility_matches_frozen_manifest": (
            engine_visible_participant_columns == expected_engine_columns
        ),
        "silent_first_match_disabled": (
            join_contract.get("silent_first_match_allowed") is False
        ),
    }
    passed = all(pass_conditions.values())

    body: dict[str, object] = {
        "dataset": "ds003775",
        "gate": "D3_METADATA_JOIN_VERIFIED",
        "source_release": {
            "nemar_repo": REPO,
            "nemar_ref": REF,
            "openneuro_doi": manifest["source_release"]["openneuro_doi"],
        },
        "participant_row_count": len(rows),
        "bids_subject_count": len(bids_subjects),
        "duplicate_participant_ids": duplicate_ids,
        "participant_only_ids": participant_only,
        "bids_only_ids": bids_only,
        "participant_columns": list(header),
        "unreviewed_columns": unreviewed_columns,
        "manifest_only_columns": manifest_only_columns,
        "engine_visible_participant_columns": engine_visible_participant_columns,
        "expected_engine_visible_participant_columns": expected_engine_columns,
        "missingness": missingness,
        "role_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "pass_conditions": pass_conditions,
        "status": "PASS" if passed else "FAIL",
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    body["canonical_body_sha256"] = hashlib.sha256(canonical).hexdigest()
    return body


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.manifest)
    payload = json.dumps(result, indent=2, sort_keys=True)
    print(payload)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
