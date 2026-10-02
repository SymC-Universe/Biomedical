"""Dependency-free BIDS hierarchy/provenance audit helpers for NSD vNext.

The auditor is intentionally structural. It does not load EEG signal arrays and
it does not inspect clinical labels beyond reporting metadata columns. Its job
is to establish whether subject/session/run/task identities can be recovered
without guesswork before any scientific feature extraction begins.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Iterable


_ENTITY_RE = re.compile(r"(?:^|_)(sub|ses|task|acq|run|recording|proc)-([^_/]+)")
_MISSING_TOKENS = {"", "n/a", "na", "nan", "none", "null"}


def parse_bids_entities(path: str | Path) -> dict[str, str]:
    """Parse common BIDS entities from a relative path or filename."""
    text = str(path).replace("\\", "/")
    entities: dict[str, str] = {}
    for key, value in _ENTITY_RE.findall(text):
        entities.setdefault(key, value)
    return entities


def _read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def _duplicates(values: Iterable[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    dup: set[str] = set()
    for value in values:
        if value in seen:
            dup.add(value)
        seen.add(value)
    return tuple(sorted(dup))


def _present(value: str | None) -> bool:
    return value is not None and value.strip().lower() not in _MISSING_TOKENS


@dataclass(frozen=True)
class BidsHierarchyAudit:
    dataset_name: str | None
    dataset_doi: str | None
    bids_version: str | None
    license: str | None
    participant_rows: int
    participant_ids: tuple[str, ...]
    duplicate_participant_ids: tuple[str, ...]
    participant_columns: tuple[str, ...]
    tree_subject_ids: tuple[str, ...]
    participants_missing_from_tree: tuple[str, ...]
    tree_subjects_missing_from_participants: tuple[str, ...]
    explicit_session_count: int
    subjects_with_multiple_sessions: tuple[str, ...]
    sessions_by_subject: tuple[tuple[str, tuple[str, ...]], ...]
    task_labels: tuple[str, ...]
    run_labels: tuple[str, ...]
    eeg_file_count: int
    events_tsv_count: int
    channels_tsv_count: int
    eeg_json_count: int
    scans_tsv_count: int
    scans_row_count: int
    scans_rows_with_session: int
    scans_rows_without_session: int
    scan_session_labels: tuple[str, ...]
    sessions_tsv_count: int
    sessions_table_issues: tuple[str, ...]

    @property
    def subject_identity_verified(self) -> bool:
        return (
            self.participant_rows > 0
            and not self.duplicate_participant_ids
            and not self.participants_missing_from_tree
            and not self.tree_subjects_missing_from_participants
        )

    @property
    def hierarchy_structurally_consistent(self) -> bool:
        return self.subject_identity_verified and not self.sessions_table_issues

    @property
    def scan_session_metadata_complete(self) -> bool | None:
        """Whether all scan rows carry non-missing session labels.

        None means the dataset has no scans.tsv rows, so no inference about scan
        session completeness is possible from this field.
        """
        if self.scans_row_count == 0:
            return None
        return self.scans_rows_without_session == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "dataset_doi": self.dataset_doi,
            "bids_version": self.bids_version,
            "license": self.license,
            "participant_rows": self.participant_rows,
            "participant_ids": list(self.participant_ids),
            "duplicate_participant_ids": list(self.duplicate_participant_ids),
            "participant_columns": list(self.participant_columns),
            "tree_subject_count": len(self.tree_subject_ids),
            "tree_subject_ids": list(self.tree_subject_ids),
            "participants_missing_from_tree": list(self.participants_missing_from_tree),
            "tree_subjects_missing_from_participants": list(self.tree_subjects_missing_from_participants),
            "explicit_session_count": self.explicit_session_count,
            "subjects_with_multiple_sessions_count": len(self.subjects_with_multiple_sessions),
            "subjects_with_multiple_sessions": list(self.subjects_with_multiple_sessions),
            "sessions_by_subject": {subject: list(sessions) for subject, sessions in self.sessions_by_subject},
            "task_labels": list(self.task_labels),
            "run_labels": list(self.run_labels),
            "eeg_file_count": self.eeg_file_count,
            "events_tsv_count": self.events_tsv_count,
            "channels_tsv_count": self.channels_tsv_count,
            "eeg_json_count": self.eeg_json_count,
            "scans_tsv_count": self.scans_tsv_count,
            "scans_row_count": self.scans_row_count,
            "scans_rows_with_session": self.scans_rows_with_session,
            "scans_rows_without_session": self.scans_rows_without_session,
            "scan_session_labels": list(self.scan_session_labels),
            "scan_session_metadata_complete": self.scan_session_metadata_complete,
            "sessions_tsv_count": self.sessions_tsv_count,
            "sessions_table_issues": list(self.sessions_table_issues),
            "subject_identity_verified": self.subject_identity_verified,
            "hierarchy_structurally_consistent": self.hierarchy_structurally_consistent,
        }


def audit_bids_tree(root: str | Path) -> BidsHierarchyAudit:
    """Audit a checked-out BIDS dataset without loading signal data."""
    root_path = Path(root)
    if not root_path.is_dir():
        raise ValueError(f"BIDS root does not exist or is not a directory: {root_path}")

    description_path = root_path / "dataset_description.json"
    description = _read_json(description_path) if description_path.exists() else {}

    participants_path = root_path / "participants.tsv"
    participants = _read_tsv(participants_path) if participants_path.exists() else []
    participant_columns = tuple(participants[0].keys()) if participants else ()
    participant_ids = tuple(
        row.get("participant_id", "").strip() for row in participants if row.get("participant_id", "").strip()
    )
    duplicate_participant_ids = _duplicates(participant_ids)

    tree_subject_ids = tuple(sorted(path.name for path in root_path.glob("sub-*") if path.is_dir()))
    participant_set = set(participant_ids)
    tree_subject_set = set(tree_subject_ids)

    sessions: dict[str, set[str]] = {subject: set() for subject in tree_subject_ids}
    tasks: set[str] = set()
    runs: set[str] = set()
    eeg_file_count = 0
    events_tsv_count = 0
    channels_tsv_count = 0
    eeg_json_count = 0

    for subject in tree_subject_ids:
        subject_path = root_path / subject
        explicit_session_dirs = [p for p in subject_path.glob("ses-*") if p.is_dir()]
        for session_dir in explicit_session_dirs:
            sessions[subject].add(session_dir.name)

        for path in subject_path.rglob("*"):
            # OpenNeuro mirrors can contain git-annex/LFS-style symlinks whose
            # targets are intentionally absent in metadata-only checkouts. The
            # path still represents a BIDS data file and must be counted.
            if not path.is_file() and not path.is_symlink():
                continue
            relative = path.relative_to(root_path)
            entities = parse_bids_entities(relative)
            if "ses" in entities:
                sessions[subject].add(f"ses-{entities['ses']}")
            if "task" in entities:
                tasks.add(entities["task"])
            if "run" in entities:
                runs.add(entities["run"])

            lower = path.name.lower()
            if any(
                lower.endswith(suffix)
                for suffix in ("_eeg.set", "_eeg.edf", "_eeg.bdf", "_eeg.vhdr", "_eeg.eeg", "_eeg.fif")
            ):
                eeg_file_count += 1
            if lower.endswith("_events.tsv"):
                events_tsv_count += 1
            if lower.endswith("_channels.tsv"):
                channels_tsv_count += 1
            if lower.endswith("_eeg.json"):
                eeg_json_count += 1

    # BIDS scans tables can preserve acquisition/session information even when
    # directory entities are incomplete. Audit them separately rather than
    # inferring that run labels are sessions.
    scans_tsv_paths = sorted(root_path.rglob("*_scans.tsv"))
    scans_row_count = 0
    scans_rows_with_session = 0
    scans_rows_without_session = 0
    scan_session_labels: set[str] = set()
    for scans_path in scans_tsv_paths:
        rows = _read_tsv(scans_path)
        scans_row_count += len(rows)
        for row in rows:
            session_value = row.get("session")
            if _present(session_value):
                value = session_value.strip()
                scans_rows_with_session += 1
                scan_session_labels.add(value)
            else:
                scans_rows_without_session += 1

    sessions_tsv_paths = sorted(root_path.rglob("*_sessions.tsv"))
    sessions_table_issues: list[str] = []
    for sessions_path in sessions_tsv_paths:
        rows = _read_tsv(sessions_path)
        subject_entity = parse_bids_entities(sessions_path.relative_to(root_path)).get("sub")
        subject = f"sub-{subject_entity}" if subject_entity else None
        session_ids = [row.get("session_id", "").strip() for row in rows]
        if not subject:
            sessions_table_issues.append(f"cannot infer subject for {sessions_path.relative_to(root_path)}")
            continue
        if subject not in sessions:
            sessions_table_issues.append(f"sessions table references unknown subject {subject}")
            continue
        duplicates = _duplicates(value for value in session_ids if value)
        if duplicates:
            sessions_table_issues.append(f"duplicate session_id in {sessions_path.relative_to(root_path)}: {duplicates}")
        declared = {value for value in session_ids if value}
        observed = sessions[subject]
        if declared and observed and declared != observed:
            sessions_table_issues.append(
                f"session mismatch for {subject}: table={sorted(declared)} tree={sorted(observed)}"
            )

    sessions_by_subject = tuple(
        (subject, tuple(sorted(values))) for subject, values in sorted(sessions.items())
    )
    subjects_with_multiple_sessions = tuple(
        subject for subject, values in sessions_by_subject if len(values) > 1
    )
    explicit_session_count = sum(len(values) for _, values in sessions_by_subject)

    return BidsHierarchyAudit(
        dataset_name=description.get("Name"),
        dataset_doi=description.get("DatasetDOI"),
        bids_version=description.get("BIDSVersion"),
        license=description.get("License"),
        participant_rows=len(participants),
        participant_ids=participant_ids,
        duplicate_participant_ids=duplicate_participant_ids,
        participant_columns=participant_columns,
        tree_subject_ids=tree_subject_ids,
        participants_missing_from_tree=tuple(sorted(participant_set - tree_subject_set)),
        tree_subjects_missing_from_participants=tuple(sorted(tree_subject_set - participant_set)),
        explicit_session_count=explicit_session_count,
        subjects_with_multiple_sessions=subjects_with_multiple_sessions,
        sessions_by_subject=sessions_by_subject,
        task_labels=tuple(sorted(tasks)),
        run_labels=tuple(sorted(runs)),
        eeg_file_count=eeg_file_count,
        events_tsv_count=events_tsv_count,
        channels_tsv_count=channels_tsv_count,
        eeg_json_count=eeg_json_count,
        scans_tsv_count=len(scans_tsv_paths),
        scans_row_count=scans_row_count,
        scans_rows_with_session=scans_rows_with_session,
        scans_rows_without_session=scans_rows_without_session,
        scan_session_labels=tuple(sorted(scan_session_labels)),
        sessions_tsv_count=len(sessions_tsv_paths),
        sessions_table_issues=tuple(sessions_table_issues),
    )
