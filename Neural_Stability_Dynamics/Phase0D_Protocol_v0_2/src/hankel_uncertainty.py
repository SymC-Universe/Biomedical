from __future__ import annotations

import numpy as np

from .ssi_cov import output_covariances


def nsd_covariance_hankel(Y, block_rows):
    """Reproduce the exact finite-sample covariance Hankel used by NSD SSI-COV."""
    Y = np.asarray(Y, float)
    b = int(block_rows)
    if Y.ndim != 2 or b <= 0:
        raise ValueError("Y must be samples x channels and block_rows positive")
    n, p = Y.shape
    if n <= 2 * b:
        raise ValueError("record too short for requested block_rows")
    covs = output_covariances(Y, 2 * b - 1)
    H = np.empty((p * b, p * b), float)
    for i in range(b):
        for j in range(b):
            H[i*p:(i+1)*p, j*p:(j+1)*p] = covs[i+j]
    return H


def batch_hankel_covariance_root(Y, block_rows, n_batches):
    """P0-D batch estimate of sampling covariance for the NSD Hankel.

    Each contiguous batch uses NSD's own lag-specific covariance denominators.
    T @ T.T is sample_cov(vec(H_batch)) / n_batches. This is an exploratory
    approximation, not a frozen uncertainty rule.
    """
    Y = np.asarray(Y, float)
    K = int(n_batches)
    if Y.ndim != 2 or K < 3:
        raise ValueError("Y must be 2D and n_batches >= 3")
    m = Y.shape[0] // K
    if m <= 2 * int(block_rows):
        raise ValueError("batches too short for requested block_rows")
    blocks = []
    for k in range(K):
        segment = Y[k*m:(k+1)*m]
        Hk = nsd_covariance_hankel(segment, block_rows)
        blocks.append(Hk.reshape(-1, order="F"))
    B = np.column_stack(blocks)
    mean = B.mean(axis=1, keepdims=True)
    T = (B - mean) / np.sqrt(K * (K - 1.0))
    return T, {"n_batches": K, "samples_per_batch": m, "discarded_tail_samples": int(Y.shape[0] - K*m)}


def diagonal_variance_from_root(T):
    T = np.asarray(T, float)
    if T.ndim != 2:
        raise ValueError("T must be 2D")
    return np.sum(T * T, axis=1)
