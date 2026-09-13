import json
from pathlib import Path

from src.chi_bio_empirical_freeze_contract import validate_empirical_freeze


FREEZE = Path("config/gri_Chi_bio_shortterm_g2_r1_A3_empirical_freeze_20260913_v1.json")


def _record():
    return json.loads(FREEZE.read_text(encoding="utf-8"))


def test_active_shortterm_freeze_passes_empirical_contract():
    record = _record()
    validate_empirical_freeze(record)
    assert record["status"] == "FROZEN_BEFORE_REAL_SCC25_G2_OUTCOMES"
    assert record["chi_bio_outcomes_opened_before_freeze"] is False
    assert record["frozen_before_real_candidate_values"] is True
    assert record["chi_bio_status"] == "NOT_ADMITTED"
    assert record["biological_unity_boundary_admitted"] is False


def test_shortterm_model_roles_are_frozen_without_posthoc_rank_winner():
    record = _record()
    assert record["primary_transition_model"] == "SHARED_T_PLUS_TREATMENT_INPUT_PLUS_INTERCEPT"
    assert record["secondary_transition_model"] == "TREATMENT_INTERACTION_T_PLUS_DELTA_T_PLUS_INPUT_PLUS_INTERCEPT"
    assert record["rank_design"] == "A3_ROBUSTNESS_REQUIRED_R2_R3"
    assert record["primary_rank"] is None
    assert record["sensitivity_ranks"] == []
    assert record["robustness_ranks"] == [2, 3]
    assert "REPRESENTATION_DEPENDENT_NO_TRANSFER" in record["rank_robustness_rule"]


def test_shortterm_feature_and_day0_rules_are_treatment_blind():
    record = _record()
    feature = record["feature_universe_rule"]
    assert "CPM >= 1 in at least 3 of 6 PBS states" in feature
    assert "CTX values are forbidden from feature selection" in feature
    day0 = record["day0_initialization_rule"]
    assert "single shared pre-treatment initial state" in day0
    assert record["source_binding"]["declared_transitions"] == 10


def test_shortterm_numerical_and_adequacy_guards_are_explicit():
    record = _record()
    assert "67108864" in record["conditioning_refusal_rule"]
    adequacy = record["model_adequacy_refusal_rule"]
    assert "persistence" in adequacy
    assert "arm-specific leave-one-out mean-next-state" in adequacy
    escalation = record["d2_escalation_rule"]
    assert "at least 6 of 10 omitted transitions" in escalation
    assert "BOTH r=2 and r=3" in escalation


def test_shortterm_uncertainty_is_serial_sensitivity_not_iid_bootstrap():
    record = _record()
    uncertainty = record["uncertainty_rule"]
    assert "Do not use an iid bootstrap over days" in uncertainty
    assert "shared-origin block refit" in uncertainty
    assert "leave-one-PBS-state basis refits" in uncertainty
    assert "REFUSE_UNCERTAINTY_SPANS_BOUNDARY" in uncertainty


def test_shortterm_transport_forbids_unearned_daily_weekly_conversion():
    record = _record()
    transport = record["transport_rule"]
    assert "Do not exponentiate" in transport
    assert "roots" in transport
    assert "separately earned semigroup/time-homogeneity validation" in transport


def test_shortterm_source_binding_is_exact():
    source = _record()["source_binding"]
    assert source["series"] == "GSE114446"
    assert source["processed_file"] == "GSE114446_STCCountsCG.txt.gz"
    assert source["processed_file_sha256"] == "c1318f5ad3b62d26c043de370cdca7300548337918f4543b13769bbe7a08a6c2"
    assert source["cell_line"] == "SCC25"
    assert source["pbs_states"] == 6
    assert source["ctx_states"] == 5
