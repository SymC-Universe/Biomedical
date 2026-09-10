from __future__ import annotations
import numpy as np


def fit_linear_predictor(Y_train, ridge=0.0):
    """Fit Y[t+1] = Y[t] A^T by least squares. P0 adequacy diagnostic only."""
    Y = np.asarray(Y_train, float)
    if Y.ndim != 2 or Y.shape[0] < 3:
        raise ValueError("Y_train must be samples x channels")
    X, T = Y[:-1], Y[1:]
    p = X.shape[1]
    G = X.T @ X + float(ridge) * np.eye(p)
    A_t = np.linalg.pinv(G) @ X.T @ T
    return A_t.T


def one_step_residuals(Y, A):
    Y = np.asarray(Y, float)
    A = np.asarray(A, float)
    if Y.ndim != 2 or A.shape != (Y.shape[1], Y.shape[1]):
        raise ValueError("shape mismatch")
    pred = Y[:-1] @ A.T
    return Y[1:] - pred


def normalized_prediction_error(Y, A):
    residual = one_step_residuals(Y, A)
    denom = float(np.sum((Y[1:] - Y[1:].mean(0, keepdims=True)) ** 2))
    if denom <= 0:
        return np.nan
    return float(np.sum(residual ** 2) / denom)


def residual_autocorrelation_energy(residuals, max_lag):
    """Scale-free residual temporal-structure diagnostic.

    Returns summed Frobenius energy of lagged residual correlation matrices.
    It is intentionally a descriptive P0 quantity, not a frozen pass threshold.
    """
    E = np.asarray(residuals, float)
    if E.ndim != 2 or E.shape[0] <= max_lag:
        raise ValueError("insufficient residual samples")
    E = E - E.mean(0, keepdims=True)
    cov0 = (E.T @ E) / E.shape[0]
    d = np.sqrt(np.maximum(np.diag(cov0), 1e-15))
    scale = d[:, None] * d[None, :]
    total = 0.0
    for lag in range(1, int(max_lag) + 1):
        c = (E[lag:].T @ E[:-lag]) / (E.shape[0] - lag)
        r = c / scale
        total += float(np.linalg.norm(r, "fro") ** 2)
    return total


def adequacy_record(train, test, ridge=0.0, max_lag=10):
    A = fit_linear_predictor(train, ridge=ridge)
    train_resid = one_step_residuals(train, A)
    return {
        "status": "P0_DESCRIPTIVE_NOT_ADJUDICATED",
        "spectral_radius_discrete": float(np.max(np.abs(np.linalg.eigvals(A)))),
        "train_residual_autocorrelation_energy": residual_autocorrelation_energy(train_resid, max_lag),
        "test_normalized_prediction_error": normalized_prediction_error(test, A),
    }
