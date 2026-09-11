from __future__ import annotations
import numpy as np
from scipy.optimize import linear_sum_assignment
from .selector import mac, pole_distance


def _global_assignment_margin(cost, chosen_row, chosen_col, base_total):
    """Cost increase when one chosen pair is forbidden and assignment re-solved."""
    alt = np.asarray(cost, float).copy()
    alt[int(chosen_row), int(chosen_col)] = np.inf
    try:
        rr, cc = linear_sum_assignment(alt)
    except ValueError:
        return np.inf
    chosen_costs = alt[rr, cc]
    if np.any(~np.isfinite(chosen_costs)):
        return np.inf
    alt_total = float(np.sum(chosen_costs))
    delta = alt_total - float(base_total)
    tol = 1e-12 * max(abs(float(base_total)), abs(alt_total), 1.0)
    if delta < -tol:
        raise RuntimeError("alternative assignment improved on reported global optimum")
    return float(max(delta, 0.0))


def track_modes(vals_a, shapes_a, vals_b, shapes_b, min_hz=0.0):
    """Return P0 cross-order assignment candidates without scientific labels.

    A Hungarian assignment is bookkeeping, not evidence that a mode is truly
    shared, lost, or added. Unmatched modes are therefore reported as
    cardinality-unmatched candidates. `assignment_margin` is the nonnegative
    increase in the globally re-optimized assignment cost when that chosen pair
    is forbidden. Zero means an equally good global alternative exists.
    """
    va = np.asarray(vals_a, complex)
    vb = np.asarray(vals_b, complex)
    sa = np.asarray(shapes_a, complex)
    sb = np.asarray(shapes_b, complex)

    if sa.ndim != 2 or sb.ndim != 2 or sa.shape[0] != sb.shape[0]:
        raise ValueError("mode-shape matrices must share channel dimension")
    if sa.shape[1] != len(va) or sb.shape[1] != len(vb):
        raise ValueError("mode-shape column count must match pole count")

    ia = np.where(va.imag / (2 * np.pi) >= float(min_hz))[0]
    ib = np.where(vb.imag / (2 * np.pi) >= float(min_hz))[0]
    if len(ia) == 0 or len(ib) == 0:
        return {
            "status": "P0_ASSIGNMENT_NOT_ADJUDICATED",
            "assignment_total_cost": 0.0,
            "candidate_pairs": [],
            "unmatched_a": [int(i) for i in ia],
            "unmatched_b": [int(j) for j in ib],
            "semantic_note": "No shared/lost/added claim is licensed by assignment alone.",
        }

    cost = np.empty((len(ia), len(ib)), float)
    meta = {}
    for r, i in enumerate(ia):
        for c, j in enumerate(ib):
            d = pole_distance(va[i], vb[j])
            m = mac(sa[:, i], sb[:, j])
            m = 0.0 if not np.isfinite(m) else m
            combined = float(d + (1.0 - m))
            cost[r, c] = combined
            meta[(r, c)] = (d, m, combined)

    rr, cc = linear_sum_assignment(cost)
    base_total = float(np.sum(cost[rr, cc]))
    candidate_pairs = []
    used_a = set()
    used_b = set()
    for r, c in zip(rr, cc):
        i, j = int(ia[r]), int(ib[c])
        d, m, combined = meta[(r, c)]
        margin = _global_assignment_margin(cost, r, c, base_total)
        candidate_pairs.append(
            {
                "a_index": i,
                "b_index": j,
                "pole_distance": float(d),
                "MAC": float(m),
                "combined_cost": combined,
                "assignment_margin": margin,
                "status": "CANDIDATE_PAIR_NOT_ADJUDICATED",
            }
        )
        used_a.add(i)
        used_b.add(j)

    unmatched_a = [int(i) for i in ia if int(i) not in used_a]
    unmatched_b = [int(j) for j in ib if int(j) not in used_b]
    return {
        "status": "P0_ASSIGNMENT_NOT_ADJUDICATED",
        "assignment_total_cost": base_total,
        "candidate_pairs": candidate_pairs,
        "unmatched_a": unmatched_a,
        "unmatched_b": unmatched_b,
        "semantic_note": (
            "Assignment and cardinality-unmatched modes are candidates only; "
            "shared/lost/added requires a later frozen uncertainty-aware rule."
        ),
    }
