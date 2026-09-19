import pytest

from nsd_engine import (
    HierarchyKey,
    assert_subject_disjoint,
    audit_duplicate_hierarchy,
    audit_join,
)


def test_duplicate_hierarchy_is_detected():
    key = HierarchyKey("s1", "ses1", "run1")
    audit = audit_duplicate_hierarchy([key, HierarchyKey("s1", "ses2"), key])
    assert not audit.passed
    assert audit.duplicate_keys == (key,)


def test_unique_hierarchy_passes():
    audit = audit_duplicate_hierarchy([
        HierarchyKey("s1", "ses1"),
        HierarchyKey("s1", "ses2"),
        HierarchyKey("s2", "ses1"),
    ])
    assert audit.passed


def test_join_reports_unmatched_without_inventing_metadata():
    audit = audit_join(
        [{"subject": "s1", "session": "a"}, {"subject": "s2", "session": "a"}],
        [{"subject": "s1", "session": "a", "dx": "control"}],
        ["subject", "session"],
    )
    assert audit.matched_left_rows == 1
    assert audit.unmatched_left_rows == 1
    assert audit.ambiguous_left_rows == 0
    assert audit.passed


def test_join_detects_ambiguous_metadata():
    audit = audit_join(
        [{"subject": "s1", "session": "a"}],
        [
            {"subject": "s1", "session": "a", "dx": "x"},
            {"subject": "s1", "session": "a", "dx": "y"},
        ],
        ["subject", "session"],
    )
    assert not audit.passed
    assert audit.ambiguous_left_rows == 1
    assert audit.duplicate_right_keys == (("s1", "a"),)


def test_subject_leakage_is_rejected():
    with pytest.raises(ValueError, match="subject leakage"):
        assert_subject_disjoint(["s1", "s2"], ["s2", "s3"])


def test_subject_disjoint_split_passes():
    assert_subject_disjoint(["s1", "s2"], ["s3", "s4"])
