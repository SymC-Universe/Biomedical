from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.linalg import block_diag
from scipy.optimize import linear_sum_assignment

from src.chi_conglomerate import (
    analytic_same_conglomerate_example,
    chi_from_pole_pair,
    conglomerate_chi,
    second_order_generator,
)
from src.ssi_cov import decompose, fit_from_decomposition
from src.synthetic_systems import simulate_linear


DT = 0.01
N_SAMPLES = 8000
BLOCK_ROWS = 30
PROCESS_SCALE = 0.30
MEASUREMENT_NOISE_FRACTION = 0.03
REPLICATES = 8
SEED = 202609111011

SINGLE_OMEGA_N = 2.0 * np.pi * 3.0
SINGLE_CHI = [0.20, 0.50, 0.80, 0.95, 0.99, 1.00, 1.01, 1.05, 1.20, 1.50, 2.00]

MULTI_OMEGA_N = [2.0 * np.pi * 2.0, 2.0 * np.pi * 7.0]
MULTI_CASES = [
    ("both_under", [0.35, 0.55]),
    ("common_subcritical", [0.75, 0.75]),
    ("mixed_cross_boundary", [0.65, 1.25]),
    ("both_over", [1.25, 1.50]),
    ("wide_heterogeneity", [0.25, 1.75]),
    ("near_boundary_mixed", [0.95, 1.05]),
]


def _fixed_output_map(n_channels, n_state, seed):
    rng = np.random.default_rng(seed)
    C = rng.normal(size=(n_channels, n_state))
    return C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)


def _add_measurement_noise(Y, seed):
    if MEASUREMENT_NOISE_FRACTION <= 0.0:
        return Y
    rng = np.random.default_rng(seed)
    sd = np.maximum(Y.std(axis=0, keepdims=True), 1e-12)
    return Y + MEASUREMENT_NOISE_FRACTION * sd * rng.normal(size=Y.shape)


def _fit(Y, order):
    U, S, p = decompose(Y, BLOCK_ROWS)
    vals, shapes = fit_from_decomposition(U, S, p, order, DT)
    return np.asarray(vals, complex), np.asarray(shapes, complex), np.asarray(S, float)


def _truth_branch(chi):
    if chi < 1.0:
        return "UNDERDAMPED"
    if chi > 1.0:
        return "OVERDAMPED"
    return "CRITICAL_REPEATED_ROOT"


def _estimated_pair_type(vals, tol=1e-7):
    vals = np.asarray(vals, complex)
    return "COMPLEX_PAIR" if np.max(np.abs(vals.imag)) > tol else "REAL_PAIR"


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


