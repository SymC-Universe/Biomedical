import numpy as np

from src.chi_conglomerate import (
    analytic_same_conglomerate_example,
    chi_from_pole_pair,
    conglomerate_chi,
    second_order_generator,
)


def test_pair_invariant_recovers_constructed_chi_on_all_branches():
    omega_n = 2.0 * np.pi * 3.0
    for chi in [0.2, 0.8, 0.99, 1.0, 1.01, 1.2, 2.0]:
        vals = np.linalg.eigvals(second_order_generator(chi, omega_n))
        out = chi_from_pole_pair(vals)
        assert np.isclose(out["chi"], chi, rtol=1e-10, atol=1e-10)
        assert np.isclose(out["omega_n"], omega_n, rtol=1e-10, atol=1e-10)


def test_conglomerate_reduces_to_single_component_and_common_chi():
    for chi in [0.3, 0.9, 1.0, 1.7]:
        one = conglomerate_chi([chi], [7.3])
        assert np.isclose(one["chi_C"], chi)
        common = conglomerate_chi([chi, chi, chi], [1.0, 5.0, 11.0])
        assert np.isclose(common["chi_C"], chi)


def test_conglomerate_is_permutation_invariant_and_bounded_by_components():
    chi = np.array([0.35, 0.9, 1.4])
    wn = np.array([2.0, 5.0, 9.0])
    w = np.array([1.0, 0.4, 2.0])
    a = conglomerate_chi(chi, wn, w)
    p = np.array([2, 0, 1])
    b = conglomerate_chi(chi[p], wn[p], w[p])
    assert np.isclose(a["chi_C"], b["chi_C"])
    assert a["component_min"] <= a["chi_C"] <= a["component_max"]
    assert np.isclose(a["chi_C"], a["weighted_rms_identity"])


def test_different_modal_architectures_can_share_same_conglomerate_chi():
    ex = analytic_same_conglomerate_example(0.8, 0.4)
    assert ex["set_A"] != ex["set_B"]
    assert np.isclose(ex["chi_C_A"], 0.8)
    assert np.isclose(ex["chi_C_B"], 0.8)
