#!/usr/bin/env python3
"""Finite-sample structural-order calibration map for NSD Bio Chi.

Known-truth qualification only. This probe maps dimensionless positive-lag
Hankel/recurrence diagnostics across exact second-order, out-of-C but still
second-order, colored third-pole, and genuine two-mode truths.

No admission threshold is selected. Every fine/coarse pair is generated from
the same realization and exact deterministic decimation by two.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import brentq

from nsd_engine.latent_oscillator_covariance import (
    LatentOscillatorTruth,
    simulate_latent_oscillator,
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
        [[math.cos(theta), -math.sin(theta)],
         [math.sin(theta),  math.cos(theta)]],
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


def scalar_positive_bound(A: float, rho: float, xi: float, sign: int, start: float) -> float:
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


def sample_positive_lag_covariances(signal: np.ndarray, max_lag: int = 10):
    x = np.asarray(signal, dtype=float)
    x = x - float(np.mean(x))
    variance = float(np.mean(x * x))
    if variance <= 0.0:
        raise ValueError("zero variance")
    x = x / math.sqrt(variance)
    return np.asarray(
        [float(np.mean(x[:-lag] * x[lag:])) for lag in range(1, max_lag + 1)],
        dtype=float,
    )


def structural_metrics(signal: np.ndarray):
    gamma = sample_positive_lag_covariances(signal, max_lag=10)
    H3 = np.asarray(
        [[gamma[i + j] for j in range(3)] for i in range(3)],
        dtype=float,
    )
    singular = np.linalg.svd(H3, compute_uv=False)
    s3_over_s2 = float(singular[2] / max(singular[1], 1e-15))
    s3_over_s1 = float(singular[2] / max(singular[0], 1e-15))

    # Fit the order-two positive-lag recurrence on lags 1..5, then score
    # held-lag residuals 6..10. This is within-sequence structural mapping,
    # not a production train/test split.
    rows = []
    targets = []
    # gamma array index j is lag j+1.
    for k in range(1, 4):
        rows.append([gamma[k], -gamma[k - 1]])
        targets.append(gamma[k + 1])
    coeff, _, _, _ = np.linalg.lstsq(
        np.asarray(rows), np.asarray(targets), rcond=None
    )
    a_hat, b_hat = (float(coeff[0]), float(coeff[1]))

    residuals = []
    references = []
    for k in range(4, 8):
        predicted = a_hat * gamma[k] - b_hat * gamma[k - 1]
        observed = gamma[k + 1]
        residuals.append(observed - predicted)
        references.append(observed)
    residual_rms = float(math.sqrt(np.mean(np.asarray(residuals) ** 2)))
    reference_rms = float(math.sqrt(np.mean(np.asarray(references) ** 2)))
    normalized_residual_rms = residual_rms / max(reference_rms, 1e-15)

    return {
        "hankel_s3_over_s2": s3_over_s2,
        "hankel_s3_over_s1": s3_over_s1,
        "recurrence_normalized_holdlag_rms": normalized_residual_rms,
        "fitted_a": a_hat,
        "fitted_b": b_hat,
    }


def quantiles(values):
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


def rank_auc(reference, target):
    """Threshold-free P(target > reference), with half-credit for ties."""
    ref = np.asarray(reference, dtype=float)
    tar = np.asarray(target, dtype=float)
    greater = 0.0
    total = 0
    for x in tar:
        greater += float(np.sum(x > ref))
        greater += 0.5 * float(np.sum(x == ref))
        total += ref.size
    return float(greater / total) if total else float("nan")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fs", type=float, default=256.0)
    parser.add_argument("--seconds", type=float, default=30.0)
    parser.add_argument("--seeds", type=int, default=40)
    args = parser.parse_args()

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

    H_DC = H_C + 0.5 * (H_D - H_C)
    H_SD = 0.5 * (H_D + S_pos)

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
            "D_not_C": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_DC, seed=seed + 2000
            ),
            "S_not_D": arma_second_order_signal(
                fs=fs, seconds=args.seconds, A=A, rho=rho, xi=xi, H=H_SD, seed=seed + 4000
            ),
            "colored_phi_0_7": colored_process_signal(
                fs=fs, seconds=args.seconds, seed=seed
            ),
            "genuine_two_mode": two_mode_signal(
                fs=fs, seconds=args.seconds, seed=seed
            ),
        }
        for truth_class, fine in signals.items():
            for rate_label, signal in (
                ("fine", fine),
                ("coarse_decimate2", fine[::2]),
            ):
                metrics = structural_metrics(signal)
                rows.append({
                    "truth_class": truth_class,
                    "seed": seed,
                    "rate_label": rate_label,
                    "sampling_rate_hz": fs if rate_label == "fine" else fs / 2.0,
                    **metrics,
                })

    summary = {}
    metrics = (
        "hankel_s3_over_s2",
        "hankel_s3_over_s1",
        "recurrence_normalized_holdlag_rms",
    )
    classes = sorted({row["truth_class"] for row in rows})
    rates = ("fine", "coarse_decimate2")
    for truth_class in classes:
        summary[truth_class] = {}
        for rate_label in rates:
            subset = [
                row for row in rows
                if row["truth_class"] == truth_class and row["rate_label"] == rate_label
            ]
            summary[truth_class][rate_label] = {
                metric: quantiles([row[metric] for row in subset])
                for metric in metrics
            }

    reference_classes = {
        "C_g0", "C_g_neg075", "C_g_pos075", "D_not_C", "S_not_D"
    }
    discrimination = {}
    for target_class in ("colored_phi_0_7", "genuine_two_mode"):
        discrimination[target_class] = {}
        for rate_label in rates:
            reference_rows = [
                row for row in rows
                if row["truth_class"] in reference_classes
                and row["rate_label"] == rate_label
            ]
            target_rows = [
                row for row in rows
                if row["truth_class"] == target_class
                and row["rate_label"] == rate_label
            ]
            discrimination[target_class][rate_label] = {
                metric: rank_auc(
                    [row[metric] for row in reference_rows],
                    [row[metric] for row in target_rows],
                )
                for metric in metrics
            }

    payload = {
        "status": "PREDECISION_CALIBRATION_ONLY",
        "licenses_real_eeg_local_chi": False,
        "defines_structural_order_threshold": False,
        "fine_sampling_rate_hz": fs,
        "coarse_sampling_rate_hz": fs / 2.0,
        "seconds": args.seconds,
        "seed_count": args.seeds,
        "truth_coordinates": {
            "A": A,
            "natural_frequency_hz": fn,
            "zeta": zeta,
            "H_C": H_C,
            "H_D": H_D,
            "H_D_not_C": H_DC,
            "H_S_not_D": H_SD,
        },
        "rows": rows,
        "summary": summary,
        "threshold_free_rank_auc": discrimination,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "row_count": len(rows),
        "status": payload["status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
