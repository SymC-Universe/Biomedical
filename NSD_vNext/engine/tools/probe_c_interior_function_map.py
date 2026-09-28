#!/usr/bin/env python3
"""Bio Chi C-interior Function Map.

GOM v1.0 / APQ-qualified P0-D execution.

This tool implements the frozen plan:
- 16 explicit C-family qualification cells;
- three fixed realization seeds;
- 256 Hz fine paths with exact factor-2 same-path decimation;
- qualification-only C1Q fits;
- a generic covariance-recurrence pole diagnostic;
- current A0/A1/A2 comparison on frozen sentinel cells only;
- no empirical admission threshold and no real-EEG licensing.

The map is a correct-specification estimator Function Map, not biological
validation. Synthetic design density is not biological prevalence.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
from pathlib import Path
import platform
import sys
from typing import Any

import numpy as np
import scipy

from nsd_engine.continuous_lineage_candidate import fit_continuous_lineage_candidate

# Reuse the already-qualified exact C truth constructor/path simulator.
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
SEEDS = [104729, 208457, 417923]
PREFLIGHT_CELLS = {0, 5, 10, 15}
FINE_FS = 256.0
DECIMATION = 2
SECONDS = 60.0
PRIMARY_MAXITER = 80
PRIMARY_MAX_STARTS = 18
RESCUE_MAXITER = 160
RESCUE_MAX_STARTS = 24


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


def covariance_recurrence_pole(signal: np.ndarray, fs: float, max_lag: int = 12) -> dict[str, Any]:
    """Generic second-order positive-lag recurrence diagnostic.

    Fits gamma_{k+2} = a gamma_{k+1} - b gamma_k by least squares on
    normalized positive-lag sample covariances. This is intentionally not the
    C1Q state-space likelihood/parameterization.
    """
    x = np.asarray(signal, dtype=float)
    x = x - float(np.mean(x))
    variance = float(np.mean(x * x))
    if not math.isfinite(variance) or variance <= 0.0:
        return {"status": "REFUSE_ZERO_VARIANCE"}

    x = x / math.sqrt(variance)
    gamma = np.asarray(
        [float(np.mean(x[:-lag] * x[lag:])) for lag in range(1, max_lag + 1)],
        dtype=float,
    )
    if not np.isfinite(gamma).all():
        return {"status": "REFUSE_NONFINITE_COVARIANCE"}

    # gamma indices represent lags 1..max_lag.
    rows = []
    targets = []
    for i in range(max_lag - 2):
        rows.append([gamma[i + 1], -gamma[i]])
        targets.append(gamma[i + 2])
    X = np.asarray(rows, dtype=float)
    y = np.asarray(targets, dtype=float)

    if np.linalg.matrix_rank(X) < 2:
        return {
            "status": "REFUSE_RANK_DEFICIENT",
            "condition_number": float(np.linalg.cond(X)),
        }

    coeff, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    a = float(coeff[0])
    b = float(coeff[1])
    condition = float(np.linalg.cond(X))
    residual = y - X @ coeff
    residual_rms = float(math.sqrt(float(np.mean(residual * residual))))

    if not (math.isfinite(a) and math.isfinite(b)):
        return {
            "status": "REFUSE_NONFINITE_COEFFICIENT",
            "a": a,
            "b": b,
            "condition_number": condition,
        }
    if not (0.0 < b < 1.0):
        return {
            "status": "REFUSE_NONSTABLE_B",
            "a": a,
            "b": b,
            "condition_number": condition,
            "residual_rms": residual_rms,
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
            "condition_number": condition,
            "residual_rms": residual_rms,
        }

    theta = math.acos(xi)
    L = -math.log(rho)
    chi = L / math.sqrt(L * L + theta * theta)
    natural_frequency_hz = (
        fs * math.sqrt(L * L + theta * theta) / (2.0 * math.pi)
    )
    damped_frequency_hz = fs * theta / (2.0 * math.pi)

    return {
        "status": "ESTIMATED",
        "a": a,
        "b": b,
        "rho": rho,
        "xi": xi,
        "theta": theta,
        "L": L,
        "chi": chi,
        "natural_frequency_hz": natural_frequency_hz,
        "damped_frequency_hz": damped_frequency_hz,
        "condition_number": condition,
        "residual_rms": residual_rms,
    }


def serialize_fit(fit) -> dict[str, Any]:
    raw = [float(v) for v in fit.raw_parameters]
    return {
        "status": "FIT_RETURNED",
        "success": bool(fit.success),
        "negative_log_likelihood": float(fit.negative_log_likelihood),
        "bic": float(fit.bic),
        "attempted_start_count": int(fit.attempted_start_count),
        "converged_start_count": int(fit.converged_start_count),
        "optimizer_message": str(fit.optimizer_message),
        "raw_parameters": raw,
        "max_abs_raw_parameter": float(max(abs(v) for v in raw)),
        "raw_box_min_distance": float(min(8.0 - abs(v) for v in raw)),
        "parameters": {k: float(v) for k, v in fit.parameters.items()},
        "g_distance_to_C_boundary": float(1.0 - abs(fit.parameters["g"])),
    }


def run_c1q(signal: np.ndarray, fs: float) -> dict[str, Any]:
    try:
        primary = fit_continuous_lineage_candidate(
            signal,
            fs,
            optimizer_maxiter=PRIMARY_MAXITER,
            max_optimized_starts=PRIMARY_MAX_STARTS,
        )
        out = {"primary": serialize_fit(primary), "rescue": None}
        if not primary.success:
            try:
                rescue = fit_continuous_lineage_candidate(
                    signal,
                    fs,
                    optimizer_maxiter=RESCUE_MAXITER,
                    max_optimized_starts=RESCUE_MAX_STARTS,
                )
                out["rescue"] = serialize_fit(rescue)
            except Exception as exc:
                out["rescue"] = {
                    "status": "OPTIMIZATION_UNRESOLVED",
                    "error": f"{type(exc).__name__}: {exc}",
                }
        return out
    except Exception as exc:
        out = {
            "primary": {
                "status": "OPTIMIZATION_UNRESOLVED",
                "error": f"{type(exc).__name__}: {exc}",
            },
            "rescue": None,
        }
        try:
            rescue = fit_continuous_lineage_candidate(
                signal,
                fs,
                optimizer_maxiter=RESCUE_MAXITER,
                max_optimized_starts=RESCUE_MAX_STARTS,
            )
            out["rescue"] = serialize_fit(rescue)
        except Exception as rescue_exc:
            out["rescue"] = {
                "status": "OPTIMIZATION_UNRESOLVED",
                "error": f"{type(rescue_exc).__name__}: {rescue_exc}",
            }
        return out


def chosen_fit(c1q: dict[str, Any]) -> dict[str, Any] | None:
    primary = c1q.get("primary")
    if primary and primary.get("status") == "FIT_RETURNED" and primary.get("success"):
        return primary
    rescue = c1q.get("rescue")
    if rescue and rescue.get("status") == "FIT_RETURNED" and rescue.get("success"):
        return rescue
    if primary and primary.get("status") == "FIT_RETURNED":
        return primary
    if rescue and rescue.get("status") == "FIT_RETURNED":
        return rescue
    return None


def truth_checks(truth: dict[str, Any], m: int) -> dict[str, Any]:
    q_c_min = float(np.min(np.linalg.eigvalsh(truth["Qc"])))
    q_d_min = float(np.min(np.linalg.eigvalsh(truth["Qd"])))
    alias_safe = bool(m * truth["theta"] < math.pi)
    return {
        "Qc_min_eigenvalue": q_c_min,
        "Qd_min_eigenvalue": q_d_min,
        "alias_safe_factor_m": alias_safe,
        "m_theta": float(m * truth["theta"]),
    }


def rate_row(
    *,
    cell: tuple[int, float, float, float, float],
    seed: int,
    rate_label: str,
    signal: np.ndarray,
    fs: float,
    truth: dict[str, Any],
) -> dict[str, Any]:
    index, A, fn, chi, g = cell
    c1q = run_c1q(signal, fs)
    selected = chosen_fit(c1q)
    recurrence = covariance_recurrence_pole(signal, fs)

    row: dict[str, Any] = {
        "cell_index": index,
        "seed": seed,
        "rate_label": rate_label,
        "sampling_rate_hz": fs,
        "sample_count": int(signal.size),
        "truth_A": A,
        "truth_natural_frequency_hz": fn,
        "truth_chi": chi,
        "truth_g": g,
        "truth_damped_frequency_hz": float(truth["nu"] / (2.0 * math.pi)),
        "c1q": c1q,
        "recurrence": recurrence,
    }

    if selected is not None:
        pars = selected["parameters"]
        row.update(
            {
                "c1q_selected_source": (
                    "primary"
                    if selected is c1q.get("primary")
                    else "rescue"
                ),
                "c1q_fit_success": bool(selected.get("success", False)),
                "c1q_fitted_chi": float(pars["damping_ratio"]),
                "c1q_signed_chi_error": float(pars["damping_ratio"] - chi),
                "c1q_abs_chi_error": float(abs(pars["damping_ratio"] - chi)),
                "c1q_fitted_g": float(pars["g"]),
                "c1q_signed_g_error": float(pars["g"] - g),
                "c1q_abs_g_error": float(abs(pars["g"] - g)),
                "c1q_fitted_natural_frequency_hz": float(
                    pars["natural_frequency_hz"]
                ),
                "c1q_abs_natural_frequency_error_hz": float(
                    abs(pars["natural_frequency_hz"] - fn)
                ),
                "c1q_raw_box_min_distance": float(
                    selected["raw_box_min_distance"]
                ),
                "c1q_converged_start_count": int(
                    selected["converged_start_count"]
                ),
            }
        )
    else:
        row.update(
            {
                "c1q_selected_source": None,
                "c1q_fit_success": False,
                "c1q_fitted_chi": None,
                "c1q_signed_chi_error": None,
                "c1q_abs_chi_error": None,
                "c1q_fitted_g": None,
                "c1q_signed_g_error": None,
                "c1q_abs_g_error": None,
                "c1q_fitted_natural_frequency_hz": None,
                "c1q_abs_natural_frequency_error_hz": None,
                "c1q_raw_box_min_distance": None,
                "c1q_converged_start_count": 0,
            }
        )

    if recurrence.get("status") == "ESTIMATED":
        row.update(
            {
                "recurrence_fitted_chi": float(recurrence["chi"]),
                "recurrence_abs_chi_error": float(
                    abs(recurrence["chi"] - chi)
                ),
                "recurrence_abs_natural_frequency_error_hz": float(
                    abs(recurrence["natural_frequency_hz"] - fn)
                ),
            }
        )
    else:
        row.update(
            {
                "recurrence_fitted_chi": None,
                "recurrence_abs_chi_error": None,
                "recurrence_abs_natural_frequency_error_hz": None,
            }
        )

    if (
        row["c1q_fitted_chi"] is not None
        and row["recurrence_fitted_chi"] is not None
    ):
        row["c1q_recurrence_chi_disagreement"] = float(
            abs(row["c1q_fitted_chi"] - row["recurrence_fitted_chi"])
        )
    else:
        row["c1q_recurrence_chi_disagreement"] = None

    return row


def pair_summary(
    cell: tuple[int, float, float, float, float],
    seed: int,
    fine_row: dict[str, Any],
    coarse_row: dict[str, Any],
) -> dict[str, Any]:
    index, A, fn, chi, g = cell

    def absdiff(key: str) -> float | None:
        x = fine_row.get(key)
        y = coarse_row.get(key)
        if x is None or y is None:
            return None
        return float(abs(float(x) - float(y)))

    return {
        "cell_index": index,
        "seed": seed,
        "truth_A": A,
        "truth_natural_frequency_hz": fn,
        "truth_chi": chi,
        "truth_g": g,
        "c1q_practical_rate_chi_drift": absdiff("c1q_fitted_chi"),
        "c1q_practical_rate_g_drift": absdiff("c1q_fitted_g"),
        "c1q_practical_rate_fn_drift_hz": absdiff(
            "c1q_fitted_natural_frequency_hz"
        ),
        "recurrence_practical_rate_chi_drift": absdiff(
            "recurrence_fitted_chi"
        ),
        "fine_c1q_success": bool(fine_row.get("c1q_fit_success")),
        "coarse_c1q_success": bool(coarse_row.get("c1q_fit_success")),
        "fine_recurrence_status": fine_row["recurrence"]["status"],
        "coarse_recurrence_status": coarse_row["recurrence"]["status"],
    }


def cell_subset(mode: str, shard: int | None) -> list[tuple[int, float, float, float, float]]:
    if mode == "preflight":
        return [cell for cell in CELLS if cell[0] in PREFLIGHT_CELLS]
    if mode == "full":
        if shard is None or shard not in {0, 1, 2, 3}:
            raise ValueError("full mode requires --shard 0..3")
        start = shard * 4
        return CELLS[start : start + 4]
    raise ValueError(mode)


def run_map(mode: str, shard: int | None, output_dir: Path) -> dict[str, Any]:
    cells = cell_subset(mode, shard)
    seeds = [SEEDS[0]] if mode == "preflight" else SEEDS

    rows = []
    pairs = []
    truth_audit = []

    for cell in cells:
        index, A, fn, chi, g = cell
        for seed in seeds:
            truth = construct_truth(
                fs=FINE_FS,
                A=A,
                natural_frequency_hz=fn,
                zeta=chi,
                g=g,
            )
            checks = truth_checks(truth, DECIMATION)
            truth_audit.append(
                {
                    "cell_index": index,
                    "seed": seed,
                    **checks,
                }
            )
            if checks["Qc_min_eigenvalue"] < -1e-8:
                raise RuntimeError(
                    f"mechanical truth defect: cell {index} Qc not PSD"
                )
            if checks["Qd_min_eigenvalue"] < -1e-8:
                raise RuntimeError(
                    f"mechanical truth defect: cell {index} Qd not PSD"
                )
            if not checks["alias_safe_factor_m"]:
                raise RuntimeError(
                    f"frozen design violates alias safety at cell {index}"
                )

            fine = simulate_same_path(truth, seconds=SECONDS, seed=seed)
            coarse = fine[::DECIMATION]
            if fine.size != int(round(SECONDS * FINE_FS)):
                raise RuntimeError("fine sample count does not match frozen design")
            if coarse.size != math.ceil(fine.size / DECIMATION):
                raise RuntimeError("coarse sample count does not match exact decimation")

            fine_row = rate_row(
                cell=cell,
                seed=seed,
                rate_label="fine",
                signal=fine,
                fs=FINE_FS,
                truth=truth,
            )
            coarse_row = rate_row(
                cell=cell,
                seed=seed,
                rate_label="coarse",
                signal=coarse,
                fs=FINE_FS / DECIMATION,
                truth=truth,
            )
            rows.extend([fine_row, coarse_row])
            pairs.append(pair_summary(cell, seed, fine_row, coarse_row))

    payload = {
        "status": "P0D_FUNCTION_MAP_PREFLIGHT" if mode == "preflight" else "P0D_FUNCTION_MAP_SHARD",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "promotes_c1q": False,
        "biological_prevalence_claim": False,
        "mode": mode,
        "shard": shard,
        "environment": environment_record(),
        "design": {
            "fine_sampling_rate_hz": FINE_FS,
            "decimation": DECIMATION,
            "coarse_sampling_rate_hz": FINE_FS / DECIMATION,
            "seconds": SECONDS,
            "seeds": seeds,
            "cells": [list(cell) for cell in cells],
            "primary_optimizer_maxiter": PRIMARY_MAXITER,
            "primary_max_optimized_starts": PRIMARY_MAX_STARTS,
            "rescue_optimizer_maxiter": RESCUE_MAXITER,
            "rescue_max_optimized_starts": RESCUE_MAX_STARTS,
        },
        "truth_audit": truth_audit,
        "rows": rows,
        "pairs": pairs,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = "preflight" if mode == "preflight" else f"shard_{shard}"
    json_path = output_dir / f"bio_chi_c_function_map_{suffix}.json"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    csv_path = output_dir / f"bio_chi_c_function_map_{suffix}.csv"
    flat_fields = [
        "cell_index",
        "seed",
        "rate_label",
        "sampling_rate_hz",
        "sample_count",
        "truth_A",
        "truth_natural_frequency_hz",
        "truth_chi",
        "truth_g",
        "c1q_fit_success",
        "c1q_fitted_chi",
        "c1q_abs_chi_error",
        "c1q_fitted_g",
        "c1q_abs_g_error",
        "c1q_fitted_natural_frequency_hz",
        "c1q_abs_natural_frequency_error_hz",
        "c1q_raw_box_min_distance",
        "c1q_converged_start_count",
        "recurrence_fitted_chi",
        "recurrence_abs_chi_error",
        "recurrence_abs_natural_frequency_error_hz",
        "c1q_recurrence_chi_disagreement",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=flat_fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in flat_fields})

    print(
        json.dumps(
            {
                "status": payload["status"],
                "json": str(json_path),
                "csv": str(csv_path),
                "row_count": len(rows),
                "pair_count": len(pairs),
            },
            sort_keys=True,
        )
    )
    return payload


def finite(values):
    return [float(v) for v in values if v is not None and math.isfinite(float(v))]


def stats(values) -> dict[str, Any]:
    x = finite(values)
    if not x:
        return {"count": 0, "min": None, "median": None, "max": None}
    arr = np.asarray(x, dtype=float)
    return {
        "count": int(arr.size),
        "min": float(np.min(arr)),
        "median": float(np.median(arr)),
        "max": float(np.max(arr)),
    }


def merge_results(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    files = sorted(input_dir.rglob("bio_chi_c_function_map_shard_*.json"))
    if len(files) != 4:
        raise RuntimeError(f"expected four shard JSON files, found {len(files)}")

    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    rows = [row for payload in payloads for row in payload["rows"]]
    pairs = [row for payload in payloads for row in payload["pairs"]]
    truth_audit = [row for payload in payloads for row in payload["truth_audit"]]

    observed_cells = sorted({int(row["cell_index"]) for row in rows})
    observed_seeds = sorted({int(row["seed"]) for row in rows})
    if observed_cells != list(range(16)):
        raise RuntimeError(f"design identity mismatch: cells {observed_cells}")
    if observed_seeds != SEEDS:
        raise RuntimeError(f"design identity mismatch: seeds {observed_seeds}")
    if len(rows) != 16 * len(SEEDS) * 2:
        raise RuntimeError(f"unexpected row count {len(rows)}")
    if len(pairs) != 16 * len(SEEDS):
        raise RuntimeError(f"unexpected pair count {len(pairs)}")

    summary = {
        "c1q_abs_chi_error": stats(row.get("c1q_abs_chi_error") for row in rows),
        "c1q_abs_g_error": stats(row.get("c1q_abs_g_error") for row in rows),
        "c1q_abs_natural_frequency_error_hz": stats(
            row.get("c1q_abs_natural_frequency_error_hz") for row in rows
        ),
        "recurrence_abs_chi_error": stats(
            row.get("recurrence_abs_chi_error") for row in rows
        ),
        "c1q_recurrence_chi_disagreement": stats(
            row.get("c1q_recurrence_chi_disagreement") for row in rows
        ),
        "c1q_practical_rate_chi_drift": stats(
            row.get("c1q_practical_rate_chi_drift") for row in pairs
        ),
        "c1q_practical_rate_g_drift": stats(
            row.get("c1q_practical_rate_g_drift") for row in pairs
        ),
        "recurrence_practical_rate_chi_drift": stats(
            row.get("recurrence_practical_rate_chi_drift") for row in pairs
        ),
        "c1q_success_count": int(sum(bool(row.get("c1q_fit_success")) for row in rows)),
        "c1q_total_fit_count": len(rows),
        "recurrence_estimated_count": int(
            sum(row["recurrence"]["status"] == "ESTIMATED" for row in rows)
        ),
        "recurrence_total_count": len(rows),
        "optimizer_unresolved_rows": [
            {
                "cell_index": row["cell_index"],
                "seed": row["seed"],
                "rate_label": row["rate_label"],
            }
            for row in rows
            if not row.get("c1q_fit_success")
        ],
        "recurrence_refusals": [
            {
                "cell_index": row["cell_index"],
                "seed": row["seed"],
                "rate_label": row["rate_label"],
                "status": row["recurrence"]["status"],
            }
            for row in rows
            if row["recurrence"]["status"] != "ESTIMATED"
        ],
    }

    merged = {
        "status": "P0D_FUNCTION_MAP_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "promotes_c1q": False,
        "biological_prevalence_claim": False,
        "source_files": [str(path) for path in files],
        "environment_records": [p["environment"] for p in payloads],
        "rows": rows,
        "pairs": pairs,
        "truth_audit": truth_audit,
        "summary": summary,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "bio_chi_c_function_map_complete.json"
    out.write_text(json.dumps(merged, indent=2, sort_keys=True), encoding="utf-8")

    md = output_dir / "bio_chi_c_function_map_summary.md"
    lines = [
        "# Bio Chi C-Interior Function Map Summary",
        "",
        "**Status:** P0-D exploratory correct-specification estimator map",
        "",
        "No scientific threshold is defined. No real-EEG local chi is licensed.",
        "",
        "## Full-envelope descriptive summaries",
        "",
    ]
    for key, value in summary.items():
        if isinstance(value, dict):
            lines.append(
                f"- **{key}:** count={value['count']}, min={value['min']}, "
                f"median={value['median']}, max={value['max']}"
            )
    lines.extend(
        [
            "",
            f"- **C1Q successful fits:** {summary['c1q_success_count']}/{summary['c1q_total_fit_count']}",
            f"- **Generic recurrence estimates:** {summary['recurrence_estimated_count']}/{summary['recurrence_total_count']}",
            "",
            "Interpretation remains bounded to the frozen synthetic qualification envelope.",
        ]
    )
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "status": merged["status"],
                "output": str(out),
                "summary": str(md),
                "row_count": len(rows),
                "pair_count": len(pairs),
            },
            sort_keys=True,
        )
    )
    return merged


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("preflight", "full", "merge"),
        required=True,
    )
    parser.add_argument("--shard", type=int)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.mode == "merge":
        if args.input_dir is None:
            raise ValueError("merge mode requires --input-dir")
        merge_results(args.input_dir, args.output_dir)
    else:
        run_map(args.mode, args.shard, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
