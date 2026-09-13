from __future__ import annotations

"""Derivation hardening for the approved G1 Chi_bio candidate family.

This module does not compute a biological Chi_bio value. It tests when the
model-native unity boundary used by the Guo-Amir-style normalized interaction
construction survives transfer to a more general transcriptomic regulatory
state with an explicit restoring operator.

The central safety rule is that, for a general continuous-time system

    dx/dt = P(x) - R x,

with production/regulatory Jacobian K = dP/dx and restoring matrix R, the local
Jacobian is J = K - R.  The tempting normalized matrix M = R^{-1} K does *not*
in general satisfy alpha(J) < 0 iff alpha(M) < 1 when R is heterogeneous and K
is directed/non-normal.  Code below makes the exact sufficient cases explicit
and gives the general Jacobian truth separately.
"""

from dataclasses import dataclass

import numpy as np

from src.chi_bio_candidate_math import spectral_abscissa


@dataclass(frozen=True)
class G1HardeningAudit:
    jacobian_spectral_abscissa: float
    naive_left_normalized_abscissa: float
    scalar_restoration_exact: bool
    symmetric_generalized_exact: bool
    exact_unity_route: str


def _real_square_finite(matrix: np.ndarray, name: str) -> np.ndarray:
    arr = np.asarray(matrix, dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
        raise ValueError(f"{name} must be a nonempty square 2D array")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr


def _same_shape(a: np.ndarray, b: np.ndarray) -> None:
    if a.shape != b.shape:
        raise ValueError("production and restoration matrices must have the same shape")


def local_jacobian(production_jacobian: np.ndarray, restoration: np.ndarray) -> np.ndarray:
    """Return J = K - R for the local continuous-time linearization."""

    k = _real_square_finite(production_jacobian, "production_jacobian")
    r = _real_square_finite(restoration, "restoration")
    _same_shape(k, r)
    return k - r


def naive_left_normalized_interaction(
    production_jacobian: np.ndarray, restoration: np.ndarray
) -> np.ndarray:
    """Return M = R^{-1} K.

    This object is useful diagnostically, but alpha(M)=1 is *not* a general
    local-stability boundary for heterogeneous directed systems.
    """

    k = _real_square_finite(production_jacobian, "production_jacobian")
    r = _real_square_finite(restoration, "restoration")
    _same_shape(k, r)
    try:
        return np.linalg.solve(r, k)
    except np.linalg.LinAlgError as exc:
        raise ValueError("restoration matrix must be nonsingular") from exc


def is_positive_scalar_identity(restoration: np.ndarray, *, tolerance: float = 1e-10) -> bool:
    """Return True only when R is beta*I with beta>0 within tolerance."""

    r = _real_square_finite(restoration, "restoration")
    if tolerance < 0 or not np.isfinite(tolerance):
        raise ValueError("tolerance must be finite and nonnegative")
    beta = float(np.trace(r) / r.shape[0])
    if beta <= 0:
        return False
    return bool(np.allclose(r, beta * np.eye(r.shape[0]), atol=tolerance, rtol=0.0))


def scalar_restoration_g1_value(
    production_jacobian: np.ndarray,
    restoration: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> float:
    """Exact G1 value for the common-restoration case R=beta*I.

    For this restricted model class J = beta(M-I), so
    alpha(J) = beta*(alpha(M)-1) exactly and unity is the local stability
    boundary.
    """

    k = _real_square_finite(production_jacobian, "production_jacobian")
    r = _real_square_finite(restoration, "restoration")
    _same_shape(k, r)
    if not is_positive_scalar_identity(r, tolerance=tolerance):
        raise ValueError("exact scalar-restoration G1 requires restoration = beta*I with beta>0")
    beta = float(np.trace(r) / r.shape[0])
    return spectral_abscissa(k / beta)


def _is_symmetric(arr: np.ndarray, tolerance: float) -> bool:
    return bool(np.allclose(arr, arr.T, atol=tolerance, rtol=0.0))


def symmetric_generalized_g1_value(
    production_jacobian: np.ndarray,
    restoration: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> float:
    """Return the exact generalized unity coordinate for symmetric K and SPD R.

    If K=K.T and R is symmetric positive definite, J=K-R is symmetric and
    Sylvester inertia gives

        J negative definite  iff  lambda_max(R^-1/2 K R^-1/2) < 1.

    This is an exact unity boundary for that gradient-like/symmetric model
    class. It is not licensed for a directed regulatory operator.
    """

    k = _real_square_finite(production_jacobian, "production_jacobian")
    r = _real_square_finite(restoration, "restoration")
    _same_shape(k, r)
    if tolerance < 0 or not np.isfinite(tolerance):
        raise ValueError("tolerance must be finite and nonnegative")
    if not _is_symmetric(k, tolerance):
        raise ValueError("symmetric generalized G1 requires a symmetric production Jacobian")
    if not _is_symmetric(r, tolerance):
        raise ValueError("symmetric generalized G1 requires a symmetric restoration matrix")
    evals_r, evecs_r = np.linalg.eigh(r)
    if float(np.min(evals_r)) <= tolerance:
        raise ValueError("symmetric generalized G1 requires restoration positive definite")
    invsqrt = (evecs_r * (1.0 / np.sqrt(evals_r))) @ evecs_r.T
    normalized = invsqrt @ k @ invsqrt
    normalized = 0.5 * (normalized + normalized.T)
    return float(np.max(np.linalg.eigvalsh(normalized)))


def g1_hardening_audit(
    production_jacobian: np.ndarray,
    restoration: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> G1HardeningAudit:
    """Audit whether a proposed G1 unity route is exact for the supplied class."""

    k = _real_square_finite(production_jacobian, "production_jacobian")
    r = _real_square_finite(restoration, "restoration")
    _same_shape(k, r)

    j_alpha = spectral_abscissa(local_jacobian(k, r))
    naive_alpha = spectral_abscissa(naive_left_normalized_interaction(k, r))

    scalar_exact = is_positive_scalar_identity(r, tolerance=tolerance)
    symmetric_exact = False
    if _is_symmetric(k, tolerance) and _is_symmetric(r, tolerance):
        try:
            symmetric_generalized_g1_value(k, r, tolerance=tolerance)
            symmetric_exact = True
        except ValueError:
            symmetric_exact = False

    if scalar_exact:
        route = "COMMON_RESTORATION_EXACT"
    elif symmetric_exact:
        route = "SYMMETRIC_GENERALIZED_EXACT"
    else:
        route = "NO_EXACT_UNITY_ROUTE_FROM_NAIVE_NORMALIZATION"

    return G1HardeningAudit(
        jacobian_spectral_abscissa=j_alpha,
        naive_left_normalized_abscissa=naive_alpha,
        scalar_restoration_exact=scalar_exact,
        symmetric_generalized_exact=symmetric_exact,
        exact_unity_route=route,
    )
