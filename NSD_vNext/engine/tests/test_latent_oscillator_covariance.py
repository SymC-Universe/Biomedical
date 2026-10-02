import numpy as np
import pytest

from nsd_engine.latent_oscillator_covariance import (
    LatentOscillatorTruth,
    fit_latent_oscillator_covariance,
    simulate_latent_oscillator,
)
from nsd_engine.schema import RefusalCode


@pytest.mark.parametrize(
    "frequency_hz,zeta",
    [
        (5.0, 0.2),
        (10.0, 0.5),
        (20.0, 0.8),
    ],
)
def test_latent_covariance_recovers_clean_truth(frequency_hz, zeta):
    truth = LatentOscillatorTruth(frequency_hz, zeta, 256.0)
    signal = simulate_latent_oscillator(
        truth,
        seconds=120.0,
        measurement_noise_to_latent_sd=0.0,
        seed=20260914,
    )
    result = fit_latent_oscillator_covariance(signal, 256.0, fmin_hz=1.0, fmax_hz=45.0)

    assert result.admitted is True
    assert result.natural_frequency_hz == pytest.approx(frequency_hz, rel=0.05)
    assert result.damping_ratio == pytest.approx(zeta, abs=0.06)
    assert result.latent_variance_fraction == pytest.approx(1.0, abs=0.12)
    assert result.autocorrelation_r_squared > 0.8


@pytest.mark.parametrize("noise_ratio", [0.25, 0.5, 1.0])
def test_latent_covariance_retains_truth_under_additive_observation_noise(noise_ratio):
    truth = LatentOscillatorTruth(10.0, 0.5, 256.0)
    signal = simulate_latent_oscillator(
        truth,
        seconds=180.0,
        measurement_noise_to_latent_sd=noise_ratio,
        seed=20260914,
    )
    result = fit_latent_oscillator_covariance(signal, 256.0, fmin_hz=1.0, fmax_hz=45.0)

    assert result.admitted is True
    assert result.natural_frequency_hz == pytest.approx(10.0, rel=0.06)
    assert result.damping_ratio == pytest.approx(0.5, abs=0.08)
    expected_fraction = 1.0 / (1.0 + noise_ratio**2)
    assert result.latent_variance_fraction == pytest.approx(expected_fraction, abs=0.12)
    assert result.autocorrelation_r_squared > 0.7


def test_latent_covariance_refuses_nonfinite_signal():
    signal = np.ones(1000)
    signal[10] = np.nan
    result = fit_latent_oscillator_covariance(signal, 256.0)
    assert result.admitted is False
    assert result.refusal_code is RefusalCode.SIGNAL_INSUFFICIENT


def test_latent_covariance_refuses_zero_variance():
    result = fit_latent_oscillator_covariance(np.ones(1000), 256.0)
    assert result.admitted is False
    assert result.refusal_code is RefusalCode.MODE_NONIDENTIFIABLE


def test_latent_covariance_refuses_too_short_signal():
    result = fit_latent_oscillator_covariance(np.arange(100.0), 256.0, min_samples=512)
    assert result.admitted is False
    assert result.refusal_code is RefusalCode.SIGNAL_INSUFFICIENT
