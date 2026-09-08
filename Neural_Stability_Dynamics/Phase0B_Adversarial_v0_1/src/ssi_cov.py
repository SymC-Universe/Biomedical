from __future__ import annotations
import numpy as np


def output_covariances(Y, max_lag):
    n, p = Y.shape
    out = []
    for lag in range(1, max_lag + 1):
        out.append((Y[lag:].T @ Y[:-lag]) / (n - lag))
    return out


def decompose(Y, block_rows):
    Y = np.asarray(Y, float)
    if Y.ndim != 2:
        raise ValueError("Y must be samples x channels")
    n, p = Y.shape
    if n < 20 * block_rows:
        raise ValueError("record too short")
    covs = output_covariances(Y, 2 * block_rows)
    H = np.empty((p * block_rows, p * block_rows))
    for i in range(block_rows):
        for j in range(block_rows):
            H[i * p:(i + 1) * p, j * p:(j + 1) * p] = covs[i + j]
    U, S, Vh = np.linalg.svd(H, full_matrices=False)
    return U, S, p


def fit_from_decomposition(U, S, p, order, dt):
    if order <= 0 or order >= len(S):
        raise ValueError("invalid order")
    O = U[:, :order] @ np.diag(np.sqrt(np.maximum(S[:order], 0)))
    C = O[:p, :]
    F = np.linalg.pinv(O[:-p, :]) @ O[p:, :]
    vals_d, vecs = np.linalg.eig(F)
    vals_c = np.log(vals_d.astype(complex)) / dt
    shapes = C @ vecs
    return vals_c, shapes
