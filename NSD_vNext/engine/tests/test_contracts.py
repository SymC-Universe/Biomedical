import pytest

from nsd_engine import (
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


def provenance():
    return ProvenanceRecord(
        subject_id="sub-001",
        session_id="ses-001",
        recording_condition="eyes_closed",
        source_dataset="fixture",
        sampling_rate_hz=256.0,
        engine_version="0.1.0",
        config_hash=canonical_config_hash({"fit_range_hz": [2, 40]}),
        run_id="run-001",
    )


def qc():
    return SignalQC(300.0, 285.0, True, ("line_noise_checked",))


def spectral():
    return SpectralState(
        aperiodic_exponent=1.2,
        aperiodic_offset=0.1,
        peaks=(SpectralPeak("p1", 10.0, 0.4, 1.5, "gaussian_descriptive"),),
        fit_quality={"r2": 0.95},
        fit_model="periodic_aperiodic_descriptive",
    )


def test_config_hash_is_canonical():
    assert canonical_config_hash({"b": 2, "a": 1}) == canonical_config_hash({"a": 1, "b": 2})


def test_no_peak_state_is_valid_without_scalar():
    result = EngineResult(
        provenance=provenance(),
        signal_qc=qc(),
        spectral_state=SpectralState(1.1, 0.0, (), {"r2": 0.9}, "descriptive"),
        scalar_refusals=(
            ScalarRefusal("chi_mode", RefusalCode.NO_PEAK, "No qualifying periodic peak"),
        ),
    )
    assert result.scalar_names() == ()
    assert result.refusal_codes() == (RefusalCode.NO_PEAK,)


def test_licensed_chi_requires_existing_mode_lineage():
    with pytest.raises(ValueError, match="unknown mode"):
        EngineResult(
            provenance=provenance(),
            signal_qc=qc(),
            spectral_state=spectral(),
            candidate_modes=(),
            licensed_scalars=(LicensedScalar("chi_mode", 0.8, 0.05, "m1", "fixture"),),
        )


def test_mode_specific_chi_is_allowed_with_lineage():
    mode = CandidateMode("m1", "known_truth_fixture", 10.0, 2.0, -2.0, 62.8, True)
    result = EngineResult(
        provenance=provenance(),
        signal_qc=qc(),
        spectral_state=spectral(),
        candidate_modes=(mode,),
        licensed_scalars=(LicensedScalar("chi_mode_m1", 0.2, 0.02, "m1", "known truth fixture"),),
    )
    assert result.scalar_names() == ("chi_mode_m1",)


def test_whole_system_chi_is_prohibited():
    with pytest.raises(ValueError, match="whole-system chi"):
        LicensedScalar("whole_brain_chi", 0.9, 0.1, "m1", "invalid fixture")


def test_duplicate_modes_are_rejected():
    m1 = CandidateMode("m1", "fixture", 10.0, identifiable=True)
    with pytest.raises(ValueError, match="mode_id values must be unique"):
        EngineResult(
            provenance=provenance(),
            signal_qc=qc(),
            spectral_state=spectral(),
            candidate_modes=(m1, m1),
        )


def test_negative_bandwidth_is_rejected():
    with pytest.raises(ValueError, match="bandwidth_hz must be > 0"):
        SpectralPeak("p1", 10.0, 0.2, -1.0, "gaussian_descriptive")


def test_usable_duration_cannot_exceed_total_duration():
    with pytest.raises(ValueError, match="cannot exceed"):
        SignalQC(10.0, 11.0, True)
