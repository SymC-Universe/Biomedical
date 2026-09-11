from __future__ import annotations

import itertools
import numpy as np
from scipy.optimize import linear_sum_assignment

from .chi_conglomerate import chi_from_pole_pair


def pair_partitions_four(poles):
    """Return the three unique partitions of four poles into two unordered pairs."""
    z = np.asarray(poles, dtype=complex).reshape(-1)
    if len(z) != 4:
        raise ValueError("exactly four poles are required")
    return [
        (z[[0, 1]], z[[2, 3]]),
        (z[[0, 2]], z[[1, 3]]),
        (z[[0, 3]], z[[1, 2]]),
    ]


def pair_set_distance(reference, candidate):
    """Relative one-to-one complex-plane distance between two two-pole sets."""
    ref = np.asarray(reference, dtype=complex).reshape(-1)
    cand = np.asarray(candidate, dtype=complex).reshape(-1)
    if len(ref) != 2 or len(cand) != 2:
        raise ValueError("reference and candidate must each contain two poles")
    denom = np.maximum(1.0, np.abs(ref))[:, None]
    cost = np.abs(ref[:, None] - cand[None, :]) / denom
    rows, cols = linear_sum_assignment(cost)
    return float(np.mean(cost[rows, cols]))


def conjugacy_mismatch(pair):
    z = np.asarray(pair, dtype=complex).reshape(-1)
    if len(z) != 2:
        raise ValueError("pair must contain two poles")
    scale = max(1.0, float(np.mean(np.abs(z))))
    return float(abs(z[0] - np.conj(z[1])) / scale)


def initial_two_lineages(poles):
    """Initialize two lineages from the most conjugate-compatible partition.

    After choosing a partition without truth, lineages are labeled by increasing
    reconstructed natural scale omega_n. This initializer is intended for a
    starting record where both second-order factors are algebraically valid.
    """
    candidates = []
    for idx, (a, b) in enumerate(pair_partitions_four(poles)):
        try:
            ia = chi_from_pole_pair(a)
            ib = chi_from_pole_pair(b)
        except Exception:
            continue
        score = conjugacy_mismatch(a) + conjugacy_mismatch(b)
        candidates.append((score, idx, a.copy(), b.copy(), ia, ib))
    if not candidates:
        raise ValueError("no algebraically valid initial two-lineage partition")
    score, idx, a, b, ia, ib = min(candidates, key=lambda x: x[0])
    if ia["omega_n"] <= ib["omega_n"]:
        pairs = [a, b]
        invariants = [ia, ib]
    else:
        pairs = [b, a]
        invariants = [ib, ia]
    return {
        "pairs": pairs,
        "invariants": invariants,
        "partition_index": int(idx),
        "initialization_cost": float(score),
        "label_rule": "INCREASING_RECONSTRUCTED_OMEGA_N",
    }


def advance_two_lineages(previous_pairs, current_poles):
    """Choose current two-pair partition and labeling by minimum continuity cost."""
    prev = [np.asarray(p, dtype=complex).reshape(-1) for p in previous_pairs]
    if len(prev) != 2 or any(len(p) != 2 for p in prev):
        raise ValueError("previous_pairs must contain two two-pole sets")
    best = None
    for idx, partition in enumerate(pair_partitions_four(current_poles)):
        for swap in (False, True):
            cand = [partition[1], partition[0]] if swap else [partition[0], partition[1]]
            cost0 = pair_set_distance(prev[0], cand[0])
            cost1 = pair_set_distance(prev[1], cand[1])
            total = cost0 + cost1
            item = (total, idx, swap, cand[0].copy(), cand[1].copy(), cost0, cost1)
            if best is None or item[0] < best[0]:
                best = item
    total, idx, swap, a, b, cost0, cost1 = best
    return {
        "pairs": [a, b],
        "partition_index": int(idx),
        "partition_swapped": bool(swap),
        "continuity_cost_total": float(total),
        "continuity_cost_by_lineage": [float(cost0), float(cost1)],
    }


def count_valid_second_order_partitions(poles):
    """Count static pair partitions yielding two stable real-coefficient factors."""
    count = 0
    valid = []
    for idx, (a, b) in enumerate(pair_partitions_four(poles)):
        try:
            ia = chi_from_pole_pair(a)
            ib = chi_from_pole_pair(b)
        except Exception:
            continue
        count += 1
        valid.append(
            {
                "partition_index": int(idx),
                "chi": [float(ia["chi"]), float(ib["chi"])],
                "omega_n": [float(ia["omega_n"]), float(ib["omega_n"])],
            }
        )
    return {"count": int(count), "valid": valid}
