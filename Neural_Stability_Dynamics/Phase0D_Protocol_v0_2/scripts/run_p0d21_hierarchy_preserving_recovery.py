from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.linalg import expm

from src.chi_conglomerate import second_order_generator
from src.coupled_conglomeration import assemble_coupled_generator

T_GRID = np.linspace(0.0, 1.0, 1001)
H_VALUES = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]


def _environment(A1, A2, K12, K21):
    return np.block([[A1, K12], [K21, A2]])


def _full_generator(A0, A1, A2, K01, K10, K12, K21):
    Z = np.zeros((2, 2))
    return np.block([[A0, K01, Z], [K10, A1, K12], [Z, K21, A2]])


def _outer_trajectory(A, x0):
    x0 = np.asarray(x0, dtype=float)
    return np.asarray([(expm(A * float(t)) @ x0)[:2] for t in T_GRID])


def _tau(A):
    alpha = float(np.max(np.linalg.eigvals(A).real))
    return alpha, (float(-1.0 / alpha) if alpha < 0.0 else None)


def _response_metrics(full, grouped, truncated):
    perturbations = {
        "OUTER_POSITION_LIKE": np.array([1.0, 0.0]),
        "OUTER_VELOCITY_LIKE": np.array([0.0, 1.0]),
    }
    rows = {}
    for name, xg in perturbations.items():
        x_full = np.concatenate([xg, np.zeros(4)])
        x_grouped = x_full.copy()
        x_trunc = np.concatenate([xg, np.zeros(2)])
        yf = _outer_trajectory(full, x_full)
        yg = _outer_trajectory(grouped, x_grouped)
        yt = _outer_trajectory(truncated, x_trunc)
        rows[name] = {
            "max_outer_error_grouped_vs_full": float(np.max(np.linalg.norm(yg - yf, axis=1))),
            "max_outer_error_truncated_vs_full": float(np.max(np.linalg.norm(yt - yf, axis=1))),
            "full_outer_peak_norm": float(np.max(np.linalg.norm(yf, axis=1))),
            "truncated_outer_peak_norm": float(np.max(np.linalg.norm(yt, axis=1))),
            "full_outer_norm_at_1s": float(np.linalg.norm(yf[-1])),
            "truncated_outer_norm_at_1s": float(np.linalg.norm(yt[-1])),
        }
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.75, 2.0 * np.pi * 5.0)
    A2 = second_order_generator(0.90, 2.0 * np.pi * 7.0)
    M = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float)
    K01 = 4.0 * M
    K10 = 4.0 * M
    Z = np.zeros((2, 2))

    truncated = assemble_coupled_generator(
        [A0, A1], {(0, 1): K01, (1, 0): K10}
    )["generator"]
    alpha_trunc, tau_trunc = _tau(truncated)

    rows = []
    for h in H_VALUES:
        K12 = float(h) * M
        K21 = float(h) * M
        full = _full_generator(A0, A1, A2, K01, K10, K12, K21)
        Ae = _environment(A1, A2, K12, K21)
        K0e = np.hstack([K01, Z])
        Ke0 = np.vstack([K10, Z])
        grouped = assemble_coupled_generator(
            [A0, Ae], {(0, 1): K0e, (1, 0): Ke0}
        )["generator"]

        alpha_full, tau_full = _tau(full)
        alpha_grouped, tau_grouped = _tau(grouped)
        response = _response_metrics(full, grouped, truncated)
        rows.append({
            "intermediary_coupling_h": float(h),
            "full_grouped_generator_max_abs_difference": float(np.max(np.abs(full - grouped))),
            "spectral_abscissa_full": alpha_full,
            "spectral_abscissa_grouped": alpha_grouped,
            "spectral_abscissa_truncated": alpha_trunc,
            "tau_full_s": tau_full,
            "tau_grouped_s": tau_grouped,
            "tau_truncated_s": tau_trunc,
            "stable_full": bool(alpha_full < 0.0),
            "stable_grouped": bool(alpha_grouped < 0.0),
            "stable_truncated": bool(alpha_trunc < 0.0),
            "outer_response": response,
        })

    payload = {
        "status": "P0-D21_HIERARCHY_PRESERVING_RECOVERY_NOT_P0Q_NOT_P1",
        "question": (
            "Does exact hierarchical grouping preserve outer-system recovery when internal dynamics are retained, "
            "and how much recovery error appears if the internally coupled subsystem is incorrectly dropped?"
        ),
        "design": {
            "local_chi_fixed": [0.55, 0.75, 0.90],
            "local_frequency_hz_fixed": [3.0, 5.0, 7.0],
            "outer_G_B_edge_norm_fixed": 4.0,
            "intermediary_B_C_edge_norms": H_VALUES,
            "time_grid_seconds": [0.0, 1.0],
            "time_grid_points": int(len(T_GRID)),
            "grouped_representation_retains_internal_B_C_state": True,
            "truncated_control_drops_C": True,
            "atlas_used": False,
            "thresholds_frozen": False,
        },
        "rows": rows,
        "nonclaims": [
            "Exact regrouping is not claimed to be dimensionality reduction.",
            "No biological hierarchy is inferred.",
            "No acceptable reduction-error threshold is selected.",
            "No chi_system is defined.",
            "No Atlas evidence or outcome labels are used.",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(out.resolve())
    for row in rows:
        print(json.dumps({
            "h": row["intermediary_coupling_h"],
            "stable": row["stable_full"],
            "tau_full": row["tau_full_s"],
            "tau_truncated": row["tau_truncated_s"],
            "grouped_matrix_error": row["full_grouped_generator_max_abs_difference"],
            "position_outer_error_grouped": row["outer_response"]["OUTER_POSITION_LIKE"]["max_outer_error_grouped_vs_full"],
            "position_outer_error_truncated": row["outer_response"]["OUTER_POSITION_LIKE"]["max_outer_error_truncated_vs_full"],
            "velocity_outer_error_grouped": row["outer_response"]["OUTER_VELOCITY_LIKE"]["max_outer_error_grouped_vs_full"],
            "velocity_outer_error_truncated": row["outer_response"]["OUTER_VELOCITY_LIKE"]["max_outer_error_truncated_vs_full"],
        }, sort_keys=True))
    print("P0-D21 HIERARCHY-PRESERVING RECOVERY COMPLETE. No reduction threshold or chi_system rule frozen.")


if __name__ == "__main__":
    main()
