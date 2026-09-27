#!/usr/bin/env python3
"""Adversarial controls for the qualification-only C1Q candidate.

This probe asks whether C1Q fixes one-mode nonzero-g nuisance pressure without
silently absorbing genuine multimodality or colored-process misspecification.
It does not change production A0/A1/A2 or license real EEG.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from nsd_engine.continuous_lineage_candidate import fit_continuous_lineage_candidate
from nsd_engine.latent_oscillator_covariance import (
    LatentOscillatorTruth,
    simulate_latent_oscillator,
)
from nsd_engine.state_space_adequacy import compare_state_space_candidates


FS = 256.0
SECONDS = 30.0


def _standardize(values):
    values = np.asarray(values, dtype=float)
    return (values - np.mean(values)) / np.std(values)


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
    n = int(round(SECONDS * FS))
    burn = int(round(5.0 * FS))
    total = n + burn
    transition = _rotation_transition(FS, 10.0, 0.30)
    rho = math.sqrt(float(abs(np.linalg.det(transition))))
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
        state = transition @ state + innovation

    latent = latent[burn:].copy()
    latent_sd = float(np.std(latent))
    observed = latent + rng.normal(0.0, 0.50 * latent_sd, size=n)
    return observed


def _two_mode_signal(seed: int) -> np.ndarray:
    first = simulate_latent_oscillator(
        LatentOscillatorTruth(10.0, 0.25, FS),
        seconds=SECONDS,
        measurement_noise_to_latent_sd=0.0,
        seed=seed,
    )
    second = simulate_latent_oscillator(
        LatentOscillatorTruth(20.0, 0.35, FS),
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


def _fit(signal: np.ndarray, optimizer_maxiter: int):
    current = compare_state_space_candidates(
        signal,
        FS,
        optimizer_maxiter=optimizer_maxiter,
    )
    c1q = fit_continuous_lineage_candidate(
        signal,
        FS,
        optimizer_maxiter=optimizer_maxiter,
        max_optimized_starts=8,
    )
    bics = {fit.family: fit.bic for fit in current.fits}
    bics["C1Q"] = c1q.bic
    ordered = sorted(bics.items(), key=lambda item: item[1])
    return {
        "current_winner": current.bic_winner,
        "extended_winner": ordered[0][0],
        "extended_margin_to_second": ordered[1][1] - ordered[0][1],
        "bics": bics,
        "C1Q": {
            "bic": c1q.bic,
            "negative_log_likelihood": c1q.negative_log_likelihood,
            "parameters": c1q.parameters,
            "success": c1q.success,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--optimizer-maxiter", type=int, default=50)
    parser.add_argument("--seed", type=int, action="append", default=None)
    args = parser.parse_args()
    seeds = args.seed if args.seed is not None else [0, 1]

    payload = {
        "status": "QUALIFICATION_ONLY",
        "licenses_real_eeg_local_chi": False,
        "promotes_c1q": False,
        "cells": [],
    }

    for seed in seeds:
        isotropic = simulate_latent_oscillator(
            LatentOscillatorTruth(10.0, 0.30, FS),
            seconds=SECONDS,
            measurement_noise_to_latent_sd=0.50,
            seed=seed,
        )
        payload["cells"].append({
            "truth_class": "a1_isotropic_one_mode",
            "seed": seed,
            "expected_role": "nested_simpler_control",
            **_fit(isotropic, args.optimizer_maxiter),
        })

        payload["cells"].append({
            "truth_class": "genuine_separated_two_mode",
            "seed": seed,
            "expected_role": "multimodal_control",
            **_fit(_two_mode_signal(seed), args.optimizer_maxiter),
        })

        for kind in (
            "anisotropic_white_4_to_1",
            "rank1_white_axis_drive",
            "colored_process_phi_0_7",
        ):
            payload["cells"].append({
                "truth_class": kind,
                "seed": seed,
                "expected_role": (
                    "one_mode_white_forcing_shape_control"
                    if kind != "colored_process_phi_0_7"
                    else "colored_process_refusal_control"
                ),
                **_fit(_process_signal(kind, seed), args.optimizer_maxiter),
            })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "cell_count": len(payload["cells"]),
        "status": payload["status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
