"""Prospective substrate-closure contracts for NSD Bio Chi.

These tests formalize exact projection/closure distinctions motivated by the
Substrate Inheritance work. They do not define a numerical closure threshold,
do not change A0/A1/A2, and do not license real EEG local chi.

For an orthogonal P/Q split of a linear generator L, the block form is

    L = [[L_PP, L_PQ],
         [L_QP, L_QQ]]

with three distinct mechanisms:
- L_QP != 0: a state initialized in P leaks into Q;
- L_PQ != 0: hidden/substrate state Q can directly drive P;
- Sigma(z) = L_PQ (zI-L_QQ)^-1 L_QP: excursions through Q return to P
  and generate frequency-dependent reduced dynamics / memory.

No empirical cutoff is introduced here. Tests use exact zero/nonzero fixtures
and the exact Schur-complement resolvent identity.
"""

from __future__ import annotations

import numpy as np
import pytest


P_IDX = np.asarray([0, 1], dtype=int)
Q_IDX = np.asarray([2, 3], dtype=int)


def _matrix(
    *,
    omega1: float = 1.0,
    zeta1: float = 0.2,
    omega2: float = 1.0,
    zeta2: float = 0.2,
    position_coupling_12: float = 0.0,
    position_coupling_21: float = 0.0,
    velocity_coupling_12: float = 0.0,
    velocity_coupling_21: float = 0.0,
) -> np.ndarray:
    return np.asarray(
        [
            [0.0, 1.0, 0.0, 0.0],
            [
                -(omega1 * omega1),
                -2.0 * zeta1 * omega1,
                position_coupling_12,
                velocity_coupling_12,
            ],
            [0.0, 0.0, 0.0, 1.0],
            [
                position_coupling_21,
                velocity_coupling_21,
                -(omega2 * omega2),
                -2.0 * zeta2 * omega2,
            ],
        ],
        dtype=float,
    )


def _blocks(L: np.ndarray):
    Lpp = L[np.ix_(P_IDX, P_IDX)]
    Lpq = L[np.ix_(P_IDX, Q_IDX)]
    Lqp = L[np.ix_(Q_IDX, P_IDX)]
    Lqq = L[np.ix_(Q_IDX, Q_IDX)]
    return Lpp, Lpq, Lqp, Lqq


def leakage_norm(L: np.ndarray) -> float:
    """Exact P->Q leakage magnitude ||L_QP||_F."""
    return float(np.linalg.norm(_blocks(L)[2], ord="fro"))


def hidden_input_norm(L: np.ndarray) -> float:
    """Exact Q->P direct dependence magnitude ||L_PQ||_F."""
    return float(np.linalg.norm(_blocks(L)[1], ord="fro"))


def self_energy(L: np.ndarray, z: complex) -> np.ndarray:
    """Exact Schur-complement self-energy Sigma(z)."""
    _, Lpq, Lqp, Lqq = _blocks(L)
    return Lpq @ np.linalg.inv(z * np.eye(Lqq.shape[0]) - Lqq) @ Lqp


def projected_resolvent(L: np.ndarray, z: complex) -> np.ndarray:
    full = np.linalg.inv(z * np.eye(L.shape[0]) - L)
    return full[np.ix_(P_IDX, P_IDX)]


def reduced_resolvent(L: np.ndarray, z: complex) -> np.ndarray:
    Lpp, _, _, _ = _blocks(L)
    sigma = self_energy(L, z)
    return np.linalg.inv(z * np.eye(Lpp.shape[0]) - Lpp - sigma)


def test_uncoupled_subspace_is_exactly_closed_and_memory_free():
    L = _matrix()
    z = 0.7 + 0.9j

    assert leakage_norm(L) == pytest.approx(0.0, abs=1e-15)
    assert hidden_input_norm(L) == pytest.approx(0.0, abs=1e-15)
    assert np.linalg.norm(self_energy(L, z), ord="fro") == pytest.approx(0.0, abs=1e-15)


def test_q_to_p_feedforward_is_invariant_but_hidden_input_exposed():
    """P is invariant for P-only initial states, but arbitrary hidden Q can drive P."""
    L = _matrix(position_coupling_12=2.0)
    z = 0.7 + 0.9j

    assert leakage_norm(L) == pytest.approx(0.0, abs=1e-15)
    assert hidden_input_norm(L) > 0.0
    assert np.linalg.norm(self_energy(L, z), ord="fro") == pytest.approx(0.0, abs=1e-15)


def test_p_to_q_feedforward_leaks_without_return_memory():
    """P excites Q, but Q has no path back to P, so Sigma(z) remains zero."""
    L = _matrix(position_coupling_21=2.0)
    z = 0.7 + 0.9j

    assert leakage_norm(L) > 0.0
    assert hidden_input_norm(L) == pytest.approx(0.0, abs=1e-15)
    assert np.linalg.norm(self_energy(L, z), ord="fro") == pytest.approx(0.0, abs=1e-15)


def test_bidirectional_coupling_creates_return_memory():
    L = _matrix(position_coupling_12=0.8, position_coupling_21=0.8)
    z = 0.7 + 0.9j

    assert leakage_norm(L) > 0.0
    assert hidden_input_norm(L) > 0.0
    assert np.linalg.norm(self_energy(L, z), ord="fro") > 0.0


@pytest.mark.parametrize(
    "z",
    [
        0.5 + 0.8j,
        1.2 + 0.4j,
        2.0 + 1.5j,
    ],
)
def test_self_energy_reproduces_exact_projected_resolvent(z: complex):
    """Schur-complement reduced dynamics exactly match the P block of the full resolvent."""
    L = _matrix(
        position_coupling_12=0.8,
        position_coupling_21=0.6,
        velocity_coupling_12=0.25,
        velocity_coupling_21=-0.15,
    )

    exact = projected_resolvent(L, z)
    reduced = reduced_resolvent(L, z)
    np.testing.assert_allclose(reduced, exact, rtol=2e-12, atol=2e-12)


def test_same_local_blocks_can_have_different_closure_class():
    """Local isolated oscillator parameters do not determine projection closure."""
    uncoupled = _matrix()
    bidirectional = _matrix(position_coupling_12=0.8, position_coupling_21=0.8)

    np.testing.assert_allclose(
        uncoupled[np.ix_(P_IDX, P_IDX)],
        bidirectional[np.ix_(P_IDX, P_IDX)],
        rtol=0.0,
        atol=0.0,
    )

    assert leakage_norm(uncoupled) == 0.0
    assert hidden_input_norm(uncoupled) == 0.0
    assert leakage_norm(bidirectional) > 0.0
    assert hidden_input_norm(bidirectional) > 0.0


def test_self_energy_is_frequency_dependent_when_return_path_exists():
    L = _matrix(position_coupling_12=0.8, position_coupling_21=0.8)

    low = self_energy(L, 0.4 + 0.3j)
    high = self_energy(L, 2.0 + 1.4j)

    assert np.linalg.norm(low - high, ord="fro") > 1e-6
