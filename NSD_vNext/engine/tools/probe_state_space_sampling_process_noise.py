#!/usr/bin/env python3
"""Sampling-rate and process-noise P0-Q extension for NSD A0/A1/A2."""

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


def _fit_record(signal: np.ndarray, fs: float) -> dict[str, object]:
    cmp = compare_state_space_candidates(
        signal,
        fs,
        fmin_hz=1.0,
        fmax_hz=45.0,
        optimizer_maxiter=80,
    )
    a1 = cmp.by_family("A1")
    return {
        "bic_winner": cmp.bic_winner,
        "bic_margin_to_second": cmp.bic_margin_to_second,
        "a1": {
            "natural_frequency_hz": a1.parameters["natural_frequency_hz"],
            "damping_ratio": a1.parameters["damping_ratio"],
            "latent_fraction": a1.parameters["latent_fraction"],
            "rho": a1.parameters["rho"],
            "innovation_max_abs_autocorrelation":
                a1.innovation_max_abs_autocorrelation,
            "near_optimal_start_count": a1.near_optimal_start_count,
            "near_optimal_parameter_ranges": {
                k: list(v) for k, v in a1.near_optimal_parameter_ranges.items()
            },
        },
        "fits": [
            {
                "family": fit.family,
                "success": fit.success,
                "bic": fit.bic,
                "negative_log_likelihood": fit.negative_log_likelihood,
                "innovation_max_abs_autocorrelation":
                    fit.innovation_max_abs_autocorrelation,
                "near_optimal_start_count": fit.near_optimal_start_count,
                "start_nll_range": fit.start_nll_range,
                "parameters": dict(fit.parameters),
                "near_optimal_parameter_ranges": {
                    k: list(v) for k, v in fit.near_optimal_parameter_ranges.items()
                },
            }
            for fit in cmp.fits
        ],
    }


def _sampling_rows(fs: float) -> list[dict[str, object]]:
    if fs not in (128.0, 512.0):
        raise ValueError("sampling extension fs must be 128 or 512")
    rows = []
    for frequency in (5.0, 10.0, 20.0):
        for damping in (0.20, 0.50, 0.80):
            for seed in (0, 1, 2):
                signal = simulate_latent_oscillator(
                    LatentOscillatorTruth(frequency, damping, fs),
                    seconds=30.0,
                    measurement_noise_to_latent_sd=0.50,
                    seed=seed,
                )
                fit = _fit_record(signal, fs)
                fit.update({
                    "part": "sampling_rate",
                    "sampling_rate_hz": fs,
                    "truth_natural_frequency_hz": frequency,
                    "truth_damping_ratio": damping,
                    "duration_seconds": 30.0,
                    "observation_noise_to_latent_sd": 0.50,
                    "seed": seed,
                    "a1_frequency_relative_error": abs(
                        fit["a1"]["natural_frequency_hz"] - frequency
                    ) / frequency,
                    "a1_damping_absolute_error": abs(
                        fit["a1"]["damping_ratio"] - damping
                    ),
                })
                rows.append(fit)
    return rows


def _rotation_transition(fs: float, frequency: float, damping: float) -> np.ndarray:
    omega_n = 2.0 * math.pi * frequency
    decay = damping * omega_n
    omega_d = omega_n * math.sqrt(1.0 - damping * damping)
    rho = math.exp(-decay / fs)
    theta = omega_d / fs
    return rho * np.asarray(
        [[math.cos(theta), -math.sin(theta)],
         [math.sin(theta),  math.cos(theta)]],
        dtype=np.float64,
    )


