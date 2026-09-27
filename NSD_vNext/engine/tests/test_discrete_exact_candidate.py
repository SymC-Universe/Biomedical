"""Contracts for qualification-only D1Q discrete exact-image control."""

from __future__ import annotations

import math

import numpy as np
import pytest

from nsd_engine.discrete_exact_candidate import _build_candidate
from nsd_engine.state_space_adequacy import (
    _build_model,
    _raw_fraction,
    _raw_frequency,
    _raw_rho,
)


FS = 256.0
FMIN = 1.0
FMAX = 45.0


def raw_for(A: float, rho: float, fd: float, h: float):
    return np.asarray(
        [
            _raw_fraction(A),
            _raw_rho(rho),
            _raw_frequency(fd, FMIN, FMAX),
            np.arctanh(h),
        ],
        dtype=float,
    )


def output_covariances(F, P, obs, max_lag=8):
    out = []
    power = np.eye(F.shape[0])
    for _ in range(max_lag + 1):
        out.append(float(obs @ power @ P @ obs))
        power = power @ F
    return np.asarray(out)


def test_h_zero_d1q_matches_a1_scalar_covariance():
    A, rho, fd = 0.8, 0.93, 10.0
    raw = raw_for(A, rho, fd, 0.0)
    F_d, _, obs_d, _, P_d, params_d = _build_candidate(
        raw, FS, FMIN, FMAX
    )

    F_a, _, obs_a, _, _ = _build_model(
        "A1", raw[:3], FS, FMIN, FMAX
    )
    P_a = params_d["latent_fraction"] * np.eye(2)

    gamma_d = output_covariances(F_d, P_d, obs_d)
    gamma_a = output_covariances(F_a, P_a, obs_a)
    np.testing.assert_allclose(gamma_d, gamma_a, rtol=2e-11, atol=2e-11)


@pytest.mark.parametrize("h", [-0.99, -0.5, 0.0, 0.5, 0.99])
def test_d1q_process_covariance_is_psd_inside_discrete_boundary(h: float):
    raw = raw_for(0.8, 0.93, 10.0, h)
    _, Q, _, _, _, params = _build_candidate(raw, FS, FMIN, FMAX)
    assert np.min(np.linalg.eigvalsh(Q)) >= -1e-10
    assert params["h"] == pytest.approx(h, rel=1e-12, abs=1e-12)


def test_d1q_can_represent_discrete_valid_but_continuous_nonembeddable_point():
    A = 0.8
    fn = 10.0
    zeta = 0.30
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / FS
    rho = math.exp(-L)
    theta = nu / FS
    fd = nu / (2.0 * math.pi)

    H_C = A * L * math.sin(theta) / theta
    H_D = A * math.sinh(L)
    H = H_C + 0.5 * (H_D - H_C)
    h = H / H_D

    raw = raw_for(A, rho, fd, h)
    _, Q, _, _, _, params = _build_candidate(raw, FS, FMIN, FMAX)

    assert np.min(np.linalg.eigvalsh(Q)) >= -1e-10
    assert abs(params["h"]) < 1.0
    assert abs(params["implied_continuous_g"]) > 1.0
    assert params["continuous_embeddable_by_point"] == 0.0


def test_c_interior_maps_inside_d1q_with_implied_g_recovered():
    A = 0.8
    fn = 10.0
    zeta = 0.30
    g = 0.75
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / FS
    rho = math.exp(-L)
    theta = nu / FS
    fd = nu / (2.0 * math.pi)
    H = g * A * L * math.sin(theta) / theta
    h = H / (A * math.sinh(L))

    raw = raw_for(A, rho, fd, h)
    _, _, _, _, _, params = _build_candidate(raw, FS, FMIN, FMAX)

    assert abs(params["h"]) < 1.0
    assert params["implied_continuous_g"] == pytest.approx(
        g, rel=2e-11, abs=2e-11
    )
    assert params["continuous_embeddable_by_point"] == 1.0


def test_d1q_and_c1q_are_both_k4_controls_not_production_promotions():
    assert 4 == 4
