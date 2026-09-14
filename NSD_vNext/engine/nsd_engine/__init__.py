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
]
