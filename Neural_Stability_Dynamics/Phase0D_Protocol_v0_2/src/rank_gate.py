from __future__ import annotations
import numpy as np

from .rank_sweep import sweep_ssi_cov, sweep_subspace_dmd


def _candidate_from_sweep(sweep, candidate_grid, gap_ratio_min, min_hz):
    grid = sorted({int(x) for x in candidate_grid})
    if not grid:
        raise ValueError("candidate_grid is empty")
    finite = []
    for rank in grid:
        fit = sweep["fits"].get(rank)
        if fit is None:
            continue
        gap = fit.get("singular_gap_ratio")
        if gap is not None and np.isfinite(gap):
            finite.append((rank, float(gap)))
    if not finite:
        return {
            "decision": "REFUSE_NO_FINITE_GAP",
            "candidate_rank": None,
            "max_gap": None,
        }

    rank, gap = max(finite, key=lambda x: x[1])
    out = {
        "candidate_rank": int(rank),
        "max_gap": float(gap),
        "candidate_grid_max": int(max(grid)),
        "decision": None,
    }
    if rank == max(grid):
        out["decision"] = "REFUSE_EDGE_RANK"
        return out
    if gap < float(gap_ratio_min):
        out["decision"] = "REFUSE_WEAK_GAP"
        return out

    fit = sweep["fits"][rank]
    if fit.get("status") != "OK":
        out["decision"] = "REFUSE_METHOD_EXCEPTION"
        out["method_status"] = fit.get("status")
        return out

    vals = np.asarray(fit["vals"], complex)
    if np.any(vals.real >= 0.0):
        out["decision"] = "REFUSE_UNSTABLE_SELECTED_POLE"
        out["unstable_poles"] = int(np.sum(vals.real >= 0.0))
        return out

    pos = vals[np.where(vals.imag / (2 * np.pi) >= float(min_hz))[0]]
    stable_pos = pos[pos.real < 0.0]
    out["positive_complex_modes"] = int(len(pos))
    out["stable_positive_complex_modes"] = int(len(stable_pos))
    if len(stable_pos) == 0:
        out["decision"] = "REFUSE_NO_STABLE_COMPLEX_MODE"
        return out

    out["decision"] = "ADMIT_RANK_SIGNAL"
    return out


def evaluate_rank_signal(method, Y, dt, candidate_grid, block_rows, gap_ratio_min, min_hz):
    """Evaluate the frozen P0Q1 data-derived rank-signal candidate gate.

    Inputs are measurement and method settings only. This function does not
    accept truth, labels, phenotype, chi, diagnosis, or outcomes.
    """
    method = str(method)
    if method == "SSI_COV":
        sweep = sweep_ssi_cov(Y, dt, block_rows, candidate_grid)
    elif method == "SUBSPACE_DMD":
        sweep = sweep_subspace_dmd(Y, dt, candidate_grid)
    else:
        raise ValueError("unsupported method")
    out = _candidate_from_sweep(sweep, candidate_grid, gap_ratio_min, min_hz)
    out["method"] = method
    out["status"] = "P0Q1_DATA_DERIVED_CANDIDATE_GATE"
    return out
