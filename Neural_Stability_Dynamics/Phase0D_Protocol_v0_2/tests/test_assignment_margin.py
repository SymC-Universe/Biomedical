import numpy as np

from src.mode_tracking import track_modes


def test_global_assignment_margin_is_nonnegative_for_unique_assignment():
    va = np.array([-0.5 + 2.0j, -0.8 + 5.0j])
    vb = np.array([-0.51 + 2.01j, -0.79 + 5.01j])
    sa = np.eye(2, dtype=complex)
    sb = np.eye(2, dtype=complex)
    out = track_modes(va, sa, vb, sb, min_hz=0.0)
    assert len(out["candidate_pairs"]) == 2
    assert all(p["assignment_margin"] >= 0.0 for p in out["candidate_pairs"])
    assert all(p["assignment_margin"] > 0.0 for p in out["candidate_pairs"])


def test_global_assignment_margin_is_zero_for_exact_global_tie():
    va = np.array([-1.0 + 2.0j])
    vb = np.array([-1.0 + 2.0j, -1.0 + 2.0j])
    sa = np.array([[1.0], [0.0]], dtype=complex)
    sb = np.array([[1.0, 1.0], [0.0, 0.0]], dtype=complex)
    out = track_modes(va, sa, vb, sb, min_hz=0.0)
    assert out["candidate_pairs"][0]["assignment_margin"] == 0.0
