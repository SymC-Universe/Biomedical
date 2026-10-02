#!/usr/bin/env python3
"""Map failure behavior and model-adequacy diagnostics for M2.

This is a known-truth / known-misspecification exercise. It does not tune a
clinical threshold and it does not apply the estimator to EEG.

The first adversarial pass showed that the narrow single-oscillator covariance
estimator can mechanically return an oscillatory fit for signals that are not a
single stationary latent oscillator. This pass therefore adds three diagnostic
families without changing the production admission rule:

1. single oscillator versus a non-oscillatory AR(1)-like covariance model;
2. single oscillator versus a two-oscillator covariance model;
3. split-half parameter stability.

The covariance information criteria below are deliberately called
"pseudo-BIC": autocorrelation lags are correlated observations, so these values
are qualification diagnostics rather than formal likelihood-based BIC values.
A later full state-space likelihood route can replace them if warranted.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import least_squares

ENGINE_ROOT = Path(__file__).resolve().parents[1]
if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

from nsd_engine.latent_oscillator_covariance import (
    LatentOscillatorTruth,
    fit_latent_oscillator_covariance,
    simulate_latent_oscillator,
)


FS = 256.0
SECONDS = 30.0
SEEDS = (0, 1, 2)
FMIN_HZ = 1.0
FMAX_HZ = 45.0
MAX_LAG_SECONDS = 1.0


def _standardize(x: np.ndarray) -> np.ndarray:
    y = np.asarray(x, dtype=float)
    y = y - float(np.mean(y))
    sd = float(np.std(y))
    if sd <= 0:
        return y
    return y / sd


def _colored_noise(n: int, phi: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    eps = rng.normal(size=n)
    x = np.zeros(n, dtype=float)
    scale = math.sqrt(max(1e-12, 1.0 - phi * phi))
    for i in range(1, n):
        x[i] = phi * x[i - 1] + scale * eps[i]
    return _standardize(x)


def _single(seed: int) -> np.ndarray:
    truth = LatentOscillatorTruth(10.0, 0.30, FS)
    return simulate_latent_oscillator(
        truth, seconds=SECONDS, measurement_noise_to_latent_sd=0.5, seed=seed
    )


def _two_modes(seed: int, close: bool = False) -> np.ndarray:
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.25, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    second_freq = 12.0 if close else 20.0
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(second_freq, 0.35, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed + 100,
    )
    rng = np.random.default_rng(seed + 200)
    y = 0.8 * _standardize(first) + 0.8 * _standardize(second)
    y += rng.normal(0.0, 0.35, size=y.size)
    return _standardize(y)


def _colored_observation(seed: int) -> np.ndarray:
    latent = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    noise = _colored_noise(latent.size, phi=0.85, seed=seed + 300)
    return _standardize(_standardize(latent) + 0.7 * noise)


def _frequency_shift(seed: int) -> np.ndarray:
    half = SECONDS / 2.0
    a = simulate_latent_oscillator(
        LatentOscillatorTruth(8.0, 0.25, FS),
        seconds=half,
        measurement_noise_to_latent_sd=0.25,
        seed=seed,
    )
    b = simulate_latent_oscillator(
        LatentOscillatorTruth(13.0, 0.25, FS),
        seconds=half,
        measurement_noise_to_latent_sd=0.25,
        seed=seed + 400,
    )
    return _standardize(np.concatenate([a, b]))


def _bursty(seed: int) -> np.ndarray:
    latent = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.20, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    n = latent.size
    t = np.arange(n) / FS
    envelope = np.zeros(n)
    for start in (2.0, 8.0, 15.0, 23.0):
        envelope[(t >= start) & (t < start + 2.0)] = 1.0
    rng = np.random.default_rng(seed + 500)
    return _standardize(envelope * latent + rng.normal(0.0, 0.25, size=n))


def _ar1_nonoscillatory(seed: int) -> np.ndarray:
    return _colored_noise(int(round(FS * SECONDS)), phi=0.97, seed=seed + 600)


def _white_noise(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 700)
    return rng.normal(size=int(round(FS * SECONDS)))


GENERATORS = {
    "single_valid_truth": _single,
    "two_modes_separated": lambda seed: _two_modes(seed, close=False),
    "two_modes_close": lambda seed: _two_modes(seed, close=True),
    "colored_observation_noise": _colored_observation,
    "frequency_shift_mid_record": _frequency_shift,
    "finite_bursts": _bursty,
    "nonoscillatory_ar1": _ar1_nonoscillatory,
    "white_noise": _white_noise,
}


def _median(values):
    vals = [float(v) for v in values if v is not None and math.isfinite(float(v))]
    return float(np.median(vals)) if vals else None


def _normalized_autocorrelation(signal: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(signal, dtype=np.float64)
    centered = values - float(np.mean(values))
    variance = float(np.mean(centered**2))
    max_lag = min(int(round(MAX_LAG_SECONDS * FS)), values.size // 8)
    lags = np.arange(1, max_lag + 1, dtype=np.float64)
    correlations = np.asarray(
        [
            float(np.dot(centered[:-lag], centered[lag:]) / (values.size - lag) / variance)
            for lag in range(1, max_lag + 1)
        ],
        dtype=np.float64,
    )
    return lags, correlations


def _pseudo_bic(rss: float, n: int, k: int) -> float:
    scaled = max(float(rss) / max(1, n), 1e-15)
    return float(n * math.log(scaled) + k * math.log(max(2, n)))


def _fit_ar1_covariance(lags: np.ndarray, correlations: np.ndarray) -> dict[str, float]:
    def residual(parameters: np.ndarray) -> np.ndarray:
        b, rho = parameters
        return b * (rho**lags) - correlations

    best = None
    for b0 in (0.2, 0.5, 0.9):
        for rho0 in (0.5, 0.8, 0.95, 0.99):
            fit = least_squares(
                residual,
                x0=np.asarray([b0, rho0], dtype=np.float64),
                bounds=(
                    np.asarray([1e-6, 1e-6], dtype=np.float64),
                    np.asarray([0.999999, 0.999999], dtype=np.float64),
                ),
                method="trf",
                loss="soft_l1",
                f_scale=0.05,
                max_nfev=2000,
            )
            if best is None or fit.cost < best.cost:
                best = fit

    b, rho = (float(value) for value in best.x)
    predicted = b * (rho**lags)
    rss = float(np.sum((correlations - predicted) ** 2))
    return {
        "latent_fraction": b,
        "rho": rho,
        "rss": rss,
        "pseudo_bic": _pseudo_bic(rss, len(lags), 2),
    }


def _fft_candidate_frequencies(signal: np.ndarray) -> list[float]:
    centered = np.asarray(signal, dtype=float) - float(np.mean(signal))
    power = np.abs(np.fft.rfft(centered)) ** 2
    freqs = np.fft.rfftfreq(centered.size, d=1.0 / FS)
    mask = (freqs >= FMIN_HZ) & (freqs <= FMAX_HZ)
    candidate_freqs = freqs[mask]
    candidate_power = power[mask]
    if candidate_freqs.size == 0:
        return [10.0, 20.0]

    order = np.argsort(candidate_power)[::-1]
    chosen: list[float] = []
    for index in order:
        frequency = float(candidate_freqs[int(index)])
        if all(abs(frequency - existing) >= 1.0 for existing in chosen):
            chosen.append(frequency)
        if len(chosen) == 4:
            break

    if len(chosen) < 2:
        primary = chosen[0] if chosen else 10.0
        alternate = min(FMAX_HZ - 0.5, max(FMIN_HZ + 0.5, primary * 1.5))
        if abs(alternate - primary) < 1.0:
            alternate = min(FMAX_HZ - 0.5, primary + 5.0)
        chosen.append(alternate)
    return chosen


def _softmax_three(u1: float, u2: float) -> tuple[float, float, float]:
    logits = np.asarray([u1, u2, 0.0], dtype=np.float64)
    logits -= float(np.max(logits))
    weights = np.exp(logits)
    weights /= float(np.sum(weights))
    return float(weights[0]), float(weights[1]), float(weights[2])


def _fit_two_oscillator_covariance(
    signal: np.ndarray,
    lags: np.ndarray,
    correlations: np.ndarray,
) -> dict[str, object]:
    theta_min = 2.0 * math.pi * FMIN_HZ / FS
    theta_max = 2.0 * math.pi * FMAX_HZ / FS
    candidates = _fft_candidate_frequencies(signal)

    def unpack(parameters: np.ndarray):
        u1, u2, rho1, rho2, theta1, theta2 = (float(v) for v in parameters)
        b1, b2, residual_fraction = _softmax_three(u1, u2)
        return b1, b2, residual_fraction, rho1, rho2, theta1, theta2

    def residual(parameters: np.ndarray) -> np.ndarray:
        b1, b2, _, rho1, rho2, theta1, theta2 = unpack(parameters)
        predicted = (
            b1 * (rho1**lags) * np.cos(theta1 * lags)
            + b2 * (rho2**lags) * np.cos(theta2 * lags)
        )
        return predicted - correlations

    starts = []
    pairs: list[tuple[float, float]] = []
    for first in candidates:
        for second in candidates:
            if second <= first or abs(second - first) < 0.75:
                continue
            pairs.append((first, second))
    primary = candidates[0]
    pairs.extend(
        [
            (
                max(FMIN_HZ + 0.25, primary * 0.8),
                min(FMAX_HZ - 0.25, primary * 1.2),
            ),
            (
                max(FMIN_HZ + 0.25, primary),
                min(FMAX_HZ - 0.25, primary + 8.0),
            ),
            (8.0, 20.0),
        ]
    )

    unique_pairs = []
    for pair in pairs:
        a, b = sorted(pair)
        if b - a < 0.75:
            continue
        rounded = (round(a, 3), round(b, 3))
        if rounded not in unique_pairs:
            unique_pairs.append(rounded)

    for first, second in unique_pairs[:12]:
        theta1 = 2.0 * math.pi * first / FS
        theta2 = 2.0 * math.pi * second / FS
        for rho0 in (0.75, 0.92, 0.985):
            starts.append((0.0, 0.0, rho0, rho0, theta1, theta2))

    best = None
    lower = np.asarray([-8.0, -8.0, 1e-4, 1e-4, theta_min, theta_min])
    upper = np.asarray([8.0, 8.0, 0.999999, 0.999999, theta_max, theta_max])
    for start in starts:
        fit = least_squares(
            residual,
            x0=np.asarray(start, dtype=np.float64),
            bounds=(lower, upper),
            method="trf",
            loss="soft_l1",
            f_scale=0.05,
            max_nfev=3500,
        )
        if best is None or fit.cost < best.cost:
            best = fit

    b1, b2, residual_fraction, rho1, rho2, theta1, theta2 = unpack(best.x)
    components = [
        {
            "latent_fraction": b1,
            "rho": rho1,
            "frequency_hz": theta1 * FS / (2.0 * math.pi),
        },
        {
            "latent_fraction": b2,
            "rho": rho2,
            "frequency_hz": theta2 * FS / (2.0 * math.pi),
        },
    ]
    components.sort(key=lambda item: item["frequency_hz"])
    predicted = sum(
        component["latent_fraction"]
        * (component["rho"] ** lags)
        * np.cos((2.0 * math.pi * component["frequency_hz"] / FS) * lags)
        for component in components
    )
    rss = float(np.sum((correlations - predicted) ** 2))
    return {
        "components": components,
        "residual_zero_lag_fraction": residual_fraction,
        "rss": rss,
        "pseudo_bic": _pseudo_bic(rss, len(lags), 6),
    }


def _single_oscillator_diagnostics(
    signal: np.ndarray,
    estimate,
    lags: np.ndarray,
    correlations: np.ndarray,
) -> dict[str, float | None]:
    if not estimate.admitted:
        return {"rss": None, "pseudo_bic": None}
    predicted = (
        float(estimate.latent_variance_fraction)
        * (float(estimate.rho) ** lags)
        * np.cos(float(estimate.theta_rad_per_sample) * lags)
    )
    rss = float(np.sum((correlations - predicted) ** 2))
    return {
        "rss": rss,
        "pseudo_bic": _pseudo_bic(rss, len(lags), 3),
    }


def _split_half_diagnostics(signal: np.ndarray) -> dict[str, object]:
    midpoint = len(signal) // 2
    halves = [signal[:midpoint], signal[midpoint:]]
    fits = [
        fit_latent_oscillator_covariance(
            half,
            FS,
            fmin_hz=FMIN_HZ,
            fmax_hz=FMAX_HZ,
            max_lag_seconds=MAX_LAG_SECONDS,
            min_samples=512,
        )
        for half in halves
    ]
    admitted = [fit.admitted for fit in fits]
    result: dict[str, object] = {
        "both_admitted": bool(all(admitted)),
        "first_admitted": bool(admitted[0]),
        "second_admitted": bool(admitted[1]),
    }
    if all(admitted):
        f1 = float(fits[0].natural_frequency_hz)
        f2 = float(fits[1].natural_frequency_hz)
        z1 = float(fits[0].damping_ratio)
        z2 = float(fits[1].damping_ratio)
        denominator = max(1e-12, 0.5 * (abs(f1) + abs(f2)))
        result.update(
            {
                "frequency_symmetric_relative_difference": abs(f1 - f2) / denominator,
                "damping_absolute_difference": abs(z1 - z2),
                "first_frequency_hz": f1,
                "second_frequency_hz": f2,
                "first_damping_ratio": z1,
                "second_damping_ratio": z2,
            }
        )
    else:
        result.update(
            {
                "frequency_symmetric_relative_difference": None,
                "damping_absolute_difference": None,
            }
        )
    return result


def _adequacy_diagnostics(signal: np.ndarray, estimate) -> dict[str, object]:
    lags, correlations = _normalized_autocorrelation(signal)
    single = _single_oscillator_diagnostics(signal, estimate, lags, correlations)
    ar1 = _fit_ar1_covariance(lags, correlations)
    two = _fit_two_oscillator_covariance(signal, lags, correlations)
    split = _split_half_diagnostics(signal)

    single_bic = single["pseudo_bic"]
    ar1_bic = ar1["pseudo_bic"]
    two_bic = two["pseudo_bic"]
    return {
        "lag_count": int(len(lags)),
        "single_oscillator": single,
        "ar1_covariance": ar1,
        "two_oscillator": two,
        "split_half": split,
        "pseudo_bic_single_minus_ar1": (
            float(single_bic) - float(ar1_bic)
            if single_bic is not None
            else None
        ),
        "pseudo_bic_two_minus_single": (
            float(two_bic) - float(single_bic)
            if single_bic is not None
            else None
        ),
        "interpretation": (
            "Negative single-minus-AR1 favors the single oscillator over the "
            "non-oscillatory covariance alternative. Negative two-minus-single "
            "favors a two-oscillator covariance description. These are qualification "
            "diagnostics, not formal likelihood-based information criteria."
        ),
    }


def run() -> dict[str, object]:
    rows = []
    for scenario, generator in GENERATORS.items():
        for seed in SEEDS:
            signal = generator(seed)
            estimate = fit_latent_oscillator_covariance(
                signal,
                FS,
                fmin_hz=FMIN_HZ,
                fmax_hz=FMAX_HZ,
                max_lag_seconds=MAX_LAG_SECONDS,
                min_samples=512,
            )
            diagnostics = _adequacy_diagnostics(signal, estimate)
            row = {
                "scenario": scenario,
                "seed": seed,
                "admitted": estimate.admitted,
                "refusal_code": (
                    estimate.refusal_code.value if estimate.refusal_code is not None else None
                ),
                "autocorrelation_r_squared": estimate.autocorrelation_r_squared,
                "fitted_natural_frequency_hz": estimate.natural_frequency_hz,
                "fitted_damping_ratio": estimate.damping_ratio,
                "latent_variance_fraction": estimate.latent_variance_fraction,
                "observation_noise_to_latent_variance_ratio":
                    estimate.observation_noise_to_latent_variance_ratio,
                "adequacy": diagnostics,
            }
            if scenario == "single_valid_truth" and estimate.admitted:
                row["frequency_relative_error"] = abs(
                    float(estimate.natural_frequency_hz) - 10.0
                ) / 10.0
                row["damping_absolute_error"] = abs(
                    float(estimate.damping_ratio) - 0.30
                )
            rows.append(row)

    summaries = {}
    for scenario in GENERATORS:
        subset = [row for row in rows if row["scenario"] == scenario]
        admitted = [row for row in subset if row["admitted"]]
        summaries[scenario] = {
            "n": len(subset),
            "admission_rate": len(admitted) / len(subset),
            "median_autocorrelation_r_squared": _median(
                [row["autocorrelation_r_squared"] for row in admitted]
            ),
            "median_fitted_natural_frequency_hz": _median(
                [row["fitted_natural_frequency_hz"] for row in admitted]
            ),
            "median_fitted_damping_ratio": _median(
                [row["fitted_damping_ratio"] for row in admitted]
            ),
            "median_frequency_relative_error_valid_truth": _median(
                [row.get("frequency_relative_error") for row in admitted]
            ),
            "median_damping_absolute_error_valid_truth": _median(
                [row.get("damping_absolute_error") for row in admitted]
            ),
            "median_pseudo_bic_single_minus_ar1": _median(
                [
                    row["adequacy"]["pseudo_bic_single_minus_ar1"]
                    for row in admitted
                ]
            ),
            "median_pseudo_bic_two_minus_single": _median(
                [
                    row["adequacy"]["pseudo_bic_two_minus_single"]
                    for row in admitted
                ]
            ),
            "median_split_half_frequency_symmetric_relative_difference": _median(
                [
                    row["adequacy"]["split_half"][
                        "frequency_symmetric_relative_difference"
                    ]
                    for row in admitted
                ]
            ),
            "median_split_half_damping_absolute_difference": _median(
                [
                    row["adequacy"]["split_half"]["damping_absolute_difference"]
                    for row in admitted
                ]
            ),
        }

    return {
        "route": "M2 latent oscillator covariance estimator",
        "scope": "known-truth / known-misspecification adversarial adequacy map",
        "sampling_rate_hz": FS,
        "duration_seconds": SECONDS,
        "seeds": list(SEEDS),
        "summaries": summaries,
        "rows": rows,
        "interpretation": (
            "Admissions in misspecified scenarios are not successes. The added "
            "alternative-model and split-half diagnostics are used to discover an "
            "error-aware operating region before any real-EEG admission rule is frozen."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["summaries"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
