#!/usr/bin/env python3
"""Map the P0-Q operating region of the A0/A1/A2 likelihood candidates.

This sweep asks two separate qualification questions:

1. Where does A1 recover a true single latent oscillator across frequency,
   damping, duration, and white observation-noise conditions?
2. At what frequency separation and amplitude imbalance does A2 begin to
   distinguish two latent oscillators from A1?

No threshold from this map is a production admission rule by itself.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
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
SEEDS = (0, 1, 2)


def _standardize(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    values = values - float(np.mean(values))
    sd = float(np.std(values))
    return values / sd if sd > 0 else values


def _median(values):
    usable = [
        float(value)
        for value in values
        if value is not None and math.isfinite(float(value))
    ]
    return float(np.median(usable)) if usable else None


def _single_mode_rows() -> list[dict[str, object]]:
    rows = []
    for frequency_hz in (5.0, 10.0, 20.0):
        for damping_ratio in (0.2, 0.5, 0.8):
            for duration_seconds in (10.0, 30.0):
                for observation_noise_ratio in (0.0, 0.5, 1.0):
                    for seed in SEEDS:
                        signal = simulate_latent_oscillator(
                            LatentOscillatorTruth(
                                frequency_hz,
                                damping_ratio,
                                FS,
                            ),
                            seconds=duration_seconds,
                            measurement_noise_to_latent_sd=observation_noise_ratio,
                            seed=seed,
                        )
                        comparison = compare_state_space_candidates(
                            signal,
                            FS,
                            optimizer_maxiter=70,
                        )
                        a1 = comparison.by_family("A1")
                        fit_diagnostics = {
                            fit.family: {
                                "success": fit.success,
                                "bic": fit.bic,
                                "negative_log_likelihood":
                                    fit.negative_log_likelihood,
                                "candidate_start_count":
                                    fit.candidate_start_count,
                                "attempted_start_count":
                                    fit.attempted_start_count,
                                "converged_start_count":
                                    fit.converged_start_count,
                                "near_optimal_start_count":
                                    fit.near_optimal_start_count,
                                "start_nll_range": fit.start_nll_range,
                                "innovation_max_abs_autocorrelation":
                                    fit.innovation_max_abs_autocorrelation,
                                "parameters": dict(fit.parameters),
                                "near_optimal_parameter_ranges":
                                    fit.near_optimal_parameter_ranges,
                            }
                            for fit in comparison.fits
                        }
                        rows.append(
                            {
                                "frequency_hz": frequency_hz,
                                "damping_ratio": damping_ratio,
                                "duration_seconds": duration_seconds,
                                "observation_noise_to_latent_sd": observation_noise_ratio,
                                "seed": seed,
                                "bic_winner": comparison.bic_winner,
                                "bic_margin_to_second": comparison.bic_margin_to_second,
                                "a1_frequency_relative_error": abs(
                                    a1.parameters["natural_frequency_hz"]
                                    - frequency_hz
                                )
                                / frequency_hz,
                                "a1_damping_absolute_error": abs(
                                    a1.parameters["damping_ratio"]
                                    - damping_ratio
                                ),
                                "a1_innovation_max_abs_autocorrelation":
                                    a1.innovation_max_abs_autocorrelation,
                                "a1_near_optimal_start_count":
                                    a1.near_optimal_start_count,
                                "a1_parameters": dict(a1.parameters),
                                "fit_diagnostics": fit_diagnostics,
                            }
                        )
    return rows


def _two_mode_signal(
    second_frequency_hz: float,
    amplitude_ratio: float,
    seed: int,
) -> np.ndarray:
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.25, FS),
        seconds=30.0,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(second_frequency_hz, 0.35, FS),
        seconds=30.0,
        measurement_noise_to_latent_sd=0.0,
        seed=seed + 100,
    )
    rng = np.random.default_rng(seed + 200)
    return _standardize(
        _standardize(first)
        + amplitude_ratio * _standardize(second)
        + rng.normal(0.0, 0.35, size=first.size)
    )


def _two_mode_rows() -> list[dict[str, object]]:
    rows = []
    for second_frequency_hz in (10.5, 11.0, 12.0, 15.0, 20.0):
        for amplitude_ratio in (0.35, 0.60, 1.00):
            for seed in SEEDS:
                signal = _two_mode_signal(
                    second_frequency_hz,
                    amplitude_ratio,
                    seed,
                )
                comparison = compare_state_space_candidates(
                    signal,
                    FS,
                    optimizer_maxiter=80,
                )
                a2 = comparison.by_family("A2")
                fit_diagnostics = {
                    fit.family: {
                        "success": fit.success,
                        "bic": fit.bic,
                        "negative_log_likelihood": fit.negative_log_likelihood,
                        "candidate_start_count": fit.candidate_start_count,
                        "attempted_start_count": fit.attempted_start_count,
                        "converged_start_count": fit.converged_start_count,
                        "near_optimal_start_count":
                            fit.near_optimal_start_count,
                        "start_nll_range": fit.start_nll_range,
                        "innovation_max_abs_autocorrelation":
                            fit.innovation_max_abs_autocorrelation,
                        "parameters": dict(fit.parameters),
                        "near_optimal_parameter_ranges":
                            fit.near_optimal_parameter_ranges,
                    }
                    for fit in comparison.fits
                }
                estimated_frequencies = sorted(
                    [
                        a2.parameters["mode1_natural_frequency_hz"],
                        a2.parameters["mode2_natural_frequency_hz"],
                    ]
                )
                rows.append(
                    {
                        "first_frequency_hz": 10.0,
                        "second_frequency_hz": second_frequency_hz,
                        "true_separation_hz": second_frequency_hz - 10.0,
                        "second_to_first_amplitude_ratio": amplitude_ratio,
                        "seed": seed,
                        "bic_winner": comparison.bic_winner,
                        "bic_margin_to_second": comparison.bic_margin_to_second,
                        "a2_estimated_natural_frequencies_hz":
                            estimated_frequencies,
                        "a2_estimated_separation_hz":
                            estimated_frequencies[1] - estimated_frequencies[0],
                        "a2_innovation_max_abs_autocorrelation":
                            a2.innovation_max_abs_autocorrelation,
                        "a2_near_optimal_start_count":
                            a2.near_optimal_start_count,
                        "a2_near_optimal_parameter_ranges":
                            a2.near_optimal_parameter_ranges,
                        "fit_diagnostics": fit_diagnostics,
                    }
                )
    return rows


def _single_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    keys = sorted(
        {
            (
                row["frequency_hz"],
                row["damping_ratio"],
                row["duration_seconds"],
                row["observation_noise_to_latent_sd"],
            )
            for row in rows
        }
    )
    output = []
    for key in keys:
        subset = [
            row
            for row in rows
            if (
                row["frequency_hz"],
                row["damping_ratio"],
                row["duration_seconds"],
                row["observation_noise_to_latent_sd"],
            )
            == key
        ]
        output.append(
            {
                "frequency_hz": key[0],
                "damping_ratio": key[1],
                "duration_seconds": key[2],
                "observation_noise_to_latent_sd": key[3],
                "n": len(subset),
                "a1_bic_selection_rate": float(
                    np.mean(
                        [
                            1.0 if row["bic_winner"] == "A1" else 0.0
                            for row in subset
                        ]
                    )
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
            }
        )
    return output


def _two_mode_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    keys = sorted(
        {
            (
                row["true_separation_hz"],
                row["second_to_first_amplitude_ratio"],
            )
            for row in rows
        }
    )
    output = []
    for key in keys:
        subset = [
            row
            for row in rows
            if (
                row["true_separation_hz"],
                row["second_to_first_amplitude_ratio"],
            )
            == key
        ]
        output.append(
            {
                "true_separation_hz": key[0],
                "second_to_first_amplitude_ratio": key[1],
                "n": len(subset),
                "a2_bic_selection_rate": float(
                    np.mean(
                        [
                            1.0 if row["bic_winner"] == "A2" else 0.0
                            for row in subset
                        ]
                    )
                ),
                "median_a2_estimated_separation_hz": _median(
                    [row["a2_estimated_separation_hz"] for row in subset]
                ),
                "median_a2_innovation_max_abs_autocorrelation": _median(
                    [
                        row["a2_innovation_max_abs_autocorrelation"]
                        for row in subset
                    ]
                ),
            }
        )
    return output


def run() -> dict[str, object]:
    single_rows = _single_mode_rows()
    two_mode_rows = _two_mode_rows()
    return {
        "purpose": "P0-Q likelihood state-space operating-region map",
        "sampling_rate_hz": FS,
        "seeds": list(SEEDS),
        "single_mode_summary": _single_summary(single_rows),
        "two_mode_resolution_summary": _two_mode_summary(two_mode_rows),
        "single_mode_rows": single_rows,
        "two_mode_rows": two_mode_rows,
        "interpretation_ceiling": (
            "Qualification map only. Selection rates and errors may define a "
            "candidate future operating region only after inspection and freeze; "
            "they do not license real-EEG damping, chi, diagnosis, or prognosis."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "single_mode_summary": result["single_mode_summary"],
                "two_mode_resolution_summary": result[
                    "two_mode_resolution_summary"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
