from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.optimize import linear_sum_assignment

from src.dmd import fit_dmd, fit_tls_dmd
from src.ssi_cov import decompose, fit_from_decomposition, fit_state_space
from src.selector import subspace_similarity
from src.synthetic_systems import (
    add_measurement_noise,
    make_linear_system,
    make_noise_bases,
    simulate_linear,
    simulate_shared_basis_switch,
    truth_modes,
)
from src.model_adequacy import covariance_adequacy_record


DT = 0.02
N_SAMPLES = 2400
N_CHANNELS = 6
BLOCK_ROWS = 18
PROCESS_SCALE = 0.35
REPLICATES = 6
MIN_HZ = 0.25


def _positive(vals):
    vals = np.asarray(vals, complex)
    return np.where(vals.imag / (2 * np.pi) >= MIN_HZ)[0]


def _score_against_truth(true_vals, true_shapes, est_vals, est_shapes):
    tv = np.asarray(true_vals, complex)
    ev = np.asarray(est_vals, complex)
    ts = np.asarray(true_shapes, complex)
    es = np.asarray(est_shapes, complex)
    ti = _positive(tv)
    ei = _positive(ev)

    out = {
        "truth_positive_complex_modes": int(len(ti)),
        "estimated_positive_complex_modes": int(len(ei)),
        "matched_modes": 0,
        "matched_fraction_of_truth": 0.0 if len(ti) else None,
        "median_relative_pole_error": None,
        "p90_relative_pole_error": None,
        "frequency_mae_hz": None,
        "relative_decay_mae": None,
        "matched_carrier_subspace_similarity": None,
        "estimated_unstable_fraction": float(np.mean(ev.real >= 0.0)) if len(ev) else None,
    }
    if len(ti) == 0 or len(ei) == 0:
        return out

    cost = np.empty((len(ti), len(ei)), float)
    for r, i in enumerate(ti):
        for c, j in enumerate(ei):
            cost[r, c] = float(abs(tv[i] - ev[j]) / max(abs(tv[i]), abs(ev[j]), 1e-12))
    rr, cc = linear_sum_assignment(cost)
    if len(rr) == 0:
        return out

    tsel = np.asarray([ti[r] for r in rr], int)
    esel = np.asarray([ei[c] for c in cc], int)
    errors = np.asarray([cost[r, c] for r, c in zip(rr, cc)], float)
    freq_err = np.abs(tv[tsel].imag - ev[esel].imag) / (2 * np.pi)
    true_decay = np.maximum(-tv[tsel].real, 1e-12)
    decay_err = np.abs((-ev[esel].real) - true_decay) / true_decay

    out.update({
        "matched_modes": int(len(rr)),
        "matched_fraction_of_truth": float(len(rr) / len(ti)),
        "median_relative_pole_error": float(np.median(errors)),
        "p90_relative_pole_error": float(np.quantile(errors, 0.90)),
        "frequency_mae_hz": float(np.mean(freq_err)),
        "relative_decay_mae": float(np.mean(decay_err)),
        "matched_carrier_subspace_similarity": float(
            subspace_similarity(ts[:, tsel], es[:, esel])
        ),
    })
    return out


def _method_record(method, Y, order, true_vals, true_shapes):
    try:
        if method == "SSI_COV_ORACLE_ORDER":
            U, S, p = decompose(Y, BLOCK_ROWS)
            vals, shapes = fit_from_decomposition(U, S, p, order, DT)
        elif method == "DMD_EXACT_ORACLE_RANK":
            vals, shapes = fit_dmd(Y, DT, order)
        elif method == "DMD_TLS_ORACLE_RANK":
            vals, shapes = fit_tls_dmd(Y, DT, order)
        else:
            raise ValueError("unknown method")
        out = _score_against_truth(true_vals, true_shapes, vals, shapes)
        out["status"] = "OK"
        return out
    except Exception as exc:
        return {
            "status": "METHOD_EXCEPTION_PRESERVED",
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }


