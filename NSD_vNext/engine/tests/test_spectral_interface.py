import pytest

from nsd_engine import (
    DescriptiveSpectralEstimate,
    SpectralConfig,
    SpectralPeak,
    SpectralState,
)


def state():
    return SpectralState(
        aperiodic_exponent=1.1,
        aperiodic_offset=0.2,
        peaks=(SpectralPeak("p1", 10.0, 0.5, 1.2, "gaussian_descriptive"),),
        fit_quality={"r2": 0.95},
        fit_model="periodic_aperiodic_descriptive",
    )


def test_descriptive_spectral_estimate_cannot_license_dynamical_chi():
    estimate = DescriptiveSpectralEstimate(
        method_name="fixture_spectral",
        method_version="0.0",
        config=SpectralConfig(2.0, 40.0, "welch", 4.0, 0.5),
        state=state(),
        diagnostics={},
    )
    assert estimate.licenses_dynamical_chi is False


def test_frequency_range_must_be_ordered():
    with pytest.raises(ValueError, match="fmax_hz"):
        SpectralConfig(40.0, 2.0, "welch")


def test_overlap_fraction_is_bounded():
    with pytest.raises(ValueError, match="overlap_fraction"):
        SpectralConfig(2.0, 40.0, "welch", 4.0, 1.0)


def test_window_must_be_positive_when_present():
    with pytest.raises(ValueError, match="window_seconds"):
        SpectralConfig(2.0, 40.0, "welch", 0.0, 0.5)
