from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src.run_chi_bio_chronic_g2_empirical import (
    _fit_basis,
    _make_transitions,
    _overall_disposition,
    _validate_freeze,
)


def test_chronic_freeze_contract_is_machine_valid() -> None:
    freeze = json.loads(
        Path("config/gri_Chi_bio_chronic_g2_r1_A3_empirical_freeze_20260913_v1.json").read_text(
            encoding="utf-8"
        )
    )
    _validate_freeze(freeze)
    assert freeze["source_binding"]["declared_transitions"] == 20
    assert freeze["chronic_ctx_columns_read_by_design_input_probe"] is False
    assert freeze["chi_bio_status"] == "NOT_ADMITTED"


def test_chronic_transition_geometry_is_exactly_ten_plus_ten_without_shared_day0() -> None:
    pbs = np.arange(22, dtype=float).reshape(11, 2)
    ctx = 100.0 + np.arange(22, dtype=float).reshape(11, 2)
    x0, x1, u, arm = _make_transitions(pbs, ctx)

    assert x0.shape == (20, 2)
    assert x1.shape == (20, 2)
    assert np.array_equal(x0[:10], pbs[:-1])
    assert np.array_equal(x1[:10], pbs[1:])
    assert np.array_equal(x0[10:], ctx[:-1])
    assert np.array_equal(x1[10:], ctx[1:])
    assert np.array_equal(u[:, 0], np.array([0.0] * 10 + [1.0] * 10))
    assert np.array_equal(arm, np.array([0] * 10 + [1] * 10))
    assert not np.array_equal(x0[0], x0[10])


def test_basis_sign_is_canonicalized_and_rank_three_is_available_when_present() -> None:
    t = np.linspace(-2.0, 2.0, 11)
    pbs = np.column_stack(
        [
            t,
            t**2 - np.mean(t**2),
            t**3,
            np.sin(t),
            np.cos(t),
        ]
    )
    basis = _fit_basis(pbs, 3)
    assert basis["numerical_rank"] >= 3
    assert basis["components"].shape == (3, 5)
    for component in basis["components"]:
        pivot = int(np.argmax(np.abs(component)))
        assert component[pivot] >= 0.0


def test_cross_rank_material_disagreement_refuses_transfer() -> None:
    r2 = {
        "d1_adequacy": "PASS",
        "d1_mathematical_unit_circle_side": "BELOW",
        "d1_nonnormal_warning": "ABSENT",
        "d2_reorganization_support": "NOT_SUPPORTED",
    }
    r3 = dict(r2)
    r3["d1_mathematical_unit_circle_side"] = "INDETERMINATE"
    assert _overall_disposition({"2": r2, "3": r3}) == "REPRESENTATION_DEPENDENT_NO_TRANSFER"


def test_d2_support_requires_both_ranks_before_overall_reorganization_label() -> None:
    material = {
        "d1_adequacy": "PASS",
        "d1_mathematical_unit_circle_side": "BELOW",
        "d1_nonnormal_warning": "ABSENT",
        "d2_reorganization_support": "SUPPORTED",
        "d2_control_mathematical_unit_circle_side": "BELOW",
        "d2_treated_mathematical_unit_circle_side": "BELOW",
        "d2_delta_rho_sign": "POSITIVE",
        "d2_control_nonnormal_warning": "ABSENT",
        "d2_treated_nonnormal_warning": "ABSENT",
    }
    assert _overall_disposition({"2": material, "3": dict(material)}) == "REORGANIZATION_SUPPORTED"
