from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from src.run_chi_bio_chronic_g2_empirical import (
    DEFAULT_FREEZE,
    _download_source,
    _fit_basis,
    _fit_states,
    _load_json,
    _open_frozen_source,
    _project,
    _make_transitions,
    _validate_freeze,
)
from src.run_chi_bio_shortterm_g2_empirical import _fit

DT_WEEKS = 1.0
IMAG_TOL_MULT = 1e-10


def _eig_record(t: np.ndarray) -> dict:
    eig = np.linalg.eigvals(t)
    scale = max(1.0, float(np.max(np.abs(eig))))
    tol = IMAG_TOL_MULT * scale
    vals = sorted(eig.tolist(), key=lambda z: (round(float(np.real(z)), 14), round(float(np.imag(z)), 14)))

    rows = []
    positive_complex = []
    for z in vals:
        re = float(np.real(z))
        im = float(np.imag(z))
        mod = float(abs(z))
        angle = float(np.angle(z))
        row = {
            "real": re,
            "imag": im,
            "modulus": mod,
            "wrapped_phase_rad": angle,
            "is_numerically_real": abs(im) <= tol,
        }
        rows.append(row)
        if im > tol:
            alpha = math.log(mod) / DT_WEEKS if mod > 0.0 else float("-inf")
            branches = []
            for k in (-1, 0, 1):
                omega = (angle + 2.0 * math.pi * k) / DT_WEEKS
                denom = math.hypot(alpha, omega)
                ratio = (-alpha / denom) if math.isfinite(alpha) and denom > 0.0 else None
                branches.append({
                    "branch_k": k,
                    "continuous_decay_real_per_week": alpha if math.isfinite(alpha) else None,
                    "continuous_angular_frequency_rad_per_week": omega,
                    "derived_ratio_not_licensed_chi": ratio,
                })
            positive_complex.append({
                "discrete_eigenvalue": row,
                "branch_sensitivity": branches,
            })

    n_real = sum(r["is_numerically_real"] for r in rows)
    n_pairs = len(positive_complex)
    return {
        "dimension": int(t.shape[0]),
        "imag_tolerance": tol,
        "eigenvalues": rows,
        "n_numerically_real_eigenvalues": int(n_real),
        "n_complex_conjugate_pairs": int(n_pairs),
        "has_complex_conjugate_pair": bool(n_pairs > 0),
        "complex_pair_positive_imag_records": positive_complex,
    }


def _record_fit(label: str, fit: dict) -> dict:
    rec = {"label": label, "fit_status": fit.get("status")}
    if fit.get("status") == "PASS":
        rec["eigenstructure"] = _eig_record(fit["T"])
    return rec


