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

from src.chi_conglomerate import chi_from_pole_pair, second_order_generator
from src.participation_balance import (
    balanced_block_process_scales,
    participation_from_scales,
    simulate_block_process,
)
from src.pole_lineage import (
    advance_two_lineages,
    count_valid_second_order_partitions,
    initial_two_lineages,
    pair_set_distance,
)
from src.ssi_cov import decompose, fit_from_decomposition

DT = 0.01
N_SAMPLES = 8000
BLOCK_ROWS = 30
BASE_PROCESS_SCALE = 0.30
MEASUREMENT_NOISE_FRACTION = 0.03
REPLICATES = 8
SEED = 202609111500
TARGET_OMEGA_N = 2.0 * np.pi * 2.0
COMPANION_OMEGA_N = 2.0 * np.pi * 7.0
COMPANION_CHI = 0.55
REFERENCE_BALANCE_CHI = 0.70
CHI_PATH = [0.50, 0.70, 0.85, 0.93, 0.97, 0.99, 1.00, 1.01, 1.03, 1.07, 1.15, 1.30, 1.50]
VISIBILITY = ["fixed_reference_output_balance", "pointwise_output_balance"]


def _fixed_output_map():
    rng = np.random.default_rng(SEED)
    C = rng.normal(size=(8, 4))
    return C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)


def _blocks(target_chi):
    return [
        second_order_generator(target_chi, TARGET_OMEGA_N),
        second_order_generator(COMPANION_CHI, COMPANION_OMEGA_N),
    ]


def _add_measurement_noise(Y, seed):
    rng = np.random.default_rng(seed)
    sd = np.maximum(Y.std(axis=0, keepdims=True), 1e-12)
    out = Y + MEASUREMENT_NOISE_FRACTION * sd * rng.normal(size=Y.shape)
    out -= out.mean(axis=0, keepdims=True)
    return out


def _fit(Y):
    U, S, p = decompose(Y, BLOCK_ROWS)
    vals, _ = fit_from_decomposition(U, S, p, 4, DT)
    return np.asarray(vals, complex), np.asarray(S, float)


def _truth_pairs(target_chi):
    return [
        np.linalg.eigvals(second_order_generator(target_chi, TARGET_OMEGA_N)),
        np.linalg.eigvals(second_order_generator(COMPANION_CHI, COMPANION_OMEGA_N)),
    ]


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


def _branch_from_invariant(inv):
    nd = float(inv["chi"] * inv["chi"] - 1.0)
    if nd < -1e-8:
        return "UNDERDAMPED_COMPLEX_SIDE"
    if nd > 1e-8:
        return "OVERDAMPED_REAL_SIDE"
    return "REPEATED_ROOT_BOUNDARY"


def _fixed_scales(C):
    ref = _blocks(REFERENCE_BALANCE_CHI)
    return balanced_block_process_scales(
        ref, C, DT, BASE_PROCESS_SCALE, "output_trace"
    )["scales"]


def _scales_and_participation(target_chi, C, visibility, fixed_scales):
    blocks = _blocks(target_chi)
    if visibility == "fixed_reference_output_balance":
        scales = fixed_scales
    elif visibility == "pointwise_output_balance":
        scales = balanced_block_process_scales(
            blocks, C, DT, BASE_PROCESS_SCALE, "output_trace"
        )["scales"]
    else:
        raise ValueError("unknown visibility condition")
    return scales, participation_from_scales(blocks, C, DT, scales)


def _run_path(rep, visibility, C, fixed_scales):
    previous = None
    initialized_at = None
    rows = []
    for point_index, target_chi in enumerate(CHI_PATH):
        truth = _truth_pairs(target_chi)
        blocks = _blocks(target_chi)
        A = block_diag(*blocks)
        scales, participation = _scales_and_participation(
            target_chi, C, visibility, fixed_scales
        )
        try:
            vis_offset = 0 if visibility == VISIBILITY[0] else 50000000
            proc_seed = SEED + vis_offset + rep * 100000 + point_index * 1000 + 1
            noise_seed = SEED + vis_offset + rep * 100000 + point_index * 1000 + 2
            Y = simulate_block_process(
                A,
                C,
                DT,
                N_SAMPLES,
                scales,
                np.random.default_rng(proc_seed),
            )
            Y = _add_measurement_noise(Y, noise_seed)
            vals, S = _fit(Y)
            static = count_valid_second_order_partitions(vals)
            if previous is None:
                step = initial_two_lineages(vals)
                pairs = step["pairs"]
                continuity = None
                initialization_cost = float(step["initialization_cost"])
                initialized_at = target_chi
            else:
                step = advance_two_lineages(previous, vals)
                pairs = step["pairs"]
                continuity = float(step["continuity_cost_total"])
                initialization_cost = None
            inv_target = chi_from_pole_pair(pairs[0])
            inv_companion = chi_from_pole_pair(pairs[1])
            target_truth_distance = pair_set_distance(truth[0], pairs[0])
            companion_truth_distance = pair_set_distance(truth[1], pairs[0])
            identity_correct = target_truth_distance < companion_truth_distance
            rows.append(
                {
                    "point_index": point_index,
                    "chi_truth": target_chi,
                    "status": "OK",
                    "initialized_at_chi": initialized_at,
                    "chi_est": float(inv_target["chi"]),
                    "chi_abs_error": float(abs(inv_target["chi"] - target_chi)),
                    "target_branch_est": _branch_from_invariant(inv_target),
                    "target_pair_complex": bool(np.max(np.abs(pairs[0].imag)) > 1e-7),
                    "companion_chi_est": float(inv_companion["chi"]),
                    "retrospective_target_identity_correct": bool(identity_correct),
                    "target_truth_pair_distance": float(target_truth_distance),
                    "target_to_companion_truth_distance": float(companion_truth_distance),
                    "continuity_cost": continuity,
                    "initialization_cost": initialization_cost,
                    "static_valid_second_order_partitions": int(static["count"]),
                    "target_output_participation_fraction": float(
                        participation["output_fractions"][0]
                    ),
                    "companion_output_participation_fraction": float(
                        participation["output_fractions"][1]
                    ),
                    "block_process_scales": [float(x) for x in scales],
                    "all_estimated_poles_stable": bool(np.all(vals.real < 0.0)),
                    "s4_over_s1": float(S[3] / S[0]),
                    "tracked_target_poles": [
                        {"real": float(z.real), "imag": float(z.imag)} for z in pairs[0]
                    ],
                }
            )
            previous = [pairs[0].copy(), pairs[1].copy()]
        except Exception as exc:
            rows.append(
                {
                    "point_index": point_index,
                    "chi_truth": target_chi,
                    "status": "EXCEPTION_PRESERVED",
                    "initialized_at_chi": initialized_at,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "target_output_participation_fraction": float(
                        participation["output_fractions"][0]
                    ),
                    "companion_output_participation_fraction": float(
                        participation["output_fractions"][1]
                    ),
                    "block_process_scales": [float(x) for x in scales],
                }
            )
    return rows


