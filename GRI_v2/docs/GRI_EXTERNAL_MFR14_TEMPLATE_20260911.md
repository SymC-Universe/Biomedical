# GRI external confirmation MFR-14 template

**Date:** 2026-09-11  
**Status:** TEMPLATE ONLY, NOT A FREEZE  
**Protocol:** General Protocol v0.7.1 + v0.7.1A  
**Purpose:** prepare the future external P1 record without filling outcome-dependent choices now.

> This file is not a preregistration. It becomes a freeze only after all required fields are completed, reviewed, versioned, and verifiably timestamped before decisive evidence is opened.

## MFR-01 Frozen claim

- `claim_id:`
- `version:`
- `exact_claim_text:`
- `claim_scope:`
- `frozen_scientific_question_task:`
- `intended_value_axis:`

## MFR-02 Hypothesis provenance

Choose one or more:

- `DOMAIN_THEORY`
- `EXTERNAL_THEORY`
- `FRAMEWORK_DERIVED`
- `DATA_DERIVED`
- `CROSS_DOMAIN_TRANSFER`

Record:

- `provenance_class:`
- `origin_record:`
- `promotion_debt_if_data_derived:`

## MFR-03 Target object / native observable

- `native_observable_or_state_variable:`
- `measurement_method:`
- `object_capable_of_falsifying_claim:`
- `why_internal_GRI_score_alone_is_not_the_target:`

## MFR-04 Representation and validity regime

- `native_statistical_or_biological_model:`
- `GRI_representation_used:`
- `validity_conditions:`
- `inclusion_rules:`
- `exclusion_rules:`
- `units_conventions:`
- `conditions_where_representation_is_not_licensed:`
- `coverage_role:` NOMINAL_FUNCTION | PERTURBED_FUNCTION | BOUNDARY_OR_TRANSITION | RARE_NATURAL_LIMIT

## MFR-05 Strongest relevant native comparator

- `comparator_status:` COMPARATOR_IDENTIFIED | NO_NATIVE_COMPARATOR
- `comparator_name_version:`
- `comparator_selection_route:`
- `literature_benchmark_expert_basis:`
- `selection_freeze_date_version:`
- `same_decisive_split_possible:` yes/no + reason

If `NO_NATIVE_COMPARATOR`, state the strongest domain-native null/alternative and do not claim ADDS over a nonexistent toolkit.

## MFR-06 Null / competing explanation

- `primary_null:`
- `competing_explanation_1:`
- `competing_explanation_2:`
- `nuisance_structure_preserved_by_null:`

## MFR-07 Expected response

- `expected_direction_class_ordering_or_invariance:`
- `opposite_or_incompatible_outcome_that_could_occur:`

## MFR-08 Decision / adjudication rule

- `primary_metric:`
- `decision_rule:`
- `threshold_or_region_if_justified:`
- `why_threshold_is_domain_justified:`

## MFR-09 Uncertainty / tolerance / indeterminate zone

- `measurement_uncertainty:`
- `numerical_tolerance:`
- `model_uncertainty:`
- `indeterminate_rule:`

## MFR-10 Pathway-specific independence / leakage map

- `data_independence:`
- `cohort_system_independence:`
- `outcome_independence:`
- `parameter_tuning_independence:`
- `method_independence:`
- `atlas_independence:`
- `source_literature_independence:`
- `temporal_independence:`
- `shared_information_that_could_force_agreement:`
- `independence_conclusion:`

## MFR-11 Multiplicity / search-space accounting

- `endpoint_family:`
- `feature_family:`
- `model_family:`
- `subgroup_family:`
- `threshold_family:`
- `correction_or_hierarchy:`
- `full_selection_procedure_repeated_in_null:` yes/no/not-applicable

## MFR-12 Freeze identity and untouched decisive test

- `freeze_identifier:`
- `freeze_timestamp:`
- `system_model_version:`
- `engine_version:`
- `atlas_version:`
- `prediction_record_version:`
- `confirmatory_dataset_system_experiment:`
- `evidence_unopened_at_freeze:` yes/no
- `verification_of_unopened_status:`

## MFR-13 Explicit falsifier

- `falsifying_result:`
- `native_comparator_failure_condition:`
- `loss_of_relation_condition:`
- `representation_failure_condition_if_applicable:`

## MFR-14 Precommitted failure consequence

Choose and specify:

- `CLAIM_FALSIFIED`
- `CLAIM_NARROWED`
- `REPRESENTATION_RETIRED_FOR_REGIME`
- `NO_ADDED_SYMC_VALUE`
- `DOMAIN_LIMITED`
- `REGIME_LIMITED`
- `TOOL_VERSION_NOT_QUALIFIED`
- other explicit consequence

Record:

- `failure_consequence:`
- `what_will_not_be_retuned_on_same_evidence:`

# Prediction-specific extension

- `prediction_id:`
- `prediction_class:` S | M
- `scientific_layer:` scalar | modal/vector | conglomerate/system | inheritance | emergence | failure | refusal
- `perturbation_exposure_changed_condition:`
- `standard_toolkit_prediction_same_test:`
- `test_family:`
- `explicit_falsification_criterion:`
- `result:` [blank before opening]
- `epistemic_status:` PROSPECTIVE_PREDICTION before opening

# v0.7.1A Function/Limit extension

- `function_map_region_being_tested:`
- `limit_map_region_being_tested:`
- `support_state_expected:` WORKS_HERE | STOPS_WORKING_HERE | NOT_KNOWN_HERE
- `rare_natural_testbed:` yes/no

If yes:

- `rarity_basis:`
- `rarity_source:`
- `eligible_candidate_universe:`
- `selection_independent_of_engine:`
- `matched_ordinary_context:`
- `representative_status:` NONREPRESENTATIVE_LIMIT_PROBE unless separately justified

# Pre-freeze checklist

Before this template can become a P1 freeze:

1. all 14 MFR fields complete;
2. scientific question fixed before comparator selection;
3. comparator route documented and frozen;
4. System Model/Engine scope frozen;
5. Atlas version frozen and decisively used reference families independence-audited;
6. decisive evidence unopened;
7. multiplicity/search space fixed;
8. falsifier and failure consequence explicit;
9. no result field populated;
10. verifiable timestamp/commit/deposit created.
