import math
import pytest

from nsd_engine import DHOTruth, impulse_response, transfer_power


def test_pole_and_frequency_relationships_are_exact():
    truth = DHOTruth(10.0, 0.2)
    assert truth.omega0_rad_s == pytest.approx(20.0 * math.pi)
    assert truth.decay_rate_per_s == pytest.approx(0.2 * 20.0 * math.pi)
    assert truth.pole_real_per_s == pytest.approx(-truth.decay_rate_per_s)
    assert truth.pole_imag_rad_s == pytest.approx(truth.damped_omega_rad_s)
    assert truth.damped_frequency_hz < truth.natural_frequency_hz


def test_resonance_center_is_not_automatically_natural_frequency():
    truth = DHOTruth(10.0, 0.2)
    assert truth.resonance_frequency_hz is not None
    assert truth.resonance_frequency_hz < truth.natural_frequency_hz
    assert truth.resonance_frequency_hz != pytest.approx(truth.damped_frequency_hz)


def test_high_damping_can_have_no_displacement_resonance_peak_while_still_underdamped():
    truth = DHOTruth(10.0, 0.8)
    assert truth.damping_ratio < 1.0
    assert truth.resonance_frequency_hz is None
    assert truth.damped_frequency_hz > 0


def test_impulse_response_initial_conditions():
    truth = DHOTruth(8.0, 0.1)
    dt = 1.0 / 10000.0
    times, values = impulse_response(
        truth,
        0.01,
        10000.0,
        initial_displacement=0.0,
        initial_velocity=1.0,
    )
    assert times[0] == 0.0
    assert values[0] == pytest.approx(0.0)
    numerical_initial_velocity = (values[1] - values[0]) / dt
    assert numerical_initial_velocity == pytest.approx(1.0, rel=0.02)


def test_transfer_power_peaks_near_analytic_resonance():
    truth = DHOTruth(10.0, 0.15)
    frequencies = [i / 100.0 for i in range(1, 2001)]
    powers = transfer_power(truth, frequencies)
    peak_frequency = frequencies[max(range(len(powers)), key=powers.__getitem__)]
    assert peak_frequency == pytest.approx(truth.resonance_frequency_hz, abs=0.02)


def test_fixture_rejects_non_underdamped_zeta():
    with pytest.raises(ValueError, match="0 < zeta < 1"):
        DHOTruth(10.0, 1.0)
