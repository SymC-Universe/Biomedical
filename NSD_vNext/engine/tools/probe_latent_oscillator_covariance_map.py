#!/usr/bin/env python3
"""Known-truth operating-region map for the latent covariance oscillator route.

This runs before any real EEG fit. It maps recovery, observation-noise handling,
and model-fit diagnostics across frequency, damping, duration, and additive
white observation noise under the estimator's own generating model.
"""

from __future__ import annotations

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


FS_HZ = 256.0
FREQUENCIES_HZ = (5.0, 10.0, 20.0)
DAMPING_RATIOS = (0.20, 0.50, 0.80, 0.95)
DURATIONS_S = (10.0, 30.0, 120.0)
MEASUREMENT_NOISE_TO_LATENT_SD = (0.0, 0.25, 0.50, 1.0)
SEEDS = (20260914, 20260915)


def _summary(values: list[float]) -> dict[str, float | int | None]:
    finite = np.asarray([value for value in values if math.isfinite(value)], dtype=float)
    if finite.size == 0:
        return {"n": 0, "median": None, "minimum": None, "maximum": None}
    return {
        "n": int(finite.size),
        "median": float(np.median(finite)),
        "minimum": float(np.min(finite)),
        "maximum": float(np.max(finite)),
    }


def main() -> int:
    rows: list[dict[str, object]] = []
    for frequency_hz in FREQUENCIES_HZ:
        for zeta in DAMPING_RATIOS:
            truth = LatentOscillatorTruth(frequency_hz, zeta, FS_HZ)
            for duration_s in DURATIONS_S:
                for noise_ratio in MEASUREMENT_NOISE_TO_LATENT_SD:
                    fits: list[dict[str, object]] = []
                    expected_latent_fraction = 1.0 / (1.0 + noise_ratio**2)
                    expected_noise_to_latent_variance = noise_ratio**2
                    for seed in SEEDS:
                        signal = simulate_latent_oscillator(
                            truth,
                            seconds=duration_s,
                            measurement_noise_to_latent_sd=noise_ratio,
                            seed=seed,
                        )
                        result = fit_latent_oscillator_covariance(
                            signal,
                            FS_HZ,
                            fmin_hz=1.0,
                            fmax_hz=45.0,
                            max_lag_seconds=1.0,
                        )
                        item: dict[str, object] = {
                            "seed": seed,
                            "admitted": result.admitted,
                            "refusal_code": result.refusal_code.value if result.refusal_code else None,
                        }
                        if result.admitted:
                            assert result.natural_frequency_hz is not None
                            assert result.damping_ratio is not None
                            assert result.latent_variance_fraction is not None
                            assert result.observation_noise_to_latent_variance_ratio is not None
                            assert result.autocorrelation_r_squared is not None
                            item.update(
                                {
                                    "frequency_relative_error": abs(result.natural_frequency_hz - frequency_hz) / frequency_hz,
                                    "damping_absolute_error": abs(result.damping_ratio - zeta),
                                    "latent_fraction_absolute_error": abs(result.latent_variance_fraction - expected_latent_fraction),
                                    "noise_to_latent_variance_absolute_error": abs(result.observation_noise_to_latent_variance_ratio - expected_noise_to_latent_variance),
                                    "autocorrelation_r_squared": result.autocorrelation_r_squared,
                                }
                            )
                        fits.append(item)

                    admitted = [item for item in fits if item["admitted"]]
                    rows.append(
                        {
                            "truth": {
                                "natural_frequency_hz": frequency_hz,
                                "damping_ratio": zeta,
                                "damped_frequency_hz": truth.damped_frequency_hz,
                                "expected_latent_variance_fraction": expected_latent_fraction,
                                "expected_observation_noise_to_latent_variance_ratio": expected_noise_to_latent_variance,
                            },
                            "duration_seconds": duration_s,
                            "measurement_noise_to_latent_sd": noise_ratio,
                            "n_seeds": len(SEEDS),
                            "admission_rate": len(admitted) / len(fits),
                            "frequency_relative_error": _summary([float(item["frequency_relative_error"]) for item in admitted]),
                            "damping_absolute_error": _summary([float(item["damping_absolute_error"]) for item in admitted]),
                            "latent_fraction_absolute_error": _summary([float(item["latent_fraction_absolute_error"]) for item in admitted]),
                            "noise_variance_ratio_absolute_error": _summary([float(item["noise_to_latent_variance_absolute_error"]) for item in admitted]),
                            "autocorrelation_r_squared": _summary([float(item["autocorrelation_r_squared"]) for item in admitted]),
                            "refusal_codes": sorted({str(item["refusal_code"]) for item in fits if item["refusal_code"] is not None}),
                        }
                    )

    output = {
        "scope": "latent damped-rotation covariance estimator known-truth map",
        "sampling_rate_hz": FS_HZ,
        "frequencies_hz": list(FREQUENCIES_HZ),
        "damping_ratios": list(DAMPING_RATIOS),
        "durations_seconds": list(DURATIONS_S),
        "measurement_noise_to_latent_sd": list(MEASUREMENT_NOISE_TO_LATENT_SD),
        "seeds": list(SEEDS),
        "rows": rows,
        "interpretation_ceiling": "known-truth recovery under the stated latent oscillator plus white observation-noise model only; no real EEG, diagnostic, prognostic, or whole-system claim",
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
