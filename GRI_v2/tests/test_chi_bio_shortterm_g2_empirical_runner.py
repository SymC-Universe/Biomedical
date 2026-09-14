import numpy as np

from src.run_chi_bio_shortterm_g2_empirical import (
    COND_CEILING,
    _fit,
    _make_transitions,
    _unit_side,
)


def test_shared_day0_transition_geometry_is_exactly_ten():
    pbs = np.arange(12, dtype=float).reshape(6, 2)
    ctx = (100.0 + np.arange(10, dtype=float)).reshape(5, 2)
    x0, x1, u, arm = _make_transitions(pbs, ctx)
    assert x0.shape == (10, 2)
    assert x1.shape == (10, 2)
    assert u[:, 0].tolist() == [0.0] * 5 + [1.0] * 5
    assert arm.tolist() == [0] * 5 + [1] * 5
    assert np.array_equal(x0[5], pbs[0])
    assert np.array_equal(x1[5], ctx[0])


def test_d1_fit_accepts_a_full_rank_well_conditioned_synthetic_design():
    x0 = np.array([
        [-2.0, 0.5],
        [-1.0, 1.2],
        [0.0, -0.7],
        [1.0, 0.3],
        [2.0, -1.1],
        [-1.5, -0.2],
        [-0.5, 0.9],
        [0.5, -1.4],
        [1.5, 1.1],
        [2.5, 0.1],
    ])
    u = np.vstack([np.zeros((5, 1)), np.ones((5, 1))])
    t = np.array([[0.7, 0.1], [-0.05, 0.8]])
    b = np.array([0.2, -0.1])
    c = np.array([0.03, 0.02])
    x1 = x0 @ t.T + u * b.reshape(1, -1) + c
    fit = _fit(x0, x1, u, "D1")
    assert fit["status"] == "PASS"
    assert fit["design_rank"] == fit["design_columns"] == 4
    assert fit["scaled_condition_number"] < COND_CEILING
    assert np.allclose(fit["T"], t)


def test_unit_side_requires_consistent_envelope():
    assert _unit_side([0.7, 0.8, 0.9], True) == "BELOW"
    assert _unit_side([1.1, 1.2], True) == "ABOVE"
    assert _unit_side([0.9, 1.1], True) == "INDETERMINATE"
    assert _unit_side([0.9], False) == "INDETERMINATE"
