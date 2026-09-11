from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment


def fit_poles_from_hankel(H, n_channels, order, dt):
    """Run the current fixed-order SSI-COV realization directly from a Hankel.

    This mirrors the realization used in src.ssi_cov after the covariance Hankel
    has been assembled. It is a P0-D uncertainty helper, not a rank selector.
    """
    H = np.asarray(H, float)
    p = int(n_channels)
    r = int(order)
    dt = float(dt)
    if H.ndim != 2 or H.shape[0] != H.shape[1]:
        raise ValueError("H must be square")
    if p <= 0 or r <= 0 or dt <= 0:
        raise ValueError("n_channels, order and dt must be positive")
    if H.shape[0] % p != 0:
        raise ValueError("H dimension must be divisible by n_channels")

    U, S, _ = np.linalg.svd(H, full_matrices=False)
    if r >= len(S):
        raise ValueError("order exceeds usable Hankel rank")
    O = U[:, :r] @ np.diag(np.sqrt(np.maximum(S[:r], 0.0)))
    if O.shape[0] <= p:
        raise ValueError("insufficient block rows for state transition fit")
    F = np.linalg.pinv(O[:-p, :]) @ O[p:, :]
    mu = np.linalg.eigvals(F)
    if np.any(np.abs(mu) <= np.finfo(float).eps):
        raise ValueError("numerically zero discrete pole")
    return np.log(mu.astype(complex)) / dt


def positive_frequency_poles(vals_c, min_hz=0.0):
    vals = np.asarray(vals_c, complex)
    hz = vals.imag / (2.0 * np.pi)
    keep = np.where(hz > float(min_hz))[0]
    out = vals[keep]
    if len(out) == 0:
        return out
    return out[np.argsort(out.imag)]


def match_poles(reference, candidate):
    """One-to-one complex-plane assignment of candidate poles to reference."""
    ref = np.asarray(reference, complex)
    cand = np.asarray(candidate, complex)
    if ref.ndim != 1 or cand.ndim != 1 or len(ref) != len(cand):
        raise ValueError("reference and candidate must be equal-length vectors")
    if len(ref) == 0:
        return cand.copy(), np.array([], dtype=float)
    cost = np.abs(ref[:, None] - cand[None, :])
    rows, cols = linear_sum_assignment(cost)
    if not np.array_equal(rows, np.arange(len(ref))):
        raise RuntimeError("unexpected assignment row order")
    return cand[cols], cost[rows, cols]


def pole_coordinates(vals_c):
    vals = np.asarray(vals_c, complex)
    return {
        "decay": -vals.real.astype(float),
        "frequency_hz": (vals.imag / (2.0 * np.pi)).astype(float),
    }


def propagate_hankel_root_to_poles(
    H,
    T,
    n_channels,
    order,
    dt,
    epsilon=0.5,
    min_hz=1e-9,
):
    """Numerically propagate a Hankel covariance root to native pole coordinates.

    Columns of T are treated as covariance-root directions for vec_F(H). For
    each direction a symmetric perturb-and-refit derivative is computed at a
    fixed model order. The returned variances are first-order P0-D estimates.
    """
    H = np.asarray(H, float)
    T = np.asarray(T, float)
    eps = float(epsilon)
    if eps <= 0:
        raise ValueError("epsilon must be positive")
    if T.ndim != 2 or T.shape[0] != H.size:
        raise ValueError("T must have H.size rows")

    base_all = fit_poles_from_hankel(H, n_channels, order, dt)
    base = positive_frequency_poles(base_all, min_hz=min_hz)
    if len(base) == 0:
        raise ValueError("base fit has no positive-frequency poles")
    base_q = pole_coordinates(base)

    d_decay = np.empty((len(base), T.shape[1]), float)
    d_freq = np.empty((len(base), T.shape[1]), float)
    assignment_max = np.empty(T.shape[1], float)

    hvec = H.reshape(-1, order="F")
    for k in range(T.shape[1]):
        direction = T[:, k]
        Hp = (hvec + eps * direction).reshape(H.shape, order="F")
        Hm = (hvec - eps * direction).reshape(H.shape, order="F")

        pp = positive_frequency_poles(
            fit_poles_from_hankel(Hp, n_channels, order, dt), min_hz=min_hz
        )
        pm = positive_frequency_poles(
            fit_poles_from_hankel(Hm, n_channels, order, dt), min_hz=min_hz
        )
        if len(pp) != len(base) or len(pm) != len(base):
            raise ValueError("perturbation changed positive-frequency modal count")
        pp, cp = match_poles(base, pp)
        pm, cm = match_poles(base, pm)
        qp = pole_coordinates(pp)
        qm = pole_coordinates(pm)
        d_decay[:, k] = (qp["decay"] - qm["decay"]) / (2.0 * eps)
        d_freq[:, k] = (qp["frequency_hz"] - qm["frequency_hz"]) / (2.0 * eps)
        assignment_max[k] = max(float(np.max(cp)), float(np.max(cm)))

    return {
        "base_poles": base,
        "base_coordinates": base_q,
        "variance_decay": np.sum(d_decay * d_decay, axis=1),
        "variance_frequency_hz": np.sum(d_freq * d_freq, axis=1),
        "derivative_decay": d_decay,
        "derivative_frequency_hz": d_freq,
        "assignment_distance_max": assignment_max,
        "epsilon": eps,
    }
