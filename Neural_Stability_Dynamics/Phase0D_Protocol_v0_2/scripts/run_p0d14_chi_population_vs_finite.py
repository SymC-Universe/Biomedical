from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.chi_conglomerate import chi_from_pole_pair, second_order_generator
from src.population_covariance import population_covariance_hankel
from src.ssi_cov import decompose, fit_from_decomposition
from src.synthetic_systems import simulate_linear

DT = 0.01
BLOCK_ROWS = 30
PROCESS_SCALE = 0.30
N_CHANNELS = 6
REPLICATES = 8
SEED = 202609111700
OMEGA_N = 2.0 * np.pi * 2.0
CHI_VALUES = [0.80, 0.99, 1.00, 1.01, 1.20, 1.50, 2.00]
N_VALUES = [8000, 32000]
NOISE_FRACTIONS = [0.0, 0.03]


def _C():
    rng = np.random.default_rng(SEED)
    C = rng.normal(size=(N_CHANNELS, 2))
    return C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-12)


def _fit_population(A, C):
    H, _ = population_covariance_hankel(A, C, DT, BLOCK_ROWS, PROCESS_SCALE)
    U, S, _ = np.linalg.svd(H, full_matrices=False)
    vals, _ = fit_from_decomposition(U, S, N_CHANNELS, 2, DT)
    return np.asarray(vals, complex), np.asarray(S, float)


def _fit_sample(Y):
    U, S, p = decompose(Y, BLOCK_ROWS)
    vals, _ = fit_from_decomposition(U, S, p, 2, DT)
    return np.asarray(vals, complex), np.asarray(S, float)


def _add_white_noise(Y, fraction, seed):
    if fraction == 0.0:
        return Y.copy()
    rng = np.random.default_rng(seed)
    sd = np.maximum(Y.std(axis=0, keepdims=True), 1e-12)
    out = Y + float(fraction) * sd * rng.normal(size=Y.shape)
    out -= out.mean(axis=0, keepdims=True)
    return out


def _summary(values):
    x = np.asarray(values, float)
    x = x[np.isfinite(x)]
    if len(x) == 0:
        return {"n": 0, "median": None, "p10": None, "p90": None}
    return {
        "n": int(len(x)),
        "median": float(np.median(x)),
        "p10": float(np.quantile(x, 0.10)),
        "p90": float(np.quantile(x, 0.90)),
    }


def _branch_complex(vals):
    return bool(np.max(np.abs(np.asarray(vals).imag)) > 1e-7)


def _timescale_ratio(chi):
    chi = float(chi)
    if chi < 1.0:
        return None
    if chi == 1.0:
        return 1.0
    return float((chi + np.sqrt(chi * chi - 1.0)) ** 2)


