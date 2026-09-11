from __future__ import annotations

import numpy as np

from .ssi_cov import output_covariances


def unique_lag_covariance_vector(Y, max_lag):
    """Stack vec_F(R_l) for the exact native NSD lag-covariance estimates."""
    Y = np.asarray(Y, float)
    L = int(max_lag)
    if Y.ndim != 2 or L <= 0 or Y.shape[0] <= L:
        raise ValueError("invalid Y or max_lag")
    covs = output_covariances(Y, L)
    return np.concatenate([R.reshape(-1, order="F") for R in covs])


def lag_product_contribution_sequence(Y, max_lag):
    """Return g_t whose sample mean exactly equals native lag covariances.

    For lag l, rows t < n-l contain n/(n-l) * vec_F(y[t+l] y[t]^T)
    and final l rows are zero. The finite-record edge padding is explicit.
    """
    Y = np.asarray(Y, float)
    L = int(max_lag)
    if Y.ndim != 2 or L <= 0 or Y.shape[0] <= L:
        raise ValueError("invalid Y or max_lag")
    n, p = Y.shape
    G = np.zeros((n, L * p * p), float)
    for lag in range(1, L + 1):
        prod = Y[lag:, :, None] * Y[:-lag, None, :]
        # transpose channel axes so C-order row flattening equals vec_F(matrix)
        flat_f = prod.transpose(0, 2, 1).reshape(n - lag, p * p)
        start = (lag - 1) * p * p
        stop = lag * p * p
        G[: n - lag, start:stop] = (n / (n - lag)) * flat_f
    return G


def bartlett_hac_diagonal_variance_of_mean(G, bandwidth):
    """Diagonal Bartlett-HAC variance of the sample mean of a vector series.

    Uses zero-padded FFT autocovariance sums and the conventional denominator n
    for Gamma_h. Returned values estimate diag(Omega / n).
    """
    G = np.asarray(G, float)
    bw = int(bandwidth)
    if G.ndim != 2 or len(G) < 2:
        raise ValueError("G must be observations x coordinates")
    n, _ = G.shape
    if bw < 0 or bw >= n:
        raise ValueError("bandwidth must be in [0, n-1]")
    Z = G - G.mean(axis=0, keepdims=True)
    nfft = 1 << int((2 * n - 1).bit_length())
    F = np.fft.rfft(Z, n=nfft, axis=0)
    acsum = np.fft.irfft(np.conj(F) * F, n=nfft, axis=0).real[: bw + 1]
    omega = acsum[0] / n
    if bw:
        for h in range(1, bw + 1):
            weight = 1.0 - h / (bw + 1.0)
            omega += 2.0 * weight * (acsum[h] / n)
    return omega / n


def disjoint_batch_diagonal_variance(Y, max_lag, n_batches):
    """Unique-lag analogue of the current P0-D5 disjoint batch variance."""
    Y = np.asarray(Y, float)
    K = int(n_batches)
    L = int(max_lag)
    if Y.ndim != 2 or K < 3:
        raise ValueError("Y must be 2D and n_batches >= 3")
    m = Y.shape[0] // K
    if m <= L:
        raise ValueError("batches too short for max_lag")
    cols = []
    for k in range(K):
        segment = Y[k * m : (k + 1) * m]
        cols.append(unique_lag_covariance_vector(segment, L))
    B = np.column_stack(cols)
    mean = B.mean(axis=1, keepdims=True)
    T = (B - mean) / np.sqrt(K * (K - 1.0))
    return np.sum(T * T, axis=1)
