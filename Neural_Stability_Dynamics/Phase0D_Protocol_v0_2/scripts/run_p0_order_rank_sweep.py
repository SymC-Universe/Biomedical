from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.rank_sweep import adjacent_rank_stability, sweep_ssi_cov, sweep_subspace_dmd
from scripts.run_p0_comparator_stress_matrix import (
    DT,
    MIN_HZ,
    REPLICATES,
    _condition_specs,
    _score_against_truth,
    _simulate_condition,
)

CANDIDATE_RANKS = [1, 2, 3, 4, 5, 6]


def _data_only_fit_record(fit):
    out = {
        "status": fit.get("status"),
        "singular_gap_ratio": (
            None
            if not np.isfinite(fit.get("singular_gap_ratio", np.nan))
            else float(fit["singular_gap_ratio"])
        ),
    }
    if fit.get("status") == "OK":
        vals = np.asarray(fit["vals"], complex)
        out.update({
            "estimated_poles": int(len(vals)),
            "estimated_positive_complex_modes": int(
                np.sum(vals.imag / (2 * np.pi) >= MIN_HZ)
            ),
            "unstable_fraction": float(fit["unstable_fraction"]),
        })
    else:
        out.update({
            "exception_type": fit.get("exception_type"),
            "exception_message": fit.get("exception_message"),
        })
    return out


def _one_sweep_record(sweep, true_vals, true_shapes):
    ranks = {}
    for rank, fit in sorted(sweep["fits"].items()):
        row = {"data_only": _data_only_fit_record(fit)}
        if fit.get("status") == "OK":
            row["truth_evaluation_P0_only"] = _score_against_truth(
                true_vals, true_shapes, fit["vals"], fit["shapes"]
            )
        else:
            row["truth_evaluation_P0_only"] = None
        ranks[str(rank)] = row
    return {
        "selection": None,
        "selection_status": sweep["selection_status"],
        "singular_values_first_12": [float(x) for x in sweep["singular_values"][:12]],
        "ranks": ranks,
        "adjacent_rank_stability_data_only": adjacent_rank_stability(
            sweep, min_hz=MIN_HZ
        ),
    }


def _finite(values):
    return np.asarray([v for v in values if v is not None and np.isfinite(v)], float)


def _aggregate(records, method):
    by_rank = {}
    for rank in CANDIDATE_RANKS:
        data_rows = []
        truth_rows = []
        for record in records:
            row = record[method]["ranks"][str(rank)]
            data_rows.append(row["data_only"])
            if row["truth_evaluation_P0_only"] is not None:
                truth_rows.append(row["truth_evaluation_P0_only"])
        ok = [r for r in data_rows if r["status"] == "OK"]
        gaps = _finite([r.get("singular_gap_ratio") for r in ok])
        unstable = _finite([r.get("unstable_fraction") for r in ok])
        pole_err = _finite([r.get("median_relative_pole_error") for r in truth_rows])
        freq_err = _finite([r.get("frequency_mae_hz") for r in truth_rows])
        decay_err = _finite([r.get("relative_decay_mae") for r in truth_rows])
        coverage = _finite([r.get("matched_fraction_of_truth") for r in truth_rows])
        subspace = _finite([
            r.get("matched_carrier_subspace_similarity") for r in truth_rows
        ])
        by_rank[str(rank)] = {
            "records": len(data_rows),
            "ok_records": len(ok),
            "method_exceptions": len(data_rows) - len(ok),
            "singular_gap_ratio_median": float(np.median(gaps)) if len(gaps) else None,
            "unstable_fraction_median": float(np.median(unstable)) if len(unstable) else None,
            "truth_matched_fraction_median_P0_only": float(np.median(coverage)) if len(coverage) else None,
            "truth_median_relative_pole_error_median_P0_only": float(np.median(pole_err)) if len(pole_err) else None,
            "truth_frequency_mae_hz_median_P0_only": float(np.median(freq_err)) if len(freq_err) else None,
            "truth_relative_decay_mae_median_P0_only": float(np.median(decay_err)) if len(decay_err) else None,
            "truth_carrier_subspace_similarity_median_P0_only": float(np.median(subspace)) if len(subspace) else None,
        }
    return by_rank


def build_record():
    conditions = []
    for condition in _condition_specs():
        records = []
        for replicate in range(REPLICATES):
            Y, true_order, true_vals, true_shapes = _simulate_condition(condition, replicate)
            ssi = sweep_ssi_cov(Y, DT, block_rows=18, candidate_orders=CANDIDATE_RANKS)
            sub = sweep_subspace_dmd(Y, DT, candidate_ranks=CANDIDATE_RANKS)
            records.append({
                "replicate": replicate,
                "true_state_order_P0_evaluation_only": int(true_order),
                "SSI_COV": _one_sweep_record(ssi, true_vals, true_shapes),
                "SUBSPACE_DMD": _one_sweep_record(sub, true_vals, true_shapes),
            })
        conditions.append({
            "condition": condition["name"],
            "replicates": REPLICATES,
            "candidate_rank_order_grid": CANDIDATE_RANKS,
            "aggregates": {
                "SSI_COV": _aggregate(records, "SSI_COV"),
                "SUBSPACE_DMD": _aggregate(records, "SUBSPACE_DMD"),
            },
            "records": records,
        })

    return {
        "schema": "nsd-phase0d-v0.2-p0-order-rank-sweep-v1",
        "status": "P0_TRUTH_BLIND_SWEEP_WITH_SEPARATE_TRUTH_EVALUATION_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL",
        "p1_authorized": False,
        "candidate_grid": CANDIDATE_RANKS,
        "firewall": (
            "Sweep functions receive measurements and method settings only. They do not "
            "receive truth, labels, chi, phenotype or outcomes and they return no selected rank. "
            "Known truth is attached afterward in this P0 script strictly for evaluation."
        ),
        "conditions": conditions,
        "nonclaims": [
            "No rank or order is selected by this sweep.",
            "No singular-gap, stability, error, MAC or assignment-margin threshold is frozen.",
            "No truth-derived optimum may be reused as a P1 selector without promotion debt and new untouched evidence.",
            "SSI and Subspace-DMD singular spectra are method-native diagnostics and are not numerically interchangeable.",
            "No EEG, phenotype, chi, regime boundary or mechanism is tested."
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/p0_qualification/order_rank_sweep.json",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_record(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("P0 ORDER/RANK SWEEP COMPLETE. No rank selected and no P1 science executed.")


if __name__ == "__main__":
    main()
