from __future__ import annotations

import numpy as np


def second_order_generator(chi: float, omega_n: float) -> np.ndarray:
    """Dimensionless-state first-order realization of q''+2 chi wn q'+wn^2 q=0."""
    chi = float(chi)
    omega_n = float(omega_n)
    if not np.isfinite(chi) or chi <= 0.0:
        raise ValueError("chi must be finite and positive")
    if not np.isfinite(omega_n) or omega_n <= 0.0:
        raise ValueError("omega_n must be finite and positive")
    return omega_n * np.array([[0.0, 1.0], [-1.0, -2.0 * chi]], dtype=float)


def chi_from_pole_pair(poles, reality_tol: float = 1e-7):
    """Recover second-order invariants from one explicitly paired pole factor.

    This function does not decide whether two arbitrary poles belong together.
    That pairing must be licensed elsewhere. It only evaluates the invariants of
    a supplied two-pole factor.
    """
    vals = np.asarray(poles, dtype=complex).reshape(-1)
    if len(vals) != 2:
        raise ValueError("exactly two poles are required")
    if not np.all(np.isfinite(vals.real)) or not np.all(np.isfinite(vals.imag)):
        raise ValueError("poles must be finite")

    gamma_c = -(vals[0] + vals[1])
    omega2_c = vals[0] * vals[1]
    scale = max(1.0, abs(gamma_c), abs(omega2_c))
    if abs(gamma_c.imag) > reality_tol * scale:
        raise ValueError("paired poles do not yield a sufficiently real gamma")
    if abs(omega2_c.imag) > reality_tol * scale:
        raise ValueError("paired poles do not yield a sufficiently real omega_n^2")

    gamma = float(gamma_c.real)
    omega2 = float(omega2_c.real)
    if gamma <= 0.0:
        raise ValueError("paired factor is not stably damped under this convention")
    if omega2 <= 0.0:
        raise ValueError("paired factor has nonpositive omega_n^2")

    omega_n = float(np.sqrt(omega2))
    chi = gamma / (2.0 * omega_n)
    return {
        "chi": float(chi),
        "gamma": float(gamma),
        "omega_n": float(omega_n),
        "omega_n_sq": float(omega2),
        "discriminant": float(gamma * gamma - 4.0 * omega2),
    }


def conglomerate_chi(component_chi, omega_n, weights=None):
    """Developmental RMS damping/natural-scale conglomerate chi candidate."""
    chi = np.asarray(component_chi, dtype=float).reshape(-1)
    wn = np.asarray(omega_n, dtype=float).reshape(-1)
    if len(chi) == 0 or len(chi) != len(wn):
        raise ValueError("component_chi and omega_n must be equal nonzero length")
    if np.any(~np.isfinite(chi)) or np.any(chi <= 0.0):
        raise ValueError("component chi values must be finite and positive")
    if np.any(~np.isfinite(wn)) or np.any(wn <= 0.0):
        raise ValueError("omega_n values must be finite and positive")

    if weights is None:
        w = np.ones_like(chi)
    else:
        w = np.asarray(weights, dtype=float).reshape(-1)
        if len(w) != len(chi):
            raise ValueError("weights length mismatch")
        if np.any(~np.isfinite(w)) or np.any(w < 0.0) or not np.any(w > 0.0):
            raise ValueError("weights must be finite, nonnegative and not all zero")

    damping_half = chi * wn
    numerator_sq = float(np.sum(w * damping_half * damping_half))
    denominator_sq = float(np.sum(w * wn * wn))
    value = float(np.sqrt(numerator_sq / denominator_sq))

    natural_energy_weights = w * wn * wn
    natural_energy_weights = natural_energy_weights / np.sum(natural_energy_weights)
    return {
        "chi_C": value,
        "component_chi": chi.copy(),
        "omega_n": wn.copy(),
        "input_weights": w.copy(),
        "natural_scale_weights": natural_energy_weights,
        "component_min": float(np.min(chi)),
        "component_max": float(np.max(chi)),
        "component_range": float(np.max(chi) - np.min(chi)),
        "weighted_rms_identity": float(
            np.sqrt(np.sum(natural_energy_weights * chi * chi))
        ),
    }


def analytic_same_conglomerate_example(target: float = 0.8, first: float = 0.4):
    """Construct two equal-frequency component sets with the same chi_C.

    Set A is [target, target]. Set B is [first, second], where second is
    chosen so their equal-frequency RMS equals target. This demonstrates that
    chi_C cannot replace the retained modal composition.
    """
    target = float(target)
    first = float(first)
    if target <= 0.0 or first <= 0.0:
        raise ValueError("target and first must be positive")
    second_sq = 2.0 * target * target - first * first
    if second_sq <= 0.0:
        raise ValueError("requested first value cannot realize the target RMS")
    second = float(np.sqrt(second_sq))
    a = conglomerate_chi([target, target], [1.0, 1.0])
    b = conglomerate_chi([first, second], [1.0, 1.0])
    return {
        "target": target,
        "set_A": [target, target],
        "set_B": [first, second],
        "chi_C_A": float(a["chi_C"]),
        "chi_C_B": float(b["chi_C"]),
    }
