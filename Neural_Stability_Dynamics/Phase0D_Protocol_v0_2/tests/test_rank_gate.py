import inspect
import numpy as np

from src.rank_gate import _candidate_from_sweep, evaluate_rank_signal


def _sweep(rank, gap, vals, grid=(1,2,3,4)):
    fits = {}
    for r in grid:
        fits[r] = {
            "status": "OK",
            "singular_gap_ratio": gap if r == rank else 1.1,
            "vals": np.asarray(vals if r == rank else [-1.0 + 1.0j], complex),
            "shapes": np.ones((2, len(vals if r == rank else [-1.0 + 1.0j])), complex),
            "unstable_fraction": 0.0,
        }
    return {"fits": fits}


def test_rank_gate_interface_has_no_truth_or_phenotype_inputs():
    names = {x.lower() for x in inspect.signature(evaluate_rank_signal).parameters}
    forbidden = ["truth", "label", "diagnosis", "phenotype", "outcome", "chi"]
    assert not any(token in name for name in names for token in forbidden)


def test_candidate_gate_refuses_weak_gap():
    out = _candidate_from_sweep(_sweep(2, 2.9, [-1 + 2j, -1 - 2j]), [1,2,3,4], 3.0, 0.25)
    assert out["decision"] == "REFUSE_WEAK_GAP"


def test_candidate_gate_refuses_edge_rank():
    out = _candidate_from_sweep(_sweep(4, 20.0, [-1 + 2j, -1 - 2j]), [1,2,3,4], 3.0, 0.25)
    assert out["decision"] == "REFUSE_EDGE_RANK"


def test_candidate_gate_refuses_unstable_pole():
    out = _candidate_from_sweep(_sweep(2, 10.0, [0.1 + 2j, 0.1 - 2j]), [1,2,3,4], 3.0, 0.25)
    assert out["decision"] == "REFUSE_UNSTABLE_SELECTED_POLE"


def test_candidate_gate_refuses_no_stable_complex_mode():
    out = _candidate_from_sweep(_sweep(2, 10.0, [-1.0, -2.0]), [1,2,3,4], 3.0, 0.25)
    assert out["decision"] == "REFUSE_NO_STABLE_COMPLEX_MODE"


def test_candidate_gate_admits_supported_stable_complex_signal():
    out = _candidate_from_sweep(_sweep(2, 10.0, [-1 + 2j, -1 - 2j]), [1,2,3,4], 3.0, 0.25)
    assert out["decision"] == "ADMIT_RANK_SIGNAL"
