from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np

from src.chi_conglomerate import chi_from_pole_pair, second_order_generator
from src.coupled_conglomeration import (
    assemble_coupled_generator,
    feedback_return_operator,
)


def _complex_dict(z):
    z = complex(z)
    return {"real": float(z.real), "imag": float(z.imag)}


def _matrix_complex_dict(A):
    A = np.asarray(A, complex)
    return [[_complex_dict(z) for z in row] for row in A]


def _pair_distance(a, b):
    a = np.asarray(a, complex)
    b = np.asarray(b, complex)
    return float(
        min(
            abs(a[0] - b[0]) + abs(a[1] - b[1]),
            abs(a[0] - b[1]) + abs(a[1] - b[0]),
        )
    )


def _all_partitions(vals):
    vals = list(np.asarray(vals, complex).reshape(-1))
    if len(vals) != 4:
        raise ValueError("P0-D17 expects four poles")
    return [
        [np.array([vals[0], vals[1]]), np.array([vals[2], vals[3]])],
        [np.array([vals[0], vals[2]]), np.array([vals[1], vals[3]])],
        [np.array([vals[0], vals[3]]), np.array([vals[1], vals[2]])],
    ]


def _real_factor(pair, tol=1e-7):
    p = np.asarray(pair, complex)
    gamma = -(p[0] + p[1])
    omega2 = p[0] * p[1]
    scale = max(1.0, abs(gamma), abs(omega2))
    return bool(
        abs(gamma.imag) <= tol * scale
        and abs(omega2.imag) <= tol * scale
        and omega2.real > 0.0
    )


def _track_partition(previous, poles):
    candidates = []
    for partition in _all_partitions(poles):
        if all(_real_factor(pair) for pair in partition):
            candidates.append(partition)
    if not candidates:
        return None, None
    if previous is None:
        # At g=0 the two local factors are distinct in natural scale.
        scored = []
        for partition in candidates:
            try:
                wn = [chi_from_pole_pair(pair)["omega_n"] for pair in partition]
            except ValueError:
                continue
            order = np.argsort(wn)
            sorted_partition = [partition[int(order[0])], partition[int(order[1])]]
            separation = abs(wn[int(order[1])] - wn[int(order[0])])
            scored.append((separation, sorted_partition))
        if not scored:
            return None, None
        _, selected = max(scored, key=lambda item: item[0])
        return selected, 0.0

    best = None
    for partition in candidates:
        direct = _pair_distance(previous[0], partition[0]) + _pair_distance(previous[1], partition[1])
        swapped = _pair_distance(previous[0], partition[1]) + _pair_distance(previous[1], partition[0])
        if swapped < direct:
            partition = [partition[1], partition[0]]
            cost = swapped
        else:
            cost = direct
        if best is None or cost < best[0]:
            best = (cost, partition)
    return best[1], float(best[0])


def _factor_summary(pair):
    try:
        out = chi_from_pole_pair(pair)
        branch = "COMPLEX_PAIR" if np.max(np.abs(np.asarray(pair).imag)) > 1e-7 else "REAL_SPLIT"
        return {
            "status": "CHI_DEFINED",
            "chi": float(out["chi"]),
            "omega_n": float(out["omega_n"]),
            "branch": branch,
            "poles": [_complex_dict(z) for z in pair],
        }
    except ValueError as exc:
        return {
            "status": "CHI_NOT_DEFINED_UNDER_STABLE_SECOND_ORDER_CONVENTION",
            "reason": str(exc),
            "poles": [_complex_dict(z) for z in pair],
        }


def _spectrum_distance(reference, current):
    ref = list(np.asarray(reference, complex))
    cur = list(np.asarray(current, complex))
    best = None
    for perm in itertools.permutations(range(len(cur))):
        cost = float(sum(abs(ref[i] - cur[perm[i]]) for i in range(len(ref))))
        if best is None or cost < best:
            best = cost
    return float(best)


