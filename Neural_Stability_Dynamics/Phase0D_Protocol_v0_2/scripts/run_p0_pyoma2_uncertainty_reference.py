from __future__ import annotations
import argparse
import importlib.metadata
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.optimize import linear_sum_assignment

from src.synthetic_systems import make_linear_system, simulate_linear, truth_modes


DT = 0.02
N_SAMPLES = 3600
N_CHANNELS = 4
BLOCK_ROWS = 12
ORDER = 4
NBLOCKS_UNCERTAINTY = 12
REPLICATES = 6
PROCESS_SCALE = 0.35


def _load_pyoma_ssi():
    try:
        from pyoma2.functions import ssi
    except Exception as exc:
        raise RuntimeError(
            "pyOMA_2 reference dependency is unavailable; this script is for the "
            "dedicated external-reference workflow only"
        ) from exc
    return ssi


def _truth_spec():
    return {
        "modes": [
            {"type": "complex", "decay": 0.6, "frequency_hz": 3.0},
            {"type": "complex", "decay": 1.0, "frequency_hz": 8.0},
        ],
        "similarity": "orthogonal",
    }


def _positive_indices(vals):
    vals = np.asarray(vals, complex)
    return np.where(vals.imag > 0.0)[0]


def _match_truth(true_vals, est_vals):
    ti = _positive_indices(true_vals)
    ei = _positive_indices(est_vals)
    if len(ti) == 0 or len(ei) == 0:
        return []
    tf = np.abs(np.asarray(true_vals)[ti]) / (2 * np.pi)
    ef = np.abs(np.asarray(est_vals)[ei]) / (2 * np.pi)
    cost = np.abs(tf[:, None] - ef[None, :])
    rr, cc = linear_sum_assignment(cost)
    return [(int(ti[r]), int(ei[c])) for r, c in zip(rr, cc)]


def _one_record(replicate):
    ssi = _load_pyoma_ssi()
    seed = 330000 + 1000 * replicate
    A, C = make_linear_system(
        _truth_spec(), N_CHANNELS, np.random.default_rng(seed)
    )
    Y = simulate_linear(
        A,
        C,
        DT,
        N_SAMPLES,
        PROCESS_SCALE,
        np.random.default_rng(seed + 1),
    )
    true_vals, _ = truth_modes(A, C)

    H, T = ssi.build_hank(
        Y=Y.T,
        Yref=Y.T,
        br=BLOCK_ROWS,
        method="cov",
        calc_unc=True,
        nb=NBLOCKS_UNCERTAINTY,
    )
    Obs, AA, CC, _ = ssi.SSI_fast(H, BLOCK_ROWS, ORDER, step=1)
    Fn, Xi, Phi, Lambds, Fn_std, Xi_std, Phi_std = ssi.SSI_poles(
        Obs,
        AA,
        CC,
        ORDER,
        DT,
        step=1,
        HC=False,
        xi_max=1.0,
        calc_unc=True,
        H=H,
        T=T,
    )

    col = ORDER
    est_vals = np.asarray(Lambds[:, col], complex)
    matches = _match_truth(true_vals, est_vals)
    rows = []
    for true_i, est_i in matches:
        tv = complex(true_vals[true_i])
        ev = complex(est_vals[est_i])
        true_fn = float(abs(tv) / (2 * np.pi))
        true_xi = float(-tv.real / abs(tv))
        est_fn = float(Fn[est_i, col])
        est_xi = float(Xi[est_i, col])
        fn_se = float(Fn_std[est_i, col])
        xi_se = float(Xi_std[est_i, col])
        rows.append({
            "true_frequency_hz": true_fn,
            "estimated_frequency_hz": est_fn,
            "frequency_standard_error": fn_se,
            "frequency_abs_error": float(abs(est_fn - true_fn)),
            "frequency_abs_error_over_se": (
                float(abs(est_fn - true_fn) / fn_se)
                if np.isfinite(fn_se) and fn_se > 0
                else None
            ),
            "frequency_truth_within_plusminus_1p96_se": (
                bool(abs(est_fn - true_fn) <= 1.96 * fn_se)
                if np.isfinite(fn_se) and fn_se > 0
                else None
            ),
            "true_damping_ratio": true_xi,
            "estimated_damping_ratio": est_xi,
            "damping_standard_error": xi_se,
            "damping_abs_error": float(abs(est_xi - true_xi)),
            "damping_abs_error_over_se": (
                float(abs(est_xi - true_xi) / xi_se)
                if np.isfinite(xi_se) and xi_se > 0
                else None
            ),
            "damping_truth_within_plusminus_1p96_se": (
                bool(abs(est_xi - true_xi) <= 1.96 * xi_se)
                if np.isfinite(xi_se) and xi_se > 0
                else None
            ),
        })

    return {
        "replicate": replicate,
        "matched_positive_complex_modes": len(rows),
        "modes": rows,
        "finite_frequency_uncertainties": int(
            sum(np.isfinite(r["frequency_standard_error"]) and r["frequency_standard_error"] > 0 for r in rows)
        ),
        "finite_damping_uncertainties": int(
            sum(np.isfinite(r["damping_standard_error"]) and r["damping_standard_error"] > 0 for r in rows)
        ),
    }


