from __future__ import annotations

import numpy as np

from .chi_conglomerate import chi_from_pole_pair
from .modal_uncertainty import fit_poles_from_hankel


def pair_invariants_from_hankel(H, n_channels, dt):
    """Fit one fixed-order-2 SSI factor and return branch-complete invariants."""
    vals = np.asarray(fit_poles_from_hankel(H, n_channels, 2, dt), complex)
    if len(vals) != 2:
        raise ValueError("fixed-order-2 fit did not return exactly two poles")
    inv = chi_from_pole_pair(vals)
    return {
        "poles": vals,
        "chi": float(inv["chi"]),
        "gamma": float(inv["gamma"]),
        "omega_n": float(inv["omega_n"]),
        "delta_chi": float(inv["chi"] * inv["chi"] - 1.0),
    }


def propagate_hankel_root_to_chi(H, T, n_channels, dt, epsilon=0.5):
    """First-order propagation from an NSD Hankel covariance root to chi.

    The supplied model is always treated as one already-licensed second-order
    factor. This helper does not decide model order, component admission, pole
    pairing, branch classification, confidence level or indeterminacy.
    """
    H = np.asarray(H, float)
    T = np.asarray(T, float)
    eps = float(epsilon)
    if H.ndim != 2 or H.shape[0] != H.shape[1]:
        raise ValueError("H must be square")
    if T.ndim != 2 or T.shape[0] != H.size:
        raise ValueError("T must have H.size rows")
    if eps <= 0.0:
        raise ValueError("epsilon must be positive")

    base = pair_invariants_from_hankel(H, n_channels, dt)
    keys = ["chi", "delta_chi", "gamma", "omega_n"]
    derivatives = {key: np.empty(T.shape[1], float) for key in keys}
    hvec = H.reshape(-1, order="F")

    for k in range(T.shape[1]):
        direction = T[:, k]
        Hp = (hvec + eps * direction).reshape(H.shape, order="F")
        Hm = (hvec - eps * direction).reshape(H.shape, order="F")
        plus = pair_invariants_from_hankel(Hp, n_channels, dt)
        minus = pair_invariants_from_hankel(Hm, n_channels, dt)
        for key in keys:
            derivatives[key][k] = (plus[key] - minus[key]) / (2.0 * eps)

    return {
        "base": base,
        "variance_chi": float(np.sum(derivatives["chi"] ** 2)),
        "variance_delta_chi": float(np.sum(derivatives["delta_chi"] ** 2)),
        "variance_gamma": float(np.sum(derivatives["gamma"] ** 2)),
        "variance_omega_n": float(np.sum(derivatives["omega_n"] ** 2)),
        "derivative_chi": derivatives["chi"],
        "derivative_delta_chi": derivatives["delta_chi"],
        "derivative_gamma": derivatives["gamma"],
        "derivative_omega_n": derivatives["omega_n"],
        "epsilon": eps,
    }