def _run_variant(name, K_return_template, K_out_template, g_values, A0, A1, local_union):
    previous = None
    rows = []
    for g in g_values:
        g = float(g)
        K01 = g * K_return_template
        K10 = g * K_out_template
        couplings = {} if g == 0 else {(0, 1): K01, (1, 0): K10}
        A = assemble_coupled_generator([A0, A1], couplings)["generator"]
        poles = np.linalg.eigvals(A)
        partition, continuity_cost = _track_partition(previous, poles)
        if partition is not None:
            previous = [p.copy() for p in partition]
            factors = [_factor_summary(pair) for pair in partition]
        else:
            factors = []

        sigma0 = feedback_return_operator(A0, A1, K01, K10, s=0.0)
        sigma3 = feedback_return_operator(
            A0, A1, K01, K10, s=1j * 2.0 * np.pi * 3.0
        )
        rows.append(
            {
                "variant": name,
                "coupling_rate": g,
                "edge_norm_return": float(np.linalg.norm(K01, 2)),
                "edge_norm_out": float(np.linalg.norm(K10, 2)),
                "stable_full_system": bool(np.max(poles.real) < 0.0),
                "max_real_pole": float(np.max(poles.real)),
                "full_poles": [_complex_dict(z) for z in poles],
                "lineage_partition_status": "AVAILABLE" if partition is not None else "UNRESOLVED",
                "continuity_cost": continuity_cost,
                "global_lineages": factors,
                "feedback_return_norm_dc": float(np.linalg.norm(sigma0, 2)),
                "feedback_return_norm_3hz": float(np.linalg.norm(sigma3, 2)),
                "feedback_return_dc": _matrix_complex_dict(sigma0),
                "feedback_return_3hz": _matrix_complex_dict(sigma3),
                "spectrum_displacement_from_uncoupled": _spectrum_distance(local_union, poles),
            }
        )
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    local_union = np.concatenate([np.linalg.eigvals(A0), np.linalg.eigvals(A1)])

    mx = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=float)
    mv = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=float)
    mm = np.array([[0.0, 0.0], [1.0, 1.0]], dtype=float) / np.sqrt(2.0)

    variants = {
        "POSITION_OUT_POSITION_RETURN": (mx, mx),
        "POSITION_OUT_VELOCITY_RETURN": (mv, mx),
        "VELOCITY_OUT_POSITION_RETURN": (mx, mv),
        "VELOCITY_OUT_VELOCITY_RETURN": (mv, mv),
        "MIXED_OUT_MIXED_RETURN": (mm, mm),
    }
    # Every nonzero edge template has spectral norm 1, so every variant has the
    # same outgoing and return edge norms at fixed g. Only transformation
    # geometry differs.
    g_values = [0, 2, 4, 6, 8, 10, 12]

    surfaces = {
        name: _run_variant(name, ret, out, g_values, A0, A1, local_union)
        for name, (ret, out) in variants.items()
    }

    payload = {
        "status": "P0-D17_DEVELOPMENTAL_TRANSFORMATION_GEOMETRY_NOT_P0Q_NOT_P1",
        "question": (
            "At equal directed edge norms, does changing the transformation applied along the "
            "outgoing and return pathways change the feedback-return operator and emergent global dynamics?"
        ),
        "design": {
            "local_chi_fixed": [0.55, 0.85],
            "local_frequency_hz_fixed": [3.0, 5.0],
            "coupling_rates": g_values,
            "template_spectral_norms": {
                name: [float(np.linalg.norm(ret, 2)), float(np.linalg.norm(out, 2))]
                for name, (ret, out) in variants.items()
            },
            "atlas_used": False,
            "outcome_labels_used": False,
            "thresholds_frozen": False,
        },
        "surfaces": surfaces,
        "nonclaims": [
            "No neural coupling orientation is inferred.",
            "No transformation family is preferred.",
            "No coupling threshold is selected.",
            "No single system chi is defined.",
            "No Atlas evidence is used.",
        ],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(out.resolve())

    for name, rows in surfaces.items():
        last = rows[-1]
        chis = [
            item.get("chi")
            for item in last["global_lineages"]
            if item.get("status") == "CHI_DEFINED"
        ]
        print(
            json.dumps(
                {
                    "variant": name,
                    "g": last["coupling_rate"],
                    "edge_norms": [last["edge_norm_out"], last["edge_norm_return"]],
                    "stable": last["stable_full_system"],
                    "feedback_norm_dc": last["feedback_return_norm_dc"],
                    "feedback_norm_3hz": last["feedback_return_norm_3hz"],
                    "global_chi_defined": chis,
                    "spectrum_displacement": last["spectrum_displacement_from_uncoupled"],
                },
                sort_keys=True,
            )
        )
    print("P0-D17 FEEDBACK TRANSFORMATION GEOMETRY COMPLETE. No coupling or chi_system rule frozen.")


if __name__ == "__main__":
    main()
