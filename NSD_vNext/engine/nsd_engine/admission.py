"""Mechanical scalar-admission gate for NSD vNext.

This module does not derive chi. It accepts a proposed scalar value from a
separately qualified model and enforces the minimum provenance/qualification
conditions before the value can become a LicensedScalar.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .schema import CandidateMode, LicensedScalar, RefusalCode, ScalarRefusal


@dataclass(frozen=True)
class ScalarProposal:
    name: str
    value: float
    uncertainty: float | None
    derivation: str
    dependencies: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("ScalarProposal.name must be non-empty")
        if not self.derivation.strip():
            raise ValueError("ScalarProposal.derivation must be non-empty")
        if not math.isfinite(self.value):
            raise ValueError("ScalarProposal.value must be finite")
        if self.uncertainty is not None and (
            not math.isfinite(self.uncertainty) or self.uncertainty < 0
        ):
            raise ValueError("ScalarProposal.uncertainty must be finite and >= 0 when present")


@dataclass(frozen=True)
class AdmissionEvidence:
    estimator_qualified: bool
    natural_frequency_mapping_verified: bool
    damping_or_decay_mapping_verified: bool
    broadening_resolved: bool
    uncertainty_acceptable: bool
    in_domain: bool


@dataclass(frozen=True)
class AdmissionDecision:
    licensed: LicensedScalar | None = None
    refusal: ScalarRefusal | None = None

    def __post_init__(self) -> None:
        if (self.licensed is None) == (self.refusal is None):
            raise ValueError("AdmissionDecision must contain exactly one of licensed or refusal")

    @property
    def admitted(self) -> bool:
        return self.licensed is not None


def decide_scalar_admission(
    mode: CandidateMode,
    proposal: ScalarProposal,
    evidence: AdmissionEvidence,
) -> AdmissionDecision:
    """Apply the frozen minimum scalar-admission firewall.

    The order is intentional: out-of-domain and model-identification failures
    are surfaced before downstream interpretation checks. No branch fabricates
    a substitute scalar.
    """
    if not evidence.in_domain:
        return AdmissionDecision(
            refusal=ScalarRefusal(
                proposal.name,
                RefusalCode.OUT_OF_DOMAIN,
                "Candidate mode lies outside the estimator's qualified operating domain",
                mode.mode_id,
            )
        )
    if not evidence.estimator_qualified or not mode.identifiable:
        return AdmissionDecision(
            refusal=ScalarRefusal(
                proposal.name,
                RefusalCode.MODE_NONIDENTIFIABLE,
                "Estimator/mode has not earned identifiable dynamical-parameter status",
                mode.mode_id,
            )
        )
    if not evidence.natural_frequency_mapping_verified:
        return AdmissionDecision(
            refusal=ScalarRefusal(
                proposal.name,
                RefusalCode.FREQ_NOT_OMEGA0,
                "Observed frequency has not been validly mapped to the required natural-frequency quantity",
                mode.mode_id,
            )
        )
    if not evidence.damping_or_decay_mapping_verified:
        return AdmissionDecision(
            refusal=ScalarRefusal(
                proposal.name,
                RefusalCode.WIDTH_NOT_DAMPING,
                "Decay/damping mapping is not licensed for this candidate mode",
                mode.mode_id,
            )
        )
    if not evidence.broadening_resolved:
        return AdmissionDecision(
            refusal=ScalarRefusal(
                proposal.name,
                RefusalCode.BROADENING_UNRESOLVED,
                "Non-damping broadening remains unresolved",
                mode.mode_id,
            )
        )
    if not evidence.uncertainty_acceptable:
        return AdmissionDecision(
            refusal=ScalarRefusal(
                proposal.name,
                RefusalCode.UNCERTAINTY_TOO_LARGE,
                "Scalar uncertainty exceeds the frozen admissible bound",
                mode.mode_id,
            )
        )

    return AdmissionDecision(
        licensed=LicensedScalar(
            name=proposal.name,
            value=proposal.value,
            uncertainty=proposal.uncertainty,
            source_mode_id=mode.mode_id,
            derivation=proposal.derivation,
            dependencies=proposal.dependencies,
        )
    )
