from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.rank_sweep import sweep_ssi_cov, sweep_subspace_dmd
from src.synthetic_systems import generate_1f, make_noise_bases
from scripts.run_p0_comparator_stress_matrix import (
    DT,
    N_CHANNELS,
    N_SAMPLES,
    REPLICATES,
    _condition_specs,
    _simulate_condition,
)

CANDIDATE_RANKS = [1, 2, 3, 4, 5, 6]
NULL_REPLICATES = 12
BLOCK_ROWS = 18


def _finite_gap_by_rank(sweep):
    out = {}
    for rank, fit in sorted(sweep["fits"].items()):
        g = fit.get("singular_gap_ratio")
        out[int(rank)] = None if g is None or not np.isfinite(g) else float(g)
    return out


def _max_gap_record(sweep):
    by_rank = _finite_gap_by_rank(sweep)
    finite = [(rank, gap) for rank, gap in by_rank.items() if gap is not None]
    if not finite:
        return {
            "status": "NO_FINITE_GAP",
            "max_gap": None,
            "argmax_rank": None,
            "gap_by_rank": {str(k): v for k, v in by_rank.items()},
        }
    rank, gap = max(finite, key=lambda x: x[1])
    return {
        "status": "P0_DIAGNOSTIC_NOT_SELECTED",
        "max_gap": float(gap),
        "argmax_rank": int(rank),
        "gap_by_rank": {str(k): v for k, v in by_rank.items()},
    }


def _evaluate_record(Y):
    return {
        "SSI_COV": _max_gap_record(
            sweep_ssi_cov(Y, DT, BLOCK_ROWS, CANDIDATE_RANKS)
        ),
        "SUBSPACE_DMD": _max_gap_record(
            sweep_subspace_dmd(Y, DT, CANDIDATE_RANKS)
        ),
    }


def _null_record(kind, replicate):
    seed = 910000 + 1000 * replicate + sum(ord(c) for c in kind)
    rng = np.random.default_rng(seed)
    if kind == "iid_white":
        Y = rng.normal(size=(N_SAMPLES, N_CHANNELS))
    elif kind == "spatially_mixed_white":
        Z = rng.normal(size=(N_SAMPLES, N_CHANNELS))
        M = rng.normal(size=(N_CHANNELS, N_CHANNELS))
        Y = Z @ M.T
        Y -= Y.mean(0, keepdims=True)
        Y /= np.maximum(Y.std(0, keepdims=True), 1e-12)
    elif kind == "ar1_rho0p8":
        _, colored = make_noise_bases(
            N_SAMPLES, N_CHANNELS, 0.8, rng
        )
        M = rng.normal(size=(N_CHANNELS, N_CHANNELS))
        Y = colored @ M.T
        Y -= Y.mean(0, keepdims=True)
        Y /= np.maximum(Y.std(0, keepdims=True), 1e-12)
    elif kind == "one_over_f_beta1":
        Y = generate_1f(N_SAMPLES, N_CHANNELS, 1.0, rng)
    elif kind == "one_over_f_beta2":
        Y = generate_1f(N_SAMPLES, N_CHANNELS, 2.0, rng)
    else:
        raise ValueError("unknown null kind")
    return _evaluate_record(Y)


def _structured_records():
    out = []
    for condition in _condition_specs():
        rows = []
        for replicate in range(REPLICATES):
            Y, true_order, _, _ = _simulate_condition(condition, replicate)
            rows.append({
                "replicate": replicate,
                "true_state_order_P0_evaluation_only": int(true_order),
                "methods": _evaluate_record(Y),
            })
        out.append({"condition": condition["name"], "records": rows})
    return out


def _null_records():
    kinds = [
        "iid_white",
        "spatially_mixed_white",
        "ar1_rho0p8",
        "one_over_f_beta1",
        "one_over_f_beta2",
    ]
    out = []
    for kind in kinds:
        rows = []
        for replicate in range(NULL_REPLICATES):
            rows.append({
                "replicate": replicate,
                "methods": _null_record(kind, replicate),
            })
        out.append({"null_family": kind, "records": rows})
    return out


def _summary(rows, method):
    gaps = []
    ranks = []
    for row in rows:
        rec = row["methods"][method]
        if rec["max_gap"] is not None:
            gaps.append(float(rec["max_gap"]))
            ranks.append(int(rec["argmax_rank"]))
    if not gaps:
        return {"n": 0}
    unique, counts = np.unique(np.asarray(ranks, int), return_counts=True)
    return {
        "n": int(len(gaps)),
        "max_gap_min": float(np.min(gaps)),
        "max_gap_q10": float(np.quantile(gaps, 0.10)),
        "max_gap_median": float(np.median(gaps)),
        "max_gap_q90": float(np.quantile(gaps, 0.90)),
        "max_gap_max": float(np.max(gaps)),
        "argmax_rank_counts": {
            str(int(k)): int(v) for k, v in zip(unique, counts)
        },
    }


def _attach_summaries(groups, group_key):
    out = []
    for group in groups:
        rows = group["records"]
        out.append({
            group_key: group[group_key],
            "summary": {
                "SSI_COV": _summary(rows, "SSI_COV"),
                "SUBSPACE_DMD": _summary(rows, "SUBSPACE_DMD"),
            },
            "records": rows,
        })
    return out


def build_record():
    structured = _attach_summaries(_structured_records(), "condition")
    nulls = _attach_summaries(_null_records(), "null_family")
    return {
        "schema": "nsd-phase0d-v0.2-p0-rank-signal-null-stress-v1",
        "status": "P0_DIAGNOSTIC_STRESS_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL",
        "p1_authorized": False,
        "candidate_grid": CANDIDATE_RANKS,
        "structured_replicates_per_condition": REPLICATES,
        "null_replicates_per_family": NULL_REPLICATES,
        "purpose": (
            "Measure whether method-native singular-gap strength and its argmax rank "
            "carry any truth-blind evidence that separates structured stochastic systems "
            "from null/no-discrete-mode processes. No threshold or selector is created."
        ),
        "structured": structured,
        "nulls": nulls,
        "nonclaims": [
            "The maximum gap is not an accepted rank selector.",
            "No null-calibrated refusal threshold is selected from these development records.",
            "Any threshold suggested after inspection is DATA_DERIVED and incurs promotion debt.",
            "The null families are method stressors, not an exhaustive model of resting EEG background activity.",
            "No EEG, phenotype, chi, regime boundary, or mechanism is tested."
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/p0_qualification/rank_signal_null_stress.json",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_record(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("P0 RANK-SIGNAL NULL STRESS COMPLETE. No selector and no P1 science executed.")


if __name__ == "__main__":
    main()
