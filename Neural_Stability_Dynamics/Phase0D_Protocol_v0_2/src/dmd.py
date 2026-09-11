from __future__ import annotations
import numpy as np


def _snapshot_pair(Y, dt, rank):
    Y = np.asarray(Y, float)
    if Y.ndim != 2 or Y.shape[0] < 3:
        raise ValueError("Y must be samples x channels with at least 3 samples")
    if dt <= 0:
        raise ValueError("dt must be positive")
    X = Y[:-1].T
    Xp = Y[1:].T
    r = int(rank)
    if r <= 0 or r > min(X.shape):
        raise ValueError("invalid rank")
    return X, Xp, float(dt), r


def _reduced_dmd_from_pair(X, Xp, dt, rank):
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


def fit_dmd(Y, dt, rank):
    """Exact DMD comparator for samples x channels data.

    P0 comparator plumbing only. Standard/exact DMD is retained as a diagnostic
    baseline because published work shows that it can be biased by snapshot
    sensor noise. It must not be treated as the sole strongest fair noisy-data
    comparator merely because it is convenient.
    """
    X, Xp, dt, r = _snapshot_pair(Y, dt, rank)
    return _reduced_dmd_from_pair(X, Xp, dt, r)


def fit_tls_dmd(Y, dt, rank):
    """Total-least-squares DMD candidate for additive snapshot noise.

    The augmented snapshot matrix [X; X'] is rank-r projected before solving
    the reduced DMD problem. This implements the total-DMD/noise-aware route
    used in the DMD literature. P0 comparator candidate only: no P1 rank rule,
    superiority claim, or neural-noise model is encoded here.
    """
    X, Xp, dt, r = _snapshot_pair(Y, dt, rank)
    augmented = np.vstack([X, Xp])
    _, s_aug, Vh_aug = np.linalg.svd(augmented, full_matrices=False)
    if r > len(s_aug):
        raise ValueError("invalid TLS-DMD rank")
    sr_aug = s_aug[:r]
    tol = np.finfo(float).eps * max(augmented.shape) * max(float(sr_aug[0]), 1.0)
    if np.any(sr_aug <= tol):
        raise ValueError("requested TLS-DMD rank is numerically singular")

    Vr = Vh_aug.conj().T[:, :r]
    X_projected = X @ Vr
    Xp_projected = Xp @ Vr
    return _reduced_dmd_from_pair(X_projected, Xp_projected, dt, r)
