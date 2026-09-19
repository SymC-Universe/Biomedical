import numpy as np
import pytest

from nsd_engine.specparam_adapter import (
    REQUIRED_SPECPARAM_VERSION,
    SpecparamSettings,
    fit_specparam_descriptive,
    installed_specparam_version,
)


def _freqs():
    return np.arange(1.0, 45.0 + 0.25, 0.25, dtype=float)


def _fixed_log_power(freqs, offset=1.2, exponent=1.5):
    return offset - exponent * np.log10(freqs)


def _knee_log_power(freqs, offset=2.0, knee=25.0, exponent=2.0):
    return offset - np.log10(knee + freqs**exponent)


def _gaussian(freqs, cf, height, sigma):
    return height * np.exp(-((freqs - cf) ** 2) / (2.0 * sigma**2))


def _linear_power(log_power):
    return 10.0**log_power


def _metric(result, key):
    return dict(result.metrics)[key]


def test_exact_release_candidate_is_frozen():
    assert installed_specparam_version() == REQUIRED_SPECPARAM_VERSION == "2.0.0rc7"


def test_pure_fixed_aperiodic_truth_recovers_without_inventing_peak():
    freqs = _freqs()
    truth_offset = 1.2
    truth_exponent = 1.5
    power = _linear_power(_fixed_log_power(freqs, truth_offset, truth_exponent))

    result = fit_specparam_descriptive(
        freqs,
        power,
        settings=SpecparamSettings(
            aperiodic_mode="fixed",
            max_n_peaks=6,
            min_peak_height=0.05,
            peak_threshold=2.0,
            fmin_hz=1.0,
            fmax_hz=45.0,
        ),
    )

    assert result.aperiodic_parameter_names == ("offset", "exponent")
    assert result.aperiodic_parameters[0] == pytest.approx(truth_offset, abs=1e-3)
    assert result.aperiodic_parameters[1] == pytest.approx(truth_exponent, abs=1e-3)
    assert result.zero_peak_state is True
    assert result.peaks == ()
    assert result.licenses_damping is False
    assert result.licenses_natural_frequency is False
    assert result.licenses_chi is False
    assert result.licenses_modal_pole is False


def test_single_gaussian_peak_truth_recovers_descriptive_parameters():
    freqs = _freqs()
    log_power = _fixed_log_power(freqs, offset=1.0, exponent=1.2)
    log_power += _gaussian(freqs, cf=10.0, height=0.6, sigma=1.0)

    result = fit_specparam_descriptive(
        freqs,
        _linear_power(log_power),
        settings=SpecparamSettings(
            aperiodic_mode="fixed",
            max_n_peaks=3,
            min_peak_height=0.1,
            peak_threshold=2.0,
            fmin_hz=1.0,
            fmax_hz=45.0,
        ),
    )

    assert len(result.peaks) == 1
    peak = result.peaks[0]
    assert peak.center_frequency_hz == pytest.approx(10.0, abs=0.15)
    assert peak.power_above_aperiodic_log10 == pytest.approx(0.6, abs=0.05)
    assert peak.bandwidth_hz == pytest.approx(2.0, abs=0.2)
    assert result.licenses_damping is False
    assert result.licenses_chi is False


def test_two_separated_peak_truth_recovers_two_descriptive_components():
    freqs = _freqs()
    log_power = _fixed_log_power(freqs, offset=1.0, exponent=1.0)
    log_power += _gaussian(freqs, cf=10.0, height=0.65, sigma=0.8)
    log_power += _gaussian(freqs, cf=20.0, height=0.45, sigma=1.2)

    result = fit_specparam_descriptive(
        freqs,
        _linear_power(log_power),
        settings=SpecparamSettings(
            aperiodic_mode="fixed",
            max_n_peaks=4,
            min_peak_height=0.1,
            peak_threshold=2.0,
            fmin_hz=1.0,
            fmax_hz=45.0,
        ),
    )

    assert len(result.peaks) == 2
    peaks = sorted(result.peaks, key=lambda value: value.center_frequency_hz)
    assert peaks[0].center_frequency_hz == pytest.approx(10.0, abs=0.2)
    assert peaks[0].bandwidth_hz == pytest.approx(1.6, abs=0.25)
    assert peaks[1].center_frequency_hz == pytest.approx(20.0, abs=0.2)
    assert peaks[1].bandwidth_hz == pytest.approx(2.4, abs=0.3)


def test_knee_truth_is_better_described_by_knee_than_fixed_when_peaks_disabled():
    freqs = _freqs()
    truth_offset = 2.0
    truth_knee = 25.0
    truth_exponent = 2.0
    power = _linear_power(_knee_log_power(freqs, truth_offset, truth_knee, truth_exponent))

    knee_result = fit_specparam_descriptive(
        freqs,
        power,
        settings=SpecparamSettings(
            aperiodic_mode="knee",
            max_n_peaks=0,
            min_peak_height=0.1,
            peak_threshold=2.0,
            fmin_hz=1.0,
            fmax_hz=45.0,
        ),
    )
    fixed_result = fit_specparam_descriptive(
        freqs,
        power,
        settings=SpecparamSettings(
            aperiodic_mode="fixed",
            max_n_peaks=0,
            min_peak_height=0.1,
            peak_threshold=2.0,
            fmin_hz=1.0,
            fmax_hz=45.0,
        ),
    )

    assert knee_result.aperiodic_parameter_names == ("offset", "knee", "exponent")
    assert knee_result.aperiodic_parameters[0] == pytest.approx(truth_offset, abs=0.02)
    assert knee_result.aperiodic_parameters[1] == pytest.approx(truth_knee, abs=0.5)
    assert knee_result.aperiodic_parameters[2] == pytest.approx(truth_exponent, abs=0.02)
    assert _metric(knee_result, "error_mae") < _metric(fixed_result, "error_mae")
    assert knee_result.zero_peak_state is True
    assert fixed_result.zero_peak_state is True


def test_broad_gaussian_is_kept_descriptive_only():
    freqs = _freqs()
    log_power = _fixed_log_power(freqs, offset=1.0, exponent=1.0)
    log_power += _gaussian(freqs, cf=15.0, height=0.5, sigma=4.0)

    result = fit_specparam_descriptive(
        freqs,
        _linear_power(log_power),
        settings=SpecparamSettings(
            aperiodic_mode="fixed",
            max_n_peaks=2,
            min_peak_height=0.1,
            peak_threshold=2.0,
            peak_width_limits=(0.5, 12.0),
            fmin_hz=1.0,
            fmax_hz=45.0,
        ),
    )

    assert len(result.peaks) >= 1
    closest = min(result.peaks, key=lambda value: abs(value.center_frequency_hz - 15.0))
    assert closest.center_frequency_hz == pytest.approx(15.0, abs=0.5)
    assert closest.bandwidth_hz == pytest.approx(8.0, abs=1.0)
    assert result.licenses_damping is False
    assert result.licenses_natural_frequency is False
    assert result.licenses_chi is False


def test_adapter_rejects_logged_or_nonpositive_power_input():
    freqs = _freqs()
    log_power = _fixed_log_power(freqs)
    with pytest.raises(ValueError, match="strictly positive"):
        fit_specparam_descriptive(freqs, log_power)
