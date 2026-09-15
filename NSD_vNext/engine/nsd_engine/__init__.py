"""NSD vNext Structural Engine contract scaffold.

This package intentionally contains no clinical classifier and no estimator that
manufactures a dynamical scalar. It defines auditable result contracts plus
label-blind qualification utilities.
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
from .metadata import MetadataRole, MetadataRoleManifest, conservative_role_guess
from .spectral import (
    DescriptiveSpectralEstimate,
    DescriptiveSpectralEstimator,
    SpectralConfig,
)
from .qc import ChannelQC, QCThresholds, SignalQCReport, evaluate_signal_qc
from .system_stability import (
    LinearSystem2D,
    locally_stable_globally_unstable_fixture,
    locally_unstable_globally_stabilized_fixture,
    same_local_different_coupling_fixture,
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
    "MetadataRole",
    "MetadataRoleManifest",
    "conservative_role_guess",
    "DescriptiveSpectralEstimate",
    "DescriptiveSpectralEstimator",
    "SpectralConfig",
    "ChannelQC",
    "QCThresholds",
    "SignalQCReport",
    "evaluate_signal_qc",
    "LinearSystem2D",
    "locally_stable_globally_unstable_fixture",
    "locally_unstable_globally_stabilized_fixture",
    "same_local_different_coupling_fixture",
]
