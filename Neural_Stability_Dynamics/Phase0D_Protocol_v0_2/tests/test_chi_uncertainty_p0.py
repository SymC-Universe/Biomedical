import numpy as np

from src.chi_conglomerate import second_order_generator
from src.chi_uncertainty import pair_invariants_from_hankel, propagate_hankel_root_to_chi
from src.hankel_uncertainty import batch_hankel_covariance_root, nsd_covariance_hankel
from src.population_covariance import population_covariance_hankel
from src.synthetic_systems import simulate_linear


def _C():
    rng = np.random.default_rng(20260911)
    C = rng.normal(size=(6, 2))
    return C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)


def test_pair_invariant_hankel_coordinate_is_branch_complete_at_population():
    C = _C()
    for chi in [0.8, 1.0, 1.2, 1.5]:
        A = second_order_generator(chi, 2.0 * np.pi * 2.0)
        H, _ = population_covariance_hankel(A, C, 0.01, 30, 0.30)
        out = pair_invariants_from_hankel(H, 6, 0.01)
        assert np.isclose(out["chi"], chi, rtol=1e-7, atol=1e-7)
        assert np.isclose(out["delta_chi"], chi * chi - 1.0, rtol=1e-7, atol=1e-7)


def test_zero_root_gives_zero_chi_and_discriminant_variance():
    C = _C()
    A = second_order_generator(0.8, 2.0 * np.pi * 2.0)
    Y = simulate_linear(A, C, 0.01, 8000, 0.30, np.random.default_rng(42))
    H = nsd_covariance_hankel(Y, 30)
    T = np.zeros((H.size, 5), float)
    out = propagate_hankel_root_to_chi(H, T, 6, 0.01, epsilon=0.5)
    assert np.isclose(out["variance_chi"], 0.0)
    assert np.isclose(out["variance_delta_chi"], 0.0)


def test_native_batch_root_produces_finite_nonnegative_coordinate_variance():
    C = _C()
    A = second_order_generator(1.01, 2.0 * np.pi * 2.0)
    Y = simulate_linear(A, C, 0.01, 8000, 0.30, np.random.default_rng(43))
    H = nsd_covariance_hankel(Y, 30)
    T, _ = batch_hankel_covariance_root(Y, 30, 12)
    out = propagate_hankel_root_to_chi(H, T, 6, 0.01, epsilon=0.5)
    assert np.isfinite(out["variance_chi"])
    assert np.isfinite(out["variance_delta_chi"])
    assert out["variance_chi"] >= 0.0
    assert out["variance_delta_chi"] >= 0.0
    assert out["variance_chi"] > 0.0
    assert out["variance_delta_chi"] > 0.0