def _single_surface():
    C = _fixed_output_map(6, 2, SEED + 1)
    groups = []
    for k, chi_truth in enumerate(SINGLE_CHI):
        A = second_order_generator(chi_truth, SINGLE_OMEGA_N)
        truth_poles = np.linalg.eigvals(A)
        records = []
        for rep in range(REPLICATES):
            try:
                Y = simulate_linear(
                    A,
                    C,
                    DT,
                    N_SAMPLES,
                    PROCESS_SCALE,
                    np.random.default_rng(SEED + 100000 * k + 1000 * rep + 11),
                )
                Y = _add_measurement_noise(Y, SEED + 100000 * k + 1000 * rep + 12)
                vals, _, S = _fit(Y, 2)
                inv = chi_from_pole_pair(vals)
                records.append(
                    {
                        "replicate": rep,
                        "status": "OK",
                        "chi_est": inv["chi"],
                        "omega_n_est": inv["omega_n"],
                        "gamma_est": inv["gamma"],
                        "abs_chi_error": abs(inv["chi"] - chi_truth),
                        "relative_omega_n_error": abs(inv["omega_n"] - SINGLE_OMEGA_N) / SINGLE_OMEGA_N,
                        "all_estimated_poles_stable": bool(np.all(vals.real < 0.0)),
                        "estimated_pair_type": _estimated_pair_type(vals),
                        "estimated_poles": [
                            {"real": float(z.real), "imag": float(z.imag)} for z in vals
                        ],
                        "singular_support_s2_over_s1": float(S[1] / S[0]),
                    }
                )
            except Exception as exc:
                records.append(
                    {
                        "replicate": rep,
                        "status": "EXCEPTION_PRESERVED",
                        "exception_type": type(exc).__name__,
                        "exception_message": str(exc),
                    }
                )
        ok = [r for r in records if r["status"] == "OK"]
        groups.append(
            {
                "chi_truth": chi_truth,
                "truth_branch": _truth_branch(chi_truth),
                "omega_n_truth": SINGLE_OMEGA_N,
                "truth_poles": [
                    {"real": float(z.real), "imag": float(z.imag)} for z in truth_poles
                ],
                "records": records,
                "summary": {
                    "successful": len(ok),
                    "exceptions": len(records) - len(ok),
                    "chi_est": _summary([r["chi_est"] for r in ok]),
                    "abs_chi_error": _summary([r["abs_chi_error"] for r in ok]),
                    "relative_omega_n_error": _summary(
                        [r["relative_omega_n_error"] for r in ok]
                    ),
                    "stable_fit_fraction": (
                        float(np.mean([r["all_estimated_poles_stable"] for r in ok]))
                        if ok
                        else None
                    ),
                    "complex_pair_fraction": (
                        float(np.mean([r["estimated_pair_type"] == "COMPLEX_PAIR" for r in ok]))
                        if ok
                        else None
                    ),
                },
            }
        )
    return groups


def _truth_pairs(chis):
    return [
        np.linalg.eigvals(second_order_generator(c, wn))
        for c, wn in zip(chis, MULTI_OMEGA_N)
    ]


def _match_to_truth_pairs(estimated, truth_pairs):
    truth = np.concatenate(truth_pairs)
    est = np.asarray(estimated, complex)
    if len(est) != len(truth):
        raise ValueError("estimated/truth pole count mismatch")
    cost = np.abs(truth[:, None] - est[None, :])
    rows, cols = linear_sum_assignment(cost)
    if not np.array_equal(rows, np.arange(len(truth))):
        raise RuntimeError("unexpected truth assignment row order")
    matched = est[cols]
    return [matched[0:2], matched[2:4]], float(np.max(cost[rows, cols]))


def _multi_surface():
    C = _fixed_output_map(8, 4, SEED + 2)
    groups = []
    for k, (name, chis) in enumerate(MULTI_CASES):
        blocks = [
            second_order_generator(c, wn) for c, wn in zip(chis, MULTI_OMEGA_N)
        ]
        A = block_diag(*blocks)
        tpairs = _truth_pairs(chis)
        truth_c = conglomerate_chi(chis, MULTI_OMEGA_N)
        records = []
        for rep in range(REPLICATES):
            try:
                Y = simulate_linear(
                    A,
                    C,
                    DT,
                    N_SAMPLES,
                    PROCESS_SCALE,
                    np.random.default_rng(SEED + 900000 + 100000 * k + 1000 * rep + 21),
                )
                Y = _add_measurement_noise(
                    Y, SEED + 900000 + 100000 * k + 1000 * rep + 22
                )
                vals, _, S = _fit(Y, 4)
                epairs, assignment_max = _match_to_truth_pairs(vals, tpairs)
                inv = [chi_from_pole_pair(pair) for pair in epairs]
                est_c = conglomerate_chi(
                    [x["chi"] for x in inv], [x["omega_n"] for x in inv]
                )
                records.append(
                    {
                        "replicate": rep,
                        "status": "OK",
                        "component_chi_est": [float(x["chi"]) for x in inv],
                        "component_omega_n_est": [float(x["omega_n"]) for x in inv],
                        "component_abs_chi_error": [
                            float(abs(x["chi"] - t)) for x, t in zip(inv, chis)
                        ],
                        "chi_C_est": float(est_c["chi_C"]),
                        "chi_C_abs_error": float(abs(est_c["chi_C"] - truth_c["chi_C"])),
                        "all_estimated_poles_stable": bool(np.all(vals.real < 0.0)),
                        "truth_assignment_max_pole_distance": assignment_max,
                        "singular_support_s4_over_s1": float(S[3] / S[0]),
                    }
                )
            except Exception as exc:
                records.append(
                    {
                        "replicate": rep,
                        "status": "EXCEPTION_PRESERVED",
                        "exception_type": type(exc).__name__,
                        "exception_message": str(exc),
                    }
                )
        ok = [r for r in records if r["status"] == "OK"]
        groups.append(
            {
                "case": name,
                "component_chi_truth": list(chis),
                "omega_n_truth": list(MULTI_OMEGA_N),
                "chi_C_truth": float(truth_c["chi_C"]),
                "component_range_truth": float(max(chis) - min(chis)),
                "records": records,
                "summary": {
                    "successful": len(ok),
                    "exceptions": len(records) - len(ok),
                    "chi_C_est": _summary([r["chi_C_est"] for r in ok]),
                    "chi_C_abs_error": _summary([r["chi_C_abs_error"] for r in ok]),
                    "component_1_abs_error": _summary(
                        [r["component_abs_chi_error"][0] for r in ok]
                    ),
                    "component_2_abs_error": _summary(
                        [r["component_abs_chi_error"][1] for r in ok]
                    ),
                    "stable_fit_fraction": (
                        float(np.mean([r["all_estimated_poles_stable"] for r in ok]))
                        if ok
                        else None
                    ),
                    "truth_assignment_max_pole_distance": _summary(
                        [r["truth_assignment_max_pole_distance"] for r in ok]
                    ),
                },
            }
        )
    return groups


