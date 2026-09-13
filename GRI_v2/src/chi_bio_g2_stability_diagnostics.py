from __future__ import annotations

"""Deterministic small-sample stability diagnostics for prospective G2 models.

These diagnostics quantify sensitivity to individual transition rows. They are
not biological bootstrap uncertainty, do not assume iid time points, and do not
supply a p-value or an empirical refusal threshold.
"""

from dataclasses import dataclass

import numpy as np

from src.chi_bio_g2_empirical_preflight import (
    fit_treatment_interaction_transition,
    transition_diagnostics,
)


@dataclass(frozen=True)
class LeaveOneTransitionRecord:
    omitted_index: int
    status: str
    design_rank: int
    design_columns: int
    condition_number: float
    control_rho: float | None
    treated_rho: float | None
    control_sigma_max: float | None
    treated_sigma_max: float | None
    control_nonnormal_warning: bool | None
    treated_nonnormal_warning: bool | None


@dataclass(frozen=True)
class LeaveOneTransitionSummary:
    records: tuple[LeaveOneTransitionRecord, ...]
    all_refits_identifiable: bool
    control_rho_min: float | None
    control_rho_max: float | None
    treated_rho_min: float | None
    treated_rho_max: float | None
    control_unit_circle_side_invariant: bool | None
    treated_unit_circle_side_invariant: bool | None
    treatment_rho_delta_sign_invariant: bool | None


def _side(value: float) -> int:
    return int(np.sign(float(value) - 1.0))


def leave_one_transition_out_interaction(
    x_now: np.ndarray,
    x_next: np.ndarray,
    treatment_indicator: np.ndarray,
) -> LeaveOneTransitionSummary:
    x0 = np.asarray(x_now, dtype=float)
    x1 = np.asarray(x_next, dtype=float)
    u = np.asarray(treatment_indicator, dtype=float)
    if x0.ndim != 2 or x1.shape != x0.shape:
        raise ValueError("x_now and x_next must be matching 2D arrays")
    if u.shape != (x0.shape[0], 1):
        raise ValueError("treatment_indicator must have one row per transition")
    if x0.shape[0] < 3:
        raise ValueError("at least three transitions are required")

    rows: list[LeaveOneTransitionRecord] = []
    for omit in range(x0.shape[0]):
        keep = np.ones(x0.shape[0], dtype=bool)
        keep[omit] = False
        fit = fit_treatment_interaction_transition(
            x0[keep], x1[keep], treatment_indicator=u[keep]
        )
        if fit.status != "FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN":
            rows.append(
                LeaveOneTransitionRecord(
                    omitted_index=omit,
                    status=fit.status,
                    design_rank=fit.design_rank,
                    design_columns=fit.design_columns,
                    condition_number=float(fit.condition_number),
                    control_rho=None,
                    treated_rho=None,
                    control_sigma_max=None,
                    treated_sigma_max=None,
                    control_nonnormal_warning=None,
                    treated_nonnormal_warning=None,
                )
            )
            continue
        cd = transition_diagnostics(fit.control_transition)
        td = transition_diagnostics(fit.treated_transition)
        rows.append(
            LeaveOneTransitionRecord(
                omitted_index=omit,
                status=fit.status,
                design_rank=fit.design_rank,
                design_columns=fit.design_columns,
                condition_number=float(fit.condition_number),
                control_rho=cd.spectral_radius,
                treated_rho=td.spectral_radius,
                control_sigma_max=cd.largest_singular_value,
                treated_sigma_max=td.largest_singular_value,
                control_nonnormal_warning=cd.nonnormal_transient_warning,
                treated_nonnormal_warning=td.nonnormal_transient_warning,
            )
        )

    valid = [r for r in rows if r.control_rho is not None and r.treated_rho is not None]
    all_ok = len(valid) == len(rows)
    if not valid:
        return LeaveOneTransitionSummary(
            records=tuple(rows),
            all_refits_identifiable=False,
            control_rho_min=None,
            control_rho_max=None,
            treated_rho_min=None,
            treated_rho_max=None,
            control_unit_circle_side_invariant=None,
            treated_unit_circle_side_invariant=None,
            treatment_rho_delta_sign_invariant=None,
        )

    cr = [float(r.control_rho) for r in valid]
    tr = [float(r.treated_rho) for r in valid]
    c_sides = {_side(v) for v in cr}
    t_sides = {_side(v) for v in tr}
    delta_signs = {int(np.sign(t - c)) for c, t in zip(cr, tr)}
    return LeaveOneTransitionSummary(
        records=tuple(rows),
        all_refits_identifiable=all_ok,
        control_rho_min=min(cr),
        control_rho_max=max(cr),
        treated_rho_min=min(tr),
        treated_rho_max=max(tr),
        control_unit_circle_side_invariant=len(c_sides) == 1,
        treated_unit_circle_side_invariant=len(t_sides) == 1,
        treatment_rho_delta_sign_invariant=len(delta_signs) == 1,
    )
