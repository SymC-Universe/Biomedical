from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.model_adequacy import (
    covariance_reconstruction_error,
    fit_covariance_markov_parameter,
    fit_linear_predictor,
    normalized_prediction_error,
    one_step_residuals,
    surrogate_whiteness_record,
)
from src.ssi_cov import fit_state_space, output_covariances
from src.synthetic_systems import (
    add_measurement_noise,
    generate_1f,
    make_linear_system,
    make_noise_bases,
    simulate_linear,
    simulate_observation_switch,
    simulate_shared_basis_switch,
)


DT = 0.02
N_SAMPLES = 4800
HALF = N_SAMPLES // 2
N_CHANNELS = 6
BLOCK_ROWS = 18
PROCESS_SCALE = 0.35
ORDERS = [2, 4, 6]
REPLICATES = 8
MAX_LAG = 24
FIT_LAGS = list(range(1, 13))
TRAIN_HELDOUT_LAGS = list(range(13, 25))
TEST_LAGS = list(range(1, 25))
RESIDUAL_LAGS = 12
SURROGATES = 99
SEED_BASE = 202609112100


BASE_MODES = [
    {"type": "complex", "decay": 0.6, "frequency_hz": 3.0},
    {"type": "complex", "decay": 1.0, "frequency_hz": 8.0},
]


def _conditions():
    return [
        {
            "name": "stationary_linear",
            "coverage_role": "NOMINAL_FUNCTION",
            "kind": "linear",
            "system": {"modes": BASE_MODES, "similarity": "orthogonal"},
            "noise": None,
        },
        {
            "name": "stationary_white_sensor_10pct",
            "coverage_role": "PERTURBED_FUNCTION",
            "kind": "linear",
            "system": {"modes": BASE_MODES, "similarity": "orthogonal"},
            "noise": {"type": "white", "fraction_channel_sd": 0.10},
        },
        {
            "name": "stationary_colored_sensor_10pct_rho0p8",
            "coverage_role": "PERTURBED_FUNCTION",
            "kind": "linear",
            "system": {"modes": BASE_MODES, "similarity": "orthogonal"},
            "noise": {"type": "colored", "fraction_channel_sd": 0.10, "rho": 0.8},
        },
        {
            "name": "structural_frequency_switch",
            "coverage_role": "BOUNDARY_OR_TRANSITION",
            "kind": "structural_switch",
            "system": {
                "modes_first": BASE_MODES,
                "modes_second": [
                    {"type": "complex", "decay": 0.6, "frequency_hz": 3.6},
                    {"type": "complex", "decay": 1.0, "frequency_hz": 9.2},
                ],
                "similarity": "orthogonal",
                "switch_sample": HALF,
            },
            "noise": None,
        },
        {
            "name": "observation_map_switch_0p6",
            "coverage_role": "BOUNDARY_OR_TRANSITION",
            "kind": "observation_switch",
            "system": {
                "modes": BASE_MODES,
                "similarity": "orthogonal",
                "output_rotation_strength": 0.6,
                "switch_sample": HALF,
            },
            "noise": None,
        },
        {
            "name": "one_over_f_beta1p5",
            "coverage_role": "BOUNDARY_OR_TRANSITION",
            "kind": "one_over_f",
            "beta": 1.5,
            "noise": None,
        },
    ]


def _center(X):
    X = np.asarray(X, float)
    return X - X.mean(axis=0, keepdims=True)


def _simulate(condition, replicate):
    seed = SEED_BASE + 10000 * int(replicate) + 100 * _conditions().index(condition)
    sys_rng = np.random.default_rng(seed)
    proc_rng = np.random.default_rng(seed + 1)
    noise_rng = np.random.default_rng(seed + 2)

    if condition["kind"] == "linear":
        A, C = make_linear_system(condition["system"], N_CHANNELS, sys_rng)
        Y = simulate_linear(A, C, DT, N_SAMPLES, PROCESS_SCALE, proc_rng)
    elif condition["kind"] == "structural_switch":
        Y = simulate_shared_basis_switch(
            condition["system"], N_CHANNELS, DT, N_SAMPLES,
            PROCESS_SCALE, sys_rng, proc_rng,
        )
    elif condition["kind"] == "observation_switch":
        Y = simulate_observation_switch(
            condition["system"], N_CHANNELS, DT, N_SAMPLES,
            PROCESS_SCALE, sys_rng, proc_rng,
        )
    elif condition["kind"] == "one_over_f":
        Y = generate_1f(N_SAMPLES, N_CHANNELS, float(condition["beta"]), proc_rng)
    else:
        raise ValueError(f"unknown condition kind: {condition['kind']}")

    noise = condition.get("noise")
    if noise is not None:
        rho = float(noise.get("rho", 0.0))
        white, colored = make_noise_bases(N_SAMPLES, N_CHANNELS, rho, noise_rng)
        Y = add_measurement_noise(Y, noise, white, colored)
    return _center(Y[:HALF]), _center(Y[HALF:])


