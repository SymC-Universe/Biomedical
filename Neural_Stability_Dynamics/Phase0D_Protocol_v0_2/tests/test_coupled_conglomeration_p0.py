import numpy as np

from src.coupled_conglomeration import (
    assemble_coupled_generator,
    coupled_spectrum,
    feedback_return_operator,
    schur_determinant_identity,
)


def test_zero_coupling_reduces_to_block_diagonal_system():
    A0 = np.array([[-1.0, 2.0], [-3.0, -4.0]])
    A1 = np.array([[-0.5]])
    out = assemble_coupled_generator([A0, A1])
    expected = np.block(
        [[A0, np.zeros((2, 1))], [np.zeros((1, 2)), A1]]
    )
    assert np.allclose(out["generator"], expected)


def test_directed_coupling_uses_receiver_sender_convention():
    A0 = np.array([[-1.0]])
    A1 = np.array([[-2.0, 0.0], [0.0, -3.0]])
    K_0_from_1 = np.array([[4.0, 5.0]])
    K_1_from_0 = np.array([[6.0], [7.0]])
    out = assemble_coupled_generator(
        [A0, A1], {(0, 1): K_0_from_1, (1, 0): K_1_from_0}
    )
    A = out["generator"]
    assert np.allclose(A[0:1, 1:3], K_0_from_1)
    assert np.allclose(A[1:3, 0:1], K_1_from_0)


def test_feedback_return_requires_closed_path():
    Ag = np.array([[-1.0]])
    Ae = np.array([[-2.0]])
    # Group sends to environment, but nothing returns to group.
    Sigma = feedback_return_operator(
        Ag,
        Ae,
        np.array([[0.0]]),
        np.array([[3.0]]),
        s=1.0 + 0.5j,
    )
    assert np.allclose(Sigma, 0.0)


def test_scalar_feedback_return_matches_analytic_expression():
    Ag = np.array([[-1.0]])
    Ae = np.array([[-2.0]])
    Kge = np.array([[3.0]])
    Keg = np.array([[5.0]])
    s = 1.25 + 0.75j
    Sigma = feedback_return_operator(Ag, Ae, Kge, Keg, s)
    expected = 15.0 / (s + 2.0)
    assert np.allclose(Sigma[0, 0], expected)


def test_schur_feedback_reduction_matches_full_characteristic_determinant():
    Ag = np.array([[-1.0, 2.0], [-4.0, -3.0]])
    Ae = np.array([[-0.7, 0.4], [-0.2, -1.2]])
    Kge = np.array([[0.3, -0.1], [0.2, 0.5]])
    Keg = np.array([[0.4, 0.0], [-0.2, 0.1]])
    for s in [0.5 + 0.2j, 2.0 + 1.0j, -0.1 + 3.0j]:
        out = schur_determinant_identity(Ag, Ae, Kge, Keg, s)
        assert out["relative_residual"] < 1e-12


def test_feedback_coupling_can_reorganize_global_modes_without_any_averaging():
    A0 = np.array([[-1.0]])
    A1 = np.array([[-2.0]])
    uncoupled = coupled_spectrum([A0, A1])
    coupled = coupled_spectrum(
        [A0, A1], {(0, 1): np.array([[1.5]]), (1, 0): np.array([[1.0]])}
    )
    p0 = np.sort_complex(uncoupled["uncoupled_poles"])
    p1 = np.sort_complex(coupled["coupled_poles"])
    assert np.allclose(p0, np.array([-2.0, -1.0]))
    assert not np.allclose(p1, p0)
