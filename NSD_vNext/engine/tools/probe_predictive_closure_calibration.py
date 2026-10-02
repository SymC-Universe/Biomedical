#!/usr/bin/env python3
"""Exploratory predictive-closure calibration map for NSD Bio Chi.

Known-truth qualification only. This tool maps exact substrate/projection
mechanisms to claim-relative predictive effects without defining an admission
threshold.

It reports operator-level prediction error for the resolved P subspace,
hidden-state sensitivity, memory-kernel magnitude, and underdamped pole/chi
shift across closed, one-way, and bidirectional coupling fixtures.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import expm


P = np.asarray([0, 1], dtype=int)
Q = np.asarray([2, 3], dtype=int)


def oscillator_block(omega: float, zeta: float) -> np.ndarray:
    return np.asarray(
        [[0.0, 1.0], [-(omega * omega), -2.0 * zeta * omega]],
        dtype=float,
    )


def generator(
    *,
    omega_p: float,
    zeta_p: float,
    omega_q: float,
    zeta_q: float,
    c_q_to_p: float,
    c_p_to_q: float,
) -> np.ndarray:
    L = np.zeros((4, 4), dtype=float)
    L[:2, :2] = oscillator_block(omega_p, zeta_p)
    L[2:, 2:] = oscillator_block(omega_q, zeta_q)
    L[1, 2] = c_q_to_p
    L[3, 0] = c_p_to_q
    return L


def blocks(L: np.ndarray):
    return (
        L[np.ix_(P, P)],
        L[np.ix_(P, Q)],
        L[np.ix_(Q, P)],
        L[np.ix_(Q, Q)],
    )


def memory_kernel(L: np.ndarray, t: float) -> np.ndarray:
    _, Lpq, Lqp, Lqq = blocks(L)
    return Lpq @ expm(Lqq * t) @ Lqp


def hidden_map(L: np.ndarray, t: float) -> np.ndarray:
    """Map hidden initial q0 to resolved p(t) for p0=0."""
    E = expm(L * t)
    return E[np.ix_(P, Q)]


def resolved_propagator(L: np.ndarray, t: float) -> np.ndarray:
    return expm(L * t)[np.ix_(P, P)]


def markov_propagator(L: np.ndarray, t: float) -> np.ndarray:
    Lpp, _, _, _ = blocks(L)
    return expm(Lpp * t)


def rms_operator_curve(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(math.sqrt(float(np.mean(np.asarray(values, dtype=float) ** 2))))


def local_positive_imag_pole(L: np.ndarray) -> complex:
    Lpp, _, _, _ = blocks(L)
    candidates = [complex(x) for x in np.linalg.eigvals(Lpp) if x.imag > 0]
    if not candidates:
        raise ValueError("resolved local block is not underdamped")
    return max(candidates, key=lambda x: x.imag)


def matched_full_pole(L: np.ndarray, target: complex) -> complex | None:
    candidates = [complex(x) for x in np.linalg.eigvals(L) if x.imag > 0 and x.real < 0]
    if not candidates:
        return None
    return min(candidates, key=lambda x: abs(x - target))


def chi_from_complex_pole(pole: complex) -> float | None:
    if pole.real >= 0 or pole.imag == 0:
        return None
    return float(-pole.real / abs(pole))


def metrics(L: np.ndarray, *, horizon: float, samples: int):
    times = np.linspace(0.0, horizon, samples)
    prediction_errors = []
    hidden_sensitivities = []
    memory_magnitudes = []

    for t in times:
        exact = resolved_propagator(L, float(t))
        markov = markov_propagator(L, float(t))
        denom = max(float(np.linalg.norm(exact, ord=2)), 1e-15)
        prediction_errors.append(float(np.linalg.norm(exact - markov, ord=2)) / denom)
        hidden_sensitivities.append(float(np.linalg.norm(hidden_map(L, float(t)), ord=2)))
        memory_magnitudes.append(float(np.linalg.norm(memory_kernel(L, float(t)), ord=2)))

    local_pole = local_positive_imag_pole(L)
    full_pole = matched_full_pole(L, local_pole)
    local_chi = chi_from_complex_pole(local_pole)
    full_chi = chi_from_complex_pole(full_pole) if full_pole is not None else None

    return {
        "resolved_prediction_relative_operator_rms": rms_operator_curve(prediction_errors),
        "resolved_prediction_relative_operator_max": float(max(prediction_errors)),
        "hidden_initial_state_operator_rms": rms_operator_curve(hidden_sensitivities),
        "hidden_initial_state_operator_max": float(max(hidden_sensitivities)),
        "memory_kernel_operator_rms": rms_operator_curve(memory_magnitudes),
        "memory_kernel_operator_max": float(max(memory_magnitudes)),
        "local_positive_imag_pole": [local_pole.real, local_pole.imag],
        "matched_full_positive_imag_pole": (
            [full_pole.real, full_pole.imag] if full_pole is not None else None
        ),
        "pole_displacement_abs": (
            float(abs(full_pole - local_pole)) if full_pole is not None else None
        ),
        "local_chi": local_chi,
        "matched_full_chi": full_chi,
        "chi_displacement_abs": (
            float(abs(full_chi - local_chi))
            if full_chi is not None and local_chi is not None
            else None
        ),
        "full_spectral_abscissa": float(max(np.real(np.linalg.eigvals(L)))),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--horizon", type=float, default=2.0)
    parser.add_argument("--samples", type=int, default=401)
    parser.add_argument("--omega-p", type=float, default=2.0 * math.pi * 10.0)
    parser.add_argument("--zeta-p", type=float, default=0.30)
    parser.add_argument("--omega-q", type=float, default=2.0 * math.pi * 18.0)
    parser.add_argument("--zeta-q", type=float, default=0.40)
    parser.add_argument("--coupling-fraction", type=float, action="append", default=None)
    args = parser.parse_args()

    fractions = args.coupling_fraction if args.coupling_fraction is not None else [0.0, 0.05, 0.10, 0.20]
    base_scale = args.omega_p * args.omega_p

    payload = {
        "status": "EXPLORATORY_KNOWN_TRUTH_ONLY",
        "licenses_real_eeg_local_chi": False,
        "defines_closure_threshold": False,
        "horizon_seconds": args.horizon,
        "samples": args.samples,
        "resolved_mode": {
            "omega_rad_s": args.omega_p,
            "zeta": args.zeta_p,
        },
        "hidden_mode": {
            "omega_rad_s": args.omega_q,
            "zeta": args.zeta_q,
        },
        "cells": [],
    }

    for fraction in fractions:
        coupling = float(fraction) * base_scale
        fixtures = {
            "closed": (0.0, 0.0),
            "p_to_q_leakage_only": (0.0, coupling),
            "q_to_p_hidden_input_only": (coupling, 0.0),
            "bidirectional_return_memory": (coupling, coupling),
        }
        for label, (c_q_to_p, c_p_to_q) in fixtures.items():
            L = generator(
                omega_p=args.omega_p,
                zeta_p=args.zeta_p,
                omega_q=args.omega_q,
                zeta_q=args.zeta_q,
                c_q_to_p=c_q_to_p,
                c_p_to_q=c_p_to_q,
            )
            cell = {
                "class": label,
                "coupling_fraction": float(fraction),
                "c_q_to_p": c_q_to_p,
                "c_p_to_q": c_p_to_q,
                **metrics(L, horizon=args.horizon, samples=args.samples),
            }
            payload["cells"].append(cell)

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
