from __future__ import annotations

"""Hard gate for the first outcome-bearing G2/R1 empirical execution.

No real temporal source runner should proceed unless a scientific freeze record
passes this contract. The contract supports the earlier primary+sensitivity
rank design and the explicitly approved A3 design in which r=2 and r=3 are
co-equal robustness representations and neither may be promoted after seeing
outcomes.
"""

from collections.abc import Mapping
from typing import Any


class EmpiricalFreezeContractError(ValueError):
    pass


ALLOWED_PRIMARY_REDUCTIONS = frozenset({"R1_CONTROL_ONLY_UNSUPERVISED"})
ALLOWED_PRIMARY_RANKS = frozenset({2, 3})
ALLOWED_RANK_DESIGNS = frozenset({
    "PRIMARY_PLUS_SENSITIVITY",
    "A3_ROBUSTNESS_REQUIRED_R2_R3",
})
ALLOWED_TRANSITION_MODELS = frozenset({
    "SHARED_T_PLUS_TREATMENT_INPUT_PLUS_INTERCEPT",
    "SEPARATE_ARM_T_PLUS_INTERCEPT",
    "TREATMENT_INTERACTION_T_PLUS_DELTA_T_PLUS_INPUT_PLUS_INTERCEPT",
})
ALLOWED_BASIS_SCOPE = frozenset({
    "PBS_CONTROL_ONLY_PER_SOURCE",
    "EXTERNAL_FIXED_BASIS",
})
FORBIDDEN_SELECTION_INPUTS = frozenset({
    "CHI_BIO_VALUE",
    "DISTANCE_TO_UNITY",
    "UNITY_CROSSING_WEEK",
    "PROLIFERATION_RESPONSE",
    "ATAC_AGREEMENT",
    "SCRNA_CARRIER_AGREEMENT",
    "RESISTANT_CLONE_LABEL",
    "ATLAS_PLACEMENT",
    "SURVIVAL_OR_CLINICAL_OUTCOME",
})
REQUIRED_REFUSALS = frozenset({
    "REFUSE_RANK_DEFICIENT_DESIGN",
    "REFUSE_ILL_CONDITIONED_DESIGN",
    "REFUSE_UNSTABLE_OR_NONTRANSPORTABLE_BASIS",
    "REFUSE_SOURCE_IDENTITY_MISMATCH",
    "REFUSE_UNCERTAINTY_SPANS_BOUNDARY",
    "REFUSE_REPRESENTATION_DEPENDENT_NO_TRANSFER",
})


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_empirical_freeze(record: Mapping[str, Any]) -> None:
    if not isinstance(record, Mapping):
        raise EmpiricalFreezeContractError("record must be a mapping")

    for key in ("freeze_id", "scientific_approval_reference", "freeze_timestamp"):
        if not _nonempty(record.get(key)):
            raise EmpiricalFreezeContractError(f"{key} is required")

    if record.get("chi_bio_outcomes_opened_before_freeze") is not False:
        raise EmpiricalFreezeContractError(
            "chi_bio_outcomes_opened_before_freeze must be explicitly false"
        )
    if record.get("frozen_before_real_candidate_values") is not True:
        raise EmpiricalFreezeContractError(
            "empirical design must be frozen before real candidate values"
        )

    reduction = record.get("primary_reduction_id")
    if reduction not in ALLOWED_PRIMARY_REDUCTIONS:
        raise EmpiricalFreezeContractError(f"unsupported primary_reduction_id: {reduction!r}")

    rank_design = record.get("rank_design", "PRIMARY_PLUS_SENSITIVITY")
    if rank_design not in ALLOWED_RANK_DESIGNS:
        raise EmpiricalFreezeContractError(f"unsupported rank_design: {rank_design!r}")

    rank = record.get("primary_rank")
    sensitivity = record.get("sensitivity_ranks", [])
    if not isinstance(sensitivity, list):
        raise EmpiricalFreezeContractError("sensitivity_ranks must be a list")

    if rank_design == "PRIMARY_PLUS_SENSITIVITY":
        if not isinstance(rank, int) or isinstance(rank, bool) or rank not in ALLOWED_PRIMARY_RANKS:
            raise EmpiricalFreezeContractError("primary_rank must be prospectively frozen as 2 or 3")
        if any((not isinstance(x, int) or isinstance(x, bool) or x not in ALLOWED_PRIMARY_RANKS) for x in sensitivity):
            raise EmpiricalFreezeContractError("sensitivity_ranks may only contain 2 or 3")
        if rank in sensitivity:
            raise EmpiricalFreezeContractError("primary_rank may not also be listed as sensitivity")
    else:
        if rank is not None:
            raise EmpiricalFreezeContractError("A3 rank design may not designate a primary_rank")
        if sensitivity:
            raise EmpiricalFreezeContractError("A3 rank design may not designate sensitivity_ranks")
        if record.get("robustness_ranks") != [2, 3]:
            raise EmpiricalFreezeContractError("A3 rank design requires robustness_ranks [2, 3]")
        rule = record.get("rank_robustness_rule")
        if not _nonempty(rule) or "REPRESENTATION_DEPENDENT_NO_TRANSFER" not in rule:
            raise EmpiricalFreezeContractError(
                "A3 rank design requires a frozen representation-dependent refusal rule"
            )
        if not _nonempty(record.get("material_conclusion_schema")):
            raise EmpiricalFreezeContractError(
                "A3 rank design requires a frozen material_conclusion_schema before execution"
            )

    basis_scope = record.get("basis_scope")
    if basis_scope not in ALLOWED_BASIS_SCOPE:
        raise EmpiricalFreezeContractError(f"unsupported basis_scope: {basis_scope!r}")
    if basis_scope == "PBS_CONTROL_ONLY_PER_SOURCE" and record.get("basis_fit_uses_treated_states") is not False:
        raise EmpiricalFreezeContractError("control-only basis must explicitly exclude treated states")

    model = record.get("primary_transition_model")
    if model not in ALLOWED_TRANSITION_MODELS:
        raise EmpiricalFreezeContractError(f"unsupported primary_transition_model: {model!r}")

    for key in (
        "normalization_rule",
        "feature_universe_rule",
        "day0_initialization_rule",
        "conditioning_refusal_rule",
        "model_adequacy_refusal_rule",
        "uncertainty_rule",
        "transport_rule",
    ):
        if not _nonempty(record.get(key)):
            raise EmpiricalFreezeContractError(f"{key} is required")

    signals = frozenset(str(x) for x in record.get("selection_inputs", []))
    bad = signals & FORBIDDEN_SELECTION_INPUTS
    if bad:
        raise EmpiricalFreezeContractError(
            "forbidden selection input(s): " + ", ".join(sorted(bad))
        )

    refusals = frozenset(str(x) for x in record.get("supported_refusals", []))
    missing = REQUIRED_REFUSALS - refusals
    if missing:
        raise EmpiricalFreezeContractError(
            "missing required refusal(s): " + ", ".join(sorted(missing))
        )

    if record.get("proliferation_reserved_for_postconstruction_test") is not True:
        raise EmpiricalFreezeContractError("proliferation must remain reserved post-construction")
    if record.get("atac_reserved_for_postconstruction_relational_test") is not True:
        raise EmpiricalFreezeContractError("ATAC must remain reserved post-construction")
    if record.get("scrna_reserved_for_postconstruction_carrier_test") is not True:
        raise EmpiricalFreezeContractError("scRNA must remain reserved post-construction")

    if record.get("biological_unity_boundary_admitted") is not False:
        raise EmpiricalFreezeContractError("biological unity boundary must remain unadmitted")
