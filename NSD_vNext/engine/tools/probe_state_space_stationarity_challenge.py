#!/usr/bin/env python3
"""Prospective stationarity challenge for the NSD A0/A1/A2 modal lane."""

from __future__ import annotations

import argparse
import importlib.util
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
SECONDS = 30.0
SEEDS = (0, 1, 2)


def _standardize(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    values = values - float(np.mean(values))
    sd = float(np.std(values))
    if not math.isfinite(sd) or sd <= 0:
        raise ValueError("invalid standard deviation")
    return values / sd


def _load_existing_generators():
    source = Path(__file__).with_name("probe_state_space_model_adequacy.py")
    spec = importlib.util.spec_from_file_location("nsd_existing_adequacy_generators", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load existing adequacy generators")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if float(module.FS) != FS or float(module.SECONDS) != SECONDS:
        raise RuntimeError("existing generator constants changed")
    return module


def _stationary_single(seed: int) -> np.ndarray:
    return simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.50,
        seed=seed,
    )


def _damping_shift(seed: int) -> np.ndarray:
    half = SECONDS / 2.0
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.20, FS),
        seconds=half,
        measurement_noise_to_latent_sd=0.25,
        seed=seed,
    )
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.70, FS),
        seconds=half,
        measurement_noise_to_latent_sd=0.25,
        seed=seed + 800,
    )
    return _standardize(np.concatenate([first, second]))


def _amplitude_step(seed: int) -> np.ndarray:
    half = SECONDS / 2.0
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=half,
        measurement_noise_to_latent_sd=0.50,
        seed=seed,
    )
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.30, FS),
        seconds=half,
        measurement_noise_to_latent_sd=0.50,
        seed=seed + 900,
    )
    return _standardize(np.concatenate([first, 2.0 * second]))


def _fit(values: np.ndarray) -> dict[str, object]:
    comparison = compare_state_space_candidates(
        values,
        FS,
        fmin_hz=1.0,
        fmax_hz=45.0,
        optimizer_maxiter=80,
    )
    a1 = comparison.by_family("A1")
    return {
        "winner": comparison.bic_winner,
        "bic_margin_to_second": comparison.bic_margin_to_second,
        "a1_natural_frequency_hz": a1.parameters["natural_frequency_hz"],
        "a1_damping_ratio": a1.parameters["damping_ratio"],
        "a1_latent_fraction": a1.parameters["latent_fraction"],
        "a1_innovation_max_abs_autocorrelation":
            a1.innovation_max_abs_autocorrelation,
    }


def _sym_rel(a: float, b: float) -> float:
    scale = 0.5 * (abs(a) + abs(b))
    return abs(a - b) / scale if scale > 0 else float("nan")


def _rms_occupancy(values: np.ndarray) -> dict[str, float]:
    chunks = np.array_split(values, 8)
    rms = np.asarray(
        [math.sqrt(float(np.mean(np.asarray(chunk) ** 2))) for chunk in chunks],
        dtype=np.float64,
    )
    mean = float(np.mean(rms))
    minimum = float(np.min(rms))
    return {
        "rms_window_values": rms.tolist(),
        "rms_coefficient_of_variation": (
            float(np.std(rms, ddof=0) / mean) if mean > 0 else float("nan")
        ),
        "rms_max_to_min_ratio": (
            float(np.max(rms) / minimum) if minimum > 0 else float("inf")
        ),
    }


