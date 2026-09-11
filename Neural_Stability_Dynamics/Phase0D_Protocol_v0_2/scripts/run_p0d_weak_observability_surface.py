from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.rank_gate import _candidate_from_sweep
from src.rank_sweep import adjacent_rank_stability, sweep_ssi_cov, sweep_subspace_dmd
from src.synthetic_systems import (
    add_measurement_noise,
    make_linear_system,
    make_noise_bases,
    simulate_linear,
    truth_modes,
)
from scripts.run_p0_comparator_stress_matrix import _score_against_truth


WEAK_SCALES = [1.0, 0.5, 0.25, 0.10, 0.05, 0.03, 0.02, 0.01, 0.005]
REPLICATES = 8
SEED_BASE = 202609111100


def _load_p0q1_freeze(path):
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    if cfg.get("status") != "FROZEN_P0_PROSPECTIVE_QUALIFICATION_NOT_P1":
        raise ValueError("P0Q1 freeze status is invalid")
    return cfg


def _weak_family(cfg):
    for family in cfg["oscillatory_families_expected_rank_signal"]:
        if family["name"] == "weak_second_mode_3pct_white7pct":
            return family
    raise KeyError("frozen P0Q1 weak-observability family not found")


def _system_spec(family, weak_scale):
    return {
        "modes": family["modes"],
        "similarity": family.get("similarity", "orthogonal"),
        "weak_block": int(family.get("weak_block", 1)),
        "weak_scale": float(weak_scale),
    }


def _simulate(cfg, family, weak_scale, replicate):
    seed = SEED_BASE + 10000 * int(replicate) + int(round(float(weak_scale) * 1000000))
    rng_sys = np.random.default_rng(seed)
    rng_proc = np.random.default_rng(seed + 1)
    rng_noise = np.random.default_rng(seed + 2)
    A, C = make_linear_system(_system_spec(family, weak_scale), int(cfg["n_channels"]), rng_sys)
    clean = simulate_linear(
        A,
        C,
        float(cfg["dt"]),
        int(cfg["n_samples"]),
        float(cfg["process_scale"]),
        rng_proc,
    )
    noise = family.get("noise")
    Y = clean
    if noise is not None:
        rho = float(noise.get("rho", 0.0))
        white, colored = make_noise_bases(clean.shape[0], clean.shape[1], rho, rng_noise)
        Y = add_measurement_noise(clean, noise, white, colored)
    true_vals, true_shapes = truth_modes(A, C)
    return Y, A.shape[0], true_vals, true_shapes


def _positive_indices(vals, min_hz):
    vals = np.asarray(vals, complex)
    return np.where(vals.imag / (2 * np.pi) >= float(min_hz))[0]


def _truth_output_norm_ratio(vals, shapes, min_hz):
    idx = _positive_indices(vals, min_hz)
    if len(idx) < 2:
        return None
    norms = np.asarray([np.linalg.norm(np.asarray(shapes)[:, i]) for i in idx], float)
    if len(norms) == 0 or not np.all(np.isfinite(norms)) or np.max(norms) <= 0:
        return None
    return float(np.min(norms) / np.max(norms))


def _finite(value):
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    return x if np.isfinite(x) else None


def _sweep(method, Y, cfg):
    grid = cfg["candidate_grid"]
    if method == "SSI_COV":
        return sweep_ssi_cov(Y, float(cfg["dt"]), int(cfg["block_rows"]), grid)
    if method == "SUBSPACE_DMD":
        return sweep_subspace_dmd(Y, float(cfg["dt"]), grid)
    raise ValueError(f"unsupported method: {method}")


def _score_fit(sweep, rank, true_vals, true_shapes):
    if rank is None:
        return None
    fit = sweep["fits"].get(int(rank))
    if fit is None or fit.get("status") != "OK":
        return None
    return _score_against_truth(true_vals, true_shapes, fit["vals"], fit["shapes"])


def _gap_profile(sweep, grid):
    rows = []
    for rank in grid:
        fit = sweep["fits"].get(int(rank))
        rows.append(
            {
                "rank": int(rank),
                "status": None if fit is None else fit.get("status"),
                "singular_gap_ratio": None if fit is None else _finite(fit.get("singular_gap_ratio")),
                "positive_complex_modes": None if fit is None else fit.get("positive_complex_modes"),
                "unstable_fraction": None if fit is None else _finite(fit.get("unstable_fraction")),
            }
        )
    return rows