def _condition_specs():
    base_modes = [
        {"type": "complex", "decay": 0.6, "frequency_hz": 3.0},
        {"type": "complex", "decay": 1.0, "frequency_hz": 8.0},
    ]
    return [
        {
            "name": "baseline_stochastic",
            "system": {"modes": base_modes, "similarity": "orthogonal"},
            "noise": None,
        },
        {
            "name": "white_sensor_10pct",
            "system": {"modes": base_modes, "similarity": "orthogonal"},
            "noise": {"type": "white", "fraction_channel_sd": 0.10},
        },
        {
            "name": "colored_sensor_10pct_rho0p8",
            "system": {"modes": base_modes, "similarity": "orthogonal"},
            "noise": {"type": "colored", "fraction_channel_sd": 0.10, "rho": 0.8},
        },
        {
            "name": "weak_second_mode_5pct_plus_white5pct",
            "system": {
                "modes": base_modes,
                "similarity": "orthogonal",
                "weak_block": 1,
                "weak_scale": 0.05,
            },
            "noise": {"type": "white", "fraction_channel_sd": 0.05},
        },
        {
            "name": "crowded_modes_plus_white5pct",
            "system": {
                "modes": [
                    {"type": "complex", "decay": 0.7, "frequency_hz": 6.0},
                    {"type": "complex", "decay": 0.7, "frequency_hz": 6.15},
                ],
                "similarity": "orthogonal",
            },
            "noise": {"type": "white", "fraction_channel_sd": 0.05},
        },
        {
            "name": "condition_number_25_plus_white5pct",
            "system": {
                "modes": base_modes,
                "similarity": "cond",
                "condition_number": 25.0,
            },
            "noise": {"type": "white", "fraction_channel_sd": 0.05},
        },
    ]


def _simulate_condition(condition, replicate):
    seed_base = 100000 + 1000 * replicate + sum(ord(c) for c in condition["name"])
    sys_rng = np.random.default_rng(seed_base)
    proc_rng = np.random.default_rng(seed_base + 1)
    noise_rng = np.random.default_rng(seed_base + 2)
    A, C = make_linear_system(condition["system"], N_CHANNELS, sys_rng)
    clean = simulate_linear(A, C, DT, N_SAMPLES, PROCESS_SCALE, proc_rng)
    Y = clean
    noise = condition["noise"]
    if noise is not None:
        rho = float(noise.get("rho", 0.0))
        white, colored = make_noise_bases(N_SAMPLES, N_CHANNELS, rho, noise_rng)
        Y = add_measurement_noise(clean, noise, white, colored)
    true_vals, true_shapes = truth_modes(A, C)
    return Y, A.shape[0], true_vals, true_shapes


def _finite(values):
    return np.asarray([v for v in values if v is not None and np.isfinite(v)], float)


def _aggregate_method(records):
    ok = [r for r in records if r.get("status") == "OK"]
    fields = [
        "matched_fraction_of_truth",
        "median_relative_pole_error",
        "p90_relative_pole_error",
        "frequency_mae_hz",
        "relative_decay_mae",
        "matched_carrier_subspace_similarity",
        "estimated_unstable_fraction",
        "estimated_positive_complex_modes",
    ]
    out = {
        "records": int(len(records)),
        "ok_records": int(len(ok)),
        "method_exceptions": int(len(records) - len(ok)),
    }
    for field in fields:
        vals = _finite([r.get(field) for r in ok])
        if len(vals):
            out[field + "_median"] = float(np.median(vals))
            out[field + "_p90"] = float(np.quantile(vals, 0.90))
        else:
            out[field + "_median"] = None
            out[field + "_p90"] = None
    return out


def comparator_stress_matrix():
    methods = [
        "SSI_COV_ORACLE_ORDER",
        "DMD_EXACT_ORACLE_RANK",
        "DMD_TLS_ORACLE_RANK",
    ]
    conditions_out = []
    for condition in _condition_specs():
        by_method = {m: [] for m in methods}
        for replicate in range(REPLICATES):
            Y, order, true_vals, true_shapes = _simulate_condition(condition, replicate)
            for method in methods:
                by_method[method].append(
                    _method_record(method, Y, order, true_vals, true_shapes)
                )
        conditions_out.append({
            "condition": condition["name"],
            "replicates": REPLICATES,
            "oracle_state_order_or_rank": int(order),
            "method_summaries": {
                method: _aggregate_method(records)
                for method, records in by_method.items()
            },
            "records": by_method,
        })
    return conditions_out


