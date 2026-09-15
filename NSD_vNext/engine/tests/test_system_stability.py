import pytest

from nsd_engine.system_stability import (
    LinearSystem2D,
    locally_stable_globally_unstable_fixture,
    locally_unstable_globally_stabilized_fixture,
    same_local_different_coupling_fixture,
)


def _sorted_real_parts(system: LinearSystem2D):
    return sorted(value.real for value in system.eigenvalues)


def test_same_local_same_eigenvalues_can_have_different_transient_reactivity():
    baseline, reactive = same_local_different_coupling_fixture()

    assert baseline.same_isolated_local_dynamics(reactive)
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


def test_normality_measure_zero_for_symmetric_matrix():
    system = LinearSystem2D(-1.0, 2.0, 2.0, -1.0, name="symmetric")
    assert system.normal is True
    assert system.nonnormality_commutator_norm_sq == pytest.approx(0.0)
