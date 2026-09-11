import numpy as np

from src.chi_conglomerate import chi_from_pole_pair, second_order_generator
from src.population_covariance import population_covariance_hankel
from src.ssi_cov import fit_from_decomposition


def _C():
    rng = np.random.default_rng(20260911)
    C = rng.normal(size=(6, 2))
    return C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)


def _population_fit(chi):
    A = second_order_generator(chi, 2.0 * np.pi * 2.0)
    H, _ = population_covariance_hankel(A, _C(), 0.01, 30, 0.30)
    U, S, _ = np.linalg.svd(H, full_matrices=False)
    vals, _ = fit_from_decomposition(U, S, 6, 2, 0.01)
    return vals, S


def test_population_hankel_recovers_chi_below_at_and_above_boundary():
    for chi in [0.8, 0.99, 1.0, 1.01, 1.2, 1.5, 2.0]:
        vals, _ = _population_fit(chi)
        out = chi_from_pole_pair(vals)
        assert np.isclose(out["chi"], chi, rtol=1e-7, atol=1e-7)


def test_population_hankel_has_two_supported_directions_and_numerical_tail():
    for chi in [0.8, 1.0, 1.5, 2.0]:
        _, S = _population_fit(chi)
        assert S[1] > 1e-8 * S[0]
        assert S[2] < 1e-10 * S[0]
