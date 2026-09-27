#!/usr/bin/env python3
"""Combined structural-predictive refusal map for Bio Chi N-B1.

Qualification only. No admission threshold is selected and no production
estimator is changed.

The probe fits the existing qualification-only C1Q and D1Q one-mode candidates
on the first half of known-truth realizations, freezes parameters, and scores
the contiguous second half using the same cold-start-plus-burn convention as
the current NSD holdout machinery. It combines those predictive diagnostics
with positive-lag recurrence/Hankel diagnostics on the untouched holdout.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq
from scipy.signal import lfilter

from nsd_engine.continuous_lineage_candidate import (
    _steady_state as _c1q_steady_state,
    fit_continuous_lineage_candidate,
)
from nsd_engine.discrete_exact_candidate import (
    _steady_state as _d1q_steady_state,
    fit_discrete_exact_candidate,
)
from nsd_engine.latent_oscillator_covariance import (
    LatentOscillatorTruth,
    simulate_latent_oscillator,
)
from nsd_engine.state_space_adequacy import (
    compare_state_space_candidates,
    evaluate_comparison_on_holdout,
)


def _sqrt_psd(matrix: np.ndarray) -> np.ndarray:
    values, vectors = np.linalg.eigh(0.5 * (matrix + matrix.T))
    if float(np.min(values)) < -1e-9:
        raise ValueError("matrix is not PSD")
    return vectors @ np.diag(np.sqrt(np.clip(values, 0.0, None)))


def continuous_c_signal(
    *,
    fs: float,
    seconds: float,
    A: float,
    fn: float,
    zeta: float,
    g: float,
    seed: int,
) -> np.ndarray:
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    dt = 1.0 / fs
    G = g * A * alpha
    D = A * (2.0 * alpha * alpha + nu * nu)
    K = np.asarray([[-alpha, -1.0], [nu * nu, -alpha]], dtype=float)
    P = np.asarray([[A, -G], [-G, D]], dtype=float)
    F = expm(K * dt)
    Qd = P - F @ P @ F.T

    n = int(round(seconds * fs))
    rng = np.random.default_rng(seed)
    x = _sqrt_psd(P) @ rng.normal(size=2)
    qsqrt = _sqrt_psd(Qd)
    observation_sd = math.sqrt(1.0 - A)
    out = np.empty(n, dtype=float)
    for index in range(n):
        out[index] = x[0] + observation_sd * rng.normal()
        x = F @ x + qsqrt @ rng.normal(size=2)
    return out


def rotation_transition(fs: float, frequency: float, damping: float) -> np.ndarray:
    omega_n = 2.0 * math.pi * frequency
    decay = damping * omega_n
    omega_d = omega_n * math.sqrt(1.0 - damping * damping)
    rho = math.exp(-decay / fs)
    theta = omega_d / fs
    return rho * np.asarray(
        [
            [math.cos(theta), -math.sin(theta)],
            [math.sin(theta), math.cos(theta)],
        ],
        dtype=float,
    )


def colored_process_signal(*, fs: float, seconds: float, seed: int) -> np.ndarray:
    burn = int(round(5.0 * fs))
    n = int(round(seconds * fs))
    total = n + burn
    transition = rotation_transition(fs, 10.0, 0.30)
    rho = math.sqrt(float(abs(np.linalg.det(transition))))
    base_sd = math.sqrt(max(1e-12, 1.0 - rho * rho))
    rng = np.random.default_rng(seed + 10000)
    state = rng.normal(size=2)
    colored = np.zeros(2)
    phi = 0.7
    colored_scale = math.sqrt(1.0 - phi * phi)
    latent = np.empty(total)
    for index in range(total):
        latent[index] = state[0]
        colored = phi * colored + colored_scale * rng.normal(size=2)
        state = transition @ state + base_sd * colored
    latent = latent[burn:]
    sd = float(np.std(latent))
    return latent + rng.normal(0.0, 0.50 * sd, size=n)


def two_mode_signal(*, fs: float, seconds: float, seed: int) -> np.ndarray:
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.25, fs),
        seconds=seconds,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(20.0, 0.35, fs),
        seconds=seconds,
        measurement_noise_to_latent_sd=0.0,
        seed=seed + 100,
    )
    rng = np.random.default_rng(seed + 200)
    first = (first - np.mean(first)) / np.std(first)
    second = (second - np.mean(second)) / np.std(second)
    return 0.8 * first + 0.8 * second + rng.normal(0.0, 0.35, size=first.size)


def residual_q(A: float, rho: float, xi: float, H: float):
    q2 = rho * rho * (1.0 - A)
    q1 = rho * (
        (1.0 + rho * rho) * H
        + xi * (A * (1.0 + 3.0 * rho * rho) - 2.0 * (1.0 + rho * rho))
    )
    q0 = (
        1.0
        + rho**4
        + 4.0 * rho * rho * xi * xi
        - 2.0 * A * rho**4
        - 4.0 * A * rho * rho * xi * xi
        - 4.0 * H * rho * rho * xi
    )
    return q0, q1, q2


def spectral_minimum(A: float, rho: float, xi: float, H: float) -> float:
    q0, q1, q2 = residual_q(A, rho, xi, H)

    def poly(x):
        return 4.0 * q2 * x * x + 2.0 * q1 * x + q0 - 2.0 * q2

    candidates = [-1.0, 1.0]
    if q2 > 0.0:
        vertex = -q1 / (4.0 * q2)
        if -1.0 <= vertex <= 1.0:
            candidates.append(vertex)
    return float(min(poly(x) for x in candidates))


def scalar_positive_bound(
    A: float, rho: float, xi: float, sign: int, start: float
) -> float:
    inside = sign * abs(start)
    outside = inside
    for _ in range(80):
        outside *= 1.5
        if spectral_minimum(A, rho, xi, outside) <= 0.0:
            break
    else:
        raise RuntimeError("failed to bracket scalar-positive boundary")
    lo, hi = sorted((inside, outside))
    return float(brentq(lambda H: spectral_minimum(A, rho, xi, H), lo, hi))


def spectral_factor(A: float, rho: float, xi: float, H: float):
    q0, q1, q2 = residual_q(A, rho, xi, H)
    roots = np.roots(np.asarray([q2, q1, q0, q1, q2], dtype=float))
    inside = [complex(root) for root in roots if abs(root) < 1.0 - 1e-8]
    if len(inside) != 2:
        inside = sorted((complex(root) for root in roots), key=abs)[:2]
    r1, r2 = inside
    m1 = float(np.real(-(r1 + r2)))
    m2 = float(np.real(r1 * r2))
    sigma2 = float(q2 / m2)
    if sigma2 <= 0.0:
        raise RuntimeError("invalid spectral factor")
    return sigma2, m1, m2


def arma_second_order_signal(
    *,
    fs: float,
    seconds: float,
    A: float,
    rho: float,
    xi: float,
    H: float,
    seed: int,
) -> np.ndarray:
    sigma2, m1, m2 = spectral_factor(A, rho, xi, H)
    n = int(round(fs * seconds))
    burn = int(round(5.0 * fs))
    total = n + burn
    rng = np.random.default_rng(seed)
    eps = rng.normal(0.0, math.sqrt(sigma2), size=total + 2)
    y = np.zeros(total + 2)
    ar1 = 2.0 * rho * xi
    ar2 = -(rho * rho)
    for t in range(2, total + 2):
        y[t] = (
            ar1 * y[t - 1]
            + ar2 * y[t - 2]
            + eps[t]
            + m1 * eps[t - 1]
            + m2 * eps[t - 2]
        )
    return y[burn + 2 : burn + 2 + n]


def sample_positive_lag_covariances(
    signal: np.ndarray, max_lag: int = 10
) -> np.ndarray:
    x = np.asarray(signal, dtype=float)
    x = x - float(np.mean(x))
    variance = float(np.mean(x * x))
    if variance <= 0.0:
        raise ValueError("zero variance")
    x = x / math.sqrt(variance)
    return np.asarray(
        [
            float(np.mean(x[:-lag] * x[lag:]))
            for lag in range(1, max_lag + 1)
        ],
        dtype=float,
    )


def structural_metrics(signal: np.ndarray) -> dict[str, float]:
    gamma = sample_positive_lag_covariances(signal, max_lag=10)
    H3 = np.asarray(
        [[gamma[i + j] for j in range(3)] for i in range(3)],
        dtype=float,
    )
    singular = np.linalg.svd(H3, compute_uv=False)

    rows = []
    targets = []
    for k in range(1, 4):
        rows.append([gamma[k], -gamma[k - 1]])
        targets.append(gamma[k + 1])
    coeff, _, _, _ = np.linalg.lstsq(
        np.asarray(rows), np.asarray(targets), rcond=None
    )
    a_hat, b_hat = float(coeff[0]), float(coeff[1])

    residuals = []
    references = []
    for k in range(4, 8):
        predicted = a_hat * gamma[k] - b_hat * gamma[k - 1]
        observed = gamma[k + 1]
        residuals.append(observed - predicted)
        references.append(observed)
    residual_rms = float(math.sqrt(np.mean(np.asarray(residuals) ** 2)))
    reference_rms = float(math.sqrt(np.mean(np.asarray(references) ** 2)))

    return {
        "hankel_s3_over_s2": float(singular[2] / max(singular[1], 1e-15)),
        "hankel_s3_over_s1": float(singular[2] / max(singular[0], 1e-15)),
        "recurrence_normalized_holdlag_rms": residual_rms
        / max(reference_rms, 1e-15),
    }


def innovation_diagnostics(
    innovations: np.ndarray, burn: int
) -> dict[str, float]:
    used = np.asarray(innovations[burn:], dtype=float)
    rms = float(math.sqrt(float(np.mean(used * used))))
    centered = used - float(np.mean(used))
    variance = float(np.dot(centered, centered))
    if variance <= 0.0 or used.size < 5:
        return {
            "innovation_rms": rms,
            "innovation_max_abs_autocorrelation": 0.0,
        }
    max_lag = min(20, used.size // 10)
    ac = []
    for lag in range(1, max_lag + 1):
        ac.append(
            float(np.dot(centered[:-lag], centered[lag:])) / variance
        )
    return {
        "innovation_rms": rms,
        "innovation_max_abs_autocorrelation": float(
            np.max(np.abs(ac)) if ac else 0.0
        ),
    }


def score_frozen_candidate(
    holdout: np.ndarray,
    *,
    training_mean: float,
    training_sd: float,
    raw_parameters: tuple[float, ...],
    sampling_rate_hz: float,
    candidate: str,
    fmin_hz: float = 1.0,
    fmax_hz: float = 45.0,
) -> dict[str, float]:
    standardized = (np.asarray(holdout, dtype=float) - training_mean) / training_sd
    raw = np.asarray(raw_parameters, dtype=float)
    if candidate == "C1Q":
        steady = _c1q_steady_state(raw, sampling_rate_hz, fmin_hz, fmax_hz)
    elif candidate == "D1Q":
        steady = _d1q_steady_state(raw, sampling_rate_hz, fmin_hz, fmax_hz)
    else:
        raise ValueError(candidate)
    if steady is None:
        return {
            "negative_log_likelihood_per_sample": float("inf"),
            "innovation_rms": float("inf"),
            "innovation_max_abs_autocorrelation": float("inf"),
        }

    numerator, denominator, innovation_variance, _ = steady
    prediction = lfilter(numerator, denominator, standardized)
    innovation = standardized - prediction
    burn = min(128, max(0, standardized.size // 20))
    used = innovation[burn:]
    nll = float(
        0.5
        * used.size
        * (math.log(2.0 * math.pi) + math.log(innovation_variance))
        + 0.5 * np.dot(used, used) / innovation_variance
    )
    return {
        "negative_log_likelihood_per_sample": nll / used.size,
        **innovation_diagnostics(innovation, burn),
    }


def quantiles(values) -> dict[str, float]:
    x = np.asarray(values, dtype=float)
    return {
        "min": float(np.min(x)),
        "q05": float(np.quantile(x, 0.05)),
        "q25": float(np.quantile(x, 0.25)),
        "median": float(np.median(x)),
        "q75": float(np.quantile(x, 0.75)),
        "q95": float(np.quantile(x, 0.95)),
        "max": float(np.max(x)),
    }


def rank_auc(reference, target) -> float:
    """Threshold-free P(target > reference), with half-credit for ties."""
    ref = np.asarray(reference, dtype=float)
    tar = np.asarray(target, dtype=float)
    score = 0.0
    total = 0
    for x in tar:
        score += float(np.sum(x > ref))
        score += 0.5 * float(np.sum(x == ref))
        total += ref.size
    return float(score / total) if total else float("nan")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fs", type=float, default=256.0)
    parser.add_argument("--seconds", type=float, default=60.0)
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--optimizer-maxiter", type=int, default=60)
    args = parser.parse_args()

    if args.seconds < 20.0:
        raise ValueError("seconds must be at least 20")
    fs = args.fs
    A = 0.8
    fn = 10.0
    zeta = 0.30
    omega_n = 2.0 * math.pi * fn
    alpha = zeta * omega_n
    nu = omega_n * math.sqrt(1.0 - zeta * zeta)
    L = alpha / fs
    rho = math.exp(-L)
    theta = nu / fs
    xi = math.cos(theta)

    H_C = A * L * math.sin(theta) / theta
    H_D = A * math.sinh(L)
    S_pos = scalar_positive_bound(A, rho, xi, +1, H_D)
    S_neg = scalar_positive_bound(A, rho, xi, -1, H_D)
    H_DC_pos = H_C + 0.5 * (H_D - H_C)
    H_DC_neg = -H_DC_pos
    H_SD_pos = 0.5 * (H_D + S_pos)
    H_SD_neg = 0.5 * (-H_D + S_neg)

    rows = []
    for seed in range(args.seeds):
        signals = {
            "C_g0": continuous_c_signal(
                fs=fs, seconds=args.seconds, A=A, fn=fn, zeta=zeta, g=0.0, seed=seed
            ),
            "C_g_neg075": continuous_c_signal(
                fs=fs, seconds=args.seconds, A=A, fn=fn, zeta=zeta, g=-0.75, seed=seed
            ),
            "C_g_pos075": continuous_c_signal(
                fs=fs, seconds=args.seconds, A=A, fn=fn, zeta=zeta, g=0.75, seed=seed
            ),
            "D_not_C_neg": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_DC_neg,
                seed=seed + 2000,
            ),
            "D_not_C_pos": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_DC_pos,
                seed=seed + 3000,
            ),
            "S_not_D_neg": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_SD_neg,
                seed=seed + 4000,
            ),
            "S_not_D_pos": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_SD_pos,
                seed=seed + 5000,
            ),
            "colored_phi_0_7": colored_process_signal(
                fs=fs, seconds=args.seconds, seed=seed
            ),
            "genuine_two_mode": two_mode_signal(
                fs=fs, seconds=args.seconds, seed=seed
            ),
        }

        for truth_class, signal in signals.items():
            split = signal.size // 2
            train = signal[:split]
            holdout = signal[split:]
            train_mean = float(np.mean(train))
            train_sd = float(np.std(train))

            c1q = fit_continuous_lineage_candidate(
                train,
                fs,
                optimizer_maxiter=args.optimizer_maxiter,
            )
            d1q = fit_discrete_exact_candidate(
                train,
                fs,
                optimizer_maxiter=args.optimizer_maxiter,
            )
            current = compare_state_space_candidates(
                train,
                fs,
                optimizer_maxiter=args.optimizer_maxiter,
            )
            current_holdout = evaluate_comparison_on_holdout(current, holdout)

            c1q_holdout = score_frozen_candidate(
                holdout,
                training_mean=train_mean,
                training_sd=train_sd,
                raw_parameters=c1q.raw_parameters,
                sampling_rate_hz=fs,
                candidate="C1Q",
            )
            d1q_holdout = score_frozen_candidate(
                holdout,
                training_mean=train_mean,
                training_sd=train_sd,
                raw_parameters=d1q.raw_parameters,
                sampling_rate_hz=fs,
                candidate="D1Q",
            )
            structure = structural_metrics(holdout)

            rows.append(
                {
                    "truth_class": truth_class,
                    "seed": seed,
                    "training_samples": int(train.size),
                    "holdout_samples": int(holdout.size),
                    "C1Q_training_bic": c1q.bic,
                    "C1Q_training_nll": c1q.negative_log_likelihood,
                    "C1Q_fitted_chi": c1q.parameters["damping_ratio"],
                    "C1Q_fitted_g": c1q.parameters["g"],
                    **{
                        f"C1Q_holdout_{k}": v
                        for k, v in c1q_holdout.items()
                    },
                    "D1Q_training_bic": d1q.bic,
                    "D1Q_training_nll": d1q.negative_log_likelihood,
                    "D1Q_fitted_chi": d1q.parameters["damping_ratio"],
                    "D1Q_fitted_h": d1q.parameters["h"],
                    "D1Q_implied_continuous_g": d1q.parameters[
                        "implied_continuous_g"
                    ],
                    **{
                        f"D1Q_holdout_{k}": v
                        for k, v in d1q_holdout.items()
                    },
                    "D1Q_minus_C1Q_training_nll": (
                        d1q.negative_log_likelihood
                        - c1q.negative_log_likelihood
                    ),
                    "D1Q_minus_C1Q_holdout_nll_per_sample": (
                        d1q_holdout["negative_log_likelihood_per_sample"]
                        - c1q_holdout["negative_log_likelihood_per_sample"]
                    ),
                    "A012_training_bic_winner": current.bic_winner,
                    "A012_training_bic_margin_to_second": current.bic_margin_to_second,
                    "A012_holdout_raw_winner": current_holdout["raw_winner"],
                    "A012_holdout_interpretable_winner": current_holdout[
                        "interpretable_winner"
                    ],
                    "A012_holdout_margin_to_second_per_sample": current_holdout[
                        "margin_to_second_per_sample"
                    ],
                    **structure,
                }
            )

    numeric_metrics = (
        "C1Q_holdout_negative_log_likelihood_per_sample",
        "C1Q_holdout_innovation_max_abs_autocorrelation",
        "D1Q_holdout_negative_log_likelihood_per_sample",
        "D1Q_holdout_innovation_max_abs_autocorrelation",
        "D1Q_minus_C1Q_holdout_nll_per_sample",
        "recurrence_normalized_holdlag_rms",
        "hankel_s3_over_s2",
    )

    classes = sorted({row["truth_class"] for row in rows})
    summary = {
        truth_class: {
            metric: quantiles([row[metric] for row in rows if row["truth_class"] == truth_class])
            for metric in numeric_metrics
        }
        for truth_class in classes
    }

    c_reference = {
        "C_g0",
        "C_g_neg075",
        "C_g_pos075",
    }
    discrimination = {}
    for target in (
        "colored_phi_0_7",
        "genuine_two_mode",
        "D_not_C_neg",
        "D_not_C_pos",
        "S_not_D_neg",
        "S_not_D_pos",
    ):
        discrimination[target] = {
            metric: rank_auc(
                [row[metric] for row in rows if row["truth_class"] in c_reference],
                [row[metric] for row in rows if row["truth_class"] == target],
            )
            for metric in numeric_metrics
        }

    payload = {
        "status": "PREDECISION_CALIBRATION_ONLY",
        "licenses_real_eeg_local_chi": False,
        "defines_refusal_threshold": False,
        "changes_production_estimator": False,
        "holdout_semantics": "frozen_parameter_cold_start_generalization_after_burn",
        "fine_sampling_rate_hz": fs,
        "seconds_total": args.seconds,
        "seconds_training": args.seconds / 2.0,
        "seconds_holdout": args.seconds / 2.0,
        "seed_count": args.seeds,
        "truth_coordinates": {
            "A": A,
            "natural_frequency_hz": fn,
            "zeta": zeta,
            "H_C": H_C,
            "H_D": H_D,
            "H_D_not_C_negative": H_DC_neg,
            "H_D_not_C_positive": H_DC_pos,
            "H_S_not_D_negative": H_SD_neg,
            "H_S_not_D_positive": H_SD_pos,
        },
        "rows": rows,
        "summary": summary,
        "threshold_free_rank_auc_against_C_interiors": discrimination,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "row_count": len(rows),
                "status": payload["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
