from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.optimize import linear_sum_assignment

from src.hankel_uncertainty import nsd_covariance_hankel, batch_hankel_covariance_root
from src.modal_uncertainty import positive_frequency_poles, propagate_hankel_root_to_poles, pole_coordinates
from src.synthetic_systems import make_linear_system, simulate_linear, make_noise_bases, add_measurement_noise

DT = 0.02
BLOCK_ROWS = 12
N_CHANNELS = 4
ORDER = 4
PROCESS_SCALE = 0.35
DURATIONS = [3600, 7200]
BATCH_COUNTS = [6, 12]
REPLICATES = 24
EPSILONS = [0.25, 0.50]
SEED = 202609112300
MODES = [
    {"type": "complex", "decay": 0.6, "frequency_hz": 3.0},
    {"type": "complex", "decay": 1.0, "frequency_hz": 8.0},
]
CONDITIONS = [
    ("nominal", None),
    ("white_sensor_10pct", {"type": "white", "fraction_channel_sd": 0.10}),
]


def _simulate_fixed(A, C, n, rep, noise):
    r = np.random.default_rng(SEED + 10000 * rep + n)
    Y = simulate_linear(A, C, DT, n, PROCESS_SCALE, r)
    if noise is not None:
        rn = np.random.default_rng(SEED + 900000 + 10000 * rep + n)
        white, colored = make_noise_bases(n, N_CHANNELS, 0.0, rn)
        Y = add_measurement_noise(Y, noise, white, colored)
    return Y


def _truth_positive(A):
    vals = positive_frequency_poles(np.linalg.eigvals(A), min_hz=1e-9)
    return vals[np.argsort(vals.imag)]


def _truth_assignment(truth, base):
    cost = np.abs(truth[:, None] - base[None, :])
    rows, cols = linear_sum_assignment(cost)
    if not np.array_equal(rows, np.arange(len(truth))):
        raise RuntimeError("unexpected truth assignment row order")
    return cols, cost[rows, cols]


def _safe_stats(values):
    arr = np.asarray(values, float)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return {"n": 0, "median": None, "p10": None, "p90": None}
    return {
        "n": int(len(arr)),
        "median": float(np.median(arr)),
        "p10": float(np.quantile(arr, 0.10)),
        "p90": float(np.quantile(arr, 0.90)),
    }


