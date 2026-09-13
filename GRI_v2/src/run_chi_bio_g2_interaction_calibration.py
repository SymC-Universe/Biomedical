from __future__ import annotations

"""Synthetic calibration for the prospective G2 treatment-interaction model.

This runner uses only known-truth synthetic systems. It is deliberately unable
to read SCC25/TCGA files and does not choose empirical thresholds. Its purpose
is to quantify how the tiny 5+5 transition architecture behaves for r=2 and
r=3 under controlled measurement-noise levels before a real-data freeze.
"""

import argparse
import json
from pathlib import Path

import numpy as np

from src.chi_bio_g2_empirical_preflight import (
    fit_treatment_interaction_transition,
    transition_diagnostics,
)


SEED = 20260913
DEFAULT_REPLICATES = 500
NOISE_LEVELS = (0.0, 0.01, 0.05, 0.10)
RANKS = (2, 3)


def _operators(d: int, scenario: str) -> tuple[np.ndarray, np.ndarray]:
    if d == 2:
        control = np.array([[0.78, 0.08], [0.0, 0.72]], dtype=float)
        if scenario == "STABLE_TREATED":
            treated = np.array([[0.90, 0.06], [0.0, 0.82]], dtype=float)
        elif scenario == "NEAR_BOUNDARY_TREATED":
            treated = np.array([[0.98, 0.05], [0.0, 0.86]], dtype=float)
        elif scenario == "ABOVE_BOUNDARY_TREATED":
            treated = np.array([[1.05, 0.04], [0.0, 0.88]], dtype=float)
        elif scenario == "NONNORMAL_STABLE_TREATED":
            treated = np.array([[0.90, 1.20], [0.0, 0.90]], dtype=float)
        else:
            raise ValueError(scenario)
    elif d == 3:
        control = np.array(
            [[0.78, 0.05, 0.02], [0.0, 0.72, 0.04], [0.0, 0.0, 0.64]], dtype=float
        )
        if scenario == "STABLE_TREATED":
            treated = np.array(
                [[0.90, 0.05, 0.01], [0.0, 0.82, 0.03], [0.0, 0.0, 0.70]], dtype=float
            )
        elif scenario == "NEAR_BOUNDARY_TREATED":
            treated = np.array(
                [[0.98, 0.04, 0.01], [0.0, 0.86, 0.03], [0.0, 0.0, 0.72]], dtype=float
            )
        elif scenario == "ABOVE_BOUNDARY_TREATED":
            treated = np.array(
                [[1.05, 0.04, 0.01], [0.0, 0.88, 0.03], [0.0, 0.0, 0.74]], dtype=float
            )
        elif scenario == "NONNORMAL_STABLE_TREATED":
            treated = np.array(
                [[0.90, 1.10, 0.20], [0.0, 0.90, 0.80], [0.0, 0.0, 0.90]], dtype=float
            )
        else:
            raise ValueError(scenario)
    else:
        raise ValueError("calibration only supports r=2 or r=3")
    return control, treated


def _simulate_arm(
    transition: np.ndarray,
    x0: np.ndarray,
    *,
    treatment: float,
    steps: int,
    additive_input: np.ndarray,
    intercept: np.ndarray,
) -> np.ndarray:
    states = [np.asarray(x0, dtype=float)]
    for _ in range(steps):
        nxt = transition @ states[-1] + treatment * additive_input + intercept
        states.append(nxt)
    return np.vstack(states)


def _quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    return float(np.quantile(np.asarray(values, dtype=float), q))


def _summarize(values: list[float]) -> dict[str, float | None]:
    return {
        "median": _quantile(values, 0.50),
        "p90": _quantile(values, 0.90),
        "p95": _quantile(values, 0.95),
        "max": float(np.max(values)) if values else None,
    }


