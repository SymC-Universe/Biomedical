import numpy as np

from src.chi_bio_g2_stability_diagnostics import leave_one_transition_out_interaction


def _fixture(d: int = 2):
    if d == 2:
        t0 = np.array([[0.78, 0.05], [0.0, 0.70]])
        tt = np.array([[1.05, 0.04], [0.0, 0.85]])
    else:
        t0 = np.array([[0.78, 0.05, 0.01], [0.0, 0.70, 0.03], [0.0, 0.0, 0.62]])
        tt = np.array([[1.05, 0.04, 0.01], [0.0, 0.85, 0.03], [0.0, 0.0, 0.70]])
    b = np.linspace(0.03, -0.02, d)
    c = np.linspace(0.02, -0.01, d)
    x_init = np.linspace(0.7, 1.3, d)

    def arm(t, treatment):
        xs = [x_init]
        for _ in range(5):
            xs.append(t @ xs[-1] + treatment * b + c)
        return np.vstack(xs)

    control = arm(t0, 0.0)
    treated = arm(tt, 1.0)
    x0 = np.vstack([control[:-1], treated[:-1]])
    x1 = np.vstack([control[1:], treated[1:]])
    u = np.vstack([np.zeros((5, 1)), np.ones((5, 1))])
    return x0, x1, u


def test_leave_one_transition_diagnostics_preserve_known_side_when_refits_identifiable():
    x0, x1, u = _fixture(2)
    summary = leave_one_transition_out_interaction(x0, x1, u)
    assert len(summary.records) == 10
    # This diagnostic is deliberately descriptive. When every reduced fit is
    # identifiable, the noiseless known-truth fixture must retain its sides.
    if summary.all_refits_identifiable:
        assert summary.control_unit_circle_side_invariant is True
        assert summary.treated_unit_circle_side_invariant is True
        assert summary.treatment_rho_delta_sign_invariant is True
        assert summary.control_rho_max < 1.0
        assert summary.treated_rho_min > 1.0


def test_r3_leave_one_out_is_allowed_to_expose_rank_fragility_instead_of_hiding_it():
    x0, x1, u = _fixture(3)
    summary = leave_one_transition_out_interaction(x0, x1, u)
    assert len(summary.records) == 10
    assert isinstance(summary.all_refits_identifiable, bool)
    # No assertion that r=3 must pass: a rank-deficient LOTO refit is evidence
    # of tiny-sample fragility and must remain visible to the later freeze.


def test_diagnostics_do_not_claim_bootstrap_uncertainty():
    x0, x1, u = _fixture(2)
    summary = leave_one_transition_out_interaction(x0, x1, u)
    assert not hasattr(summary, "p_value")
    assert not hasattr(summary, "confidence_interval")
