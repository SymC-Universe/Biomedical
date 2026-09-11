from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from src.chi_conglomerate import chi_from_pole_pair, second_order_generator
from src.coupled_conglomeration import (
    assemble_coupled_generator,
    feedback_return_operator,
)


def _complex_dict(z):
    z = complex(z)
    return {"real": float(z.real), "imag": float(z.imag)}


def _pair_distance(a, b):
    a = np.asarray(a, complex)
    b = np.asarray(b, complex)
    return float(
        min(
            abs(a[0] - b[0]) + abs(a[1] - b[1]),
            abs(a[0] - b[1]) + abs(a[1] - b[0]),
        )
    )


def _second_order_pairs(poles, tol=1e-7):
    vals = list(np.asarray(poles, complex).reshape(-1))
    used = [False] * len(vals)
    pairs = []

    # Complex-conjugate factors are algebraically licensed without arbitrary
    # pairing. Remaining exactly-two real poles form the second real factor.
    for i, z in enumerate(vals):
        if used[i] or z.imag <= tol:
            continue
        candidates = [
            (abs(vals[j] - np.conj(z)), j)
            for j in range(len(vals))
            if j != i and not used[j]
        ]
        if not candidates:
            continue
        distance, j = min(candidates)
        scale = max(1.0, abs(z), abs(vals[j]))
        if distance <= tol * scale:
            used[i] = True
            used[j] = True
            pairs.append(np.array([z, vals[j]], dtype=complex))

    remaining = [vals[i] for i, flag in enumerate(used) if not flag]
    if remaining:
        if len(remaining) == 2 and all(abs(z.imag) <= tol for z in remaining):
            pairs.append(np.array(remaining, dtype=complex))
        else:
            raise ValueError("spectrum does not admit the unambiguous 2+2 partition used by P0-D16")
    if len(pairs) != 2:
        raise ValueError("expected exactly two second-order factors")
    return pairs


def _track_two_pairs(previous, current):
    if previous is None:
        # Initial uncoupled identity by natural scale only. No outcome/Atlas use.
        return sorted(current, key=lambda p: chi_from_pole_pair(p)["omega_n"])
    direct = _pair_distance(previous[0], current[0]) + _pair_distance(previous[1], current[1])
    swapped = _pair_distance(previous[0], current[1]) + _pair_distance(previous[1], current[0])
    return current if direct <= swapped else [current[1], current[0]]


def _surface(architecture, g_values, A0, A1, M):
    previous = None
    rows = []
    local_poles = [np.linalg.eigvals(A0), np.linalg.eigvals(A1)]
    for g in g_values:
        g = float(g)
        if architecture == "ONE_WAY_0_TO_1":
            couplings = {(1, 0): g * M} if g != 0 else {}
            K_group_from_env = np.zeros_like(M)
            K_env_from_group = g * M
        elif architecture == "BIDIRECTIONAL_CLOSED_LOOP":
            couplings = (
                {(1, 0): g * M, (0, 1): g * M} if g != 0 else {}
            )
            K_group_from_env = g * M
            K_env_from_group = g * M
        else:
            raise ValueError("unknown architecture")

        A = assemble_coupled_generator([A0, A1], couplings)["generator"]
        poles = np.linalg.eigvals(A)
        pairs = _track_two_pairs(previous, _second_order_pairs(poles))
        previous = [p.copy() for p in pairs]
        factors = [chi_from_pole_pair(p) for p in pairs]
        feedback_dc = feedback_return_operator(
            A0, A1, K_group_from_env, K_env_from_group, s=0.0
        )
        feedback_3hz = feedback_return_operator(
            A0,
            A1,
            K_group_from_env,
            K_env_from_group,
            s=1j * 2.0 * np.pi * 3.0,
        )

        # Spectrum displacement from the fixed local union, scored only as a
        # descriptive P0-D mechanism quantity.
        local_union = np.concatenate(local_poles)
        total_displacement = 0.0
        remaining = list(poles)
        for z in local_union:
            j = int(np.argmin([abs(z - q) for q in remaining]))
            total_displacement += float(abs(z - remaining[j]))
            remaining.pop(j)

        rows.append(
            {
                "architecture": architecture,
                "coupling_rate": g,
                "stable": bool(np.max(poles.real) < 0.0),
                "max_real_pole": float(np.max(poles.real)),
                "local_chi_fixed": [0.55, 0.85],
                "global_lineage_chi": [float(f["chi"]) for f in factors],
                "global_lineage_branch": [
                    "COMPLEX_PAIR" if np.max(np.abs(p.imag)) > 1e-7 else "REAL_SPLIT"
                    for p in pairs
                ],
                "global_lineage_omega_n": [float(f["omega_n"]) for f in factors],
                "global_lineage_poles": [
                    [_complex_dict(z) for z in pair] for pair in pairs
                ],
                "feedback_return_norm_dc": float(np.linalg.norm(feedback_dc, 2)),
                "feedback_return_norm_at_3hz": float(np.linalg.norm(feedback_3hz, 2)),
                "spectrum_displacement_from_fixed_local_union": float(total_displacement),
            }
        )
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    # Directed position-to-acceleration-like coupling in the dimensionless-state
    # realization. g has generator-rate units. This is a synthetic mechanism
    # surface, not a neural coupling model.
    M = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float)
    g_values = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16, 18, 20, 22]

    one_way = _surface("ONE_WAY_0_TO_1", g_values, A0, A1, M)
    closed = _surface("BIDIRECTIONAL_CLOSED_LOOP", g_values, A0, A1, M)

    payload = {
        "status": "P0-D16_DEVELOPMENTAL_COUPLED_FEEDBACK_SURFACE_NOT_P0Q_NOT_P1",
        "question": (
            "Can fixed local chi coordinates coexist with strongly changing global coupled lineages "
            "when only directed feedback closure is varied?"
        ),
        "design": {
            "local_subsystem_0": {"chi": 0.55, "frequency_hz": 3.0},
            "local_subsystem_1": {"chi": 0.85, "frequency_hz": 5.0},
            "coupling_matrix_template": M.tolist(),
            "coupling_rates": g_values,
            "architectures": ["ONE_WAY_0_TO_1", "BIDIRECTIONAL_CLOSED_LOOP"],
            "atlas_used": False,
            "thresholds_frozen": False,
        },
        "one_way": one_way,
        "closed_loop": closed,
        "nonclaims": [
            "No biological neural coupling law is inferred.",
            "No system chi formula is frozen.",
            "No coupling threshold or target zone is selected.",
            "No Atlas outcome or phenotype information is used.",
            "The surface demonstrates mechanism geometry only.",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(out.resolve())
    for row in closed:
        print(
            json.dumps(
                {
                    "g": row["coupling_rate"],
                    "stable": row["stable"],
                    "global_chi": row["global_lineage_chi"],
                    "branches": row["global_lineage_branch"],
                    "feedback_dc": row["feedback_return_norm_dc"],
                    "spectrum_displacement": row[
                        "spectrum_displacement_from_fixed_local_union"
                    ],
                },
                sort_keys=True,
            )
        )
    print("P0-D16 COUPLED FEEDBACK CHI SURFACE COMPLETE. No chi_system or P1 rule frozen.")


if __name__ == "__main__":
    main()
