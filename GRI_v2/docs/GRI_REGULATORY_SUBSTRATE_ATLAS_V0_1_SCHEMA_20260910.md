# GRI Regulatory Substrate Atlas v0.1 schema

**Date:** 2026-09-10  
**Status:** P0-D/P0-Q ARCHITECTURE DRAFT, NOT A LOCKED ATLAS  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## 1. Purpose

The Regulatory Substrate Atlas is an independently constructed empirical reference landscape used to contextualize GRI System Model / Engine outputs.

It answers:

> Where has a state like this been observed before, under what biological and technical conditions, with what uncertainty and evidence status?

It does not tell the Engine what it is supposed to find, and Atlas information may not tune Engine rules in a confirmatory path.

## 2. Separation from the Engine

Canonical architecture:

`GRI System Model -> implemented by GRI Engine`

`GRI System Model + Independent Regulatory Substrate Atlas -> GRI Tool`

`Validated GRI System Model + Independent Regulatory Substrate Atlas + Prospective Validation -> Predictive GRI Tool`

The Engine must be capable of basic measurement/inference without Atlas labels. Atlas comparison is a separate, read-only step.

## 3. Record schema

Each Atlas record should contain, where applicable:

### Identity and biological context

- `atlas_record_id`
- `atlas_version`
- `entity_type`
- `cohort_or_system_id`
- `cancer_type`
- `tissue`
- `normal_tumor_status`
- `subtype_or_phenotype`
- `condition`
- `acquisition_context`
- `research_role`

### Measurement provenance

- `measurement_modality`
- `source_dataset_or_publication`
- `source_version`
- `source_identifier`
- `source_hash_or_immutable_id`
- `retrieval_date`
- `raw_observable`
- `units_or_conventions`
- `platform`
- `batch_or_site_context`
- `sample_size`
- `missingness_summary`
- `preprocessing_harmonization_record`

### Architecture fields

- `scalar_coordinates`
- `scalar_epistemic_class`
- `modal_vector_features`
- `modal_epistemic_class`
- `conglomerate_system_features`
- `conglomerate_epistemic_class`
- `cross_component_relationships`
- `open_channel_features`
- `reduction_adequacy_status`
- `failure_boundary_status`

### v0.7.1A Function/Limit fields

- `function_map_status`
- `function_operating_regime`
- `occupancy_status`
- `response_surface_or_trajectory`
- `supported_relationships`
- `compensation_redistribution_status`
- `identifiability`
- `limit_map_status`
- `limit_type`
- `boundary_or_transition_status`
- `first_failing_component_if_known`
- `rare_natural_testbed_status`
- `rarity_basis`
- `base_rate_context`

### Uncertainty and validity

- `uncertainty_method`
- `uncertainty_values`
- `known_confounders`
- `validity_regime`
- `inclusion_status`
- `evidence_tier`
- `claim_ceiling`

### Independence fields

- `data_independence`
- `cohort_or_system_independence`
- `outcome_independence`
- `parameter_or_tuning_independence`
- `method_independence`
- `atlas_independence_grade`
- `source_or_literature_independence`
- `temporal_independence`
- `shared_information_capable_of_forcing_agreement`

### Promotion / lifecycle fields

- `selection_status`
- `reason_selected`
- `discovery_or_confirmatory_status`
- `promotion_debt_status`
- `candidate_provisional_verified_locked_status`
- `supersedes_record_id`
- `superseded_by_record_id`
- `dispute_status`
- `exclusion_reason`
- `provenance_manifest_id`

## 4. Allowed record states

Use the protocol lifecycle states where applicable:

- `candidate`
- `provisional`
- `verified`
- `locked_reference`
- `superseded`
- `disputed`
- `excluded`
- `blocked_unverified`

No record is promoted solely because it agrees with the Engine.

## 5. Research-role coverage

Each Atlas record should use one or more of:

- `NOMINAL_FUNCTION`
- `PERTURBED_FUNCTION`
- `BOUNDARY_OR_TRANSITION`
- `RARE_NATURAL_LIMIT`
- `NOT_AVAILABLE`
- `NOT_APPLICABLE`
- `UNRESOLVED`

These are research roles, not biological phases.

