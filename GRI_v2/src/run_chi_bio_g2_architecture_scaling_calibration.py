from __future__ import annotations

"""Compare D1/D2 predictive behavior as transition count scales from 5+5 to 10+10.

Synthetic P0-D only. No empirical molecular source is readable here. This asks
whether the chronic SCC25 transition count can materially reduce the variance
penalty that made D2 fragile in the short-term architecture.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from src.run_chi_bio_g2_model_comparison_calibration import (
    _loto_errors,
    _operator_pair,
    _simulate,
)


SEED = 20260913
DEFAULT_REPLICATES = 250
RANKS = (2, 3)
ARM_STEPS = (5, 10)
NOISE_LEVELS = (0.0, 0.01, 0.05)
SCENARIOS = (
    "SHARED_OPERATOR",
    "REORGANIZED_STABLE",
    "REORGANIZED_ABOVE_UNIT_CIRCLE",
    "REORGANIZED_NONNORMAL_STABLE",
)


def _summary(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"median": None, "p90": None, "p95": None, "max": None}
    a = np.asarray(values, dtype=float)
    return {
        "median": float(np.quantile(a, 0.50)),
        "p90": float(np.quantile(a, 0.90)),
        "p95": float(np.quantile(a, 0.95)),
        "max": float(np.max(a)),
    }


def run_calibration(*, replicates: int = DEFAULT_REPLICATES, seed: int = SEED) -> dict:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rng = np.random.default_rng(seed)
    records: list[dict] = []

    for steps in ARM_STEPS:
        for d in RANKS:
            for scenario in SCENARIOS:
                t_control, t_treated = _operator_pair(d, scenario)
                for noise_sd in NOISE_LEVELS:
                    d1_errors: list[float] = []
                    d2_errors: list[float] = []
                    d1_conditions: list[float] = []
                    d2_conditions: list[float] = []
                    d1_all_id = 0
                    d2_all_id = 0
                    comparable = 0
                    d2_lower_error = 0

                    for _ in range(replicates):
                        initial = rng.normal(size=d)
                        if float(np.linalg.norm(initial)) < 0.25:
                            initial = initial + np.linspace(0.5, 1.0, d)
                        b = np.linspace(0.03, -0.02, d)
                        c = np.linspace(0.02, -0.01, d)
                        control = _simulate(
                            t_control,
                            initial,
                            treatment=0.0,
                            additive_input=b,
                            intercept=c,
                            steps=steps,
                        )
                        treated = _simulate(
                            t_treated,
                            initial,
                            treatment=1.0,
                            additive_input=b,
                            intercept=c,
                            steps=steps,
                        )
                        if noise_sd:
                            control = control + rng.normal(0.0, noise_sd, size=control.shape)
                            treated = treated + rng.normal(0.0, noise_sd, size=treated.shape)

                        x0 = np.vstack([control[:-1], treated[:-1]])
                        x1 = np.vstack([control[1:], treated[1:]])
                        u = np.vstack([
                            np.zeros((steps, 1)),
                            np.ones((steps, 1)),
                        ])
                        result = _loto_errors(x0, x1, u)

                        d1_all_id += int(result["d1_all_identifiable"])
                        d2_all_id += int(result["d2_all_identifiable"])
                        if result["d1_mean_relative_error"] is not None:
                            d1_errors.append(float(result["d1_mean_relative_error"]))
                        if result["d2_mean_relative_error"] is not None:
                            d2_errors.append(float(result["d2_mean_relative_error"]))
                        if result["d1_max_condition"] is not None:
                            d1_conditions.append(float(result["d1_max_condition"]))
                        if result["d2_max_condition"] is not None:
                            d2_conditions.append(float(result["d2_max_condition"]))
                        if result["d1_all_identifiable"] and result["d2_all_identifiable"]:
                            comparable += 1
                            d2_lower_error += int(
                                float(result["d2_mean_relative_error"])
                                < float(result["d1_mean_relative_error"])
                            )

                    records.append(
                        {
                            "arm_steps": steps,
                            "transitions_total": 2 * steps,
                            "rank": d,
                            "scenario": scenario,
                            "noise_sd": noise_sd,
                            "replicates": replicates,
                            "d1_all_loto_identifiable_fraction": d1_all_id / replicates,
                            "d2_all_loto_identifiable_fraction": d2_all_id / replicates,
                            "d1_loto_relative_prediction_error": _summary(d1_errors),
                            "d2_loto_relative_prediction_error": _summary(d2_errors),
                            "d1_loto_max_condition": _summary(d1_conditions),
                            "d2_loto_max_condition": _summary(d2_conditions),
                            "both_models_all_loto_identifiable_fraction": comparable / replicates,
                            "d2_lower_loto_error_fraction_given_both_identifiable": (
                                d2_lower_error / comparable if comparable else None
                            ),
                        }
                    )

    return {
        "status": "SYNTHETIC_PRE_OUTCOME_ARCHITECTURE_SCALING_ONLY",
        "seed": seed,
        "replicates_per_cell": replicates,
        "ranks": list(RANKS),
        "arm_steps": list(ARM_STEPS),
        "noise_levels": list(NOISE_LEVELS),
        "scenarios": list(SCENARIOS),
        "short_term_architecture": "5 PBS + 5 CTX transitions",
        "chronic_architecture": "10 PBS + 10 CTX transitions",
        "real_source_files_opened": False,
        "empirical_model_selected": False,
        "empirical_threshold_selected": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
        "warning": "Synthetic noise coordinates are not empirical SCC25 noise estimates. This calibration compares information geometry only.",
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument(
        "--output",
        default="development_outputs/chi_bio_g2/GRI_CHI_BIO_G2_ARCHITECTURE_SCALING_CALIBRATION.json",
    )
    args = parser.parse_args()
    result = run_calibration(replicates=args.replicates, seed=args.seed)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
