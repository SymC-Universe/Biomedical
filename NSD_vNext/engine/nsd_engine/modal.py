"""Interfaces for qualified modal estimators.

This module defines how a modal method may report candidates to the NSD Engine.
It intentionally implements no DMD, OMA, neural-mass, or oscillator estimator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence, runtime_checkable, Any

from .schema import CandidateMode


@dataclass(frozen=True)
class ModalEstimateBatch:
    """One method's mode candidates plus method-level diagnostics."""

    method_name: str
    method_version: str
    modes: tuple[CandidateMode, ...]
    diagnostics: Mapping[str, Any]
    qualified_for_scalar_admission: bool = False

    def __post_init__(self) -> None:
        if not self.method_name.strip():
            raise ValueError("method_name must be non-empty")
        if not self.method_version.strip():
            raise ValueError("method_version must be non-empty")
        ids = [mode.mode_id for mode in self.modes]
        if len(ids) != len(set(ids)):
            raise ValueError("ModalEstimateBatch mode_id values must be unique")
        for mode in self.modes:
            if mode.source_method != self.method_name:
                raise ValueError(
                    f"mode {mode.mode_id!r} source_method {mode.source_method!r} "
                    f"does not match batch method {self.method_name!r}"
                )


@runtime_checkable
class ModalEstimator(Protocol):
    """Protocol every modal implementation must satisfy.

    A concrete implementation may consume arrays or richer recording objects,
    but must return an auditable ModalEstimateBatch. Clinical labels are not a
    parameter in this interface.
    """

    name: str
    version: str

    def estimate(self, signal: Sequence[float], sampling_rate_hz: float) -> ModalEstimateBatch:
        ...
