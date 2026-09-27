"""Predictive approximate-closure contracts for NSD Bio Chi.

Qualification only. These tests implement the exact P/Q elimination identities
behind the approved predictive-closure policy. They deliberately avoid any
empirical closure threshold and do not modify A0/A1/A2.

For
    p' = L_PP p + L_PQ q
    q' = L_QP p + L_QQ q,

eliminating q gives
    p'(t) = L_PP p(t)
            + L_PQ exp(L_QQ t) q0
            + integral_0^t K(t-s) p(s) ds,

where
    K(t) = L_PQ exp(L_QQ t) L_QP.

This separates hidden-initial-state forcing from endogenous return memory.
"""

from __future__ import annotations

import numpy as np
import pytest
from scipy.linalg import expm


P = np.asarray([0, 1], dtype=int)
Q = np.asarray([2, 3], dtype=int)


def _matrix(
    *,
    position_coupling_12: float = 0.0,
    position_coupling_21: float = 0.0,
    velocity_coupling_12: float = 0.0,
    velocity_coupling_21: float = 0.0,
) -> np.ndarray:
    return np.asarray(
        [
            [0.0, 1.0, 0.0, 0.0],
            [-1.0, -0.4, position_coupling_12, velocity_coupling_12],
            [0.0, 0.0, 0.0, 1.0],
            [
                position_coupling_21,
                velocity_coupling_21,
                -(1.7**2),
                -2.0 * 0.35 * 1.7,
            ],
        ],
        dtype=float,
    )


def _blocks(L: np.ndarray):
    return (
        L[np.ix_(P, P)],
        L[np.ix_(P, Q)],
        L[np.ix_(Q, P)],
        L[np.ix_(Q, Q)],
    )


def memory_kernel(L: np.ndarray, t: float) -> np.ndarray:
    _, Lpq, Lqp, Lqq = _blocks(L)
    return Lpq @ expm(Lqq * t) @ Lqp


def hidden_initial_forcing(L: np.ndarray, t: float, q0: np.ndarray) -> np.ndarray:
    _, Lpq, _, Lqq = _blocks(L)
    return Lpq @ expm(Lqq * t) @ q0


def full_p_trajectory(L: np.ndarray, p0: np.ndarray, q0: np.ndarray, times: np.ndarray):
    x0 = np.concatenate((p0, q0))
    return np.asarray([(expm(L * float(t)) @ x0)[:2] for t in times])


def markov_p_trajectory(L: np.ndarray, p0: np.ndarray, times: np.ndarray):
    Lpp, _, _, _ = _blocks(L)
    return np.asarray([expm(Lpp * float(t)) @ p0 for t in times])


def relative_rms(reference: np.ndarray, candidate: np.ndarray) -> float:
    numerator = float(np.sqrt(np.mean((reference - candidate) ** 2)))
    denominator = float(np.sqrt(np.mean(reference**2)))
    if denominator == 0.0:
        return 0.0 if numerator == 0.0 else float("inf")
    return numerator / denominator


def test_p_to_q_leakage_without_return_does_not_harm_p_prediction():
    """Raw leakage is nonzero, but the claimed P trajectory remains exactly Markovian."""
    L = _matrix(position_coupling_21=0.9)
    _, Lpq, Lqp, _ = _blocks(L)
    times = np.linspace(0.0, 8.0, 401)
    p0 = np.asarray([1.0, 0.0])
    q0 = np.zeros(2)

    assert np.linalg.norm(Lqp) > 0.0
    assert np.linalg.norm(Lpq) == pytest.approx(0.0, abs=1e-15)
    assert np.linalg.norm(memory_kernel(L, 1.0)) == pytest.approx(0.0, abs=1e-15)

    full = full_p_trajectory(L, p0, q0, times)
    reduced = markov_p_trajectory(L, p0, times)
    np.testing.assert_allclose(full, reduced, rtol=2e-12, atol=2e-12)
    assert relative_rms(full, reduced) < 1e-12


def test_q_to_p_hidden_input_has_no_return_memory_but_can_harm_prediction():
    """Hidden-state uncertainty is distinct from endogenous memory."""
    L = _matrix(position_coupling_12=0.9)
    _, Lpq, Lqp, _ = _blocks(L)
    times = np.linspace(0.0, 8.0, 401)
    p0 = np.asarray([1.0, 0.0])
    q0_zero = np.zeros(2)
    q0_hidden = np.asarray([0.5, -0.25])

    assert np.linalg.norm(Lpq) > 0.0
    assert np.linalg.norm(Lqp) == pytest.approx(0.0, abs=1e-15)
    assert np.linalg.norm(memory_kernel(L, 1.0)) == pytest.approx(0.0, abs=1e-15)
    assert np.linalg.norm(hidden_initial_forcing(L, 0.5, q0_hidden)) > 0.0

    reduced = markov_p_trajectory(L, p0, times)
    zero_hidden = full_p_trajectory(L, p0, q0_zero, times)
    hidden = full_p_trajectory(L, p0, q0_hidden, times)

    np.testing.assert_allclose(zero_hidden, reduced, rtol=2e-12, atol=2e-12)
    assert relative_rms(hidden, reduced) > 1e-3


def test_bidirectional_path_creates_memory_and_harms_p_prediction_even_q0_zero():
    L = _matrix(position_coupling_12=0.8, position_coupling_21=0.7)
    times = np.linspace(0.0, 8.0, 401)
    p0 = np.asarray([1.0, 0.0])
    q0 = np.zeros(2)

    assert np.linalg.norm(memory_kernel(L, 0.5)) > 0.0

    full = full_p_trajectory(L, p0, q0, times)
    reduced = markov_p_trajectory(L, p0, times)
    assert relative_rms(full, reduced) > 1e-3


def test_hidden_initial_forcing_decays_with_stable_hidden_generator():
    L = _matrix(position_coupling_12=0.9)
    q0 = np.asarray([0.5, -0.25])

    early = np.linalg.norm(hidden_initial_forcing(L, 0.25, q0))
    late = np.linalg.norm(hidden_initial_forcing(L, 20.0, q0))

    assert early > 0.0
    assert late < early


def test_memory_kernel_is_zero_if_either_direction_is_absent():
    cases = [
        _matrix(position_coupling_12=0.8),
        _matrix(position_coupling_21=0.8),
    ]
    for L in cases:
        for t in (0.0, 0.25, 1.0, 3.0):
            assert np.linalg.norm(memory_kernel(L, t)) == pytest.approx(0.0, abs=1e-14)


def test_memory_kernel_is_time_dependent_for_bidirectional_fixture():
    L = _matrix(position_coupling_12=0.8, position_coupling_21=0.7)
    first = memory_kernel(L, 0.2)
    second = memory_kernel(L, 1.0)
    assert np.linalg.norm(first) > 0.0
    assert np.linalg.norm(second) > 0.0
    assert np.linalg.norm(first - second) > 1e-6
