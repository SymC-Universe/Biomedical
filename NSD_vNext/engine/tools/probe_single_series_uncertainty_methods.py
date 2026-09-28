#!/usr/bin/env python3
"""Single-series uncertainty method comparison for Bio Chi C1Q-RS.

Compares local Hessian curvature, chi profile likelihood, and fitted-model
parametric bootstrap against the completed repeated-realization known-truth
uncertainty map. P0-Q only. No confidence threshold, admission rule, production
promotion, semantic membership, biological prevalence, or real-EEG license.
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
from scipy.optimize import minimize

from nsd_engine.continuous_lineage_candidate import (
    _build_candidate,
    _fraction_from_raw,
    _frequency_from_raw,
    _nll,
    _raw_fraction,
    _raw_frequency,
    _raw_rho,
)
from nsd_engine.continuous_lineage_candidate_rs import (
    _recurrence_covariance_seed,
    fit_continuous_lineage_candidate_rs,
)
from nsd_engine.continuous_lineage_profile import physical_nll
from probe_continuous_lineage_nonzero_g import construct_truth, simulate_same_path


CELLS = {
    0: (0.808004818, 14.655366315, 0.508266046, 0.584395017),
    1: (0.287373873, 12.656497417, 0.230462532, -0.441439599),
    2: (0.503600127, 22.101059450, 0.757180555, 0.086737482),
    6: (0.292389809, 18.952085106, 0.496195269, -0.719590691),
}
OBSERVED_SEED = 989969
FINE_FS = 256.0
SECONDS = 60.0
BOOTSTRAP_SEEDS = list(range(700001, 700033))
CHI_BASE_GRID = np.linspace(0.05, 0.98, 61)
RAW_BOUND = 8.0
PROFILE_MAXITER = 80
BOOTSTRAP_MAXITER = 80
BOOTSTRAP_MAX_STARTS = 18


def environment_record() -> dict[str, Any]:
    import scipy
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_ref": os.environ.get("GITHUB_REF"),
    }


def standardize(signal: np.ndarray) -> np.ndarray:
    x = np.asarray(signal, dtype=float)
    sd = float(np.std(x))
    if not math.isfinite(sd) or sd <= 0:
        raise ValueError("invalid signal variance")
    return (x - float(np.mean(x))) / sd


def get_case_signal(cell_index: int, rate: str):
    A, fn, chi, g = CELLS[cell_index]
    truth = construct_truth(
        fs=FINE_FS,
        A=A,
        natural_frequency_hz=fn,
        zeta=chi,
        g=g,
    )
    fine = simulate_same_path(truth, seconds=SECONDS, seed=OBSERVED_SEED)
    if rate == "fine":
        return fine, FINE_FS, dict(A=A, fn=fn, chi=chi, g=g)
    if rate == "coarse":
        return fine[::2], FINE_FS / 2.0, dict(A=A, fn=fn, chi=chi, g=g)
    raise ValueError(rate)


def selected_rs(signal: np.ndarray, fs: float):
    return fit_continuous_lineage_candidate_rs(
        signal,
        fs,
        optimizer_maxiter=80,
        max_optimized_starts=18,
    )


def physical_vector_from_fit(fit) -> np.ndarray:
    p = fit.parameters
    return np.asarray(
        [
            p["latent_fraction"],
            p["natural_frequency_hz"],
            p["damping_ratio"],
            p["g"],
        ],
        dtype=float,
    )


def physical_objective(std: np.ndarray, fs: float, x: np.ndarray) -> float:
    A, fn, chi, g = [float(v) for v in x]
    try:
        return physical_nll(
            std,
            A=A,
            natural_frequency_hz=fn,
            chi=chi,
            g=g,
            sampling_rate_hz=fs,
            burn_in_samples=128,
        )
    except Exception:
        return 1e100


def hessian_diagnostic(std: np.ndarray, fs: float, fit) -> dict[str, Any]:
    x0 = physical_vector_from_fit(fit)
    steps = np.asarray(
        [
            max(1e-4, 1e-3 * abs(x0[0])),
            max(0.005, 1e-3 * abs(x0[1])),
            max(1e-4, 1e-3 * abs(x0[2])),
            1e-3,
        ],
        dtype=float,
    )
    # Keep central steps inside simple physical domains. The exact C1Q domain
    # is checked by the canonical physical wrapper at every evaluation.
    lower = np.asarray([1e-4, 0.01, 1e-4, -0.9999])
    upper = np.asarray([0.9999, 200.0, 0.9999, 0.9999])
    for i in range(4):
        allowed = min(x0[i] - lower[i], upper[i] - x0[i])
        if allowed <= 0:
            return {"status": "HESSIAN_REFUSED_BOUNDARY"}
        steps[i] = min(steps[i], 0.45 * allowed)
        if steps[i] <= 1e-10:
            return {"status": "HESSIAN_REFUSED_BOUNDARY"}

    f0 = physical_objective(std, fs, x0)
    if not math.isfinite(f0) or f0 >= 1e90:
        return {"status": "HESSIAN_REFUSED_INVALID_OPTIMUM"}

    n = 4
    H = np.empty((n, n), dtype=float)
    for i in range(n):
        ei = np.zeros(n); ei[i] = steps[i]
        fp = physical_objective(std, fs, x0 + ei)
        fm = physical_objective(std, fs, x0 - ei)
        if max(fp, fm) >= 1e90:
            return {"status": "HESSIAN_REFUSED_STEP_INVALID", "dimension": i}
        H[i, i] = (fp - 2.0 * f0 + fm) / (steps[i] ** 2)
        for j in range(i):
            ej = np.zeros(n); ej[j] = steps[j]
            fpp = physical_objective(std, fs, x0 + ei + ej)
            fpm = physical_objective(std, fs, x0 + ei - ej)
            fmp = physical_objective(std, fs, x0 - ei + ej)
            fmm = physical_objective(std, fs, x0 - ei - ej)
            if max(fpp, fpm, fmp, fmm) >= 1e90:
                return {
                    "status": "HESSIAN_REFUSED_CROSS_STEP_INVALID",
                    "dimensions": [i, j],
                }
            value = (fpp - fpm - fmp + fmm) / (4.0 * steps[i] * steps[j])
            H[i, j] = H[j, i] = value

    eig = np.linalg.eigvalsh(H)
    result = {
        "status": "HESSIAN_COMPUTED",
        "coordinate_order": ["A", "natural_frequency_hz", "chi", "g"],
        "steps": steps.tolist(),
        "hessian": H.tolist(),
        "eigenvalues": eig.tolist(),
        "condition_number": float(np.linalg.cond(H)),
        "positive_definite": bool(np.all(eig > 0)),
    }
    if np.all(eig > 0):
        cov = np.linalg.inv(H)
        result["inverse_hessian_covariance"] = cov.tolist()
        result["local_chi_standard_error"] = float(math.sqrt(max(cov[2, 2], 0.0)))
    else:
        result["inverse_hessian_covariance"] = None
        result["local_chi_standard_error"] = None
    return result


def raw_profile_from_nuisance(
    nuisance: np.ndarray,
    chi: float,
    fs: float,
) -> np.ndarray | None:
    raw_A, raw_fd, raw_g = [float(v) for v in nuisance]
    try:
        fd = _frequency_from_raw(raw_fd, 1.0, 45.0)
        nu = 2.0 * math.pi * fd
        alpha = nu * chi / math.sqrt(1.0 - chi * chi)
        rho = math.exp(-alpha / fs)
        raw_rho = _raw_rho(rho)
    except Exception:
        return None
    raw = np.asarray([raw_A, raw_rho, raw_fd, raw_g], dtype=float)
    if not np.isfinite(raw).all() or np.any(raw < -RAW_BOUND) or np.any(raw > RAW_BOUND):
        return None
    return raw


def profile_nll(std: np.ndarray, fs: float, chi: float, nuisance: np.ndarray) -> float:
    raw = raw_profile_from_nuisance(nuisance, chi, fs)
    if raw is None:
        return 1e100
    return _nll(std, raw, fs, 1.0, 45.0, 128)


def nuisance_from_physical(A: float, fn: float, chi: float, g: float):
    fd = fn * math.sqrt(max(1e-12, 1.0 - chi * chi))
    try:
        return np.asarray(
            [
                _raw_fraction(A),
                _raw_frequency(fd, 1.0, 45.0),
                float(np.arctanh(np.clip(g, -0.999999, 0.999999))),
            ],
            dtype=float,
        )
    except Exception:
        return None


def nuisance_physical(nuisance: np.ndarray, chi: float, fs: float) -> dict[str, float] | None:
    raw = raw_profile_from_nuisance(nuisance, chi, fs)
    if raw is None:
        return None
    try:
        _, _, _, _, p = _build_candidate(raw, fs, 1.0, 45.0)
        return {k: float(v) for k, v in p.items()}
    except Exception:
        return None


def profile_starts(std: np.ndarray, fs: float, fit, chi: float, previous):
    p = fit.parameters
    starts = []
    if previous is not None:
        starts.append(("continuation", np.asarray(previous, dtype=float)))

    global_start = nuisance_from_physical(
        p["latent_fraction"], p["natural_frequency_hz"], chi, p["g"]
    )
    if global_start is not None:
        starts.append(("global_projected", global_start))

    rec = _recurrence_covariance_seed(std, fs, 1.0, 45.0)
    if rec.get("status") == "SEED_READY":
        rr = np.asarray(rec["raw_parameters"], dtype=float)
        starts.append(("recurrence", rr[[0, 2, 3]]))

    fn0 = float(p["natural_frequency_hz"])
    fixed = [
        (0.25, max(1.2, 0.75 * fn0), -0.6),
        (0.25, fn0, 0.6),
        (0.55, max(1.2, 0.75 * fn0), 0.0),
        (0.55, min(44.0, 1.25 * fn0), -0.6),
        (0.85, fn0, 0.6),
        (0.85, min(44.0, 1.25 * fn0), 0.0),
    ]
    for i, (A, fn, g) in enumerate(fixed):
        s = nuisance_from_physical(A, fn, chi, g)
        if s is not None and np.all(np.abs(s) <= 8.0):
            starts.append((f"fixed_{i}", s))

    # Deduplicate near-identical starts without outcome knowledge.
    unique = []
    for origin, s in starts:
        if not any(np.max(np.abs(s - u[1])) < 1e-10 for u in unique):
            unique.append((origin, s))
    return unique


def profile_case(signal: np.ndarray, fs: float, fit, truth_chi: float):
    std = standardize(signal)
    fitted_chi = float(fit.parameters["damping_ratio"])
    grid = sorted(set([float(x) for x in CHI_BASE_GRID] + [fitted_chi, float(truth_chi)]))

    # Evaluate outward from the nearest fitted-chi grid point so continuation
    # is local in both directions.
    center = min(range(len(grid)), key=lambda i: abs(grid[i] - fitted_chi))
    order = [center]
    for distance in range(1, len(grid)):
        lo = center - distance
        hi = center + distance
        if lo >= 0:
            order.append(lo)
        if hi < len(grid):
            order.append(hi)
        if len(order) >= len(grid):
            break

    results = {}
    prev_by_direction = {"low": None, "high": None, "center": None}
    for idx in order:
        chi = grid[idx]
        direction = "center" if idx == center else ("low" if idx < center else "high")
        previous = prev_by_direction[direction]
        starts = profile_starts(std, fs, fit, chi, previous)
        solutions = []
        for origin, start in starts:
            res = minimize(
                lambda x: profile_nll(std, fs, chi, x),
                start,
                method="L-BFGS-B",
                bounds=[(-8.0, 8.0)] * 3,
                options={"maxiter": PROFILE_MAXITER, "ftol": 1e-8, "maxls": 30},
            )
            if math.isfinite(float(res.fun)) and float(res.fun) < 1e90:
                solutions.append((origin, res))
        if not solutions:
            results[idx] = {
                "chi": chi,
                "status": "NO_FINITE_PROFILE_SOLUTION",
                "nll": None,
            }
            continue
        origin, best = min(solutions, key=lambda t: float(t[1].fun))
        bestx = np.asarray(best.x, dtype=float)
        prev_by_direction[direction] = bestx
        results[idx] = {
            "chi": chi,
            "status": "PROFILED",
            "nll": float(best.fun),
            "winning_start": origin,
            "nuisance_raw": bestx.tolist(),
            "nuisance_physical": nuisance_physical(bestx, chi, fs),
            "start_count": len(starts),
            "converged_count": int(sum(bool(x.success) for _, x in solutions)),
        }

    points = [results[i] for i in range(len(grid))]
    global_nll = float(fit.negative_log_likelihood)
    finite = [p for p in points if p["nll"] is not None]
    for p in points:
        p["delta_nll"] = (
            float(p["nll"] - global_nll) if p["nll"] is not None else None
        )

    def exact_point(target):
        return min(points, key=lambda p: abs(p["chi"] - target))

    fitpoint = exact_point(fitted_chi)
    truthpoint = exact_point(truth_chi)
    mech_tol = 1e-5 * max(1.0, abs(global_nll))
    fit_reproduces = bool(
        fitpoint["nll"] is not None
        and abs(float(fitpoint["nll"]) - global_nll) <= mech_tol
    )
    if not fit_reproduces:
        raise RuntimeError(
            f"fitted-chi profile point failed global-NLL reproduction: "
            f"profile={fitpoint['nll']} global={global_nll}"
        )

    nlls = np.asarray(
        [float(p["nll"]) if p["nll"] is not None else np.nan for p in points]
    )
    minima = []
    for i in range(1, len(points) - 1):
        if np.isfinite(nlls[i-1:i+2]).all() and nlls[i] <= nlls[i-1] and nlls[i] <= nlls[i+1]:
            minima.append({"chi": points[i]["chi"], "delta_nll": points[i]["delta_nll"]})

    return {
        "global_nll": global_nll,
        "fitted_chi": fitted_chi,
        "truth_chi": truth_chi,
        "fitted_chi_profile_reproduces_global": fit_reproduces,
        "fitted_chi_profile_delta_nll": fitpoint["delta_nll"],
        "truth_chi_profile_delta_nll": truthpoint["delta_nll"],
        "profile_points": points,
        "local_minima": minima,
        "left_edge_delta_nll": points[0]["delta_nll"],
        "right_edge_delta_nll": points[-1]["delta_nll"],
        "finite_point_count": len(finite),
    }


def observed_case(cell: int, rate: str):
    signal, fs, truth = get_case_signal(cell, rate)
    fit = selected_rs(signal, fs)
    std = standardize(signal)
    return signal, fs, truth, fit, std


def run_profile_case(cell: int, rate: str, outdir: Path):
    signal, fs, truth, fit, std = observed_case(cell, rate)
    payload = {
        "status": "P0Q_SINGLE_SERIES_PROFILE_CASE_COMPLETE",
        "cell": cell,
        "rate": rate,
        "fs": fs,
        "truth": truth,
        "observed_seed": OBSERVED_SEED,
        "fit": {
            "nll": float(fit.negative_log_likelihood),
            "parameters": {k: float(v) for k, v in fit.parameters.items()},
            "raw_parameters": [float(v) for v in fit.raw_parameters],
            "winning_start_origin": fit.winning_start_origin,
        },
        "hessian": hessian_diagnostic(std, fs, fit),
        "profile": profile_case(signal, fs, fit, truth["chi"]),
        "environment": environment_record(),
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"uncertainty_profile_cell_{cell}_{rate}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(out), "cell": cell, "rate": rate}, sort_keys=True))


def run_bootstrap_chunk(cell: int, rate: str, chunk: int, outdir: Path):
    signal, fs, truth, fit, _ = observed_case(cell, rate)
    start = chunk * 8
    seeds = BOOTSTRAP_SEEDS[start:start+8]
    if len(seeds) != 8:
        raise ValueError("bootstrap chunk must contain 8 frozen seeds")

    p = fit.parameters
    bootstrap_truth = construct_truth(
        fs=fs,
        A=float(p["latent_fraction"]),
        natural_frequency_hz=float(p["natural_frequency_hz"]),
        zeta=float(p["damping_ratio"]),
        g=float(p["g"]),
    )
    rows = []
    for seed in seeds:
        sim = simulate_same_path(bootstrap_truth, seconds=SECONDS, seed=seed)
        bfit = fit_continuous_lineage_candidate_rs(
            sim,
            fs,
            optimizer_maxiter=BOOTSTRAP_MAXITER,
            max_optimized_starts=BOOTSTRAP_MAX_STARTS,
        )
        bp = bfit.parameters
        rows.append({
            "seed": seed,
            "fitted_chi": float(bp["damping_ratio"]),
            "fitted_g": float(bp["g"]),
            "fitted_natural_frequency_hz": float(bp["natural_frequency_hz"]),
            "delta_chi_from_observed_fit": float(bp["damping_ratio"] - p["damping_ratio"]),
            "delta_g_from_observed_fit": float(bp["g"] - p["g"]),
            "delta_fn_from_observed_fit_hz": float(bp["natural_frequency_hz"] - p["natural_frequency_hz"]),
            "winning_start_origin": bfit.winning_start_origin,
            "success": bool(bfit.success),
        })
    payload = {
        "status": "P0Q_SINGLE_SERIES_BOOTSTRAP_CHUNK_COMPLETE",
        "cell": cell,
        "rate": rate,
        "chunk": chunk,
        "fs": fs,
        "truth": truth,
        "observed_fit": {k: float(v) for k, v in p.items()},
        "rows": rows,
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"bootstrap_cell_{cell}_{rate}_chunk_{chunk}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(out), "rows": len(rows)}, sort_keys=True))


def dist(vals):
    x = np.asarray([float(v) for v in vals], dtype=float)
    med = float(np.median(x))
    return {
        "count": int(x.size),
        "mean": float(np.mean(x)),
        "std": float(np.std(x, ddof=1)) if x.size > 1 else 0.0,
        "median": med,
        "mad": float(np.median(np.abs(x-med))),
        "q25": float(np.quantile(x, 0.25)),
        "q75": float(np.quantile(x, 0.75)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
    }


def merge(profile_dir: Path, bootstrap_dir: Path, source_uncertainty: Path, outdir: Path):
    profile_files = sorted(profile_dir.rglob("uncertainty_profile_cell_*_*.json"))
    boot_files = sorted(bootstrap_dir.rglob("bootstrap_cell_*_chunk_*.json"))
    if len(profile_files) != 8:
        raise RuntimeError(f"expected 8 profile files, found {len(profile_files)}")
    if len(boot_files) != 32:
        raise RuntimeError(f"expected 32 bootstrap chunk files, found {len(boot_files)}")

    profiles = [json.loads(p.read_text()) for p in profile_files]
    boots = [json.loads(p.read_text()) for p in boot_files]
    source = json.loads(source_uncertainty.read_text())
    source_rows = source["rows"]

    cases = {}
    for p in profiles:
        key = f"{p['cell']}:{p['rate']}"
        brows = [
            r
            for b in boots
            if b["cell"] == p["cell"] and b["rate"] == p["rate"]
            for r in b["rows"]
        ]
        if len(brows) != 32:
            raise RuntimeError(f"case {key} expected 32 bootstrap rows, found {len(brows)}")
        truth_rows = [
            r for r in source_rows
            if r["cell_index"] == p["cell"] and r["rate_label"] == p["rate"]
        ]
        if len(truth_rows) != 12:
            raise RuntimeError(f"case {key} expected 12 source rows, found {len(truth_rows)}")
        cases[key] = {
            "profile_hessian": p,
            "bootstrap": {
                "chi": dist(r["fitted_chi"] for r in brows),
                "g": dist(r["fitted_g"] for r in brows),
                "natural_frequency_hz": dist(r["fitted_natural_frequency_hz"] for r in brows),
                "rows": brows,
            },
            "known_truth_repeated_realizations": {
                "chi": dist(r["fitted_chi"] for r in truth_rows),
                "g": dist(r["fitted_g"] for r in truth_rows),
                "natural_frequency_hz": dist(r["fitted_natural_frequency_hz"] for r in truth_rows),
                "rows": truth_rows,
            },
        }

    result = {
        "status": "P0Q_SINGLE_SERIES_UNCERTAINTY_METHOD_COMPARISON_COMPLETE",
        "cases": cases,
        "licenses_real_eeg_local_chi": False,
        "defines_confidence_threshold": False,
        "defines_admission_threshold": False,
        "promotes_production_estimator": False,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "single_series_uncertainty_method_comparison.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(out), "case_count": len(cases)}, sort_keys=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["profile", "bootstrap", "merge"], required=True)
    ap.add_argument("--cell", type=int)
    ap.add_argument("--rate", choices=["fine", "coarse"])
    ap.add_argument("--chunk", type=int)
    ap.add_argument("--profile-dir", type=Path)
    ap.add_argument("--bootstrap-dir", type=Path)
    ap.add_argument("--source-uncertainty", type=Path)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    if args.mode == "profile":
        run_profile_case(args.cell, args.rate, args.output_dir)
    elif args.mode == "bootstrap":
        run_bootstrap_chunk(args.cell, args.rate, args.chunk, args.output_dir)
    else:
        if args.profile_dir is None or args.bootstrap_dir is None or args.source_uncertainty is None:
            raise ValueError("merge requires profile-dir, bootstrap-dir, and source-uncertainty")
        merge(args.profile_dir, args.bootstrap_dir, args.source_uncertainty, args.output_dir)


if __name__ == "__main__":
    main()
