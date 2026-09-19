import pytest

from nsd_engine.system_stability import (
    LinearSystem2D,
    different_local_same_global_spectrum_fixture,
    locally_stable_globally_unstable_fixture,
    locally_unstable_globally_stabilized_fixture,
    same_local_different_coupling_fixture,
)


def _sorted_real_parts(system: LinearSystem2D):
    return sorted(value.real for value in system.eigenvalues)


def test_same_local_same_eigenvalues_can_have_different_transient_reactivity():
    baseline, reactive = same_local_different_coupling_fixture()

    assert baseline.same_isolated_local_dynamics(reactive)
    assert baseline.same_eigenspectrum(reactive)
    assert _sorted_real_parts(baseline) == pytest.approx([-1.0, -1.0])
    assert _sorted_real_parts(reactive) == pytest.approx([-1.0, -1.0])
    assert baseline.asymptotically_stable is True
    assert reactive.asymptotically_stable is True

    assert baseline.numerical_abscissa == pytest.approx(-1.0)
    assert baseline.reactive is False
    assert reactive.numerical_abscissa == pytest.approx(1.0)
    assert reactive.reactive is True
    assert baseline.normal is True
    assert reactive.normal is False


def test_same_spectrum_can_still_have_different_finite_time_gain():
    baseline, reactive = same_local_different_coupling_fixture()

    t0, g0 = baseline.max_transient_gain(t_max=5.0, samples=501)
    tr, gr = reactive.max_transient_gain(t_max=5.0, samples=501)

    assert t0 == pytest.approx(0.0)
    assert g0 == pytest.approx(1.0)
    assert tr > 0.0
    assert gr > 1.5


def test_different_local_rates_can_share_embedded_eigenspectrum():
    baseline, compensated = different_local_same_global_spectrum_fixture()

    assert baseline.same_isolated_local_dynamics(compensated) is False
    assert baseline.isolated_local_rates == pytest.approx((-1.0, -2.0))
    assert compensated.isolated_local_rates == pytest.approx((1.0, -4.0))
    assert baseline.same_eigenspectrum(compensated)
    assert _sorted_real_parts(baseline) == pytest.approx([-2.0, -1.0])
    assert _sorted_real_parts(compensated) == pytest.approx([-2.0, -1.0])
    assert baseline.asymptotically_stable is True
    assert compensated.asymptotically_stable is True


def test_locally_stable_components_can_be_globally_unstable():
    system = locally_stable_globally_unstable_fixture()

    assert system.local_components_stable is True
    assert _sorted_real_parts(system) == pytest.approx([-3.0, 1.0])
    assert system.spectral_abscissa == pytest.approx(1.0)
    assert system.asymptotically_stable is False


def test_locally_unstable_component_can_be_globally_asymptotically_stabilized():
    system = locally_unstable_globally_stabilized_fixture()

    assert system.local_components_stable is False
    assert system.isolated_local_rates == pytest.approx((1.0, -3.0))
    assert _sorted_real_parts(system) == pytest.approx([-1.0, -1.0])
    assert system.spectral_abscissa == pytest.approx(-1.0)
    assert system.asymptotically_stable is True

    # Asymptotic stability does not erase transient reactivity.
    assert system.numerical_abscissa == pytest.approx(1.0)
    assert system.reactive is True


def test_transient_gain_input_validation():
    system = LinearSystem2D(-1.0, 0.0, 0.0, -1.0, name="stable")

    with pytest.raises(ValueError):
        system.transient_gain(-0.1)
    with pytest.raises(ValueError):
        system.max_transient_gain(t_max=0.0)
    with pytest.raises(ValueError):
        system.max_transient_gain(samples=1)


def test_normality_measure_zero_for_symmetric_matrix():
    system = LinearSystem2D(-1.0, 2.0, 2.0, -1.0, name="symmetric")
    assert system.normal is True
    assert system.nonnormality_commutator_norm_sq == pytest.approx(0.0)
