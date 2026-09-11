import numpy as np

from src.chi_conglomerate import second_order_generator
from src.coupled_conglomeration import feedback_return_operator


def _environment(A1, A2, K12, K21):
    return np.block([[A1, K12], [K21, A2]])


def _nested_feedback(A0, A1, A2, K01, K10, K12, K21, s):
    # Eliminate subsystem 2 into subsystem 1, then subsystem 1 into subsystem 0.
    M2 = complex(s) * np.eye(A2.shape[0]) - A2
    sigma_1_from_2 = K12 @ np.linalg.solve(M2, K21)
    M1_eff = complex(s) * np.eye(A1.shape[0]) - A1 - sigma_1_from_2
    return K01 @ np.linalg.solve(M1_eff, K10)


def test_grouped_environment_reduces_to_direct_feedback_when_intermediary_uncoupled():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.75, 2.0 * np.pi * 5.0)
    A2 = second_order_generator(0.90, 2.0 * np.pi * 7.0)
    K01 = np.array([[0.0, 0.0], [4.0, 0.0]])
    K10 = np.array([[0.0, 0.0], [4.0, 0.0]])
    Z = np.zeros((2, 2))

    Ae = _environment(A1, A2, Z, Z)
    K0e = np.hstack([K01, Z])
    Ke0 = np.vstack([K10, Z])

    for s in [0.0, 1j * 2.0 * np.pi * 3.0, 2.0 + 4.0j]:
        grouped = feedback_return_operator(A0, Ae, K0e, Ke0, s)
        direct = feedback_return_operator(A0, A1, K01, K10, s)
        assert np.allclose(grouped, direct, rtol=1e-11, atol=1e-11)


def test_nested_reduction_matches_grouped_environment_feedback():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.75, 2.0 * np.pi * 5.0)
    A2 = second_order_generator(0.90, 2.0 * np.pi * 7.0)
    K01 = np.array([[0.0, 0.0], [4.0, 0.0]])
    K10 = np.array([[0.0, 0.0], [4.0, 0.0]])
    K12 = np.array([[0.0, 0.0], [2.0, 0.0]])
    K21 = np.array([[0.0, 0.0], [2.0, 0.0]])
    Z = np.zeros((2, 2))

    Ae = _environment(A1, A2, K12, K21)
    K0e = np.hstack([K01, Z])
    Ke0 = np.vstack([K10, Z])

    for s in [0.0, 1j * 2.0 * np.pi * 3.0, 2.0 + 4.0j]:
        grouped = feedback_return_operator(A0, Ae, K0e, Ke0, s)
        nested = _nested_feedback(A0, A1, A2, K01, K10, K12, K21, s)
        assert np.allclose(grouped, nested, rtol=1e-10, atol=1e-10)


def test_intermediary_dynamics_change_return_seen_by_outer_group_without_changing_outer_edges():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.75, 2.0 * np.pi * 5.0)
    A2 = second_order_generator(0.90, 2.0 * np.pi * 7.0)
    K01 = np.array([[0.0, 0.0], [4.0, 0.0]])
    K10 = np.array([[0.0, 0.0], [4.0, 0.0]])
    Z = np.zeros((2, 2))
    K12 = np.array([[0.0, 0.0], [6.0, 0.0]])
    K21 = np.array([[0.0, 0.0], [6.0, 0.0]])

    direct = feedback_return_operator(A0, A1, K01, K10, 1j * 2.0 * np.pi * 3.0)

    Ae = _environment(A1, A2, K12, K21)
    K0e = np.hstack([K01, Z])
    Ke0 = np.vstack([K10, Z])
    grouped = feedback_return_operator(A0, Ae, K0e, Ke0, 1j * 2.0 * np.pi * 3.0)

    assert not np.allclose(grouped, direct)


def test_internal_basis_changes_of_environment_leave_outer_feedback_operator_invariant():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.75, 2.0 * np.pi * 5.0)
    A2 = second_order_generator(0.90, 2.0 * np.pi * 7.0)
    K01 = np.array([[0.0, 0.0], [4.0, 0.0]])
    K10 = np.array([[0.0, 0.0], [4.0, 0.0]])
    K12 = np.array([[0.0, 0.0], [3.0, 1.0]])
    K21 = np.array([[0.0, 0.0], [-1.0, 2.0]])
    Z = np.zeros((2, 2))

    Ae = _environment(A1, A2, K12, K21)
    K0e = np.hstack([K01, Z])
    Ke0 = np.vstack([K10, Z])

    S1 = np.array([[1.1, 0.2], [-0.1, 0.9]])
    S2 = np.array([[0.8, -0.2], [0.3, 1.2]])
    Se = np.block([[S1, Z], [Z, S2]])
    Sei = np.linalg.inv(Se)
    Aep = Se @ Ae @ Sei
    K0ep = K0e @ Sei
    Kep0 = Se @ Ke0

    for s in [0.0, 1j * 2.0 * np.pi * 3.0, 2.0 + 4.0j]:
        base = feedback_return_operator(A0, Ae, K0e, Ke0, s)
        transformed = feedback_return_operator(A0, Aep, K0ep, Kep0, s)
        assert np.allclose(base, transformed, rtol=1e-10, atol=1e-10)
