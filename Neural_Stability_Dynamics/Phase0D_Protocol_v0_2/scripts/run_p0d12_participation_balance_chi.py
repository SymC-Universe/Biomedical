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

from src.chi_conglomerate import chi_from_pole_pair, conglomerate_chi, second_order_generator
from src.participation_balance import balanced_block_process_scales, simulate_block_process
from src.ssi_cov import decompose, fit_from_decomposition

DT = 0.01
N_SAMPLES = 8000
BLOCK_ROWS = 30
BASE_PROCESS_SCALE = 0.30
MEASUREMENT_NOISE_FRACTION = 0.03
REPLICATES = 8
SEED = 202609111230
OMEGA_N = [2.0 * np.pi * 2.0, 2.0 * np.pi * 7.0]
CASES = [
    ("both_under", [0.35, 0.55]),
    ("common_subcritical", [0.75, 0.75]),
    ("mixed_cross_boundary", [0.65, 1.25]),
]
EXCITATION_MODES = ["equal_state_noise", "latent_trace", "output_trace"]


def _fixed_output_map():
    rng = np.random.default_rng(SEED)
    C = rng.normal(size=(8, 4))
    return C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)


def _add_measurement_noise(Y, seed):
    rng = np.random.default_rng(seed)
    sd = np.maximum(Y.std(axis=0, keepdims=True), 1e-12)
    out = Y + MEASUREMENT_NOISE_FRACTION * sd * rng.normal(size=Y.shape)
    out -= out.mean(axis=0, keepdims=True)
    return out


def _truth_pairs(chis):
    return [np.linalg.eigvals(second_order_generator(c, w)) for c, w in zip(chis, OMEGA_N)]


def _match_pairs(estimated, truth_pairs):
    truth = np.concatenate(truth_pairs)
    est = np.asarray(estimated, complex)
    if len(est) != len(truth):
        raise ValueError("estimated/truth pole count mismatch")
    cost = np.abs(truth[:, None] - est[None, :])
    rows, cols = linear_sum_assignment(cost)
    if not np.array_equal(rows, np.arange(len(truth))):
        raise RuntimeError("unexpected assignment row order")
    matched = est[cols]
    return [matched[:2], matched[2:]], float(np.max(cost[rows, cols]))


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


def _fit_record(Y):
    U, S, p = decompose(Y, BLOCK_ROWS)
    vals, _ = fit_from_decomposition(U, S, p, 4, DT)
    return np.asarray(vals, complex), np.asarray(S, float)


