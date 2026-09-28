#!/usr/bin/env python3
"""C1Q-RS Function Map repair qualification.

P0-Q only. Reuses the immutable C-interior Function Map design and archived
C1Q rows, regenerates exact known-truth paths, fits C1Q-RS with preserved
legacy primary/rescue semantics, and compares recurrence augmentation with one
compute-matched next-ranked legacy start on the frozen root-cause cells.

No estimator is promoted and no scientific threshold is defined.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize

from nsd_engine.continuous_lineage_candidate import (
    _nll,
    _select_legacy_optimized_starts,
)
from nsd_engine.continuous_lineage_candidate_rs import (
    ContinuousLineageRSCandidateFit,
    fit_continuous_lineage_candidate_rs,
)
from probe_continuous_lineage_nonzero_g import construct_truth, simulate_same_path


CELLS = [
    (0, 0.371004707, 9.892272022, 0.504089061, -0.034300108),
    (1, 0.658443794, 15.100740636, 0.482040667, 0.044371614),
    (2, 0.892343308, 4.476334769, 0.778687826, -0.570623136),
    (3, 0.473630218, 20.687577935, 0.231985860, 0.557254179),
    (4, 0.432551656, 6.878767651, 0.364377508, 0.760427584),
    (5, 0.758293355, 23.785478780, 0.648926574, -0.773792034),
    (6, 0.612110780, 12.301666114, 0.267449703, 0.247541299),
    (7, 0.242637803, 18.189667420, 0.726651006, -0.237471201),
    (8, 0.261257801, 3.293630781, 0.308216329, -0.634738243),
    (9, 0.591763440, 22.214669872, 0.679922958, 0.649498792),
    (10, 0.784792872, 8.710853929, 0.405086727, -0.373406155),
    (11, 0.410513189, 16.623925384, 0.602130437, 0.361601254),
    (12, 0.544221032, 13.869666623, 0.824758969, 0.158424690),
    (13, 0.825529283, 16.967463199, 0.190551668, -0.170228185),
    (14, 0.720473163, 8.447991112, 0.550089446, 0.446320035),
    (15, 0.307933592, 22.559304427, 0.440546398, -0.431563991),
]
BOUNDARY_CELLS = {0, 5, 7, 8, 9, 11, 12, 15}
SEEDS = [104729, 208457, 417923]
FINE_FS = 256.0
DECIMATION = 2
SECONDS = 60.0
PRIMARY_MAXITER = 80
PRIMARY_MAX_STARTS = 18
RESCUE_MAXITER = 160
RESCUE_MAX_STARTS = 24
FMIN = 1.0
FMAX = 45.0
BURN = 128
MECH_REL_TOL = 1e-6


def standardize(signal: np.ndarray) -> np.ndarray:
    x = np.asarray(signal, dtype=float)
    return (x - float(np.mean(x))) / float(np.std(x))


def fit_rs_route(signal: np.ndarray, fs: float) -> dict[str, Any]:
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
    elif rescue is not None and rescue.negative_log_likelihood < primary.negative_log_likelihood:
        chosen = rescue
        source = "rescue"
    else:
        chosen = primary
        source = "primary"

    return {
        "primary": serialize_rs(primary),
        "rescue": serialize_rs(rescue) if rescue is not None else None,
        "chosen_source": source,
        "chosen": serialize_rs(chosen),
    }


def serialize_rs(fit: ContinuousLineageRSCandidateFit | None) -> dict[str, Any] | None:
    if fit is None:
        return None
    return {
        "success": fit.success,
        "negative_log_likelihood": fit.negative_log_likelihood,
        "bic": fit.bic,
        "parameters": fit.parameters,
        "raw_parameters": list(fit.raw_parameters),
        "attempted_start_count": fit.attempted_start_count,
        "converged_start_count": fit.converged_start_count,
        "legacy_attempted_start_count": fit.legacy_attempted_start_count,
        "legacy_converged_start_count": fit.legacy_converged_start_count,
        "legacy_best_negative_log_likelihood": fit.legacy_best_negative_log_likelihood,
        "legacy_best_success": fit.legacy_best_success,
        "legacy_best_raw_parameters": list(fit.legacy_best_raw_parameters),
        "winning_start_origin": fit.winning_start_origin,
        "recurrence_seed_status": fit.recurrence_seed_status,
        "recurrence_seed_ready": fit.recurrence_seed_ready,
        "recurrence_seed_A_unprojected": fit.recurrence_seed_A_unprojected,
        "recurrence_seed_g_unprojected": fit.recurrence_seed_g_unprojected,
        "recurrence_seed_A_projected": fit.recurrence_seed_A_projected,
        "recurrence_seed_g_projected": fit.recurrence_seed_g_projected,
        "recurrence_seed_raw_parameters": (
            list(fit.recurrence_seed_raw_parameters)
            if fit.recurrence_seed_raw_parameters is not None
            else None
        ),
        "recurrence_seed_start_nll": fit.recurrence_seed_start_nll,
        "next_ranked_legacy_raw_parameters": (
            list(fit.next_ranked_legacy_raw_parameters)
            if fit.next_ranked_legacy_raw_parameters is not None
            else None
        ),
    }


def optimize_extra_legacy(
    signal: np.ndarray,
    fs: float,
    *,
    legacy_stage: str,
) -> dict[str, Any]:
    x = standardize(signal)
    if legacy_stage == "rescue":
        nstarts = RESCUE_MAX_STARTS
        maxiter = RESCUE_MAXITER
    else:
        nstarts = PRIMARY_MAX_STARTS
        maxiter = PRIMARY_MAXITER

    selection = _select_legacy_optimized_starts(
        x, fs, FMIN, FMAX, BURN, nstarts
    )
    start = selection["next_ranked"]
    if start is None:
        return {"status": "NO_NEXT_RANKED_LEGACY_START"}

    start_nll = float(_nll(x, start, fs, FMIN, FMAX, BURN))
    result = minimize(
        lambda raw: _nll(x, raw, fs, FMIN, FMAX, BURN),
        np.asarray(start, dtype=float),
        method="L-BFGS-B",
        bounds=[(-8.0, 8.0)] * 4,
        options={"maxiter": maxiter, "ftol": 1e-8, "maxls": 30},
    )
    return {
        "status": "OPTIMIZED",
        "start_rank": nstarts + 1,
        "start_nll": start_nll,
        "negative_log_likelihood": float(result.fun),
        "success": bool(result.success),
        "raw_parameters": [float(v) for v in result.x],
        "message": str(result.message),
    }


def source_row_map(source: dict[str, Any]) -> dict[tuple[int, int, str], dict[str, Any]]:
    return {
        (int(r["cell_index"]), int(r["seed"]), str(r["rate_label"])): r
        for r in source["rows"]
    }


def run_cell(source_map: Path, cell_index: int, output_dir: Path) -> dict[str, Any]:
    source = json.loads(source_map.read_text(encoding="utf-8"))
    if source.get("status") != "P0D_FUNCTION_MAP_COMPLETE":
        raise RuntimeError("unexpected source Function Map status")
    rows = source_row_map(source)

    cell = CELLS[cell_index]
    _, A, fn, chi, g = cell
    output_rows = []
    for seed in SEEDS:
        truth = construct_truth(
            fs=FINE_FS,
            A=A,
            natural_frequency_hz=fn,
            zeta=chi,
            g=g,
        )
        fine = simulate_same_path(truth, seconds=SECONDS, seed=seed)
        signals = {"fine": fine, "coarse": fine[::DECIMATION]}
        rates = {"fine": FINE_FS, "coarse": FINE_FS / DECIMATION}

        for rate_label in ("fine", "coarse"):
            src = rows[(cell_index, seed, rate_label)]
            old_nll = float(
                src["c1q"][src["c1q_selected_source"]][
                    "negative_log_likelihood"
                ]
            )
            rs = fit_rs_route(signals[rate_label], rates[rate_label])
            chosen = rs["chosen"]
            tolerance = MECH_REL_TOL * max(1.0, abs(old_nll))
            nonworsening = bool(
                chosen["negative_log_likelihood"] <= old_nll + tolerance
            )
            if not nonworsening:
                raise RuntimeError(
                    f"strict containment failed cell={cell_index} seed={seed} "
                    f"rate={rate_label}: old={old_nll}, "
                    f"rs={chosen['negative_log_likelihood']}"
                )

            pars = chosen["parameters"]
            row = {
                "cell_index": cell_index,
                "seed": seed,
                "rate_label": rate_label,
                "sampling_rate_hz": rates[rate_label],
                "truth_A": A,
                "truth_natural_frequency_hz": fn,
                "truth_chi": chi,
                "truth_g": g,
                "archived_c1q_selected_source": src["c1q_selected_source"],
                "archived_c1q_nll": old_nll,
                "archived_c1q_abs_chi_error": src["c1q_abs_chi_error"],
                "archived_c1q_abs_g_error": src["c1q_abs_g_error"],
                "rs": rs,
                "rs_nll_improvement": float(
                    old_nll - chosen["negative_log_likelihood"]
                ),
                "rs_abs_chi_error": float(abs(pars["damping_ratio"] - chi)),
                "rs_abs_g_error": float(abs(pars["g"] - g)),
                "rs_abs_fn_error_hz": float(
                    abs(pars["natural_frequency_hz"] - fn)
                ),
                "strict_nonworsening_pass": nonworsening,
                "extra_legacy_control": None,
            }

            if cell_index in BOUNDARY_CELLS:
                extra = optimize_extra_legacy(
                    signals[rate_label],
                    rates[rate_label],
                    legacy_stage=src["c1q_selected_source"],
                )
                row["extra_legacy_control"] = extra
                if extra["status"] == "OPTIMIZED":
                    row["extra_legacy_best_with_archived_nll"] = float(
                        min(old_nll, extra["negative_log_likelihood"])
                    )
                    row["rs_minus_compute_matched_best_nll"] = float(
                        chosen["negative_log_likelihood"]
                        - row["extra_legacy_best_with_archived_nll"]
                    )
                else:
                    row["extra_legacy_best_with_archived_nll"] = old_nll
                    row["rs_minus_compute_matched_best_nll"] = None

            output_rows.append(row)

    payload = {
        "status": "P0Q_C1Q_RS_FUNCTION_MAP_CELL_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "promotes_c1q_rs": False,
        "cell_index": cell_index,
        "rows": output_rows,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / f"c1q_rs_function_map_cell_{cell_index}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"cell": cell_index, "rows": len(output_rows), "output": str(out)}, sort_keys=True))
    return payload


def stats(values) -> dict[str, Any]:
    vals = np.asarray(
        [float(v) for v in values if v is not None and math.isfinite(float(v))],
        dtype=float,
    )
    if vals.size == 0:
        return {"count": 0, "min": None, "median": None, "max": None}
    return {
        "count": int(vals.size),
        "min": float(np.min(vals)),
        "median": float(np.median(vals)),
        "max": float(np.max(vals)),
    }


def merge(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    files = sorted(input_dir.rglob("c1q_rs_function_map_cell_*.json"))
    if len(files) != 16:
        raise RuntimeError(f"expected 16 cell artifacts, found {len(files)}")
    payloads = [json.loads(p.read_text(encoding="utf-8")) for p in files]
    rows = [r for p in payloads for r in p["rows"]]
    if len(rows) != 96:
        raise RuntimeError(f"expected 96 rows, found {len(rows)}")

    boundary_rows = [r for r in rows if int(r["cell_index"]) in BOUNDARY_CELLS]
    summary = {
        "row_count": len(rows),
        "strict_nonworsening_pass_count": int(
            sum(r["strict_nonworsening_pass"] for r in rows)
        ),
        "recurrence_seed_ready_count": int(
            sum(r["rs"]["chosen"]["recurrence_seed_ready"] for r in rows)
        ),
        "recurrence_winning_count": int(
            sum(r["rs"]["chosen"]["winning_start_origin"] == "recurrence" for r in rows)
        ),
        "rs_nll_improvement": stats(r["rs_nll_improvement"] for r in rows),
        "archived_abs_chi_error": stats(
            r["archived_c1q_abs_chi_error"] for r in rows
        ),
        "rs_abs_chi_error": stats(r["rs_abs_chi_error"] for r in rows),
        "archived_abs_g_error": stats(
            r["archived_c1q_abs_g_error"] for r in rows
        ),
        "rs_abs_g_error": stats(r["rs_abs_g_error"] for r in rows),
        "rs_abs_fn_error_hz": stats(r["rs_abs_fn_error_hz"] for r in rows),
        "boundary_row_count": len(boundary_rows),
        "recurrence_beats_compute_matched_extra_count": int(
            sum(
                r.get("rs_minus_compute_matched_best_nll") is not None
                and r["rs_minus_compute_matched_best_nll"]
                < -MECH_REL_TOL
                * max(1.0, abs(r["archived_c1q_nll"]))
                for r in boundary_rows
            )
        ),
    }

    by_rate = {}
    for rate in ("fine", "coarse"):
        rr = [r for r in rows if r["rate_label"] == rate]
        by_rate[rate] = {
            "row_count": len(rr),
            "rs_nll_improvement": stats(r["rs_nll_improvement"] for r in rr),
            "rs_abs_chi_error": stats(r["rs_abs_chi_error"] for r in rr),
            "rs_abs_g_error": stats(r["rs_abs_g_error"] for r in rr),
            "recurrence_winning_count": int(
                sum(r["rs"]["chosen"]["winning_start_origin"] == "recurrence" for r in rr)
            ),
        }

    merged = {
        "status": "P0Q_C1Q_RS_FUNCTION_MAP_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "promotes_c1q_rs": False,
        "rows": rows,
        "summary": summary,
        "by_rate": by_rate,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "c1q_rs_function_map_complete.json"
    out.write_text(json.dumps(merged, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": merged["status"], "rows": len(rows), "output": str(out)}, sort_keys=True))
    return merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("cell", "merge"), required=True)
    parser.add_argument("--source-map", type=Path)
    parser.add_argument("--cell", type=int)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.mode == "cell":
        if args.source_map is None or args.cell is None:
            raise ValueError("cell mode requires --source-map and --cell")
        run_cell(args.source_map, args.cell, args.output_dir)
    else:
        if args.input_dir is None:
            raise ValueError("merge mode requires --input-dir")
        merge(args.input_dir, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
