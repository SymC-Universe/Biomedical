#!/usr/bin/env python3
"""Spectral-KL adequacy probe for nonzero-g continuous-lineage truths.

Qualification-only predecision analysis. The tool compares the best achievable
current A1 spectrum (H=0) with the best A2 approximation to an exact one-mode
C-family truth with nonzero g. It reports expected Whittle/KL loss and the
finite-n BIC implication for a declared effective sample count.

This does not change A1/A2 and does not license real EEG.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution, minimize


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def current_reachable_bounds(fs: float):
    lo, hi = -8.0, 8.0
    A_lo = 1e-5 + (1.0 - 2e-5) * sigmoid(lo)
    A_hi = 1e-5 + (1.0 - 2e-5) * sigmoid(hi)
    rho_lo = 1e-3 + (0.999 - 1e-3) * sigmoid(lo)
    rho_hi = 1e-3 + (0.999 - 1e-3) * sigmoid(hi)
    f_lo = 1.0 + (45.0 - 1.0) * sigmoid(lo)
    f_hi = 1.0 + (45.0 - 1.0) * sigmoid(hi)
    split_lo = 1e-4 + (1.0 - 2e-4) * sigmoid(lo)
    split_hi = 1e-4 + (1.0 - 2e-4) * sigmoid(hi)
    return {
        "A": (A_lo, A_hi),
        "rho": (rho_lo, rho_hi),
        "frequency_hz": (f_lo, f_hi),
        "theta": (2.0 * math.pi * f_lo / fs, 2.0 * math.pi * f_hi / fs),
        "split": (split_lo, split_hi),
    }


def residual_psd(A, rho, xi, H, w):
    q2 = rho * rho * (1.0 - A)
    q1 = rho * (
        (1.0 + rho * rho) * H
        + xi * (A * (1.0 + 3.0 * rho * rho) - 2.0 * (1.0 + rho * rho))
    )
    q0 = (
        1.0
        + rho**4
        + 4.0 * rho * rho * xi * xi
        - 2.0 * A * rho**4
        - 4.0 * A * rho * rho * xi * xi
        - 4.0 * H * rho * rho * xi
    )
    numerator = q0 + 2.0 * q1 * np.cos(w) + 2.0 * q2 * np.cos(2.0 * w)
    phi = (
        1.0
        - 2.0 * rho * xi * np.exp(-1j * w)
        + rho * rho * np.exp(-2j * w)
    )
    return numerator / (np.abs(phi) ** 2)


def component_psd(fraction, rho, theta, w):
    den1 = 1.0 - 2.0 * rho * np.cos(w - theta) + rho * rho
    den2 = 1.0 - 2.0 * rho * np.cos(w + theta) + rho * rho
    return (
        fraction
        * 0.5
        * (1.0 - rho * rho)
        * (1.0 / den1 + 1.0 / den2)
    )


def a1_psd(params, w):
    A, rho, theta = params
    return residual_psd(A, rho, math.cos(theta), 0.0, w)


def a2_psd(params, w):
    total, split, rho1, rho2, theta1, theta2 = params
    first = total * split
    second = total * (1.0 - split)
    return (
        (1.0 - total)
        + component_psd(first, rho1, theta1, w)
        + component_psd(second, rho2, theta2, w)
    )


def kl_rate(true_psd, model_psd):
    if np.any(~np.isfinite(model_psd)) or np.any(model_psd <= 0.0):
        return 1e100
    value = np.log(model_psd / true_psd) + true_psd / model_psd - 1.0
    return 0.5 * float(np.mean(value))


def chi_from_rho_theta(rho: float, theta: float) -> float:
    L = -math.log(rho)
    return L / math.sqrt(L * L + theta * theta)


def fit_a1(true_psd, w, bounds, seed):
    box = [bounds["A"], bounds["rho"], bounds["theta"]]

    def objective(x):
        return kl_rate(true_psd, a1_psd(x, w))

    result = differential_evolution(
        objective,
        box,
        seed=seed,
        maxiter=180,
        popsize=10,
        tol=1e-8,
        polish=True,
        workers=1,
        updating="immediate",
    )
    return float(result.fun), np.asarray(result.x, dtype=float)


def fit_a2(true_psd, w, bounds, seed):
    box = [
        bounds["A"],
        bounds["split"],
        bounds["rho"],
        bounds["rho"],
        bounds["theta"],
        bounds["theta"],
    ]

    def objective(x):
        return kl_rate(true_psd, a2_psd(x, w))

    result = differential_evolution(
        objective,
        box,
        seed=seed,
        maxiter=260,
        popsize=10,
        tol=2e-7,
        polish=False,
        workers=1,
        updating="immediate",
    )
    refined = minimize(
        objective,
        np.asarray(result.x, dtype=float),
        method="L-BFGS-B",
        bounds=box,
        options={"maxiter": 1200, "ftol": 1e-13},
    )
    return float(refined.fun), np.asarray(refined.x, dtype=float)


def truth(fs, A, natural_frequency_hz, zeta, g):
    omega_n = 2.0 * math.pi * natural_frequency_hz
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    dt = 1.0 / fs
    rho = math.exp(-alpha * dt)
    theta = nu * dt
    xi = math.cos(theta)
    G = g * A * alpha
    H = G * math.sin(theta) / nu
    return {
        "A": A,
        "rho": rho,
        "theta": theta,
        "xi": xi,
        "H": H,
        "chi": zeta,
        "g": g,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fs", type=float, default=256.0)
    parser.add_argument("--A", type=float, default=0.8)
    parser.add_argument("--natural-frequency-hz", type=float, default=10.0)
    parser.add_argument("--zeta", type=float, default=0.30)
    parser.add_argument("--g", type=float, action="append", default=None)
    parser.add_argument("--effective-n", type=int, default=7552)
    parser.add_argument("--grid-size", type=int, default=4096)
    parser.add_argument("--seed", type=int, default=20260927)
    args = parser.parse_args()

    g_values = args.g if args.g is not None else [-0.75, 0.0, 0.75]
    w = np.linspace(-math.pi, math.pi, args.grid_size, endpoint=False)
    bounds = current_reachable_bounds(args.fs)
    penalty_delta = 3.0 * math.log(args.effective_n)

    payload = {
        "status": "PREDECISION_ANALYTIC_ONLY",
        "licenses_real_eeg_local_chi": False,
        "changes_production_estimator": False,
        "effective_n": args.effective_n,
        "bic_parameter_delta_A2_minus_A1": 3,
        "bic_penalty_delta": penalty_delta,
        "truth": {
            "fs": args.fs,
            "A": args.A,
            "natural_frequency_hz": args.natural_frequency_hz,
            "zeta": args.zeta,
        },
        "reachable_bounds": bounds,
        "cells": [],
    }

    for index, g in enumerate(g_values):
        t = truth(
            args.fs,
            args.A,
            args.natural_frequency_hz,
            args.zeta,
            float(g),
        )
        true_psd = residual_psd(t["A"], t["rho"], t["xi"], t["H"], w)
        if float(np.min(true_psd)) <= 0.0:
            raise RuntimeError("truth spectrum is not strictly positive")

        a1_kl, a1_params = fit_a1(true_psd, w, bounds, args.seed + 10 * index)
        a2_kl, a2_params = fit_a2(true_psd, w, bounds, args.seed + 10 * index + 1)
        expected_nll_improvement = (a1_kl - a2_kl) * args.effective_n
        expected_bic_delta = (
            2.0 * (a2_kl - a1_kl) * args.effective_n + penalty_delta
        )

        payload["cells"].append(
            {
                "g": float(g),
                "H": t["H"],
                "truth_chi": t["chi"],
                "A1": {
                    "kl_rate": a1_kl,
                    "params": a1_params.tolist(),
                    "fitted_chi": chi_from_rho_theta(
                        float(a1_params[1]), float(a1_params[2])
                    ),
                },
                "A2": {
                    "kl_rate": a2_kl,
                    "params": a2_params.tolist(),
                },
                "expected_A1_to_A2_nll_improvement_at_effective_n": expected_nll_improvement,
                "expected_BIC_A2_minus_A1_at_effective_n": expected_bic_delta,
                "descriptive_BIC_preference_at_effective_n": (
                    "A2" if expected_bic_delta < 0.0 else "A1"
                ),
            }
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "cell_count": len(payload["cells"]),
        "status": payload["status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
