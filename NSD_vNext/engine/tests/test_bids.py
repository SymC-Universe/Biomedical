import json
from pathlib import Path

from nsd_engine.bids import audit_bids_tree, parse_bids_entities


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_description(root: Path) -> None:
    write_text(
        root / "dataset_description.json",
        json.dumps(
            {
                "Name": "fixture",
                "BIDSVersion": "1.9.0",
                "License": "CC0",
                "DatasetDOI": "10.example/fixture",
            }
        ),
    )


def test_parse_bids_entities_from_path():
    entities = parse_bids_entities(
        "sub-01/ses-02/eeg/sub-01_ses-02_task-rest_run-03_eeg.set"
    )
    assert entities == {"sub": "01", "ses": "02", "task": "rest", "run": "03"}


def test_single_session_dataset_without_ses_directories_is_valid(tmp_path):
    make_description(tmp_path)
    write_text(tmp_path / "participants.tsv", "participant_id\tgroup\nsub-01\tcontrol\n")
    write_text(tmp_path / "sub-01/eeg/sub-01_task-rest_eeg.set", "LFS pointer fixture")
    write_text(tmp_path / "sub-01/eeg/sub-01_task-rest_channels.tsv", "name\ttype\nCz\tEEG\n")
    write_text(tmp_path / "sub-01/eeg/sub-01_task-rest_eeg.json", "{}")

    audit = audit_bids_tree(tmp_path)
    assert audit.subject_identity_verified
    assert audit.hierarchy_structurally_consistent
    assert audit.explicit_session_count == 0
    assert audit.subjects_with_multiple_sessions == ()
    assert audit.task_labels == ("rest",)
    assert audit.eeg_file_count == 1
    assert audit.scan_session_metadata_complete is None


def test_repeat_sessions_are_counted_and_joined_to_one_subject(tmp_path):
    make_description(tmp_path)
    write_text(tmp_path / "participants.tsv", "participant_id\nsub-01\n")
    write_text(
        tmp_path / "sub-01/sub-01_sessions.tsv",
        "session_id\n" "ses-t1\n" "ses-t2\n",
    )
    for session in ("ses-t1", "ses-t2"):
        write_text(
            tmp_path / f"sub-01/{session}/eeg/sub-01_{session}_task-rest_eeg.set",
            "LFS pointer fixture",
        )

    audit = audit_bids_tree(tmp_path)
    assert audit.explicit_session_count == 2
    assert audit.subjects_with_multiple_sessions == ("sub-01",)
    assert audit.sessions_tsv_count == 1
    assert audit.sessions_table_issues == ()
    assert audit.hierarchy_structurally_consistent


def test_sessions_table_mismatch_is_detected(tmp_path):
    make_description(tmp_path)
    write_text(tmp_path / "participants.tsv", "participant_id\nsub-01\n")
    write_text(tmp_path / "sub-01/sub-01_sessions.tsv", "session_id\nses-t1\n")
    write_text(
        tmp_path / "sub-01/ses-t2/eeg/sub-01_ses-t2_task-rest_eeg.set",
        "LFS pointer fixture",
    )

    audit = audit_bids_tree(tmp_path)
    assert not audit.hierarchy_structurally_consistent
    assert any("session mismatch" in issue for issue in audit.sessions_table_issues)


def test_participant_tree_mismatch_is_detected(tmp_path):
    make_description(tmp_path)
    write_text(
        tmp_path / "participants.tsv",
        "participant_id\nsub-01\nsub-02\n",
    )
    write_text(tmp_path / "sub-01/eeg/sub-01_task-rest_eeg.set", "pointer")

    audit = audit_bids_tree(tmp_path)
    assert not audit.subject_identity_verified
    assert audit.participants_missing_from_tree == ("sub-02",)


def test_duplicate_participant_rows_are_detected(tmp_path):
    make_description(tmp_path)
    write_text(
        tmp_path / "participants.tsv",
        "participant_id\nsub-01\nsub-01\n",
    )
    write_text(tmp_path / "sub-01/eeg/sub-01_task-rest_eeg.set", "pointer")

    audit = audit_bids_tree(tmp_path)
    assert audit.duplicate_participant_ids == ("sub-01",)
    assert not audit.subject_identity_verified


def test_scans_table_reports_complete_session_labels(tmp_path):
    make_description(tmp_path)
    write_text(tmp_path / "participants.tsv", "participant_id\nsub-01\n")
    write_text(tmp_path / "sub-01/eeg/sub-01_task-rest_run-01_eeg.set", "pointer")
    write_text(
        tmp_path / "sub-01/sub-01_scans.tsv",
        "filename\tsession\n"
        "eeg/sub-01_task-rest_run-01_eeg.set\tday1\n",
    )

    audit = audit_bids_tree(tmp_path)
    assert audit.scans_tsv_count == 1
    assert audit.scans_row_count == 1
    assert audit.scans_rows_with_session == 1
    assert audit.scans_rows_without_session == 0
    assert audit.scan_session_labels == ("day1",)
    assert audit.scan_session_metadata_complete is True


def test_scans_table_preserves_unresolved_session_rows(tmp_path):
    make_description(tmp_path)
    write_text(tmp_path / "participants.tsv", "participant_id\nsub-01\n")
    write_text(tmp_path / "sub-01/eeg/sub-01_task-rest_run-01_eeg.set", "pointer")
    write_text(tmp_path / "sub-01/eeg/sub-01_task-rest_run-02_eeg.set", "pointer")
    write_text(
        tmp_path / "sub-01/sub-01_scans.tsv",
        "filename\tsession\n"
        "eeg/sub-01_task-rest_run-01_eeg.set\tn/a\n"
        "eeg/sub-01_task-rest_run-02_eeg.set\t\n",
    )

    audit = audit_bids_tree(tmp_path)
    assert audit.scans_tsv_count == 1
    assert audit.scans_row_count == 2
    assert audit.scans_rows_with_session == 0
    assert audit.scans_rows_without_session == 2
    assert audit.scan_session_labels == ()
    assert audit.scan_session_metadata_complete is False
