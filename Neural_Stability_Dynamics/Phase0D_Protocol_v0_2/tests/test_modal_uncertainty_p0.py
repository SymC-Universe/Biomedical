import numpy as np

from src.hankel_uncertainty import nsd_covariance_hankel, batch_hankel_covariance_root
from src.modal_uncertainty import fit_poles_from_hankel, match_poles, propagate_hankel_root_to_poles
from src.ssi_cov import decompose, fit_from_decomposition
from src.synthetic_systems import make_linear_system, simulate_linear


def _record(n=3600):
    rng = np.random.default_rng(20260911)
    A, C = make_linear_system(
        {
            "modes": [
                {"type": "complex", "decay": 0.6, "frequency_hz": 3.0},
                {"type": "complex", "decay": 1.0, "frequency_hz": 8.0},
            ],
            "similarity": "orthogonal",
        },
        4,
        rng,
    )
    Y = simulate_linear(A, C, 0.02, n, 0.35, np.random.default_rng(20260912))
    return Y


def test_hankel_direct_fit_matches_current_ssi_realization():
    Y = _record()
    b = 12
    order = 4
    H = nsd_covariance_hankel(Y, b)
    direct = fit_poles_from_hankel(H, 4, order, 0.02)
    U, S, p = decompose(Y, b)
    current, _ = fit_from_decomposition(U, S, p, order, 0.02)
    matched, distance = match_poles(current, direct)
    assert np.max(distance) < 1e-9
    assert np.allclose(matched, current, atol=1e-9, rtol=1e-9)


def test_zero_hankel_root_produces_zero_first_order_variance():
    Y = _record()
    H = nsd_covariance_hankel(Y, 12)
    T = np.zeros((H.size, 4), float)
    out = propagate_hankel_root_to_poles(H, T, 4, 4, 0.02)
    assert len(out["base_poles"]) == 2
    assert np.allclose(out["variance_decay"], 0.0)
    assert np.allclose(out["variance_frequency_hz"], 0.0)


def test_native_batch_root_produces_finite_nonnegative_pole_variance():
    Y = _record(7200)
    H = nsd_covariance_hankel(Y, 12)
    T, _ = batch_hankel_covariance_root(Y, 12, 12)
    out = propagate_hankel_root_to_poles(H, T, 4, 4, 0.02, epsilon=0.5)
    assert len(out["base_poles"]) == 2
    assert np.all(np.isfinite(out["variance_decay"]))
    assert np.all(np.isfinite(out["variance_frequency_hz"]))
    assert np.all(out["variance_decay"] >= 0.0)
    assert np.all(out["variance_frequency_hz"] >= 0.0)
    assert np.any(out["variance_decay"] > 0.0)
    assert np.any(out["variance_frequency_hz"] > 0.0)