def build_surface(cfg):
    family = _weak_family(cfg)
    rule = cfg["rank_signal_rule"]
    min_hz = float(rule["complex_frequency_min_hz"])
    grid = [int(x) for x in cfg["candidate_grid"]]
    records = []

    for weak_scale in WEAK_SCALES:
        for replicate in range(REPLICATES):
            Y, planted_order, true_vals, true_shapes = _simulate(cfg, family, weak_scale, replicate)
            truth_ratio = _truth_output_norm_ratio(true_vals, true_shapes, min_hz)
            for method in cfg["methods"]:
                sweep = _sweep(method, Y, cfg)
                gate = _candidate_from_sweep(
                    sweep,
                    grid,
                    float(rule["gap_ratio_min"]),
                    min_hz,
                )
                candidate_rank = gate.get("candidate_rank")
                candidate_score = _score_fit(sweep, candidate_rank, true_vals, true_shapes)
                oracle_score = _score_fit(sweep, planted_order, true_vals, true_shapes)
                records.append(
                    {
                        "weak_scale": float(weak_scale),
                        "replicate": int(replicate),
                        "method": method,
                        "coverage_role": (
                            "NOMINAL_FUNCTION" if weak_scale >= 0.5
                            else "PERTURBED_FUNCTION" if weak_scale >= 0.10
                            else "BOUNDARY_OR_TRANSITION"
                        ),
                        "research_mode": "P0-D",
                        "truth_output_positive_mode_norm_ratio_P0_ONLY": truth_ratio,
                        "planted_state_order_P0_ONLY": int(planted_order),
                        "historical_P0Q1_gate_overlay": {
                            "status": "NONINDEPENDENT_DIAGNOSTIC_REUSE_NOT_REQUALIFICATION",
                            "candidate_rank": candidate_rank,
                            "max_gap": _finite(gate.get("max_gap")),
                            "decision": gate.get("decision"),
                            "source_rule": "configs/P0Q1_RANK_SIGNAL_FREEZE.json",
                        },
                        "candidate_rank_truth_score_P0_ONLY": candidate_score,
                        "planted_rank_truth_score_P0_ONLY": oracle_score,
                        "gap_profile_data_only": _gap_profile(sweep, grid),
                        "adjacent_rank_stability_data_only": adjacent_rank_stability(sweep, min_hz=min_hz),
                    }
                )

    summary = []
    for weak_scale in WEAK_SCALES:
        for method in cfg["methods"]:
            group = [
                r for r in records
                if r["weak_scale"] == float(weak_scale) and r["method"] == method
            ]
            ranks = [r["historical_P0Q1_gate_overlay"]["candidate_rank"] for r in group]
            decisions = [r["historical_P0Q1_gate_overlay"]["decision"] for r in group]

            def med(path):
                vals = []
                for rec in group:
                    cur = rec
                    for key in path:
                        if cur is None:
                            break
                        cur = cur.get(key)
                    if cur is not None:
                        try:
                            cur = float(cur)
                        except (TypeError, ValueError):
                            continue
                        if np.isfinite(cur):
                            vals.append(cur)
                return float(np.median(vals)) if vals else None

            summary.append(
                {
                    "weak_scale": float(weak_scale),
                    "method": method,
                    "records": len(group),
                    "candidate_rank_counts": {str(k): v for k, v in sorted(Counter(ranks).items(), key=lambda x: str(x[0]))},
                    "decision_counts": dict(Counter(decisions)),
                    "truth_output_mode_norm_ratio_median_P0_ONLY": med(["truth_output_positive_mode_norm_ratio_P0_ONLY"]),
                    "max_gap_median": med(["historical_P0Q1_gate_overlay", "max_gap"]),
                    "candidate_rank_pole_error_median_P0_ONLY": med(["candidate_rank_truth_score_P0_ONLY", "median_relative_pole_error"]),
                    "candidate_rank_frequency_mae_hz_median_P0_ONLY": med(["candidate_rank_truth_score_P0_ONLY", "frequency_mae_hz"]),
                    "candidate_rank_decay_mae_median_P0_ONLY": med(["candidate_rank_truth_score_P0_ONLY", "relative_decay_mae"]),
                    "candidate_rank_carrier_subspace_similarity_median_P0_ONLY": med(["candidate_rank_truth_score_P0_ONLY", "matched_carrier_subspace_similarity"]),
                    "planted_rank_unstable_fraction_median_P0_ONLY": med(["planted_rank_truth_score_P0_ONLY", "estimated_unstable_fraction"]),
                    "planted_rank_pole_error_median_P0_ONLY": med(["planted_rank_truth_score_P0_ONLY", "median_relative_pole_error"]),
                }
            )

    return {
        "schema": "nsd-phase0d-v0.2-p0d2-weak-observability-surface-v1",
        "status": "P0_D_POST_RESULT_RESPONSE_SURFACE_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + v0.7.1A Addendum",
        "p1_authorized": False,
        "origin": "P0-D follow-up because P0-D1 localized all planted-rank stops to the weak-observability condition; axis choice is therefore post-result/data-derived.",
        "p0q1_status_firewall": {
            "SSI_COV": "SURVIVES_P0Q1_UNCHANGED",
            "SUBSPACE_DMD": "FAILS_P0Q1_UNCHANGED",
            "note": "The frozen P0Q1 rank-signal rule is reused only as a diagnostic overlay. These new records cannot rescue or requalify P0Q1."
        },
        "control": {
            "weak_scales": WEAK_SCALES,
            "replicates_per_scale": REPLICATES,
            "seed_base": SEED_BASE,
            "frozen_P0Q1_rule_source": "configs/P0Q1_RANK_SIGNAL_FREEZE.json",
            "candidate_grid": grid,
            "gap_ratio_min": float(rule["gap_ratio_min"]),
            "complex_frequency_min_hz": min_hz,
            "base_family": family,
        },
        "summary": summary,
        "records": records,
        "nonclaims": [
            "This is P0-D response-surface mapping, not a new P0-Q holdout and not P1.",
            "The weak-scale axis was selected after P0-D1 and is explicitly post-result.",
            "The historical P0Q1 gate overlay is non-independent diagnostic reuse and cannot change the official P0Q1 outcomes.",
            "No new threshold is fit to this surface.",
            "Planted latent order and data-derived candidate rank are kept as separate objects.",
            "No EEG, biological mechanism, phenotype, chi coordinate or neural regime boundary is tested."
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze", default="configs/P0Q1_RANK_SIGNAL_FREEZE.json")
    parser.add_argument("--output", default="results/p0d_mapping/weak_observability_surface_v1.json")
    args = parser.parse_args()
    cfg = _load_p0q1_freeze(args.freeze)
    record = build_surface(cfg)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for row in record["summary"]:
        print(json.dumps(row, sort_keys=True))
    print("P0-D WEAK-OBSERVABILITY RESPONSE SURFACE COMPLETE. No P0Q1 or P1 status changed.")


if __name__ == "__main__":
    main()
