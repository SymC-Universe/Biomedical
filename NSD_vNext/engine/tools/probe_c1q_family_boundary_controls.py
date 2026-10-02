#!/usr/bin/env python3
"""C1Q family-boundary controls for D\C and S\D truths.

Qualification only. This probe generates exact stationary scalar Gaussian
second-order laws from the regular (A,rho,xi,H) covariance coordinates.

D\C cells are valid discrete exact-white-Q laws but fail continuous-time
embeddability on the licensed branch. S\D cells are strictly scalar-positive
but lie outside the discrete exact image.

The probe asks how current A0/A1/A2 and qualification-only C1Q behave near
these semantic boundaries. Model preference never overrides truth-family
membership.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

from nsd_engine.continuous_lineage_candidate import fit_continuous_lineage_candidate
from nsd_engine.state_space_adequacy import compare_state_space_candidates


def coordinates(fs: float, A: float, fn: float, zeta: float):
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / fs
    rho = math.exp(-L)
    theta = nu / fs
    xi = math.cos(theta)
    H_C = A * L * math.sin(theta) / theta
    H_D = A * math.sinh(L)
    return {
        "A": A,
        "alpha": alpha,
        "nu": nu,
        "L": L,
        "rho": rho,
        "theta": theta,
        "xi": xi,
        "H_C": H_C,
        "H_D": H_D,
        "chi": zeta,
    }


def residual_q(A: float, rho: float, xi: float, H: float):
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
    return q0, q1, q2


def spectral_minimum(A: float, rho: float, xi: float, H: float) -> float:
    q0, q1, q2 = residual_q(A, rho, xi, H)

    def poly(x):
        return 4.0 * q2 * x * x + 2.0 * q1 * x + q0 - 2.0 * q2

    candidates = [-1.0, 1.0]
    if q2 > 0.0:
        vertex = -q1 / (4.0 * q2)
        if -1.0 <= vertex <= 1.0:
            candidates.append(vertex)
    return float(min(poly(x) for x in candidates))


def scalar_positive_bound(A: float, rho: float, xi: float, sign: int, start: float) -> float:
    if sign not in (-1, 1):
        raise ValueError("sign must be +/-1")
    inside = sign * abs(start)
    if spectral_minimum(A, rho, xi, inside) <= 0.0:
        raise RuntimeError("start must lie inside scalar-positive region")

    outside = inside
    for _ in range(80):
        outside *= 1.5
        if spectral_minimum(A, rho, xi, outside) <= 0.0:
            break
    else:
        raise RuntimeError("failed to bracket scalar-positive boundary")

    if sign > 0:
        return float(
            brentq(
                lambda H: spectral_minimum(A, rho, xi, H),
                inside,
                outside,
            )
        )
    return float(
        brentq(
            lambda H: spectral_minimum(A, rho, xi, H),
            outside,
            inside,
        )
    )


def spectral_factor(A: float, rho: float, xi: float, H: float):
    q0, q1, q2 = residual_q(A, rho, xi, H)
    polynomial = np.asarray([q2, q1, q0, q1, q2], dtype=float)
    roots = np.roots(polynomial)
    inside = [complex(root) for root in roots if abs(root) < 1.0 - 1e-8]
    if len(inside) != 2:
        inside = sorted((complex(root) for root in roots), key=abs)[:2]
    r1, r2 = inside
    m1 = float(np.real(-(r1 + r2)))
    m2 = float(np.real(r1 * r2))
    sigma2 = float(q2 / m2)
    if sigma2 <= 0.0:
        raise RuntimeError("invalid innovation variance from spectral factor")
    return sigma2, m1, m2


def simulate(A: float, rho: float, xi: float, H: float, *, fs: float, seconds: float, seed: int):
    sigma2, m1, m2 = spectral_factor(A, rho, xi, H)
    n = int(round(fs * seconds))
    burn = int(round(5.0 * fs))
    total = n + burn
    rng = np.random.default_rng(seed)
    eps = rng.normal(0.0, math.sqrt(sigma2), size=total + 2)
    y = np.zeros(total + 2, dtype=float)
    ar1 = 2.0 * rho * xi
    ar2 = -(rho * rho)

    for t in range(2, total + 2):
        y[t] = (
            ar1 * y[t - 1]
            + ar2 * y[t - 2]
            + eps[t]
            + m1 * eps[t - 1]
            + m2 * eps[t - 2]
        )
    return y[burn + 2 : burn + 2 + n]


def fit(signal: np.ndarray, fs: float, optimizer_maxiter: int):
    current = compare_state_space_candidates(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
    )
    c1q = fit_continuous_lineage_candidate(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    bics = {item.family: item.bic for item in current.fits}
    bics["C1Q"] = c1q.bic
    ordered = sorted(bics.items(), key=lambda item: item[1])
    return {
        "current_winner": current.bic_winner,
        "extended_winner": ordered[0][0],
        "extended_margin_to_second": ordered[1][1] - ordered[0][1],
        "bics": bics,
        "C1Q": {
            "bic": c1q.bic,
            "parameters": c1q.parameters,
            "g_boundary_distance": 1.0 - abs(c1q.parameters["g"]),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fs", type=float, default=128.0)
    parser.add_argument("--seconds", type=float, default=30.0)
    parser.add_argument("--optimizer-maxiter", type=int, default=50)
    parser.add_argument("--seed", type=int, action="append", default=None)
    args = parser.parse_args()
    seeds = args.seed if args.seed is not None else [0, 1]

    coord = coordinates(args.fs, 0.8, 10.0, 0.30)
    A, rho, xi = coord["A"], coord["rho"], coord["xi"]
    positive_S = scalar_positive_bound(A, rho, xi, +1, coord["H_D"])
    negative_S = scalar_positive_bound(A, rho, xi, -1, -coord["H_D"])

    truth_specs = []
    for sign in (-1, 1):
        H_C = sign * coord["H_C"]
        H_D = sign * coord["H_D"]
        H_DC = sign * (coord["H_C"] + 0.5 * (coord["H_D"] - coord["H_C"]))
        S_bound = negative_S if sign < 0 else positive_S
        H_SD = 0.5 * (H_D + S_bound)
        truth_specs.extend(
            [
                ("D_not_C", sign, H_DC, H_C, H_D, S_bound),
                ("S_not_D", sign, H_SD, H_C, H_D, S_bound),
            ]
        )

    payload = {
        "status": "QUALIFICATION_ONLY",
        "licenses_real_eeg_local_chi": False,
        "promotes_c1q": False,
        "coordinates": coord,
        "scalar_positive_bounds": {
            "negative": negative_S,
            "positive": positive_S,
        },
        "cells": [],
    }

    for truth_class, sign, H, H_C, H_D, S_bound in truth_specs:
        implied_g = (H / A) * coord["theta"] / (
            coord["L"] * math.sin(coord["theta"])
        )
        if spectral_minimum(A, rho, xi, H) <= 0.0:
            raise RuntimeError("constructed truth is not scalar positive")

        if truth_class == "D_not_C":
            if not (abs(H) <= coord["H_D"] and abs(implied_g) > 1.0):
                raise RuntimeError("D_not_C construction failed")
        else:
            if not abs(H) > coord["H_D"]:
                raise RuntimeError("S_not_D construction failed")

        for seed in seeds:
            signal = simulate(
                A, rho, xi, H,
                fs=args.fs,
                seconds=args.seconds,
                seed=seed + (1000 if sign > 0 else 0),
            )
            payload["cells"].append({
                "truth_class": truth_class,
                "sign": sign,
                "seed": seed,
                "H": H,
                "H_C_signed": H_C,
                "H_D_signed": H_D,
                "S_boundary_signed": S_bound,
                "implied_continuous_g": implied_g,
                "spectral_minimum": spectral_minimum(A, rho, xi, H),
                **fit(signal, args.fs, args.optimizer_maxiter),
            })

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
