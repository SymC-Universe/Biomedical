from __future__ import annotations

"""Pre-outcome D1-versus-D2 predictive calibration on synthetic trajectories.

D1: shared transition operator + additive treatment input.
D2: treatment-interaction operator T_CTX = T_PBS + DeltaT.

The calibration uses leave-one-transition prediction under the exact 5+5
short-term architecture. It cannot read empirical molecular sources and does
not choose a real-data model threshold.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from src.chi_bio_g2_empirical_preflight import (
    fit_shared_transition,
    fit_treatment_interaction_transition,
)


SEED = 20260913
DEFAULT_REPLICATES = 250
RANKS = (2, 3)
NOISE_LEVELS = (0.0, 0.01, 0.05)
SCENARIOS = (
    "SHARED_OPERATOR",
    "REORGANIZED_STABLE",
    "REORGANIZED_ABOVE_UNIT_CIRCLE",
    "REORGANIZED_NONNORMAL_STABLE",
)


def _operator_pair(d: int, scenario: str) -> tuple[np.ndarray, np.ndarray]:
    if d == 2:
        control = np.array([[0.78, 0.08], [0.0, 0.72]], dtype=float)
        if scenario == "SHARED_OPERATOR":
            treated = control.copy()
        elif scenario == "REORGANIZED_STABLE":
            treated = np.array([[0.90, 0.06], [0.0, 0.82]], dtype=float)
        elif scenario == "REORGANIZED_ABOVE_UNIT_CIRCLE":
            treated = np.array([[1.05, 0.04], [0.0, 0.88]], dtype=float)
        elif scenario == "REORGANIZED_NONNORMAL_STABLE":
            treated = np.array([[0.90, 1.20], [0.0, 0.90]], dtype=float)
        else:
            raise ValueError(scenario)
    elif d == 3:
        control = np.array(
            [[0.78, 0.05, 0.02], [0.0, 0.72, 0.04], [0.0, 0.0, 0.64]], dtype=float
        )
        if scenario == "SHARED_OPERATOR":
            treated = control.copy()
        elif scenario == "REORGANIZED_STABLE":
            treated = np.array(
                [[0.90, 0.05, 0.01], [0.0, 0.82, 0.03], [0.0, 0.0, 0.70]], dtype=float
            )
        elif scenario == "REORGANIZED_ABOVE_UNIT_CIRCLE":
            treated = np.array(
                [[1.05, 0.04, 0.01], [0.0, 0.88, 0.03], [0.0, 0.0, 0.74]], dtype=float
            )
        elif scenario == "REORGANIZED_NONNORMAL_STABLE":
            treated = np.array(
                [[0.90, 1.10, 0.20], [0.0, 0.90, 0.80], [0.0, 0.0, 0.90]], dtype=float
            )
        else:
            raise ValueError(scenario)
    else:
        raise ValueError("rank must be 2 or 3")
    return control, treated


def _simulate(
    transition: np.ndarray,
    initial: np.ndarray,
    *,
    treatment: float,
    additive_input: np.ndarray,
    intercept: np.ndarray,
    steps: int = 5,
) -> np.ndarray:
    states = [np.asarray(initial, dtype=float)]
    for _ in range(steps):
        states.append(transition @ states[-1] + treatment * additive_input + intercept)
    return np.vstack(states)


def _predict_d1(fit, x: np.ndarray, u: float) -> np.ndarray:
    pred = fit.transition @ x
    if fit.input_matrix is not None:
        pred = pred + fit.input_matrix[:, 0] * float(u)
    if fit.intercept is not None:
        pred = pred + fit.intercept
    return pred


def _predict_d2(fit, x: np.ndarray, u: float) -> np.ndarray:
    transition = fit.control_transition + float(u) * fit.treatment_delta_transition
    pred = transition @ x
    if fit.input_matrix is not None:
        pred = pred + fit.input_matrix[:, 0] * float(u)
    if fit.intercept is not None:
        pred = pred + fit.intercept
    return pred


def _loto_errors(x_now: np.ndarray, x_next: np.ndarray, u: np.ndarray) -> dict:
    d1_errors: list[float] = []
    d2_errors: list[float] = []
    d1_conditions: list[float] = []
    d2_conditions: list[float] = []
    d1_ok = True
    d2_ok = True

    for omit in range(x_now.shape[0]):
        keep = np.ones(x_now.shape[0], dtype=bool)
        keep[omit] = False
        d1 = fit_shared_transition(
            x_now[keep], x_next[keep], exogenous_inputs=u[keep], include_intercept=True
        )
        d2 = fit_treatment_interaction_transition(
            x_now[keep], x_next[keep], treatment_indicator=u[keep]
        )
        y = x_next[omit]
        denom = max(float(np.linalg.norm(y)), 1e-12)

        if d1.status != "FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN":
            d1_ok = False
        else:
            pred = _predict_d1(d1, x_now[omit], float(u[omit, 0]))
            d1_errors.append(float(np.linalg.norm(y - pred) / denom))
            d1_conditions.append(float(d1.condition_number))

        if d2.status != "FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN":
            d2_ok = False
        else:
            pred = _predict_d2(d2, x_now[omit], float(u[omit, 0]))
            d2_errors.append(float(np.linalg.norm(y - pred) / denom))
            d2_conditions.append(float(d2.condition_number))

    return {
        "d1_all_identifiable": d1_ok and len(d1_errors) == x_now.shape[0],
        "d2_all_identifiable": d2_ok and len(d2_errors) == x_now.shape[0],
        "d1_mean_relative_error": float(np.mean(d1_errors)) if d1_errors else None,
        "d2_mean_relative_error": float(np.mean(d2_errors)) if d2_errors else None,
        "d1_max_condition": max(d1_conditions) if d1_conditions else None,
        "d2_max_condition": max(d2_conditions) if d2_conditions else None,
    }


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
                        t_control, initial, treatment=0.0, additive_input=b, intercept=c
                    )
                    treated = _simulate(
                        t_treated, initial, treatment=1.0, additive_input=b, intercept=c
                    )
                    if noise_sd:
                        control = control + rng.normal(0.0, noise_sd, size=control.shape)
                        treated = treated + rng.normal(0.0, noise_sd, size=treated.shape)

                    x0 = np.vstack([control[:-1], treated[:-1]])
                    x1 = np.vstack([control[1:], treated[1:]])
                    u = np.vstack([np.zeros((5, 1)), np.ones((5, 1))])
                    r = _loto_errors(x0, x1, u)
                    d1_all_id += int(r["d1_all_identifiable"])
                    d2_all_id += int(r["d2_all_identifiable"])
                    if r["d1_mean_relative_error"] is not None:
                        d1_errors.append(float(r["d1_mean_relative_error"]))
                    if r["d2_mean_relative_error"] is not None:
                        d2_errors.append(float(r["d2_mean_relative_error"]))
                    if r["d1_max_condition"] is not None:
                        d1_conditions.append(float(r["d1_max_condition"]))
                    if r["d2_max_condition"] is not None:
                        d2_conditions.append(float(r["d2_max_condition"]))
                    if r["d1_all_identifiable"] and r["d2_all_identifiable"]:
                        comparable += 1
                        d2_lower_error += int(
                            float(r["d2_mean_relative_error"]) < float(r["d1_mean_relative_error"])
                        )

                records.append(
                    {
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
        "status": "SYNTHETIC_PRE_OUTCOME_MODEL_COMPARISON_ONLY",
        "seed": seed,
        "replicates_per_cell": replicates,
        "ranks": list(RANKS),
        "noise_levels": list(NOISE_LEVELS),
        "scenarios": list(SCENARIOS),
        "architecture": "5 PBS + 5 CTX transitions with shared synthetic pretreatment initial state",
        "d1_model": "SHARED_T_PLUS_TREATMENT_INPUT_PLUS_INTERCEPT",
        "d2_model": "TREATMENT_INTERACTION_T_PLUS_DELTA_T_PLUS_INPUT_PLUS_INTERCEPT",
        "records": records,
        "real_source_files_opened": False,
        "empirical_model_selected": False,
        "empirical_threshold_selected": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
        "warning": "Synthetic noise coordinates are not SCC25 measurement-noise estimates. Predictive calibration may guide a prospective model-escalation rule but cannot select a model from real outcomes.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument(
        "--output",
        default="development_outputs/chi_bio_g2/GRI_CHI_BIO_G2_D1_D2_MODEL_COMPARISON_CALIBRATION.json",
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