def build():
    C = _C()
    population = []
    finite = []
    for chi_index, chi_truth in enumerate(CHI_VALUES):
        A = second_order_generator(chi_truth, OMEGA_N)
        vals_p, S_p = _fit_population(A, C)
        inv_p = chi_from_pole_pair(vals_p)
        population.append(
            {
                "chi_truth": chi_truth,
                "chi_est": float(inv_p["chi"]),
                "chi_abs_error": float(abs(inv_p["chi"] - chi_truth)),
                "complex_pair": _branch_complex(vals_p),
                "s2_over_s1": float(S_p[1] / S_p[0]),
                "s3_over_s1": float(S_p[2] / S_p[0]),
                "s2_over_s3": float(S_p[1] / max(S_p[2], 1e-300)),
                "timescale_ratio_fast_over_slow": _timescale_ratio(chi_truth),
                "poles": [{"real": float(z.real), "imag": float(z.imag)} for z in vals_p],
            }
        )

        for n in N_VALUES:
            clean_records = []
            for rep in range(REPLICATES):
                clean = simulate_linear(
                    A,
                    C,
                    DT,
                    n,
                    PROCESS_SCALE,
                    np.random.default_rng(SEED + chi_index * 1000000 + n * 10 + rep),
                )
                clean_records.append(clean)
            for noise_fraction in NOISE_FRACTIONS:
                records = []
                for rep, clean in enumerate(clean_records):
                    try:
                        Y = _add_white_noise(
                            clean,
                            noise_fraction,
                            SEED + 90000000 + chi_index * 1000000 + n * 10 + rep,
                        )
                        vals, S = _fit_sample(Y)
                        inv = chi_from_pole_pair(vals)
                        records.append(
                            {
                                "replicate": rep,
                                "status": "OK",
                                "chi_est": float(inv["chi"]),
                                "chi_abs_error": float(abs(inv["chi"] - chi_truth)),
                                "complex_pair": _branch_complex(vals),
                                "all_poles_stable": bool(np.all(vals.real < 0.0)),
                                "s2_over_s1": float(S[1] / S[0]),
                                "s2_over_s3": float(S[1] / max(S[2], 1e-300)),
                            }
                        )
                    except Exception as exc:
                        records.append(
                            {
                                "replicate": rep,
                                "status": "EXCEPTION_PRESERVED",
                                "exception_type": type(exc).__name__,
                                "exception_message": str(exc),
                            }
                        )
                ok = [r for r in records if r["status"] == "OK"]
                finite.append(
                    {
                        "chi_truth": chi_truth,
                        "n_samples": n,
                        "measurement_noise_fraction_channel_sd": noise_fraction,
                        "timescale_ratio_fast_over_slow": _timescale_ratio(chi_truth),
                        "records": records,
                        "summary": {
                            "successful": len(ok),
                            "exceptions": len(records) - len(ok),
                            "chi_est": _summary([r["chi_est"] for r in ok]),
                            "chi_abs_error": _summary([r["chi_abs_error"] for r in ok]),
                            "complex_pair_fraction": (
                                float(np.mean([r["complex_pair"] for r in ok])) if ok else None
                            ),
                            "stable_fit_fraction": (
                                float(np.mean([r["all_poles_stable"] for r in ok])) if ok else None
                            ),
                            "s2_over_s1": _summary([r["s2_over_s1"] for r in ok]),
                            "s2_over_s3": _summary([r["s2_over_s3"] for r in ok]),
                        },
                    }
                )
    return {
        "schema": "nsd-p0d14-chi-population-vs-finite-v1",
        "status": "P0_D_ESTIMATOR_IDENTIFIABILITY_DIAGNOSIS_NOT_QUALIFICATION",
        "protocol": "General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum",
        "p1_authorized": False,
        "atlas_used": False,
        "design": {
            "dt": DT,
            "block_rows": BLOCK_ROWS,
            "process_scale": PROCESS_SCALE,
            "channels": N_CHANNELS,
            "replicates": REPLICATES,
            "omega_n": OMEGA_N,
            "chi_values": CHI_VALUES,
            "n_values": N_VALUES,
            "measurement_noise_fractions": NOISE_FRACTIONS,
            "fixed_development_order": 2,
        },
        "population": population,
        "finite": finite,
        "nonclaims": [
            "No neural record length or sampling rate is selected.",
            "No branch or uncertainty threshold is selected.",
            "No Atlas value, phenotype or outcome is used.",
            "No chi_system, P0-Q or P1 rule is frozen.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--output", default="results/p0d_mapping/chi_population_vs_finite_v1.json"
    )
    args = ap.parse_args()
    rec = build()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for row in rec["population"]:
        print(json.dumps({"surface": "population", **row}, sort_keys=True))
    for row in rec["finite"]:
        print(
            json.dumps(
                {
                    "surface": "finite",
                    "chi_truth": row["chi_truth"],
                    "n_samples": row["n_samples"],
                    "noise": row["measurement_noise_fraction_channel_sd"],
                    "timescale_ratio": row["timescale_ratio_fast_over_slow"],
                    **row["summary"],
                },
                sort_keys=True,
            )
        )
    print("P0-D14 POPULATION VS FINITE-SAMPLE CHI DIAGNOSIS COMPLETE. No branch or P1 rule frozen.")


if __name__ == "__main__":
    main()
