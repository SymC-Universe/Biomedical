#!/usr/bin/env python3
"""C1Q likelihood-basin root-cause diagnostic.

GOM v1.0 / APQ-1 frozen P0-Q execution.

For all rows in the eight Function Map boundary-collapse cells, this tool:
- regenerates the exact frozen known-truth realization;
- evaluates C1Q NLL at the population generating coordinates;
- reproduces NLL at the immutable selected raw coordinates from the source artifact;
- locally optimizes once from truth;
- locally polishes once from the selected solution;
- records continuous likelihood and parameter displacements.

No estimator is modified and no scientific admission threshold is defined.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize

from nsd_engine.continuous_lineage_candidate import _nll, _steady_state
from nsd_engine.state_space_adequacy import (
    _raw_fraction,
    _raw_frequency,
    _raw_rho,
)
from probe_continuous_lineage_nonzero_g import construct_truth, simulate_same_path


BOUNDARY_CELLS = (0, 5, 7, 8, 9, 11, 12, 15)
SOURCE_RUN = 36368579380
SOURCE_ARTIFACT_ID = 10948327278
SOURCE_DIGEST = (
    "sha256:cb4ceade9271c80a5b002f0b9f6ba791ae3e0ae049b64ede0a3fdb0aee2b5a0c"
)
SOURCE_HEAD = "45f74d8e3e8d027ab8b4bbb8572b81af0f00f55b"
FINE_FS = 256.0
DECIMATION = 2
SECONDS = 60.0
FMIN = 1.0
FMAX = 45.0
BURN = 128
LOCAL_MAXITER = 200
MECHANICAL_REL_TOL = 1e-6


def truth_raw(A: float, fn_hz: float, chi: float, g: float, fs: float) -> np.ndarray:
    omega_n = 2.0 * math.pi * fn_hz
    alpha = chi * omega_n
    nu = omega_n * math.sqrt(max(0.0, 1.0 - chi * chi))
    rho = math.exp(-alpha / fs)
    fd_hz = nu / (2.0 * math.pi)
    return np.asarray(
        [
            _raw_fraction(A),
            _raw_rho(rho),
            _raw_frequency(fd_hz, FMIN, FMAX),
            float(np.arctanh(np.clip(g, -0.999999999, 0.999999999))),
        ],
        dtype=np.float64,
    )


def standardize(signal: np.ndarray) -> np.ndarray:
    values = np.asarray(signal, dtype=np.float64)
    mean = float(np.mean(values))
    sd = float(np.std(values))
    if not math.isfinite(sd) or sd <= 0.0:
        raise ValueError("signal has zero or non-finite standard deviation")
    return (values - mean) / sd


def evaluate_nll(standardized: np.ndarray, raw: np.ndarray, fs: float) -> float:
    return float(_nll(standardized, raw, fs, FMIN, FMAX, BURN))


def local_optimize(standardized: np.ndarray, start: np.ndarray, fs: float) -> dict[str, Any]:
    result = minimize(
        lambda raw: _nll(
            standardized,
            raw,
            fs,
            FMIN,
            FMAX,
            BURN,
        ),
        np.asarray(start, dtype=np.float64),
        method="L-BFGS-B",
        bounds=[(-8.0, 8.0)] * 4,
        options={"maxiter": LOCAL_MAXITER, "ftol": 1e-10, "maxls": 50},
    )
    raw = np.asarray(result.x, dtype=np.float64)
    steady = _steady_state(raw, fs, FMIN, FMAX)
    parameters = None if steady is None else {k: float(v) for k, v in steady[3].items()}
    return {
        "success": bool(result.success),
        "message": str(result.message),
        "nit": int(getattr(result, "nit", -1)),
        "nfev": int(getattr(result, "nfev", -1)),
        "nll": float(result.fun),
        "raw_parameters": [float(v) for v in raw],
        "raw_box_min_distance": float(min(8.0 - abs(float(v)) for v in raw)),
        "parameters": parameters,
    }


def source_selected(row: dict[str, Any]) -> dict[str, Any]:
    key = row["c1q_selected_source"]
    selected = row["c1q"][key]
    if selected.get("status") != "FIT_RETURNED":
        raise RuntimeError(
            f"source selected fit is not FIT_RETURNED for "
            f"cell={row['cell_index']} seed={row['seed']} rate={row['rate_label']}"
        )
    return selected


def physical_distance(a: dict[str, float] | None, b: dict[str, float] | None) -> dict[str, float | None]:
    if a is None or b is None:
        return {
            "chi_abs": None,
            "g_abs": None,
            "natural_frequency_hz_abs": None,
            "latent_fraction_abs": None,
        }
    return {
        "chi_abs": float(abs(a["damping_ratio"] - b["damping_ratio"])),
        "g_abs": float(abs(a["g"] - b["g"])),
        "natural_frequency_hz_abs": float(
            abs(a["natural_frequency_hz"] - b["natural_frequency_hz"])
        ),
        "latent_fraction_abs": float(abs(a["latent_fraction"] - b["latent_fraction"])),
    }


def truth_parameters(A: float, fn_hz: float, chi: float, g: float) -> dict[str, float]:
    return {
        "latent_fraction": float(A),
        "natural_frequency_hz": float(fn_hz),
        "damping_ratio": float(chi),
        "g": float(g),
    }


def diagnostic_row(
    source_row: dict[str, Any],
    signal: np.ndarray,
) -> dict[str, Any]:
    fs = float(source_row["sampling_rate_hz"])
    standardized = standardize(signal)

    truth = truth_raw(
        float(source_row["truth_A"]),
        float(source_row["truth_natural_frequency_hz"]),
        float(source_row["truth_chi"]),
        float(source_row["truth_g"]),
        fs,
    )
    selected = source_selected(source_row)
    selected_raw = np.asarray(selected["raw_parameters"], dtype=np.float64)
    artifact_nll = float(selected["negative_log_likelihood"])

    truth_nll = evaluate_nll(standardized, truth, fs)
    selected_eval_nll = evaluate_nll(standardized, selected_raw, fs)

    tolerance = MECHANICAL_REL_TOL * max(1.0, abs(artifact_nll))
    reproduction_error = abs(selected_eval_nll - artifact_nll)
    reproduction_pass = bool(reproduction_error <= tolerance)
    if not reproduction_pass:
        raise RuntimeError(
            "source NLL reproduction failure "
            f"cell={source_row['cell_index']} seed={source_row['seed']} "
            f"rate={source_row['rate_label']} artifact={artifact_nll} "
            f"recomputed={selected_eval_nll} error={reproduction_error} tol={tolerance}"
        )

    truth_seed = local_optimize(standardized, truth, fs)
    selected_polish = local_optimize(standardized, selected_raw, fs)

    truth_steady = _steady_state(truth, fs, FMIN, FMAX)
    truth_physical = (
        truth_parameters(
            float(source_row["truth_A"]),
            float(source_row["truth_natural_frequency_hz"]),
            float(source_row["truth_chi"]),
            float(source_row["truth_g"]),
        )
        if truth_steady is not None
        else None
    )
    selected_physical = {k: float(v) for k, v in selected["parameters"].items()}

    effective_n = int(signal.size - BURN)
    truth_seed_nll = float(truth_seed["nll"])
    selected_polish_nll = float(selected_polish["nll"])

    return {
        "cell_index": int(source_row["cell_index"]),
        "seed": int(source_row["seed"]),
        "rate_label": source_row["rate_label"],
        "sampling_rate_hz": fs,
        "sample_count": int(signal.size),
        "effective_sample_count": effective_n,
        "truth": {
            "A": float(source_row["truth_A"]),
            "natural_frequency_hz": float(source_row["truth_natural_frequency_hz"]),
            "chi": float(source_row["truth_chi"]),
            "g": float(source_row["truth_g"]),
            "raw_parameters": [float(v) for v in truth],
        },
        "source_selected": {
            "artifact_nll": artifact_nll,
            "recomputed_nll": selected_eval_nll,
            "reproduction_error": float(reproduction_error),
            "reproduction_tolerance": float(tolerance),
            "reproduction_pass": reproduction_pass,
            "raw_parameters": [float(v) for v in selected_raw],
            "raw_box_min_distance": float(selected["raw_box_min_distance"]),
            "parameters": selected_physical,
        },
        "truth_nll": truth_nll,
        "truth_seed_local": truth_seed,
        "selected_seed_polish": selected_polish,
        "nll_differences": {
            "selected_minus_truth": float(selected_eval_nll - truth_nll),
            "truth_seed_minus_truth": float(truth_seed_nll - truth_nll),
            "truth_seed_minus_selected": float(truth_seed_nll - selected_eval_nll),
            "selected_polish_minus_selected": float(
                selected_polish_nll - selected_eval_nll
            ),
            "selected_minus_truth_per_effective_sample": float(
                (selected_eval_nll - truth_nll) / effective_n
            ),
            "truth_seed_minus_selected_per_effective_sample": float(
                (truth_seed_nll - selected_eval_nll) / effective_n
            ),
        },
        "mechanical_direction_flags": {
            "selected_beats_truth": bool(selected_eval_nll < truth_nll - tolerance),
            "truth_seed_beats_source_selected": bool(
                truth_seed_nll < selected_eval_nll - tolerance
            ),
            "selected_polish_beats_source_selected": bool(
                selected_polish_nll < selected_eval_nll - tolerance
            ),
        },
        "raw_distances": {
            "truth_seed_to_truth_l2": float(
                np.linalg.norm(
                    np.asarray(truth_seed["raw_parameters"], dtype=float) - truth
                )
            ),
            "truth_seed_to_selected_l2": float(
                np.linalg.norm(
                    np.asarray(truth_seed["raw_parameters"], dtype=float)
                    - selected_raw
                )
            ),
            "selected_polish_to_selected_l2": float(
                np.linalg.norm(
                    np.asarray(selected_polish["raw_parameters"], dtype=float)
                    - selected_raw
                )
            ),
        },
        "physical_distances": {
            "truth_seed_to_truth": physical_distance(
                truth_seed.get("parameters"), truth_physical
            ),
            "truth_seed_to_selected": physical_distance(
                truth_seed.get("parameters"), selected_physical
            ),
            "selected_to_truth": physical_distance(
                selected_physical, truth_physical
            ),
        },
        "source_context": {
            "source_c1q_abs_chi_error": source_row.get("c1q_abs_chi_error"),
            "source_c1q_abs_g_error": source_row.get("c1q_abs_g_error"),
            "source_recurrence_status": source_row["recurrence"]["status"],
            "source_recurrence_fitted_chi": source_row.get(
                "recurrence_fitted_chi"
            ),
        },
    }


def run_cell(source_map: Path, cell_index: int, output_dir: Path) -> dict[str, Any]:
    source = json.loads(source_map.read_text(encoding="utf-8"))
    if source.get("status") != "P0D_FUNCTION_MAP_COMPLETE":
        raise RuntimeError("unexpected source artifact status")

    rows = [r for r in source["rows"] if int(r["cell_index"]) == cell_index]
    if cell_index not in BOUNDARY_CELLS:
        raise ValueError(f"cell {cell_index} not in frozen boundary-cell set")
    if len(rows) != 6:
        raise RuntimeError(f"expected six source rows for cell {cell_index}, got {len(rows)}")

    by_seed: dict[int, dict[str, dict[str, Any]]] = {}
    for row in rows:
        by_seed.setdefault(int(row["seed"]), {})[row["rate_label"]] = row

    output_rows = []
    for seed, rate_rows in sorted(by_seed.items()):
        fine_row = rate_rows["fine"]
        truth = construct_truth(
            fs=FINE_FS,
            A=float(fine_row["truth_A"]),
            natural_frequency_hz=float(fine_row["truth_natural_frequency_hz"]),
            zeta=float(fine_row["truth_chi"]),
            g=float(fine_row["truth_g"]),
        )
        fine = simulate_same_path(truth, seconds=SECONDS, seed=seed)
        coarse = fine[::DECIMATION]

        output_rows.append(diagnostic_row(fine_row, fine))
        output_rows.append(diagnostic_row(rate_rows["coarse"], coarse))

    payload = {
        "status": "P0Q_C1Q_LIKELIHOOD_BASIN_CELL_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "changes_estimator": False,
        "source_run": SOURCE_RUN,
        "source_artifact_id": SOURCE_ARTIFACT_ID,
        "source_digest": SOURCE_DIGEST,
        "source_head": SOURCE_HEAD,
        "cell_index": cell_index,
        "row_count": len(output_rows),
        "rows": output_rows,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"c1q_likelihood_basin_cell_{cell_index}.json"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    csv_path = output_dir / f"c1q_likelihood_basin_cell_{cell_index}.csv"
    fields = [
        "cell_index",
        "seed",
        "rate_label",
        "truth_chi",
        "truth_g",
        "source_selected_chi",
        "source_selected_g",
        "truth_nll",
        "source_selected_nll",
        "truth_seed_nll",
        "selected_polish_nll",
        "selected_minus_truth",
        "truth_seed_minus_selected",
        "selected_polish_minus_selected",
        "truth_seed_to_truth_raw_l2",
        "truth_seed_to_selected_raw_l2",
        "source_selected_raw_box_min_distance",
        "selected_beats_truth",
        "truth_seed_beats_source_selected",
        "selected_polish_beats_source_selected",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for r in output_rows:
            writer.writerow(
                {
                    "cell_index": r["cell_index"],
                    "seed": r["seed"],
                    "rate_label": r["rate_label"],
                    "truth_chi": r["truth"]["chi"],
                    "truth_g": r["truth"]["g"],
                    "source_selected_chi": r["source_selected"]["parameters"]["damping_ratio"],
                    "source_selected_g": r["source_selected"]["parameters"]["g"],
                    "truth_nll": r["truth_nll"],
                    "source_selected_nll": r["source_selected"]["recomputed_nll"],
                    "truth_seed_nll": r["truth_seed_local"]["nll"],
                    "selected_polish_nll": r["selected_seed_polish"]["nll"],
                    "selected_minus_truth": r["nll_differences"]["selected_minus_truth"],
                    "truth_seed_minus_selected": r["nll_differences"]["truth_seed_minus_selected"],
                    "selected_polish_minus_selected": r["nll_differences"]["selected_polish_minus_selected"],
                    "truth_seed_to_truth_raw_l2": r["raw_distances"]["truth_seed_to_truth_l2"],
                    "truth_seed_to_selected_raw_l2": r["raw_distances"]["truth_seed_to_selected_l2"],
                    "source_selected_raw_box_min_distance": r["source_selected"]["raw_box_min_distance"],
                    "selected_beats_truth": r["mechanical_direction_flags"]["selected_beats_truth"],
                    "truth_seed_beats_source_selected": r["mechanical_direction_flags"]["truth_seed_beats_source_selected"],
                    "selected_polish_beats_source_selected": r["mechanical_direction_flags"]["selected_polish_beats_source_selected"],
                }
            )

    print(json.dumps({"cell": cell_index, "rows": len(output_rows), "json": str(json_path)}, sort_keys=True))
    return payload


def finite_stats(values) -> dict[str, Any]:
    x = np.asarray([float(v) for v in values if v is not None and math.isfinite(float(v))])
    if x.size == 0:
        return {"count": 0, "min": None, "median": None, "max": None}
    return {
        "count": int(x.size),
        "min": float(np.min(x)),
        "median": float(np.median(x)),
        "max": float(np.max(x)),
    }


def merge(input_dir: Path, output_dir: Path) -> dict[str, Any]:
    files = sorted(input_dir.rglob("c1q_likelihood_basin_cell_*.json"))
    if len(files) != len(BOUNDARY_CELLS):
        raise RuntimeError(f"expected {len(BOUNDARY_CELLS)} cell JSON files, found {len(files)}")

    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    rows = [r for p in payloads for r in p["rows"]]
    if len(rows) != 48:
        raise RuntimeError(f"expected 48 rows, found {len(rows)}")
    cells = sorted({int(r["cell_index"]) for r in rows})
    if cells != list(BOUNDARY_CELLS):
        raise RuntimeError(f"cell identity mismatch: {cells}")

    summary = {
        "selected_minus_truth_nll": finite_stats(
            r["nll_differences"]["selected_minus_truth"] for r in rows
        ),
        "truth_seed_minus_selected_nll": finite_stats(
            r["nll_differences"]["truth_seed_minus_selected"] for r in rows
        ),
        "selected_polish_minus_selected_nll": finite_stats(
            r["nll_differences"]["selected_polish_minus_selected"] for r in rows
        ),
        "truth_seed_to_truth_raw_l2": finite_stats(
            r["raw_distances"]["truth_seed_to_truth_l2"] for r in rows
        ),
        "truth_seed_to_selected_raw_l2": finite_stats(
            r["raw_distances"]["truth_seed_to_selected_l2"] for r in rows
        ),
        "source_selected_raw_box_min_distance": finite_stats(
            r["source_selected"]["raw_box_min_distance"] for r in rows
        ),
        "source_reproduction_pass_count": int(
            sum(r["source_selected"]["reproduction_pass"] for r in rows)
        ),
        "selected_beats_truth_count": int(
            sum(r["mechanical_direction_flags"]["selected_beats_truth"] for r in rows)
        ),
        "truth_seed_beats_source_selected_count": int(
            sum(
                r["mechanical_direction_flags"]["truth_seed_beats_source_selected"]
                for r in rows
            )
        ),
        "selected_polish_beats_source_selected_count": int(
            sum(
                r["mechanical_direction_flags"]["selected_polish_beats_source_selected"]
                for r in rows
            )
        ),
        "row_count": len(rows),
    }

    # Full distributions by rate and cell, not only aggregate counts.
    by_rate = {}
    for rate in ("fine", "coarse"):
        rr = [r for r in rows if r["rate_label"] == rate]
        by_rate[rate] = {
            "selected_minus_truth_nll": finite_stats(
                r["nll_differences"]["selected_minus_truth"] for r in rr
            ),
            "truth_seed_minus_selected_nll": finite_stats(
                r["nll_differences"]["truth_seed_minus_selected"] for r in rr
            ),
            "truth_seed_beats_source_selected_count": int(
                sum(
                    r["mechanical_direction_flags"]["truth_seed_beats_source_selected"]
                    for r in rr
                )
            ),
            "row_count": len(rr),
        }

    by_cell = {}
    for cell in BOUNDARY_CELLS:
        rr = [r for r in rows if int(r["cell_index"]) == cell]
        by_cell[str(cell)] = {
            "selected_minus_truth_nll": finite_stats(
                r["nll_differences"]["selected_minus_truth"] for r in rr
            ),
            "truth_seed_minus_selected_nll": finite_stats(
                r["nll_differences"]["truth_seed_minus_selected"] for r in rr
            ),
            "truth_seed_beats_source_selected_count": int(
                sum(
                    r["mechanical_direction_flags"]["truth_seed_beats_source_selected"]
                    for r in rr
                )
            ),
            "row_count": len(rr),
        }

    merged = {
        "status": "P0Q_C1Q_LIKELIHOOD_BASIN_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "changes_estimator": False,
        "source_run": SOURCE_RUN,
        "source_artifact_id": SOURCE_ARTIFACT_ID,
        "source_digest": SOURCE_DIGEST,
        "source_head": SOURCE_HEAD,
        "rows": rows,
        "summary": summary,
        "by_rate": by_rate,
        "by_cell": by_cell,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "c1q_likelihood_basin_complete.json"
    out.write_text(json.dumps(merged, indent=2, sort_keys=True), encoding="utf-8")

    md = output_dir / "c1q_likelihood_basin_summary.md"
    lines = [
        "# C1Q Likelihood-Basin Root-Cause Summary",
        "",
        "**Status:** P0-Q exploratory root-cause diagnostic",
        "",
        "No estimator change, scientific threshold, biological prevalence claim, or real-EEG admission is defined.",
        "",
        f"- Source NLL reproduced: {summary['source_reproduction_pass_count']}/{summary['row_count']}",
        f"- Stored selected fit has lower NLL than population truth coordinates: {summary['selected_beats_truth_count']}/{summary['row_count']}",
        f"- Truth-seeded local basin beats stored selected solution: {summary['truth_seed_beats_source_selected_count']}/{summary['row_count']}",
        f"- Selected-seeded polish beats stored selected solution: {summary['selected_polish_beats_source_selected_count']}/{summary['row_count']}",
        "",
        "Continuous NLL and parameter-distance distributions are preserved in the JSON artifact; these counts use only the frozen mechanical numerical-comparison tolerance and are not scientific admission thresholds.",
    ]
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")

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
