#!/usr/bin/env python3
"""Map AR(2) modal recovery and refusal across known-truth operating regions.

The map sweeps natural frequency, damping ratio, duration, and additive
measurement-noise ratio. It is deliberately label-free and precedes any attempt
to fit the estimator to real EEG.
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

from nsd_engine.ar2_modal import AR2Truth, fit_ar2_modal, simulate_ar2_truth


FS_HZ = 256.0
FREQUENCIES_HZ = (5.0, 10.0, 20.0)
DAMPING_RATIOS = (0.10, 0.20, 0.40, 0.60, 0.80, 0.90, 0.95)
DURATIONS_S = (10.0, 30.0, 120.0)
MEASUREMENT_NOISE_TO_SIGNAL_SD = (0.0, 0.25, 0.50, 1.0)
SEEDS = (20260914, 20260915, 20260916)


def _summary(values: list[float]) -> dict[str, float | None]:
    finite = np.asarray([v for v in values if math.isfinite(v)], dtype=float)
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
            truth = AR2Truth(frequency_hz, zeta, FS_HZ)
            for duration_s in DURATIONS_S:
                for noise_ratio in MEASUREMENT_NOISE_TO_SIGNAL_SD:
                    fits: list[dict[str, object]] = []
                    for seed in SEEDS:
                        clean = simulate_ar2_truth(
                            truth,
                            seconds=duration_s,
                            innovation_sd=1.0,
                            measurement_noise_sd=0.0,
                            seed=seed,
                        )
                        if noise_ratio > 0:
                            rng = np.random.default_rng(seed + 1000000)
                            observed = clean + rng.normal(
                                0.0,
                                noise_ratio * float(np.std(clean)),
                                size=clean.size,
                            )
                        else:
                            observed = clean
                        result = fit_ar2_modal(observed, FS_HZ)
                        item: dict[str, object] = {
                            "seed": seed,
                            "admitted": result.admitted,
                            "refusal_code": result.refusal_code.value if result.refusal_code else None,
                        }
                        if result.admitted:
                            assert result.natural_frequency_hz is not None
                            assert result.damping_ratio is not None
                            assert result.decay_rate_per_s is not None
                            item.update(
                                {
                                    "natural_frequency_hz": result.natural_frequency_hz,
                                    "damping_ratio": result.damping_ratio,
                                    "decay_rate_per_s": result.decay_rate_per_s,
                                    "frequency_relative_error": abs(result.natural_frequency_hz - frequency_hz) / frequency_hz,
                                    "damping_absolute_error": abs(result.damping_ratio - zeta),
                                    "decay_relative_error": abs(result.decay_rate_per_s - truth.decay_rate_per_s) / truth.decay_rate_per_s,
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
                                "decay_rate_per_s": truth.decay_rate_per_s,
                            },
                            "duration_seconds": duration_s,
                            "measurement_noise_to_clean_signal_sd": noise_ratio,
                            "n_seeds": len(SEEDS),
                            "admission_rate": len(admitted) / len(fits),
                            "frequency_relative_error": _summary([
                                float(item["frequency_relative_error"]) for item in admitted
                            ]),
                            "damping_absolute_error": _summary([
                                float(item["damping_absolute_error"]) for item in admitted
                            ]),
                            "decay_relative_error": _summary([
                                float(item["decay_relative_error"]) for item in admitted
                            ]),
                            "refusal_codes": sorted({
                                str(item["refusal_code"])
                                for item in fits
                                if item["refusal_code"] is not None
                            }),
                        }
                    )

    output = {
        "scope": "AR2 output-only modal known-truth operating-region map",
        "sampling_rate_hz": FS_HZ,
        "frequencies_hz": list(FREQUENCIES_HZ),
        "damping_ratios": list(DAMPING_RATIOS),
        "durations_seconds": list(DURATIONS_S),
        "measurement_noise_to_clean_signal_sd": list(MEASUREMENT_NOISE_TO_SIGNAL_SD),
        "seeds": list(SEEDS),
        "rows": rows,
        "interpretation_ceiling": "known-truth estimator recovery/refusal only; no real EEG admission, clinical meaning, or whole-system stability claim",
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
