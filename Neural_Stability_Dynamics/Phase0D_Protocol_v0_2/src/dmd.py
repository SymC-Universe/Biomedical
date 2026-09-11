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
    """Exact DMD diagnostic baseline for samples x channels data.

    Standard/exact DMD is retained because it is transparent, but published
    work shows sensor-noise bias. It must not be used as the sole strongest
    fair noisy stochastic comparator merely because it is convenient.
    """
    X, Xp, dt, r = _snapshot_pair(Y, dt, rank)
    return _reduced_dmd_from_pair(X, Xp, dt, r)


def fit_tls_dmd(Y, dt, rank):
    """Total-least-squares DMD candidate for additive snapshot noise.

    The augmented snapshot matrix [X; X'] is rank-r projected before solving
    the reduced DMD problem. This is a P0 diagnostic comparator candidate, not
    a frozen neural-noise model or P1 comparator.
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


def fit_subspace_dmd(Y, dt, rank):
    """Subspace DMD for random dynamics with observation noise.

    Python translation of the authors' corrected Subspace DMD implementation
    (Takeishi, Kawahara & Yairi, Phys. Rev. E 96, 033310, 2017). Four shifted
    snapshot blocks are formed, future snapshots are projected onto the row
    space of past snapshots, and the reduced stochastic Koopman approximation
    is eigendecomposed.

    P0 comparator plumbing only. No P1 rank rule or superiority claim lives
    here.
    """
    Y = np.asarray(Y, float)
    if Y.ndim != 2 or Y.shape[0] < 5:
        raise ValueError("Y must be samples x channels with at least 5 samples")
    if dt <= 0:
        raise ValueError("dt must be positive")
    n = Y.shape[1]
    r = int(rank)
    if r <= 0 or r > n:
        raise ValueError("Subspace DMD rank must be between 1 and channel count")

    Yt = Y.T
    Y0 = Yt[:, :-3]
    Y1 = Yt[:, 1:-2]
    Y2 = Yt[:, 2:-1]
    Y3 = Yt[:, 3:]
    Yp = np.vstack([Y0, Y1])
    Yf = np.vstack([Y2, Y3])

    _, sp, Vhp = np.linalg.svd(Yp, full_matrices=False)
    if len(sp) == 0:
        raise ValueError("empty past-snapshot singular spectrum")
    tol_p = np.finfo(float).eps * max(Yp.shape) * max(float(sp[0]), 1.0)
    rp = int(np.sum(sp > tol_p))
    if rp == 0:
        raise ValueError("past snapshot matrix is numerically rank zero")
    Vp = Vhp.conj().T[:, :rp]
    O = (Yf @ Vp) @ Vp.conj().T

    Uq, sq, _ = np.linalg.svd(O, full_matrices=False)
    if r > len(sq):
        raise ValueError("requested Subspace DMD rank exceeds projected future rank")
    tol_q = np.finfo(float).eps * max(O.shape) * max(float(sq[0]), 1.0)
    if np.any(sq[:r] <= tol_q):
        raise ValueError("requested Subspace DMD rank is numerically singular")
    Uq = Uq[:, :r]
    Uq1 = Uq[:n, :]
    Uq2 = Uq[n:, :]

    U, s, Vh = np.linalg.svd(Uq1, full_matrices=False)
    if r > len(s):
        raise ValueError("requested Subspace DMD rank exceeds Uq1 rank")
    sr = s[:r]
    tol = np.finfo(float).eps * max(Uq1.shape) * max(float(sr[0]), 1.0)
    if np.any(sr <= tol):
        raise ValueError("Subspace DMD Uq1 is numerically singular at requested rank")
    Ur = U[:, :r]
    Vr = Vh.conj().T[:, :r]
    M = Uq2 @ Vr @ np.diag(1.0 / sr)
    Atilde = Ur.conj().T @ M
    mu, W = np.linalg.eig(Atilde)
    if np.any(np.abs(mu) <= np.finfo(float).eps):
        raise ValueError("Subspace DMD produced a numerically zero eigenvalue")
    modes = M @ W @ np.diag(1.0 / mu)
    vals_c = np.log(mu.astype(complex)) / float(dt)
    return vals_c, modes
