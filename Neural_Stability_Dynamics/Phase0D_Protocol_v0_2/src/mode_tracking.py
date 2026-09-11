from __future__ import annotations
import numpy as np
from scipy.optimize import linear_sum_assignment
from .selector import mac, pole_distance


def _alternative_min(values, excluded_index):
    values = np.asarray(values, float)
    if values.size <= 1:
        return np.inf
    keep = np.ones(values.size, dtype=bool)
    keep[int(excluded_index)] = False
    return float(np.min(values[keep]))


def track_modes(vals_a, shapes_a, vals_b, shapes_b, min_hz=0.0):
    """Return P0 cross-order assignment candidates without scientific labels.

    A Hungarian assignment is bookkeeping, not evidence that a mode is truly
    shared, lost, or added. Unmatched modes are therefore reported as
    cardinality-unmatched candidates, and assignment margins are exposed so
    ambiguous pairings remain visible for later uncertainty-aware adjudication.
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
    candidate_pairs = []
    used_a = set()
    used_b = set()
    for r, c in zip(rr, cc):
        i, j = int(ia[r]), int(ib[c])
        d, m, combined = meta[(r, c)]
        row_alt = _alternative_min(cost[r, :], c)
        col_alt = _alternative_min(cost[:, c], r)
        best_alt = min(row_alt, col_alt)
        margin = np.inf if not np.isfinite(best_alt) else float(best_alt - combined)
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
        "candidate_pairs": candidate_pairs,
        "unmatched_a": unmatched_a,
        "unmatched_b": unmatched_b,
        "semantic_note": (
            "Assignment and cardinality-unmatched modes are candidates only; "
            "shared/lost/added requires a later frozen uncertainty-aware rule."
        ),
    }