def run_calibration(*, replicates: int = DEFAULT_REPLICATES, seed: int = SEED) -> dict:
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    rng = np.random.default_rng(seed)
    scenarios = (
        "STABLE_TREATED",
        "NEAR_BOUNDARY_TREATED",
        "ABOVE_BOUNDARY_TREATED",
        "NONNORMAL_STABLE_TREATED",
    )
    records: list[dict] = []

    for d in RANKS:
        for scenario in scenarios:
            t0, tt = _operators(d, scenario)
            dt = tt - t0
            truth_control = transition_diagnostics(t0)
            truth_treated = transition_diagnostics(tt)
            for noise_sd in NOISE_LEVELS:
                conds: list[float] = []
                control_rho_errors: list[float] = []
                treated_rho_errors: list[float] = []
                delta_frob_errors: list[float] = []
                full_rank = 0
                treated_side_correct = 0
                nonnormal_warning_correct = 0

                for _ in range(replicates):
                    x_init = rng.normal(loc=0.0, scale=1.0, size=d)
                    # Avoid a degenerate nearly-zero starting state without conditioning on outcomes.
                    if float(np.linalg.norm(x_init)) < 0.25:
                        x_init = x_init + np.linspace(0.5, 1.0, d)
                    b = np.linspace(0.03, -0.02, d)
                    c = np.linspace(0.02, -0.01, d)
                    control = _simulate_arm(
                        t0, x_init, treatment=0.0, steps=5, additive_input=b, intercept=c
                    )
                    treated = _simulate_arm(
                        tt, x_init, treatment=1.0, steps=5, additive_input=b, intercept=c
                    )
                    if noise_sd:
                        control = control + rng.normal(0.0, noise_sd, size=control.shape)
                        treated = treated + rng.normal(0.0, noise_sd, size=treated.shape)

                    x_now = np.vstack([control[:-1], treated[:-1]])
                    x_next = np.vstack([control[1:], treated[1:]])
                    u = np.vstack([np.zeros((5, 1)), np.ones((5, 1))])
                    fit = fit_treatment_interaction_transition(
                        x_now, x_next, treatment_indicator=u
                    )
                    if fit.status != "FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN":
                        continue
                    full_rank += 1
                    conds.append(float(fit.condition_number))
                    cdiag = transition_diagnostics(fit.control_transition)
                    tdiag = transition_diagnostics(fit.treated_transition)
                    control_rho_errors.append(abs(cdiag.spectral_radius - truth_control.spectral_radius))
                    treated_rho_errors.append(abs(tdiag.spectral_radius - truth_treated.spectral_radius))
                    denom = max(float(np.linalg.norm(dt, ord="fro")), 1e-12)
                    delta_frob_errors.append(
                        float(np.linalg.norm(fit.treatment_delta_transition - dt, ord="fro") / denom)
                    )
                    true_side = np.sign(truth_treated.spectral_radius - 1.0)
                    fit_side = np.sign(tdiag.spectral_radius - 1.0)
                    treated_side_correct += int(true_side == fit_side)
                    nonnormal_warning_correct += int(
                        tdiag.nonnormal_transient_warning == truth_treated.nonnormal_transient_warning
                    )

                denom = max(full_rank, 1)
                records.append(
                    {
                        "rank": d,
                        "scenario": scenario,
                        "noise_sd": noise_sd,
                        "replicates": replicates,
                        "full_rank_fit_fraction": full_rank / replicates,
                        "truth_control_rho": truth_control.spectral_radius,
                        "truth_treated_rho": truth_treated.spectral_radius,
                        "truth_treated_sigma_max": truth_treated.largest_singular_value,
                        "truth_nonnormal_warning": truth_treated.nonnormal_transient_warning,
                        "condition_number": _summarize(conds),
                        "control_rho_abs_error": _summarize(control_rho_errors),
                        "treated_rho_abs_error": _summarize(treated_rho_errors),
                        "delta_transition_relative_frobenius_error": _summarize(delta_frob_errors),
                        "treated_unit_circle_side_accuracy_given_full_rank": treated_side_correct / denom,
                        "nonnormal_warning_accuracy_given_full_rank": nonnormal_warning_correct / denom,
                    }
                )

    return {
        "status": "SYNTHETIC_PRE_OUTCOME_CALIBRATION_ONLY",
        "seed": seed,
        "replicates_per_cell": replicates,
        "ranks": list(RANKS),
        "noise_levels": list(NOISE_LEVELS),
        "short_term_transition_architecture": "5 PBS + 5 CTX transitions; shared pretreatment initialization in synthetic fixture",
        "model": "TREATMENT_INTERACTION_T_PLUS_DELTA_T_PLUS_INPUT_PLUS_INTERCEPT",
        "records": records,
        "real_source_files_opened": False,
        "empirical_thresholds_selected": False,
        "empirical_rank_winner_selected": False,
        "chi_bio_computed": False,
        "promotion_effect": "NONE",
        "warning": "Noise levels are synthetic stress coordinates, not estimates of SCC25 measurement error and not empirical refusal thresholds.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=DEFAULT_REPLICATES)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument(
        "--output",
        default="development_outputs/chi_bio_g2/GRI_CHI_BIO_G2_INTERACTION_SYNTHETIC_CALIBRATION.json",
    )
    args = parser.parse_args()
    result = run_calibration(replicates=args.replicates, seed=args.seed)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
