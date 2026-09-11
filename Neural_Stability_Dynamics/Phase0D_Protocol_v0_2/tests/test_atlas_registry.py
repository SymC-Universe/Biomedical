import pytest

from src.atlas_registry import validate_atlas_entry


def _base_entry():
    return {
        "source_id": "src-001",
        "coordinate_family": "SPECTRAL_POLE",
        "coordinate_name": "frequency_hz",
        "native_or_derived": "DERIVED",
        "value_or_object": 8.0,
        "units": "Hz",
        "estimator_method": "source-native",
        "evidence_tier": "DERIVED_LICENSED",
        "research_role": "NOMINAL_FUNCTION",
        "function_limit_state": "WORKS_HERE",
        "independence_pathways": {
            "data": "UNRESOLVED",
            "cohort_system": "UNRESOLVED",
            "outcome_label": "UNRESOLVED",
            "parameter_tuning": "UNRESOLVED",
            "method_estimator": "UNRESOLVED",
            "atlas": "UNRESOLVED",
            "source_literature": "UNRESOLVED",
            "temporal_decisive_evidence": "UNRESOLVED",
        },
        "scope_ceiling": "SUPPORTED_IN_TESTED_REGIME",
        "derivation_record_if_any": "omega/(2*pi)",
    }


def test_valid_derived_coordinate_is_accepted():
    assert validate_atlas_entry(_base_entry()) is True


def test_derived_coordinate_without_derivation_is_rejected():
    entry = _base_entry()
    entry["derivation_record_if_any"] = None
    with pytest.raises(ValueError):
        validate_atlas_entry(entry)


def test_chi_is_withheld_without_explicit_license():
    entry = _base_entry()
    entry["coordinate_name"] = "chi"
    with pytest.raises(ValueError):
        validate_atlas_entry(entry)


def test_chi_license_requires_derivation_and_native_inputs():
    entry = _base_entry()
    entry["coordinate_name"] = "chi"
    entry["chi_admission"] = {
        "status": "LICENSED",
        "derivation": "explicit second-order derivation",
        "native_inputs_retained": True,
    }
    assert validate_atlas_entry(entry) is True


def test_independence_cannot_be_collapsed_to_one_grade():
    entry = _base_entry()
    entry["independence_pathways"] = {"overall": "INDEPENDENT"}
    with pytest.raises(ValueError):
        validate_atlas_entry(entry)
