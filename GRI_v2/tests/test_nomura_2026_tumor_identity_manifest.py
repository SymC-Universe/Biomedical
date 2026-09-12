from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


_PATH = (
    Path(__file__).resolve().parents[1]
    / "config"
    / "gri_nomura_2026_tumor_identity_manifest_p0d.json"
)


def _data():
    with _PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_nomura_manifest_reproduces_paper_cohort_arithmetic():
    data = _data()
    samples = data["samples"]
    assert len(samples) == 36
    groups = defaultdict(list)
    for row in samples:
        groups[row["patient_group"]].append(row)
    assert len(groups) == 19
    matched = {key: rows for key, rows in groups.items() if len(rows) > 1}
    unmatched = {key: rows for key, rows in groups.items() if len(rows) == 1}
    assert len(matched) == 15
    assert sum(len(rows) for rows in matched.values()) == 32
    assert len(unmatched) == 4


def test_manifest_gsm_and_tumor_ids_are_unique():
    samples = _data()["samples"]
    assert len({row["gsm"] for row in samples}) == 36
    assert len({row["tumor_id"] for row in samples}) == 36


def test_group_size_field_matches_reconstructed_group_size():
    samples = _data()["samples"]
    counts = Counter(row["patient_group"] for row in samples)
    for row in samples:
        assert row["group_size"] == counts[row["patient_group"]]


def test_three_tumor_groups_are_preserved():
    data = _data()
    assert data["matched_groups"]["SM15"] == ["SM15P", "SM15R", "SM15R2"]
    assert data["matched_groups"]["TK19"] == ["TK19P", "TK19R", "TK19R2"]
    assert data["summary"]["groups_with_three_tumors"] == 2


def test_recurrence_only_longitudinal_groups_are_not_rewritten_as_primary_pairs():
    data = _data()
    for group in ("MD03", "SM10", "TK16", "TK17"):
        assert all(not tumor.endswith("P") for tumor in data["matched_groups"][group])
    assert data["firewalls"]["P_IS_NOT_ASSUMED_FOR_EVERY_LONGITUDINAL_GROUP"] is True
    assert data["firewalls"]["EARLIEST_AVAILABLE_IS_NOT_AUTOMATICALLY_PRIMARY"] is True


def test_unmatched_singletons_are_not_forced_into_pairs():
    data = _data()
    assert data["unmatched_singletons"] == ["SM16P", "TKU3197", "TK18R", "TKU3095"]


def test_source_manifest_remains_p0d_and_outcome_blind():
    data = _data()
    assert data["status"] == "P0_D_SOURCE_IDENTITY_MANIFEST"
    assert data["firewalls"]["NO_MOLECULAR_OUTCOME_VALUES_READ"] is True
    assert data["firewalls"]["NO_P1_SELECTION"] is True
