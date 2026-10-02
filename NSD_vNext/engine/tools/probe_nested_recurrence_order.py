#!/usr/bin/env python3
"""Threshold-free nested covariance recurrence-order qualification."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from probe_structural_order_finite_sample import (
    arma_second_order_signal,
    colored_process_signal,
    continuous_c_signal,
    quantiles,
    rank_auc,
    scalar_positive_bound,
    two_mode_signal,
)


def covariances(signal, max_lag):
    x = np.asarray(signal, dtype=float)
    x = x - float(np.mean(x))
    v = float(np.mean(x * x))
    x = x / math.sqrt(v)
    return np.asarray(
        [float(np.mean(x[:-k] * x[k:])) for k in range(1, max_lag + 1)]
    )


def fit_recurrence(gamma, order, last_lag):
    rows, target = [], []
    for lag in range(order + 1, last_lag + 1):
        j = lag - 1
        rows.append([gamma[j - q - 1] for q in range(order)])
        target.append(gamma[j])
    X = np.asarray(rows, dtype=float)
    y = np.asarray(target, dtype=float)
    coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return coef, float(np.linalg.cond(X))


def score_recurrence(gamma, coef, first_lag, last_lag):
    p = len(coef)
    residuals, observed = [], []
    for lag in range(first_lag, last_lag + 1):
        j = lag - 1
        row = np.asarray([gamma[j - q - 1] for q in range(p)])
        pred = float(np.dot(coef, row))
        residuals.append(float(gamma[j]) - pred)
        observed.append(float(gamma[j]))
    rms = math.sqrt(float(np.mean(np.asarray(residuals) ** 2)))
    ref = math.sqrt(float(np.mean(np.asarray(observed) ** 2)))
    return rms / max(ref, 1e-15)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--fs", type=float, default=256.0)
    ap.add_argument("--seconds", type=float, default=120.0)
    ap.add_argument("--seeds", type=int, default=20)
    args = ap.parse_args()

    fs = args.fs
    A, fn, zeta = 0.8, 10.0, 0.30
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
    S_neg = scalar_positive_bound(A, rho, xi, -1, H_D)
    H_DC_pos = H_C + 0.5 * (H_D - H_C)
    H_DC_neg = -H_DC_pos
    H_SD_pos = 0.5 * (H_D + S_pos)
    H_SD_neg = 0.5 * (-H_D + S_neg)

    rows = []
    for seed in range(args.seeds):
        signals = {
            "C_g0": continuous_c_signal(
                fs=fs, seconds=args.seconds, A=A, fn=fn, zeta=zeta, g=0.0, seed=seed
            ),
            "C_g_neg075": continuous_c_signal(
                fs=fs, seconds=args.seconds, A=A, fn=fn, zeta=zeta, g=-0.75, seed=seed
            ),
            "C_g_pos075": continuous_c_signal(
                fs=fs, seconds=args.seconds, A=A, fn=fn, zeta=zeta, g=0.75, seed=seed
            ),
            "D_not_C_neg": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_DC_neg,
                seed=seed + 2000,
            ),
            "D_not_C_pos": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_DC_pos,
                seed=seed + 3000,
            ),
            "S_not_D_neg": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_SD_neg,
                seed=seed + 4000,
            ),
            "S_not_D_pos": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_SD_pos,
                seed=seed + 5000,
            ),
            "colored_phi_0_7": colored_process_signal(
                fs=fs, seconds=args.seconds, seed=seed
            ),
            "genuine_two_mode": two_mode_signal(
                fs=fs, seconds=args.seconds, seed=seed
            ),
        }
        for truth_class, fine in signals.items():
            for rate_label, signal in (("fine", fine), ("coarse_decimate2", fine[::2])):
                split = signal.size // 2
                train = covariances(signal[:split], 30)
                hold = covariances(signal[split:], 30)
                rec = {"truth_class": truth_class, "seed": seed, "rate_label": rate_label}
                errors = {}
                for order in (2, 3, 4):
                    coef, cond = fit_recurrence(train, order, 16)
                    err = score_recurrence(hold, coef, 17, 30)
                    rec[f"order{order}_holdout_rms"] = err
                    rec[f"order{order}_condition"] = cond
                    errors[order] = err
                rec["improvement_2_to_3"] = errors[2] - errors[3]
                rec["improvement_3_to_4"] = errors[3] - errors[4]
                rec["relative_improvement_2_to_3"] = rec["improvement_2_to_3"] / max(errors[2], 1e-15)
                rec["relative_improvement_3_to_4"] = rec["improvement_3_to_4"] / max(errors[3], 1e-15)
                rows.append(rec)

    metrics = (
        "order2_holdout_rms", "order3_holdout_rms", "order4_holdout_rms",
        "improvement_2_to_3", "improvement_3_to_4",
        "relative_improvement_2_to_3", "relative_improvement_3_to_4",
    )
    classes = sorted({r["truth_class"] for r in rows})
    rates = ("fine", "coarse_decimate2")
    summary = {
        c: {
            rate: {
                m: quantiles([r[m] for r in rows if r["truth_class"] == c and r["rate_label"] == rate])
                for m in metrics
            }
            for rate in rates
        }
        for c in classes
    }

    c_ref = {"C_g0", "C_g_neg075", "C_g_pos075"}
    discrimination = {}
    for target in ("colored_phi_0_7", "genuine_two_mode"):
        discrimination[target] = {}
        for rate in rates:
            ref = [r for r in rows if r["truth_class"] in c_ref and r["rate_label"] == rate]
            tar = [r for r in rows if r["truth_class"] == target and r["rate_label"] == rate]
            discrimination[target][rate] = {
                m: rank_auc([r[m] for r in ref], [r[m] for r in tar])
                for m in ("improvement_2_to_3", "improvement_3_to_4",
                          "relative_improvement_2_to_3", "relative_improvement_3_to_4")
            }

    payload = {
        "status": "PREDECISION_CALIBRATION_ONLY",
        "licenses_real_eeg_local_chi": False,
        "defines_order_threshold": False,
        "changes_production_estimator": False,
        "seconds_total": args.seconds,
        "seed_count": args.seeds,
        "rows": rows,
        "summary": summary,
        "threshold_free_rank_auc_against_C_interiors": discrimination,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"row_count": len(rows), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
