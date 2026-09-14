from __future__ import annotations

"""Exploratory mathematical probes for Chi_bio candidate generator classes.

These functions implement only model-class invariants already derived in the
P0-D G1/G2 notes. They do NOT define the GRI biological state vector, do NOT
construct a GRI operator, and do NOT compute an admitted Chi_bio value.

They exist so candidate mathematics can be checked against known-truth matrices
before any real cancer state representation is selected.
"""

from typing import Literal

import numpy as np


Regime = Literal["BELOW_UNITY", "AT_UNITY_WITHIN_TOLERANCE", "ABOVE_UNITY"]


def _square_finite_matrix(matrix: np.ndarray) -> np.ndarray:
    arr = np.asarray(matrix)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or arr.shape[0] == 0:
        raise ValueError("matrix must be a nonempty square 2D array")
    if not np.all(np.isfinite(arr)):
        raise ValueError("matrix must contain only finite values")
    return arr


def spectral_abscissa(matrix: np.ndarray) -> float:
    """Return max(real(eigenvalue)) for a finite square matrix."""

    arr = _square_finite_matrix(matrix)
    eigvals = np.linalg.eigvals(arr)
    return float(np.max(np.real(eigvals)))


def spectral_radius(matrix: np.ndarray) -> float:
    """Return max(abs(eigenvalue)) for a finite square matrix."""

    arr = _square_finite_matrix(matrix)
    eigvals = np.linalg.eigvals(arr)
    return float(np.max(np.abs(eigvals)))


def unity_regime(value: float, *, tolerance: float = 1e-10) -> Regime:
    """Classify a scalar relative to unity without giving it biological meaning."""

    if not np.isfinite(value):
        raise ValueError("value must be finite")
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    if value < 1.0 - tolerance:
        return "BELOW_UNITY"
    if value > 1.0 + tolerance:
        return "ABOVE_UNITY"
    return "AT_UNITY_WITHIN_TOLERANCE"


def g1_normalized_interaction_value(matrix_m: np.ndarray) -> float:
    """P0-D G1 model-class scalar alpha(M) = max Re eig(M).

    This is not Chi_bio unless a future frozen GRI System Model independently
    licenses the corresponding biological operator M_GRI.
    """

    return spectral_abscissa(matrix_m)


def g1_jacobian_from_normalized_interaction(
    matrix_m: np.ndarray, *, beta0: float
) -> np.ndarray:
    """Return beta0 * (M - I) for the G1 source-model relation."""

    arr = _square_finite_matrix(matrix_m)
    if not np.isfinite(beta0) or beta0 <= 0:
        raise ValueError("beta0 must be finite and strictly positive")
    return beta0 * (arr - np.eye(arr.shape[0], dtype=arr.dtype))


def g2_transition_value(matrix_t: np.ndarray) -> float:
    """P0-D G2 model-class scalar rho(T).

    This is not Chi_bio unless a future frozen GRI System Model independently
    licenses the corresponding biological transition operator T_GRI.
    """

    return spectral_radius(matrix_t)


def largest_singular_value(matrix: np.ndarray) -> float:
    """Return the induced Euclidean one-step gain, useful for nonnormal checks."""

    arr = _square_finite_matrix(matrix)
    return float(np.linalg.svd(arr, compute_uv=False)[0])
