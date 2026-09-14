"""Explicit metadata-role firewall for the NSD Structural Engine.

The Structural Engine is allowed to know recording identity and acquisition/state
context required to interpret a signal. Demographics, diagnoses, symptoms, and
outcomes are retained downstream but cannot be used to define structural
features or tune admission thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


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
