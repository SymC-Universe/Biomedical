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

from src.ssi_cov import output_covariances, decompose, fit_from_decomposition
from src.synthetic_systems import make_linear_system, simulate_linear, truth_modes

DT = 0.02
BLOCK_ROWS = 12
ORDER = 4
N_CHANNELS = 4
PROCESS_SCALE = 0.35
REPLICATES = 6
DURATIONS = [1800, 3600, 7200]


def _our_hankel(Y, block_rows):
    Y = np.asarray(Y, float)
    n, p = Y.shape
    covs = output_covariances(Y, 2 * block_rows)
    H = np.empty((p * block_rows, p * block_rows))
    for i in range(block_rows):
        for j in range(block_rows):
            H[i*p:(i+1)*p, j*p:(j+1)*p] = covs[i+j]
    return H


def _complex(z):
    z = complex(z)
    return {"real": float(z.real), "imag": float(z.imag)}


def _match(a, b):
    a = np.asarray(a, complex)
    b = np.asarray(b, complex)
    cost = np.abs(a[:, None] - b[None, :]) / np.maximum(
        np.maximum(np.abs(a)[:, None], np.abs(b)[None, :]), 1e-12
    )
    rr, cc = linear_sum_assignment(cost)
    return [(int(r), int(c), float(cost[r,c])) for r,c in zip(rr,cc)]


def _positive(vals):
    vals = np.asarray(vals, complex)
    return np.where(vals.imag > 0.0)[0]


def _one_record(n_samples, replicate):
    from pyoma2.functions import ssi

    seed = 440000 + 10000 * int(n_samples) + replicate
    spec = {
        "modes": [
            {"type": "complex", "decay": 0.6, "frequency_hz": 3.0},
            {"type": "complex", "decay": 1.0, "frequency_hz": 8.0},
        ],
        "similarity": "orthogonal",
    }
    A, C = make_linear_system(spec, N_CHANNELS, np.random.default_rng(seed))
    Y = simulate_linear(
        A, C, DT, int(n_samples), PROCESS_SCALE, np.random.default_rng(seed + 1)
    )
    truth, _ = truth_modes(A, C)

    H_ours = _our_hankel(Y, BLOCK_ROWS)
    H_py, _ = ssi.build_hank(
        Y=Y.T,
        Yref=Y.T,
        br=BLOCK_ROWS,
        method="cov",
        calc_unc=False,
    )
    Uo, So, po = decompose(Y, BLOCK_ROWS)
    vals_ours, shapes_ours = fit_from_decomposition(Uo, So, po, ORDER, DT)

    Obs, AA, CC, _ = ssi.SSI_fast(H_py, BLOCK_ROWS, ORDER, step=1)
    Fn, Xi, Phi, Lambds, _, _, _ = ssi.SSI_poles(
        Obs,
        AA,
        CC,
        ORDER,
        DT,
        step=1,
        HC=False,
        xi_max=1.0,
        calc_unc=False,
    )
    vals_py = np.asarray(Lambds[:, ORDER], complex)

    rel_H = float(np.linalg.norm(H_ours - H_py, "fro") / max(np.linalg.norm(H_py, "fro"), 1e-15))
    s_py = np.linalg.svd(H_py, compute_uv=False)
    k = min(len(So), len(s_py))
    so_norm = So[:k] / max(float(So[0]), 1e-15)
    sp_norm = s_py[:k] / max(float(s_py[0]), 1e-15)
    rel_singular = float(np.linalg.norm(so_norm - sp_norm) / max(np.linalg.norm(sp_norm), 1e-15))

    io = _positive(vals_ours)
    ip = _positive(vals_py)
    it = _positive(truth)
    pair_op = _match(vals_ours[io], vals_py[ip]) if len(io) and len(ip) else []
    pair_ot = _match(vals_ours[io], truth[it]) if len(io) and len(it) else []
    pair_pt = _match(vals_py[ip], truth[it]) if len(ip) and len(it) else []

    return {
        "n_samples": int(n_samples),
        "replicate": int(replicate),
        "hankel_shape_ours": list(H_ours.shape),
        "hankel_shape_pyoma2": list(H_py.shape),
        "relative_frobenius_hankel_difference": rel_H,
        "relative_normalized_singular_spectrum_difference": rel_singular,
        "our_positive_complex_poles": [_complex(z) for z in vals_ours[io]],
        "pyoma2_positive_complex_poles": [_complex(z) for z in vals_py[ip]],
        "truth_positive_complex_poles": [_complex(z) for z in truth[it]],
        "our_vs_pyoma2_relative_pole_errors": [x[2] for x in pair_op],
        "our_vs_truth_relative_pole_errors": [x[2] for x in pair_ot],
        "pyoma2_vs_truth_relative_pole_errors": [x[2] for x in pair_pt],
        "our_vs_pyoma2_median_relative_pole_error": float(np.median([x[2] for x in pair_op])) if pair_op else None,
        "our_vs_truth_median_relative_pole_error": float(np.median([x[2] for x in pair_ot])) if pair_ot else None,
        "pyoma2_vs_truth_median_relative_pole_error": float(np.median([x[2] for x in pair_pt])) if pair_pt else None,
    }


