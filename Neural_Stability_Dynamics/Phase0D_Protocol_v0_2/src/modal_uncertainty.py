from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment


def fit_modal_from_hankel(H, n_channels, order, dt):
    """Run the current fixed-order SSI-COV realization directly from a Hankel.

    Returns continuous-time poles and observable carrier vectors. This mirrors
    the realization used in src.ssi_cov after the covariance Hankel has been
    assembled. It is a P0-D uncertainty helper, not a rank selector.
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
    C = O[:p, :]
    F = np.linalg.pinv(O[:-p, :]) @ O[p:, :]
    mu, vecs = np.linalg.eig(F)
    if np.any(np.abs(mu) <= np.finfo(float).eps):
        raise ValueError("numerically zero discrete pole")
    vals_c = np.log(mu.astype(complex)) / dt
    shapes = C @ vecs
    return vals_c, shapes


def fit_poles_from_hankel(H, n_channels, order, dt):
    vals_c, _ = fit_modal_from_hankel(H, n_channels, order, dt)
    return vals_c


def positive_frequency_poles(vals_c, min_hz=0.0):
    vals = np.asarray(vals_c, complex)
    hz = vals.imag / (2.0 * np.pi)
    keep = np.where(hz > float(min_hz))[0]
    out = vals[keep]
    if len(out) == 0:
        return out
    return out[np.argsort(out.imag)]


def positive_frequency_modal(vals_c, shapes, min_hz=0.0):
    vals = np.asarray(vals_c, complex)
    shapes = np.asarray(shapes, complex)
    if shapes.ndim != 2 or shapes.shape[1] != len(vals):
        raise ValueError("shapes must be channels x poles")
    hz = vals.imag / (2.0 * np.pi)
    keep = np.where(hz > float(min_hz))[0]
    if len(keep) == 0:
        return vals[keep], shapes[:, keep]
    order = keep[np.argsort(vals[keep].imag)]
    return vals[order], shapes[:, order]


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


def carrier_subspace_basis(shapes, rtol=1e-10):
    """Return an orthonormal basis for the observable complex carrier span."""
    X = np.asarray(shapes, complex)
    if X.ndim != 2 or X.shape[1] == 0:
        raise ValueError("shapes must contain at least one carrier column")
    U, s, _ = np.linalg.svd(X, full_matrices=False)
    if len(s) == 0 or s[0] <= 0:
        raise ValueError("carrier matrix is numerically rank zero")
    rank = int(np.sum(s > float(rtol) * s[0]))
    if rank == 0:
        raise ValueError("carrier subspace is numerically rank zero")
    return U[:, :rank]


def carrier_subspace_projector(shapes, rtol=1e-10):
    Q = carrier_subspace_basis(shapes, rtol=rtol)
    return Q @ Q.conj().T


def principal_angles_from_bases(Qa, Qb):
    Qa = np.asarray(Qa, complex)
    Qb = np.asarray(Qb, complex)
    if Qa.ndim != 2 or Qb.ndim != 2 or Qa.shape[0] != Qb.shape[0]:
        raise ValueError("bases must share ambient dimension")
    s = np.linalg.svd(Qa.conj().T @ Qb, compute_uv=False)
    s = np.clip(np.real(s), 0.0, 1.0)
    return np.arccos(s)


def propagate_hankel_root_to_poles(
    H,
    T,
    n_channels,
    order,
    dt,
    epsilon=0.5,
    min_hz=1e-9,
):
    """Numerically propagate a Hankel covariance root to native pole coordinates."""
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


def propagate_hankel_root_to_carrier_subspace(
    H,
    T,
    n_channels,
    order,
    dt,
    epsilon=0.5,
    min_hz=1e-9,
):
    """Propagate Hankel uncertainty to the joint observable carrier projector.

    The output is the first-order expected squared Frobenius displacement of the
    projector, i.e. the trace of the local projector covariance in vector form.
    No threshold or confidence interpretation is attached to this P0-D object.
    """
    H = np.asarray(H, float)
    T = np.asarray(T, float)
    eps = float(epsilon)
    if eps <= 0:
        raise ValueError("epsilon must be positive")
    if T.ndim != 2 or T.shape[0] != H.size:
        raise ValueError("T must have H.size rows")

    vals0, shapes0 = fit_modal_from_hankel(H, n_channels, order, dt)
    poles0, carriers0 = positive_frequency_modal(vals0, shapes0, min_hz=min_hz)
    if len(poles0) == 0:
        raise ValueError("base fit has no positive-frequency carrier subspace")
    Q0 = carrier_subspace_basis(carriers0)
    P0 = Q0 @ Q0.conj().T
    base_rank = Q0.shape[1]

    derivative_norm_sq = np.empty(T.shape[1], float)
    max_principal_angle = np.empty(T.shape[1], float)
    hvec = H.reshape(-1, order="F")

    for k in range(T.shape[1]):
        direction = T[:, k]
        Hp = (hvec + eps * direction).reshape(H.shape, order="F")
        Hm = (hvec - eps * direction).reshape(H.shape, order="F")

        vp, sp = fit_modal_from_hankel(Hp, n_channels, order, dt)
        vm, sm = fit_modal_from_hankel(Hm, n_channels, order, dt)
        pp, cp = positive_frequency_modal(vp, sp, min_hz=min_hz)
        pm, cm = positive_frequency_modal(vm, sm, min_hz=min_hz)
        if len(pp) != len(poles0) or len(pm) != len(poles0):
            raise ValueError("perturbation changed positive-frequency modal count")
        Qp = carrier_subspace_basis(cp)
        Qm = carrier_subspace_basis(cm)
        if Qp.shape[1] != base_rank or Qm.shape[1] != base_rank:
            raise ValueError("perturbation changed carrier subspace rank")
        Pp = Qp @ Qp.conj().T
        Pm = Qm @ Qm.conj().T
        dP = (Pp - Pm) / (2.0 * eps)
        derivative_norm_sq[k] = float(np.linalg.norm(dP, "fro") ** 2)
        angles_p = principal_angles_from_bases(Q0, Qp)
        angles_m = principal_angles_from_bases(Q0, Qm)
        max_principal_angle[k] = max(
            float(np.max(angles_p)) if len(angles_p) else 0.0,
            float(np.max(angles_m)) if len(angles_m) else 0.0,
        )

    return {
        "base_poles": poles0,
        "base_basis": Q0,
        "base_projector": P0,
        "subspace_rank": int(base_rank),
        "projector_variance_trace": float(np.sum(derivative_norm_sq)),
        "directional_projector_derivative_norm_sq": derivative_norm_sq,
        "max_principal_angle_by_direction_rad": max_principal_angle,
        "epsilon": eps,
    }