def _point_summaries(paths, visibility):
    rows = []
    for point_index, chi in enumerate(CHI_PATH):
        here = [p[point_index] for p in paths]
        ok = [r for r in here if r["status"] == "OK"]
        rows.append(
            {
                "visibility": visibility,
                "chi_truth": chi,
                "successful": len(ok),
                "exceptions": len(here) - len(ok),
                "chi_est": _summary([r["chi_est"] for r in ok]),
                "chi_abs_error": _summary([r["chi_abs_error"] for r in ok]),
                "identity_correct_fraction": (
                    float(np.mean([r["retrospective_target_identity_correct"] for r in ok]))
                    if ok
                    else None
                ),
                "complex_pair_fraction": (
                    float(np.mean([r["target_pair_complex"] for r in ok])) if ok else None
                ),
                "continuity_cost": _summary(
                    [r["continuity_cost"] for r in ok if r["continuity_cost"] is not None]
                ),
                "static_valid_second_order_partitions": _summary(
                    [r["static_valid_second_order_partitions"] for r in ok]
                ),
                "target_output_participation_fraction": _summary(
                    [r["target_output_participation_fraction"] for r in here]
                ),
                "s4_over_s1": _summary([r["s4_over_s1"] for r in ok]),
                "stable_fit_fraction": (
                    float(np.mean([r["all_estimated_poles_stable"] for r in ok]))
                    if ok
                    else None
                ),
            }
        )
    return rows


def build():
    C = _fixed_output_map()
    fixed_scales = _fixed_scales(C)
    all_conditions = []
    for visibility in VISIBILITY:
        paths = [_run_path(rep, visibility, C, fixed_scales) for rep in range(REPLICATES)]
        all_conditions.append(
            {
                "visibility": visibility,
                "paths": paths,
                "point_summaries": _point_summaries(paths, visibility),
            }
        )
    return {
        "schema": "nsd-p0d13-chi-lineage-through-ep-v1",
        "status": "P0_D_BOUNDARY_LINEAGE_MAP_NOT_QUALIFICATION",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "atlas_used": False,
        "design": {
            "dt": DT,
            "n_samples": N_SAMPLES,
            "block_rows": BLOCK_ROWS,
            "fixed_development_order": 4,
            "measurement_noise_fraction_channel_sd": MEASUREMENT_NOISE_FRACTION,
            "replicates": REPLICATES,
            "target_omega_n": TARGET_OMEGA_N,
            "companion_omega_n": COMPANION_OMEGA_N,
            "companion_chi": COMPANION_CHI,
            "chi_path": CHI_PATH,
            "visibility_conditions": VISIBILITY,
            "fixed_reference_balance_chi": REFERENCE_BALANCE_CHI,
            "fixed_reference_scales": [float(x) for x in fixed_scales],
        },
        "conditions": all_conditions,
        "nonclaims": [
            "The pole-continuity rule is a P0-D candidate, not a frozen real-data lineage rule.",
            "Pointwise visibility balance is a synthetic control, not a biological weighting rule.",
            "Truth is used only for retrospective identity scoring.",
            "No Atlas value, phenotype, outcome or target zone is used.",
            "No chi_system admission, confidence rule, P0-Q rule or P1 rule is frozen.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--output", default="results/p0d_mapping/chi_lineage_through_ep_v1.json"
    )
    args = ap.parse_args()
    rec = build()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for condition in rec["conditions"]:
        for row in condition["point_summaries"]:
            print(json.dumps(row, sort_keys=True))
    print("P0-D13 CHI LINEAGE THROUGH EP COMPLETE. No real-data lineage or P1 rule frozen.")


if __name__ == "__main__":
    main()
