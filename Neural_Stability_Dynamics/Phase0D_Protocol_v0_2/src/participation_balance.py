from __future__ import annotations

import numpy as np
from scipy.linalg import expm, solve_discrete_lyapunov


def unit_block_stationary_covariance(A_block, dt):
    """Stationary covariance for unit process std under the NSD discrete simulator.

    The simulator increment is sqrt(dt) * Normal(0,I), so unit process
    covariance per step is Q=dt*I.
    """
    A = np.asarray(A_block, dtype=float)
    dt = float(dt)
    if A.shape != (2, 2) or dt <= 0.0:
        raise ValueError("A_block must be 2x2 and dt positive")
    F = expm(A * dt)
    if np.max(np.abs(np.linalg.eigvals(F))) >= 1.0:
        raise ValueError("block must be discrete-time stable")
    P = solve_discrete_lyapunov(F, dt * np.eye(2))
    P = 0.5 * (P + P.T)
    return P


def block_participation_units(blocks, C, dt):
    """Return latent and observable stationary variance units for 2D blocks."""
    C = np.asarray(C, dtype=float)
    if C.ndim != 2 or C.shape[1] != 2 * len(blocks):
        raise ValueError("C columns must match 2D block count")
    latent = []
    output = []
    covs = []
    for j, block in enumerate(blocks):
        P = unit_block_stationary_covariance(block, dt)
        Cj = C[:, 2 * j : 2 * (j + 1)]
        latent.append(float(np.trace(P)))
        output.append(float(np.trace(Cj @ P @ Cj.T)))
        covs.append(P)
    latent = np.asarray(latent, dtype=float)
    output = np.asarray(output, dtype=float)
    if np.any(latent <= 0.0) or np.any(output <= 0.0):
        raise ValueError("stationary participation units must be positive")
    return {"latent_trace_units": latent, "output_trace_units": output, "unit_covariances": covs}


def participation_from_scales(blocks, C, dt, scales):
    """Evaluate stationary latent/output participation for supplied block scales."""
    units = block_participation_units(blocks, C, dt)
    s = np.asarray(scales, dtype=float).reshape(-1)
    if len(s) != len(blocks) or np.any(~np.isfinite(s)) or np.any(s <= 0.0):
        raise ValueError("scales must be finite positive values matching block count")
    latent_contrib = s * s * units["latent_trace_units"]
    output_contrib = s * s * units["output_trace_units"]
    return {
        "scales": s,
        "latent_contributions": latent_contrib,
        "latent_fractions": latent_contrib / np.sum(latent_contrib),
        "output_contributions": output_contrib,
        "output_fractions": output_contrib / np.sum(output_contrib),
        "latent_total": float(np.sum(latent_contrib)),
        "output_total": float(np.sum(output_contrib)),
    }


def balanced_block_process_scales(blocks, C, dt, base_scale, mode):
    """Choose block noise stds that preserve total E0 trace while equalizing one trace.

    mode='equal_state_noise' returns the incumbent equal amplitudes.
    mode='latent_trace' equalizes stationary latent trace.
    mode='output_trace' equalizes stationary output covariance trace.
    """
    base = float(base_scale)
    if base <= 0.0:
        raise ValueError("base_scale must be positive")
    units = block_participation_units(blocks, C, dt)
    n = len(blocks)
    if mode == "equal_state_noise":
        scales = np.full(n, base, dtype=float)
    elif mode == "latent_trace":
        u = units["latent_trace_units"]
        target = float(np.mean(base * base * u))
        scales = np.sqrt(target / u)
    elif mode == "output_trace":
        u = units["output_trace_units"]
        target = float(np.mean(base * base * u))
        scales = np.sqrt(target / u)
    else:
        raise ValueError("unknown balance mode")

    out = participation_from_scales(blocks, C, dt, scales)
    out.update(
        {
            "mode": mode,
            "incumbent_latent_total": float(base * base * np.sum(units["latent_trace_units"])),
            "incumbent_output_total": float(base * base * np.sum(units["output_trace_units"])),
        }
    )
    return out


def simulate_block_process(A, C, dt, n_samples, block_scales, rng, burn=None):
    """Simulate a block-structured linear system with per-2D-block noise scales."""
    A = np.asarray(A, dtype=float)
    C = np.asarray(C, dtype=float)
    dt = float(dt)
    n_samples = int(n_samples)
    scales = np.asarray(block_scales, dtype=float).reshape(-1)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be square")
    if A.shape[0] != C.shape[1] or A.shape[0] != 2 * len(scales):
        raise ValueError("A, C and block_scales dimensions do not match 2D blocks")
    if np.any(scales <= 0.0) or dt <= 0.0 or n_samples <= 0:
        raise ValueError("scales, dt and n_samples must be positive")
    F = expm(A * dt)
    if burn is None:
        burn = max(2000, int(20.0 / dt))
    state_std = np.repeat(scales, 2)
    x = np.zeros(A.shape[0], dtype=float)
    for _ in range(int(burn)):
        x = F @ x + np.sqrt(dt) * state_std * rng.normal(size=len(x))
    Y = np.empty((n_samples, C.shape[0]), dtype=float)
    for k in range(n_samples):
        x = F @ x + np.sqrt(dt) * state_std * rng.normal(size=len(x))
        Y[k] = C @ x
    Y -= Y.mean(axis=0, keepdims=True)
    return Y
