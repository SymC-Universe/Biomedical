from __future__ import annotations

import numpy as np
import pytest

from scripts.run_p0d20_recovery_transformation_geometry import (
    _templates,
    recovery_summary,
    run_surface,
)
from src.chi_conglomerate import second_order_generator
from src.coupled_conglomeration import assemble_coupled_generator


def test_feedback_templates_have_matched_unit_edge_norms():
    for out_template, return_template in _templates().values():
        assert np.isclose(np.linalg.norm(out_template, 2), 1.0, rtol=0.0, atol=1e-12)
        assert np.isclose(np.linalg.norm(return_template, 2), 1.0, rtol=0.0, atol=1e-12)


def test_uncoupled_rows_are_identical_across_variant_labels():
    rows = [r for r in run_surface() if r["coupling_rate"] == 0.0]
    assert len(rows) == 5
    ref = rows[0]
    for row in rows[1:]:
        assert np.isclose(row["spectral_abscissa_per_s"], ref["spectral_abscissa_per_s"], atol=1e-12)
        assert np.isclose(
            row["worst_case_dimensionless_transient_gain"],
            ref["worst_case_dimensionless_transient_gain"],
            atol=1e-12,
        )


def test_position_position_g12_matches_prior_closed_loop_regression():
    rows = run_surface()
    row = next(
        r for r in rows
        if r["variant"] == "POSITION_OUT_POSITION_RETURN" and r["coupling_rate"] == 12.0
    )
    assert np.isclose(row["spectral_abscissa_per_s"], -17.703614271133652, rtol=1e-11, atol=1e-11)
    assert np.isclose(row["dominant_asymptotic_time_scale_s"], 0.05648564099312388, rtol=1e-11, atol=1e-11)


def test_recovery_summary_rejects_known_bad_nonfinite_generator():
    bad = np.eye(2)
    bad[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        recovery_summary(bad, np.array([0.0, 0.1]))


def test_recovery_summary_calls_valid_generator_and_reports_stability():
    A0 = second_order_generator(0.55, 2.0 * np.pi * 3.0)
    A1 = second_order_generator(0.85, 2.0 * np.pi * 5.0)
    full = assemble_coupled_generator([A0, A1], {})["generator"]
    out = recovery_summary(full, np.array([0.0, 0.01, 0.02]))
    assert out["asymptotically_stable"] is True
    assert out["spectral_abscissa_per_s"] < 0.0
    assert out["worst_case_dimensionless_transient_gain"] >= 1.0