def build():
    C = _fixed_output_map()
    cells = []
    for case_index, (case, chis) in enumerate(CASES):
        blocks = [second_order_generator(c, w) for c, w in zip(chis, OMEGA_N)]
        A = block_diag(*blocks)
        truth_pairs = _truth_pairs(chis)
        truth_c = conglomerate_chi(chis, OMEGA_N)["chi_C"]
        for excitation in EXCITATION_MODES:
            participation = balanced_block_process_scales(
                blocks, C, DT, BASE_PROCESS_SCALE, excitation
            )
            records = []
            for rep in range(REPLICATES):
                try:
                    # The process random path is paired across excitation modes within
                    # each case/replicate so the comparison isolates scale allocation.
                    proc_seed = SEED + 100000 * case_index + 1000 * rep + 1
                    noise_seed = SEED + 900000 + 100000 * case_index + 1000 * rep + 2
                    Y = simulate_block_process(
                        A,
                        C,
                        DT,
                        N_SAMPLES,
                        participation["scales"],
                        np.random.default_rng(proc_seed),
                    )
                    Y = _add_measurement_noise(Y, noise_seed)
                    vals, S = _fit_record(Y)
                    pairs, max_assignment = _match_pairs(vals, truth_pairs)
                    inv = [chi_from_pole_pair(pair) for pair in pairs]
                    est_c = conglomerate_chi(
                        [x["chi"] for x in inv], [x["omega_n"] for x in inv]
                    )["chi_C"]
                    records.append(
                        {
                            "replicate": rep,
                            "status": "OK",
                            "component_chi_est": [float(x["chi"]) for x in inv],
                            "component_abs_chi_error": [
                                float(abs(x["chi"] - t)) for x, t in zip(inv, chis)
                            ],
                            "component_omega_n_est": [float(x["omega_n"]) for x in inv],
                            "chi_C_est": float(est_c),
                            "chi_C_abs_error": float(abs(est_c - truth_c)),
                            "truth_assignment_max_pole_distance": max_assignment,
                            "all_estimated_poles_stable": bool(np.all(vals.real < 0.0)),
                            "s4_over_s1": float(S[3] / S[0]),
                            "s4_over_s5_gap": float(S[3] / max(S[4], 1e-15)),
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
            cells.append(
                {
                    "case": case,
                    "component_chi_truth": list(chis),
                    "chi_C_truth": float(truth_c),
                    "excitation_mode": excitation,
                    "block_process_scales": [float(x) for x in participation["scales"]],
                    "latent_participation_fractions": [
                        float(x) for x in participation["latent_fractions"]
                    ],
                    "output_participation_fractions": [
                        float(x) for x in participation["output_fractions"]
                    ],
                    "records": records,
                    "summary": {
                        "successful": len(ok),
                        "exceptions": len(records) - len(ok),
                        "component_1_abs_chi_error": _summary(
                            [r["component_abs_chi_error"][0] for r in ok]
                        ),
                        "component_2_abs_chi_error": _summary(
                            [r["component_abs_chi_error"][1] for r in ok]
                        ),
                        "chi_C_abs_error": _summary([r["chi_C_abs_error"] for r in ok]),
                        "chi_C_est": _summary([r["chi_C_est"] for r in ok]),
                        "truth_assignment_max_pole_distance": _summary(
                            [r["truth_assignment_max_pole_distance"] for r in ok]
                        ),
                        "s4_over_s1": _summary([r["s4_over_s1"] for r in ok]),
                        "s4_over_s5_gap": _summary([r["s4_over_s5_gap"] for r in ok]),
                        "stable_fit_fraction": (
                            float(np.mean([r["all_estimated_poles_stable"] for r in ok]))
                            if ok
                            else None
                        ),
                    },
                }
            )
    return {
        "schema": "nsd-p0d12-participation-balance-chi-v1",
        "status": "P0_D_PARTICIPATION_MECHANISM_DIAGNOSIS_NOT_QUALIFICATION",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "atlas_used": False,
        "design": {
            "dt": DT,
            "n_samples": N_SAMPLES,
            "block_rows": BLOCK_ROWS,
            "fixed_development_order": 4,
            "base_process_scale": BASE_PROCESS_SCALE,
            "measurement_noise_fraction_channel_sd": MEASUREMENT_NOISE_FRACTION,
            "replicates": REPLICATES,
            "omega_n": OMEGA_N,
            "cases": [{"name": n, "chi": c} for n, c in CASES],
            "excitation_modes": EXCITATION_MODES,
        },
        "cells": cells,
        "nonclaims": [
            "No balancing construction is a biological weighting rule.",
            "No Atlas value, phenotype, outcome or target chi is used.",
            "Truth pole matching is diagnostic only.",
            "No component-support threshold or chi_system admission rule is selected.",
            "No P0-Q or P1 rule is frozen.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--output", default="results/p0d_mapping/participation_balance_chi_v1.json"
    )
    args = ap.parse_args()
    rec = build()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for cell in rec["cells"]:
        print(
            json.dumps(
                {
                    "case": cell["case"],
                    "excitation": cell["excitation_mode"],
                    "latent_fractions": cell["latent_participation_fractions"],
                    "output_fractions": cell["output_participation_fractions"],
                    **cell["summary"],
                },
                sort_keys=True,
            )
        )
    print("P0-D12 PARTICIPATION-BALANCE CHI DIAGNOSIS COMPLETE. No weighting or P1 rule frozen.")


if __name__ == "__main__":
    main()
