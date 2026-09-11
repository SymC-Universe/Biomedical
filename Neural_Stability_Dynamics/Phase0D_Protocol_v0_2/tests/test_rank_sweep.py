import inspect
import numpy as np

from src.rank_sweep import (
    adjacent_rank_stability,
    singular_gap_ratio,
    sweep_ssi_cov,
    sweep_subspace_dmd,
)


def test_rank_sweep_interfaces_have_no_truth_or_label_inputs():
    for fn in [sweep_ssi_cov, sweep_subspace_dmd, adjacent_rank_stability]:
        names = {p.lower() for p in inspect.signature(fn).parameters}
        assert not any(
            token in name
            for name in names
            for token in ["truth", "label", "diagnosis", "phenotype", "outcome", "chi"]
        )


def test_ssi_and_subspace_rank_sweeps_do_not_select_a_rank():
    rng = np.random.default_rng(55)
    Y = rng.normal(size=(1200, 4))
    ssi = sweep_ssi_cov(Y, dt=0.02, block_rows=12, candidate_orders=[1, 2, 3, 4])
    sub = sweep_subspace_dmd(Y, dt=0.02, candidate_ranks=[1, 2, 3, 4])
    assert ssi["selection"] is None
    assert sub["selection"] is None
    assert ssi["selection_status"] == "NO_SELECTION_P0_SWEEP_ONLY"
    assert sub["selection_status"] == "NO_SELECTION_P0_SWEEP_ONLY"
    assert sorted(ssi["fits"]) == [1, 2, 3, 4]
    assert sorted(sub["fits"]) == [1, 2, 3, 4]


def test_adjacent_rank_stability_is_assignment_only_not_adjudication():
    rng = np.random.default_rng(56)
    Y = rng.normal(size=(1400, 4))
    sweep = sweep_subspace_dmd(Y, dt=0.02, candidate_ranks=[1, 2, 3, 4])
    stability = adjacent_rank_stability(sweep, min_hz=0.0)
    assert len(stability) == 3
    for row in stability:
        assert row["status"] in {
            "P0_ASSIGNMENT_NOT_ADJUDICATED",
            "UNRESOLVED_METHOD_EXCEPTION",
        }
        assert "decision" not in row
        assert "admit" not in row


def test_singular_gap_ratio_reports_without_thresholding():
    s = np.array([10.0, 5.0, 1.0, 0.5])
    assert singular_gap_ratio(s, 1) == 2.0
    assert singular_gap_ratio(s, 2) == 5.0
    assert np.isnan(singular_gap_ratio(s, 4))
