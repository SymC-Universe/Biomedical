#!/usr/bin/env python3
"""Paired-sampling semantic controls for qualification-only C1Q.

Known-truth qualification only. The same fine-rate realization is decimated by
two and C1Q is fit at both rates. The probe maps fitted chi/g consistency for:

- genuine C interior truths;
- D\C second-order truths;
- S\D scalar-positive second-order truths.

No cross-rate tolerance is selected here.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

from nsd_engine.continuous_lineage_candidate import fit_continuous_lineage_candidate


def _sqrt_psd(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(0.5 * (matrix + matrix.T))
    if float(np.min(values)) < -1e-9:
        raise ValueError("matrix is not PSD")
    return vectors @ np.diag(np.sqrt(np.clip(values, 0.0, None)))


def continuous_c_signal(
    *, fs: float, seconds: float, A: float, fn: float, zeta: float, g: float, seed: int
):
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    G = g * A * alpha
    D = A * (2.0 * alpha * alpha + nu * nu)
    K = np.asarray([[-alpha, -1.0], [nu * nu, -alpha]], dtype=float)
    P = np.asarray([[A, -G], [-G, D]], dtype=float)
    F = expm(K / fs)
    Qd = P - F @ P @ F.T

    n = int(round(seconds * fs))
    rng = np.random.default_rng(seed)
    x = _sqrt_psd(P) @ rng.normal(size=2)
    qsqrt = _sqrt_psd(Qd)
    out = np.empty(n)
    obs_sd = math.sqrt(1.0 - A)
    for index in range(n):
        out[index] = x[0] + obs_sd * rng.normal()
        x = F @ x + qsqrt @ rng.normal(size=2)
    return out


def residual_q(A, rho, xi, H):
    q2 = rho * rho * (1.0 - A)
    q1 = rho * (
        (1.0 + rho * rho) * H
        + xi * (A * (1.0 + 3.0 * rho * rho) - 2.0 * (1.0 + rho * rho))
    )
    q0 = (
        1.0 + rho**4 + 4.0 * rho * rho * xi * xi
        - 2.0 * A * rho**4
        - 4.0 * A * rho * rho * xi * xi
        - 4.0 * H * rho * rho * xi
    )
    return q0, q1, q2


def spectral_minimum(A, rho, xi, H):
    q0, q1, q2 = residual_q(A, rho, xi, H)

    def poly(x):
        return 4.0 * q2 * x * x + 2.0 * q1 * x + q0 - 2.0 * q2

    candidates = [-1.0, 1.0]
    if q2 > 0.0:
        vertex = -q1 / (4.0 * q2)
        if -1.0 <= vertex <= 1.0:
            candidates.append(vertex)
    return float(min(poly(x) for x in candidates))


def scalar_positive_bound(A, rho, xi, sign, start):
    inside = sign * abs(start)
    outside = inside
    for _ in range(80):
        outside *= 1.5
        if spectral_minimum(A, rho, xi, outside) <= 0.0:
            break
    else:
        raise RuntimeError("failed to bracket S boundary")
    lo, hi = sorted((inside, outside))
    return float(brentq(lambda H: spectral_minimum(A, rho, xi, H), lo, hi))


def spectral_factor(A, rho, xi, H):
    q0, q1, q2 = residual_q(A, rho, xi, H)
    roots = np.roots(np.asarray([q2, q1, q0, q1, q2], dtype=float))
    inside = [complex(root) for root in roots if abs(root) < 1.0 - 1e-8]
    if len(inside) != 2:
        inside = sorted((complex(root) for root in roots), key=abs)[:2]
    r1, r2 = inside
    m1 = float(np.real(-(r1 + r2)))
    m2 = float(np.real(r1 * r2))
    sigma2 = float(q2 / m2)
    if sigma2 <= 0.0:
        raise RuntimeError("invalid spectral factor")
    return sigma2, m1, m2


def arma_signal(*, fs, seconds, A, rho, xi, H, seed):
    sigma2, m1, m2 = spectral_factor(A, rho, xi, H)
    n = int(round(seconds * fs))
    burn = int(round(5.0 * fs))
    total = n + burn
    rng = np.random.default_rng(seed)
    eps = rng.normal(0.0, math.sqrt(sigma2), size=total + 2)
    y = np.zeros(total + 2)
    ar1 = 2.0 * rho * xi
    ar2 = -(rho * rho)
    for t in range(2, total + 2):
        y[t] = (
            ar1 * y[t - 1] + ar2 * y[t - 2]
            + eps[t] + m1 * eps[t - 1] + m2 * eps[t - 2]
        )
    return y[burn + 2 : burn + 2 + n]


def fit(signal, fs, optimizer_maxiter):
    result = fit_continuous_lineage_candidate(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    return {
        "bic": result.bic,
        "chi": result.parameters["damping_ratio"],
        "g": result.parameters["g"],
        "g_boundary_distance": 1.0 - abs(result.parameters["g"]),
        "natural_frequency_hz": result.parameters["natural_frequency_hz"],
        "damped_frequency_hz": result.parameters["damped_frequency_hz"],
        "rho": result.parameters["rho"],
        "A": result.parameters["latent_fraction"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fine-fs", type=float, default=256.0)
    parser.add_argument("--seconds", type=float, default=30.0)
    parser.add_argument("--optimizer-maxiter", type=int, default=50)
    parser.add_argument("--seed", type=int, action="append", default=None)
    args = parser.parse_args()
    seeds = args.seed if args.seed is not None else [0, 1]

    fs = args.fine_fs
    A = 0.8
    fn = 10.0
    zeta = 0.30
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / fs
    rho = math.exp(-L)
    theta = nu / fs
    xi = math.cos(theta)
    H_C = A * L * math.sin(theta) / theta
    H_D = A * math.sinh(L)
    S_pos = scalar_positive_bound(A, rho, xi, +1, H_D)
    S_neg = scalar_positive_bound(A, rho, xi, -1, -H_D)

    specs = [
        ("C_g_neg075", "C", None, -0.75),
        ("C_g_pos075", "C", None, +0.75),
        ("D_not_C_negative", "D_not_C", -(H_C + 0.5 * (H_D - H_C)), None),
        ("D_not_C_positive", "D_not_C", +(H_C + 0.5 * (H_D - H_C)), None),
        ("S_not_D_negative", "S_not_D", 0.5 * (-H_D + S_neg), None),
        ("S_not_D_positive", "S_not_D", 0.5 * (H_D + S_pos), None),
    ]

    rows = []
    for label, family, H, g_truth in specs:
        for seed in seeds:
            if family == "C":
                fine = continuous_c_signal(
                    fs=fs, seconds=args.seconds, A=A, fn=fn, zeta=zeta,
                    g=float(g_truth), seed=seed,
                )
            else:
                fine = arma_signal(
                    fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi,
                    H=float(H), seed=seed + (1000 if "positive" in label else 0),
                )
            coarse = fine[::2]
            fine_fit = fit(fine, fs, args.optimizer_maxiter)
            coarse_fit = fit(coarse, fs / 2.0, args.optimizer_maxiter)
            rows.append({
                "truth_label": label,
                "truth_family": family,
                "seed": seed,
                "truth_chi": zeta,
                "truth_g_if_C": g_truth,
                "truth_H_fine": H,
                "fine_fit": fine_fit,
                "coarse_fit": coarse_fit,
                "abs_chi_shift": abs(coarse_fit["chi"] - fine_fit["chi"]),
                "abs_g_shift": abs(coarse_fit["g"] - fine_fit["g"]),
                "abs_frequency_shift_hz": abs(
                    coarse_fit["natural_frequency_hz"]
                    - fine_fit["natural_frequency_hz"]
                ),
            })

    payload = {
        "status": "PREDECISION_CALIBRATION_ONLY",
        "licenses_real_eeg_local_chi": False,
        "defines_sampling_consistency_threshold": False,
        "fine_sampling_rate_hz": fs,
        "coarse_sampling_rate_hz": fs / 2.0,
        "seconds": args.seconds,
        "truth_coordinates": {
            "A": A,
            "natural_frequency_hz": fn,
            "chi": zeta,
            "H_C": H_C,
            "H_D": H_D,
            "S_negative": S_neg,
            "S_positive": S_pos,
        },
        "rows": rows,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "row_count": len(rows),
        "status": payload["status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