def build_record():
    return {
        "schema": "nsd-p0d11-preatlas-chi-conglomeration-v1",
        "status": "P0_D_PREATLAS_CHI_RECONSTRUCTION_NOT_VALIDATION",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "atlas_used_for_formula_or_tuning": False,
        "design": {
            "dt": DT,
            "n_samples": N_SAMPLES,
            "block_rows": BLOCK_ROWS,
            "process_scale": PROCESS_SCALE,
            "measurement_noise_fraction_channel_sd": MEASUREMENT_NOISE_FRACTION,
            "replicates": REPLICATES,
            "single_chi_grid": SINGLE_CHI,
            "single_omega_n": SINGLE_OMEGA_N,
            "multi_omega_n": MULTI_OMEGA_N,
            "fixed_known_development_orders": {"single": 2, "multi": 4},
        },
        "single_component_surface": _single_surface(),
        "multi_component_surface": _multi_surface(),
        "same_scalar_different_architecture": analytic_same_conglomerate_example(
            0.8, 0.4
        ),
        "nonclaims": [
            "No neural population chi is estimated.",
            "No Atlas value, phenotype, outcome, clinical label or historical SymC target is used to tune this experiment.",
            "Truth pole pairing in the multi-component surface is diagnostic only.",
            "Equal component weights are developmental and not a biological weighting rule.",
            "No chi_system admission rule, threshold, target zone or P1 adjudication is frozen.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--output", default="results/p0d_mapping/preatlas_chi_conglomeration_v1.json"
    )
    args = ap.parse_args()
    rec = build_record()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for group in rec["single_component_surface"]:
        print(
            json.dumps(
                {
                    "surface": "single",
                    "chi_truth": group["chi_truth"],
                    "truth_branch": group["truth_branch"],
                    **group["summary"],
                },
                sort_keys=True,
            )
        )
    for group in rec["multi_component_surface"]:
        print(
            json.dumps(
                {
                    "surface": "multi",
                    "case": group["case"],
                    "component_chi_truth": group["component_chi_truth"],
                    "chi_C_truth": group["chi_C_truth"],
                    **group["summary"],
                },
                sort_keys=True,
            )
        )
    print(
        "P0-D11 PRE-ATLAS CHI RECONSTRUCTION COMPLETE. No Atlas calibration, chi_system admission or P1 rule frozen."
    )


if __name__ == "__main__":
    main()
