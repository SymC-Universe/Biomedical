from __future__ import annotations
import numpy as np

from .dmd import fit_subspace_dmd, subspace_dmd_projected_singular_values
from .mode_tracking import track_modes
from .ssi_cov import decompose, fit_from_decomposition


def singular_gap_ratio(singular_values, rank):
    s = np.asarray(singular_values, float)
    rank = int(rank)
    if rank <= 0 or rank >= len(s):
        return np.nan
    return float(s[rank - 1] / max(s[rank], 1e-15))


def _rank_record(vals, shapes, gap):
    vals = np.asarray(vals, complex)
    shapes = np.asarray(shapes, complex)
    return {
        "status": "OK",
        "vals": vals,
        "shapes": shapes,
        "singular_gap_ratio": float(gap) if np.isfinite(gap) else np.nan,
        "unstable_fraction": float(np.mean(vals.real >= 0.0)) if len(vals) else np.nan,
    }


def sweep_ssi_cov(Y, dt, block_rows, candidate_orders):
    """Truth-blind SSI-COV order sweep. No order is selected here."""
    U, S, p = decompose(Y, block_rows)
    fits = {}
    for order in sorted({int(x) for x in candidate_orders}):
        try:
            vals, shapes = fit_from_decomposition(U, S, p, order, dt)
            fits[order] = _rank_record(vals, shapes, singular_gap_ratio(S, order))
        except Exception as exc:
            fits[order] = {
                "status": "METHOD_EXCEPTION_PRESERVED",
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "singular_gap_ratio": singular_gap_ratio(S, order),
            }
    return {
        "method": "SSI_COV",
        "singular_values": np.asarray(S, float),
        "fits": fits,
        "selection": None,
        "selection_status": "NO_SELECTION_P0_SWEEP_ONLY",
    }


def sweep_subspace_dmd(Y, dt, candidate_ranks):
    """Truth-blind Subspace-DMD rank sweep. No rank is selected here."""
    S = subspace_dmd_projected_singular_values(Y)
    fits = {}
    for rank in sorted({int(x) for x in candidate_ranks}):
        try:
            vals, shapes = fit_subspace_dmd(Y, dt, rank)
            fits[rank] = _rank_record(vals, shapes, singular_gap_ratio(S, rank))
        except Exception as exc:
            fits[rank] = {
                "status": "METHOD_EXCEPTION_PRESERVED",
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "singular_gap_ratio": singular_gap_ratio(S, rank),
            }
    return {
        "method": "SUBSPACE_DMD",
        "singular_values": np.asarray(S, float),
        "fits": fits,
        "selection": None,
        "selection_status": "NO_SELECTION_P0_SWEEP_ONLY",
    }


def adjacent_rank_stability(sweep, min_hz=0.0):
    """Expose data-only cross-rank assignments without accepting/rejecting modes."""
    fits = sweep["fits"]
    ranks = sorted(fits)
    out = []
    for a, b in zip(ranks[:-1], ranks[1:]):
        ra, rb = fits[a], fits[b]
        if ra.get("status") != "OK" or rb.get("status") != "OK":
            out.append({
                "rank_a": int(a),
                "rank_b": int(b),
                "status": "UNRESOLVED_METHOD_EXCEPTION",
            })
            continue
        track = track_modes(
            ra["vals"], ra["shapes"], rb["vals"], rb["shapes"], min_hz=min_hz
        )
        pairs = track["candidate_pairs"]
        pole = np.asarray([p["pole_distance"] for p in pairs], float)
        mac = np.asarray([p["MAC"] for p in pairs], float)
        margins = np.asarray([p["assignment_margin"] for p in pairs], float)
        finite_margin = margins[np.isfinite(margins)]
        out.append({
            "rank_a": int(a),
            "rank_b": int(b),
            "status": "P0_ASSIGNMENT_NOT_ADJUDICATED",
            "candidate_pairs": int(len(pairs)),
            "unmatched_a": int(len(track["unmatched_a"])),
            "unmatched_b": int(len(track["unmatched_b"])),
            "median_pole_distance": float(np.median(pole)) if len(pole) else None,
            "median_MAC": float(np.median(mac)) if len(mac) else None,
            "minimum_finite_assignment_margin": (
                float(np.min(finite_margin)) if len(finite_margin) else None
            ),
        })
    return out
