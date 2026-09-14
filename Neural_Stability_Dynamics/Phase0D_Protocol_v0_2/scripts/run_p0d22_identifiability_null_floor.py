from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.linalg import block_diag, expm

from src.ssi_cov import decompose, fit_from_decomposition
from src.selector import match_indices

DT = 0.01
N_SAMPLES = 4000
BURN = 2500
N_CHANNELS = 8
BLOCK_ROWS = 18
SSI_ORDER = 4
REPLICATES = 8
WEAK_SCALES = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003]
MEASUREMENT_NOISE_FRACTION = 0.05


def _mode_block(chi: float, damped_frequency_hz: float) -> np.ndarray:
    chi = float(chi)
    wd = 2.0 * np.pi * float(damped_frequency_hz)
    omega0 = wd / np.sqrt(1.0 - chi * chi)
    decay = chi * omega0
    return np.array([[-decay, -wd], [wd, -decay]], dtype=float)


def _latent_generator() -> np.ndarray:
    return block_diag(_mode_block(0.55, 3.0), _mode_block(0.85, 5.0))


def _truth_summary(A: np.ndarray) -> dict:
    vals = np.linalg.eigvals(np.asarray(A, float))
    positive = vals[vals.imag > 0]
    positive = positive[np.argsort(positive.imag)]
    chis = [-float(v.real) / float(abs(v)) for v in positive]
    alpha = float(np.max(vals.real))
    return {
        "poles": [[float(v.real), float(v.imag)] for v in vals],
        "positive_mode_chi": chis,
        "spectral_abscissa": alpha,
        "tau": None if alpha >= 0 else float(-1.0 / alpha),
    }


