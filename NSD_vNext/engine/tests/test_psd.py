import math

import numpy as np
import pytest

from nsd_engine.psd import WelchConfig, estimate_welch_psd


def _sine(freq_hz: float, fs: float, seconds: float, amplitude: float = 1.0):
    t = np.arange(int(fs * seconds), dtype=float) / fs
    return amplitude * np.sin(2.0 * math.pi * freq_hz * t)


def test_welch_recovers_known_sine_frequency_without_dynamical_license():
    fs = 256.0
    signal = _sine(10.0, fs, 8.0)
    result = estimate_welch_psd(
        signal,
        fs,
        fmin_hz=1.0,
        fmax_hz=45.0,
        config=WelchConfig(window_seconds=2.0, overlap_fraction=0.5),
    )

    peak_index = int(np.argmax(result.power))
    assert result.frequencies_hz[peak_index] == pytest.approx(10.0)
    assert result.frequency_resolution_hz == pytest.approx(0.5)
    assert result.segment_count == 7
    assert result.licenses_damping is False
    assert result.licenses_dynamical_chi is False


def test_welch_density_integrates_to_sine_variance():
    fs = 256.0
    signal = _sine(12.0, fs, 16.0, amplitude=2.0)
    result = estimate_welch_psd(
        signal,
        fs,
        fmin_hz=0.0,
        fmax_hz=fs / 2,
        config=WelchConfig(window_seconds=4.0, overlap_fraction=0.5, scaling="density"),
    )

    df = result.frequency_resolution_hz
    integrated_power = sum(result.power) * df
    expected_variance = 2.0  # variance of amplitude-2 sinusoid
    assert integrated_power == pytest.approx(expected_variance, rel=0.03)


def test_welch_frequency_range_is_explicitly_clipped():
    fs = 100.0
    signal = _sine(8.0, fs, 10.0)
    result = estimate_welch_psd(
        signal,
        fs,
        fmin_hz=5.0,
        fmax_hz=20.0,
        config=WelchConfig(window_seconds=2.0),
    )

    assert result.frequencies_hz[0] >= 5.0
    assert result.frequencies_hz[-1] <= 20.0


def test_welch_refuses_nonfinite_signal():
    with pytest.raises(ValueError, match="non-finite"):
        estimate_welch_psd([0.0, 1.0, float("nan"), 0.0], 10.0, fmax_hz=5.0)


def test_welch_refuses_window_longer_than_signal():
    with pytest.raises(ValueError, match="shorter than one requested Welch window"):
        estimate_welch_psd(
            [0.0] * 100,
            100.0,
            fmax_hz=50.0,
            config=WelchConfig(window_seconds=2.0),
        )


def test_welch_refuses_frequency_above_nyquist():
    with pytest.raises(ValueError, match="Nyquist"):
        estimate_welch_psd([0.0] * 1000, 100.0, fmax_hz=60.0)
