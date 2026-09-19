"""Mechanical provenance and hierarchy safeguards for NSD vNext."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class HierarchyKey:
    subject_id: str
    session_id: str
    run_id: str | None = None
    trial_id: str | None = None

    def __post_init__(self) -> None:
        if not self.subject_id.strip():
            raise ValueError("subject_id must be non-empty")
        if not self.session_id.strip():
            raise ValueError("session_id must be non-empty")
        for name in ("run_id", "trial_id"):
            value = getattr(self, name)
            if value is not None and not value.strip():
                raise ValueError(f"{name} must be non-empty when present")


@dataclass(frozen=True)
class DuplicateAudit:
    duplicate_keys: tuple[HierarchyKey, ...]

    @property
    def passed(self) -> bool:
        return not self.duplicate_keys


@dataclass(frozen=True)
class JoinAudit:
    key_fields: tuple[str, ...]
    matched_left_rows: int
    unmatched_left_rows: int
    ambiguous_left_rows: int
    duplicate_right_keys: tuple[tuple[Any, ...], ...]

    @property
    def passed(self) -> bool:
        return self.ambiguous_left_rows == 0 and not self.duplicate_right_keys


def audit_duplicate_hierarchy(keys: Iterable[HierarchyKey]) -> DuplicateAudit:
    seen: set[HierarchyKey] = set()
    duplicates: list[HierarchyKey] = []
    for key in keys:
        if key in seen and key not in duplicates:
            duplicates.append(key)
        seen.add(key)
    return DuplicateAudit(tuple(duplicates))


def _key_tuple(row: Mapping[str, Any], key_fields: Sequence[str]) -> tuple[Any, ...]:
    missing = [field for field in key_fields if field not in row]
    if missing:
        raise KeyError(f"row missing join keys: {missing}")
    return tuple(row[field] for field in key_fields)


def audit_join(
    left_rows: Sequence[Mapping[str, Any]],
    right_rows: Sequence[Mapping[str, Any]],
    key_fields: Sequence[str],
) -> JoinAudit:
    """Audit a metadata join without performing a silent first-match assignment."""
    if not key_fields:
        raise ValueError("key_fields must not be empty")

    right_counts: dict[tuple[Any, ...], int] = {}
    for row in right_rows:
        key = _key_tuple(row, key_fields)
        right_counts[key] = right_counts.get(key, 0) + 1

    duplicate_right_keys = tuple(
        sorted((key for key, count in right_counts.items() if count > 1), key=repr)
    )

    matched = 0
    unmatched = 0
    ambiguous = 0
    for row in left_rows:
        key = _key_tuple(row, key_fields)
        count = right_counts.get(key, 0)
        if count == 0:
            unmatched += 1
        elif count == 1:
            matched += 1
        else:
            ambiguous += 1

    return JoinAudit(
        key_fields=tuple(key_fields),
        matched_left_rows=matched,
        unmatched_left_rows=unmatched,
        ambiguous_left_rows=ambiguous,
        duplicate_right_keys=duplicate_right_keys,
    )


def assert_subject_disjoint(train_subject_ids: Iterable[str], test_subject_ids: Iterable[str]) -> None:
    train = {value for value in train_subject_ids if value}
    test = {value for value in test_subject_ids if value}
    overlap = train & test
    if overlap:
        raise ValueError(f"subject leakage across split: {sorted(overlap)}")
