from __future__ import annotations

"""Outcome-blind preflight machinery for a future G2 temporal analysis.

This module is deliberately representation-agnostic and is not authorized to
choose an empirical state dimension. It provides deterministic mechanics for a
pre-frozen control-only PCA basis and transition fits, plus refusal diagnostics.
No public cancer source is read by this module.
"""

from dataclasses import dataclass

import numpy as np

from src.chi_bio_candidate_math import spectral_radius
from src.chi_bio_g2_qualification import largest_singular_value


@dataclass(frozen=True)
class ControlPCABasis:
    mean: np.ndarray
    components: np.ndarray
    singular_values: np.ndarray
    state_dimension: int
    feature_dimension: int
    control_sample_count: int


@dataclass(frozen=True)
class TransitionFit:
    transition: np.ndarray
    input_matrix: np.ndarray | None
    intercept: np.ndarray | None
    design_rank: int
    design_columns: int
    n_transitions: int
    residual_frobenius: float
    relative_residual_frobenius: float
    condition_number: float
    status: str


@dataclass(frozen=True)
class TreatmentInteractionFit:
    control_transition: np.ndarray
    treatment_delta_transition: np.ndarray
    treated_transition: np.ndarray
    input_matrix: np.ndarray | None
    intercept: np.ndarray | None
    design_rank: int
    design_columns: int
    n_transitions: int
    residual_frobenius: float
    relative_residual_frobenius: float
    condition_number: float
    status: str


@dataclass(frozen=True)
class TransitionDiagnostics:
    spectral_radius: float
    largest_singular_value: float
    nonnormal_transient_warning: bool
    eigenvalue_realpart_gap: float


def _finite_2d(array: np.ndarray, name: str) -> np.ndarray:
    arr = np.asarray(array, dtype=float)
    if arr.ndim != 2 or arr.shape[0] == 0 or arr.shape[1] == 0:
        raise ValueError(f"{name} must be a nonempty 2D array")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must contain only finite values")
    return arr


def fit_control_pca(control_features: np.ndarray, *, state_dimension: int) -> ControlPCABasis:
    """Fit a PCA/SVD basis to control states only at a predeclared dimension."""

    x = _finite_2d(control_features, "control_features")
    d = int(state_dimension)
    if d <= 0:
        raise ValueError("state_dimension must be positive")
    centered = x - np.mean(x, axis=0, keepdims=True)
    _, s, vt = np.linalg.svd(centered, full_matrices=False)
    numerical_rank = int(np.linalg.matrix_rank(centered))
    if d > numerical_rank:
        raise ValueError(
            f"state_dimension {d} exceeds control-centered numerical rank {numerical_rank}"
        )
    return ControlPCABasis(
        mean=np.mean(x, axis=0),
        components=vt[:d].copy(),
        singular_values=s[:d].copy(),
        state_dimension=d,
        feature_dimension=x.shape[1],
        control_sample_count=x.shape[0],
    )


def project_with_frozen_basis(basis: ControlPCABasis, features: np.ndarray) -> np.ndarray:
    x = _finite_2d(features, "features")
    if x.shape[1] != basis.feature_dimension:
        raise ValueError("feature dimension does not match frozen PCA basis")
    return (x - basis.mean) @ basis.components.T


