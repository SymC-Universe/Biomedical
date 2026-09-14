"""NSD vNext Structural Engine contract scaffold.

This package intentionally contains no clinical classifier and no estimator that
manufactures a dynamical scalar. It defines auditable result contracts only.
"""

from .schema import (
    CandidateMode,
    EngineResult,
    LicensedScalar,
    ProvenanceRecord,
    RefusalCode,
    ScalarRefusal,
    SignalQC,
    SpectralPeak,
    SpectralState,
    canonical_config_hash,
)
from .provenance import (
    DuplicateAudit,
    HierarchyKey,
    JoinAudit,
    assert_subject_disjoint,
    audit_duplicate_hierarchy,
    audit_join,
)
from .serialization import to_canonical_json
from .known_truth import DHOTruth, impulse_response, transfer_power
from .modal import ModalEstimateBatch, ModalEstimator
from .admission import (
    AdmissionDecision,
    AdmissionEvidence,
    ScalarProposal,
    decide_scalar_admission,
)

__all__ = [
    "CandidateMode",
    "EngineResult",
    "LicensedScalar",
    "ProvenanceRecord",
    "RefusalCode",
    "ScalarRefusal",
    "SignalQC",
    "SpectralPeak",
    "SpectralState",
    "canonical_config_hash",
    "DuplicateAudit",
    "HierarchyKey",
    "JoinAudit",
    "assert_subject_disjoint",
    "audit_duplicate_hierarchy",
    "audit_join",
    "to_canonical_json",
    "DHOTruth",
    "impulse_response",
    "transfer_power",
    "ModalEstimateBatch",
    "ModalEstimator",
    "AdmissionDecision",
    "AdmissionEvidence",
    "ScalarProposal",
    "decide_scalar_admission",
]
