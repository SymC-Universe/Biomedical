from __future__ import annotations

import numpy as np

from src.run_chi_bio_g1_restoration_r0_embedding_preflight import _principal_log_diagnostic


def test_principal_log_positive_diagonal_reconstructs_without_biological_promotion() -> None:
    t = np.diag([0.8, 0.6]).astype(float)
    out = _principal_log_diagnostic(t)
    assert out["status"] == "PRINCIPAL_BRANCH_CANDIDATE_COMPUTED"
    assert out["embedding_admitted"] is False
    assert out["matrix_log_uniqueness_established"] is False
    assert out["restoration_decomposition_performed"] is False
    assert out["normalized_g1_computed"] is False
    assert out["chi_bio_computed"] is False
    assert out["reconstruction_relative_frobenius_error"] < 1e-12
    assert out["principal_log_imag_frobenius"] < 1e-12


def test_principal_log_damped_rotation_reports_branch_without_selecting_restoration() -> None:
    radius = 0.85
    theta = 0.4
    t = radius * np.array(
        [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)],
        ],
        dtype=float,
    )
    out = _principal_log_diagnostic(t)
    assert out["status"] == "PRINCIPAL_BRANCH_CANDIDATE_COMPUTED"
    assert out["embedding_admitted"] is False
    assert out["matrix_log_uniqueness_established"] is False
    assert out["restoration_decomposition_performed"] is False
    assert out["reconstruction_relative_frobenius_error"] < 1e-12
    assert len(out["eigenvalue_arguments_radians"]) == 2


def test_singular_transition_operator_refuses_log_candidate() -> None:
    t = np.array([[0.8, 0.0], [0.0, 0.0]], dtype=float)
    out = _principal_log_diagnostic(t)
    assert out["status"] == "REFUSE_SINGULAR_TRANSITION_OPERATOR"
