import numpy as np

from src.lag_covariance_hac import (
    bartlett_hac_diagonal_variance_of_mean,
    lag_product_contribution_sequence,
    unique_lag_covariance_vector,
)


def test_lag_product_contribution_mean_is_exact_native_covariance_vector():
    rng = np.random.default_rng(20260911)
    Y = rng.normal(size=(200, 3))
    G = lag_product_contribution_sequence(Y, 7)
    direct = unique_lag_covariance_vector(Y, 7)
    assert G.shape == (200, 7 * 9)
    assert np.allclose(G.mean(axis=0), direct, atol=1e-12, rtol=1e-12)


def test_zero_bandwidth_hac_matches_iid_mean_variance_diagonal():
    rng = np.random.default_rng(20260912)
    G = rng.normal(size=(400, 5))
    got = bartlett_hac_diagonal_variance_of_mean(G, 0)
    expected = np.var(G, axis=0, ddof=0) / len(G)
    assert np.allclose(got, expected, atol=1e-12, rtol=1e-12)


def test_fft_bartlett_hac_matches_direct_autocovariance_sum():
    rng = np.random.default_rng(20260913)
    G = rng.normal(size=(240, 4))
    bw = 8
    got = bartlett_hac_diagonal_variance_of_mean(G, bw)
    Z = G - G.mean(axis=0, keepdims=True)
    n = len(G)
    omega = np.sum(Z * Z, axis=0) / n
    for h in range(1, bw + 1):
        gamma = np.sum(Z[h:] * Z[:-h], axis=0) / n
        omega += 2.0 * (1.0 - h / (bw + 1.0)) * gamma
    expected = omega / n
    assert np.allclose(got, expected, atol=1e-12, rtol=1e-12)
