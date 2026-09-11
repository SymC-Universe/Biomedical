import numpy as np

from src.chi_conglomerate import (
    analytic_same_conglomerate_example,
    chi_from_2x2_block,
    chi_from_pole_pair,
    conglomerate_chi,
    second_order_generator,
)


def test_pair_invariant_recovers_constructed_chi_on_all_branches():
    omega_n = 2.0 * np.pi * 3.0
    for chi in [0.2, 0.8, 0.99, 1.0, 1.01, 1.2, 2.0]:
        A = second_order_generator(chi, omega_n)
        vals = np.linalg.eigvals(A)
        out = chi_from_pole_pair(vals)
        block = chi_from_2x2_block(A)
        assert np.isclose(out["chi"], chi, rtol=1e-10, atol=1e-10)
        assert np.isclose(out["omega_n"], omega_n, rtol=1e-10, atol=1e-10)
        assert np.isclose(block["chi"], chi, rtol=1e-10, atol=1e-10)
        assert np.isclose(block["normalized_discriminant"], chi * chi - 1.0)


def test_block_chi_is_similarity_invariant_and_tracks_branch():
    rng = np.random.default_rng(20260911)
    for chi, branch in [
        (0.7, "COMPLEX_PAIR"),
        (1.0, "REPEATED_ROOT_BOUNDARY"),
        (1.4, "REAL_SPLIT"),
    ]:
        A = second_order_generator(chi, 9.0)
        while True:
            T = rng.normal(size=(2, 2))
            if abs(np.linalg.det(T)) > 0.2:
                break
        B = T @ A @ np.linalg.inv(T)
        a = chi_from_2x2_block(A)
        b = chi_from_2x2_block(B)
        assert np.isclose(a["chi"], b["chi"], rtol=1e-10, atol=1e-10)
        assert np.isclose(a["trace"], b["trace"], rtol=1e-10, atol=1e-10)
        assert np.isclose(a["determinant"], b["determinant"], rtol=1e-10, atol=1e-10)
        assert b["branch"] == branch


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