def _rank_diagnostics(pbs: np.ndarray, ctx: np.ndarray, rank: int) -> dict:
    basis, x0, x1, u, _ = _fit_states(pbs, ctx, rank)

    fits = []
    point = _fit(x0, x1, u, "D1")
    fits.append(_record_fit("POINT", point))

    for omit in range(x0.shape[0]):
        keep = np.ones(x0.shape[0], dtype=bool)
        keep[omit] = False
        fit = _fit(x0[keep], x1[keep], u[keep], "D1")
        fits.append(_record_fit(f"LOTO_{omit}", fit))

    keep = np.ones(x0.shape[0], dtype=bool)
    keep[[0, 10]] = False
    fits.append(_record_fit("EARLIEST_PAIRED_BLOCK", _fit(x0[keep], x1[keep], u[keep], "D1")))

    for omit in range(11):
        try:
            b = _fit_basis(np.delete(pbs, omit, axis=0), rank)
            ps = _project(b, pbs)
            cs = _project(b, ctx)
            a0, a1, au, _ = _make_transitions(ps, cs)
            fit = _fit(a0, a1, au, "D1")
        except Exception as exc:
            fit = {"status": "REFUSE_UNSTABLE_OR_NONTRANSPORTABLE_BASIS", "reason": f"{type(exc).__name__}: {exc}"}
        fits.append(_record_fit(f"BASIS_LOO_{omit}", fit))

    all_pass = all(r["fit_status"] == "PASS" for r in fits)
    pair_flags = [
        r["eigenstructure"]["has_complex_conjugate_pair"]
        for r in fits if r["fit_status"] == "PASS"
    ]
    point_pair = (
        fits[0].get("eigenstructure", {}).get("has_complex_conjugate_pair")
        if fits[0]["fit_status"] == "PASS" else None
    )

    if not all_pass:
        structure = "INDETERMINATE_REQUIRED_REFIT_FAILURE"
        eligibility = "NOT_ELIGIBLE_FOR_SCALAR_ADMISSION_REVIEW"
    elif pair_flags and all(pair_flags):
        structure = "PAIR_STRUCTURE_PERSISTENT_DERIVATION_REQUIRED"
        eligibility = "ELIGIBLE_FOR_PROSPECTIVE_SCALAR_DERIVATION_REVIEW"
    elif any(pair_flags):
        structure = "PAIR_STRUCTURE_REPRESENTATION_DEPENDENT"
        eligibility = "NOT_ELIGIBLE_FOR_SCALAR_ADMISSION_REVIEW"
    else:
        structure = "DISCRETE_EIGENSTRUCTURE_ONLY_NO_PAIR"
        eligibility = "NOT_ELIGIBLE_FOR_COMPLEX_PAIR_SCALAR_DERIVATION"

    return {
        "rank": rank,
        "basis_numerical_rank": int(basis["numerical_rank"]),
        "n_required_operator_fits": len(fits),
        "all_required_operator_fits_admissible": all_pass,
        "point_has_complex_pair": point_pair,
        "n_fits_with_complex_pair": int(sum(pair_flags)),
        "n_admissible_fits": int(len(pair_flags)),
        "pair_structure_disposition": structure,
        "scalar_derivation_eligibility": eligibility,
        "scalar_chi_licensed": False,
        "why_not_licensed": (
            "The fitted object is a source-native discrete one-week operator. "
            "A complex pair, if present, does not by itself license continuous-time "
            "second-order dynamics, a unique logarithm branch, or biological chi."
        ),
        "fits": fits,
    }


def main() -> int:
    freeze = _load_json(DEFAULT_FREEZE)
    _validate_freeze(freeze)
    payload, history = _download_source()
    source = _open_frozen_source(payload, freeze)
    pbs = source.pop("pbs")
    ctx = source.pop("ctx")

    by_rank = {str(rank): _rank_diagnostics(pbs, ctx, rank) for rank in (2, 3)}
    dispositions = [by_rank[str(r)]["pair_structure_disposition"] for r in (2, 3)]

    if any(x == "INDETERMINATE_REQUIRED_REFIT_FAILURE" for x in dispositions):
        overall = "INDETERMINATE_REQUIRED_REFIT_FAILURE"
    elif len(set(dispositions)) > 1:
        overall = "REPRESENTATION_DEPENDENT_SCALAR_ELIGIBILITY"
    elif dispositions[0] == "PAIR_STRUCTURE_PERSISTENT_DERIVATION_REQUIRED":
        overall = "ELIGIBLE_FOR_PROSPECTIVE_SCALAR_DERIVATION_REVIEW"
    else:
        overall = dispositions[0]

    result = {
        "schema": "GRI_SCC25_G2_SCALAR_ADMISSION_EIGENSTRUCTURE_V01",
        "status": "COMPLETE_POSTRESULT_DIAGNOSTIC",
        "epistemic_class": "P0_D_POSTRESULT_DIAGNOSTIC",
        "historical_g2_result_modified": False,
        "source_sha256": source["source_sha256"],
        "download_attempt_history": history,
        "by_rank": by_rank,
        "cross_rank_disposition": overall,
        "rho_T_promoted_to_chi": False,
        "continuous_time_generator_assumed": False,
        "logarithm_branch_selected": False,
        "biological_unity_boundary_admitted": False,
        "scalar_chi_admitted": False,
        "next_gate": (
            "If and only if eigenstructure is eligible, prospective review must establish "
            "continuous-generator/branch/second-order licensing before any quantity is named chi. "
            "Otherwise proceed with local/modal z_i <-> capital-Chi testing."
        ),
    }

    out = Path("development_outputs/scc25_g2_scalar_admission_diagnostic")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "GRI_SCC25_G2_SCALAR_ADMISSION_EIGENSTRUCTURE_V01.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
