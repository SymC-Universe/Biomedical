"""Prospective lineage/sampling contracts for NSD Bio Chi.

These tests encode analytic claim boundaries only. They do not alter or license
A0/A1/A2, do not admit real EEG, and do not choose among the continuous-time
embeddable (C), discrete exact-image (D), or scalar-positive (S) families.

The contracts cover:
- exact m-fold covariance decimation,
- sampling-invariant continuous-time nuisance coordinate g,
- sample-rate-specific contraction of the discrete exact-image coordinate h,
- exact Hankel determinant transport and alias-induced order collapse,
- a constructive S\D -> D\C coarse-graining witness.

All formulas are evaluated in the regular recurrence coordinates
(A, rho, xi, H).
"""

from __future__ import annotations

import math

import numpy as np
import pytest


def chebyshev_t(n: int, x: float) -> float:
    if n == 0:
        return 1.0
    if n == 1:
        return float(x)
    t0, t1 = 1.0, float(x)
    for _ in range(2, n + 1):
        t0, t1 = t1, 2.0 * x * t1 - t0
    return t1


def chebyshev_u(n: int, x: float) -> float:
    if n == 0:
        return 1.0
    if n == 1:
        return 2.0 * float(x)
    u0, u1 = 1.0, 2.0 * float(x)
    for _ in range(2, n + 1):
        u0, u1 = u1, 2.0 * x * u1 - u0
    return u1


def covariance_lag(k: int, A: float, rho: float, xi: float, H: float) -> float:
    if k == 0:
        return 1.0
    return rho**k * (
        A * chebyshev_t(k, xi) + H * chebyshev_u(k - 1, xi)
    )


def decimate_coordinates(
    A: float,
    rho: float,
    xi: float,
    H: float,
    m: int,
) -> tuple[float, float, float, float]:
    return (
        A,
        rho**m,
        chebyshev_t(m, xi),
        H * chebyshev_u(m - 1, xi),
    )


def hankel_delta(A: float, rho: float, xi: float, H: float) -> float:
    return rho**4 * (A * A * (xi * xi - 1.0) - H * H)


def discrete_exact_bound(A: float, rho: float) -> float:
    return A * math.sinh(-math.log(rho))


def continuous_g(
    A: float,
    rho: float,
    xi: float,
    H: float,
) -> float:
    L = -math.log(rho)
    if A <= 0.0:
        raise ValueError("A must be positive")

    if xi < 1.0:
        theta = math.acos(xi)
        return (H / A) * theta / (L * math.sin(theta))
    if xi == pytest.approx(1.0, abs=1e-14):
        return H / (A * L)

    psi = math.acosh(xi)
    return (H / A) * psi / (L * math.sinh(psi))


def normalized_discrete_h(A: float, rho: float, H: float) -> float:
    if A <= 0.0:
        raise ValueError("A must be positive")
    return H / discrete_exact_bound(A, rho)


def residual_q(A: float, rho: float, xi: float, H: float) -> tuple[float, float, float]:
    q2 = rho * rho * (1.0 - A)
    q1 = rho * (
        (1.0 + rho * rho) * H
        + xi * (A * (1.0 + 3.0 * rho * rho) - 2.0 * (1.0 + rho * rho))
    )
    q0 = (
        1.0
        + rho**4
        + 4.0 * rho * rho * xi * xi
        - 2.0 * A * rho**4
        - 4.0 * A * rho * rho * xi * xi
        - 4.0 * H * rho * rho * xi
    )
    return q0, q1, q2


def residual_spectrum_minimum(A: float, rho: float, xi: float, H: float) -> float:
    """Exact minimum of q0 + 2 q1 cos(w) + 2 q2 cos(2w) on w in [0, pi]."""
    q0, q1, q2 = residual_q(A, rho, xi, H)

    def poly(x: float) -> float:
        return 4.0 * q2 * x * x + 2.0 * q1 * x + q0 - 2.0 * q2

    candidates = [-1.0, 1.0]
    if q2 > 0.0:
        vertex = -q1 / (4.0 * q2)
        if -1.0 <= vertex <= 1.0:
            candidates.append(vertex)
    return min(poly(x) for x in candidates)


@pytest.mark.parametrize(
    ("xi", "label"),
    [
        (math.cos(0.55), "underdamped"),
        (1.0, "critical"),
        (math.cosh(0.08), "overdamped"),
    ],
)
def test_exact_decimation_preserves_covariance_sequence(xi: float, label: str):
    A, rho, H, m = 0.8, 0.91, 0.035, 3
    A_m, rho_m, xi_m, H_m = decimate_coordinates(A, rho, xi, H, m)

    for coarse_lag in range(1, 8):
        direct = covariance_lag(coarse_lag * m, A, rho, xi, H)
        mapped = covariance_lag(coarse_lag, A_m, rho_m, xi_m, H_m)
        assert mapped == pytest.approx(direct, rel=2e-12, abs=2e-12), label


def test_critical_decimation_scales_H_linearly():
    A, rho, xi, H, m = 0.8, 0.93, 1.0, 0.025, 5
    _, _, xi_m, H_m = decimate_coordinates(A, rho, xi, H, m)

    assert xi_m == pytest.approx(1.0, abs=1e-14)
    assert H_m == pytest.approx(m * H, rel=1e-12)


