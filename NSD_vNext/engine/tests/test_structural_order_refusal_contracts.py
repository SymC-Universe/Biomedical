"""Exact structural-order refusal contracts for NSD Bio Chi.

Qualification only. These tests separate genuine second-order lineage from an
additional colored/memory pole using exact covariance identities. No
finite-sample threshold is defined.

For a second-order covariance recurrence
    gamma[k+2] = a gamma[k+1] - b gamma[k],
the recurrence residual is identically zero and every 3x3 Hankel matrix formed
from consecutive positive lags has rank <= 2.

Adding a distinct third exponential pole generically gives rank 3 and a
nonzero recurrence residual. This is the structural failure exposed by the
colored-process control that C1Q can otherwise approximate well.
"""

from __future__ import annotations

import cmath
import math

import numpy as np
import pytest


def second_order_covariance(
    k: int,
    *,
    A: float,
    rho: float,
    xi: float,
    H: float,
) -> float:
    if k < 0:
        raise ValueError("k must be non-negative")
    if k == 0:
        return 1.0

    if abs(xi) < 1.0:
        theta = math.acos(xi)
        return rho**k * (
            A * math.cos(k * theta)
            + H * math.sin(k * theta) / math.sin(theta)
        )
    if xi == pytest.approx(1.0, abs=1e-14):
        return rho**k * (A + H * k)

    psi = math.acosh(xi)
    return rho**k * (
        A * math.cosh(k * psi)
        + H * math.sinh(k * psi) / math.sinh(psi)
    )


def recurrence_residual(gamma, k: int, a: float, b: float) -> float:
    return float(gamma(k + 2) - a * gamma(k + 1) + b * gamma(k))


def hankel3(gamma, start: int = 1) -> np.ndarray:
    return np.asarray(
        [[gamma(start + i + j) for j in range(3)] for i in range(3)],
        dtype=float,
    )


@pytest.mark.parametrize(
    "xi",
    [
        math.cos(0.45),
        1.0,
        math.cosh(0.06),
    ],
)
def test_exact_second_order_law_has_zero_third_order_hankel_determinant(xi):
    A, rho, H = 0.8, 0.91, 0.03
    if xi > 1.0:
        assert math.acosh(xi) < -math.log(rho)

    gamma = lambda k: second_order_covariance(
        k, A=A, rho=rho, xi=xi, H=H
    )
    matrix = hankel3(gamma)

    assert abs(np.linalg.det(matrix)) < 2e-13
    singular = np.linalg.svd(matrix, compute_uv=False)
    assert singular[-1] < 2e-13


@pytest.mark.parametrize(
    "xi",
    [
        math.cos(0.45),
        1.0,
        math.cosh(0.06),
    ],
)
def test_exact_second_order_recurrence_residual_is_zero(xi):
    A, rho, H = 0.8, 0.91, 0.03
    gamma = lambda k: second_order_covariance(
        k, A=A, rho=rho, xi=xi, H=H
    )
    a = 2.0 * rho * xi
    b = rho * rho

    for k in range(1, 10):
        assert recurrence_residual(gamma, k, a, b) == pytest.approx(
            0.0, abs=3e-13
        )


def test_distinct_third_pole_breaks_second_order_recurrence_exactly():
    fs = 256.0
    fn = 10.0
    zeta = 0.30
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    omega_d = omega_n * math.sqrt(1.0 - zeta * zeta)
    rho = math.exp(-alpha / fs)
    theta = omega_d / fs
    xi = math.cos(theta)
    a = 2.0 * rho * xi
    b = rho * rho

    A = 0.86394453
    B = 0.16609964
    phi = 0.7
    C = -0.06394453

    def gamma(k: int) -> float:
        return (
            rho**k
            * (
                A * math.cos(k * theta)
                + B * math.sin(k * theta)
            )
            + C * phi**k
        )

    factor = phi * phi - a * phi + b
    assert abs(factor) > 1e-4

    for k in range(1, 8):
        expected = C * phi**k * factor
        assert recurrence_residual(gamma, k, a, b) == pytest.approx(
            expected, rel=3e-11, abs=3e-13
        )
        assert abs(expected) > 0.0


def test_frozen_colored_process_covariance_is_generically_rank_three():
    fs = 256.0
    fn = 10.0
    zeta = 0.30
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    omega_d = omega_n * math.sqrt(1.0 - zeta * zeta)
    rho = math.exp(-alpha / fs)
    theta = omega_d / fs

    A = 0.86394453
    B = 0.16609964
    phi = 0.7
    C = -0.06394453

    def gamma(k: int) -> float:
        return (
            rho**k
            * (
                A * math.cos(k * theta)
                + B * math.sin(k * theta)
            )
            + C * phi**k
        )

    matrix = hankel3(gamma)
    determinant = float(np.linalg.det(matrix))
    singular = np.linalg.svd(matrix, compute_uv=False)

    assert abs(determinant) > 1e-7
    assert singular[-1] > 1e-6


def test_three_exponential_hankel_determinant_matches_vandermonde_factorization():
    lambdas = np.asarray(
        [
            0.91 * cmath.exp(0.41j),
            0.91 * cmath.exp(-0.41j),
            0.70 + 0.0j,
        ],
        dtype=complex,
    )
    coefficients = np.asarray(
        [
            0.44 - 0.08j,
            0.44 + 0.08j,
            -0.06 + 0.0j,
        ],
        dtype=complex,
    )

    def gamma(k: int):
        return sum(c * lam**k for c, lam in zip(coefficients, lambdas))

    matrix = np.asarray(
        [[gamma(1 + i + j) for j in range(3)] for i in range(3)],
        dtype=complex,
    )
    direct = np.linalg.det(matrix)

    vandermonde_sq = 1.0 + 0.0j
    for i in range(3):
        for j in range(i + 1, 3):
            vandermonde_sq *= (lambdas[j] - lambdas[i]) ** 2
    expected = (
        np.prod(coefficients)
        * np.prod(lambdas)
        * vandermonde_sq
    )

    assert direct == pytest.approx(expected, rel=2e-11, abs=2e-13)
    assert abs(direct) > 1e-8
