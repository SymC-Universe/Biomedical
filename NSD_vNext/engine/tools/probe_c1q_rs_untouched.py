#!/usr/bin/env python3
"""Untouched C1Q-RS interior qualification.

Prospective P0-Q qualification using frozen new C-family coordinates and new
realization seeds. Compares unchanged legacy C1Q with C1Q-RS on the exact same
known-truth paths. No biological admission or scientific threshold is defined.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from nsd_engine.continuous_lineage_candidate import (
    fit_continuous_lineage_candidate,
)
from nsd_engine.continuous_lineage_candidate_rs import (
    fit_continuous_lineage_candidate_rs,
)
from probe_continuous_lineage_nonzero_g import (
    construct_truth,
    simulate_same_path,
)


CELLS = [
    (0, 0.688150539, 20.201612910, 0.551117689, -0.020547418),
    (1, 0.336642675, 13.188539490, 0.377758221, 0.028267951),
    (2, 0.528666673, 16.642470066, 0.682941012, -0.560485229),
    (3, 0.887143663, 5.759101400, 0.158522118, 0.589873901),
    (4, 0.759569973, 18.659578890, 0.435244692, 0.728151667),
    (5, 0.418348405, 3.740129625, 0.613944070, -0.720637715),
    (6, 0.216579191, 22.308349485, 0.303208497, 0.289988850),
    (7, 0.564855985, 11.081272740, 0.833566780, -0.260393216),
    (8, 0.635893316, 14.425340595, 0.276149426, -0.658955383),
    (9, 0.276813467, 8.013827052, 0.805831470, 0.691468263),
    (10, 0.434784128, 21.081338726, 0.495778490, -0.322123064),
    (11, 0.786905533, 12.346410183, 0.673786919, 0.326719342),
    (12, 0.816036363, 24.560055207, 0.731768850, 0.191559513),
    (13, 0.468545259, 8.867165821, 0.208024861, -0.158838145),
    (14, 0.320309133, 17.820472134, 0.512522389, 0.426626757),
    (15, 0.660755691, 4.616835512, 0.339855204, -0.422238585),
]
SEEDS = [314159, 271828, 161803]
PREFLIGHT_CELLS = {0, 5, 10, 15}
FINE_FS = 256.0
DECIMATION = 2
SECONDS = 60.0
PRIMARY_MAXITER = 80
PRIMARY_MAX_STARTS = 18
RESCUE_MAXITER = 160
RESCUE_MAX_STARTS = 24
MECH_REL_TOL = 1e-6


def serialize_c1q(fit) -> dict[str, Any]:
    return {
        "success": bool(fit.success),
        "negative_log_likelihood": float(fit.negative_log_likelihood),
        "bic": float(fit.bic),
        "parameters": {k: float(v) for k, v in fit.parameters.items()},
        "raw_parameters": [float(v) for v in fit.raw_parameters],
        "attempted_start_count": int(fit.attempted_start_count),
        "converged_start_count": int(fit.converged_start_count),
        "optimizer_message": str(fit.optimizer_message),
    }


def serialize_rs(fit) -> dict[str, Any]:
    return {
        "success": bool(fit.success),
        "negative_log_likelihood": float(fit.negative_log_likelihood),
        "bic": float(fit.bic),
        "parameters": {k: float(v) for k, v in fit.parameters.items()},
        "raw_parameters": [float(v) for v in fit.raw_parameters],
        "attempted_start_count": int(fit.attempted_start_count),
        "converged_start_count": int(fit.converged_start_count),
        "legacy_attempted_start_count": int(fit.legacy_attempted_start_count),
        "legacy_converged_start_count": int(fit.legacy_converged_start_count),
        "legacy_best_negative_log_likelihood": float(
            fit.legacy_best_negative_log_likelihood
        ),
        "legacy_best_success": bool(fit.legacy_best_success),
        "winning_start_origin": str(fit.winning_start_origin),
        "recurrence_seed_status": str(fit.recurrence_seed_status),
        "recurrence_seed_ready": bool(fit.recurrence_seed_ready),
        "recurrence_seed_A_unprojected": fit.recurrence_seed_A_unprojected,
        "recurrence_seed_g_unprojected": fit.recurrence_seed_g_unprojected,
        "recurrence_seed_A_projected": bool(fit.recurrence_seed_A_projected),
        "recurrence_seed_g_projected": bool(fit.recurrence_seed_g_projected),
        "optimizer_message": str(fit.optimizer_message),
    }


def fit_legacy_route(signal: np.ndarray, fs: float) -> dict[str, Any]:
    primary = fit_continuous_lineage_candidate(
        signal,
        fs,
        optimizer_maxiter=PRIMARY_MAXITER,
        max_optimized_starts=PRIMARY_MAX_STARTS,
    )
    rescue = None
    if not primary.success:
        rescue = fit_continuous_lineage_candidate(
            signal,
            fs,
            optimizer_maxiter=RESCUE_MAXITER,
            max_optimized_starts=RESCUE_MAX_STARTS,
        )

    if primary.success:
        chosen = primary
        source = "primary"
    elif rescue is not None and rescue.success:
        chosen = rescue
        source = "rescue"
    elif rescue is not None and rescue.negative_log_likelihood < primary.negative_log_likelihood:
        chosen = rescue
        source = "rescue"
    else:
        chosen = primary
        source = "primary"

    return {
        "primary": serialize_c1q(primary),
        "rescue": serialize_c1q(rescue) if rescue is not None else None,
        "chosen_source": source,
        "chosen": serialize_c1q(chosen),
    }


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


def truth_checks(truth: dict[str, Any], m: int) -> dict[str, Any]:
    qc_min = float(np.min(np.linalg.eigvalsh(truth["Qc"])))
    qd_min = float(np.min(np.linalg.eigvalsh(truth["Qd"])))
    alias_safe = bool(m * truth["theta"] < math.pi)
    return {
        "Qc_min_eigenvalue": qc_min,
        "Qd_min_eigenvalue": qd_min,
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
) -> dict[str, Any]:
    idx, A, fn, chi, g = cell
    legacy = fit_legacy_route(signal, fs)
    rs = fit_rs_route(signal, fs)
    old = legacy["chosen"]
    new = rs["chosen"]

    tol = MECH_REL_TOL * max(1.0, abs(old["negative_log_likelihood"]))
    strict = bool(
        new["negative_log_likelihood"]
        <= old["negative_log_likelihood"] + tol
    )
    if not strict:
        raise RuntimeError(
            f"strict non-worsening failed cell={idx} seed={seed} rate={rate_label}"
        )

    op = old["parameters"]
    np_ = new["parameters"]
    return {
        "cell_index": idx,
        "seed": seed,
        "rate_label": rate_label,
        "sampling_rate_hz": fs,
        "sample_count": int(signal.size),
        "truth_A": A,
        "truth_natural_frequency_hz": fn,
        "truth_chi": chi,
        "truth_g": g,
        "legacy": legacy,
        "rs": rs,
        "strict_nonworsening_pass": strict,
        "nll_improvement": float(
            old["negative_log_likelihood"]
            - new["negative_log_likelihood"]
        ),
        "legacy_abs_chi_error": float(abs(op["damping_ratio"] - chi)),
        "rs_abs_chi_error": float(abs(np_["damping_ratio"] - chi)),
        "legacy_abs_g_error": float(abs(op["g"] - g)),
        "rs_abs_g_error": float(abs(np_["g"] - g)),
        "legacy_abs_fn_error_hz": float(
            abs(op["natural_frequency_hz"] - fn)
        ),
        "rs_abs_fn_error_hz": float(
            abs(np_["natural_frequency_hz"] - fn)
        ),
        "chi_error_change_rs_minus_legacy": float(
            abs(np_["damping_ratio"] - chi)
            - abs(op["damping_ratio"] - chi)
        ),
        "g_error_change_rs_minus_legacy": float(
            abs(np_["g"] - g) - abs(op["g"] - g)
        ),
        "fn_error_change_rs_minus_legacy": float(
            abs(np_["natural_frequency_hz"] - fn)
            - abs(op["natural_frequency_hz"] - fn)
        ),
    }


def pair_row(fine: dict[str, Any], coarse: dict[str, Any]) -> dict[str, Any]:
    return {
        "cell_index": fine["cell_index"],
        "seed": fine["seed"],
        "legacy_chi_rate_drift": float(
            abs(
                fine["legacy"]["chosen"]["parameters"]["damping_ratio"]
                - coarse["legacy"]["chosen"]["parameters"]["damping_ratio"]
            )
        ),
        "rs_chi_rate_drift": float(
            abs(
                fine["rs"]["chosen"]["parameters"]["damping_ratio"]
                - coarse["rs"]["chosen"]["parameters"]["damping_ratio"]
            )
        ),
        "legacy_g_rate_drift": float(
            abs(
                fine["legacy"]["chosen"]["parameters"]["g"]
                - coarse["legacy"]["chosen"]["parameters"]["g"]
            )
        ),
        "rs_g_rate_drift": float(
            abs(
                fine["rs"]["chosen"]["parameters"]["g"]
                - coarse["rs"]["chosen"]["parameters"]["g"]
            )
        ),
    }


def run_cell(cell_index: int, preflight: bool, output_dir: Path) -> dict[str, Any]:
    cell = CELLS[cell_index]
    if preflight and cell_index not in PREFLIGHT_CELLS:
        raise ValueError("preflight cell not in frozen preflight set")
    seeds = [SEEDS[0]] if preflight else SEEDS

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
        audit = truth_checks(truth, DECIMATION)
        audits.append({"cell_index": cell_index, "seed": seed, **audit})
        if audit["Qc_min_eigenvalue"] < -1e-8:
            raise RuntimeError("invalid Qc")
        if audit["Qd_min_eigenvalue"] < -1e-8:
            raise RuntimeError("invalid Qd")
        if not audit["alias_safe_factor_m"]:
            raise RuntimeError("frozen design violates alias safety")

        fine_signal = simulate_same_path(truth, seconds=SECONDS, seed=seed)
        coarse_signal = fine_signal[::DECIMATION]
        fine = rate_row(
            cell=cell,
            seed=seed,
            rate_label="fine",
            signal=fine_signal,
            fs=FINE_FS,
        )
        coarse = rate_row(
            cell=cell,
            seed=seed,
            rate_label="coarse",
            signal=coarse_signal,
            fs=FINE_FS / DECIMATION,
        )
        rows.extend([fine, coarse])
        pairs.append(pair_row(fine, coarse))

    payload = {
        "status": (
            "P0Q_C1Q_RS_UNTOUCHED_PREFLIGHT_CELL_COMPLETE"
            if preflight
            else "P0Q_C1Q_RS_UNTOUCHED_CELL_COMPLETE"
        ),
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "promotes_c1q_rs": False,
        "cell_index": cell_index,
        "preflight": preflight,
        "truth_audit": audits,
        "rows": rows,
        "pairs": pairs,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    label = "preflight" if preflight else "full"
    out = output_dir / f"c1q_rs_untouched_{label}_cell_{cell_index}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"cell": cell_index, "preflight": preflight, "rows": len(rows), "output": str(out)}, sort_keys=True))
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
    files = sorted(input_dir.rglob("c1q_rs_untouched_full_cell_*.json"))
    if len(files) != 16:
        raise RuntimeError(f"expected 16 full cell files, found {len(files)}")
    payloads = [json.loads(p.read_text(encoding="utf-8")) for p in files]
    rows = [r for p in payloads for r in p["rows"]]
    pairs = [r for p in payloads for r in p["pairs"]]
    if len(rows) != 96 or len(pairs) != 48:
        raise RuntimeError(
            f"unexpected merged counts rows={len(rows)} pairs={len(pairs)}"
        )

    summary = {
        "row_count": len(rows),
        "pair_count": len(pairs),
        "strict_nonworsening_pass_count": int(
            sum(r["strict_nonworsening_pass"] for r in rows)
        ),
        "recurrence_seed_ready_count": int(
            sum(r["rs"]["chosen"]["recurrence_seed_ready"] for r in rows)
        ),
        "recurrence_winning_count": int(
            sum(
                r["rs"]["chosen"]["winning_start_origin"] == "recurrence"
                for r in rows
            )
        ),
        "nll_improvement": stats(r["nll_improvement"] for r in rows),
        "legacy_abs_chi_error": stats(r["legacy_abs_chi_error"] for r in rows),
        "rs_abs_chi_error": stats(r["rs_abs_chi_error"] for r in rows),
        "legacy_abs_g_error": stats(r["legacy_abs_g_error"] for r in rows),
        "rs_abs_g_error": stats(r["rs_abs_g_error"] for r in rows),
        "legacy_abs_fn_error_hz": stats(
            r["legacy_abs_fn_error_hz"] for r in rows
        ),
        "rs_abs_fn_error_hz": stats(r["rs_abs_fn_error_hz"] for r in rows),
        "chi_error_change_rs_minus_legacy": stats(
            r["chi_error_change_rs_minus_legacy"] for r in rows
        ),
        "g_error_change_rs_minus_legacy": stats(
            r["g_error_change_rs_minus_legacy"] for r in rows
        ),
        "legacy_chi_rate_drift": stats(
            r["legacy_chi_rate_drift"] for r in pairs
        ),
        "rs_chi_rate_drift": stats(r["rs_chi_rate_drift"] for r in pairs),
        "legacy_g_rate_drift": stats(
            r["legacy_g_rate_drift"] for r in pairs
        ),
        "rs_g_rate_drift": stats(r["rs_g_rate_drift"] for r in pairs),
    }

    by_rate = {}
    for rate in ("fine", "coarse"):
        rr = [r for r in rows if r["rate_label"] == rate]
        by_rate[rate] = {
            "row_count": len(rr),
            "recurrence_winning_count": int(
                sum(
                    r["rs"]["chosen"]["winning_start_origin"] == "recurrence"
                    for r in rr
                )
            ),
            "nll_improvement": stats(r["nll_improvement"] for r in rr),
            "legacy_abs_chi_error": stats(
                r["legacy_abs_chi_error"] for r in rr
            ),
            "rs_abs_chi_error": stats(r["rs_abs_chi_error"] for r in rr),
            "legacy_abs_g_error": stats(
                r["legacy_abs_g_error"] for r in rr
            ),
            "rs_abs_g_error": stats(r["rs_abs_g_error"] for r in rr),
        }

    by_cell = {}
    for cell in range(16):
        rr = [r for r in rows if r["cell_index"] == cell]
        by_cell[str(cell)] = {
            "nll_improvement": stats(r["nll_improvement"] for r in rr),
            "legacy_abs_chi_error": stats(
                r["legacy_abs_chi_error"] for r in rr
            ),
            "rs_abs_chi_error": stats(r["rs_abs_chi_error"] for r in rr),
            "legacy_abs_g_error": stats(
                r["legacy_abs_g_error"] for r in rr
            ),
            "rs_abs_g_error": stats(r["rs_abs_g_error"] for r in rr),
            "recurrence_winning_count": int(
                sum(
                    r["rs"]["chosen"]["winning_start_origin"] == "recurrence"
                    for r in rr
                )
            ),
        }

    payload = {
        "status": "P0Q_C1Q_RS_UNTOUCHED_COMPLETE",
        "licenses_real_eeg_local_chi": False,
        "defines_scientific_threshold": False,
        "promotes_c1q_rs": False,
        "rows": rows,
        "pairs": pairs,
        "summary": summary,
        "by_rate": by_rate,
        "by_cell": by_cell,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    out = output_dir / "c1q_rs_untouched_complete.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"status": payload["status"], "rows": len(rows), "pairs": len(pairs), "output": str(out)}, sort_keys=True))
    return payload


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
