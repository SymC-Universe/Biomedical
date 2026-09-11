from __future__ import annotations

import json
from pathlib import Path

from src import protocol_contracts as contract


_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "config" / "gri_v071a_tool_output_schema_draft.json"


def _schema():
    with _SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_protocol_schema_json_is_loadable():
    schema = _schema()
    assert schema["status"] == "DRAFT_NOT_FROZEN"


def test_protocol_contract_version_is_synchronized():
    schema = _schema()
    assert schema["protocol_contract_version"] == contract.protocol_contract_version()


def test_required_top_level_groups_match_executable_contract_exactly():
    schema = _schema()
    assert tuple(schema["required_top_level_groups"]) == contract.REQUIRED_TOP_LEVEL_GROUPS


def test_research_modes_match_executable_contract_exactly():
    schema = _schema()
    assert set(schema["research_mode"]["allowed"]) == set(contract.RESEARCH_MODES)


def test_function_map_states_match_executable_contract_exactly():
    schema = _schema()
    assert set(schema["function_map_output"]["allowed_summary_states"]) == set(
        contract.FUNCTION_STATES
    )


def test_limit_map_states_match_executable_contract_exactly():
    schema = _schema()
    assert set(schema["limit_map_output"]["allowed_summary_states"]) == set(
        contract.LIMIT_STATES
    )


def test_coverage_roles_match_executable_contract_exactly():
    schema = _schema()
    assert set(schema["coverage_roles"]) == set(contract.RESEARCH_ROLES)


def test_independence_dimensions_match_executable_contract_exactly():
    schema = _schema()
    assert tuple(schema["independence"]["required_dimensions"]) == tuple(
        contract._REQUIRED_INDEPENDENCE_FIELDS
    )


def test_independence_allowed_states_match_executable_contract_exactly():
    schema = _schema()
    assert set(schema["independence"]["allowed_states"]) == set(
        contract.INDEPENDENCE_GRADES
    )


def test_rare_prohibited_selection_bases_match_executable_contract_exactly():
    schema = _schema()
    assert set(schema["rare_natural_testbed"]["prohibited_selection_bases"]) == set(
        contract._PROHIBITED_RARE_SELECTION_BASES
    )


def test_current_gri_nonclaims_preserve_biological_chi_firewall():
    schema = _schema()
    assert "biological_chi_not_admitted" in schema["current_GRI_nonclaims"]


def test_pcpg_remains_nonconfirmatory_in_draft_schema():
    schema = _schema()
    pcpg = schema["current_GRI_rare_limit_context"]["PCPG"]
    assert pcpg["status"] == "ADMITTED_FOR_P0_D_LIMIT_MAPPING_ONLY"
    assert pcpg["selection_status"] == "POST_RESULT_GRI_STRESS_CASE"
    assert pcpg["representative_status"] == "NONREPRESENTATIVE_LIMIT_PROBE"
    assert pcpg["confirmatory_weight"] == "NONE"
    assert pcpg["promotion_debt"] == "OPEN"
