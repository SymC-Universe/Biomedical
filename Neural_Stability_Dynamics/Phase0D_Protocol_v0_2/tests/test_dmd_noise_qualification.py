import numpy as np
from scipy.linalg import expm
from scipy.optimize import linear_sum_assignment

from src.dmd import fit_dmd, fit_tls_dmd


def _known_system(dt=0.02):
    blocks = []
    truth = []
    for decay, hz in [(0.4, 3.0), (0.8, 8.0)]:
        b = 2 * np.pi * hz
        Ac = np.array([[-decay, -b], [b, -decay]])
        blocks.append(expm(Ac * dt))
        truth.extend([-decay + 1j * b, -decay - 1j * b])
    F = np.zeros((4, 4))
    F[:2, :2] = blocks[0]
    F[2:, 2:] = blocks[1]
    Q, _ = np.linalg.qr(np.random.default_rng(5).normal(size=(4, 4)))
    return Q @ F @ Q.T, np.asarray(truth, complex)


def _trajectory(F, n, seed):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=F.shape[0])
    Y = []
    for _ in range(n):
        Y.append(x.copy())
        x = F @ x
    return np.asarray(Y)


def _discrete_match_error(vals, truth, dt):
    a = np.exp(np.asarray(vals, complex) * dt)
    b = np.exp(np.asarray(truth, complex) * dt)
    cost = np.abs(a[:, None] - b[None, :])
    ri, cj = linear_sum_assignment(cost)
    return float(np.mean(cost[ri, cj]))


def test_tls_dmd_reduces_to_exact_recovery_on_noise_free_known_system():
    dt = 0.02
    F, truth = _known_system(dt)
    Y = _trajectory(F, 800, 10)
    exact, _ = fit_dmd(Y, dt, 4)
    tls, _ = fit_tls_dmd(Y, dt, 4)
    assert _discrete_match_error(exact, truth, dt) < 1e-10
    assert _discrete_match_error(tls, truth, dt) < 1e-10


def test_tls_dmd_sensor_noise_qualification_is_directionally_less_biased_than_exact_dmd():
    """P0 construction check, not a P1 superiority threshold."""
    dt = 0.02
    F, truth = _known_system(dt)
    exact_errors = []
    tls_errors = []
    for rep in range(12):
        clean = _trajectory(F, 1600, 100 + rep)
        rng = np.random.default_rng(1000 + rep)
        sd = np.maximum(clean.std(0, keepdims=True), 1e-12)
        noisy = clean + 0.10 * sd * rng.normal(size=clean.shape)
        exact, _ = fit_dmd(noisy, dt, 4)
        tls, _ = fit_tls_dmd(noisy, dt, 4)
        exact_errors.append(_discrete_match_error(exact, truth, dt))
        tls_errors.append(_discrete_match_error(tls, truth, dt))

    assert np.median(tls_errors) < np.median(exact_errors)
    assert np.sum(np.asarray(tls_errors) < np.asarray(exact_errors)) >= 10


def test_tls_dmd_fails_closed_on_impossible_rank():
    Y = np.random.default_rng(1).normal(size=(50, 3))
    try:
        fit_tls_dmd(Y, 0.01, 4)
    except ValueError:
        return
    raise AssertionError("TLS-DMD must reject rank above observable snapshot rank")
