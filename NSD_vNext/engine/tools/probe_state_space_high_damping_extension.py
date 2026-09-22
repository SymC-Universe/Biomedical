#!/usr/bin/env python3
"""Prospective high-damping A0/A1/A2 operating-boundary extension.

P0-Q known-truth qualification only. The scientific model families and search
settings are unchanged. This script maps how duration and observation noise
interact with increasingly high underdamped truth.
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
    simulate_latent_oscillator,
)
from nsd_engine.state_space_adequacy import compare_state_space_candidates


FS = 256.0
FREQUENCIES = (5.0, 10.0, 20.0)
DAMPING_RATIOS = (0.80, 0.90, 0.95)
NOISE_RATIOS = (0.0, 1.0)
SEEDS = (0, 1, 2)


def _median(values):
    usable = [float(x) for x in values if x is not None and math.isfinite(float(x))]
    return float(np.median(usable)) if usable else None


def _fit_record(fit):
    return {
        "family": fit.family,
        "success": fit.success,
        "bic": fit.bic,
        "negative_log_likelihood": fit.negative_log_likelihood,
        "candidate_start_count": fit.candidate_start_count,
        "attempted_start_count": fit.attempted_start_count,
        "converged_start_count": fit.converged_start_count,
        "near_optimal_start_count": fit.near_optimal_start_count,
        "start_nll_range": fit.start_nll_range,
        "innovation_max_abs_autocorrelation": fit.innovation_max_abs_autocorrelation,
        "innovation_rms": fit.innovation_rms,
        "parameters": dict(fit.parameters),
        "near_optimal_parameter_ranges": {
            key: list(value) for key, value in fit.near_optimal_parameter_ranges.items()
        },
    }


def run(duration_seconds: float) -> dict[str, object]:
    if duration_seconds not in (30.0, 120.0):
        raise ValueError("duration_seconds must be 30 or 120 for frozen v0.1")

    rows = []
    for frequency_hz in FREQUENCIES:
        for damping_ratio in DAMPING_RATIOS:
            for noise_ratio in NOISE_RATIOS:
                for seed in SEEDS:
                    signal = simulate_latent_oscillator(
                        LatentOscillatorTruth(
                            frequency_hz,
                            damping_ratio,
                            FS,
                        ),
                        seconds=duration_seconds,
                        measurement_noise_to_latent_sd=noise_ratio,
                        seed=seed,
                    )
                    comparison = compare_state_space_candidates(
                        signal,
                        FS,
                        fmin_hz=1.0,
                        fmax_hz=45.0,
                        optimizer_maxiter=80,
                    )
                    a1 = comparison.by_family("A1")
                    rows.append(
                        {
                            "frequency_hz": frequency_hz,
                            "damping_ratio": damping_ratio,
                            "duration_seconds": duration_seconds,
                            "observation_noise_to_latent_sd": noise_ratio,
                            "seed": seed,
                            "bic_winner": comparison.bic_winner,
                            "bic_margin_to_second": comparison.bic_margin_to_second,
                            "a1_frequency_relative_error": abs(
                                a1.parameters["natural_frequency_hz"] - frequency_hz
                            ) / frequency_hz,
                            "a1_damping_absolute_error": abs(
                                a1.parameters["damping_ratio"] - damping_ratio
                            ),
                            "a1_latent_fraction": a1.parameters["latent_fraction"],
                            "a1_rho": a1.parameters["rho"],
                            "a1_innovation_max_abs_autocorrelation":
                                a1.innovation_max_abs_autocorrelation,
                            "a1_near_optimal_start_count":
                                a1.near_optimal_start_count,
                            "a1_near_optimal_parameter_ranges":
                                {
                                    key: list(value)
                                    for key, value in
                                    a1.near_optimal_parameter_ranges.items()
                                },
                            "fits": [_fit_record(fit) for fit in comparison.fits],
                        }
                    )

    summaries = []
    for frequency_hz in FREQUENCIES:
        for damping_ratio in DAMPING_RATIOS:
            for noise_ratio in NOISE_RATIOS:
                subset = [
                    row for row in rows
                    if row["frequency_hz"] == frequency_hz
                    and row["damping_ratio"] == damping_ratio
                    and row["observation_noise_to_latent_sd"] == noise_ratio
                ]
                summaries.append(
                    {
                        "frequency_hz": frequency_hz,
                        "damping_ratio": damping_ratio,
                        "duration_seconds": duration_seconds,
                        "observation_noise_to_latent_sd": noise_ratio,
                        "n": len(subset),
                        "winner_counts": {
                            family: sum(row["bic_winner"] == family for row in subset)
                            for family in ("A0", "A1", "A2")
                        },
                        "a1_selection_rate": float(
                            np.mean([row["bic_winner"] == "A1" for row in subset])
                        ),
                        "median_a1_frequency_relative_error": _median(
                            [row["a1_frequency_relative_error"] for row in subset]
                        ),
                        "median_a1_damping_absolute_error": _median(
                            [row["a1_damping_absolute_error"] for row in subset]
                        ),
                        "median_a1_innovation_max_abs_autocorrelation": _median(
                            [
                                row["a1_innovation_max_abs_autocorrelation"]
                                for row in subset
                            ]
                        ),
                        "median_bic_margin_to_second": _median(
                            [row["bic_margin_to_second"] for row in subset]
                        ),
                    }
                )

    return {
        "schema": "NSD_STATE_SPACE_HIGH_DAMPING_EXTENSION_V0_1",
        "purpose": "P0-Q high-damping identifiability/operating-boundary extension",
        "sampling_rate_hz": FS,
        "duration_seconds": duration_seconds,
        "frequencies_hz": list(FREQUENCIES),
        "damping_ratios": list(DAMPING_RATIOS),
        "observation_noise_to_latent_sd": list(NOISE_RATIOS),
        "seeds": list(SEEDS),
        "summaries": summaries,
        "rows": rows,
        "interpretation_ceiling": (
            "Known-truth P0-Q only. The result may map candidate limits but does "
            "not freeze a production operating boundary or license real-EEG "
            "modal damping/local chi."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration-seconds", type=float, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.duration_seconds)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["summaries"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
