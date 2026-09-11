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
from src.modal_uncertainty import (
    carrier_subspace_basis,
    fit_modal_from_hankel,
    positive_frequency_modal,
    principal_angles_from_bases,
    propagate_hankel_root_to_carrier_subspace,
)
from src.synthetic_systems import make_linear_system, simulate_linear

DT = 0.02
BLOCK_ROWS = 12
N_CHANNELS = 4
ORDER = 4
PROCESS_SCALE = 0.35
DURATIONS = [3600, 7200]
BATCH_COUNTS = [6, 12]
REPLICATES = 24
EPSILONS = [0.25, 0.50]
SEED = 202609113100

CONDITIONS = [
    ("separated_2hz", 2.0),
    ("moderately_crowded_0p30hz", 0.30),
    ("strongly_crowded_0p05hz", 0.05),
]


def _spec(delta_hz):
    return {
        "modes": [
            {"type": "complex", "decay": 0.7, "frequency_hz": 6.0},
            {"type": "complex", "decay": 0.7, "frequency_hz": 6.0 + float(delta_hz)},
        ],
        "similarity": "orthogonal",
    }


def _truth_modal(A, C):
    vals, vecs = np.linalg.eig(A)
    return positive_frequency_modal(vals, C @ vecs, min_hz=1e-9)


def _projector(Q):
    return Q @ Q.conj().T


def _mac(a, b):
    a = np.asarray(a, complex)
    b = np.asarray(b, complex)
    den = float(np.vdot(a, a).real * np.vdot(b, b).real)
    if den <= 0:
        return np.nan
    return float(abs(np.vdot(a, b)) ** 2 / den)


def _match_truth_modes(truth_vals, truth_shapes, est_vals, est_shapes):
    if len(truth_vals) != len(est_vals):
        raise ValueError("truth and estimate positive-frequency modal counts differ")
    cost = np.abs(truth_vals[:, None] - est_vals[None, :])
    rows, cols = linear_sum_assignment(cost)
    if not np.array_equal(rows, np.arange(len(truth_vals))):
        raise RuntimeError("unexpected assignment row order")
    return [
        {
            "truth_index": int(i),
            "estimate_index": int(j),
            "pole_distance": float(cost[i, j]),
            "MAC": _mac(truth_shapes[:, i], est_shapes[:, j]),
        }
        for i, j in zip(rows, cols)
    ]


def _stats(values):
    a = np.asarray(values, float)
    a = a[np.isfinite(a)]
    if len(a) == 0:
        return {"n": 0, "median": None, "p10": None, "p90": None}
    return {
        "n": int(len(a)),
        "median": float(np.median(a)),
        "p10": float(np.quantile(a, 0.10)),
        "p90": float(np.quantile(a, 0.90)),
    }


def _empirical_projector_variance(projectors):
    stack = np.stack(projectors, axis=0)
    mean = np.mean(stack, axis=0)
    centered = stack - mean
    total = float(np.sum(np.abs(centered) ** 2) / (len(projectors) - 1))
    return total, mean


