from __future__ import annotations
import numpy as np


def fit_dmd(Y, dt, rank):
    """Exact DMD comparator for samples x channels data.

    P0 comparator plumbing only. No NSD/P1 adjudication thresholds live here.
    Returns continuous-time eigenvalues and channel-space modes.
    """
    Y = np.asarray(Y, float)
    if Y.ndim != 2 or Y.shape[0] < 3:
        raise ValueError("Y must be samples x channels with at least 3 samples")
    if dt <= 0:
        raise ValueError("dt must be positive")
    X = Y[:-1].T
    Xp = Y[1:].T
    U, s, Vh = np.linalg.svd(X, full_matrices=False)
    r = int(rank)
    if r <= 0 or r > len(s):
        raise ValueError("invalid rank")
    Ur = U[:, :r]
    sr = s[:r]
    Vr = Vh.conj().T[:, :r]
    tol = np.finfo(float).eps * max(X.shape) * max(float(sr[0]), 1.0)
    if np.any(sr <= tol):
        raise ValueError("requested DMD rank is numerically singular")
    Atilde = Ur.conj().T @ Xp @ Vr @ np.diag(1.0 / sr)
    mu, W = np.linalg.eig(Atilde)
    modes = Xp @ Vr @ np.diag(1.0 / sr) @ W
    vals_c = np.log(mu.astype(complex)) / float(dt)
    return vals_c, modes
