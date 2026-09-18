#!/usr/bin/env python3
"""Map failure behavior of the M2 latent-oscillator covariance estimator.

This is a known-truth / known-misspecification exercise. It does not tune a
clinical threshold and it does not apply the estimator to EEG. The purpose is
to see when a single latent damped oscillator is incorrectly admitted when the
generator is not a single stationary oscillator with white observation noise.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np

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


def run() -> dict[str, object]:
    rows = []
    for scenario, generator in GENERATORS.items():
        for seed in SEEDS:
            signal = generator(seed)
            estimate = fit_latent_oscillator_covariance(
                signal,
                FS,
                fmin_hz=1.0,
                fmax_hz=45.0,
                max_lag_seconds=1.0,
                min_samples=512,
            )
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
        }

    return {
        "route": "M2 latent oscillator covariance estimator",
        "scope": "known-truth / known-misspecification adversarial map",
        "sampling_rate_hz": FS,
        "duration_seconds": SECONDS,
        "seeds": list(SEEDS),
        "summaries": summaries,
        "rows": rows,
        "interpretation": (
            "Admissions in misspecified scenarios are not successes; they expose where "
            "an explicit model-adequacy/refusal rule is required before real EEG."
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