def build():
    cells = []
    for cond_idx, (name, delta) in enumerate(CONDITIONS):
        sysrng = np.random.default_rng(SEED + cond_idx * 10000000)
        A, C = make_linear_system(_spec(delta), N_CHANNELS, sysrng)
        truth_vals, truth_shapes = _truth_modal(A, C)
        Qtruth = carrier_subspace_basis(truth_shapes)
        Ptruth = _projector(Qtruth)

        for n in DURATIONS:
            base_records = []
            for rep in range(REPLICATES):
                rng = np.random.default_rng(SEED + cond_idx * 10000000 + n + 10000 * rep)
                Y = simulate_linear(A, C, DT, n, PROCESS_SCALE, rng)
                H = nsd_covariance_hankel(Y, BLOCK_ROWS)
                vals, shapes = fit_modal_from_hankel(H, N_CHANNELS, ORDER, DT)
                pvals, pshapes = positive_frequency_modal(vals, shapes, min_hz=1e-9)
                if len(pvals) != len(truth_vals):
                    base_records.append({
                        "replicate": rep,
                        "status": "BASE_MODAL_COUNT_MISMATCH",
                        "Y": Y,
                        "H": H,
                    })
                    continue
                Q = carrier_subspace_basis(pshapes)
                if Q.shape[1] != Qtruth.shape[1]:
                    base_records.append({
                        "replicate": rep,
                        "status": "BASE_SUBSPACE_RANK_MISMATCH",
                        "Y": Y,
                        "H": H,
                    })
                    continue
                P = _projector(Q)
                angles = principal_angles_from_bases(Qtruth, Q)
                matches = _match_truth_modes(truth_vals, truth_shapes, pvals, pshapes)
                base_records.append({
                    "replicate": rep,
                    "status": "OK",
                    "Y": Y,
                    "H": H,
                    "P": P,
                    "truth_max_principal_angle_rad": float(np.max(angles)),
                    "truth_projector_distance_fro": float(np.linalg.norm(P - Ptruth, "fro")),
                    "individual_MAC": [m["MAC"] for m in matches],
                    "pole_distance": [m["pole_distance"] for m in matches],
                })

            ok = [r for r in base_records if r["status"] == "OK"]
            if len(ok) < 2:
                cells.append({
                    "condition": name,
                    "delta_hz": delta,
                    "n_samples": n,
                    "status": "INSUFFICIENT_BASE_RECORDS",
                    "successful_base_records": len(ok),
                })
                continue

            empirical_var, Pbar = _empirical_projector_variance([r["P"] for r in ok])
            bias_sq = float(np.linalg.norm(Pbar - Ptruth, "fro") ** 2)
            mac_by_mode = [
                _stats([r["individual_MAC"][m] for r in ok])
                for m in range(len(truth_vals))
            ]
            base_summary = {
                "successful_base_records": len(ok),
                "empirical_projector_variance_trace": empirical_var,
                "mean_projector_bias_squared_to_truth": bias_sq,
                "truth_max_principal_angle_rad": _stats([r["truth_max_principal_angle_rad"] for r in ok]),
                "truth_projector_distance_fro": _stats([r["truth_projector_distance_fro"] for r in ok]),
                "individual_MAC_by_truth_mode": mac_by_mode,
                "pole_distance": _stats([x for r in ok for x in r["pole_distance"]]),
            }

            propagation = []
            for k in BATCH_COUNTS:
                for eps in EPSILONS:
                    predicted = []
                    direction_angles = []
                    failures = []
                    for r in ok:
                        try:
                            T, _ = batch_hankel_covariance_root(r["Y"], BLOCK_ROWS, k)
                            out = propagate_hankel_root_to_carrier_subspace(
                                r["H"], T, N_CHANNELS, ORDER, DT,
                                epsilon=eps, min_hz=1e-9,
                            )
                            predicted.append(out["projector_variance_trace"])
                            direction_angles.extend(out["max_principal_angle_by_direction_rad"].tolist())
                        except Exception as exc:
                            failures.append({
                                "replicate": r["replicate"],
                                "type": type(exc).__name__,
                                "message": str(exc),
                            })
                    mean_pred = float(np.mean(predicted)) if predicted else None
                    ratio = None
                    if mean_pred is not None and empirical_var > 0:
                        ratio = float(mean_pred / empirical_var)
                    propagation.append({
                        "n_batches": k,
                        "epsilon": eps,
                        "successful_propagations": len(predicted),
                        "failures": failures,
                        "predicted_projector_variance_trace": _stats(predicted),
                        "mean_predicted_over_empirical_variance": ratio,
                        "perturbation_max_principal_angle_rad": _stats(direction_angles),
                    })

            # Compare epsilon sensitivity for matched batch counts.
            epsilon_stability = []
            for k in BATCH_COUNTS:
                a = next(x for x in propagation if x["n_batches"] == k and x["epsilon"] == EPSILONS[0])
                b = next(x for x in propagation if x["n_batches"] == k and x["epsilon"] == EPSILONS[1])
                ma = a["predicted_projector_variance_trace"]["median"]
                mb = b["predicted_projector_variance_trace"]["median"]
                epsilon_stability.append({
                    "n_batches": k,
                    "median_variance_absolute_log_ratio": (
                        None if ma is None or mb is None or ma <= 0 or mb <= 0
                        else float(abs(np.log(ma / mb)))
                    ),
                })

            cells.append({
                "condition": name,
                "coverage_role": "NOMINAL_FUNCTION" if delta == 2.0 else "BOUNDARY_OR_TRANSITION",
                "delta_hz": delta,
                "n_samples": n,
                "status": "OK",
                "truth_subspace_rank": int(Qtruth.shape[1]),
                "base_summary": base_summary,
                "propagation": propagation,
                "epsilon_stability": epsilon_stability,
            })

    # Strip arrays from output by construction; only summaries are retained.
    return {
        "schema": "nsd-p0d9-carrier-subspace-uncertainty-v1",
        "status": "P0_D_SUBSPACE_UNCERTAINTY_CALIBRATION_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "object": "basis-invariant observable positive-frequency carrier projector",
        "design": {
            "conditions": [{"name": n, "delta_hz": d} for n, d in CONDITIONS],
            "durations": DURATIONS,
            "batch_counts": BATCH_COUNTS,
            "replicates": REPLICATES,
            "epsilons": EPSILONS,
            "channels": N_CHANNELS,
            "fixed_order": ORDER,
            "block_rows": BLOCK_ROWS,
        },
        "cells": cells,
        "nonclaims": [
            "No principal-angle, MAC or crowding threshold is selected.",
            "No confidence region on the carrier subspace is claimed.",
            "No P0-Q or P1 adjudication rule is frozen.",
            "The crowding conditions are post-P0-D3 development stresses, not independent confirmation.",
            "No neural-data validity follows from this synthetic calibration.",
        ],
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/p0d_mapping/carrier_subspace_uncertainty_v1.json")
    args = ap.parse_args()
    rec = build()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for cell in rec["cells"]:
        if cell.get("status") != "OK":
            print(json.dumps(cell, sort_keys=True))
            continue
        print(json.dumps({
            "condition": cell["condition"],
            "delta_hz": cell["delta_hz"],
            "n_samples": cell["n_samples"],
            "empirical_projector_variance_trace": cell["base_summary"]["empirical_projector_variance_trace"],
            "individual_MAC_medians": [x["median"] for x in cell["base_summary"]["individual_MAC_by_truth_mode"]],
            "truth_max_principal_angle_median_rad": cell["base_summary"]["truth_max_principal_angle_rad"]["median"],
            "predicted_over_empirical": [
                {"batches": p["n_batches"], "epsilon": p["epsilon"], "ratio": p["mean_predicted_over_empirical_variance"], "success": p["successful_propagations"]}
                for p in cell["propagation"]
            ],
            "epsilon_stability": cell["epsilon_stability"],
        }, sort_keys=True))
    print("P0-D9 CARRIER/SUBSPACE UNCERTAINTY CALIBRATION COMPLETE. No P0-Q or P1 rule frozen.")
