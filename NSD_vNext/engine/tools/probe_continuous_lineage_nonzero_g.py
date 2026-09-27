#!/usr/bin/env python3
"""Exploratory nonzero-g continuous-lineage probe for NSD Bio Chi.

Known-truth qualification only. This script does not define an admission
threshold and does not license real EEG local chi. It generates exact samples
from one continuous-time underdamped C-family oscillator, deterministically
decimates the same realized path, and runs the unchanged A0/A1/A2 comparison
at both sampling rates.

The purpose is to expose whether current A1's H=0/B=0 nuisance restriction
causes A2 preference or other model-order instability inside the intended
continuous-lineage family.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from nsd_engine.state_space_adequacy import compare_state_space_candidates
from nsd_engine.continuous_lineage_candidate import fit_continuous_lineage_candidate


def construct_truth(*, fs: float, A: float, natural_frequency_hz: float, zeta: float, g: float):
    omega_n = 2.0 * math.pi * natural_frequency_hz
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    dt = 1.0 / fs
    G = g * A * alpha
    delta = nu * nu
    D = A * (2.0 * alpha * alpha + delta)

    K = np.asarray([[-alpha, -1.0], [delta, -alpha]], dtype=float)
    P = np.asarray([[A, -G], [-G, D]], dtype=float)
    Qc = -(K @ P + P @ K.T)
    F = expm(K * dt)
    Qd = P - F @ P @ F.T
    R = 1.0 - A

    theta = nu * dt
    rho = math.exp(-alpha * dt)
    H = G * math.sin(theta) / nu
    xi = math.cos(theta)

    return {
        "fs": fs,
        "A": A,
        "natural_frequency_hz": natural_frequency_hz,
        "zeta": zeta,
        "chi": zeta,
        "g": g,
        "alpha": alpha,
        "nu": nu,
        "G": G,
        "D": D,
        "K": K,
        "P": P,
        "Qc": Qc,
        "F": F,
        "Qd": Qd,
        "R": R,
        "rho": rho,
        "theta": theta,
        "xi": xi,
        "H": H,
    }


def _sqrt_psd(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(0.5 * (matrix + matrix.T))
    if float(np.min(values)) < -1e-9:
        raise ValueError(f"matrix is not PSD; minimum eigenvalue={float(np.min(values))}")
    return vectors @ np.diag(np.sqrt(np.clip(values, 0.0, None)))


def simulate_same_path(truth, *, seconds: float, seed: int) -> np.ndarray:
    n = int(round(seconds * truth["fs"]))
    if n < 1024:
        raise ValueError("duration is too short for the state-space fitter")

    rng = np.random.default_rng(seed)
    P_sqrt = _sqrt_psd(truth["P"])
    Q_sqrt = _sqrt_psd(truth["Qd"])
    x = P_sqrt @ rng.normal(size=2)

    output = np.empty(n, dtype=float)
    observation_sd = math.sqrt(max(0.0, truth["R"]))
    for index in range(n):
        output[index] = x[0] + observation_sd * rng.normal()
        x = truth["F"] @ x + Q_sqrt @ rng.normal(size=2)
    return output


def summarize_fit(signal: np.ndarray, fs: float, *, optimizer_maxiter: int):
    comparison = compare_state_space_candidates(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
    )
    candidate = fit_continuous_lineage_candidate(
        signal,
        fs,
        optimizer_maxiter=optimizer_maxiter,
    )
    all_bics = {fit.family: fit.bic for fit in comparison.fits}
    all_bics["C1Q"] = candidate.bic
    ordered = sorted(all_bics.items(), key=lambda item: item[1])
    payload = {
        "current_bic_winner": comparison.bic_winner,
        "current_bic_margin_to_second": comparison.bic_margin_to_second,
        "extended_bic_winner": ordered[0][0],
        "extended_bic_margin_to_second": ordered[1][1] - ordered[0][1],
        "fits": {},
    }
    for fit in comparison.fits:
        payload["fits"][fit.family] = {
            "bic": fit.bic,
            "negative_log_likelihood": fit.negative_log_likelihood,
            "parameter_count": fit.parameter_count,
            "innovation_max_abs_autocorrelation": fit.innovation_max_abs_autocorrelation,
            "innovation_rms": fit.innovation_rms,
            "parameters": fit.parameters,
        }
    payload["fits"]["C1Q"] = {
        "bic": candidate.bic,
        "negative_log_likelihood": candidate.negative_log_likelihood,
        "parameter_count": candidate.parameter_count,
        "parameters": candidate.parameters,
        "success": candidate.success,
    }
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seconds", type=float, default=30.0)
    parser.add_argument("--optimizer-maxiter", type=int, default=60)
    parser.add_argument("--fine-fs", type=float, default=256.0)
    parser.add_argument("--decimation", type=int, default=2)
    parser.add_argument("--A", type=float, default=0.8)
    parser.add_argument("--natural-frequency-hz", type=float, default=10.0)
    parser.add_argument("--zeta", type=float, default=0.30)
    parser.add_argument("--g", type=float, action="append", default=None)
    parser.add_argument("--seed", type=int, action="append", default=None)
    args = parser.parse_args()

    g_values = args.g if args.g is not None else [-0.75, 0.0, 0.75]
    seeds = args.seed if args.seed is not None else [0, 1]
    m = int(args.decimation)
    if m < 2:
        raise ValueError("decimation must be >=2")

    results = {
        "status": "EXPLORATORY_KNOWN_TRUTH_ONLY",
        "licenses_real_eeg_local_chi": False,
        "changes_production_estimator": False,
        "fine_sampling_rate_hz": args.fine_fs,
        "coarse_sampling_rate_hz": args.fine_fs / m,
        "decimation": m,
        "seconds": args.seconds,
        "truth_family": "continuous_time_embeddable_C",
        "cells": [],
    }

    for g in g_values:
        truth = construct_truth(
            fs=args.fine_fs,
            A=args.A,
            natural_frequency_hz=args.natural_frequency_hz,
            zeta=args.zeta,
            g=float(g),
        )
        if abs(truth["g"]) > 1.0:
            raise ValueError("|g| must be <=1 for C-family truth")
        if m * truth["theta"] >= math.pi:
            raise ValueError("coarse branch would not remain alias-safe")

        for seed in seeds:
            fine = simulate_same_path(truth, seconds=args.seconds, seed=int(seed))
            coarse = fine[::m]
            cell = {
                "truth": {
                    "A": truth["A"],
                    "natural_frequency_hz": truth["natural_frequency_hz"],
                    "zeta": truth["zeta"],
                    "chi": truth["chi"],
                    "g": truth["g"],
                    "H_fine": truth["H"],
                    "rho_fine": truth["rho"],
                    "theta_fine": truth["theta"],
                    "seed": int(seed),
                },
                "fine_fit": summarize_fit(
                    fine,
                    args.fine_fs,
                    optimizer_maxiter=args.optimizer_maxiter,
                ),
                "coarse_fit": summarize_fit(
                    coarse,
                    args.fine_fs / m,
                    optimizer_maxiter=args.optimizer_maxiter,
                ),
            }
            results["cells"].append(cell)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "cell_count": len(results["cells"]),
        "status": results["status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