def model_adequacy_stress():
    base_modes = [
        {"type": "complex", "decay": 0.6, "frequency_hz": 3.0},
        {"type": "complex", "decay": 1.0, "frequency_hz": 8.0},
    ]
    switched_modes = [
        {"type": "complex", "decay": 0.6, "frequency_hz": 5.0},
        {"type": "complex", "decay": 1.0, "frequency_hz": 11.0},
    ]
    cases = {"stationary": [], "within_record_switch": []}
    for replicate in range(REPLICATES):
        seed = 700000 + replicate * 1000
        sys_rng = np.random.default_rng(seed)
        proc_rng = np.random.default_rng(seed + 1)
        A, C = make_linear_system(
            {"modes": base_modes, "similarity": "orthogonal"},
            N_CHANNELS,
            sys_rng,
        )
        stationary = simulate_linear(A, C, DT, N_SAMPLES, PROCESS_SCALE, proc_rng)
        Fhat, Chat, _, _ = fit_state_space(stationary, BLOCK_ROWS, A.shape[0])
        cases["stationary"].append(
            covariance_adequacy_record(
                stationary, Fhat, Chat, range(1, 9), range(9, 25)
            )
        )

        switch_spec = {
            "modes_first": base_modes,
            "modes_second": switched_modes,
            "similarity": "orthogonal",
            "switch_sample": N_SAMPLES // 2,
        }
        switched = simulate_shared_basis_switch(
            switch_spec,
            N_CHANNELS,
            DT,
            N_SAMPLES,
            PROCESS_SCALE,
            np.random.default_rng(seed + 10),
            np.random.default_rng(seed + 11),
        )
        Fhat, Chat, _, _ = fit_state_space(switched, BLOCK_ROWS, 4)
        cases["within_record_switch"].append(
            covariance_adequacy_record(
                switched, Fhat, Chat, range(1, 9), range(9, 25)
            )
        )

    out = {}
    for name, rows in cases.items():
        evals = np.asarray(
            [r["evaluation_normalized_covariance_error"] for r in rows], float
        )
        fits = np.asarray(
            [r["fit_normalized_covariance_error"] for r in rows], float
        )
        out[name] = {
            "replicates": int(len(rows)),
            "fit_error_median": float(np.median(fits)),
            "fit_error_p90": float(np.quantile(fits, 0.90)),
            "heldout_lag_error_median": float(np.median(evals)),
            "heldout_lag_error_p90": float(np.quantile(evals, 0.90)),
            "records": rows,
        }
    return out


def build_record():
    return {
        "schema": "nsd-phase0d-v0.2-p0-comparator-stress-matrix-v1",
        "status": "P0_DEVELOPMENT_MATRIX_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL",
        "p1_authorized": False,
        "design": {
            "dt": DT,
            "n_samples": N_SAMPLES,
            "n_channels": N_CHANNELS,
            "ssi_block_rows": BLOCK_ROWS,
            "process_scale": PROCESS_SCALE,
            "replicates_per_condition": REPLICATES,
            "rank_order_policy": (
                "P0 oracle state order/rank supplied identically where possible; "
                "this isolates estimator behavior and is not the future P1 rank-selection rule."
            ),
            "comparator_policy": (
                "Exact DMD is retained as a diagnostic baseline. TLS-DMD is included "
                "because published work identifies standard DMD sensor-noise bias. "
                "No comparator winner is selected by this matrix."
            ),
        },
        "comparator_stress": comparator_stress_matrix(),
        "model_adequacy_stress": model_adequacy_stress(),
        "nonclaims": [
            "No method is declared superior or selected as the P1 comparator.",
            "No P1 rank/order-selection rule is tested; oracle order/rank is a P0 isolation device.",
            "No numerical metric in this matrix is a neural or P1 threshold.",
            "No EEG, phenotype, chi, regime boundary, or mechanism is tested.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/p0_qualification/comparator_stress_matrix.json",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(build_record(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("P0 COMPARATOR / ADEQUACY STRESS MATRIX COMPLETE. No P1 science was executed.")


if __name__ == "__main__":
    main()