def stack_arm_transitions(
    state_sequences: list[np.ndarray] | tuple[np.ndarray, ...],
    *,
    arm_inputs: list[float] | tuple[float, ...] | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray | None]:
    """Stack consecutive transitions from independently ordered arm sequences.

    arm_inputs, when supplied, contributes one constant exogenous input value
    per arm. Sequences are never connected across arm boundaries.
    """

    if len(state_sequences) == 0:
        raise ValueError("at least one state sequence is required")
    if arm_inputs is not None and len(arm_inputs) != len(state_sequences):
        raise ValueError("arm_inputs must match number of state sequences")

    x0_blocks: list[np.ndarray] = []
    x1_blocks: list[np.ndarray] = []
    u_blocks: list[np.ndarray] = []
    state_dim = None
    for i, sequence in enumerate(state_sequences):
        seq = _finite_2d(sequence, f"state_sequence[{i}]")
        if seq.shape[0] < 2:
            raise ValueError("each state sequence needs at least two ordered states")
        if state_dim is None:
            state_dim = seq.shape[1]
        elif seq.shape[1] != state_dim:
            raise ValueError("all state sequences must share state dimension")
        x0_blocks.append(seq[:-1])
        x1_blocks.append(seq[1:])
        if arm_inputs is not None:
            u_blocks.append(np.full((seq.shape[0] - 1, 1), float(arm_inputs[i])))

    x0 = np.vstack(x0_blocks)
    x1 = np.vstack(x1_blocks)
    u = np.vstack(u_blocks) if arm_inputs is not None else None
    return x0, x1, u


def fit_shared_transition(
    x_now: np.ndarray,
    x_next: np.ndarray,
    *,
    exogenous_inputs: np.ndarray | None = None,
    include_intercept: bool = True,
    rank_tolerance: float | None = None,
) -> TransitionFit:
    """Fit x_next = T x_now + B u + c by least squares or refuse rank failure.

    Important: an additive treatment input changes forcing/equilibrium but leaves
    the fitted T shared across arms. It therefore cannot, by itself, establish a
    treatment-induced change in the transition operator's spectral radius.
    """

    x0 = _finite_2d(x_now, "x_now")
    x1 = _finite_2d(x_next, "x_next")
    if x0.shape != x1.shape:
        raise ValueError("x_now and x_next must have identical shape")

    pieces = [x0]
    q = 0
    u = None
    if exogenous_inputs is not None:
        u = _finite_2d(exogenous_inputs, "exogenous_inputs")
        if u.shape[0] != x0.shape[0]:
            raise ValueError("exogenous_inputs rows must match transitions")
        q = u.shape[1]
        pieces.append(u)
    if include_intercept:
        pieces.append(np.ones((x0.shape[0], 1)))

    design = np.hstack(pieces)
    rank = int(np.linalg.matrix_rank(design, tol=rank_tolerance))
    columns = design.shape[1]
    if rank < columns:
        d = x0.shape[1]
        return TransitionFit(
            transition=np.full((d, d), np.nan),
            input_matrix=np.full((d, q), np.nan) if q else None,
            intercept=np.full(d, np.nan) if include_intercept else None,
            design_rank=rank,
            design_columns=columns,
            n_transitions=x0.shape[0],
            residual_frobenius=float("nan"),
            relative_residual_frobenius=float("nan"),
            condition_number=float("inf"),
            status="REFUSE_RANK_DEFICIENT_DESIGN",
        )

    coef, *_ = np.linalg.lstsq(design, x1, rcond=None)
    fitted = design @ coef
    residual = float(np.linalg.norm(x1 - fitted, ord="fro"))
    denom = float(np.linalg.norm(x1, ord="fro"))
    rel = residual / denom if denom > 0 else residual
    cond = float(np.linalg.cond(design))

    d = x0.shape[1]
    t = coef[:d, :].T
    offset = d
    b = None
    if q:
        b = coef[offset : offset + q, :].T
        offset += q
    c = coef[offset, :].copy() if include_intercept else None

    return TransitionFit(
        transition=t,
        input_matrix=b,
        intercept=c,
        design_rank=rank,
        design_columns=columns,
        n_transitions=x0.shape[0],
        residual_frobenius=residual,
        relative_residual_frobenius=rel,
        condition_number=cond,
        status="FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN",
    )


