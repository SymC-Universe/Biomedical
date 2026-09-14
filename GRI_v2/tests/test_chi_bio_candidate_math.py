import numpy as np
import pytest

from src.chi_bio_candidate_math import (
    g1_jacobian_from_normalized_interaction,
    g1_normalized_interaction_value,
    g2_transition_value,
    largest_singular_value,
    spectral_abscissa,
    spectral_radius,
    unity_regime,
)


def test_g1_known_stable_matrix_is_below_unity():
    m = np.diag([0.2, 0.7, 0.95])
    value = g1_normalized_interaction_value(m)
    assert value == pytest.approx(0.95)
    assert unity_regime(value) == "BELOW_UNITY"


def test_g1_known_boundary_matrix_is_at_unity():
    m = np.diag([0.2, 1.0, 0.7])
    value = g1_normalized_interaction_value(m)
    assert value == pytest.approx(1.0)
    assert unity_regime(value) == "AT_UNITY_WITHIN_TOLERANCE"


def test_g1_known_unstable_matrix_is_above_unity():
    m = np.diag([0.2, 1.1, 0.7])
    value = g1_normalized_interaction_value(m)
    assert value == pytest.approx(1.1)
    assert unity_regime(value) == "ABOVE_UNITY"


def test_g1_source_model_jacobian_shifts_unity_to_zero():
    m = np.diag([0.4, 0.8, 1.0])
    j = g1_jacobian_from_normalized_interaction(m, beta0=2.5)
    assert spectral_abscissa(j) == pytest.approx(0.0)

    m_stable = np.diag([0.4, 0.8, 0.99])
    j_stable = g1_jacobian_from_normalized_interaction(m_stable, beta0=2.5)
    assert spectral_abscissa(j_stable) < 0.0

    m_unstable = np.diag([0.4, 0.8, 1.01])
    j_unstable = g1_jacobian_from_normalized_interaction(m_unstable, beta0=2.5)
    assert spectral_abscissa(j_unstable) > 0.0


def test_g2_known_transition_states_relative_to_unit_circle():
    stable = np.diag([0.2, 0.8, -0.95])
    boundary = np.diag([0.2, 1.0, -0.95])
    unstable = np.diag([0.2, 1.05, -0.95])

    assert g2_transition_value(stable) == pytest.approx(0.95)
    assert unity_regime(g2_transition_value(stable)) == "BELOW_UNITY"
    assert unity_regime(g2_transition_value(boundary)) == "AT_UNITY_WITHIN_TOLERANCE"
    assert unity_regime(g2_transition_value(unstable)) == "ABOVE_UNITY"


def test_g2_nonnormal_matrix_can_be_spectrally_stable_but_amplifying():
    t = np.array([[0.8, 5.0], [0.0, 0.8]])
    assert spectral_radius(t) == pytest.approx(0.8)
    assert largest_singular_value(t) > 1.0


def test_g2_sampling_interval_changes_value_but_not_stability_side_for_stable_rates():
    rates = np.array([-0.1, -0.4])
    t_short = np.diag(np.exp(rates * 0.5))
    t_long = np.diag(np.exp(rates * 2.0))

    rho_short = spectral_radius(t_short)
    rho_long = spectral_radius(t_long)

    assert 0.0 < rho_long < rho_short < 1.0
    assert unity_regime(rho_short) == "BELOW_UNITY"
    assert unity_regime(rho_long) == "BELOW_UNITY"


def test_invalid_matrix_and_tolerance_fail_loudly():
    with pytest.raises(ValueError):
        spectral_radius(np.array([1.0, 2.0]))
    with pytest.raises(ValueError):
        spectral_abscissa(np.array([[1.0, np.nan], [0.0, 1.0]]))
    with pytest.raises(ValueError):
        unity_regime(1.0, tolerance=-1e-3)
    with pytest.raises(ValueError):
        g1_jacobian_from_normalized_interaction(np.eye(2), beta0=0.0)
