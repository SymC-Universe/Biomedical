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


def _templates():
    mx = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float)
    mv = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float)
    mm = np.array([[0.0, 0.0], [1.0, 1.0]], dtype=float) / np.sqrt(2.0)
    return {
        "POSITION_OUT_POSITION_RETURN": (mx, mx),
        "POSITION_OUT_VELOCITY_RETURN": (mx, mv),
        "VELOCITY_OUT_POSITION_RETURN": (mv, mx),
        "VELOCITY_OUT_VELOCITY_RETURN": (mv, mv),
        "MIXED_OUT_MIXED_RETURN": (mm, mm),
    }


def recovery_summary(A, t_grid=T_GRID):
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be square")
    if not np.all(np.isfinite(A)):
        raise ValueError("A must be finite")
    t_grid = np.asarray(t_grid, dtype=float).reshape(-1)
    if len(t_grid) == 0 or np.any(~np.isfinite(t_grid)) or np.any(t_grid < 0.0):
        raise ValueError("t_grid must contain finite nonnegative times")

    poles = np.linalg.eigvals(A)
    alpha = float(np.max(poles.real))
    gains = np.array([float(svdvals(expm(A * float(t)))[0]) for t in t_grid])
    i_peak = int(np.argmax(gains))
    return {
        "spectral_abscissa_per_s": alpha,
        "asymptotically_stable": bool(alpha < 0.0),
        "dominant_asymptotic_time_scale_s": float(-1.0 / alpha) if alpha < 0.0 else None,
        "worst_case_dimensionless_transient_gain": float(gains[i_peak]),
        "worst_case_peak_time_s": float(t_grid[i_peak]),
        "gain_at_final_time": float(gains[-1]),
        "poles": [_complex_dict(z) for z in poles],
    }


def run_surface():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    rows = []

    for name, (out_template, return_template) in _templates().items():
        for g in G_VALUES:
            K10 = float(g) * out_template
            K01 = float(g) * return_template
            couplings = {} if g == 0.0 else {(1, 0): K10, (0, 1): K01}
            A = assemble_coupled_generator([A0, A1], couplings)["generator"]
            row = {
                "variant": name,
                "coupling_rate": float(g),
                "out_edge_norm": float(np.linalg.norm(K10, 2)),
                "return_edge_norm": float(np.linalg.norm(K01, 2)),
                **recovery_summary(A),
            }
            rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = run_surface()
    payload = {
        "status": "P0-D20_RECOVERY_TRANSFORMATION_GEOMETRY_NOT_P0Q_NOT_P1",
        "question": (
            "With local subsystem dynamics and matched directed edge norms fixed, does feedback "
            "transformation geometry alter asymptotic recovery and finite-time transient amplification?"
        ),
        "design": {
            "local_chi_fixed": [0.55, 0.85],
            "local_frequency_hz_fixed": [3.0, 5.0],
            "coupling_rates": G_VALUES,
            "time_grid_seconds": [0.0, 5.0],
            "time_grid_points": int(len(T_GRID)),
            "state_metric": (
                "Euclidean induced 2-norm on the synthetic dimensionless-state realization only; "
                "not licensed as a real-neural metric"
            ),
            "atlas_used": False,
            "outcome_labels_used": False,
            "chi_1p2_1p3_target_used": False,
            "thresholds_frozen": False,
        },
        "rows": rows,
        "nonclaims": [
            "No neural coupling orientation or biological magnitude is inferred.",
            "No transformation family is preferred a priori.",
            "No recovery threshold is selected.",
            "No single chi_system is defined.",
            "No Atlas evidence or phenotype outcome is used.",
            "The prospective chi 1.2-1.3 note is not used as a target or interpretation rule.",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(out.resolve())

    for target_g in [12.0, 22.0]:
        for row in [r for r in rows if r["coupling_rate"] == target_g]:
            print(json.dumps({
                "variant": row["variant"],
                "g": row["coupling_rate"],
                "edge_norms": [row["out_edge_norm"], row["return_edge_norm"]],
                "stable": row["asymptotically_stable"],
                "spectral_abscissa": row["spectral_abscissa_per_s"],
                "tau": row["dominant_asymptotic_time_scale_s"],
                "worst_case_gain": row["worst_case_dimensionless_transient_gain"],
                "peak_time": row["worst_case_peak_time_s"],
            }, sort_keys=True))
    print("P0-D20 RECOVERY TRANSFORMATION GEOMETRY COMPLETE. No recovery, chi_system, or neural rule frozen.")


if __name__ == "__main__":
    main()
