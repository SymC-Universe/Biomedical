import copy
import json
from pathlib import Path

import pytest

from src.chi_bio_abc_architecture_contract import (
    ABCArchitectureContractError,
    validate_abc_architecture_freeze,
)


FREEZE = Path("config/gri_Chi_bio_ABC_architecture_freeze_20260913_v0_1.json")


def load_record():
    return json.loads(FREEZE.read_text(encoding="utf-8"))


def test_frozen_abc_architecture_record_passes():
    validate_abc_architecture_freeze(load_record())


def test_a3_cannot_privilege_a_rank_after_approval():
    record = load_record()
    record["decision_A_first_G2_rank_design"]["primary_rank"] = 2
    with pytest.raises(ABCArchitectureContractError, match="privilege"):
        validate_abc_architecture_freeze(record)


def test_a3_requires_representation_dependent_refusal():
    record = load_record()
    record["decision_A_first_G2_rank_design"]["robustness_rule"] = "agree somehow"
    with pytest.raises(ABCArchitectureContractError, match="representation-dependent"):
        validate_abc_architecture_freeze(record)


def test_b3_does_not_freeze_exact_panel_or_authorize_g1_execution():
    record = load_record()
    assert record["decision_B_first_G1_state_basis"]["exact_panel_frozen"] is False
    assert record["decision_B_first_G1_state_basis"]["g1_empirical_state_execution_authorized"] is False
    validate_abc_architecture_freeze(record)


def test_c3_cannot_smuggle_in_normalized_g1():
    record = load_record()
    record["decision_C_G1_restoration_strategy"]["normalization_derivation_id"] = "invented-beta"
    with pytest.raises(ABCArchitectureContractError, match="normalization"):
        validate_abc_architecture_freeze(record)


def test_architecture_freeze_is_not_full_empirical_execution_authorization():
    record = load_record()
    record["authorization"]["real_G2_outcome_bearing_execution"] = True
    with pytest.raises(ABCArchitectureContractError, match="full G2"):
        validate_abc_architecture_freeze(record)
