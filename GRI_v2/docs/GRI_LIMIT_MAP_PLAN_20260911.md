# GRI Limit Map plan

**Date:** 2026-09-11  
**Mode:** P0-D / P0-Q boundary mapping  
**Protocol:** v0.7.1 + v0.7.1A  
**Confirmatory status:** NONE unless separately frozen under MFR-14

## Purpose

Consolidate all known places where the current GRI representation, estimator, reduction, or Engine scope weakens, changes class, becomes non-identifiable, or should refuse. The Limit Map is coequal with the Function Map and must not be allowed to redefine ordinary performance.

## Existing limits already established or strongly indicated

| Limit ID | Boundary | Current status | Classification |
|---|---|---|---|
| L01 | `CV/2` as biological chi/damping | Retired | REPRESENTATION_LIMIT |
| L02 | Sample rank / pseudotrajectory as time | Retired | TEMPORAL_INFERENCE_LIMIT |
| L03 | Raw Stage A cohort-size dependence | Detected and calibrated | CONSTRUCTION_LIMIT |
| L04 | Nonlinear-only dependence | Failed F2 capability | ENGINE_SCOPE_LIMIT |
| L05 | Regulatory-autonomy scalar | Redundant/dropped | REDUCTION_LIMIT |
| L06 | CKA/shared-private decomposition as novelty | Established primitive | NOVELTY_SCOPE_LIMIT |
| L07 | Strong per-cancer Hallmark semantic promotion | Failed general promotion | SEMANTIC_SCOPE_LIMIT |
| L08 | 24-cancer original pan-cancer promotion floor | Not met | PROMOTION_LIMIT |
| L09 | PCPG global transport | Recurrent stress case | TRANSPORT/REPRESENTATION_BOUNDARY_CANDIDATE |
| L10 | Five promoter-core Hallmarks lacking mapping support | Structural refusal | INPUT/ANNOTATION_LIMIT |
| L11 | H3b label-specific effect | Small/support-sensitive | INTERPRETATION_LIMIT |
| L12 | Purity/leukocyte projection as full composition control | Not licensed | CONFOUNDER_CONTROL_LIMIT |
| L13 | Raw cross-cancer Delta_CKA as universal bridge | Retired after null-floor analysis | SCALAR_REDUCTION_LIMIT |
| L14 | HM27/HM450 merged platform generalization | Unresolved externally | PLATFORM_GENERALIZATION_LIMIT |
| L15 | Biological chi | Not admitted | MODEL_ADMISSION_LIMIT |
| L16 | Temporal inheritance/recovery | Not tested by static TCGA | EVIDENCE_TYPE_LIMIT |
| L17 | External generalization/clinical utility | Not established | VALIDATION_SCOPE_LIMIT |

## Limit Map dimensions

Each limit record should include:

- `limit_id`
- `object_or_claim`
- `limit_class`
- `trigger_variable_or_condition`
- `observed_boundary_or_state`
- `boundary_type = GRADUAL | ABRUPT | STOCHASTIC | REFUSAL | NONIDENTIFIABLE | UNRESOLVED`
- `first_component_affected`
- `scalar_effect`
- `modal_effect`
- `conglomerate_effect`
- `cross_component_effect`
- `technical_or_biological_context`
- `known_alternative_explanations`
- `uncertainty`
- `evidence_status`
- `independence_status`
- `coverage_role = BOUNDARY_OR_TRANSITION | RARE_NATURAL_LIMIT | NOT_APPLICABLE`
- `support_state = STOPS_WORKING_HERE | NOT_KNOWN_HERE`
- `refusal_code_if_applicable`
- `follow_up_status`
- `provenance`

## Boundary questions to pursue prospectively

1. At what missingness/support levels do specific outputs cease to be stable or interpretable?
2. How concentrated can the leading modes become before a global scalar/CKA summary stops representing distributed structure adequately?
3. Under what platform-mixing or harmonization conditions does the representation cease to transport?
4. When does composition adjustment materially reorganize the architecture rather than merely attenuate it?
5. Can the PCPG stress pattern be explained by a domain-native biological/subtype/platform variable, or is it a general transport boundary?
6. Which Hallmark mapping support thresholds produce deterministic refusal rather than noisy estimates?
7. What nonlinear dependence patterns require a future Engine class rather than the current linear architecture?
8. Where do global and Hallmark-specific evidence disagree strongly enough that the Engine should return partial admission rather than one summary label?

## Rare-natural-testbed firewall

No current GRI case is designated `RARE_NATURAL_TESTBED` in this plan.

PCPG is retained as a recurrent stress case because it is scientifically informative, but rarity must be demonstrated independently through oncology-native evidence such as prevalence, accepted rare subtype/category, or an independently measured extreme parameter combination. Engine disagreement itself is not a rarity criterion.

For any future P1 rare-natural testbed:

- eligibility/selection must be frozen before Engine output is inspected;
- selection may use domain-native magnitude/category/exposure/date/phenotype, not agreement with GRI;
- preserve the eligible universe/search route where feasible;
- compare the rare case against ordinary or less-extreme context;
- do not treat it as representative of baseline behavior.

## Relationship to Function Map

A limit does not erase function elsewhere. A strong Function Map region does not erase a reproducible failure. Every mature output should be capable of returning:

- `WORKS_HERE`
- `STOPS_WORKING_HERE`
- `NOT_KNOWN_HERE`

## Exit condition

Limit Map v0.1 is complete when all currently material known limits/refusals are centralized with provenance and each open boundary has an explicit disposition: promotion track, dead end, artifact/noise closure with evidence, deferred resource limit, or unresolved.