def _summary(records):
    def vals(key):
        return np.asarray([r[key] for r in records if r[key] is not None], float)
    keys = [
        "relative_frobenius_hankel_difference",
        "relative_normalized_singular_spectrum_difference",
        "our_vs_pyoma2_median_relative_pole_error",
        "our_vs_truth_median_relative_pole_error",
        "pyoma2_vs_truth_median_relative_pole_error",
    ]
    out = {}
    for key in keys:
        x = vals(key)
        out[key + "_median"] = float(np.median(x)) if len(x) else None
        out[key + "_max"] = float(np.max(x)) if len(x) else None
    return out


def build_record():
    groups = []
    for n in DURATIONS:
        records = [_one_record(n, r) for r in range(REPLICATES)]
        groups.append({"n_samples": n, "summary": _summary(records), "records": records})
    return {
        "schema": "nsd-phase0d-v0.2-p0-pyoma2-point-compatibility-v1",
        "status": "P0_EXTERNAL_REFERENCE_COMPATIBILITY_NOT_ENGINE_VALIDATION",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL",
        "p1_authorized": False,
        "reference_package": {
            "name": "pyOMA_2",
            "version": importlib.metadata.version("pyOMA_2"),
            "method": "covariance SSI",
        },
        "comparison": {
            "same_block_geometry": "both use b x b covariance blocks spanning positive lags 1 through 2b-1",
            "finite_sample_difference": "NSD uses each lag's full available samples and denominator n-lag; pyOMA2 cov uses a common aligned interval N=n-(2b-1) for every block",
            "order": ORDER,
            "block_rows": BLOCK_ROWS,
            "dt": DT,
        },
        "duration_groups": groups,
        "interpretation_rule": (
            "Even close point estimates do not license direct reuse of pyOMA2's uncertainty matrix T, "
            "because T is the covariance of pyOMA2's finite-sample Hankel estimator. The comparison "
            "only determines how large the estimator-convention difference is."
        ),
        "nonclaims": [
            "No numerical compatibility threshold is frozen.",
            "pyOMA2 uncertainty is not imported into the NSD Engine by this comparison.",
            "Similarity of point poles does not prove equality of estimator covariance.",
            "No EEG, phenotype, chi, regime boundary, mechanism or P1 claim is tested."
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="results/p0_external_reference/pyoma2_point_compatibility.json")
    args = parser.parse_args()
    rec = build_record()
    if rec["reference_package"]["version"] != "1.4.2":
        raise SystemExit("Reference package version drifted from 1.4.2")
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    print("P0 pyOMA2 POINT-ESTIMATOR COMPATIBILITY COMPLETE. No uncertainty transfer was authorized.")


if __name__ == "__main__":
    main()