def _process_signal(kind: str, seed: int) -> np.ndarray:
    fs = 256.0
    seconds = 30.0
    burn_seconds = 5.0
    n = int(round(seconds * fs))
    burn = int(round(burn_seconds * fs))
    total = n + burn
    A = _rotation_transition(fs, 10.0, 0.30)
    rho = math.sqrt(float(abs(np.linalg.det(A))))
    base_sd = math.sqrt(max(1e-12, 1.0 - rho * rho))
    rng = np.random.default_rng(seed + 10000)
    state = rng.normal(0.0, 1.0, size=2)
    latent = np.empty(total, dtype=np.float64)

    colored = np.zeros(2, dtype=np.float64)
    phi = 0.7
    colored_scale = math.sqrt(1.0 - phi * phi)

    for idx in range(total):
        latent[idx] = state[0]
        if kind == "isotropic_white":
            innovation = rng.normal(0.0, base_sd, size=2)
        elif kind == "anisotropic_white_4_to_1":
            raw = rng.normal(size=2) * np.asarray([4.0, 1.0])
            raw /= math.sqrt(float(np.mean(np.asarray([16.0, 1.0]))))
            innovation = base_sd * raw
        elif kind == "rank1_white_axis_drive":
            innovation = np.asarray(
                [rng.normal(0.0, base_sd * math.sqrt(2.0)), 0.0],
                dtype=np.float64,
            )
        elif kind == "colored_process_phi_0_7":
            colored = phi * colored + colored_scale * rng.normal(size=2)
            innovation = base_sd * colored
        else:
            raise ValueError(kind)
        state = A @ state + innovation

    latent = latent[burn:].copy()
    latent_sd = float(np.std(latent))
    if not math.isfinite(latent_sd) or latent_sd <= 0:
        raise RuntimeError("invalid latent process standard deviation")
    observed = latent + rng.normal(0.0, 0.50 * latent_sd, size=n)
    return observed


def _process_rows(kind: str) -> list[dict[str, object]]:
    if kind not in {
        "isotropic_white",
        "anisotropic_white_4_to_1",
        "rank1_white_axis_drive",
        "colored_process_phi_0_7",
    }:
        raise ValueError(kind)
    rows = []
    for seed in (0, 1, 2):
        signal = _process_signal(kind, seed)
        fit = _fit_record(signal, 256.0)
        fit.update({
            "part": "process_noise",
            "process_noise_family": kind,
            "sampling_rate_hz": 256.0,
            "truth_natural_frequency_hz": 10.0,
            "truth_damping_ratio": 0.30,
            "duration_seconds": 30.0,
            "observation_noise_to_realized_latent_sd": 0.50,
            "seed": seed,
            "a1_frequency_relative_error": abs(
                fit["a1"]["natural_frequency_hz"] - 10.0
            ) / 10.0,
            "a1_damping_absolute_error": abs(
                fit["a1"]["damping_ratio"] - 0.30
            ),
        })
        rows.append(fit)
    return rows


def _median(values):
    vals = [float(v) for v in values if math.isfinite(float(v))]
    return float(np.median(vals)) if vals else None


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        return {}
    groups: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        if row["part"] == "sampling_rate":
            key = (
                f"fs={row['sampling_rate_hz']}|f={row['truth_natural_frequency_hz']}"
                f"|zeta={row['truth_damping_ratio']}"
            )
        else:
            key = str(row["process_noise_family"])
        groups.setdefault(key, []).append(row)

    out = {}
    for key, subset in groups.items():
        out[key] = {
            "n": len(subset),
            "winner_counts": {
                family: sum(row["bic_winner"] == family for row in subset)
                for family in ("A0", "A1", "A2")
            },
            "median_a1_frequency_relative_error": _median(
                [row["a1_frequency_relative_error"] for row in subset]
            ),
            "median_a1_damping_absolute_error": _median(
                [row["a1_damping_absolute_error"] for row in subset]
            ),
            "median_a1_innovation_max_abs_autocorrelation": _median(
                [
                    row["a1"]["innovation_max_abs_autocorrelation"]
                    for row in subset
                ]
            ),
        }
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["sampling", "process"], required=True)
    parser.add_argument("--value", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.mode == "sampling":
        rows = _sampling_rows(float(args.value))
        descriptor = {"sampling_rate_hz": float(args.value)}
    else:
        rows = _process_rows(args.value)
        descriptor = {"process_noise_family": args.value}

    result = {
        "schema": "NSD_STATE_SPACE_SAMPLING_PROCESS_NOISE_EXTENSION_V0_1",
        "purpose": "P0-Q sampling/process-noise adequacy extension",
        "mode": args.mode,
        **descriptor,
        "rows": rows,
        "summary": summarize(rows),
        "interpretation_ceiling": (
            "Known-truth qualification only. No production threshold, real-EEG "
            "modal damping/local chi, diagnosis, or prognosis is licensed."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
