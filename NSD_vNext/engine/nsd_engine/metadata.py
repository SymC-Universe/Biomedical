"""Explicit metadata-role firewall for the NSD Structural Engine.

The Structural Engine is allowed to know recording identity and acquisition/state
context required to interpret a signal. Demographics, diagnoses, symptoms, and
outcomes are retained downstream but cannot be used to define structural
features or tune admission thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


_MISSING_TOKENS = {"", "n/a", "na", "nan", "none", "null"}


class MetadataRole(str, Enum):
    IDENTITY = "identity"
    ACQUISITION = "acquisition"
    RECORDING_STATE = "recording_state"
    DEMOGRAPHIC_COVARIATE = "demographic_covariate"
    CLINICAL_LABEL = "clinical_label"
    CLINICAL_OUTCOME = "clinical_outcome"
    OTHER = "other"


_ENGINE_VISIBLE_ROLES = {
    MetadataRole.IDENTITY,
    MetadataRole.ACQUISITION,
    MetadataRole.RECORDING_STATE,
}


def _normalized_value(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text.lower() in _MISSING_TOKENS:
        return None
    return text


@dataclass(frozen=True)
class MetadataRoleManifest:
    roles: Mapping[str, MetadataRole]

    def __post_init__(self) -> None:
        if not self.roles:
            raise ValueError("metadata role manifest must not be empty")
        for column, role in self.roles.items():
            if not isinstance(column, str) or not column.strip():
                raise ValueError("metadata column names must be non-empty strings")
            if not isinstance(role, MetadataRole):
                raise TypeError(f"metadata role for {column!r} must be MetadataRole")

    def engine_visible_columns(self) -> tuple[str, ...]:
        return tuple(
            column for column, role in self.roles.items() if role in _ENGINE_VISIBLE_ROLES
        )

    def downstream_only_columns(self) -> tuple[str, ...]:
        return tuple(
            column for column, role in self.roles.items() if role not in _ENGINE_VISIBLE_ROLES
        )

    def clinical_columns(self) -> tuple[str, ...]:
        return tuple(
            column
            for column, role in self.roles.items()
            if role in {MetadataRole.CLINICAL_LABEL, MetadataRole.CLINICAL_OUTCOME}
        )

    def assert_engine_columns_allowed(self, columns: tuple[str, ...] | list[str]) -> None:
        unknown = [column for column in columns if column not in self.roles]
        if unknown:
            raise ValueError(f"engine columns are missing explicit metadata roles: {unknown}")

        prohibited = [
            column for column in columns if self.roles[column] not in _ENGINE_VISIBLE_ROLES
        ]
        if prohibited:
            detail = {column: self.roles[column].value for column in prohibited}
            raise ValueError(f"downstream-only metadata cannot enter Structural Engine: {detail}")


@dataclass(frozen=True)
class DuplicateFieldAudit:
    base_column: str
    duplicate_column: str
    row_count: int
    equal_nonmissing: int
    both_missing: int
    base_only: int
    duplicate_only: int
    conflicts: int
    conflict_row_ids: tuple[str, ...]

    @property
    def safely_equivalent(self) -> bool:
        return self.conflicts == 0 and self.base_only == 0 and self.duplicate_only == 0


def audit_duplicate_field_pair(
    rows: Sequence[Mapping[str, object]],
    base_column: str,
    duplicate_column: str,
    *,
    row_id_column: str = "participant_id",
) -> DuplicateFieldAudit:
    """Compare duplicated metadata columns without choosing an authoritative copy.

    Values are compared as stripped strings after standard missing tokens are
    normalized to None. The output records one-sided missingness and true
    conflicts separately so a dataset-specific provenance decision can be made
    later rather than silently selecting whichever column appears first.
    """
    if not base_column.strip() or not duplicate_column.strip():
        raise ValueError("column names must be non-empty")

    equal_nonmissing = 0
    both_missing = 0
    base_only = 0
    duplicate_only = 0
    conflicts = 0
    conflict_row_ids: list[str] = []

    for index, row in enumerate(rows):
        if base_column not in row or duplicate_column not in row:
            missing = [
                name for name in (base_column, duplicate_column) if name not in row
            ]
            raise KeyError(f"row {index} missing duplicate-audit columns: {missing}")

        base = _normalized_value(row.get(base_column))
        duplicate = _normalized_value(row.get(duplicate_column))

        if base is None and duplicate is None:
            both_missing += 1
        elif base is not None and duplicate is None:
            base_only += 1
        elif base is None and duplicate is not None:
            duplicate_only += 1
        elif base == duplicate:
            equal_nonmissing += 1
        else:
            conflicts += 1
            row_id = _normalized_value(row.get(row_id_column))
            conflict_row_ids.append(row_id or f"row-{index}")

    return DuplicateFieldAudit(
        base_column=base_column,
        duplicate_column=duplicate_column,
        row_count=len(rows),
        equal_nonmissing=equal_nonmissing,
        both_missing=both_missing,
        base_only=base_only,
        duplicate_only=duplicate_only,
        conflicts=conflicts,
        conflict_row_ids=tuple(conflict_row_ids),
    )


def conservative_role_guess(column: str) -> MetadataRole:
    """Return a conservative suggestion, never an automatic scientific decision.

    This helper exists only to flag obvious label/outcome columns during dataset
    onboarding. Every production dataset still requires a reviewed role manifest.
    Unknown columns remain OTHER rather than being silently admitted.
    """
    normalized = column.strip().lower()
    if normalized in {"participant_id", "subject_id", "session_id", "run_id", "trial_id"}:
        return MetadataRole.IDENTITY
    if normalized in {
        "site",
        "device",
        "manufacturer",
        "sampling_rate",
        "sampling_rate_hz",
        "reference",
        "montage",
    }:
        return MetadataRole.ACQUISITION
    if normalized in {
        "task",
        "condition",
        "recording_condition",
        "eyes_open",
        "eyes_closed",
        "sleep_stage",
    }:
        return MetadataRole.RECORDING_STATE
    if normalized in {"age", "sex", "gender", "handedness"}:
        return MetadataRole.DEMOGRAPHIC_COVARIATE
    if any(token in normalized for token in ("diagnos", "group", "asd", "adhd", "mdd", "bipolar")):
        return MetadataRole.CLINICAL_LABEL
    if any(token in normalized for token in ("outcome", "response", "relapse", "followup_score")):
        return MetadataRole.CLINICAL_OUTCOME
    return MetadataRole.OTHER
