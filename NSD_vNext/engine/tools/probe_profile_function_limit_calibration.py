#!/usr/bin/env python3
"""Profile Function/Limit calibration for Bio Chi.

P0-Q known-truth qualification only. This maps practical-identifiability
profile morphology across valid C truths and semantic Limit truths without
defining an admission threshold or inferring biological prevalence.
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
from probe_continuous_lineage_nonzero_g import construct_truth, simulate_same_path
from probe_combined_structural_predictive_refusal import (
    arma_second_order_signal,
    colored_process_signal,
    scalar_positive_bound,
    two_mode_signal,
)
from probe_single_series_uncertainty_methods import (
    hessian_diagnostic,
    profile_case,
    standardize,
)

FINE_FS = 256.0
SECONDS = 60.0
DECIMATION = 2
RAW_BOUND_TOL = 1e-6

SEEDS = [301103, 509203, 811223]

C_CASES = {
    "C0": dict(role="NOMINAL_FUNCTION", A=0.80, fn=10.0, chi=0.30, g=0.00),
    "C1": dict(role="NOMINAL_FUNCTION", A=0.65, fn=12.0, chi=0.45, g=0.55),
    "C2": dict(role="PERTURBED_FUNCTION", A=0.28, fn=19.0, chi=0.50, g=-0.72),
    "C3": dict(role="BOUNDARY_OR_TRANSITION", A=0.80, fn=10.0, chi=0.93, g=0.20),
    "C4": dict(role="BOUNDARY_OR_TRANSITION", A=0.80, fn=10.0, chi=0.30, g=0.95),
    "C5": dict(role="BOUNDARY_OR_TRANSITION", A=0.70, fn=42.0, chi=0.25, g=0.20),
}

LIMIT_CASES = {
    "L0": dict(role="BOUNDARY_OR_TRANSITION", generator="D_NOT_C_POS"),
    "L1": dict(role="BOUNDARY_OR_TRANSITION", generator="D_NOT_C_NEG"),
    "L2": dict(role="BOUNDARY_OR_TRANSITION", generator="S_NOT_D_POS"),
    "L3": dict(role="BOUNDARY_OR_TRANSITION", generator="S_NOT_D_NEG"),
    "L4": dict(role="BOUNDARY_OR_TRANSITION", generator="COLORED_MEMORY"),
    "L5": dict(role="BOUNDARY_OR_TRANSITION", generator="GENUINE_TWO_MODE"),
}

ALL_CASES = {**C_CASES, **LIMIT_CASES}


def environment_record() -> dict[str, Any]:
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "numpy_version": np.__version__,
        "scipy_version": scipy.__version__,
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_ref": os.environ.get("GITHUB_REF"),
    }


def limit_geometry():
    A = 0.8
    fn = 10.0
    zeta = 0.30
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / FINE_FS
    rho = math.exp(-L)
    theta = nu / FINE_FS
    xi = math.cos(theta)
    H_C = A * L * math.sin(theta) / theta
    H_D = A * math.sinh(L)
    S_pos = scalar_positive_bound(A, rho, xi, +1, H_D)
    S_neg = scalar_positive_bound(A, rho, xi, -1, H_D)
    return {
        "A": A,
        "fn": fn,
        "zeta": zeta,
        "rho": rho,
        "xi": xi,
        "H_D_not_C_pos": H_C + 0.5 * (H_D - H_C),
        "H_D_not_C_neg": -(H_C + 0.5 * (H_D - H_C)),
        "H_S_not_D_pos": 0.5 * (H_D + S_pos),
        "H_S_not_D_neg": 0.5 * (-H_D + S_neg),
    }


def generate_fine(truth_id: str, seed: int):
    if truth_id in C_CASES:
        c = C_CASES[truth_id]
        truth = construct_truth(
            fs=FINE_FS,
            A=c["A"],
            natural_frequency_hz=c["fn"],
            zeta=c["chi"],
            g=c["g"],
        )
        if 2.0 * truth["theta"] >= math.pi:
            raise RuntimeError(f"{truth_id} violates frozen alias-safe factor-2 condition")
        signal = simulate_same_path(truth, seconds=SECONDS, seed=seed)
        meta = {
            "generator": "CONTINUOUS_C",
            "semantic_C_member": True,
            "true_continuous_C_chi_defined": True,
            "truth_A": c["A"],
            "truth_natural_frequency_hz": c["fn"],
            "truth_chi": c["chi"],
            "truth_g": c["g"],
        }
        return signal, meta

    geom = limit_geometry()
    gen = LIMIT_CASES[truth_id]["generator"]
    if gen == "D_NOT_C_POS":
        signal = arma_second_order_signal(
            fs=FINE_FS, seconds=SECONDS, A=geom["A"], rho=geom["rho"],
            xi=geom["xi"], H=geom["H_D_not_C_pos"], seed=seed + 2000,
        )
    elif gen == "D_NOT_C_NEG":
        signal = arma_second_order_signal(
            fs=FINE_FS, seconds=SECONDS, A=geom["A"], rho=geom["rho"],
            xi=geom["xi"], H=geom["H_D_not_C_neg"], seed=seed + 3000,
        )
    elif gen == "S_NOT_D_POS":
        signal = arma_second_order_signal(
            fs=FINE_FS, seconds=SECONDS, A=geom["A"], rho=geom["rho"],
            xi=geom["xi"], H=geom["H_S_not_D_pos"], seed=seed + 4000,
        )
    elif gen == "S_NOT_D_NEG":
        signal = arma_second_order_signal(
            fs=FINE_FS, seconds=SECONDS, A=geom["A"], rho=geom["rho"],
            xi=geom["xi"], H=geom["H_S_not_D_neg"], seed=seed + 5000,
        )
    elif gen == "COLORED_MEMORY":
        signal = colored_process_signal(fs=FINE_FS, seconds=SECONDS, seed=seed)
    elif gen == "GENUINE_TWO_MODE":
        signal = two_mode_signal(fs=FINE_FS, seconds=SECONDS, seed=seed)
    else:
        raise ValueError(gen)

    meta = {
        "generator": gen,
        "semantic_C_member": False,
        "true_continuous_C_chi_defined": False,
        "truth_A": None,
        "truth_natural_frequency_hz": None,
        "truth_chi": None,
        "truth_g": None,
    }
    return signal, meta


def fit_rs(signal: np.ndarray, fs: float):
    return fit_continuous_lineage_candidate_rs(
        signal,
        fs,
        optimizer_maxiter=80,
        max_optimized_starts=18,
    )


def raw_edge_distance(raw) -> float:
    return float(min(8.0 - abs(float(v)) for v in raw))


def nuisance_boundary_contact_count(profile: dict[str, Any]) -> int:
    count = 0
    for p in profile["profile_points"]:
        raw = p.get("nuisance_raw")
        if raw is None:
            continue
        if min(8.0 - abs(float(v)) for v in raw) <= RAW_BOUND_TOL:
            count += 1
    return count


def profile_summary(profile: dict[str, Any]) -> dict[str, Any]:
    points = [p for p in profile["profile_points"] if p.get("nll") is not None]
    finite = [p for p in points if p.get("delta_nll") is not None]
    if not finite:
        return {
            "finite_profile_points": 0,
            "profile_delta_nll_range": None,
            "lowest_profile_chi": None,
            "lowest_profile_is_grid_edge": None,
            "nuisance_boundary_contact_count": 0,
        }
    best = min(finite, key=lambda p: float(p["nll"]))
    deltas = [float(p["delta_nll"]) for p in finite]
    chis = [float(p["chi"]) for p in profile["profile_points"]]
    low_edge = min(chis)
    high_edge = max(chis)
    return {
        "finite_profile_points": len(finite),
        "profile_delta_nll_range": float(max(deltas) - min(deltas)),
        "lowest_profile_chi": float(best["chi"]),
        "lowest_profile_is_grid_edge": bool(
            abs(float(best["chi"]) - low_edge) < 1e-12
            or abs(float(best["chi"]) - high_edge) < 1e-12
        ),
        "nuisance_boundary_contact_count": nuisance_boundary_contact_count(profile),
    }


def run_case(truth_id: str, seed: int, rate: str, outdir: Path):
    if truth_id not in ALL_CASES:
        raise ValueError(truth_id)
    if seed not in SEEDS:
        raise ValueError("seed not frozen")
    if rate not in {"fine", "coarse"}:
        raise ValueError(rate)

    fine, meta = generate_fine(truth_id, seed)
    if fine.size != int(round(FINE_FS * SECONDS)):
        raise RuntimeError("fine sample count mismatch")
    if rate == "fine":
        signal = fine
        fs = FINE_FS
    else:
        signal = fine[::DECIMATION]
        fs = FINE_FS / DECIMATION

    fit = fit_rs(signal, fs)
    std = standardize(signal)
    fit_chi = float(fit.parameters["damping_ratio"])
    true_chi_arg = (
        float(meta["truth_chi"])
        if meta["true_continuous_C_chi_defined"]
        else fit_chi
    )
    prof = profile_case(signal, fs, fit, true_chi_arg)
    if not meta["true_continuous_C_chi_defined"]:
        prof["truth_chi"] = None
        prof["truth_chi_profile_delta_nll"] = None

    hess = hessian_diagnostic(std, fs, fit)
    rdist = raw_edge_distance(fit.raw_parameters)

    payload = {
        "status": "P0Q_PROFILE_FUNCTION_LIMIT_CASE_COMPLETE",
        "truth_id": truth_id,
        "coverage_role": ALL_CASES[truth_id]["role"],
        "seed": seed,
        "rate": rate,
        "sampling_rate_hz": fs,
        "duration_seconds": SECONDS,
        **meta,
        "fit": {
            "negative_log_likelihood": float(fit.negative_log_likelihood),
            "bic": float(fit.bic),
            "parameters": {k: float(v) for k, v in fit.parameters.items()},
            "raw_parameters": [float(v) for v in fit.raw_parameters],
            "winning_start_origin": str(fit.winning_start_origin),
            "raw_box_edge_distance": rdist,
            "raw_boundary_flag": bool(rdist <= RAW_BOUND_TOL),
            "g_boundary_distance": float(1.0 - abs(fit.parameters["g"])),
        },
        "hessian": hess,
        "profile": prof,
        "profile_summary": profile_summary(prof),
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "establishes_C_membership_from_profile": False,
        "environment": environment_record(),
    }

    if meta["semantic_C_member"]:
        payload["recovery"] = {
            "signed_chi_error": float(fit.parameters["damping_ratio"] - meta["truth_chi"]),
            "abs_chi_error": float(abs(fit.parameters["damping_ratio"] - meta["truth_chi"])),
            "signed_g_error": float(fit.parameters["g"] - meta["truth_g"]),
            "abs_g_error": float(abs(fit.parameters["g"] - meta["truth_g"])),
            "signed_natural_frequency_error_hz": float(
                fit.parameters["natural_frequency_hz"] - meta["truth_natural_frequency_hz"]
            ),
            "abs_natural_frequency_error_hz": float(
                abs(fit.parameters["natural_frequency_hz"] - meta["truth_natural_frequency_hz"])
            ),
        }
    else:
        payload["recovery"] = {
            "signed_chi_error": "NOT_APPLICABLE",
            "abs_chi_error": "NOT_APPLICABLE",
            "signed_g_error": "NOT_APPLICABLE",
            "abs_g_error": "NOT_APPLICABLE",
            "signed_natural_frequency_error_hz": "NOT_APPLICABLE",
            "abs_natural_frequency_error_hz": "NOT_APPLICABLE",
        }

    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"profile_function_limit_{truth_id}_{seed}_{rate}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(out), "truth_id": truth_id, "seed": seed, "rate": rate}, sort_keys=True))


def merge(input_dir: Path, outdir: Path):
    files = sorted(input_dir.rglob("profile_function_limit_*.json"))
    if len(files) != 72:
        raise RuntimeError(f"expected 72 full case files, found {len(files)}")
    rows = [json.loads(p.read_text(encoding="utf-8")) for p in files]

    ids = sorted({r["truth_id"] for r in rows})
    if ids != sorted(ALL_CASES):
        raise RuntimeError(f"truth identity mismatch: {ids}")

    summary = {}
    for truth_id in sorted(ALL_CASES):
        rr = [r for r in rows if r["truth_id"] == truth_id]
        summary[truth_id] = {
            "row_count": len(rr),
            "semantic_C_member": bool(rr[0]["semantic_C_member"]),
            "coverage_role": rr[0]["coverage_role"],
            "hessian_status_counts": {},
            "edge_minimum_count": int(sum(r["profile_summary"]["lowest_profile_is_grid_edge"] for r in rr)),
            "raw_boundary_fit_count": int(sum(r["fit"]["raw_boundary_flag"] for r in rr)),
            "nuisance_boundary_contact_total": int(sum(r["profile_summary"]["nuisance_boundary_contact_count"] for r in rr)),
            "local_minima_counts": [len(r["profile"]["local_minima"]) for r in rr],
            "left_edge_delta_nll": [r["profile"]["left_edge_delta_nll"] for r in rr],
            "right_edge_delta_nll": [r["profile"]["right_edge_delta_nll"] for r in rr],
        }
        for r in rr:
            s = r["hessian"]["status"]
            summary[truth_id]["hessian_status_counts"][s] = summary[truth_id]["hessian_status_counts"].get(s, 0) + 1

    # Same-path fitted-chi drift.
    pairs = []
    for truth_id in sorted(ALL_CASES):
        for seed in SEEDS:
            fine = next(r for r in rows if r["truth_id"] == truth_id and r["seed"] == seed and r["rate"] == "fine")
            coarse = next(r for r in rows if r["truth_id"] == truth_id and r["seed"] == seed and r["rate"] == "coarse")
            pairs.append({
                "truth_id": truth_id,
                "seed": seed,
                "semantic_C_member": fine["semantic_C_member"],
                "fitted_chi_rate_drift": float(abs(fine["fit"]["parameters"]["damping_ratio"] - coarse["fit"]["parameters"]["damping_ratio"])),
            })

    result = {
        "status": "P0Q_PROFILE_FUNCTION_LIMIT_CALIBRATION_COMPLETE",
        "row_count": len(rows),
        "pair_count": len(pairs),
        "rows": rows,
        "pairs": pairs,
        "summary_by_truth": summary,
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "establishes_C_membership_from_profile": False,
        "biological_prevalence_claim": False,
    }

    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "profile_function_limit_calibration_complete.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"output": str(out), "rows": len(rows), "pairs": len(pairs)}, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("case", "merge"), required=True)
    parser.add_argument("--truth-id")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--rate", choices=("fine", "coarse"))
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    if args.mode == "case":
        if args.truth_id is None or args.seed is None or args.rate is None:
            raise ValueError("case mode requires truth-id, seed, and rate")
        run_case(args.truth_id, args.seed, args.rate, args.output_dir)
    else:
        if args.input_dir is None:
            raise ValueError("merge mode requires input-dir")
        merge(args.input_dir, args.output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
