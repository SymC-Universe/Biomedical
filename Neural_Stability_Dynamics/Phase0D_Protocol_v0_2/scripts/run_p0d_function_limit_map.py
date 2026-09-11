from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.landscape import make_mapping_record, split_function_limit
from src.rank_sweep import adjacent_rank_stability, sweep_ssi_cov, sweep_subspace_dmd
from scripts.run_p0_comparator_stress_matrix import (
    BLOCK_ROWS,
    DT,
    MIN_HZ,
    REPLICATES,
    _condition_specs,
    _score_against_truth,
    _simulate_condition,
)


CANDIDATE_RANKS = [1, 2, 3, 4, 5, 6]

ROLE_BY_CONDITION = {
    "baseline_stochastic": "NOMINAL_FUNCTION",
    "white_sensor_10pct": "PERTURBED_FUNCTION",
    "colored_sensor_10pct_rho0p8": "PERTURBED_FUNCTION",
    "condition_number_25_plus_white5pct": "PERTURBED_FUNCTION",
    "weak_second_mode_5pct_plus_white5pct": "BOUNDARY_OR_TRANSITION",
    "crowded_modes_plus_white5pct": "BOUNDARY_OR_TRANSITION",
}


def _finite_or_none(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if np.isfinite(value) else None


def _json_clean(value):
    if isinstance(value, dict):
        return {str(k): _json_clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_clean(v) for v in value]
    if isinstance(value, np.ndarray):
        return [_json_clean(v) for v in value.tolist()]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return _finite_or_none(value)
    if isinstance(value, complex):
        return {"real": float(value.real), "imag": float(value.imag)}
    if isinstance(value, float) and not np.isfinite(value):
        return None
    return value


def _all_rank_data_only(sweep):
    rows = []
    for rank, fit in sorted(sweep["fits"].items()):
        row = {
            "rank_or_order": int(rank),
            "status": fit.get("status"),
            "singular_gap_ratio": _finite_or_none(fit.get("singular_gap_ratio")),
        }
        if fit.get("status") == "OK":
            vals = np.asarray(fit["vals"], complex)
            row.update(
                {
                    "estimated_poles": int(len(vals)),
                    "positive_complex_modes": int(
                        np.sum(vals.imag / (2 * np.pi) >= MIN_HZ)
                    ),
                    "unstable_fraction": _finite_or_none(fit.get("unstable_fraction")),
                }
            )
        else:
            row.update(
                {
                    "exception_type": fit.get("exception_type"),
                    "exception_message": fit.get("exception_message"),
                }
            )
        rows.append(row)
    return rows


def _conditional_claim_record(
    *,
    condition,
    replicate,
    method,
    sweep,
    planted_order,
    true_vals,
    true_shapes,
):
    role = ROLE_BY_CONDITION[condition["name"]]
    fit = sweep["fits"].get(int(planted_order))
    controls = {
        "condition": condition["name"],
        "replicate": int(replicate),
        "planted_state_order_P0_truth_only": int(planted_order),
        "dt": DT,
        "block_rows_if_SSI_COV": BLOCK_ROWS if method == "SSI_COV" else None,
        "candidate_rank_order_grid": CANDIDATE_RANKS,
        "system_spec_P0_known_truth": condition["system"],
        "measurement_noise": condition["noise"],
    }

    if fit is None or fit.get("status") != "OK":
        observables = {
            "method_status": None if fit is None else fit.get("status"),
            "method_exception": None if fit is None else fit.get("exception_message"),
        }
        return make_mapping_record(
            point_id=f"{condition['name']}::rep{replicate}::{method}",
            research_mode="P0-D",
            coverage_role=role,
            location_state="STOPS_WORKING_HERE",
            claim_object="conditional planted-rank stable oscillatory candidate-set generation",
            controls=controls,
            observables=observables,
            open_channel={
                "all_rank_data_only": _all_rank_data_only(sweep),
                "adjacent_rank_stability_data_only": adjacent_rank_stability(
                    sweep, min_hz=MIN_HZ
                ),
                "singular_values_first_12": [
                    float(x) for x in np.asarray(sweep["singular_values"])[:12]
                ],
            },
            notes="P0-D method exception/failure at planted rank; no P1 inference.",
        )

    score = _score_against_truth(
        true_vals, true_shapes, fit["vals"], fit["shapes"]
    )
    truth_count = int(score["truth_positive_complex_modes"])
    est_count = int(score["estimated_positive_complex_modes"])
    unstable = _finite_or_none(score["estimated_unstable_fraction"])

    # This state is intentionally narrower than an accuracy claim. No error/MAC
    # cutoff is introduced. Accuracy remains a continuous P0-D surface.
    candidate_set_present = (
        truth_count > 0
        and est_count >= truth_count
        and unstable is not None
        and unstable == 0.0
    )
    location_state = "WORKS_HERE" if candidate_set_present else "STOPS_WORKING_HERE"

    observables = {
        "method_status": "OK",
        "truth_positive_complex_modes_P0_only": truth_count,
        "estimated_positive_complex_modes": est_count,
        "estimated_unstable_fraction": unstable,
        "matched_modes_P0_only": int(score["matched_modes"]),
        "matched_fraction_of_truth_P0_only": _finite_or_none(
            score["matched_fraction_of_truth"]
        ),
        "median_relative_pole_error_P0_only": _finite_or_none(
            score["median_relative_pole_error"]
        ),
        "p90_relative_pole_error_P0_only": _finite_or_none(
            score["p90_relative_pole_error"]
        ),
        "frequency_mae_hz_P0_only": _finite_or_none(score["frequency_mae_hz"]),
        "relative_decay_mae_P0_only": _finite_or_none(score["relative_decay_mae"]),
        "matched_carrier_subspace_similarity_P0_only": _finite_or_none(
            score["matched_carrier_subspace_similarity"]
        ),
    }

    return make_mapping_record(
        point_id=f"{condition['name']}::rep{replicate}::{method}",
        research_mode="P0-D",
        coverage_role=role,
        location_state=location_state,
        claim_object="conditional planted-rank stable oscillatory candidate-set generation",
        controls=controls,
        observables=observables,
        scope="NOT_YET_ASSIGNED",
        identifiability={
            "individual_vs_subspace_adjudication": "NOT_FROZEN_IN_P0D1",
            "truth_used_only_after_estimation": True,
        },
        open_channel={
            "all_rank_data_only": _all_rank_data_only(sweep),
            "adjacent_rank_stability_data_only": adjacent_rank_stability(
                sweep, min_hz=MIN_HZ
            ),
            "singular_values_first_12": [
                float(x) for x in np.asarray(sweep["singular_values"])[:12]
            ],
            "model_adequacy": "NOT_EVALUATED_IN_P0D1",
        },
        notes=(
            "WORKS/STOPS applies only to complete stable oscillatory candidate-set "
            "generation at planted rank. Pole/carrier accuracy is recorded continuously "
            "and is not thresholded here."
        ),
    )


def _median(records, field):
    vals = []
    for record in records:
        value = record["observables"].get(field)
        if value is not None and np.isfinite(value):
            vals.append(float(value))
    return float(np.median(vals)) if vals else None


def build_map():
    records = []
    for condition in _condition_specs():
        if condition["name"] not in ROLE_BY_CONDITION:
            raise RuntimeError(f"unclassified P0-D condition: {condition['name']}")
        for replicate in range(REPLICATES):
            Y, planted_order, true_vals, true_shapes = _simulate_condition(
                condition, replicate
            )
            sweeps = {
                "SSI_COV": sweep_ssi_cov(
                    Y, DT, block_rows=BLOCK_ROWS, candidate_orders=CANDIDATE_RANKS
                ),
                "SUBSPACE_DMD": sweep_subspace_dmd(
                    Y, DT, candidate_ranks=CANDIDATE_RANKS
                ),
            }
            for method, sweep in sweeps.items():
                records.append(
                    _conditional_claim_record(
                        condition=condition,
                        replicate=replicate,
                        method=method,
                        sweep=sweep,
                        planted_order=planted_order,
                        true_vals=true_vals,
                        true_shapes=true_shapes,
                    )
                )

    views = split_function_limit(records)
    by_method_role = defaultdict(list)
    for record in records:
        method = record["point_id"].rsplit("::", 1)[1]
        by_method_role[(method, record["coverage_role"])].append(record)

    summaries = []
    for (method, role), group in sorted(by_method_role.items()):
        states = Counter(r["location_state"] for r in group)
        summaries.append(
            {
                "method": method,
                "coverage_role": role,
                "records": len(group),
                "location_states": dict(states),
                "median_relative_pole_error_P0_only": _median(
                    group, "median_relative_pole_error_P0_only"
                ),
                "frequency_mae_hz_median_P0_only": _median(
                    group, "frequency_mae_hz_P0_only"
                ),
                "relative_decay_mae_median_P0_only": _median(
                    group, "relative_decay_mae_P0_only"
                ),
                "carrier_subspace_similarity_median_P0_only": _median(
                    group, "matched_carrier_subspace_similarity_P0_only"
                ),
            }
        )

    return _json_clean(
        {
            "schema": "nsd-phase0d-v0.2-p0d1-function-limit-map-v1",
            "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + v0.7.1A Addendum",
            "status": "P0_D_EXPLORATORY_FUNCTION_LIMIT_MAPPING_NOT_CONFIRMATORY",
            "p1_authorized": False,
            "claim_object": "conditional planted-rank stable oscillatory candidate-set generation",
            "location_state_semantics": {
                "WORKS_HERE": (
                    "At planted rank/order, the method returned at least the planted number "
                    "of positive-frequency complex candidates and no unstable poles. This is "
                    "not an accuracy or model-adequacy pass."
                ),
                "STOPS_WORKING_HERE": (
                    "The narrow candidate-set condition above failed or the method raised an "
                    "exception. This is not a claim that all method information is useless."
                ),
                "NOT_KNOWN_HERE": "Reserved for conditions where this narrow state cannot be resolved.",
            },
            "coverage": {
                "NOMINAL_FUNCTION": "ACTIVE",
                "PERTURBED_FUNCTION": "ACTIVE",
                "BOUNDARY_OR_TRANSITION": "ACTIVE",
                "RARE_NATURAL_LIMIT": "NOT_APPLICABLE_CURRENT_SYNTHETIC_STAGE",
            },
            "historical_overlays_not_rescored": {
                "P0Q1_SSI_COV": "SURVIVES_P0Q1",
                "P0Q1_SUBSPACE_DMD": "FAILS_P0Q1",
            },
            "summary_by_method_and_role": summaries,
            "view_counts": {
                "function_map": len(views["function_map"]),
                "limit_map": len(views["limit_map"]),
                "unknown_map": len(views["unknown_map"]),
            },
            "records": records,
            "nonclaims": [
                "No P1 threshold, comparator identity or adjudication rule is frozen.",
                "No error, MAC, uncertainty or adequacy cutoff is inferred from these surfaces.",
                "Planted rank/order is used only for the conditional-recovery Function/Limit view; all-rank data-only sweeps are preserved separately.",
                "Any favorable region or candidate boundary discovered here remains P0-D until independently qualified.",
                "No EEG, phenotype, biological mechanism, chi value or neural regime boundary is tested.",
            ],
        }
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/p0d_mapping/function_limit_map_v1.json",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    record = build_map()
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print(json.dumps(record["view_counts"], sort_keys=True))
    for row in record["summary_by_method_and_role"]:
        print(json.dumps(row, sort_keys=True))
    print("P0-D FUNCTION/LIMIT MAP COMPLETE. No P1 science executed.")


if __name__ == "__main__":
    main()