def _simulate_latent(A: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    F = expm(np.asarray(A, float) * DT)
    n = A.shape[0]
    x = np.zeros(n, dtype=float)
    scale = np.sqrt(DT)
    for _ in range(BURN):
        x = F @ x + scale * rng.normal(size=n)
    X = np.empty((N_SAMPLES, n), dtype=float)
    for k in range(N_SAMPLES):
        x = F @ x + scale * rng.normal(size=n)
        X[k] = x
    X -= X.mean(axis=0, keepdims=True)
    return X


def _base_observation(rng: np.random.Generator) -> np.ndarray:
    C = rng.normal(size=(N_CHANNELS, 4))
    norms = np.linalg.norm(C, axis=1, keepdims=True)
    return C / np.maximum(norms, 1e-12)


def _observation_map(C_base: np.ndarray, weak_scale: float) -> np.ndarray:
    C = np.asarray(C_base, float).copy()
    C[:, 2:4] *= float(weak_scale)
    return C


def _observability_metrics(A: np.ndarray, C: np.ndarray) -> dict:
    F = expm(np.asarray(A, float) * DT)
    blocks = []
    Fk = np.eye(A.shape[0])
    for _ in range(20):
        blocks.append(C @ Fk)
        Fk = Fk @ F
    O = np.vstack(blocks)
    s = np.linalg.svd(O, compute_uv=False)
    ratio = float(s[-1] / max(s[0], 1e-15))
    strong = float(np.linalg.norm(C[:, :2], ord="fro"))
    weak = float(np.linalg.norm(C[:, 2:4], ord="fro"))
    return {
        "observability_singular_ratio": ratio,
        "weak_to_strong_column_norm_ratio": float(weak / max(strong, 1e-15)),
    }


def _effective_rank_proxy(S: np.ndarray) -> float:
    s = np.asarray(S, float)
    den = float(np.sum(s * s))
    return 0.0 if den <= 0 else float(np.sum(s) ** 2 / den)


def _pole_pair(v: complex) -> list[float]:
    return [float(np.real(v)), float(np.imag(v))]


def _estimate(Y: np.ndarray, truth_positive: np.ndarray, truth_tau: float | None) -> dict:
    try:
        U, S, p = decompose(Y, BLOCK_ROWS)
        vals, _ = fit_from_decomposition(U, S, p, SSI_ORDER, DT)
    except Exception as exc:
        return {
            "status": "ESTIMATOR_EXCEPTION",
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }

    vals = np.asarray(vals, complex)
    finite = np.isfinite(vals.real) & np.isfinite(vals.imag)
    vals = vals[finite]
    if len(vals) == 0:
        return {
            "status": "INSUFFICIENT_FINITE_POLES",
            "hankel_effective_rank_proxy": _effective_rank_proxy(S),
        }

    positive = vals[vals.imag > 0]
    alpha = float(np.max(vals.real))
    tau = None if alpha >= 0 else float(-1.0 / alpha)
    out = {
        "status": "OK",
        "hankel_effective_rank_proxy": _effective_rank_proxy(S),
        "estimated_poles": [_pole_pair(v) for v in vals],
        "estimated_positive_complex_modes": int(len(positive)),
        "estimated_spectral_abscissa": alpha,
        "estimated_tau": tau,
        "tau_absolute_error": None if tau is None or truth_tau is None else float(abs(tau - truth_tau)),
    }

    if len(positive) < len(truth_positive):
        out["modal_scoring_status"] = "INSUFFICIENT_ESTIMATED_MODES"
        out["matched_modal_chi_mae"] = None
        return out

    pairs = match_indices(truth_positive, positive)
    if len(pairs) != len(truth_positive):
        out["modal_scoring_status"] = "MATCH_INCOMPLETE"
        out["matched_modal_chi_mae"] = None
        return out

    errors = []
    matched = []
    for i, j, distance in pairs:
        tv = truth_positive[i]
        ev = positive[j]
        tchi = -float(tv.real) / float(abs(tv))
        echi = -float(ev.real) / float(abs(ev)) if abs(ev) > 0 else np.nan
        if np.isfinite(echi):
            errors.append(abs(echi - tchi))
        matched.append({
            "truth_pole": _pole_pair(tv),
            "estimated_pole": _pole_pair(ev),
            "pole_distance": float(distance),
            "truth_chi": tchi,
            "estimated_chi": None if not np.isfinite(echi) else float(echi),
        })
    out["modal_scoring_status"] = "MATCHED"
    out["matched_modes"] = matched
    out["matched_modal_chi_mae"] = None if not errors else float(np.mean(errors))
    return out


def _median_finite(rows: list[dict], key: str) -> float | None:
    vals = [r.get(key) for r in rows]
    vals = [float(v) for v in vals if v is not None and np.isfinite(v)]
    return None if not vals else float(np.median(vals))


def build_record() -> dict:
    A = _latent_generator()
    truth = _truth_summary(A)
    truth_vals = np.linalg.eigvals(A)
    truth_positive = truth_vals[truth_vals.imag > 0]
    truth_positive = truth_positive[np.argsort(truth_positive.imag)]
    all_rows = []

    for replicate in range(REPLICATES):
        X = _simulate_latent(A, np.random.default_rng(8000 + replicate))
        C0 = _base_observation(np.random.default_rng(9000 + replicate))
        baseline = X @ C0.T
        channel_sd = np.maximum(baseline.std(axis=0, keepdims=True), 1e-12)
        noise_rng = np.random.default_rng(10000 + replicate)
        noise = noise_rng.normal(size=baseline.shape)
        noise -= noise.mean(axis=0, keepdims=True)
        noise /= np.maximum(noise.std(axis=0, keepdims=True), 1e-12)
        absolute_noise = MEASUREMENT_NOISE_FRACTION * channel_sd * noise

        for weak_scale in WEAK_SCALES:
            C = _observation_map(C0, weak_scale)
            Y = X @ C.T + absolute_noise
            Y -= Y.mean(axis=0, keepdims=True)
            row = {
                "replicate": replicate,
                "weak_scale": weak_scale,
                **_observability_metrics(A, C),
            }
            row.update(_estimate(Y, truth_positive, truth["tau"]))
            all_rows.append(row)

    aggregates = []
    for weak_scale in WEAK_SCALES:
        rows = [r for r in all_rows if r["weak_scale"] == weak_scale]
        aggregates.append({
            "weak_scale": weak_scale,
            "records": len(rows),
            "estimator_ok": int(sum(r.get("status") == "OK" for r in rows)),
            "modal_matches": int(sum(r.get("modal_scoring_status") == "MATCHED" for r in rows)),
            "observability_singular_ratio_median": _median_finite(rows, "observability_singular_ratio"),
            "weak_to_strong_column_norm_ratio_median": _median_finite(rows, "weak_to_strong_column_norm_ratio"),
            "hankel_effective_rank_proxy_median": _median_finite(rows, "hankel_effective_rank_proxy"),
            "matched_modal_chi_mae_median": _median_finite(rows, "matched_modal_chi_mae"),
            "tau_absolute_error_median": _median_finite(rows, "tau_absolute_error"),
        })

    return {
        "schema": "nsd-phase0d-p0d22-identifiability-null-floor-v1",
        "status": "P0_D_EXPLORATORY_KNOWN_TRUTH_NULL_FLOOR_NOT_CONFIRMATORY",
        "protocol": "General Cross-Project Research Protocol v0.7.7",
        "p1_authorized": False,
        "construction": {
            "dt": DT,
            "n_samples": N_SAMPLES,
            "burn": BURN,
            "n_channels": N_CHANNELS,
            "ssi_order": SSI_ORDER,
            "block_rows": BLOCK_ROWS,
            "replicates": REPLICATES,
            "weak_scales": WEAK_SCALES,
            "measurement_noise_fraction_of_baseline_channel_sd": MEASUREMENT_NOISE_FRACTION,
            "truth_invariant_across_conditions": True,
            "same_latent_trajectory_within_replicate_across_conditions": True,
            "same_absolute_measurement_noise_within_replicate_across_conditions": True,
        },
        "truth_P0_scoring_only": truth,
        "aggregates": aggregates,
        "records": all_rows,
        "firewall": (
            "Only measurements enter SSI-COV. Known truth is used after estimation for P0-D scoring. "
            "No selector threshold is tuned and no empirical outcome, Atlas value, diagnosis or phenotype is an estimator input."
        ),
        "nonclaims": [
            "No neural chi-recovery relationship is confirmed.",
            "No observability, effective-rank, chi-error or recovery-error threshold is frozen.",
            "Failure to recover a mode is insufficient information, not evidence that the mode is physically absent or chi equals zero.",
            "No chi_system, clinical rule, Atlas zone or preferred chi value is defined.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="results/p0d_mapping/identifiability_null_floor_v1.json",
    )
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    record = build_record()
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.resolve())
    for row in record["aggregates"]:
        print(json.dumps(row, sort_keys=True))
    print("P0-D22 IDENTIFIABILITY NULL-FLOOR CHALLENGE COMPLETE. No threshold or empirical relationship frozen.")


if __name__ == "__main__":
    main()
