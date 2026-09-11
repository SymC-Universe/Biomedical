import numpy as np

from src.chi_conglomerate import second_order_generator
from src.coupled_conglomeration import (
    assemble_coupled_generator,
    feedback_return_operator,
)


def _sorted_spectrum(A):
    vals = np.linalg.eigvals(A)
    return np.array(sorted(vals, key=lambda z: (round(float(z.real), 12), round(float(z.imag), 12))))


def test_consistent_subsystem_basis_changes_preserve_full_coupled_spectrum():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    K01 = np.array([[0.0, 0.0], [5.0, 2.0]])
    K10 = np.array([[0.0, 0.0], [-1.0, 4.0]])

    base = assemble_coupled_generator(
        [A0, A1], {(0, 1): K01, (1, 0): K10}
    )["generator"]

    S0 = np.array([[1.2, 0.3], [-0.2, 0.9]])
    S1 = np.array([[0.8, -0.1], [0.4, 1.3]])
    S0i = np.linalg.inv(S0)
    S1i = np.linalg.inv(S1)

    A0p = S0 @ A0 @ S0i
    A1p = S1 @ A1 @ S1i
    K01p = S0 @ K01 @ S1i
    K10p = S1 @ K10 @ S0i

    changed = assemble_coupled_generator(
        [A0p, A1p], {(0, 1): K01p, (1, 0): K10p}
    )["generator"]

    assert np.allclose(_sorted_spectrum(base), _sorted_spectrum(changed), rtol=1e-10, atol=1e-10)


def test_equal_edge_norms_do_not_imply_equal_feedback_return_operator():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)

    position_to_acceleration = np.array([[0.0, 0.0], [1.0, 0.0]])
    velocity_to_acceleration = np.array([[0.0, 0.0], [0.0, 1.0]])
    g = 8.0

    Kx = g * position_to_acceleration
    Kv = g * velocity_to_acceleration
    assert np.isclose(np.linalg.norm(Kx, 2), np.linalg.norm(Kv, 2))

    sx = feedback_return_operator(A0, A1, Kx, Kx, s=1j * 2.0 * np.pi * 3.0)
    sv = feedback_return_operator(A0, A1, Kv, Kv, s=1j * 2.0 * np.pi * 3.0)

    assert not np.allclose(sx, sv)


def test_equal_edge_norms_with_different_transformations_reorganize_spectrum_differently():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)

    mx = np.array([[0.0, 0.0], [1.0, 0.0]])
    mv = np.array([[0.0, 0.0], [0.0, 1.0]])
    g = 8.0

    Ax = assemble_coupled_generator(
        [A0, A1], {(0, 1): g * mx, (1, 0): g * mx}
    )["generator"]
    Av = assemble_coupled_generator(
        [A0, A1], {(0, 1): g * mv, (1, 0): g * mv}
    )["generator"]

    assert np.isclose(np.linalg.norm(g * mx, 2), np.linalg.norm(g * mv, 2))
    assert not np.allclose(_sorted_spectrum(Ax), _sorted_spectrum(Av))
