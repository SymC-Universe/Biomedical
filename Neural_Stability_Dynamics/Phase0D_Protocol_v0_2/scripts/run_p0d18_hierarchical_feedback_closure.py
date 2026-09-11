from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.chi_conglomerate import second_order_generator
from src.coupled_conglomeration import feedback_return_operator


def _complex_dict(z):
    z = complex(z)
    return {"real": float(z.real), "imag": float(z.imag)}


def _matrix_complex_dict(A):
    A = np.asarray(A, complex)
    return [[_complex_dict(z) for z in row] for row in A]


def _environment(A1, A2, K12, K21):
    return np.block([[A1, K12], [K21, A2]])


def _nested_feedback(A1, A2, K01, K10, K12, K21, s):
    M2 = complex(s) * np.eye(A2.shape[0]) - A2
    sigma_1_from_2 = K12 @ np.linalg.solve(M2, K21)
    M1_eff = complex(s) * np.eye(A1.shape[0]) - A1 - sigma_1_from_2
    return K01 @ np.linalg.solve(M1_eff, K10)


def _full_generator(A0, A1, A2, K01, K10, K12, K21):
    Z = np.zeros((2, 2))
    return np.block(
        [
            [A0, K01, Z],
            [K10, A1, K12],
            [Z, K21, A2],
        ]
    )


def _complex_pair_coordinates(poles, tol=1e-8):
    vals = np.asarray(poles, complex)
    positive = [z for z in vals if z.imag > tol]
    rows = []
    for z in sorted(positive, key=lambda q: abs(q.imag)):
        omega_n = float(abs(z))
        chi = float(-z.real / omega_n) if omega_n > 0 else float("nan")
        rows.append(
            {
                "pole": _complex_dict(z),
                "frequency_hz": float(abs(z.imag) / (2.0 * np.pi)),
                "omega_n": omega_n,
                "chi": chi,
            }
        )
    real_poles = [z for z in vals if abs(z.imag) <= tol]
    return {
        "complex_pair_coordinates": rows,
        "real_poles_unpaired": [_complex_dict(z) for z in real_poles],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    # Outer group G and intermediary subsystems B,C. All local generators and
    # outer G<->B couplings stay fixed. Only the internal B<->C feedback is varied.
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.75, 2.0 * np.pi * 5.0)
    A2 = second_order_generator(0.90, 2.0 * np.pi * 7.0)
    M = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float)
    K01 = 4.0 * M
    K10 = 4.0 * M
    Z = np.zeros((2, 2))

    h_values = [0, 1, 2, 3, 4, 5, 6, 8, 10]
    rows = []
    for h in h_values:
        h = float(h)
        K12 = h * M
        K21 = h * M
        Ae = _environment(A1, A2, K12, K21)
        K0e = np.hstack([K01, Z])
        Ke0 = np.vstack([K10, Z])
        A_full = _full_generator(A0, A1, A2, K01, K10, K12, K21)
        poles = np.linalg.eigvals(A_full)

        sigma_direct_dc = feedback_return_operator(A0, A1, K01, K10, s=0.0)
        sigma_grouped_dc = feedback_return_operator(A0, Ae, K0e, Ke0, s=0.0)
        sigma_nested_dc = _nested_feedback(A1, A2, K01, K10, K12, K21, s=0.0)

        s3 = 1j * 2.0 * np.pi * 3.0
        sigma_direct_3 = feedback_return_operator(A0, A1, K01, K10, s=s3)
        sigma_grouped_3 = feedback_return_operator(A0, Ae, K0e, Ke0, s=s3)
        sigma_nested_3 = _nested_feedback(A1, A2, K01, K10, K12, K21, s=s3)

        rows.append(
            {
                "intermediary_coupling_h": h,
                "outer_edge_norms_fixed": [
                    float(np.linalg.norm(K01, 2)),
                    float(np.linalg.norm(K10, 2)),
                ],
                "intermediary_edge_norms": [
                    float(np.linalg.norm(K12, 2)),
                    float(np.linalg.norm(K21, 2)),
                ],
                "stable_full_system": bool(np.max(poles.real) < 0.0),
                "max_real_pole": float(np.max(poles.real)),
                "full_poles": [_complex_dict(z) for z in poles],
                "global_complex_pair_coordinates": _complex_pair_coordinates(poles),
                "direct_feedback_norm_dc_ignoring_C": float(np.linalg.norm(sigma_direct_dc, 2)),
                "grouped_feedback_norm_dc": float(np.linalg.norm(sigma_grouped_dc, 2)),
                "grouped_minus_direct_norm_dc": float(np.linalg.norm(sigma_grouped_dc - sigma_direct_dc, 2)),
                "nested_minus_grouped_norm_dc": float(np.linalg.norm(sigma_nested_dc - sigma_grouped_dc, 2)),
                "direct_feedback_norm_3hz_ignoring_C": float(np.linalg.norm(sigma_direct_3, 2)),
                "grouped_feedback_norm_3hz": float(np.linalg.norm(sigma_grouped_3, 2)),
                "grouped_minus_direct_norm_3hz": float(np.linalg.norm(sigma_grouped_3 - sigma_direct_3, 2)),
                "nested_minus_grouped_norm_3hz": float(np.linalg.norm(sigma_nested_3 - sigma_grouped_3, 2)),
                "grouped_feedback_dc": _matrix_complex_dict(sigma_grouped_dc),
                "grouped_feedback_3hz": _matrix_complex_dict(sigma_grouped_3),
            }
        )

    payload = {
        "status": "P0-D18_HIERARCHICAL_FEEDBACK_CLOSURE_NOT_P0Q_NOT_P1",
        "question": (
            "Can an interacting intermediary network be treated as a grouped subsystem whose effective "
            "feedback return to an outer subsystem preserves the nested closed-loop dynamics, and does "
            "changing only the intermediary interaction alter the return seen by the outer subsystem?"
        ),
        "design": {
            "local_chi_fixed": [0.55, 0.75, 0.90],
            "local_frequency_hz_fixed": [3.0, 5.0, 7.0],
            "outer_G_B_edge_norm_fixed": 4.0,
            "intermediary_B_C_edge_norms": h_values,
            "atlas_used": False,
            "thresholds_frozen": False,
        },
        "rows": rows,
        "nonclaims": [
            "No neural anatomical hierarchy is inferred.",
            "No biological coupling strength is inferred.",
            "No system chi is frozen.",
            "No Atlas outcome is used.",
            "This is an exact/synthetic linear mechanism test of hierarchical closure only.",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(out.resolve())
    for row in rows:
        print(
            json.dumps(
                {
                    "h": row["intermediary_coupling_h"],
                    "stable": row["stable_full_system"],
                    "outer_edges_fixed": row["outer_edge_norms_fixed"],
                    "grouped_minus_direct_dc": row["grouped_minus_direct_norm_dc"],
                    "grouped_minus_direct_3hz": row["grouped_minus_direct_norm_3hz"],
                    "nested_minus_grouped_dc": row["nested_minus_grouped_norm_dc"],
                    "nested_minus_grouped_3hz": row["nested_minus_grouped_norm_3hz"],
                    "global_chi_complex_pairs": [
                        x["chi"]
                        for x in row["global_complex_pair_coordinates"]["complex_pair_coordinates"]
                    ],
                },
                sort_keys=True,
            )
        )
    print("P0-D18 HIERARCHICAL FEEDBACK CLOSURE COMPLETE. No hierarchy or chi_system rule frozen.")


if __name__ == "__main__":
    main()
