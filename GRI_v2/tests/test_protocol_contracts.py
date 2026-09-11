from __future__ import annotations

import copy

import pytest

from src.protocol_contracts import ProtocolContractError, validate_v071a_output


def _valid_record():
    return {
        "research_mode": "P0_Q",
        "measurement_status": {"status": "VALID"},
        "system_model": {"version": "WORKING_NOT_FROZEN"},
        "engine": {"version": "WORKING_NOT_FROZEN"},
        "atlas": {
            "version": None,
            "independence_grade": "NOT_APPLICABLE",
            "used_as_independent_engine_validation": False,
        },
        "scalar_output": {"biological_chi": None},
        "modal_output": {},
        "conglomerate_output": {},
        "cross_component_output": {},
        "function_map_output": {
            "scope_id": "test-global-geometry",
            "component_or_claim": "global_cross_layer_geometry",
            "summary_state": "WORKS_HERE",
            "research_role": "NOMINAL_FUNCTION",
        },
        "limit_map_output": {
            "scope_id": "test-semantic-specificity",
            "component_or_claim": "hallmark_semantic_specificity",
            "summary_state": "NOT_KNOWN_HERE",
            "research_role": "NOMINAL_FUNCTION",
        },
        "reduction_adequacy": {},
        "classification": {
            "biological_chi_status": "NOT_ADMITTED",
            "rare_natural_testbed_status": "NOT_ADMITTED",
        },
        "refusal": {"state": None},
        "prediction": {
            "prediction_class": None,
            "outcome_namespace": None,
            "outcome": None,
            "mfr14_complete": False,
            "freeze_id": None,
            "decisive_evidence_unopened_at_freeze": None,
        },
        "independence": {
            "data_independence": "PARTIALLY_INDEPENDENT",
            "cohort_or_system_independence": "NON_INDEPENDENT",
            "outcome_independence": "PARTIALLY_INDEPENDENT",
            "parameter_or_tuning_independence": "PARTIALLY_INDEPENDENT",
            "method_independence": "PARTIALLY_INDEPENDENT",
            "atlas_independence": "NOT_APPLICABLE",
            "source_or_literature_independence": "NON_INDEPENDENT",
            "temporal_independence": "NOT_APPLICABLE",
        },
        "uncertainty": {},
        "epistemic_status": "P0_Q_QUALIFICATION",
        "claim_ceiling": "INTERNAL_METHOD_QUALIFICATION",
        "provenance": {},
    }


def _admitted_rare_record(mode="P0_D"):
    record = _valid_record()
    record["research_mode"] = mode
    record["classification"] = {
        "biological_chi_status": "NOT_ADMITTED",
        "rare_natural_testbed_status": "ADMITTED",
        "rare_natural_testbed": {
            "domain_native_rarity_evidence": ["independent prevalence evidence"],
            "authenticity_and_confounding_gate_passed": True,
            "selection_basis": "DOMAIN_NATIVE_RARITY_PLUS_POST_RESULT_STRESS",
            "selection_independent_of_engine_result": mode != "P1",
            "base_rate_context_status": "KNOWN_AND_RECORDED",
            "representative_status": "NONREPRESENTATIVE_LIMIT_PROBE",
        },
    }
    if mode == "P1":
        record["classification"]["rare_natural_testbed"][
            "selection_independent_of_engine_result"
        ] = True
        record["prediction"].update(
            {
                "prediction_class": "S",
                "outcome_namespace": "EMPIRICAL",
                "mfr14_complete": True,
                "freeze_id": "example-freeze",
                "decisive_evidence_unopened_at_freeze": True,
            }
        )
    return record


def test_valid_p0q_record_passes_contract():
    validate_v071a_output(_valid_record())


def test_valid_rare_p0d_record_passes_contract():
    validate_v071a_output(_admitted_rare_record())


def test_missing_required_group_is_known_bad_and_fails():
    record = _valid_record()
    del record["limit_map_output"]
    with pytest.raises(ProtocolContractError, match="missing required top-level"):
        validate_v071a_output(record)


def test_unscoped_function_state_is_known_bad_and_fails():
    record = _valid_record()
    del record["function_map_output"]["scope_id"]
    with pytest.raises(ProtocolContractError, match="function_map_output missing required scope"):
        validate_v071a_output(record)


def test_unscoped_limit_state_is_known_bad_and_fails():
    record = _valid_record()
    record["limit_map_output"]["component_or_claim"] = ""
    with pytest.raises(ProtocolContractError, match="limit_map_output missing required scope"):
        validate_v071a_output(record)


def test_biological_chi_population_is_known_bad_and_fails():
    record = _valid_record()
    record["scalar_output"]["biological_chi"] = 1.0
    with pytest.raises(ProtocolContractError, match="biological_chi must be null"):
        validate_v071a_output(record)


def test_silent_biological_chi_admission_is_known_bad_and_fails():
    record = _valid_record()
    record["classification"]["biological_chi_status"] = "ADMITTED"
    with pytest.raises(ProtocolContractError, match="biological chi is not admitted"):
        validate_v071a_output(record)


def test_engine_selected_rare_case_is_known_bad_and_fails():
    record = _admitted_rare_record()
    record["classification"]["rare_natural_testbed"]["selection_basis"] = "ENGINE_OUTPUT_ONLY"
    with pytest.raises(ProtocolContractError, match="cannot be selected from Engine"):
        validate_v071a_output(record)