The Atlas should seek balanced coverage where native science and data allow. It must not define the domain only by ordinary cases or only by extreme failures.

## 6. Modality families

Candidate modality families include:

- RNA expression;
- DNA methylation;
- chromatin accessibility;
- histone state;
- proteomics / phosphoproteomics;
- single-cell structure;
- spatial organization;
- tumor purity;
- cell composition;
- pathway architecture;
- genomic alteration context;
- cancer type / subtype;
- normal/reference tissue;
- clinical/molecular covariates;
- longitudinal or perturbational measurements.

These modalities must not be collapsed prematurely into one omnibus score.

## 7. Initial development versus validation partition

### Development/historical reference families

The existing TCGA/PanCanAtlas methylation, RNA, RPPA, genomic, purity, and leukocyte evidence may populate the Atlas as **development/historical context**.

For validating the current GRI Engine, those overlapping families receive:

`NON_INDEPENDENT_FOR_ENGINE_VALIDATION`

unless a claim-specific pathway audit establishes a narrower partially independent use that cannot force the decisive agreement.

### Candidate independent reference families

A future external reference family may qualify as `INDEPENDENT` or `PARTIALLY_INDEPENDENT` only after documenting the exact pathway:

- source data;
- labels/outcomes;
- transformations;
- parameter/tuning overlap;
- method overlap;
- extraction blindness where feasible;
- temporal relationship;
- any shared nuisance reference.

Independence is assigned before confirmatory interpretation.

## 8. Rare-natural-testbed gate

Default:

`rare_natural_testbed_status = NOT_ADMITTED`

Admission requires independently supported rarity, authenticity/confounding review, base-rate context where knowable, and outcome-independent selection for P1 use.

Framework surprise is not a rarity criterion.

PCPG is therefore not entered as a rare natural testbed merely because it is a recurrent GRI stress case.

## 9. Representative-selection firewall

If the Atlas needs a representative system/point for confirmatory ranking or validation:

- selection must follow an outcome-independent rule frozen before relevant performance is inspected;
- strongest provenance may disagree with the Engine and must remain visible;
- closest agreement is not automatically the representative;
- full underlying distributions/coordinate sets remain available;
- post-result diagnostic representatives are labeled accordingly and carry promotion debt.

## 10. Function and Limit outputs

Atlas query results should separately expose:

### Function context

- where comparable organization is supported;
- range/occupancy;
- uncertainty;
- context sensitivity;
- coupling/relationship pattern;
- identifiability.

### Limit context

- known degradation/refusal region;
- type of limit;
- uncertainty;
- evidence status;
- independence class;
- rare-natural-testbed evidence if applicable.

Summary vocabulary:

- `WORKS_HERE`
- `STOPS_WORKING_HERE`
- `NOT_KNOWN_HERE`

## 11. Atlas lock requirements

Before an Atlas version is used in P1 confirmation or P2 predictive qualification:

1. freeze the inclusion rules;
2. freeze representative-selection rules;
3. freeze all decisive reference families;
4. record each reference family's independence grade;
5. freeze extraction/harmonization code and parameters;
6. preserve excluded/disputed/blocked entries;
7. hash/version the Atlas;
8. perform semantic validation in addition to file hashing;
9. freeze the Atlas together with the System Model / Engine and prediction record;
10. prohibit post-result edits to make confirmation look better.

## 12. What can be done now

Safe P0-D/P0-Q work while sensitivity runs:

- inventory candidate external sources;
- design schema and validation rules;
- classify existing TCGA families as development context;
- build pathway-specific independence fields;
- identify normal/reference and perturbational source families;
- identify candidate domain-native rarity criteria without selecting favorable cases;
- prepare extraction templates and provenance fields;
- build negative examples for `NO_ATLAS_MATCH` and non-independent reference rejection.

Not yet authorized as a scientific freeze:

- choosing a decisive external validation Atlas family based on expected GRI agreement;
- setting confirmatory thresholds from candidate Atlas outcomes;
- promoting PCPG or another case to rare-natural-testbed based on GRI results;
- declaring an Atlas `locked_reference` without source/evidence reconstruction.

**Current Atlas status:** architecture specified; independent validation Atlas not yet built or locked.