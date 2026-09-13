import numpy as np
import pytest

from src.chi_bio_g2_empirical_preflight import (
    fit_control_pca,
    fit_shared_transition,
    project_with_frozen_basis,
    stack_arm_transitions,
)


def _synthetic_six_state_control_and_treated(seed: int = 20260913):
    rng = np.random.default_rng(seed)
    # Six ordered states, matching the short-term source architecture.  Four
    # measured features keep both r=2 and r=3 mechanically possible without
    # pretending this synthetic geometry selects a biological rank.
    control = np.cumsum(rng.normal(scale=0.2, size=(6, 4)), axis=0)
    treated = control.copy()
    treated[1:] += np.linspace(0.0, 0.35, 5)[:, None] * np.array([1.0, -0.4, 0.6, 0.2])
    return control, treated


@pytest.mark.parametrize("rank", [2, 3])
def test_both_prospective_rank_options_are_mechanically_executable_without_selection(rank):
    control, treated = _synthetic_six_state_control_and_treated()
    basis = fit_control_pca(control, state_dimension=rank)
    z_control = project_with_frozen_basis(basis, control)
    z_treated = project_with_frozen_basis(basis, treated)

    x0, x1, u = stack_arm_transitions(
        (z_control, z_treated), arm_inputs=(0.0, 1.0)
    )
    fit = fit_shared_transition(
        x0,
        x1,
        exogenous_inputs=u,
        include_intercept=True,
    )

    assert fit.n_transitions == 10
    assert fit.design_columns == rank + 2
    assert fit.design_rank == fit.design_columns
    assert fit.status == "FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN"
    assert np.all(np.isfinite(fit.transition))


def test_predecision_pilot_does_not_choose_between_r2_and_r3():
    control, treated = _synthetic_six_state_control_and_treated()
    statuses = {}
    for rank in (2, 3):
        basis = fit_control_pca(control, state_dimension=rank)
        zc = project_with_frozen_basis(basis, control)
        zt = project_with_frozen_basis(basis, treated)
        x0, x1, u = stack_arm_transitions((zc, zt), arm_inputs=(0.0, 1.0))
        statuses[rank] = fit_shared_transition(
            x0, x1, exogenous_inputs=u, include_intercept=True
        ).status

    # The only purpose of this fixture is to establish mechanical feasibility
    # of both predeclared options. No synthetic or real spectral outcome is
    # compared to promote one rank over the other.
    assert statuses == {
        2: "FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN",
        3: "FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN",
    }
