#!/usr/bin/env python3
"""Audit the structural BIDS hierarchy of a checked-out public dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from nsd_engine.bids import audit_bids_tree


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, help="Checked-out BIDS dataset root")
    parser.add_argument("--output", type=Path, required=True, help="JSON output path")
    args = parser.parse_args()

    audit = audit_bids_tree(args.root)
    payload = audit.to_dict()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"dataset_name={payload['dataset_name']}")
    print(f"dataset_doi={payload['dataset_doi']}")
    print(f"bids_version={payload['bids_version']}")
    print(f"license={payload['license']}")
    print(f"participant_rows={payload['participant_rows']}")
    print("participant_columns=" + ",".join(payload["participant_columns"]))
    print(f"tree_subject_count={payload['tree_subject_count']}")
    print("duplicate_participant_ids=" + ",".join(payload["duplicate_participant_ids"]))
    print("participants_missing_from_tree=" + ",".join(payload["participants_missing_from_tree"]))
    print("tree_subjects_missing_from_participants=" + ",".join(payload["tree_subjects_missing_from_participants"]))
    print(f"subject_identity_verified={payload['subject_identity_verified']}")
    print(f"explicit_session_count={payload['explicit_session_count']}")
    print(
        "subjects_with_multiple_sessions_count="
        f"{payload['subjects_with_multiple_sessions_count']}"
    )
    print(
        "subjects_with_multiple_sessions="
        + ",".join(payload["subjects_with_multiple_sessions"])
    )
    print("task_labels=" + ",".join(payload["task_labels"]))
    print("run_labels=" + ",".join(payload["run_labels"]))
    print(f"eeg_file_count={payload['eeg_file_count']}")
    print(f"events_tsv_count={payload['events_tsv_count']}")
    print(f"channels_tsv_count={payload['channels_tsv_count']}")
    print(f"eeg_json_count={payload['eeg_json_count']}")
    print(f"sessions_tsv_count={payload['sessions_tsv_count']}")
    print(f"sessions_table_issues={len(payload['sessions_table_issues'])}")
    for issue in payload["sessions_table_issues"]:
        print(f"session_issue={issue}")
    print(f"hierarchy_structurally_consistent={payload['hierarchy_structurally_consistent']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
