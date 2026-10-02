"""Exact continuous-lineage known-truth contracts for NSD Bio Chi.

Qualification only. These tests construct continuous-time C-family truths,
sample them exactly, and verify lineage invariants and refusal-family geometry.
They do not modify A0/A1/A2 and do not license real EEG local chi.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
from scipy.linalg import expm


def _construct_c_truth(
    *,
    regime: str,
    A: float,
    alpha: float,
    nu: float,
    g: float,
    dt: float,
):
    if not 0.0 < A <= 1.0:
        raise ValueError("A must lie in (0,1]")
    if alpha <= 0.0 or dt <= 0.0:
        raise ValueError("alpha and dt must be positive")
    if not -1.0 <= g <= 1.0:
        raise ValueError("C-family truth requires |g|<=1")
    if regime not in {"under", "critical", "over"}:
        raise ValueError("unknown regime")

    if regime == "under":
        if nu <= 0.0:
            raise ValueError("underdamped nu must be positive")
        delta = nu * nu
    elif regime == "critical":
        delta = 0.0
        nu = 0.0
    else:
        if not 0.0 < nu < alpha:
            raise ValueError("stable overdamped truth requires 0<nu<alpha")
        delta = -(nu * nu)

    G = g * A * alpha
    D = A * (2.0 * alpha * alpha + delta)
    K = np.asarray([[-alpha, -1.0], [delta, -alpha]], dtype=float)
    P = np.asarray([[A, -G], [-G, D]], dtype=float)
    Qc = -(K @ P + P @ K.T)

    F = expm(K * dt)
    Qd = P - F @ P @ F.T

    L = alpha * dt
    rho = math.exp(-L)
    if regime == "under":
        theta = nu * dt
        if not theta < math.pi:
            raise ValueError("truth is not on the licensed alias-safe branch")
        xi = math.cos(theta)
        H = G * math.sin(theta) / nu
        chi = alpha / math.sqrt(alpha * alpha + nu * nu)
    elif regime == "critical":
        xi = 1.0
        H = G * dt
        chi = 1.0
    else:
        psi = nu * dt
        xi = math.cosh(psi)
        H = G * math.sinh(psi) / nu
        chi = alpha / math.sqrt(alpha * alpha - nu * nu)

    return {
        "regime": regime,
        "A": A,
        "alpha": alpha,
        "nu": nu,
        "g": g,
        "G": G,
        "D": D,
        "K": K,
        "P": P,
        "Qc": Qc,
        "F": F,
        "Qd": Qd,
        "dt": dt,
        "L": L,
        "rho": rho,
        "xi": xi,
        "H": H,
        "chi": chi,
    }


def _g_from_discrete(truth) -> float:
    A = truth["A"]
    H = truth["H"]
    L = truth["L"]
    xi = truth["xi"]
    regime = truth["regime"]

    if regime == "under":
        theta = math.acos(xi)
        return (H / A) * theta / (L * math.sin(theta))
    if regime == "critical":
        return H / (A * L)
    psi = math.acosh(xi)
    return (H / A) * psi / (L * math.sinh(psi))


def _chi_from_discrete(truth) -> float:
    L = truth["L"]
    xi = truth["xi"]
    regime = truth["regime"]

    if regime == "under":
        theta = math.acos(xi)
        return L / math.sqrt(L * L + theta * theta)
    if regime == "critical":
        return 1.0
    psi = math.acosh(xi)
    return L / math.sqrt(L * L - psi * psi)


def _decimated_coordinates(truth, m: int):
    regime = truth["regime"]
    A = truth["A"]
    rho = truth["rho"]
    H = truth["H"]
    xi = truth["xi"]

    if regime == "under":
        theta = math.acos(xi)
        factor = math.sin(m * theta) / math.sin(theta)
        xi_m = math.cos(m * theta)
    elif regime == "critical":
        factor = float(m)
        xi_m = 1.0
    else:
        psi = math.acosh(xi)
        factor = math.sinh(m * psi) / math.sinh(psi)
        xi_m = math.cosh(m * psi)

    return {
        **truth,
        "A": A,
        "rho": rho**m,
        "L": m * truth["L"],
        "xi": xi_m,
        "H": H * factor,
        "dt": m * truth["dt"],
    }


@pytest.mark.parametrize("regime,nu", [("under", 4.0), ("critical", 0.0), ("over", 0.6)])
@pytest.mark.parametrize("g", [-0.6, 0.0, 0.6])
def test_c_truth_has_psd_diffusion_and_exact_stationary_discretization(regime, nu, g):
    truth = _construct_c_truth(
        regime=regime,
        A=0.8,
        alpha=1.0,
        nu=nu,
        g=g,
        dt=1.0 / 128.0,
    )

    assert np.min(np.linalg.eigvalsh(truth["P"])) >= -1e-12
    assert np.min(np.linalg.eigvalsh(truth["Qc"])) >= -1e-12
    assert np.min(np.linalg.eigvalsh(truth["Qd"])) >= -1e-12

    rebuilt = truth["F"] @ truth["P"] @ truth["F"].T + truth["Qd"]
    np.testing.assert_allclose(rebuilt, truth["P"], rtol=2e-11, atol=2e-11)


@pytest.mark.parametrize("regime,nu", [("under", 4.0), ("critical", 0.0), ("over", 0.6)])
@pytest.mark.parametrize("g", [-0.7, 0.7])
def test_chi_and_g_are_exact_alias_safe_decimation_invariants(regime, nu, g):
    truth = _construct_c_truth(
        regime=regime,
        A=0.8,
        alpha=1.0,
        nu=nu,
        g=g,
        dt=1.0 / 256.0,
    )
    coarse = _decimated_coordinates(truth, 4)

    if regime == "under":
        assert 4 * math.acos(truth["xi"]) < math.pi

    assert _g_from_discrete(truth) == pytest.approx(g, rel=2e-12, abs=2e-12)
    assert _g_from_discrete(coarse) == pytest.approx(g, rel=2e-12, abs=2e-12)
    assert _chi_from_discrete(coarse) == pytest.approx(
        _chi_from_discrete(truth), rel=2e-12, abs=2e-12
    )


@pytest.mark.parametrize("regime,nu", [("under", 4.0), ("critical", 0.0), ("over", 0.6)])
def test_exact_process_covariance_obeys_m_step_semigroup(regime, nu):
    truth = _construct_c_truth(
        regime=regime,
        A=0.8,
        alpha=1.0,
        nu=nu,
        g=0.5,
        dt=1.0 / 128.0,
    )
    m = 5
    F = truth["F"]
    Qd = truth["Qd"]
    Fm = np.linalg.matrix_power(F, m)

    summed = np.zeros_like(Qd)
    Fj = np.eye(F.shape[0])
    for _ in range(m):
        summed += Fj @ Qd @ Fj.T
        Fj = F @ Fj

    direct = truth["P"] - Fm @ truth["P"] @ Fm.T
    np.testing.assert_allclose(summed, direct, rtol=3e-11, atol=3e-11)


@pytest.mark.parametrize("regime,nu", [("under", 4.0), ("critical", 0.0), ("over", 0.6)])
def test_nonzero_g_c_truth_is_inside_continuous_and_discrete_images(regime, nu):
    truth = _construct_c_truth(
        regime=regime,
        A=0.8,
        alpha=1.0,
        nu=nu,
        g=0.75,
        dt=1.0 / 128.0,
    )

    H_D = truth["A"] * math.sinh(truth["L"])
    assert abs(_g_from_discrete(truth)) < 1.0
    assert abs(truth["H"]) < H_D


def test_nonzero_g_truth_exposes_current_a1_b0_nuisance_restriction():
    truth = _construct_c_truth(
        regime="under",
        A=0.8,
        alpha=1.0,
        nu=4.0,
        g=0.6,
        dt=1.0 / 256.0,
    )

    assert truth["H"] != pytest.approx(0.0, abs=1e-14)
    assert abs(_g_from_discrete(truth)) < 1.0
    # Current A1 fixes the covariance-phase degree to H=0/B=0.
    # This test records the known-truth mismatch without changing A1.
