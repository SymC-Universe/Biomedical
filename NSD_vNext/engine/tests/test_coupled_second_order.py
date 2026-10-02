import pytest

from nsd_engine.coupled_second_order import (
    CoupledSecondOrder2Mode,
    locally_stable_globally_unstable_second_order_fixture,
    same_local_different_embedding_fixture,
    same_local_same_spectrum_different_transient_fixture,
)


def _sorted(values):
    return sorted(values, key=lambda z: (round(z.real, 10), round(z.imag, 10)))


def test_same_local_chi_and_same_spectrum_can_hide_transient_difference():
    baseline, coupled = same_local_same_spectrum_different_transient_fixture()

    assert baseline.same_local_modes(coupled)
    assert baseline.local_damping_ratios == pytest.approx((0.20, 0.20))
    assert baseline.same_eigenspectrum(coupled)
    assert _sorted(baseline.eigenvalues) == pytest.approx(_sorted(coupled.eigenvalues))

    assert baseline.asymptotically_stable
    assert coupled.asymptotically_stable

    tb, gb = baseline.max_transient_gain()
    tc, gc = coupled.max_transient_gain()
    assert gb == pytest.approx(1.0, abs=1e-10)
    assert tb == pytest.approx(0.0, abs=1e-10)
    assert gc > 2.0
    assert tc > 0.0
    assert coupled.numerical_abscissa > baseline.numerical_abscissa


def test_recovery_can_differ_despite_same_local_chi_and_same_spectrum():
    baseline, coupled = same_local_same_spectrum_different_transient_fixture()

    baseline_return = baseline.sustained_return_time(gain_threshold=1.05)
    coupled_return = coupled.sustained_return_time(gain_threshold=1.05)

    assert baseline_return == pytest.approx(0.0)
    assert coupled_return is not None
    assert coupled_return > 5.0


def test_same_local_modes_can_reorganize_embedded_spectrum():
    baseline, coupled = same_local_different_embedding_fixture()

    assert baseline.same_local_modes(coupled)
    assert baseline.same_eigenspectrum(coupled) is False
    assert baseline.asymptotically_stable
    assert coupled.asymptotically_stable

    base_imag = sorted(abs(z.imag) for z in baseline.eigenvalues)
    coupled_imag = sorted(abs(z.imag) for z in coupled.eigenvalues)
    assert coupled_imag != pytest.approx(base_imag)


def test_locally_stable_modal_chi_does_not_guarantee_global_stability():
    system = locally_stable_globally_unstable_second_order_fixture()

    assert system.isolated_local_stability == (True, True)
    assert system.local_damping_ratios == pytest.approx((0.20, 0.20))
    assert system.asymptotically_stable is False
    assert system.spectral_abscissa > 0.0


def test_local_poles_match_uncoupled_full_spectrum():
    system = CoupledSecondOrder2Mode(
        2.0, 0.30, 3.0, 0.40,
        name="uncoupled",
    )
    assert _sorted(system.eigenvalues) == pytest.approx(_sorted(system.isolated_local_poles))


def test_validation_and_transient_inputs():
    with pytest.raises(ValueError):
        CoupledSecondOrder2Mode(0.0, 0.2, 1.0, 0.2)

    system = CoupledSecondOrder2Mode(1.0, 0.2, 1.0, 0.2)
    with pytest.raises(ValueError):
        system.transient_gain(-0.1)
    with pytest.raises(ValueError):
        system.max_transient_gain(samples=1)
    with pytest.raises(ValueError):
        system.sustained_return_time(gain_threshold=0.0)
