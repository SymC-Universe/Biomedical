import numpy as np
from scipy.linalg import expm
from scipy.optimize import linear_sum_assignment

from src.dmd import fit_dmd, fit_subspace_dmd


def _stochastic_system(dt=0.02):
    blocks = []
    truth = []
    for decay, hz in [(0.6, 3.0), (1.0, 8.0)]:
        b = 2 * np.pi * hz
        Ac = np.array([[-decay, -b], [b, -decay]])
        blocks.append(expm(Ac * dt))
        truth.extend([-decay + 1j * b, -decay - 1j * b])
    F = np.zeros((4, 4))
    F[:2, :2] = blocks[0]
    F[2:, 2:] = blocks[1]
    Q, _ = np.linalg.qr(np.random.default_rng(51).normal(size=(4, 4)))
    return Q @ F @ Q.T, np.asarray(truth, complex)


def _random_trajectory(F, n, seed, observation_noise_fraction):
    rng = np.random.default_rng(seed)
    x = np.zeros(F.shape[0])
    Y = []
    for _ in range(n):
        x = F @ x + 0.10 * rng.normal(size=F.shape[0])
        Y.append(x.copy())
    Y = np.asarray(Y)
    sd = np.maximum(Y.std(0, keepdims=True), 1e-12)
    Y = Y + float(observation_noise_fraction) * sd * rng.normal(size=Y.shape)
    return Y


def _discrete_match_error(vals, truth, dt):
    a = np.exp(np.asarray(vals, complex) * dt)
    b = np.exp(np.asarray(truth, complex) * dt)
    cost = np.abs(a[:, None] - b[None, :])
    ri, cj = linear_sum_assignment(cost)
    return float(np.mean(cost[ri, cj]))


def test_subspace_dmd_recovers_stochastic_modes_with_observation_noise():
    dt = 0.02
    F, truth = _stochastic_system(dt)
    errors = []
    for rep in range(8):
        Y = _random_trajectory(F, 2200, 500 + rep, 0.10)
        vals, modes = fit_subspace_dmd(Y, dt, 4)
        errors.append(_discrete_match_error(vals, truth, dt))
        assert modes.shape == (4, 4)
    assert np.median(errors) < 0.01


def test_subspace_dmd_is_directionally_more_robust_than_exact_dmd_in_fixed_random_noisy_case():
    """P0 construction check only; not a P1 superiority criterion."""
    dt = 0.02
    F, truth = _stochastic_system(dt)
    exact_errors = []
    subspace_errors = []
    for rep in range(10):
        Y = _random_trajectory(F, 2000, 700 + rep, 0.20)
        exact, _ = fit_dmd(Y, dt, 4)
        subspace, _ = fit_subspace_dmd(Y, dt, 4)
        exact_errors.append(_discrete_match_error(exact, truth, dt))
        subspace_errors.append(_discrete_match_error(subspace, truth, dt))
    assert np.median(subspace_errors) < np.median(exact_errors)
    assert np.sum(np.asarray(subspace_errors) < np.asarray(exact_errors)) >= 8


def test_subspace_dmd_fails_closed_when_requested_rank_exceeds_channel_count():
    Y = np.random.default_rng(2).normal(size=(100, 3))
    try:
        fit_subspace_dmd(Y, 0.01, 4)
    except ValueError:
        return
    raise AssertionError("Subspace DMD must reject rank above channel count")
