from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.lag_covariance_hac import (
    bartlett_hac_diagonal_variance_grid,
    disjoint_batch_diagonal_variance,
    lag_product_contribution_sequence,
    unique_lag_covariance_vector,
)
from src.synthetic_systems import (
    add_measurement_noise,
    make_linear_system,
    make_noise_bases,
    simulate_linear,
)

DT = 0.02
BLOCK_ROWS = 12
MAX_LAG = 2 * BLOCK_ROWS - 1
N_CHANNELS = 4
PROCESS_SCALE = 0.35
DURATIONS = [3600, 7200]
REPLICATES = 24
HAC_BANDWIDTHS = [0, 8, 32, 128]
BATCH_COUNTS = [6, 12]
SEED = 202609113700
MODES = [
    {"type": "complex", "decay": 0.6, "frequency_hz": 3.0},
    {"type": "complex", "decay": 1.0, "frequency_hz": 8.0},
]
CONDITIONS = [
    ("nominal", None),
    ("white_sensor_10pct", {"type": "white", "fraction_channel_sd": 0.10}),
    ("colored_sensor_10pct_rho0p8", {"type": "colored", "fraction_channel_sd": 0.10}),
]


def _simulate(A, C, n, cond_idx, rep, profile):
    rng = np.random.default_rng(SEED + cond_idx * 10000000 + n + 10000 * rep)
    Y = simulate_linear(A, C, DT, n, PROCESS_SCALE, rng)
    if profile is not None:
        nrng = np.random.default_rng(SEED + 500000000 + cond_idx * 10000000 + n + 10000 * rep)
        white, colored = make_noise_bases(n, N_CHANNELS, 0.8, nrng)
        Y = add_measurement_noise(Y, profile, white, colored)
    return Y


def _summary(predicted, empirical):
    p = np.asarray(predicted, float)
    e = np.asarray(empirical, float)
    finite = np.isfinite(p) & np.isfinite(e)
    positive = finite & (p > 0) & (e > 0)
    ratio = p[positive] / e[positive]
    if np.sum(positive) >= 2:
        lp = np.log(p[positive])
        le = np.log(e[positive])
        corr = float(np.corrcoef(lp, le)[0, 1])
        abs_log = np.abs(lp - le)
    else:
        corr = None
        abs_log = np.array([], float)
    return {
        "coordinates": int(len(p)),
        "finite_fraction": float(np.mean(finite)),
        "positive_fraction": float(np.mean(positive)),
        "predicted_nonpositive_fraction": float(np.mean(finite & (p <= 0))),
        "log_variance_correlation": corr,
        "predicted_over_empirical_median": None if len(ratio) == 0 else float(np.median(ratio)),
        "ratio_p10": None if len(ratio) == 0 else float(np.quantile(ratio, 0.10)),
        "ratio_p90": None if len(ratio) == 0 else float(np.quantile(ratio, 0.90)),
        "median_absolute_log_ratio": None if len(abs_log) == 0 else float(np.median(abs_log)),
    }


def build():
    sysrng = np.random.default_rng(SEED)
    A, C = make_linear_system({"modes": MODES, "similarity": "orthogonal"}, N_CHANNELS, sysrng)
    cells = []

    for cond_idx, (condition, profile) in enumerate(CONDITIONS):
        role = "NOMINAL_FUNCTION" if profile is None else "PERTURBED_FUNCTION"
        for n in DURATIONS:
            exact = []
            hac_by_bw = {bw: [] for bw in HAC_BANDWIDTHS}
            batch_by_k = {k: [] for k in BATCH_COUNTS}

            for rep in range(REPLICATES):
                Y = _simulate(A, C, n, cond_idx, rep, profile)
                exact.append(unique_lag_covariance_vector(Y, MAX_LAG))
                G = lag_product_contribution_sequence(Y, MAX_LAG)
                grid = bartlett_hac_diagonal_variance_grid(G, HAC_BANDWIDTHS)
                for bw in HAC_BANDWIDTHS:
                    hac_by_bw[bw].append(grid[bw])
                for k in BATCH_COUNTS:
                    batch_by_k[k].append(disjoint_batch_diagonal_variance(Y, MAX_LAG, k))

            exact_arr = np.stack(exact, axis=0)
            empirical = np.var(exact_arr, axis=0, ddof=1)
            hac_rows = []
            for bw in HAC_BANDWIDTHS:
                mean_pred = np.mean(np.stack(hac_by_bw[bw], axis=0), axis=0)
                hac_rows.append({
                    "bandwidth_samples": bw,
                    "bandwidth_seconds": float(bw * DT),
                    **_summary(mean_pred, empirical),
                })
            batch_rows = []
            for k in BATCH_COUNTS:
                mean_pred = np.mean(np.stack(batch_by_k[k], axis=0), axis=0)
                batch_rows.append({
                    "n_batches": k,
                    "samples_per_batch": n // k,
                    **_summary(mean_pred, empirical),
                })

            cells.append({
                "condition": condition,
                "coverage_role": role,
                "n_samples": n,
                "duration_seconds": float(n * DT),
                "replicates": REPLICATES,
                "native_lag_coordinates": int(exact_arr.shape[1]),
                "hac": hac_rows,
                "disjoint_batch": batch_rows,
            })

    return {
        "schema": "nsd-p0d10-dependence-aware-lag-covariance-v1",
        "status": "P0_D_METHOD_DIAGNOSIS_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "native_estimator": "R_l=(Y[l:].T @ Y[:-l])/(n-l), lags 1..23",
        "design": {
            "durations": DURATIONS,
            "replicates": REPLICATES,
            "hac_bandwidths": HAC_BANDWIDTHS,
            "batch_counts": BATCH_COUNTS,
            "channels": N_CHANNELS,
            "max_lag": MAX_LAG,
            "conditions": [x[0] for x in CONDITIONS],
        },
        "cells": cells,
        "nonclaims": [
            "No HAC bandwidth is selected or frozen.",
            "No full HAC covariance root is licensed by this diagonal diagnostic.",
            "No neural-data stationarity assumption is established.",
            "No confidence convention or P0-Q/P1 uncertainty rule is frozen.",
        ],
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/p0d_mapping/dependence_aware_lag_covariance_v1.json")
    args = ap.parse_args()
    rec = build()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for cell in rec["cells"]:
        print(json.dumps({
            "condition": cell["condition"],
            "n_samples": cell["n_samples"],
            "hac": [
                {
                    "bw": x["bandwidth_samples"],
                    "ratio": x["predicted_over_empirical_median"],
                    "log_corr": x["log_variance_correlation"],
                    "malr": x["median_absolute_log_ratio"],
                    "positive_fraction": x["positive_fraction"],
                }
                for x in cell["hac"]
            ],
            "batch": [
                {
                    "K": x["n_batches"],
                    "ratio": x["predicted_over_empirical_median"],
                    "log_corr": x["log_variance_correlation"],
                    "malr": x["median_absolute_log_ratio"],
                }
                for x in cell["disjoint_batch"]
            ],
        }, sort_keys=True))
    print("P0-D10 DEPENDENCE-AWARE COVARIANCE DIAGNOSIS COMPLETE. No bandwidth or uncertainty rule frozen.")