def test_rare_case_without_base_rate_disposition_is_known_bad_and_fails():
    record = _admitted_rare_record()
    del record["classification"]["rare_natural_testbed"]["base_rate_context_status"]
    with pytest.raises(ProtocolContractError, match="base-rate-context disposition"):
        validate_v071a_output(record)


def test_rare_case_cannot_be_called_representative_without_separate_evidence():
    record = _admitted_rare_record()
    record["classification"]["rare_natural_testbed"][
        "representative_status"
    ] = "REPRESENTATIVE_BY_SEPARATE_EVIDENCE"
    with pytest.raises(ProtocolContractError, match="requires separate evidence"):
        validate_v071a_output(record)


def test_bare_representative_label_is_known_bad_and_fails():
    record = _admitted_rare_record()
    record["classification"]["rare_natural_testbed"]["representative_status"] = "REPRESENTATIVE"
    with pytest.raises(ProtocolContractError, match="preserve nonrepresentative"):
        validate_v071a_output(record)


def test_p1_rare_case_requires_engine_independent_selection():
    record = _admitted_rare_record(mode="P1")
    record["classification"]["rare_natural_testbed"][
        "selection_independent_of_engine_result"
    ] = False
    with pytest.raises(ProtocolContractError, match="must be independent of Engine result"):
        validate_v071a_output(record)


def test_nonindependent_atlas_cannot_claim_independent_engine_validation():
    record = _valid_record()
    record["atlas"] = {
        "version": "development-tcga",
        "independence_grade": "NON_INDEPENDENT_FOR_ENGINE_VALIDATION",
        "used_as_independent_engine_validation": True,
    }
    with pytest.raises(ProtocolContractError, match="cannot validate the Engine independently"):
        validate_v071a_output(record)


def test_missing_pathway_independence_dimension_is_known_bad_and_fails():
    record = _valid_record()
    del record["independence"]["temporal_independence"]
    with pytest.raises(ProtocolContractError, match="missing pathway-specific independence"):
        validate_v071a_output(record)


def test_p1_without_complete_mfr14_is_known_bad_and_fails():
    record = _valid_record()
    record["research_mode"] = "P1"
    record["prediction"].update(
        {
            "prediction_class": "S",
            "outcome_namespace": "EMPIRICAL",
            "mfr14_complete": False,
            "freeze_id": None,
            "decisive_evidence_unopened_at_freeze": None,
        }
    )
    with pytest.raises(ProtocolContractError, match="P1 requires complete MFR-14"):
        validate_v071a_output(record)


def test_p1_without_freeze_id_is_known_bad_and_fails():
    record = _valid_record()
    record["research_mode"] = "P1"
    record["prediction"].update(
        {
            "prediction_class": "S",
            "outcome_namespace": "EMPIRICAL",
            "mfr14_complete": True,
            "freeze_id": "",
            "decisive_evidence_unopened_at_freeze": True,
        }
    )
    with pytest.raises(ProtocolContractError, match="verifiable freeze_id"):
        validate_v071a_output(record)


def test_method_prediction_cannot_use_empirical_outcome_namespace():
    record = _valid_record()
    record["prediction"].update(
        {
            "prediction_class": "M",
            "outcome_namespace": "EMPIRICAL",
            "outcome": "EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST",
        }
    )
    with pytest.raises(ProtocolContractError, match="method-validity prediction"):
        validate_v071a_output(record)


def test_p0q_cannot_masquerade_as_confirmatory_empirical_survival():
    record = _valid_record()
    record["prediction"].update(
        {
            "prediction_class": "S",
            "outcome_namespace": "EMPIRICAL",
            "outcome": "EMPIRICAL_CLAIM_SURVIVES_FROZEN_TEST",
        }
    )
    with pytest.raises(ProtocolContractError, match="P0-D/P0-Q output cannot carry"):
        validate_v071a_output(record)


def test_p0d_cannot_masquerade_as_confirmatory_empirical_falsification():
    record = _valid_record()
    record["research_mode"] = "P0_D"
    record["prediction"].update(
        {
            "prediction_class": "S",
            "outcome_namespace": "EMPIRICAL",
            "outcome": "EMPIRICAL_CLAIM_FALSIFIED",
        }
    )
    with pytest.raises(ProtocolContractError, match="P0-D/P0-Q output cannot carry"):
        validate_v071a_output(record)


def test_invalid_function_state_is_known_bad_and_fails():
    record = _valid_record()
    record["function_map_output"]["summary_state"] = "EVERYTHING_WORKS"
    with pytest.raises(ProtocolContractError, match="invalid function-map"):
        validate_v071a_output(record)


def test_invalid_map_research_role_is_known_bad_and_fails():
    record = _valid_record()
    record["limit_map_output"]["research_role"] = "MAGIC_BOUNDARY"
    with pytest.raises(ProtocolContractError, match="invalid research role"):
        validate_v071a_output(record)


def test_invalid_pathway_independence_grade_is_known_bad_and_fails():
    record = _valid_record()
    record["independence"]["data_independence"] = "TOTALLY_INDEPENDENT_TRUST_ME"
    with pytest.raises(ProtocolContractError, match="invalid pathway-specific independence"):
        validate_v071a_output(record)


def test_copy_of_valid_record_remains_valid_after_non_scientific_metadata_change():
    record = copy.deepcopy(_valid_record())
    record["provenance"]["note"] = "metadata-only"
    validate_v071a_output(record)
