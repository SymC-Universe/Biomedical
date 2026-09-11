# GRI Regulatory Substrate Atlas v0.1 schema and independence architecture

**Date:** 2026-09-11  
**Status:** P0-D / TOOL-ARCHITECTURE DESIGN  
**Protocol:** v0.7.1 Sections 16-17, 19.3 + v0.7.1A A.2-A.8  
**Validated Atlas:** NO

## Purpose

Define the structure of an independently constructed Regulatory Substrate Atlas that can later provide read-only empirical context to a frozen GRI Engine. This schema does not promote any current TCGA development evidence into independent validation.

## Core rule

The Atlas answers:

> Where has a regulatory state like this been observed before, under what conditions, and with what uncertainty?

It does not tell the System Model or Engine what to find, choose thresholds, repair weak predictions, or select favorable reference cases.

## Atlas record schema

Each record should preserve the following groups.

### Identity
- `atlas_record_id`
- `atlas_version`
- `entity_id`
- `cohort_id`
- `disease_or_tissue`
- `subtype_or_state`
- `normal_tumor_status`
- `condition`
- `collection_time_or_order` where genuinely temporal
- `coverage_role = NOMINAL_FUNCTION | PERTURBED_FUNCTION | BOUNDARY_OR_TRANSITION | RARE_NATURAL_LIMIT | NOT_APPLICABLE | NOT_AVAILABLE | UNRESOLVED`

### Measurement
- `modality`
- `assay_platform`
- `raw_observable`
- `units_or_convention`
- `normalization_or_preprocessing`
- `sample_size`
- `missingness_summary`
- `batch_or_platform_context`
- `known_confounders`

### Architecture
- `scalar_coordinates`
- `scalar_epistemic_class`
- `modal_vector_features`
- `modal_epistemic_class`
- `conglomerate_system_features`
- `conglomerate_epistemic_class`
- `cross_component_relationships`
- `open_channel_state`
- `reduction_adequacy`
- `function_map_state`
- `limit_map_state`
- `support_state = WORKS_HERE | STOPS_WORKING_HERE | NOT_KNOWN_HERE`

### Uncertainty
- `uncertainty_method`
- `confidence_or_interval`
- `numerical_tolerance`
- `identifiability_status`

### Evidence and provenance
- `source_type = PRIMARY_DATASET | PRIMARY_LITERATURE | REFERENCE_DATABASE | SYNTHETIC | OTHER`
- `source_identifier`
- `source_retrieval_date`
- `source_location`
- `evidence_tier`
- `extraction_method`
- `code_version`
- `record_hash`
- `selection_status`
- `selection_rule`
- `claim_ceiling`

### Independence
- `data_independence`
- `cohort_system_independence`
- `outcome_independence`
- `parameter_tuning_independence`
- `method_independence`
- `atlas_independence_grade = INDEPENDENT | PARTIALLY_INDEPENDENT | NON_INDEPENDENT_FOR_ENGINE_VALIDATION`
- `source_literature_independence`
- `temporal_independence`
- `shared_information_that_could_force_agreement`

### Rare-natural-testbed fields, only when applicable
- `rarity_basis`
- `rarity_source`
- `eligible_candidate_universe`
- `selection_independent_of_engine = true|false`
- `matched_ordinary_context`
- `representative_status = REPRESENTATIVE | NONREPRESENTATIVE_LIMIT_PROBE`

## Initial modality families

The working Atlas may eventually include, without premature collapse:

- RNA expression;
- DNA methylation;
- chromatin accessibility;
- histone state;
- single-cell states;
- spatial organization;
- proteomics/phosphoproteomics;
- tumor purity;
- cell composition;
- pathway/module architecture;
- cancer type/subtype;
- normal/reference tissue;
- genomic alteration context;
- clinical/molecular covariates;
- longitudinal or perturbational states where genuine ordering exists.

## Independence treatment of current TCGA lineage

Current TCGA/PanCanAtlas evidence may be entered as `DEVELOPMENT/HISTORICAL_CONTEXT`, but rows that contributed to System Model/Engine development are `NON_INDEPENDENT_FOR_ENGINE_VALIDATION` for that Engine version.

This includes current methylation, RNA, RPPA, genomic, purity, leukocyte, C1, P0, and post-C1 sensitivity lineages where they share the same development evidence path.

## Promotion states

Atlas records should use the protocol states:

- candidate
- provisional
- verified
- locked reference
- superseded
- disputed
- excluded
- blocked/unverified

Promotion requires evidence and source reconstruction appropriate to the intended claim. Historical state remains preserved when a record is demoted or superseded.

## Representative-selection firewall

No representative used for validation/ranking/prediction may be chosen because it agrees best with GRI. Outcome-independent selection must be frozen before relevant performance is inspected. A post-hoc closest-agreement case can be retained only as diagnostic P0-D discovery.

## Function and Limit Map integration

Atlas v0.1 should expose both:

- **Function Map context:** occupied supported regimes, response surfaces/trajectories, supported coupling relationships, uncertainty, identifiability.
- **Limit Map context:** degradation/refusal/failure regions, rare-natural-testbed outcomes where independently qualified, and whether the limit is biological/physical, inferential, estimator-related, or unresolved.

## Minimal first Atlas release

A first Atlas does not need every modality. A defensible v0.1 can begin with a small set of independently sourced, well-provenanced families that directly test current GRI outputs, provided it:

1. preserves raw/native observables;
2. does not reuse development outcomes as independent validation;
3. freezes inclusion/extraction rules;
4. carries pathway-specific independence;
5. retains discordant references;
6. supports `NO_ATLAS_MATCH` rather than forced matching;
7. has an immutable version/hash when used in P1.

## Atlas validation exit condition

The Atlas becomes eligible for confirmatory use only after the decisive reference families have source provenance reconstructed, selection rules frozen, independence graded, and a locked version created before the associated external confirmatory evidence is opened.