@pytest.mark.parametrize(
    "xi",
    [
        math.cos(0.45),
        1.0,
        math.cosh(0.06),
    ],
)
def test_continuous_g_is_invariant_under_alias_safe_decimation(xi: float):
    A, rho, H, m = 0.8, 0.92, 0.025, 3
    if xi < 1.0:
        theta = math.acos(xi)
        assert m * theta < math.pi
    elif xi > 1.0:
        assert m * math.acosh(xi) < m * (-math.log(rho))

    fine_g = continuous_g(A, rho, xi, H)
    A_m, rho_m, xi_m, H_m = decimate_coordinates(A, rho, xi, H, m)
    coarse_g = continuous_g(A_m, rho_m, xi_m, H_m)

    assert coarse_g == pytest.approx(fine_g, rel=2e-12, abs=2e-12)


@pytest.mark.parametrize(
    "xi",
    [
        math.cos(0.60),
        1.0,
        math.cosh(0.07),
    ],
)
def test_discrete_exact_coordinate_contracts_under_coarsening(xi: float):
    A, rho, H, m = 0.8, 0.90, 0.04, 3
    if xi < 1.0:
        assert m * math.acos(xi) < math.pi
    else:
        assert xi < math.cosh(-math.log(rho))

    fine_h = abs(normalized_discrete_h(A, rho, H))
    A_m, rho_m, _, H_m = decimate_coordinates(A, rho, xi, H, m)
    coarse_h = abs(normalized_discrete_h(A_m, rho_m, H_m))

    assert coarse_h < fine_h


@pytest.mark.parametrize(
    "xi",
    [
        math.cos(0.52),
        1.0,
        math.cosh(0.05),
    ],
)
def test_hankel_determinant_obeys_exact_decimation_law(xi: float):
    A, rho, H, m = 0.8, 0.91, 0.03, 4
    fine_delta = hankel_delta(A, rho, xi, H)
    A_m, rho_m, xi_m, H_m = decimate_coordinates(A, rho, xi, H, m)
    coarse_delta = hankel_delta(A_m, rho_m, xi_m, H_m)

    expected = (
        rho ** (4 * (m - 1))
        * chebyshev_u(m - 1, xi) ** 2
        * fine_delta
    )
    assert coarse_delta == pytest.approx(expected, rel=3e-12, abs=3e-12)


def test_alias_decimation_can_collapse_fine_second_order_covariance_to_rank_one():
    A, rho, H, m = 0.8, 0.90, 0.03, 3
    theta = math.pi / m
    xi = math.cos(theta)

    fine_delta = hankel_delta(A, rho, xi, H)
    assert abs(fine_delta) > 1e-6

    A_m, rho_m, xi_m, H_m = decimate_coordinates(A, rho, xi, H, m)
    coarse_delta = hankel_delta(A_m, rho_m, xi_m, H_m)

    assert chebyshev_u(m - 1, xi) == pytest.approx(0.0, abs=1e-12)
    assert abs(coarse_delta) < 1e-12


def test_critical_and_overdamped_decimation_do_not_create_rank_loss():
    cases = [
        (1.0, 0.03),
        (math.cosh(0.06), 0.03),
    ]
    A, rho, m = 0.8, 0.90, 4

    for xi, H in cases:
        fine_delta = hankel_delta(A, rho, xi, H)
        assert abs(fine_delta) > 1e-7

        A_m, rho_m, xi_m, H_m = decimate_coordinates(A, rho, xi, H, m)
        coarse_delta = hankel_delta(A_m, rho_m, xi_m, H_m)
        assert abs(coarse_delta) > 1e-10


def test_scalar_positive_fine_law_can_enter_discrete_exact_image_after_decimation():
    """Constructive S\D -> D\C witness from the frozen predecision analysis."""
    A = 0.8
    rho = 0.9
    theta = 0.8
    xi = math.cos(theta)
    H = 0.09
    m = 3

    fine_D_bound = discrete_exact_bound(A, rho)
    fine_g = continuous_g(A, rho, xi, H)
    fine_spectral_min = residual_spectrum_minimum(A, rho, xi, H)

    assert H > fine_D_bound
    assert abs(fine_g) > 1.0
    assert fine_spectral_min > 0.0

    assert m * theta < math.pi
    A_m, rho_m, xi_m, H_m = decimate_coordinates(A, rho, xi, H, m)
    coarse_D_bound = discrete_exact_bound(A_m, rho_m)
    coarse_g = continuous_g(A_m, rho_m, xi_m, H_m)

    assert abs(H_m) < coarse_D_bound
    assert abs(coarse_g) > 1.0
    assert coarse_g == pytest.approx(fine_g, rel=2e-12, abs=2e-12)


def test_a1_isotropic_lineage_sits_inside_C_D_and_S():
    A = 0.8
    rho = 0.90
    theta = 0.55
    xi = math.cos(theta)
    H = 0.0

    assert abs(continuous_g(A, rho, xi, H)) < 1.0
    assert abs(H) < discrete_exact_bound(A, rho)
    assert residual_spectrum_minimum(A, rho, xi, H) > 0.0
