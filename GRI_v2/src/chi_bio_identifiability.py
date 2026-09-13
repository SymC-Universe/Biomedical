from __future__ import annotations

"""Algebraic identifiability checks for frozen Chi_bio candidate families.

No function in this module infers a biological operator from cancer data. The
purpose is to expose what can and cannot be identified even if an effective
local Jacobian or transition operator were known exactly.
"""

import numpy as np

from src.chi_bio_candidate_math import spectral_abscissa


def _real_square_finite(matrix: np.ndarray, name: str = "matrix") -> np.ndarray:
    arr = np.asarray(matrix, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
        raise ValueError(f"{name} must be a nonempty square 2D array")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr


def g1a_value_from_known_jacobian_and_beta(jacobian: np.ndarray, *, beta: float) -> float:
    """Return the G1A value implied by a known J and an independently known beta.

    Under the G1A restriction R=beta*I and J=K-beta*I,

        M = K/beta = I + J/beta
        alpha(M) = 1 + alpha(J)/beta.

    Thus the stability side of unity follows from alpha(J), but the numerical
    G1A value is not identified unless beta is identified independently.
    """

    j = _real_square_finite(jacobian, "jacobian")
    if not np.isfinite(beta) or beta <= 0:
        raise ValueError("beta must be finite and strictly positive")
    return float(1.0 + spectral_abscissa(j) / beta)


def g1a_values_across_restoration_scales(
    jacobian: np.ndarray, betas: list[float] | tuple[float, ...]
) -> tuple[float, ...]:
    if len(betas) == 0:
        raise ValueError("betas must be nonempty")
    return tuple(g1a_value_from_known_jacobian_and_beta(jacobian, beta=float(b)) for b in betas)


def g2_reference_interval_value(
    transition_spectral_radius: float,
    *,
    observed_interval: float,
    reference_interval: float = 1.0,
) -> float:
    """Convert rho(T_Delta) to a fixed reference interval under semigroup dynamics.

    If T_Delta = exp(J*Delta) for a time-invariant linear system, then
    rho(T_Delta) = exp(alpha(J)*Delta). Raising the radius to
    reference_interval/observed_interval expresses the multiplier over one
    frozen reference interval while preserving the exact unity boundary.

    This conversion is not licensed when the time-invariant semigroup
    assumption is not supported.
    """

    rho = float(transition_spectral_radius)
    if not np.isfinite(rho) or rho <= 0:
        raise ValueError("transition_spectral_radius must be finite and > 0")
    if not np.isfinite(observed_interval) or observed_interval <= 0:
        raise ValueError("observed_interval must be finite and > 0")
    if not np.isfinite(reference_interval) or reference_interval <= 0:
        raise ValueError("reference_interval must be finite and > 0")
    return float(rho ** (reference_interval / observed_interval))


def transition_parameter_count(
    state_dimension: int,
    *,
    exogenous_input_dimension: int = 0,
    include_intercept: bool = False,
) -> int:
    """Number of free coefficients in x_next = T x + B u + c."""

    d = int(state_dimension)
    q = int(exogenous_input_dimension)
    if d <= 0 or q < 0:
        raise ValueError("state_dimension must be >0 and exogenous_input_dimension >=0")
    predictors = d + q + (1 if include_intercept else 0)
    return d * predictors


def formal_state_dimension_rank_ceiling(
    n_transitions: int,
    *,
    exogenous_input_dimension: int = 0,
    include_intercept: bool = False,
) -> int:
    """Best-case predictor-rank ceiling for unregularized transition regression.

    This is only a necessary algebraic ceiling: it assumes full-rank design and
    does not account for serial dependence, pooled samples, collinearity,
    measurement noise, or validation needs.
    """

    n = int(n_transitions)
    q = int(exogenous_input_dimension)
    if n <= 0 or q < 0:
        raise ValueError("n_transitions must be >0 and exogenous_input_dimension >=0")
    fixed = q + (1 if include_intercept else 0)
    return max(0, n - fixed)
