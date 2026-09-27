#!/usr/bin/env python3
"""Finite-sample C1Q vs D1Q scope controls for NSD Bio Chi.

Qualification only. C1Q and D1Q are both k=4 one-mode candidates. D1Q spans
all underdamped discrete exact-image D laws and reports implied continuous g
without constraining |g|<=1. This probe maps whether known C, D\C and S\D
truths are distinguishable by the unrestricted one-mode control.

No likelihood-gap or boundary threshold is selected.
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
from nsd_engine.discrete_exact_candidate import fit_discrete_exact_candidate


def sqrt_psd(matrix):
    values, vectors = np.linalg.eigh(0.5 * (matrix + matrix.T))
    if float(np.min(values)) < -1e-9:
        raise ValueError("matrix is not PSD")
    return vectors @ np.diag(np.sqrt(np.clip(values, 0.0, None)))


def c_signal(*, fs, seconds, A, fn, zeta, g, seed):
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    G = g * A * alpha
    D = A * (2.0 * alpha * alpha + nu * nu)
    K = np.asarray([[-alpha, -1.0], [nu * nu, -alpha]], dtype=float)
    P = np.asarray([[A, -G], [-G, D]], dtype=float)
    F = expm(K / fs)
    Qd = P - F @ P @ F.T
    rng = np.random.default_rng(seed)
    x = sqrt_psd(P) @ rng.normal(size=2)
    qsqrt = sqrt_psd(Qd)
    n = int(round(seconds * fs))
    out = np.empty(n)
    obs_sd = math.sqrt(1.0 - A)
    for i in range(n):
        out[i] = x[0] + obs_sd * rng.normal()
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


def fit_pair(signal, fs, optimizer_maxiter):
    c1 = fit_continuous_lineage_candidate(
        signal, fs,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    d1 = fit_discrete_exact_candidate(
        signal, fs,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    return {
        "C1Q": {
            "nll": c1.negative_log_likelihood,
            "bic": c1.bic,
            "parameters": c1.parameters,
        },
        "D1Q": {
            "nll": d1.negative_log_likelihood,
            "bic": d1.bic,
            "parameters": d1.parameters,
            "h_boundary_distance": 1.0 - abs(d1.parameters["h"]),
            "continuous_g_excess": max(
                0.0, abs(d1.parameters["implied_continuous_g"]) - 1.0
            ),
        },
        "nll_C1Q_minus_D1Q": (
            c1.negative_log_likelihood - d1.negative_log_likelihood
        ),
        "bic_C1Q_minus_D1Q": c1.bic - d1.bic,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fs", type=float, default=128.0)
    parser.add_argument("--seconds", type=float, default=30.0)
    parser.add_argument("--optimizer-maxiter", type=int, default=50)
    parser.add_argument("--seed", type=int, action="append", default=None)
    args = parser.parse_args()
    seeds = args.seed if args.seed is not None else [0, 1]

    fs = args.fs
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
    for label, family, H, g in specs:
        for seed in seeds:
            if family == "C":
                signal = c_signal(
                    fs=fs, seconds=args.seconds, A=A, fn=fn, zeta=zeta,
                    g=float(g), seed=seed,
                )
            else:
                signal = arma_signal(
                    fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi,
                    H=float(H), seed=seed + (1000 if "positive" in label else 0),
                )
            rows.append({
                "truth_label": label,
                "truth_family": family,
                "seed": seed,
                "truth_g_if_C": g,
                "truth_H": H,
                **fit_pair(signal, fs, args.optimizer_maxiter),
            })

    payload = {
        "status": "QUALIFICATION_ONLY",
        "licenses_real_eeg_local_chi": False,
        "promotes_d1q": False,
        "defines_c_vs_d_threshold": False,
        "sampling_rate_hz": fs,
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
