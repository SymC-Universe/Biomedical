from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.linalg import expm, svdvals

from src.chi_conglomerate import second_order_generator
from src.coupled_conglomeration import assemble_coupled_generator


G_VALUES = [0.0, 4.0, 8.0, 12.0, 14.0, 18.0, 22.0]
T_GRID = np.linspace(0.0, 5.0, 2001)


def _complex_dict(z):
    z = complex(z)
    return {"real": float(z.real), "imag": float(z.imag)}


def _response_metrics(A, x0):
    x0 = np.asarray(x0, dtype=float)
    x0 = x0 / np.linalg.norm(x0)
    norms = []
    for t in T_GRID:
        xt = expm(A * float(t)) @ x0
        norms.append(float(np.linalg.norm(xt, 2)))
    norms = np.asarray(norms)
    i_peak = int(np.argmax(norms))
    return {
        "peak_norm": float(norms[i_peak]),
        "peak_time_s": float(T_GRID[i_peak]),
        "norm_at_5s": float(norms[-1]),
    }


def _worst_case_transient(A):
    gains = []
    for t in T_GRID:
        gains.append(float(svdvals(expm(A * float(t)))[0]))
    gains = np.asarray(gains)
    i_peak = int(np.argmax(gains))
    return {
        "max_induced_gain": float(gains[i_peak]),
        "peak_time_s": float(T_GRID[i_peak]),
        "gain_at_5s": float(gains[-1]),
    }


def _row(architecture, g, A0, A1, M):
    if architecture == "ONE_WAY_0_TO_1":
        couplings = {(1, 0): g * M} if g else {}
    elif architecture == "BIDIRECTIONAL_CLOSED_LOOP":
        couplings = {(1, 0): g * M, (0, 1): g * M} if g else {}
    else:
        raise ValueError("unknown architecture")

    A = assemble_coupled_generator([A0, A1], couplings)["generator"]
    poles = np.linalg.eigvals(A)
    spectral_abscissa = float(np.max(poles.real))
    tau = float(-1.0 / spectral_abscissa) if spectral_abscissa < 0.0 else None

    perturbations = {
        "SUBSYSTEM0_POSITION_LIKE": [1.0, 0.0, 0.0, 0.0],
        "SUBSYSTEM0_VELOCITY_LIKE": [0.0, 1.0, 0.0, 0.0],
        "SUBSYSTEM1_POSITION_LIKE": [0.0, 0.0, 1.0, 0.0],
        "SUBSYSTEM1_VELOCITY_LIKE": [0.0, 0.0, 0.0, 1.0],
    }
    response = {name: _response_metrics(A, x0) for name, x0 in perturbations.items()}

    return {
        "architecture": architecture,
        "coupling_rate": float(g),
        "local_chi_fixed": [0.55, 0.85],
        "spectral_abscissa_per_s": spectral_abscissa,
        "asymptotically_stable": bool(spectral_abscissa < 0.0),
        "dominant_asymptotic_time_scale_s": tau,
        "poles": [_complex_dict(z) for z in poles],
        "predeclared_perturbation_responses": response,
        "worst_case_dimensionless_transient": _worst_case_transient(A),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    M = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float)

    rows = []
    for architecture in ["ONE_WAY_0_TO_1", "BIDIRECTIONAL_CLOSED_LOOP"]:
        for g in G_VALUES:
            rows.append(_row(architecture, float(g), A0, A1, M))

    payload = {
        "status": "P0-D19_DEVELOPMENTAL_CLOSED_LOOP_RECOVERY_PREDICTION_NOT_P0Q_NOT_P1",
        "question": (
            "Do fixed local subsystem dynamics produce different asymptotic and finite-time "
            "recovery behavior when only contribution/feedback architecture changes?"
        ),
        "design": {
            "local_subsystem_0": {"chi": 0.55, "frequency_hz": 3.0},
            "local_subsystem_1": {"chi": 0.85, "frequency_hz": 5.0},
            "coupling_rates": G_VALUES,
            "time_grid_seconds": [0.0, 5.0],
            "time_grid_points": int(len(T_GRID)),
            "state_metric": (
                "Euclidean norm on the synthetic dimensionless-state realization only; "
                "not licensed as a real-neural state metric"
            ),
            "atlas_used": False,
            "recovery_threshold_frozen": False,
        },
        "rows": rows,
        "nonclaims": [
            "No clinical recovery prediction is inferred.",
            "No chi threshold is equated with failure to recover.",
            "No finite-time safety threshold is frozen.",
            "The transient norm is meaningful only for this explicitly dimensionless synthetic state realization.",
            "No Atlas outcome or phenotype information is used.",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(out.resolve())
    for row in rows:
        print(json.dumps({
            "architecture": row["architecture"],
            "g": row["coupling_rate"],
            "stable": row["asymptotically_stable"],
            "spectral_abscissa": row["spectral_abscissa_per_s"],
            "tau": row["dominant_asymptotic_time_scale_s"],
            "worst_case_gain": row["worst_case_dimensionless_transient"]["max_induced_gain"],
            "worst_case_peak_time": row["worst_case_dimensionless_transient"]["peak_time_s"],
        }, sort_keys=True))
    print("P0-D19 CLOSED-LOOP RECOVERY PREDICTION COMPLETE. No recovery or chi rule frozen.")


if __name__ == "__main__":
    main()
