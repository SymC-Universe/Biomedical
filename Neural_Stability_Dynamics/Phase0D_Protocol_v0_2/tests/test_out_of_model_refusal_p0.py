from __future__ import annotations

import numpy as np

from scripts.run_p0d23_out_of_model_refusal import (
    _condition_specs,
    _disposition,
    _native_eigenvalues,
)


def test_all_native_generators_are_stable():
    for spec in _condition_specs():
        assert np.all(_native_eigenvalues(spec["modes_first"]).real < 0)
        assert np.all(_native_eigenvalues(spec["modes_second"]).real < 0)


def test_stationary_control_halves_are_identical():
    spec = next(x for x in _condition_specs() if x["name"] == "STATIONARY_CONTROL")
    a = np.sort_complex(_native_eigenvalues(spec["modes_first"]))
    b = np.sort_complex(_native_eigenvalues(spec["modes_second"]))
    assert np.allclose(a, b)


def test_structural_switch_halves_genuinely_differ():
    spec = next(x for x in _condition_specs() if x["name"] == "STRUCTURAL_SWITCH")
    a = np.sort_complex(_native_eigenvalues(spec["modes_first"]))
    b = np.sort_complex(_native_eigenvalues(spec["modes_second"]))
    assert not np.allclose(a, b)


def test_any_refusal_forces_refuse_current_model_disposition():
    decisions = {
        "scalar": "ADMIT_SCALAR_SPECTRUM",
        "modal": "REFUSE_MODAL_UNSTABLE",
        "system": "PARTIAL_SYSTEM_ORGANIZATION_GEOMETRY_UNRESOLVED",
    }
    assert _disposition(decisions) == "REFUSE_CURRENT_MODEL"


def test_all_admission_still_does_not_claim_recovery_prediction():
    decisions = {
        "scalar": "ADMIT_SCALAR_SPECTRUM",
        "modal": "ADMIT_MODAL_STRUCTURE",
        "system": "ADMIT_SYSTEM_ORGANIZATION",
    }
    assert _disposition(decisions) == "STRUCTURAL_OUTPUT_ONLY_NO_RECOVERY_PREDICTION"