def _finite(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return value if np.isfinite(value) else None


def _ssi_record(train, test, order):
    try:
        F, C, O, S = fit_state_space(train, BLOCK_ROWS, order)
        train_covs = output_covariances(train, MAX_LAG)
        test_covs = output_covariances(test, MAX_LAG)
        G = fit_covariance_markov_parameter(F, C, train_covs, FIT_LAGS)
        fit_error, _ = covariance_reconstruction_error(F, C, G, train_covs, FIT_LAGS)
        train_holdout_error, _ = covariance_reconstruction_error(
            F, C, G, train_covs, TRAIN_HELDOUT_LAGS
        )
        test_error, _ = covariance_reconstruction_error(F, C, G, test_covs, TEST_LAGS)
        return {
            "status": "OK",
            "spectral_radius_discrete": _finite(np.max(np.abs(np.linalg.eigvals(F)))),
            "fit_lag_covariance_error": _finite(fit_error),
            "train_heldout_lag_covariance_error": _finite(train_holdout_error),
            "test_lag_covariance_error": _finite(test_error),
            "singular_values_first_12": [float(x) for x in np.asarray(S)[:12]],
        }
    except Exception as exc:
        return {
            "status": "EXCEPTION",
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }


def _generic_output_record(train, test, replicate, condition_index):
    A = fit_linear_predictor(train)
    resid = one_step_residuals(train, A)
    whiteness = surrogate_whiteness_record(
        resid,
        RESIDUAL_LAGS,
        SURROGATES,
        np.random.default_rng(SEED_BASE + 900000 + 1000 * condition_index + replicate),
    )
    return {
        "status": "OK",
        "model": "GENERIC_OUTPUT_AR1_DIAGNOSTIC_NOT_SSI_INNOVATION",
        "spectral_radius_discrete": _finite(np.max(np.abs(np.linalg.eigvals(A)))),
        "test_normalized_prediction_error": _finite(normalized_prediction_error(test, A)),
        "residual_autocorrelation_energy": _finite(whiteness["observed_energy"]),
        "surrogate_median_energy": _finite(whiteness["surrogate_median_energy"]),
        "surrogate_q95_energy_DESCRIPTIVE_ONLY": _finite(whiteness["surrogate_q95_energy"]),
        "surrogate_upper_tail_p_DESCRIPTIVE_ONLY": _finite(whiteness["monte_carlo_upper_tail_p"]),
        "surrogates": SURROGATES,
    }


def _median(group, field):
    vals = []
    for row in group:
        value = row.get(field)
        if value is not None:
            try:
                value = float(value)
            except (TypeError, ValueError):
                continue
            if np.isfinite(value):
                vals.append(value)
    return float(np.median(vals)) if vals else None


def build_surface():
    records = []
    generic_records = []
    conditions = _conditions()

    for ci, condition in enumerate(conditions):
        for replicate in range(REPLICATES):
            train, test = _simulate(condition, replicate)
            generic = _generic_output_record(train, test, replicate, ci)
            generic_record = {
                "research_mode": "P0-D",
                "condition": condition["name"],
                "coverage_role": condition["coverage_role"],
                "replicate": int(replicate),
                **generic,
            }
            generic_records.append(generic_record)

            for order in ORDERS:
                records.append(
                    {
                        "research_mode": "P0-D",
                        "condition": condition["name"],
                        "coverage_role": condition["coverage_role"],
                        "replicate": int(replicate),
                        "ssi_order": int(order),
                        **_ssi_record(train, test, order),
                    }
                )

    ssi_summary = []
    grouped = defaultdict(list)
    for row in records:
        grouped[(row["condition"], row["ssi_order"])].append(row)
    for (condition, order), group in grouped.items():
        ssi_summary.append(
            {
                "condition": condition,
                "coverage_role": group[0]["coverage_role"],
                "ssi_order": int(order),
                "records": len(group),
                "exceptions": int(sum(r["status"] != "OK" for r in group)),
                "spectral_radius_median": _median(group, "spectral_radius_discrete"),
                "fit_lag_covariance_error_median": _median(group, "fit_lag_covariance_error"),
                "train_heldout_lag_covariance_error_median": _median(group, "train_heldout_lag_covariance_error"),
                "test_lag_covariance_error_median": _median(group, "test_lag_covariance_error"),
            }
        )

    generic_summary = []
    by_condition = defaultdict(list)
    for row in generic_records:
        by_condition[row["condition"]].append(row)
    for condition, group in by_condition.items():
        generic_summary.append(
            {
                "condition": condition,
                "coverage_role": group[0]["coverage_role"],
                "records": len(group),
                "spectral_radius_median": _median(group, "spectral_radius_discrete"),
                "test_normalized_prediction_error_median": _median(group, "test_normalized_prediction_error"),
                "residual_autocorrelation_energy_median": _median(group, "residual_autocorrelation_energy"),
                "surrogate_median_energy_median": _median(group, "surrogate_median_energy"),
                "surrogate_q95_energy_median_DESCRIPTIVE_ONLY": _median(group, "surrogate_q95_energy_DESCRIPTIVE_ONLY"),
                "surrogate_upper_tail_p_median_DESCRIPTIVE_ONLY": _median(group, "surrogate_upper_tail_p_DESCRIPTIVE_ONLY"),
            }
        )

    return {
        "schema": "nsd-phase0d-v0.2-p0d4-model-adequacy-surface-v1",
        "status": "P0_D_MODEL_ADEQUACY_MAPPING_NOT_ADJUDICATED",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "scientific_question": (
            "How do two distinct adequacy diagnostics behave across stationary, perturbed, "
            "transition and non-finite-order-like synthetic observations before any adequacy threshold is selected?"
        ),
        "diagnostic_firewall": {
            "ssi_covariance_path": (
                "SSI-COV F,C are fit on the first half. A positive-lag covariance Markov parameter G is fit "
                "on train lags 1-12, then covariance reconstruction is evaluated on held-out train lags 13-24 "
                "and on the second-half covariance sequence. No Q/R or Kalman innovation covariance is claimed."
            ),
            "generic_output_path": (
                "A channel-space AR(1) predictor is fit on the first half. Its residual temporal structure and "
                "second-half one-step prediction error are independent descriptive output diagnostics and are "
                "explicitly NOT SSI-COV innovations."
            ),
        },
        "design": {
            "dt": DT,
            "n_samples": N_SAMPLES,
            "train_samples": HALF,
            "test_samples": HALF,
            "n_channels": N_CHANNELS,
            "ssi_block_rows": BLOCK_ROWS,
            "ssi_orders": ORDERS,
            "ssi_G_fit_lags": FIT_LAGS,
            "ssi_train_heldout_lags": TRAIN_HELDOUT_LAGS,
            "ssi_test_lags": TEST_LAGS,
            "residual_lags": RESIDUAL_LAGS,
            "surrogates_per_generic_record": SURROGATES,
            "replicates_per_condition": REPLICATES,
            "conditions": conditions,
        },
        "ssi_covariance_summary": ssi_summary,
        "generic_output_summary": generic_summary,
        "ssi_covariance_records": records,
        "generic_output_records": generic_records,
        "nonclaims": [
            "No model-adequacy threshold, rejection level, preferred SSI order or diagnostic weighting is selected from this surface.",
            "The surrogate q95 and Monte-Carlo p values are descriptive; no alpha level is frozen.",
            "Generic AR(1) residuals are not SSI-COV innovations.",
            "SSI positive-lag covariance reconstruction does not identify process-noise or measurement-noise covariance and is not a Kalman innovation test.",
            "A low covariance-reconstruction error does not prove that the fitted generator is the literal neural mechanism.",
            "Any favorable discriminator discovered here is P0-D/post-result and requires independent P0-Q qualification before use as a gate.",
            "No EEG, phenotype, chi coordinate, neural regime boundary or P1 claim is tested."
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/p0d_mapping/model_adequacy_surface_v1.json")
    args = parser.parse_args()
    record = build_surface()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("SSI covariance summaries:")
    for row in record["ssi_covariance_summary"]:
        print(json.dumps(row, sort_keys=True))
    print("Generic output summaries:")
    for row in record["generic_output_summary"]:
        print(json.dumps(row, sort_keys=True))
    print("P0-D MODEL-ADEQUACY SURFACE COMPLETE. No adequacy gate or P1 science was frozen.")


if __name__ == "__main__":
    main()