def fit_treatment_interaction_transition(
    x_now: np.ndarray,
    x_next: np.ndarray,
    *,
    treatment_indicator: np.ndarray,
    include_additive_input: bool = True,
    include_intercept: bool = True,
    rank_tolerance: float | None = None,
) -> TreatmentInteractionFit:
    """Fit a treatment-dependent operator without selecting outcomes.

    Model:
        x_next = T0 x_now + u * DeltaT x_now + B u + c

    where u must be a single binary column. The implied operators are
    T_control=T0 and T_treated=T0+DeltaT. This is the minimal shared-design
    formulation that can test operator reorganization rather than only an
    additive shift in forcing.
    """

    x0 = _finite_2d(x_now, "x_now")
    x1 = _finite_2d(x_next, "x_next")
    if x0.shape != x1.shape:
        raise ValueError("x_now and x_next must have identical shape")
    u = _finite_2d(treatment_indicator, "treatment_indicator")
    if u.shape != (x0.shape[0], 1):
        raise ValueError("treatment_indicator must be one column with one row per transition")
    if not np.all(np.isin(u, [0.0, 1.0])):
        raise ValueError("treatment_indicator must be binary 0/1")

    interaction = x0 * u
    pieces = [x0, interaction]
    if include_additive_input:
        pieces.append(u)
    if include_intercept:
        pieces.append(np.ones((x0.shape[0], 1)))
    design = np.hstack(pieces)
    rank = int(np.linalg.matrix_rank(design, tol=rank_tolerance))
    columns = design.shape[1]
    d = x0.shape[1]

    if rank < columns:
        return TreatmentInteractionFit(
            control_transition=np.full((d, d), np.nan),
            treatment_delta_transition=np.full((d, d), np.nan),
            treated_transition=np.full((d, d), np.nan),
            input_matrix=np.full((d, 1), np.nan) if include_additive_input else None,
            intercept=np.full(d, np.nan) if include_intercept else None,
            design_rank=rank,
            design_columns=columns,
            n_transitions=x0.shape[0],
            residual_frobenius=float("nan"),
            relative_residual_frobenius=float("nan"),
            condition_number=float("inf"),
            status="REFUSE_RANK_DEFICIENT_DESIGN",
        )

    coef, *_ = np.linalg.lstsq(design, x1, rcond=None)
    fitted = design @ coef
    residual = float(np.linalg.norm(x1 - fitted, ord="fro"))
    denom = float(np.linalg.norm(x1, ord="fro"))
    rel = residual / denom if denom > 0 else residual
    cond = float(np.linalg.cond(design))

    t0 = coef[:d, :].T
    dt = coef[d : 2 * d, :].T
    offset = 2 * d
    b = None
    if include_additive_input:
        b = coef[offset : offset + 1, :].T
        offset += 1
    c = coef[offset, :].copy() if include_intercept else None

    return TreatmentInteractionFit(
        control_transition=t0,
        treatment_delta_transition=dt,
        treated_transition=t0 + dt,
        input_matrix=b,
        intercept=c,
        design_rank=rank,
        design_columns=columns,
        n_transitions=x0.shape[0],
        residual_frobenius=residual,
        relative_residual_frobenius=rel,
        condition_number=cond,
        status="FIT_IDENTIFIABLE_AT_DECLARED_LINEAR_DESIGN",
    )


def transition_diagnostics(transition: np.ndarray) -> TransitionDiagnostics:
    t = _finite_2d(transition, "transition")
    if t.shape[0] != t.shape[1]:
        raise ValueError("transition must be square")
    eigvals = np.linalg.eigvals(t)
    realparts = np.sort(np.real(eigvals))[::-1]
    gap = float(realparts[0] - realparts[1]) if len(realparts) > 1 else float("inf")
    rho = spectral_radius(t)
    sigma = largest_singular_value(t)
    return TransitionDiagnostics(
        spectral_radius=float(rho),
        largest_singular_value=float(sigma),
        nonnormal_transient_warning=bool(rho < 1.0 and sigma > 1.0),
        eigenvalue_realpart_gap=gap,
    )
