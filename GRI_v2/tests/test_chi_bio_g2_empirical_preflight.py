import numpy as np
import pytest

from src.chi_bio_g2_empirical_preflight import (
    fit_control_pca,
    fit_shared_transition,
    project_with_frozen_basis,
    stack_arm_transitions,
    transition_diagnostics,
)


def test_control_only_basis_projects_treated_states_without_refit():
    control = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [2.0, 1.0, 0.0],
            [3.0, 1.0, 1.0],
        ]
    )
    treated = control + np.array([0.0, 0.0, 2.0])
    basis = fit_control_pca(control, state_dimension=2)
    before = basis.components.copy()
    projected = project_with_frozen_basis(basis, treated)
    assert projected.shape == (4, 2)
    assert np.array_equal(before, basis.components)


def test_control_basis_refuses_dimension_above_centered_rank():
    control = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]])
    with pytest.raises(ValueError, match="exceeds"):
        fit_control_pca(control, state_dimension=2)


def test_stack_arm_transitions_never_connects_arm_boundaries():
    a = np.array([[0.0], [1.0], [2.0]])
    b = np.array([[10.0], [11.0], [12.0]])
    x0, x1, u = stack_arm_transitions((a, b), arm_inputs=(0.0, 1.0))
    assert x0[:, 0].tolist() == [0.0, 1.0, 10.0, 11.0]
    assert x1[:, 0].tolist() == [1.0, 2.0, 11.0, 12.0]
    assert u[:, 0].tolist() == [0.0, 0.0, 1.0, 1.0]


def test_shared_transition_recovers_known_linear_system():
    t_true = np.array([[0.8, 0.1], [0.0, 0.9]])
    b_true = np.array([[0.2], [-0.1]])
    c_true = np.array([0.05, -0.02])

    rng = np.random.default_rng(7)
    x0 = rng.normal(size=(20, 2))
    u = np.array([[0.0], [1.0]] * 10)
    x1 = x0 @ t_true.T + u @ b_true.T + c_true

    fit = fit_shared_transition(x0, x1, exogenous_inputs=u, include_intercept=True)
    assert fit.status == "FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN"
    assert fit.transition == pytest.approx(t_true, abs=1e-12)
    assert fit.input_matrix == pytest.approx(b_true, abs=1e-12)
    assert fit.intercept == pytest.approx(c_true, abs=1e-12)
    assert fit.relative_residual_frobenius < 1e-12


def test_shared_transition_refuses_rank_deficient_design():
    x0 = np.ones((4, 2))
    x1 = np.ones((4, 2))
    u = np.ones((4, 1))
    fit = fit_shared_transition(x0, x1, exogenous_inputs=u, include_intercept=True)
    assert fit.status == "REFUSE_RANK_DEFICIENT_DESIGN"
    assert fit.design_rank < fit.design_columns
    assert np.isnan(fit.transition).all()


def test_transition_diagnostics_preserve_nonnormal_warning():
    t = np.array([[0.8, 4.0], [0.0, 0.8]])
    diag = transition_diagnostics(t)
    assert diag.spectral_radius == pytest.approx(0.8)
    assert diag.largest_singular_value > 1.0
    assert diag.nonnormal_transient_warning is True


def test_transition_fit_rejects_input_row_mismatch():
    x0 = np.eye(2)
    x1 = np.eye(2)
    with pytest.raises(ValueError, match="rows"):
        fit_shared_transition(x0, x1, exogenous_inputs=np.ones((3, 1)))
