from __future__ import annotations

import numpy as np
from scipy.linalg import expm

from src.chi_conglomerate import second_order_generator
from src.coupled_conglomeration import assemble_coupled_generator


def _build(h):
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.75, 2.0 * np.pi * 5.0)
    A2 = second_order_generator(0.90, 2.0 * np.pi * 7.0)
    M = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float)
    K01 = 4.0 * M
    K10 = 4.0 * M
    K12 = float(h) * M
    K21 = float(h) * M
    Z = np.zeros((2, 2))
    full = np.block([[A0, K01, Z], [K10, A1, K12], [Z, K21, A2]])
    Ae = np.block([[A1, K12], [K21, A2]])
    K0e = np.hstack([K01, Z])
    Ke0 = np.vstack([K10, Z])
    grouped = assemble_coupled_generator([A0, Ae], {(0, 1): K0e, (1, 0): Ke0})["generator"]
    truncated = assemble_coupled_generator([A0, A1], {(0, 1): K01, (1, 0): K10})["generator"]
    return full, grouped, truncated


def test_exact_grouping_preserves_generator():
    full, grouped, _ = _build(6.0)
    assert np.allclose(full, grouped, rtol=0.0, atol=0.0)


def test_exact_grouping_preserves_outer_response():
    full, grouped, _ = _build(10.0)
    x0 = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    for t in [0.0, 0.01, 0.05, 0.1, 0.5, 1.0]:
        yf = (expm(full * t) @ x0)[:2]
        yg = (expm(grouped * t) @ x0)[:2]
        assert np.allclose(yf, yg, rtol=1e-12, atol=1e-12)


def test_truncation_is_exact_when_internal_subsystem_is_decoupled():
    full, _, truncated = _build(0.0)
    xf = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    xt = np.array([1.0, 0.0, 0.0, 0.0])
    for t in [0.0, 0.05, 0.2, 1.0]:
        yf = (expm(full * t) @ xf)[:2]
        yt = (expm(truncated * t) @ xt)[:2]
        assert np.allclose(yf, yt, rtol=1e-11, atol=1e-11)


def test_truncation_changes_outer_response_when_internal_feedback_is_active():
    full, _, truncated = _build(10.0)
    xf = np.array([1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    xt = np.array([1.0, 0.0, 0.0, 0.0])
    errors = []
    for t in [0.05, 0.1, 0.2, 0.5, 1.0]:
        yf = (expm(full * t) @ xf)[:2]
        yt = (expm(truncated * t) @ xt)[:2]
        errors.append(float(np.linalg.norm(yf - yt)))
    assert max(errors) > 1e-6


def test_selected_surface_remains_stable():
    for h in [0.0, 2.0, 4.0, 6.0, 8.0, 10.0]:
        full, grouped, truncated = _build(h)
        assert float(np.max(np.linalg.eigvals(full).real)) < 0.0
        assert float(np.max(np.linalg.eigvals(grouped).real)) < 0.0
        assert float(np.max(np.linalg.eigvals(truncated).real)) < 0.0
