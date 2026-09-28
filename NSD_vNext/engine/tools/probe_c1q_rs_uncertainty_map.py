#!/usr/bin/env python3
"""Repeated-realization C1Q-RS uncertainty map for Bio Chi.

P0-D/P0-Q known-truth qualification only. The tool maps empirical estimator
sampling behavior under correct C-family specification. It does not define an
admission threshold, biological prevalence, semantic model membership, or a
real-EEG local-chi claim.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import platform
import sys
from typing import Any

import numpy as np
import scipy

from nsd_engine.continuous_lineage_candidate_rs import (
    fit_continuous_lineage_candidate_rs,
)
from probe_continuous_lineage_nonzero_g import (
    construct_truth,
    simulate_same_path,
)

CELLS = [
    (0, 0.808004818, 14.655366315, 0.508266046, 0.584395017),
    (1, 0.287373873, 12.656497417, 0.230462532, -0.441439599),
    (2, 0.503600127, 22.101059450, 0.757180555, 0.086737482),
    (3, 0.677586268, 6.585799037, 0.326081456, -0.142218795),
    (4, 0.595341533, 22.291574446, 0.247282106, -0.220373040),
    (5, 0.422104721, 5.021647139, 0.669478590, 0.352440502),
    (6, 0.292389809, 18.952085106, 0.496195269, -0.719590691),
    (7, 0.813598516, 9.736141725, 0.765096168, 0.650094895),
]

SEEDS = [
    989969,
    353795,
    292995,
    180979,
    415219,
    783915,
    881434,
    585460,
    100788,
    562898,
    806242,
    577187,
]
PREFLIGHT_CELLS = {0, 6}
PREFLIGHT_SEEDS = {989969, 100788}
FINE_FS = 256.0
DECIMATION = 2
SECONDS = 60.0
PRIMARY_MAXITER = 80
PRIMARY_MAX_STARTS = 18
RESCUE_MAXITER = 160
RESCUE_MAX_STARTS = 24
RAW_BOUNDARY_TOL = 1e-6


def environment_record() -> dict[str, Any]:
    return {
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_ref": os.environ.get("GITHUB_REF"),
        "rng": "numpy.random.default_rng",
        "repeatability_class": (
            "numerical/decision-equivalent within declared environment; "
            "cross-platform bitwise identity not promised"
        ),
    }


def serialize_fit(fit) -> dict[str, Any]:
    raw = [float(v) for v in fit.raw_parameters]
    edge_distance = float(min(8.0 - abs(v) for v in raw))
    return {
        "success": bool(fit.success),
        "negative_log_likelihood": float(fit.negative_log_likelihood),
        "bic": float(fit.bic),
        "parameters": {k: float(v) for k, v in fit.parameters.items()},
        "raw_parameters": raw,
        "attempted_start_count": int(fit.attempted_start_count),
        "converged_start_count": int(fit.converged_start_count),
        "optimizer_message": str(fit.optimizer_message),
        "winning_start_origin": str(fit.winning_start_origin),
        "recurrence_seed_status": str(fit.recurrence_seed_status),
        "recurrence_seed_ready": bool(fit.recurrence_seed_ready),
        "recurrence_seed_g_projected": bool(fit.recurrence_seed_g_projected),
        "recurrence_seed_A_projected": bool(fit.recurrence_seed_A_projected),
        "raw_box_edge_distance": edge_distance,
        "raw_boundary_flag": bool(edge_distance <= RAW_BOUNDARY_TOL),
        "g_boundary_distance": float(1.0 - abs(fit.parameters["g"])),
    }


def fit_route(signal: np.ndarray, fs: float) -> dict[str, Any]:
    primary = fit_continuous_lineage_candidate_rs(
        signal,
        fs,
        optimizer_maxiter=PRIMARY_MAXITER,
        max_optimized_starts=PRIMARY_MAX_STARTS,
    )
    rescue = None
    if not primary.legacy_best_success:
        rescue = fit_continuous_lineage_candidate_rs(
            signal,
            fs,
            optimizer_maxiter=RESCUE_MAXITER,
            max_optimized_starts=RESCUE_MAX_STARTS,
        )

    if primary.legacy_best_success:
        chosen = primary
        source = "primary"
    elif rescue is not None and rescue.legacy_best_success:
        chosen = rescue
        source = "rescue"
    elif (
        rescue is not None
        and rescue.negative_log_likelihood < primary.negative_log_likelihood
    ):
        chosen = rescue
        source = "rescue"
    else:
        chosen = primary
        source = "primary"

    return {
        "primary": serialize_fit(primary),
        "rescue": serialize_fit(rescue) if rescue is not None else None,
        "chosen_source": source,
        "chosen": serialize_fit(chosen),
    }


def truth_checks(truth: dict[str, Any]) -> dict[str, Any]:
    qc_min = float(np.min(np.linalg.eigvalsh(truth["Qc"])))
    qd_min = float(np.min(np.linalg.eigvalsh(truth["Qd"])))
    alias_safe = bool(DECIMATION * truth["theta"] < math.pi)
    return {
        "Qc_min_eigenvalue": qc_min,
        "Qd_min_eigenvalue": qd_min,
        "alias_safe_factor_2": alias_safe,
        "m_theta": float(DECIMATION * truth["theta"]),
    }


def row(
    *,
    cell: tuple[int, float, float, float, float],
    seed: int,
    rate_label: str,
    signal: np.ndarray,
    fs: float,
) -> dict[str, Any]:
    index, A, fn, chi, g = cell
    route = fit_route(signal, fs)
    fit = route["chosen"]
    pars = fit["parameters"]
    return {
        "cell_index": index,
        "seed": seed,
        "rate_label": rate_label,
        "sampling_rate_hz": fs,
        "sample_count": int(signal.size),
        "truth_A": A,
        "truth_observation_noise_fraction": float(1.0 - A),
        "truth_natural_frequency_hz": fn,
        "truth_chi": chi,
        "truth_g": g,
        "duration_seconds": SECONDS,
        "cycles_observed": float(fn * SECONDS),
        "fit_route": route,
        "fitted_A": float(pars["latent_fraction"]),
        "fitted_natural_frequency_hz": float(pars["natural_frequency_hz"]),
        "fitted_chi": float(pars["damping_ratio"]),
        "fitted_g": float(pars["g"]),
        "signed_A_error": float(pars["latent_fraction"] - A),
        "signed_fn_error_hz": float(pars["natural_frequency_hz"] - fn),
        "signed_chi_error": float(pars["damping_ratio"] - chi),
        "signed_g_error": float(pars["g"] - g),
        "abs_A_error": float(abs(pars["latent_fraction"] - A)),
        "abs_fn_error_hz": float(abs(pars["natural_frequency_hz"] - fn)),
        "abs_chi_error": float(abs(pars["damping_ratio"] - chi)),
        "abs_g_error": float(abs(pars["g"] - g)),
        "raw_boundary_flag": bool(fit["raw_boundary_flag"]),
        "raw_box_edge_distance": float(fit["raw_box_edge_distance"]),
        "g_boundary_distance": float(fit["g_boundary_distance"]),
        "recurrence_seed_ready": bool(fit["recurrence_seed_ready"]),
        "recurrence_winning": bool(
            fit["winning_start_origin"] == "recurrence"
        ),
        "fit_success": bool(fit["success"]),
    }


def pair(fine: dict[str, Any], coarse: dict[str, Any]) -> dict[str, Any]:
    return {
        "cell_index": fine["cell_index"],
        "seed": fine["seed"],
        "chi_rate_drift": float(
            abs(fine["fitted_chi"] - coarse["fitted_chi"])
        ),
        "g_rate_drift": float(
            abs(fine["fitted_g"] - coarse["fitted_g"])
        ),
        "fn_rate_drift_hz": float(
            abs(
                fine["fitted_natural_frequency_hz"]
                - coarse["fitted_natural_frequency_hz"]
            )
        ),
    }


def run_cell(
    cell_index: int,
    preflight: bool,
    output_dir: Path,
) -> dict[str, Any]:
    if cell_index < 0 or cell_index >= len(CELLS):
        raise ValueError("cell index out of range")
    cell = CELLS[cell_index]
    seeds = (
        [s for s in SEEDS if s in PREFLIGHT_SEEDS]
        if preflight
        else list(SEEDS)
    )
    if preflight and cell_index not in PREFLIGHT_CELLS:
        raise ValueError("cell is not in frozen preflight set")

    rows = []
    pairs = []
    audits = []

    for seed in seeds:
        _, A, fn, chi, g = cell
        truth = construct_truth(
            fs=FINE_FS,
            A=A,
            natural_frequency_hz=fn,
            zeta=chi,
            g=g,
        )
        audit = truth_checks(truth)
        audits.append({"cell_index": cell_index, "seed": seed, **audit})

        if audit["Qc_min_eigenvalue"] < -1e-8:
            raise RuntimeError("invalid continuous covariance")
        if audit["Qd_min_eigenvalue"] < -1e-8:
            raise RuntimeError("invalid discrete covariance")
        if not audit["alias_safe_factor_2"]:
            raise RuntimeError("frozen design violates alias safety")

        fine_signal = simulate_same_path(truth, seconds=SECONDS, seed=seed)
        coarse_signal = fine_signal[::DECIMATION]

        fine = row(
            cell=cell,
            seed=seed,
            rate_label="fine",
            signal=fine_signal,
            fs=FINE_FS,
        )
        coarse = row(
            cell=cell,
            seed=seed,
            rate_label="coarse",
            signal=coarse_signal,
            fs=FINE_FS / DECIMATION,
        )
        rows.extend([fine, coarse])
        pairs.append(pair(fine, coarse))

    payload = {
        "status": (
            "P0Q_C1Q_RS_UNCERTAINTY_PREFLIGHT_CELL_COMPLETE"
            if preflight
            else "P0Q_C1Q_RS_UNCERTAINTY_CELL_COMPLETE"
        ),
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "promotes_production_estimator": False,
        "biological_prevalence_claim": False,
        "cell_index": cell_index,
        "preflight": preflight,
        "environment": environment_record(),
        "truth_audit": audits,
        "rows": rows,
        "pairs": pairs,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    label = "preflight" if preflight else "full"
    out = output_dir / f"c1q_rs_uncertainty_{label}_cell_{cell_index}.json"
    out.write_text(
        json.dumps(payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "cell": cell_index,
                "preflight": preflight,
                "rows": len(rows),
                "output": str(out),
            },
            sort_keys=True,
        )
    )
    return payload


def values(rows, key):
    return np.asarray(
        [
            float(r[key])
            for r in rows
            if r.get(key) is not None and math.isfinite(float(r[key]))
        ],
        dtype=float,
    )


def distribution(rows, key) -> dict[str, Any]:
    x = values(rows, key)
    if x.size == 0:
        return {
            "count": 0,
            "mean": None,
            "std": None,
            "median": None,
            "mad": None,
            "q25": None,
            "q75": None,
            "min": None,
            "max": None,
        }
    med = float(np.median(x))
    return {
        "count": int(x.size),
        "mean": float(np.mean(x)),
        "std": float(np.std(x, ddof=1)) if x.size > 1 else 0.0,
        "median": med,
        "mad": float(np.median(np.abs(x - med))),
        "q25": float(np.quantile(x, 0.25)),
        "q75": float(np.quantile(x, 0.75)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
    }


def cell_rate_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    keys = [
        "fitted_chi",
        "fitted_g",
        "fitted_natural_frequency_hz",
        "signed_chi_error",
        "signed_g_error",
        "signed_fn_error_hz",
        "abs_chi_error",
        "abs_g_error",
        "abs_fn_error_hz",
    ]
    return {
        **{key: distribution(rows, key) for key in keys},
        "row_count": len(rows),
        "raw_boundary_count": int(
            sum(bool(r["raw_boundary_flag"]) for r in rows)
        ),
        "recurrence_seed_ready_count": int(
            sum(bool(r["recurrence_seed_ready"]) for r in rows)
        ),
        "recurrence_winning_count": int(
            sum(bool(r["recurrence_winning"]) for r in rows)
        ),
        "fit_success_count": int(sum(bool(r["fit_success"]) for r in rows)),
    }


def merge(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    files = sorted(input_dir.rglob("c1q_rs_uncertainty_full_cell_*.json"))
    if len(files) != 8:
        raise RuntimeError(f"expected 8 full cell files, found {len(files)}")

    payloads = [json.loads(p.read_text(encoding="utf-8")) for p in files]
    rows = [r for p in payloads for r in p["rows"]]
    pairs = [r for p in payloads for r in p["pairs"]]
    audits = [r for p in payloads for r in p["truth_audit"]]

    if len(rows) != 192:
        raise RuntimeError(f"unexpected row count {len(rows)}")
    if len(pairs) != 96:
        raise RuntimeError(f"unexpected pair count {len(pairs)}")

    cells = sorted({int(r["cell_index"]) for r in rows})
    seeds = sorted({int(r["seed"]) for r in rows})
    if cells != list(range(8)):
        raise RuntimeError(f"cell identity mismatch: {cells}")
    if seeds != sorted(SEEDS):
        raise RuntimeError(f"seed identity mismatch: {seeds}")

    by_cell_rate = {}
    for cell in range(8):
        by_cell_rate[str(cell)] = {}
        for rate in ("fine", "coarse"):
            rr = [
                r
                for r in rows
                if r["cell_index"] == cell and r["rate_label"] == rate
            ]
            by_cell_rate[str(cell)][rate] = cell_rate_summary(rr)

    pair_summary = {}
    for cell in range(8):
        rr = [r for r in pairs if r["cell_index"] == cell]
        pair_summary[str(cell)] = {
            "chi_rate_drift": distribution(rr, "chi_rate_drift"),
            "g_rate_drift": distribution(rr, "g_rate_drift"),
            "fn_rate_drift_hz": distribution(rr, "fn_rate_drift_hz"),
        }

    overall = {
        "row_count": len(rows),
        "pair_count": len(pairs),
        "fit_success_count": int(sum(bool(r["fit_success"]) for r in rows)),
        "raw_boundary_count": int(
            sum(bool(r["raw_boundary_flag"]) for r in rows)
        ),
        "recurrence_seed_ready_count": int(
            sum(bool(r["recurrence_seed_ready"]) for r in rows)
        ),
        "recurrence_winning_count": int(
            sum(bool(r["recurrence_winning"]) for r in rows)
        ),
        "abs_chi_error": distribution(rows, "abs_chi_error"),
        "abs_g_error": distribution(rows, "abs_g_error"),
        "abs_fn_error_hz": distribution(rows, "abs_fn_error_hz"),
        "chi_rate_drift": distribution(pairs, "chi_rate_drift"),
        "g_rate_drift": distribution(pairs, "g_rate_drift"),
        "fn_rate_drift_hz": distribution(pairs, "fn_rate_drift_hz"),
    }

    result = {
        "status": "P0Q_C1Q_RS_UNCERTAINTY_MAP_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "promotes_production_estimator": False,
        "biological_prevalence_claim": False,
        "environment_records": [p["environment"] for p in payloads],
        "rows": rows,
        "pairs": pairs,
        "truth_audit": audits,
        "overall": overall,
        "by_cell_rate": by_cell_rate,
        "pair_summary_by_cell": pair_summary,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "c1q_rs_uncertainty_map_complete.json"
    out.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "rows": len(rows),
                "pairs": len(pairs),
                "output": str(out),
            },
            sort_keys=True,
        )
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("cell", "merge"), required=True)
    parser.add_argument("--cell", type=int)
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.mode == "cell":
        if args.cell is None:
            raise ValueError("cell mode requires --cell")
        run_cell(args.cell, args.preflight, args.output_dir)
    else:
        if args.input_dir is None:
            raise ValueError("merge mode requires --input-dir")
        merge(args.input_dir, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
