from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.chi_conglomerate import second_order_generator
from src.chi_uncertainty import pair_invariants_from_hankel, propagate_hankel_root_to_chi
from src.hankel_uncertainty import batch_hankel_covariance_root, nsd_covariance_hankel
from src.synthetic_systems import simulate_linear

DT = 0.01
BLOCK_ROWS = 30
PROCESS_SCALE = 0.30
N_CHANNELS = 6
REPLICATES = 16
SEED = 202609111900
OMEGA_N = 2.0 * np.pi * 2.0
CHI_VALUES = [0.80, 0.95, 0.99, 1.00, 1.01, 1.05, 1.20, 1.50]
N_VALUES = [8000, 32000]
BATCH_COUNTS = [6, 12]
EPSILONS = [0.25, 0.50]


def _C():
    rng = np.random.default_rng(SEED)
    C = rng.normal(size=(N_CHANNELS, 2))
    return C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)


def _summary(values):
    x = np.asarray(values, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return {"n": 0, "median": None, "p10": None, "p90": None}
    return {
        "n": int(len(x)),
        "median": float(np.median(x)),
        "p10": float(np.quantile(x, 0.10)),
        "p90": float(np.quantile(x, 0.90)),
    }


def _safe_ratio(num, den):
    if den is None or not np.isfinite(den) or den <= 0.0:
        return None
    return float(num / den)


def _truth_sign(delta):
    if delta > 0.0:
        return 1
    if delta < 0.0:
        return -1
    return 0


def _point_sign(delta, tol=1e-12):
    if delta > tol:
        return 1
    if delta < -tol:
        return -1
    return 0


def build():
    C = _C()
    cells = []
    for chi_index, chi_truth in enumerate(CHI_VALUES):
        A = second_order_generator(chi_truth, OMEGA_N)
        delta_truth = chi_truth * chi_truth - 1.0
        for n in N_VALUES:
            base_records = []
            predictions = {(k, eps): [] for k in BATCH_COUNTS for eps in EPSILONS}
            for rep in range(REPLICATES):
                Y = simulate_linear(
                    A,
                    C,
                    DT,
                    n,
                    PROCESS_SCALE,
                    np.random.default_rng(SEED + chi_index * 1000000 + n * 10 + rep),
                )
                H = nsd_covariance_hankel(Y, BLOCK_ROWS)
                try:
                    base = pair_invariants_from_hankel(H, N_CHANNELS, DT)
                    base_records.append(
                        {
                            "replicate": rep,
                            "status": "OK",
                            "chi_est": float(base["chi"]),
                            "delta_chi_est": float(base["delta_chi"]),
                            "chi_abs_error": float(abs(base["chi"] - chi_truth)),
                            "delta_abs_error": float(abs(base["delta_chi"] - delta_truth)),
                            "point_sign": _point_sign(base["delta_chi"]),
                        }
                    )
                except Exception as exc:
                    base_records.append(
                        {
                            "replicate": rep,
                            "status": "BASE_EXCEPTION_PRESERVED",
                            "exception_type": type(exc).__name__,
                            "exception_message": str(exc),
                        }
                    )
                    continue

                roots = {}
                for k in BATCH_COUNTS:
                    try:
                        T, meta = batch_hankel_covariance_root(Y, BLOCK_ROWS, k)
                        roots[k] = (T, meta)
                    except Exception as exc:
                        for eps in EPSILONS:
                            predictions[(k, eps)].append(
                                {
                                    "replicate": rep,
                                    "status": "ROOT_EXCEPTION_PRESERVED",
                                    "exception_type": type(exc).__name__,
                                    "exception_message": str(exc),
                                }
                            )
                        continue

                for k, (T, meta) in roots.items():
                    for eps in EPSILONS:
                        try:
                            out = propagate_hankel_root_to_chi(
                                H, T, N_CHANNELS, DT, epsilon=eps
                            )
                            se_delta = float(np.sqrt(out["variance_delta_chi"]))
                            boundary_separation = (
                                float(abs(out["base"]["delta_chi"]) / se_delta)
                                if se_delta > 0.0
                                else None
                            )
                            predictions[(k, eps)].append(
                                {
                                    "replicate": rep,
                                    "status": "OK",
                                    "variance_chi": float(out["variance_chi"]),
                                    "variance_delta_chi": float(out["variance_delta_chi"]),
                                    "boundary_separation_se": boundary_separation,
                                    "samples_per_batch": int(meta["samples_per_batch"]),
                                }
                            )
                        except Exception as exc:
                            predictions[(k, eps)].append(
                                {
                                    "replicate": rep,
                                    "status": "PROPAGATION_EXCEPTION_PRESERVED",
                                    "exception_type": type(exc).__name__,
                                    "exception_message": str(exc),
                                }
                            )

            base_ok = [r for r in base_records if r["status"] == "OK"]
            chi_emp = (
                float(np.var([r["chi_est"] for r in base_ok], ddof=1))
                if len(base_ok) > 1
                else None
            )
            delta_emp = (
                float(np.var([r["delta_chi_est"] for r in base_ok], ddof=1))
                if len(base_ok) > 1
                else None
            )
            pred_summary = []
            for k in BATCH_COUNTS:
                eps_rows = {}
                for eps in EPSILONS:
                    ok = [r for r in predictions[(k, eps)] if r["status"] == "OK"]
                    eps_rows[eps] = ok
                    mean_v_chi = (
                        float(np.mean([r["variance_chi"] for r in ok])) if ok else None
                    )
                    mean_v_delta = (
                        float(np.mean([r["variance_delta_chi"] for r in ok])) if ok else None
                    )
                    pred_summary.append(
                        {
                            "n_batches": k,
                            "epsilon": eps,
                            "successful_propagations": len(ok),
                            "propagation_failures": len(predictions[(k, eps)]) - len(ok),
                            "mean_predicted_variance_chi": mean_v_chi,
                            "predicted_over_empirical_variance_chi": (
                                _safe_ratio(mean_v_chi, chi_emp) if mean_v_chi is not None else None
                            ),
                            "mean_predicted_variance_delta_chi": mean_v_delta,
                            "predicted_over_empirical_variance_delta_chi": (
                                _safe_ratio(mean_v_delta, delta_emp) if mean_v_delta is not None else None
                            ),
                            "boundary_separation_se": _summary(
                                [
                                    r["boundary_separation_se"]
                                    for r in ok
                                    if r["boundary_separation_se"] is not None
                                ]
                            ),
                        }
                    )

                shared = {
                    r["replicate"]: r for r in eps_rows[EPSILONS[0]]
                }
                stability = []
                for r in eps_rows[EPSILONS[1]]:
                    other = shared.get(r["replicate"])
                    if other is None:
                        continue
                    for key in ["variance_chi", "variance_delta_chi"]:
                        a = float(other[key])
                        b = float(r[key])
                        if a > 0.0 and b > 0.0:
                            stability.append(abs(np.log(b / a)))
                for row in pred_summary:
                    if row["n_batches"] == k:
                        row["epsilon_pair_median_absolute_log_variance_ratio"] = (
                            float(np.median(stability)) if stability else None
                        )

            truth_sign = _truth_sign(delta_truth)
            if truth_sign == 0:
                sign_fraction = None
            else:
                sign_fraction = (
                    float(np.mean([r["point_sign"] == truth_sign for r in base_ok]))
                    if base_ok
                    else None
                )
            cells.append(
                {
                    "chi_truth": chi_truth,
                    "delta_chi_truth": delta_truth,
                    "n_samples": n,
                    "base_records": base_records,
                    "prediction_records": {
                        f"K{k}_eps{eps}": predictions[(k, eps)]
                        for k in BATCH_COUNTS
                        for eps in EPSILONS
                    },
                    "summary": {
                        "base_successful": len(base_ok),
                        "base_failures": len(base_records) - len(base_ok),
                        "chi_est": _summary([r["chi_est"] for r in base_ok]),
                        "chi_abs_error": _summary([r["chi_abs_error"] for r in base_ok]),
                        "delta_chi_est": _summary([r["delta_chi_est"] for r in base_ok]),
                        "empirical_variance_chi": chi_emp,
                        "empirical_variance_delta_chi": delta_emp,
                        "point_estimate_truth_sign_fraction": sign_fraction,
                        "predicted": pred_summary,
                    },
                }
            )
    return {
        "schema": "nsd-p0d15-chi-discriminant-uncertainty-v1",
        "status": "P0_D_COORDINATE_UNCERTAINTY_CALIBRATION_NOT_QUALIFICATION",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "atlas_used": False,
        "design": {
            "dt": DT,
            "block_rows": BLOCK_ROWS,
            "process_scale": PROCESS_SCALE,
            "channels": N_CHANNELS,
            "replicates": REPLICATES,
            "omega_n": OMEGA_N,
            "chi_values": CHI_VALUES,
            "n_values": N_VALUES,
            "batch_counts": BATCH_COUNTS,
            "epsilons": EPSILONS,
            "fixed_development_order": 2,
        },
        "cells": cells,
        "nonclaims": [
            "No confidence level or INDETERMINATE cutoff is selected.",
            "No batch count or finite-difference epsilon is frozen.",
            "No branch threshold is selected from boundary-separation SE values.",
            "No Atlas value, phenotype or outcome is used.",
            "No neural chi range, chi_system, P0-Q rule or P1 rule is frozen.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--output", default="results/p0d_mapping/chi_discriminant_uncertainty_v1.json"
    )
    args = ap.parse_args()
    rec = build()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for cell in rec["cells"]:
        compact = {
            "chi_truth": cell["chi_truth"],
            "delta_truth": cell["delta_chi_truth"],
            "n_samples": cell["n_samples"],
            "base_successful": cell["summary"]["base_successful"],
            "chi_est": cell["summary"]["chi_est"],
            "point_truth_sign_fraction": cell["summary"]["point_estimate_truth_sign_fraction"],
            "predicted": cell["summary"]["predicted"],
        }
        print(json.dumps(compact, sort_keys=True))
    print("P0-D15 CHI/DISCRIMINANT UNCERTAINTY COMPLETE. No confidence, branch or P1 rule frozen.")


if __name__ == "__main__":
    main()