def _aggregate(records):
    modes = [m for r in records for m in r["modes"]]
    fz = [m["frequency_abs_error_over_se"] for m in modes if m["frequency_abs_error_over_se"] is not None]
    xz = [m["damping_abs_error_over_se"] for m in modes if m["damping_abs_error_over_se"] is not None]
    fcov = [m["frequency_truth_within_plusminus_1p96_se"] for m in modes if m["frequency_truth_within_plusminus_1p96_se"] is not None]
    xcov = [m["damping_truth_within_plusminus_1p96_se"] for m in modes if m["damping_truth_within_plusminus_1p96_se"] is not None]
    return {
        "records": len(records),
        "matched_modes": len(modes),
        "frequency_abs_error_over_se_median": float(np.median(fz)) if fz else None,
        "frequency_abs_error_over_se_p90": float(np.quantile(fz, 0.90)) if fz else None,
        "frequency_plusminus_1p96_se_coverage_descriptive": float(np.mean(fcov)) if fcov else None,
        "damping_abs_error_over_se_median": float(np.median(xz)) if xz else None,
        "damping_abs_error_over_se_p90": float(np.quantile(xz, 0.90)) if xz else None,
        "damping_plusminus_1p96_se_coverage_descriptive": float(np.mean(xcov)) if xcov else None,
    }


def build_record():
    records = [_one_record(i) for i in range(REPLICATES)]
    version = importlib.metadata.version("pyOMA_2")
    return {
        "schema": "nsd-phase0d-v0.2-p0-pyoma2-uncertainty-reference-v1",
        "status": "P0_EXTERNAL_REFERENCE_NOT_ENGINE_IMPLEMENTATION",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL",
        "p1_authorized": False,
        "reference_package": {
            "name": "pyOMA_2",
            "version": version,
            "license": "MIT",
            "source": "dagghe/pyOMA2",
            "method": "covariance SSI with calc_unc=True",
        },
        "design": {
            "dt": DT,
            "n_samples": N_SAMPLES,
            "n_channels": N_CHANNELS,
            "block_rows": BLOCK_ROWS,
            "fixed_order": ORDER,
            "uncertainty_blocks": NBLOCKS_UNCERTAINTY,
            "replicates": REPLICATES,
            "process_scale": PROCESS_SCALE,
            "construction": "stationary two-complex-mode stochastic linear system",
        },
        "aggregate": _aggregate(records),
        "records": records,
        "nonclaims": [
            "pyOMA2 is an external reference implementation and is not an NSD Engine dependency.",
            "This test does not prove that pyOMA2 uncertainty is calibrated for EEG.",
            "The fixed order is supplied for P0 uncertainty isolation and is not a P1 order-selection rule.",
            "The plus/minus 1.96 standard-error coverage is a descriptive familiar reference, not a frozen NSD confidence convention.",
            "No NSD analytical SSI uncertainty has yet been implemented merely because this reference runs.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/p0_external_reference/pyoma2_uncertainty_reference.json",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    record = build_record()
    if record["reference_package"]["version"] != "1.4.2":
        raise SystemExit("Reference package version drifted from 1.4.2")
    if any(r["matched_positive_complex_modes"] < 2 for r in record["records"]):
        raise SystemExit("External reference failed to return both planted positive complex modes")
    if any(r["finite_frequency_uncertainties"] < 2 for r in record["records"]):
        raise SystemExit("External reference did not return finite frequency uncertainties")
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("P0 pyOMA2 UNCERTAINTY REFERENCE COMPLETE. No NSD uncertainty rule was frozen.")


if __name__ == "__main__":
    main()
