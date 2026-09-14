from __future__ import annotations

"""Hard guard for the approved A3+B3+C3 Chi_bio architecture freeze.

This contract deliberately distinguishes an architecture-level scientific
freeze from a full empirical execution freeze. It prevents later code from
misreading approval of A3/B3/C3 as approval of an exact G1 regulon panel, a
normalized G1 restoration model, or an outcome-bearing G2 run with unspecified
normalization/uncertainty/transport rules.
"""

from collections.abc import Mapping
from typing import Any


class ABCArchitectureContractError(ValueError):
    pass


EXPECTED_A = "A3_ROBUSTNESS_REQUIRED_R2_R3"
EXPECTED_B = "B3_EXTERNALLY_SOURCED_REGULON_LOW_DIMENSION_HYBRID"
EXPECTED_C = "C3_WITHHOLD_NORMALIZED_G1_UNTIL_RESTORATION_RESOLVED"


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ABCArchitectureContractError(f"{name} must be a mapping")
    return value


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_abc_architecture_freeze(record: Mapping[str, Any]) -> None:
    if not isinstance(record, Mapping):
        raise ABCArchitectureContractError("record must be a mapping")
    if record.get("status") != "FROZEN_ABC_ARCHITECTURE_NOT_FULL_EMPIRICAL_FREEZE":
        raise ABCArchitectureContractError("architecture freeze status mismatch")
    if not _nonempty(record.get("scientific_approval_reference")):
        raise ABCArchitectureContractError("scientific_approval_reference is required")
    if not _nonempty(record.get("freeze_timestamp")):
        raise ABCArchitectureContractError("freeze_timestamp is required")
    if record.get("chi_bio_outcomes_opened_before_freeze") is not False:
        raise ABCArchitectureContractError("Chi_bio outcomes must remain unopened before the architecture freeze")

    a = _mapping(record.get("decision_A_first_G2_rank_design"), "decision_A_first_G2_rank_design")
    if a.get("selected_option") != EXPECTED_A:
        raise ABCArchitectureContractError("A decision must be A3")
    if a.get("rank_set") != [2, 3]:
        raise ABCArchitectureContractError("A3 requires the ordered rank set [2, 3]")
    if a.get("primary_rank") is not None or a.get("sensitivity_rank") is not None:
        raise ABCArchitectureContractError("A3 may not privilege either rank")
    if not _nonempty(a.get("robustness_rule")) or "REPRESENTATION_DEPENDENT_NO_TRANSFER" not in a.get("robustness_rule", ""):
        raise ABCArchitectureContractError("A3 robustness rule must freeze the representation-dependent refusal")
    for key in ("treated_states_used_to_select", "proliferation_used_to_select", "distance_to_unity_used_to_select"):
        if a.get(key) is not False:
            raise ABCArchitectureContractError(f"A3 selection firewall requires {key}=false")

    b = _mapping(record.get("decision_B_first_G1_state_basis"), "decision_B_first_G1_state_basis")
    if b.get("selected_option") != EXPECTED_B:
        raise ABCArchitectureContractError("B decision must be B3")
    for key in ("leading_source_repository", "leading_source_commit", "representation_sensitivity_repository", "representation_sensitivity_commit", "state_coordinate_semantics", "subset_or_dimension_rule", "transport_rule"):
        if not _nonempty(b.get(key)):
            raise ABCArchitectureContractError(f"B3 requires {key}")
    if b.get("scc25_or_tcga_candidate_values_used_to_select") is not False:
        raise ABCArchitectureContractError("B3 may not use SCC25/TCGA candidate values for selection")
    if b.get("g1_empirical_state_execution_authorized") is not False:
        raise ABCArchitectureContractError("B3 architecture approval must not authorize empirical G1 state execution")
    if b.get("exact_panel_frozen") is not False:
        raise ABCArchitectureContractError("exact G1 panel is intentionally not frozen by this architecture record")

    c = _mapping(record.get("decision_C_G1_restoration_strategy"), "decision_C_G1_restoration_strategy")
    if c.get("selected_option") != EXPECTED_C:
        raise ABCArchitectureContractError("C decision must be C3")
    if c.get("restoration_not_tuned_to_unity") is not True:
        raise ABCArchitectureContractError("C3 must preserve the anti-unity-tuning guard")
    if c.get("normalized_empirical_g1_authorized") is not False:
        raise ABCArchitectureContractError("C3 forbids normalized empirical G1 execution")
    if c.get("normalization_derivation_id") not in (None, ""):
        raise ABCArchitectureContractError("C3 may not smuggle in a G1 normalization derivation")

    auth = _mapping(record.get("authorization"), "authorization")
    if auth.get("mechanical_and_provenance_work") is not True:
        raise ABCArchitectureContractError("architecture freeze must authorize safe mechanical/provenance work")
    if auth.get("rank_neutral_synthetic_and_preflight_work") is not True:
        raise ABCArchitectureContractError("architecture freeze must authorize rank-neutral preflight work")
    if auth.get("real_G2_outcome_bearing_execution") is not False:
        raise ABCArchitectureContractError("architecture freeze is not a full G2 empirical execution freeze")
    if auth.get("real_normalized_G1_execution") is not False:
        raise ABCArchitectureContractError("architecture freeze may not authorize normalized G1")
    if auth.get("biological_unity_boundary_admitted") is not False or auth.get("chi_bio_admitted") is not False:
        raise ABCArchitectureContractError("no biological unity boundary or Chi_bio admission is allowed")
