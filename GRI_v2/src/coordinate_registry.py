from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


REQUIRED_CHI_GATES = tuple(f"G{i}" for i in range(1, 11))


@dataclass(frozen=True)
class ChiCandidate:
    name: str
    gamma_name: str
    omega_name: str
    passed_gates: frozenset[str]

    @classmethod
    def from_gates(cls, name: str, gamma_name: str, omega_name: str, passed_gates: Iterable[str]) -> "ChiCandidate":
        return cls(name, gamma_name, omega_name, frozenset(passed_gates))

    @property
    def admissible(self) -> bool:
        return set(REQUIRED_CHI_GATES).issubset(self.passed_gates)

    @property
    def missing_gates(self) -> tuple[str, ...]:
        return tuple(g for g in REQUIRED_CHI_GATES if g not in self.passed_gates)


def classify_as_chi(candidate: ChiCandidate) -> str:
    if candidate.name.strip().upper() in {"CV/2", "CV2", "CV_OVER_2"}:
        return "REJECT_HISTORICAL_CV2_IS_NOT_CHI"
    if not candidate.admissible:
        return "REJECT_MISSING_CHI_GATES:" + ",".join(candidate.missing_gates)
    return "ADMISSIBLE_CANDIDATE_CHI"
