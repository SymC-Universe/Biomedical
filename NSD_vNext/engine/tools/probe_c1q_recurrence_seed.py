#!/usr/bin/env python3
"""Truth-blind recurrence/covariance seed diagnostic for C1Q.

P0-Q / APQ-1 frozen execution. This tool does not modify C1Q. It constructs
one data-derived start from positive-lag covariance, locally optimizes the
existing C1Q likelihood from that start, and compares it with the immutable
source-selected and truth-seeded basins from the completed root-cause artifact.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize

from nsd_engine.continuous_lineage_candidate import _nll, _steady_state
from nsd_engine.state_space_adequacy import (
    _fraction_from_raw,
    _frequency_from_raw,
    _raw_fraction,
    _raw_frequency,
    _raw_rho,
    _rho_from_raw,
)
from probe_continuous_lineage_nonzero_g import construct_truth, simulate_same_path


BOUNDARY_CELLS = (0, 5, 7, 8, 9, 11, 12, 15)
SOURCE_BASIN_RUN = 36369682759
SOURCE_BASIN_ARTIFACT = 10948127976
SOURCE_BASIN_DIGEST = (
    "sha256:f8d5c1eae3a38d8b8751190767e78e264c91c44a1edacaf85619a781e9e1a105"
)
FINE_FS = 256.0
DECIMATION = 2
SECONDS = 60.0
FMIN = 1.0
FMAX = 45.0
BURN = 128
MAX_LAG = 12
LOCAL_MAXITER = 200
MECH_REL_TOL = 1e-6
G_NUMERIC_EPS = 1e-6


def standardize(signal: np.ndarray) -> np.ndarray:
    x = np.asarray(signal, dtype=np.float64)
    sd = float(np.std(x))
    if not math.isfinite(sd) or sd <= 0.0:
        raise ValueError("signal has zero or non-finite standard deviation")
    return (x - float(np.mean(x))) / sd


def normalized_covariances(x: np.ndarray, max_lag: int) -> np.ndarray:
    variance = float(np.mean(x * x))
    if not math.isfinite(variance) or variance <= 0.0:
        raise ValueError("standardized signal variance is invalid")
    return np.asarray(
        [float(np.mean(x[:-k] * x[k:])) / variance for k in range(1, max_lag + 1)],
        dtype=np.float64,
    )


def recurrence_seed(signal: np.ndarray, fs: float) -> dict[str, Any]:
    x = standardize(signal)
    gamma = normalized_covariances(x, MAX_LAG)

    Xr = []
    yr = []
    for i in range(MAX_LAG - 2):
        Xr.append([gamma[i + 1], -gamma[i]])
        yr.append(gamma[i + 2])
    Xr = np.asarray(Xr, dtype=np.float64)
    yr = np.asarray(yr, dtype=np.float64)

    rank = int(np.linalg.matrix_rank(Xr))
    cond = float(np.linalg.cond(Xr))
    if rank < 2:
        return {
            "status": "REFUSE_RANK_DEFICIENT",
            "recurrence_rank": rank,
            "recurrence_condition_number": cond,
        }

    coeff, _, _, _ = np.linalg.lstsq(Xr, yr, rcond=None)
    a = float(coeff[0])
    b = float(coeff[1])
    recurrence_residual_rms = float(
        math.sqrt(float(np.mean((yr - Xr @ coeff) ** 2)))
    )

    if not (math.isfinite(a) and math.isfinite(b) and 0.0 < b < 1.0):
        return {
            "status": "REFUSE_NONSTABLE_RECURRENCE",
            "a": a,
            "b": b,
            "recurrence_rank": rank,
            "recurrence_condition_number": cond,
            "recurrence_residual_rms": recurrence_residual_rms,
        }

    rho = math.sqrt(b)
    xi = a / (2.0 * rho)
    if not (-1.0 < xi < 1.0):
        return {
            "status": "REFUSE_NOT_UNDERDAMPED",
            "a": a,
            "b": b,
            "rho": rho,
            "xi": xi,
            "recurrence_rank": rank,
            "recurrence_condition_number": cond,
            "recurrence_residual_rms": recurrence_residual_rms,
        }

    theta = math.acos(xi)
    L = -math.log(rho)
    fd_hz = theta * fs / (2.0 * math.pi)

    rho_lo = _rho_from_raw(-8.0)
    rho_hi = _rho_from_raw(8.0)
    fd_lo = _frequency_from_raw(-8.0, FMIN, FMAX)
    fd_hi = _frequency_from_raw(8.0, FMIN, FMAX)
    if not (rho_lo <= rho <= rho_hi):
        return {
            "status": "REFUSE_RHO_OUTSIDE_C1Q_DOMAIN",
            "rho": rho,
            "rho_domain": [rho_lo, rho_hi],
            "theta": theta,
            "fd_hz": fd_hz,
            "recurrence_condition_number": cond,
        }
    if not (fd_lo <= fd_hz <= fd_hi):
        return {
            "status": "REFUSE_FREQUENCY_OUTSIDE_C1Q_DOMAIN",
            "rho": rho,
            "theta": theta,
            "fd_hz": fd_hz,
            "frequency_domain_hz": [fd_lo, fd_hi],
            "recurrence_condition_number": cond,
        }

    k = np.arange(1, MAX_LAG + 1, dtype=np.float64)
    Xamp = np.column_stack(
        [
            (rho**k) * np.cos(k * theta),
            (rho**k) * (L / theta) * np.sin(k * theta),
        ]
    )
    amp_coeff, _, _, _ = np.linalg.lstsq(Xamp, gamma, rcond=None)
    A_unprojected = float(amp_coeff[0])
    Ag_unprojected = float(amp_coeff[1])
    g_unprojected = (
        float(Ag_unprojected / A_unprojected)
        if math.isfinite(A_unprojected) and abs(A_unprojected) > 1e-12
        else float("nan")
    )
    covariance_fit_residual_rms = float(
        math.sqrt(float(np.mean((gamma - Xamp @ amp_coeff) ** 2)))
    )

    if not (math.isfinite(A_unprojected) and math.isfinite(g_unprojected)):
        return {
            "status": "REFUSE_NONFINITE_AMPLITUDE_SEED",
            "rho": rho,
            "theta": theta,
            "fd_hz": fd_hz,
            "A_unprojected": A_unprojected,
            "Ag_unprojected": Ag_unprojected,
            "g_unprojected": g_unprojected,
            "recurrence_condition_number": cond,
            "recurrence_residual_rms": recurrence_residual_rms,
            "covariance_fit_residual_rms": covariance_fit_residual_rms,
        }

    A_lo = _fraction_from_raw(-8.0)
    A_hi = _fraction_from_raw(8.0)
    A_seed = float(np.clip(A_unprojected, A_lo, A_hi))
    g_seed = float(np.clip(g_unprojected, -1.0 + G_NUMERIC_EPS, 1.0 - G_NUMERIC_EPS))

    raw = np.asarray(
        [
            _raw_fraction(A_seed),
            _raw_rho(rho),
            _raw_frequency(fd_hz, FMIN, FMAX),
            float(np.arctanh(g_seed)),
        ],
        dtype=np.float64,
    )
    if np.any(raw < -8.0) or np.any(raw > 8.0):
        return {
            "status": "REFUSE_RAW_SEED_OUTSIDE_BOX",
            "raw_parameters": [float(v) for v in raw],
        }

    return {
        "status": "SEED_READY",
        "a": a,
        "b": b,
        "rho": rho,
        "xi": xi,
        "theta": theta,
        "L": L,
        "fd_hz": fd_hz,
        "A_unprojected": A_unprojected,
        "Ag_unprojected": Ag_unprojected,
        "g_unprojected": g_unprojected,
        "A_seed": A_seed,
        "g_seed": g_seed,
        "A_projected": bool(A_seed != A_unprojected),
        "g_projected": bool(g_seed != g_unprojected),
        "raw_parameters": [float(v) for v in raw],
        "recurrence_rank": rank,
        "recurrence_condition_number": cond,
        "recurrence_residual_rms": recurrence_residual_rms,
        "covariance_fit_residual_rms": covariance_fit_residual_rms,
    }


def local_optimize(signal: np.ndarray, fs: float, raw_start: np.ndarray) -> dict[str, Any]:
    x = standardize(signal)
    start_nll = float(_nll(x, raw_start, fs, FMIN, FMAX, BURN))
    result = minimize(
        lambda raw: _nll(x, raw, fs, FMIN, FMAX, BURN),
        np.asarray(raw_start, dtype=np.float64),
        method="L-BFGS-B",
        bounds=[(-8.0, 8.0)] * 4,
        options={"maxiter": LOCAL_MAXITER, "ftol": 1e-10, "maxls": 50},
    )
    raw = np.asarray(result.x, dtype=np.float64)
    steady = _steady_state(raw, fs, FMIN, FMAX)
    parameters = None if steady is None else {k: float(v) for k, v in steady[3].items()}
    return {
        "start_nll": start_nll,
        "success": bool(result.success),
        "message": str(result.message),
        "nit": int(getattr(result, "nit", -1)),
        "nfev": int(getattr(result, "nfev", -1)),
        "nll": float(result.fun),
        "raw_parameters": [float(v) for v in raw],
        "raw_box_min_distance": float(min(8.0 - abs(float(v)) for v in raw)),
        "parameters": parameters,
    }


def run_cell(source_basin: Path, cell: int, output_dir: Path) -> dict[str, Any]:
    source = json.loads(source_basin.read_text(encoding="utf-8"))
    if source.get("status") != "P0Q_C1Q_LIKELIHOOD_BASIN_COMPLETE":
        raise RuntimeError("unexpected source basin artifact")
    if cell not in BOUNDARY_CELLS:
        raise ValueError(f"cell {cell} not in frozen cell set")

    rows = [r for r in source["rows"] if int(r["cell_index"]) == cell]
    if len(rows) != 6:
        raise RuntimeError(f"expected six source rows for cell {cell}, found {len(rows)}")

    by_seed: dict[int, dict[str, dict[str, Any]]] = {}
    for row in rows:
        by_seed.setdefault(int(row["seed"]), {})[row["rate_label"]] = row

    output_rows = []
    for seed, rate_rows in sorted(by_seed.items()):
        fine_source = rate_rows["fine"]
        truth = fine_source["truth"]
        generator = construct_truth(
            fs=FINE_FS,
            A=float(truth["A"]),
            natural_frequency_hz=float(truth["natural_frequency_hz"]),
            zeta=float(truth["chi"]),
            g=float(truth["g"]),
        )
        fine = simulate_same_path(generator, seconds=SECONDS, seed=seed)
        signals = {"fine": fine, "coarse": fine[::DECIMATION]}

        for rate in ("fine", "coarse"):
            src = rate_rows[rate]
            signal = signals[rate]
            fs = float(src["sampling_rate_hz"])
            seed_info = recurrence_seed(signal, fs)

            row_out: dict[str, Any] = {
                "cell_index": cell,
                "seed": seed,
                "rate_label": rate,
                "sampling_rate_hz": fs,
                "truth": src["truth"],
                "source_selected_nll": float(src["source_selected"]["recomputed_nll"]),
                "truth_seeded_nll": float(src["truth_seed_local"]["nll"]),
                "recurrence_seed": seed_info,
                "source_selected_raw_box_min_distance": float(
                    src["source_selected"]["raw_box_min_distance"]
                ),
            }

            if seed_info["status"] == "SEED_READY":
                fit = local_optimize(
                    signal,
                    fs,
                    np.asarray(seed_info["raw_parameters"], dtype=np.float64),
                )
                reference = float(src["truth_seed_local"]["nll"])
                tolerance = MECH_REL_TOL * max(1.0, abs(reference))
                fit_nll = float(fit["nll"])
                selected_nll = float(src["source_selected"]["recomputed_nll"])
                row_out["recurrence_seed_local"] = fit
                row_out["nll_differences"] = {
                    "recurrence_seed_minus_source_selected": float(
                        fit_nll - selected_nll
                    ),
                    "recurrence_seed_minus_truth_seeded": float(
                        fit_nll - reference
                    ),
                }
                row_out["mechanical_direction_flags"] = {
                    "recurrence_seed_beats_source_selected": bool(
                        fit_nll < selected_nll - tolerance
                    ),
                    "recurrence_seed_matches_or_beats_truth_seeded": bool(
                        fit_nll <= reference + tolerance
                    ),
                }
            else:
                row_out["recurrence_seed_local"] = None
                row_out["nll_differences"] = None
                row_out["mechanical_direction_flags"] = {
                    "recurrence_seed_beats_source_selected": False,
                    "recurrence_seed_matches_or_beats_truth_seeded": False,
                }

            output_rows.append(row_out)

    payload = {
        "status": "P0Q_C1Q_RECURRENCE_SEED_CELL_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "changes_estimator": False,
        "source_basin_run": SOURCE_BASIN_RUN,
        "source_basin_artifact": SOURCE_BASIN_ARTIFACT,
        "source_basin_digest": SOURCE_BASIN_DIGEST,
        "cell_index": cell,
        "row_count": len(output_rows),
        "rows": output_rows,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / f"c1q_recurrence_seed_cell_{cell}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"cell": cell, "rows": len(output_rows), "output": str(out)}, sort_keys=True))
    return payload


def stats(values) -> dict[str, Any]:
    vals = np.asarray(
        [float(v) for v in values if v is not None and math.isfinite(float(v))],
        dtype=np.float64,
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
    files = sorted(input_dir.rglob("c1q_recurrence_seed_cell_*.json"))
    if len(files) != len(BOUNDARY_CELLS):
        raise RuntimeError(f"expected {len(BOUNDARY_CELLS)} cell files, found {len(files)}")
    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    rows = [r for p in payloads for r in p["rows"]]
    if len(rows) != 48:
        raise RuntimeError(f"expected 48 rows, found {len(rows)}")

    ready = [r for r in rows if r["recurrence_seed"]["status"] == "SEED_READY"]
    summary = {
        "row_count": len(rows),
        "seed_ready_count": len(ready),
        "seed_refusal_count": len(rows) - len(ready),
        "A_projection_count": int(
            sum(r["recurrence_seed"].get("A_projected", False) for r in ready)
        ),
        "g_projection_count": int(
            sum(r["recurrence_seed"].get("g_projected", False) for r in ready)
        ),
        "recurrence_seed_beats_source_selected_count": int(
            sum(
                r["mechanical_direction_flags"][
                    "recurrence_seed_beats_source_selected"
                ]
                for r in rows
            )
        ),
        "recurrence_seed_matches_or_beats_truth_seeded_count": int(
            sum(
                r["mechanical_direction_flags"][
                    "recurrence_seed_matches_or_beats_truth_seeded"
                ]
                for r in rows
            )
        ),
        "recurrence_seed_minus_source_selected_nll": stats(
            r["nll_differences"]["recurrence_seed_minus_source_selected"]
            for r in ready
        ),
        "recurrence_seed_minus_truth_seeded_nll": stats(
            r["nll_differences"]["recurrence_seed_minus_truth_seeded"]
            for r in ready
        ),
        "recurrence_condition_number": stats(
            r["recurrence_seed"].get("recurrence_condition_number") for r in rows
        ),
        "covariance_fit_residual_rms": stats(
            r["recurrence_seed"].get("covariance_fit_residual_rms") for r in ready
        ),
    }

    by_rate = {}
    for rate in ("fine", "coarse"):
        rr = [r for r in rows if r["rate_label"] == rate]
        ready_r = [r for r in rr if r["recurrence_seed"]["status"] == "SEED_READY"]
        by_rate[rate] = {
            "row_count": len(rr),
            "seed_ready_count": len(ready_r),
            "recurrence_seed_beats_source_selected_count": int(
                sum(
                    r["mechanical_direction_flags"][
                        "recurrence_seed_beats_source_selected"
                    ]
                    for r in rr
                )
            ),
            "recurrence_seed_matches_or_beats_truth_seeded_count": int(
                sum(
                    r["mechanical_direction_flags"][
                        "recurrence_seed_matches_or_beats_truth_seeded"
                    ]
                    for r in rr
                )
            ),
            "recurrence_seed_minus_truth_seeded_nll": stats(
                r["nll_differences"]["recurrence_seed_minus_truth_seeded"]
                for r in ready_r
            ),
        }

    merged = {
        "status": "P0Q_C1Q_RECURRENCE_SEED_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "changes_estimator": False,
        "source_basin_run": SOURCE_BASIN_RUN,
        "source_basin_artifact": SOURCE_BASIN_ARTIFACT,
        "source_basin_digest": SOURCE_BASIN_DIGEST,
        "rows": rows,
        "summary": summary,
        "by_rate": by_rate,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "c1q_recurrence_seed_complete.json"
    out.write_text(json.dumps(merged, indent=2, sort_keys=True), encoding="utf-8")
    md = output_dir / "c1q_recurrence_seed_summary.md"
    md.write_text(
        "\n".join(
            [
                "# C1Q Recurrence-Seed Rescue Summary",
                "",
                "**Status:** P0-Q truth-blind initialization test",
                "",
                f"- Rows: {summary['row_count']}",
                f"- Seed ready: {summary['seed_ready_count']}",
                f"- Seed refusal: {summary['seed_refusal_count']}",
                f"- Recurrence seed beats source selected: {summary['recurrence_seed_beats_source_selected_count']}",
                f"- Recurrence seed matches or beats truth-seeded basin within numerical tolerance: {summary['recurrence_seed_matches_or_beats_truth_seeded_count']}",
                f"- A projection count: {summary['A_projection_count']}",
                f"- g projection count: {summary['g_projection_count']}",
                "",
                "No estimator modification, scientific threshold, biological prevalence claim, or real-EEG admission is defined.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": merged["status"], "rows": len(rows), "output": str(out)}, sort_keys=True))
    return merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("cell", "merge"), required=True)
    parser.add_argument("--source-basin", type=Path)
    parser.add_argument("--cell", type=int)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.mode == "cell":
        if args.source_basin is None or args.cell is None:
            raise ValueError("cell mode requires --source-basin and --cell")
        run_cell(args.source_basin, args.cell, args.output_dir)
    else:
        if args.input_dir is None:
            raise ValueError("merge mode requires --input-dir")
        merge(args.input_dir, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
