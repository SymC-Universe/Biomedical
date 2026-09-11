from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.dmd import fit_subspace_dmd
from scripts.run_p0_comparator_stress_matrix import (
    DT,
    REPLICATES,
    _aggregate_method,
    _condition_specs,
    _score_against_truth,
    _simulate_condition,
)


def run_matrix():
    rows = []
    for condition in _condition_specs():
        records = []
        order = None
        for replicate in range(REPLICATES):
            Y, order, true_vals, true_shapes = _simulate_condition(condition, replicate)
            try:
                vals, shapes = fit_subspace_dmd(Y, DT, order)
                rec = _score_against_truth(true_vals, true_shapes, vals, shapes)
                rec["status"] = "OK"
            except Exception as exc:
                rec = {
                    "status": "METHOD_EXCEPTION_PRESERVED",
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                }
            records.append(rec)
        rows.append({
            "condition": condition["name"],
            "replicates": REPLICATES,
            "oracle_state_rank": int(order),
            "method": "SUBSPACE_DMD_ORACLE_RANK",
            "summary": _aggregate_method(records),
            "records": records,
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/p0_qualification/subspace_dmd_stress_addendum.json",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema": "nsd-phase0d-v0.2-p0-subspace-dmd-stress-v1",
        "status": "P0_DEVELOPMENT_MATRIX_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL",
        "p1_authorized": False,
        "method_lineage": (
            "Python translation of the corrected author implementation for "
            "Takeishi, Kawahara & Yairi, Phys. Rev. E 96, 033310 (2017)."
        ),
        "same_conditions_as": "comparator_stress_matrix.json",
        "rank_policy": "same P0 oracle state rank used by the existing comparator matrix",
        "stress": run_matrix(),
        "nonclaims": [
            "Subspace DMD is not frozen as the P1 comparator.",
            "No P0 performance difference is a confirmatory superiority claim.",
            "The stochastic Koopman assumptions have not yet been licensed for EEG.",
            "No neural threshold, chi value, regime boundary, phenotype, or mechanism is tested."
        ],
    }
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("P0 SUBSPACE-DMD STRESS ADDENDUM COMPLETE. No P1 science was executed.")


if __name__ == "__main__":
    main()
