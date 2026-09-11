from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.rank_gate import _candidate_from_sweep
from src.rank_sweep import sweep_subspace_dmd, singular_gap_ratio
from src.synthetic_systems import make_linear_system, simulate_linear

DT = 0.02
N_CHANNELS = 8
PROCESS_SCALE = 0.35
LENGTHS = [1300, 2600, 5200, 10400]
REPLICATES = 8
GRID = list(range(1, 9))
SEED = 202609112800
RULE = {"gap_ratio_min": 3.0, "complex_frequency_min_hz": 0.25}

FAMILIES = [
    {
        "name": "two_real_poles",
        "state_dimension": 2,
        "truth_positive_complex_modes": 0,
        "modes": [
            {"type": "real", "pole": -0.7},
            {"type": "real", "pole": -2.4},
        ],
    },
    {
        "name": "one_oscillatory_pair",
        "state_dimension": 2,
        "truth_positive_complex_modes": 1,
        "modes": [
            {"type": "complex", "decay": 0.7, "frequency_hz": 5.0},
        ],
    },
]


def _record(family, n, rep):
    seed = SEED + 1000000 * FAMILIES.index(family) + 10000 * rep + n
    A, C = make_linear_system(
        {"modes": family["modes"], "similarity": "orthogonal"},
        N_CHANNELS,
        np.random.default_rng(seed),
    )
    Y = simulate_linear(
        A,
        C,
        DT,
        n,
        PROCESS_SCALE,
        np.random.default_rng(seed + 1),
    )
    return Y


def _stats(x):
    a = np.asarray(x, float)
    a = a[np.isfinite(a)]
    if len(a) == 0:
        return {"n": 0, "median": None, "p10": None, "p90": None}
    return {
        "n": int(len(a)),
        "median": float(np.median(a)),
        "p10": float(np.quantile(a, 0.10)),
        "p90": float(np.quantile(a, 0.90)),
    }


def build():
    groups = []
    for family in FAMILIES:
        for n in LENGTHS:
            records = []
            for rep in range(REPLICATES):
                Y = _record(family, n, rep)
                sw = sweep_subspace_dmd(Y, DT, GRID)
                S = np.asarray(sw["singular_values"], float)
                s0 = max(float(S[0]), np.finfo(float).tiny)
                gate = _candidate_from_sweep(
                    sw,
                    GRID,
                    RULE["gap_ratio_min"],
                    RULE["complex_frequency_min_hz"],
                )
                rank_rows = []
                for r in GRID:
                    fit = sw["fits"][r]
                    row = {
                        "rank": r,
                        "support_over_s1": float(S[r - 1] / s0),
                        "next_support_over_s1": float(S[r] / s0),
                        "gap": singular_gap_ratio(S, r),
                        "status": fit.get("status"),
                    }
                    if fit.get("status") == "OK":
                        vals = np.asarray(fit["vals"], complex)
                        pos = vals.imag / (2.0 * np.pi) >= RULE["complex_frequency_min_hz"]
                        row.update(
                            {
                                "unstable_poles": int(np.sum(vals.real >= 0.0)),
                                "positive_complex_modes": int(np.sum(pos)),
                                "stable_positive_complex_modes": int(np.sum(pos & (vals.real < 0.0))),
                            }
                        )
                    rank_rows.append(row)

                selected_rank = gate.get("candidate_rank")
                selected = None
                if selected_rank is not None:
                    selected = next(x for x in rank_rows if x["rank"] == selected_rank)
                records.append(
                    {
                        "replicate": rep,
                        "input_sha256": hashlib.sha256(np.ascontiguousarray(Y).tobytes()).hexdigest(),
                        "gate": gate,
                        "selected": selected,
                        "rank_rows": rank_rows,
                    }
                )

            selected = [r["selected"] for r in records if r["selected"] is not None]
            selected_ranks = [r["rank"] for r in selected]
            selected_support = [r["support_over_s1"] for r in selected]
            selected_next = [r["next_support_over_s1"] for r in selected]
            selected_gap = [r["gap"] for r in selected]
            decisions = [r["gate"]["decision"] for r in records]
            over_rank = [x > family["state_dimension"] for x in selected_ranks]
            false_complex = []
            for row in selected:
                if row.get("status") != "OK":
                    continue
                false_complex.append(
                    max(0, row.get("stable_positive_complex_modes", 0) - family["truth_positive_complex_modes"])
                )
            groups.append(
                {
                    "family": family["name"],
                    "coverage_role": "BOUNDARY_OR_TRANSITION",
                    "n_samples": n,
                    "state_dimension": family["state_dimension"],
                    "truth_positive_complex_modes": family["truth_positive_complex_modes"],
                    "records": records,
                    "summary": {
                        "candidate_rank_counts": {str(r): selected_ranks.count(r) for r in sorted(set(selected_ranks))},
                        "decision_counts": {d: decisions.count(d) for d in sorted(set(decisions))},
                        "selected_rank_exceeds_truth_dimension_fraction": float(np.mean(over_rank)) if over_rank else None,
                        "selected_support_over_s1": _stats(selected_support),
                        "selected_next_support_over_s1": _stats(selected_next),
                        "selected_gap": _stats(selected_gap),
                        "extra_stable_positive_complex_modes": _stats(false_complex),
                    },
                }
            )

    return {
        "schema": "nsd-p0d8-subspace-dmd-tail-gap-v1",
        "status": "P0_D_RETROSPECTIVE_MECHANISM_MAPPING_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p0q1_status": "SUBSPACE_DMD_FAILS_P0Q1_UNCHANGED",
        "p1_authorized": False,
        "hypothesis": "largest adjacent singular gap can occur in weak finite-sample tail directions and need not equal supported dynamic rank",
        "design": {
            "lengths": LENGTHS,
            "replicates": REPLICATES,
            "candidate_grid": GRID,
            "channels": N_CHANNELS,
            "dt": DT,
            "process_scale": PROCESS_SCALE,
            "families": [x["name"] for x in FAMILIES],
        },
        "groups": groups,
        "nonclaims": [
            "Frozen P0Q1 is not rescored or repaired.",
            "No new support-floor or rank threshold is selected.",
            "Truth is used only for retrospective synthetic diagnosis.",
            "Any revised comparator rule requires a new version and untouched P0-Q evidence.",
        ],
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/p0d_mapping/subspace_dmd_tail_gap_v1.json")
    args = ap.parse_args()
    rec = build()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for g in rec["groups"]:
        print(json.dumps({"family": g["family"], "n_samples": g["n_samples"], **g["summary"]}, sort_keys=True))
    print("P0-D8 SUBSPACE-DMD TAIL-GAP FORENSICS COMPLETE. Frozen P0Q1 unchanged.")