def _row(scenario: str, seed: int, values: np.ndarray) -> dict[str, object]:
    values = _standardize(values)
    whole = _fit(values)

    halves = np.array_split(values, 2)
    half_fits = [_fit(chunk) for chunk in halves]

    quarters = np.array_split(values, 4)
    quarter_fits = [_fit(chunk) for chunk in quarters]

    half_freq = [float(x["a1_natural_frequency_hz"]) for x in half_fits]
    half_damp = [float(x["a1_damping_ratio"]) for x in half_fits]
    half_frac = [float(x["a1_latent_fraction"]) for x in half_fits]

    q_freq = np.asarray(
        [float(x["a1_natural_frequency_hz"]) for x in quarter_fits],
        dtype=np.float64,
    )
    q_damp = np.asarray(
        [float(x["a1_damping_ratio"]) for x in quarter_fits],
        dtype=np.float64,
    )
    q_frac = np.asarray(
        [float(x["a1_latent_fraction"]) for x in quarter_fits],
        dtype=np.float64,
    )
    q_med_freq = float(np.median(np.abs(q_freq)))

    return {
        "scenario": scenario,
        "seed": seed,
        "whole": whole,
        "halves": {
            "fits": half_fits,
            "same_winner": half_fits[0]["winner"] == half_fits[1]["winner"],
            "a1_frequency_symmetric_relative_difference":
                _sym_rel(half_freq[0], half_freq[1]),
            "a1_damping_absolute_difference": abs(half_damp[0] - half_damp[1]),
            "a1_latent_fraction_absolute_difference":
                abs(half_frac[0] - half_frac[1]),
        },
        "quarters": {
            "fits": quarter_fits,
            "winner_sequence": [x["winner"] for x in quarter_fits],
            "a1_frequency_range_over_median": (
                float((np.max(q_freq) - np.min(q_freq)) / q_med_freq)
                if q_med_freq > 0 else float("nan")
            ),
            "a1_damping_range": float(np.max(q_damp) - np.min(q_damp)),
            "a1_latent_fraction_range": float(np.max(q_frac) - np.min(q_frac)),
        },
        "occupancy": _rms_occupancy(values),
    }


def _median(values):
    usable = [float(x) for x in values if math.isfinite(float(x))]
    return float(np.median(usable)) if usable else None


def run() -> dict[str, object]:
    existing = _load_existing_generators()
    generators = {
        "stationary_single": _stationary_single,
        "frequency_shift_mid_record":
            existing.GENERATORS["frequency_shift_mid_record"],
        "damping_shift_mid_record": _damping_shift,
        "finite_bursts": existing.GENERATORS["finite_bursts"],
        "amplitude_step_control": _amplitude_step,
        "colored_observation_stationary_control":
            existing.GENERATORS["colored_observation_noise"],
    }

    rows = [
        _row(scenario, seed, generator(seed))
        for scenario, generator in generators.items()
        for seed in SEEDS
    ]

    summaries = {}
    for scenario in generators:
        subset = [row for row in rows if row["scenario"] == scenario]
        summaries[scenario] = {
            "n": len(subset),
            "whole_winner_counts": {
                family: sum(row["whole"]["winner"] == family for row in subset)
                for family in ("A0", "A1", "A2")
            },
            "half_same_winner_fraction": float(
                np.mean([row["halves"]["same_winner"] for row in subset])
            ),
            "median_half_a1_frequency_symmetric_relative_difference": _median(
                [
                    row["halves"]["a1_frequency_symmetric_relative_difference"]
                    for row in subset
                ]
            ),
            "median_half_a1_damping_absolute_difference": _median(
                [
                    row["halves"]["a1_damping_absolute_difference"]
                    for row in subset
                ]
            ),
            "median_half_a1_latent_fraction_absolute_difference": _median(
                [
                    row["halves"]["a1_latent_fraction_absolute_difference"]
                    for row in subset
                ]
            ),
            "median_quarter_a1_frequency_range_over_median": _median(
                [
                    row["quarters"]["a1_frequency_range_over_median"]
                    for row in subset
                ]
            ),
            "median_quarter_a1_damping_range": _median(
                [row["quarters"]["a1_damping_range"] for row in subset]
            ),
            "median_quarter_a1_latent_fraction_range": _median(
                [row["quarters"]["a1_latent_fraction_range"] for row in subset]
            ),
            "median_rms_coefficient_of_variation": _median(
                [
                    row["occupancy"]["rms_coefficient_of_variation"]
                    for row in subset
                ]
            ),
            "median_rms_max_to_min_ratio": _median(
                [row["occupancy"]["rms_max_to_min_ratio"] for row in subset]
            ),
        }

    return {
        "schema": "NSD_STATE_SPACE_STATIONARITY_CHALLENGE_V0_1",
        "purpose": "P0-Q temporal stationarity/intermittency diagnostic map",
        "sampling_rate_hz": FS,
        "duration_seconds": SECONDS,
        "seeds": list(SEEDS),
        "summaries": summaries,
        "rows": rows,
        "interpretation_ceiling": (
            "Qualification diagnostics only. No production stationarity threshold, "
            "real-EEG modal damping/local chi, biological transition, diagnosis, "
            "or prognosis is licensed."
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
