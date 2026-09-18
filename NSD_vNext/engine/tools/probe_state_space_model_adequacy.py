#!/usr/bin/env python3
"""Run the likelihood-based A0/A1/A2 modal adequacy qualification map.

This is P0-Q known-truth / known-misspecification work only. It does not apply
modal damping to EEG and does not freeze an admission threshold.
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
from nsd_engine.state_space_adequacy import (
    compare_state_space_candidates,
    evaluate_comparison_on_holdout,
)


FS = 256.0
SECONDS = 30.0
SEEDS = (0, 1, 2)


def _standardize(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    values = values - float(np.mean(values))
    sd = float(np.std(values))
    return values / sd if sd > 0 else values


def _colored_noise(n: int, phi: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    epsilon = rng.normal(size=n)
    values = np.zeros(n, dtype=np.float64)
    scale = math.sqrt(max(1e-12, 1.0 - phi * phi))
    for index in range(1, n):
        values[index] = phi * values[index - 1] + scale * epsilon[index]
    return _standardize(values)


def _single(seed: int) -> np.ndarray:
    return simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.5,
        seed=seed,
    )


def _two_modes(seed: int, close: bool) -> np.ndarray:
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.25, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(12.0 if close else 20.0, 0.35, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed + 100,
    )
    rng = np.random.default_rng(seed + 200)
    return _standardize(
        0.8 * _standardize(first)
        + 0.8 * _standardize(second)
        + rng.normal(0.0, 0.35, size=first.size)
    )


def _colored_observation(seed: int) -> np.ndarray:
    latent = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    noise = _colored_noise(latent.size, 0.85, seed + 300)
    return _standardize(_standardize(latent) + 0.7 * noise)


def _frequency_shift(seed: int) -> np.ndarray:
    half = SECONDS / 2.0
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(8.0, 0.25, FS),
        seconds=half,
        measurement_noise_to_latent_sd=0.25,
        seed=seed,
    )
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(13.0, 0.25, FS),
        seconds=half,
        measurement_noise_to_latent_sd=0.25,
        seed=seed + 400,
    )
    return _standardize(np.concatenate([first, second]))


def _bursty(seed: int) -> np.ndarray:
    latent = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.20, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    time = np.arange(latent.size) / FS
    envelope = np.zeros(latent.size, dtype=np.float64)
    for start in (2.0, 8.0, 15.0, 23.0):
        envelope[(time >= start) & (time < start + 2.0)] = 1.0
    rng = np.random.default_rng(seed + 500)
    return _standardize(
        envelope * latent + rng.normal(0.0, 0.25, size=latent.size)
    )


def _nonoscillatory_ar1(seed: int) -> np.ndarray:
    return _colored_noise(int(round(FS * SECONDS)), 0.97, seed + 600)


def _white_noise(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed + 700)
    return rng.normal(size=int(round(FS * SECONDS)))


GENERATORS = {
    "single_valid_truth": _single,
    "two_modes_close": lambda seed: _two_modes(seed, True),
    "two_modes_separated": lambda seed: _two_modes(seed, False),
    "colored_observation_noise": _colored_observation,
    "frequency_shift_mid_record": _frequency_shift,
    "finite_bursts": _bursty,
    "nonoscillatory_ar1": _nonoscillatory_ar1,
    "white_noise": _white_noise,
}


def _median(values):
    usable = [
        float(value)
        for value in values
        if value is not None and math.isfinite(float(value))
    ]
    return float(np.median(usable)) if usable else None


def _winner_counts(rows, field):
    result = {"A0": 0, "A1": 0, "A2": 0}
    for row in rows:
        winner = row[field]
        result[winner] += 1
    return result


def run() -> dict[str, object]:
    rows = []
    for scenario, generator in GENERATORS.items():
        for seed in SEEDS:
            signal = generator(seed)
            full = compare_state_space_candidates(
                signal,
                FS,
                optimizer_maxiter=80,
            )

            midpoint = signal.size // 2
            first_half = compare_state_space_candidates(
                signal[:midpoint],
                FS,
                optimizer_maxiter=70,
            )
            second_half = compare_state_space_candidates(
                signal[midpoint:],
                FS,
                optimizer_maxiter=70,
            )
            holdout = evaluate_comparison_on_holdout(
                first_half,
                signal[midpoint:],
            )

            row = {
                "scenario": scenario,
                "seed": seed,
                "full": asdict(full),
                "split_half": {
                    "first_winner": first_half.bic_winner,
                    "second_winner": second_half.bic_winner,
                    "same_winner": first_half.bic_winner == second_half.bic_winner,
                    "first_bic_margin_to_second": first_half.bic_margin_to_second,
                    "second_bic_margin_to_second": second_half.bic_margin_to_second,
                },
                "heldout_from_first_half": holdout,
            }
            if scenario == "single_valid_truth":
                a1 = full.by_family("A1")
                row["valid_truth_error"] = {
                    "natural_frequency_relative_error": abs(
                        a1.parameters["natural_frequency_hz"] - 10.0
                    ) / 10.0,
                    "damping_ratio_absolute_error": abs(
                        a1.parameters["damping_ratio"] - 0.30
                    ),
                }
            rows.append(row)

    summaries = {}
    for scenario in GENERATORS:
        subset = [row for row in rows if row["scenario"] == scenario]
        full_winners = [row["full"]["bic_winner"] for row in subset]
        heldout_winners = [
            row["heldout_from_first_half"]["winner"] for row in subset
        ]
        summaries[scenario] = {
            "n": len(subset),
            "full_bic_winner_counts": {
                family: full_winners.count(family)
                for family in ("A0", "A1", "A2")
            },
            "heldout_winner_counts": {
                family: heldout_winners.count(family)
                for family in ("A0", "A1", "A2")
            },
            "split_half_same_winner_fraction": float(
                np.mean(
                    [
                        1.0 if row["split_half"]["same_winner"] else 0.0
                        for row in subset
                    ]
                )
            ),
            "median_full_bic_margin_to_second": _median(
                [row["full"]["bic_margin_to_second"] for row in subset]
            ),
            "median_innovation_max_abs_autocorrelation": {
                family: _median(
                    [
                        next(
                            fit["innovation_max_abs_autocorrelation"]
                            for fit in row["full"]["fits"]
                            if fit["family"] == family
                        )
                        for row in subset
                    ]
                )
                for family in ("A0", "A1", "A2")
            },
            "median_near_optimal_start_count": {
                family: _median(
                    [
                        next(
                            fit["near_optimal_start_count"]
                            for fit in row["full"]["fits"]
                            if fit["family"] == family
                        )
                        for row in subset
                    ]
                )
                for family in ("A0", "A1", "A2")
            },
            "median_start_nll_range": {
                family: _median(
                    [
                        next(
                            fit["start_nll_range"]
                            for fit in row["full"]["fits"]
                            if fit["family"] == family
                        )
                        for row in subset
                    ]
                )
                for family in ("A0", "A1", "A2")
            },
            "median_heldout_nll_per_sample": {
                family: _median(
                    [
                        row["heldout_from_first_half"][
                            "negative_log_likelihood_per_sample"
                        ][family]
                        for row in subset
                    ]
                )
                for family in ("A0", "A1", "A2")
            },
            "median_valid_truth_frequency_relative_error": _median(
                [
                    row.get("valid_truth_error", {}).get(
                        "natural_frequency_relative_error"
                    )
                    for row in subset
                ]
            ),
            "median_valid_truth_damping_absolute_error": _median(
                [
                    row.get("valid_truth_error", {}).get(
                        "damping_ratio_absolute_error"
                    )
                    for row in subset
                ]
            ),
        }

    return {
        "purpose": "P0-Q likelihood-based A0/A1/A2 model-adequacy qualification",
        "sampling_rate_hz": FS,
        "duration_seconds": SECONDS,
        "seeds": list(SEEDS),
        "interpretation_ceiling": (
            "BIC and held-out winners are qualification diagnostics only. "
            "No result licenses real-EEG modal damping, local chi, biological "
            "mode interpretation, diagnosis, or prognosis."
        ),
        "summaries": summaries,
        "rows": rows,
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
    print(json.dumps(result["summaries"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
