from __future__ import annotations

import numpy as np
from scipy.linalg import expm, solve_discrete_lyapunov


def population_output_covariances(A, C, dt, max_lag, process_scale):
    """Exact stationary positive-lag output covariances for the NSD simulator model."""
    A = np.asarray(A, dtype=float)
    C = np.asarray(C, dtype=float)
    dt = float(dt)
    L = int(max_lag)
    scale = float(process_scale)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be square")
    if C.ndim != 2 or C.shape[1] != A.shape[0]:
        raise ValueError("C dimensions do not match A")
    if dt <= 0.0 or L <= 0 or scale <= 0.0:
        raise ValueError("dt, max_lag and process_scale must be positive")
    F = expm(A * dt)
    if np.max(np.abs(np.linalg.eigvals(F))) >= 1.0:
        raise ValueError("A must generate a stable sampled system")
    Q = scale * scale * dt * np.eye(A.shape[0])
    P = solve_discrete_lyapunov(F, Q)
    P = 0.5 * (P + P.T)
    covs = []
    Fpower = np.eye(A.shape[0])
    for lag in range(1, L + 1):
        Fpower = Fpower @ F
        covs.append(C @ Fpower @ P @ C.T)
    return covs, P, F


def population_covariance_hankel(A, C, dt, block_rows, process_scale):
    """Exact-population counterpart of the current NSD covariance Hankel."""
    b = int(block_rows)
    if b <= 0:
        raise ValueError("block_rows must be positive")
    covs, P, F = population_output_covariances(
        A, C, dt, 2 * b - 1, process_scale
    )
    p = C.shape[0]
    H = np.empty((p * b, p * b), dtype=float)
    for i in range(b):
        for j in range(b):
            H[i * p : (i + 1) * p, j * p : (j + 1) * p] = covs[i + j]
    return H, {"state_covariance": P, "F": F, "covariances": covs}
