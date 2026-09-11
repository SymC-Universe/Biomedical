from __future__ import annotations

import numpy as np
from scipy.linalg import expm

from src.chi_conglomerate import second_order_generator
from src.coupled_conglomeration import assemble_coupled_generator


def _sorted_poles(A):
    vals = np.linalg.eigvals(A)
    return np.array(sorted(vals, key=lambda z: (round(float(z.real), 10), round(float(z.imag), 10))))


def test_one_way_coupling_preserves_union_spectrum():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    M = np.array([[0.0, 0.0], [1.0, 0.0]])
    uncoupled = assemble_coupled_generator([A0, A1], {})["generator"]
    one_way = assemble_coupled_generator([A0, A1], {(1, 0): 12.0 * M})["generator"]
    assert np.allclose(_sorted_poles(uncoupled), _sorted_poles(one_way), rtol=1e-10, atol=1e-10)


def test_closed_loop_coupling_changes_global_spectrum():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    M = np.array([[0.0, 0.0], [1.0, 0.0]])
    uncoupled = assemble_coupled_generator([A0, A1], {})["generator"]
    closed = assemble_coupled_generator(
        [A0, A1], {(1, 0): 12.0 * M, (0, 1): 12.0 * M}
    )["generator"]
    assert not np.allclose(_sorted_poles(uncoupled), _sorted_poles(closed), rtol=1e-7, atol=1e-7)


def test_matrix_exponential_starts_at_identity():
    A = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    assert np.allclose(expm(A * 0.0), np.eye(2), atol=1e-15)


def test_selected_surface_is_asymptotically_stable():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    M = np.array([[0.0, 0.0], [1.0, 0.0]])
    for g in [0.0, 4.0, 8.0, 12.0, 14.0, 18.0, 22.0]:
        couplings = {} if g == 0 else {(1, 0): g * M, (0, 1): g * M}
        A = assemble_coupled_generator([A0, A1], couplings)["generator"]
        assert float(np.max(np.linalg.eigvals(A).real)) < 0.0
