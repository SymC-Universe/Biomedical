import numpy as np
import pytest

from src.chi_bio_g1_qualification import (
    continuous_time_numerical_abscissa,
    dominant_mode_status,
    g1a_entrywise_noise_pilot,
    interval_relative_to_unity,
    leading_realpart_gap,
)
from src.chi_bio_candidate_math import spectral_abscissa


def test_nonnormal_companion_warning_stays_visible():
    m = np.array([[0.8, 4.0], [0.0, 0.8]])
    j = m - np.eye(2)

    assert spectral_abscissa(j) == pytest.approx(-0.2)
    assert continuous_time_numerical_abscissa(j) == pytest.approx(1.8)


def test_dominant_mode_degeneracy_uses_subspace_warning():
    exact = np.diag([0.95, 0.95])
    near = np.diag([0.95, 0.95000001])
    separated = np.diag([0.95, 0.8])

    assert leading_realpart_gap(exact) == pytest.approx(0.0)
    assert dominant_mode_status(exact, gap_tolerance=1e-6) == "DOMINANT_SUBSPACE_NEAR_DEGENERATE"
    assert dominant_mode_status(near, gap_tolerance=1e-6) == "DOMINANT_SUBSPACE_NEAR_DEGENERATE"
    assert dominant_mode_status(separated, gap_tolerance=1e-6) == "DOMINANT_MODE_SEPARATED"


def test_interval_refuses_boundary_when_uncertainty_spans_unity():
    below = interval_relative_to_unity(np.array([0.91, 0.95, 0.97, 0.98, 0.99]))
    above = interval_relative_to_unity(np.array([1.01, 1.02, 1.03, 1.04, 1.05]))
    spans = interval_relative_to_unity(np.array([0.95, 0.98, 1.0, 1.02, 1.05]))

    assert below.disposition == "BELOW_UNITY_RESOLVED"
    assert above.disposition == "ABOVE_UNITY_RESOLVED"
    assert spans.disposition == "UNCERTAINTY_SPANS_BOUNDARY"


def test_noise_pilot_is_deterministic_and_reports_uncertainty():
    truth = np.diag([0.4, 0.8, 0.98])
    a = g1a_entrywise_noise_pilot(truth, sigma=0.005, replicates=200, seed=20260912)
    b = g1a_entrywise_noise_pilot(truth, sigma=0.005, replicates=200, seed=20260912)

    assert a == b
    assert a.truth_value == pytest.approx(0.98)
    assert a.replicates == 200
    assert a.lower_2p5 <= a.median_estimate <= a.upper_97p5
    assert 0.0 <= a.fraction_at_or_above_unity <= 1.0
    assert a.unity_disposition in {
        "BELOW_UNITY_RESOLVED",
        "UNCERTAINTY_SPANS_BOUNDARY",
    }


def test_invalid_qualification_inputs_fail_loudly():
    with pytest.raises(ValueError):
        dominant_mode_status(np.eye(2), gap_tolerance=-1.0)
    with pytest.raises(ValueError):
        interval_relative_to_unity(np.array([]))
    with pytest.raises(ValueError):
        g1a_entrywise_noise_pilot(np.eye(2), sigma=-0.1, replicates=20, seed=1)
    with pytest.raises(ValueError):
        g1a_entrywise_noise_pilot(np.eye(2), sigma=0.1, replicates=1, seed=1)