def build():
    sysrng = np.random.default_rng(SEED)
    A, C = make_linear_system({"modes": MODES, "similarity": "orthogonal"}, N_CHANNELS, sysrng)
    truth = _truth_positive(A)
    truth_q = pole_coordinates(truth)

    cells = []
    for cname, noise in CONDITIONS:
        role = "NOMINAL_FUNCTION" if cname == "nominal" else "PERTURBED_FUNCTION"
        for n in DURATIONS:
            for k in BATCH_COUNTS:
                estimates = {"decay": [[] for _ in truth], "frequency_hz": [[] for _ in truth]}
                predicted = {eps: {"decay": [[] for _ in truth], "frequency_hz": [[] for _ in truth]} for eps in EPSILONS}
                assign = []
                failures = []

                for rep in range(REPLICATES):
                    Y = _simulate_fixed(A, C, n, rep, noise)
                    H = nsd_covariance_hankel(Y, BLOCK_ROWS)
                    T, _ = batch_hankel_covariance_root(Y, BLOCK_ROWS, k)
                    outs = {}
                    try:
                        for eps in EPSILONS:
                            outs[eps] = propagate_hankel_root_to_poles(
                                H, T, N_CHANNELS, ORDER, DT, epsilon=eps, min_hz=1e-9
                            )
                    except Exception as exc:
                        failures.append({"replicate": rep, "type": type(exc).__name__, "message": str(exc)})
                        continue

                    base = outs[EPSILONS[-1]]["base_poles"]
                    cols, dist = _truth_assignment(truth, base)
                    assign.extend(dist.tolist())
                    bq = outs[EPSILONS[-1]]["base_coordinates"]

                    for mode_idx, base_idx in enumerate(cols):
                        estimates["decay"][mode_idx].append(float(bq["decay"][base_idx]))
                        estimates["frequency_hz"][mode_idx].append(float(bq["frequency_hz"][base_idx]))
                        for eps in EPSILONS:
                            predicted[eps]["decay"][mode_idx].append(float(outs[eps]["variance_decay"][base_idx]))
                            predicted[eps]["frequency_hz"][mode_idx].append(float(outs[eps]["variance_frequency_hz"][base_idx]))

                mode_rows = []
                for mode_idx in range(len(truth)):
                    coord_rows = []
                    for coord in ["decay", "frequency_hz"]:
                        est = np.asarray(estimates[coord][mode_idx], float)
                        truth_value = float(truth_q[coord][mode_idx])
                        empirical_var = float(np.var(est, ddof=1)) if len(est) > 1 else None
                        bias = float(np.mean(est - truth_value)) if len(est) else None
                        rmse = float(np.sqrt(np.mean((est - truth_value) ** 2))) if len(est) else None
                        eps_rows = []
                        for eps in EPSILONS:
                            pv = np.asarray(predicted[eps][coord][mode_idx], float)
                            mean_pv = float(np.mean(pv)) if len(pv) else None
                            med_pv = float(np.median(pv)) if len(pv) else None
                            ratio = None if empirical_var in (None, 0.0) or mean_pv is None else float(mean_pv / empirical_var)
                            z = []
                            if len(est) == len(pv):
                                good = np.isfinite(pv) & (pv > 0)
                                z = (np.abs(est[good] - truth_value) / np.sqrt(pv[good])).tolist()
                            eps_rows.append({
                                "epsilon": eps,
                                "predicted_variance_mean": mean_pv,
                                "predicted_variance_median": med_pv,
                                "predicted_over_empirical_variance": ratio,
                                "absolute_standardized_error": _safe_stats(z),
                            })

                        pv_a = np.asarray(predicted[EPSILONS[0]][coord][mode_idx], float)
                        pv_b = np.asarray(predicted[EPSILONS[1]][coord][mode_idx], float)
                        good = np.isfinite(pv_a) & np.isfinite(pv_b) & (pv_a > 0) & (pv_b > 0)
                        eps_log_ratio = np.abs(np.log(pv_a[good] / pv_b[good])) if np.any(good) else np.array([])
                        coord_rows.append({
                            "coordinate": coord,
                            "truth": truth_value,
                            "successful_records": int(len(est)),
                            "empirical_variance": empirical_var,
                            "bias": bias,
                            "rmse": rmse,
                            "epsilon_results": eps_rows,
                            "epsilon_variance_absolute_log_ratio": _safe_stats(eps_log_ratio),
                        })
                    mode_rows.append({
                        "mode_index": mode_idx,
                        "truth_pole_real": float(truth[mode_idx].real),
                        "truth_pole_imag": float(truth[mode_idx].imag),
                        "coordinates": coord_rows,
                    })

                cells.append({
                    "condition": cname,
                    "coverage_role": role,
                    "n_samples": n,
                    "n_batches": k,
                    "replicates_requested": REPLICATES,
                    "successful_records": REPLICATES - len(failures),
                    "failures": failures,
                    "truth_assignment_distance": _safe_stats(assign),
                    "modes": mode_rows,
                })

    return {
        "schema": "nsd-p0d7-native-modal-uncertainty-v1",
        "status": "P0_D_FIRST_ORDER_MODAL_UNCERTAINTY_CALIBRATION_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "method": "NSD-native structured Hankel covariance root -> symmetric perturb-and-refit fixed-order SSI-COV -> pole coordinate variance",
        "design": {
            "durations": DURATIONS,
            "batch_counts": BATCH_COUNTS,
            "replicates": REPLICATES,
            "epsilons": EPSILONS,
            "block_rows": BLOCK_ROWS,
            "channels": N_CHANNELS,
            "fixed_order": ORDER,
            "conditions": [x[0] for x in CONDITIONS],
        },
        "cells": cells,
        "nonclaims": [
            "No confidence level or coverage claim is frozen.",
            "No batch count or finite-difference epsilon is selected.",
            "No uncertainty threshold or P1 INDETERMINATE rule is selected.",
            "Systematic bias remains separate from propagated sampling variance.",
            "Carrier/subspace uncertainty is not claimed by this run.",
            "No neural-data validity follows from this synthetic P0-D calibration.",
        ],
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/p0d_mapping/native_modal_uncertainty_v1.json")
    args = ap.parse_args()
    rec = build()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for cell in rec["cells"]:
        compact = {
            "condition": cell["condition"],
            "n_samples": cell["n_samples"],
            "n_batches": cell["n_batches"],
            "successful_records": cell["successful_records"],
            "variance_ratios_epsilon_0p5": [
                {
                    "mode": m["mode_index"],
                    "coordinate": c["coordinate"],
                    "ratio": c["epsilon_results"][1]["predicted_over_empirical_variance"],
                    "epsilon_log_ratio_median": c["epsilon_variance_absolute_log_ratio"]["median"],
                }
                for m in cell["modes"] for c in m["coordinates"]
            ],
        }
        print(json.dumps(compact, sort_keys=True))
    print("P0-D7 NATIVE MODAL UNCERTAINTY CALIBRATION COMPLETE. No P0-Q or P1 uncertainty rule frozen.")
