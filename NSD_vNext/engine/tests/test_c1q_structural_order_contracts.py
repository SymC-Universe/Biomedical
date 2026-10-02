"""Exact structural-order contracts for C1Q qualification.

These contracts separate two questions that ordinary BIC competition confounds:

1. Does the scalar positive-lag covariance have the second-order recurrence
   required by a single white-driven oscillator lineage?
2. If it does, is that second-order law actually inside continuous lineage C?

The first question can reject extra-pole / memory contamination but cannot
distinguish C from D\C or S\D because all three share the same second-order
denominator. The second question therefore remains a separate semantic
lineage/image-membership qualification.

No finite-sample threshold or real-EEG admission is defined here.
"""

from __future__ import annotations

import math

import numpy as np
import pytest


def _chebyshev_t(n: int, x: float) -> float:
    if n == 0:
        return 1.0
    if n == 1:
        return float(x)
    a, b = 1.0, float(x)
    for _ in range(2, n + 1):
        a, b = b, 2.0 * x * b - a
    return b


def _chebyshev_u(n: int, x: float) -> float:
    if n == 0:
        return 1.0
    if n == 1:
        return 2.0 * float(x)
    a, b = 1.0, 2.0 * float(x)
    for _ in range(2, n + 1):
        a, b = b, 2.0 * x * b - a
    return b


def _second_order_covariance(
    k: int,
    *,
    A: float,
    rho: float,
    xi: float,
    H: float,
) -> float:
    if k < 1:
        raise ValueError("positive lags only")
    return rho**k * (
        A * _chebyshev_t(k, xi)
        + H * _chebyshev_u(k - 1, xi)
    )


def _second_order_residual(
    gamma_k: float,
    gamma_k1: float,
    gamma_k2: float,
    *,
    rho: float,
    xi: float,
) -> float:
    return gamma_k2 - 2.0 * rho * xi * gamma_k1 + rho * rho * gamma_k


def _hankel(sequence, *, start: int, size: int) -> np.ndarray:
    return np.asarray(
        [
            [sequence[start + row + col] for col in range(size)]
            for row in range(size)
        ],
        dtype=float,
    )


def _residual_spectrum_minimum(A: float, rho: float, xi: float, H: float) -> float:
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

    def poly(x: float) -> float:
        return 4.0 * q2 * x * x + 2.0 * q1 * x + q0 - 2.0 * q2

    candidates = [-1.0, 1.0]
    if q2 > 0.0:
        vertex = -q1 / (4.0 * q2)
        if -1.0 <= vertex <= 1.0:
            candidates.append(vertex)
    return float(min(poly(x) for x in candidates))


def _reference_coordinates():
    fs = 128.0
    A = 0.8
    natural_frequency_hz = 10.0
    zeta = 0.30

    omega_n = 2.0 * math.pi * natural_frequency_hz
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / fs
    rho = math.exp(-L)
    theta = nu / fs
    xi = math.cos(theta)
    H_C = A * L * math.sin(theta) / theta
    H_D = A * math.sinh(L)
    return A, rho, xi, H_C, H_D


@pytest.mark.parametrize("truth_class", ["C", "D_not_C", "S_not_D"])
def test_all_white_second_order_scalar_families_share_the_same_order_two_recurrence(
    truth_class: str,
):
    A, rho, xi, H_C, H_D = _reference_coordinates()
    if truth_class == "C":
        H = 0.5 * H_C
    elif truth_class == "D_not_C":
        H = H_C + 0.5 * (H_D - H_C)
    else:
        H = 0.18

    assert _residual_spectrum_minimum(A, rho, xi, H) > 0.0
    if truth_class == "C":
        assert abs(H) < H_C
    elif truth_class == "D_not_C":
        assert H_C < abs(H) < H_D
    else:
        assert abs(H) > H_D

    gamma = {
        k: _second_order_covariance(k, A=A, rho=rho, xi=xi, H=H)
        for k in range(1, 14)
    }

    residuals = [
        _second_order_residual(
            gamma[k],
            gamma[k + 1],
            gamma[k + 2],
            rho=rho,
            xi=xi,
        )
        for k in range(1, 11)
    ]
    assert max(abs(value) for value in residuals) < 2e-12

    h3 = _hankel(gamma, start=1, size=3)
    assert abs(float(np.linalg.det(h3))) < 2e-12


def test_colored_extra_pole_is_generically_rank_three_not_rank_two():
    rho = 0.88
    theta = 0.43
    xi = math.cos(theta)
    phi = 0.70
    oscillator_weight = 0.75
    colored_weight = 0.25

    gamma = {}
    for k in range(1, 16):
        gamma[k] = (
            oscillator_weight * rho**k * math.cos(k * theta)
            + colored_weight * phi**k
        )

    order_two_residuals = [
        _second_order_residual(
            gamma[k],
            gamma[k + 1],
            gamma[k + 2],
            rho=rho,
            xi=xi,
        )
        for k in range(1, 12)
    ]
    assert max(abs(value) for value in order_two_residuals) > 1e-4

    h3 = _hankel(gamma, start=1, size=3)
    assert abs(float(np.linalg.det(h3))) > 1e-8

    a = 2.0 * rho * xi
    b = rho * rho
    third_order_residuals = []
    for k in range(1, 11):
        value = (
            gamma[k + 3]
            - (a + phi) * gamma[k + 2]
            + (b + a * phi) * gamma[k + 1]
            - b * phi * gamma[k]
        )
        third_order_residuals.append(value)
    assert max(abs(value) for value in third_order_residuals) < 2e-12

    h4 = _hankel(gamma, start=1, size=4)
    assert abs(float(np.linalg.det(h4))) < 2e-12


def test_recurrence_order_cannot_certify_continuous_lineage_membership():
    """Exact order-two adequacy is necessary for C1Q, not sufficient for C."""
    A, rho, xi, H_C, H_D = _reference_coordinates()
    representatives = {
        "C": 0.5 * H_C,
        "D_not_C": H_C + 0.5 * (H_D - H_C),
        "S_not_D": 0.18,
    }

    ranks = {}
    for label, H in representatives.items():
        gamma = {
            k: _second_order_covariance(k, A=A, rho=rho, xi=xi, H=H)
            for k in range(1, 10)
        }
        matrix = _hankel(gamma, start=1, size=3)
        ranks[label] = np.linalg.matrix_rank(matrix, tol=1e-10)

    assert ranks == {"C": 2, "D_not_C": 2, "S_not_D": 2}
