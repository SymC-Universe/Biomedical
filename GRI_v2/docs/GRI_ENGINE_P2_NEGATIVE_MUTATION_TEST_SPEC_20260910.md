# GRI Engine P2 negative and mutation test specification

**Date:** 2026-09-10  
**Status:** P0-Q ENGINE QUALIFICATION SPECIFICATION, NOT YET A P2 PASS  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Purpose

Define the production-path tests required before a future GRI Engine release can claim qualified refusal and guard behavior. This specification does not change any scientific threshold or current C1/P0 result.

Every qualifying check must:

1. call the production Engine path it claims to verify;
2. have at least one stored known-bad input that violates the guarded property;
3. demonstrably fail or refuse on that input;
4. use explicit, single-sourced tolerances;
5. validate raw input before coercion/casting shortcuts;
6. preserve the failure signature and expected refusal/output state.

## 1. Negative-control matrix

| Test ID | Known-bad / boundary input | Property being guarded | Required production behavior | Wrong behavior that must fail the test |
|---|---|---|---|---|
| NEG01 | patient rows permuted between methylation and RNA | patient-specific cross-layer alignment | patient-specific evidence collapses or is not admitted | preserved high patient-specific evidence without warning |
| NEG02 | Hallmark labels permuted while patient geometry retained | semantic specificity distinct from global geometry | label-specific support falls/refuses while global geometry may remain | global geometry falsely forced to disappear or semantic support remains promoted |
| NEG03 | synthetic pure measured confounding | independent cross-layer biology claim | prescribed context attack removes/narrows promoted independent signal | confounded signal remains promoted as independent biology |
| NEG04 | synthetic technical concordance removed by technical mask | technical robustness | technical attack identifies/narrows the false concordance | false concordance remains promoted unchanged |
| NEG05 | independent synthetic layers | global shared structure | `INSUFFICIENT_SHARED_STRUCTURE` or equivalent | valid shared-state classification |
| NEG06 | nonlinear-only shared synthetic dependence | unsupported nonlinear scope | `UNSUPPORTED_NONLINEAR_SCOPE` | calibrated linear capability claim |
| NEG07 | Hallmark with mapping below frozen support floor | feature/mapping admission | structural refusal / not evaluable | substitute another Hallmark or silently reduce requirement |
| NEG08 | duplicate/ambiguous patient identity | input identity | deterministic input refusal | first-match/averaging/implicit selection |
| NEG09 | composition-required output with < required complete support | evaluability | `NOT_EVALUABLE` | hidden imputation or sample-rule relaxation |
| NEG10 | biological chi requested under current System Model | chi admission | `CHI_NOT_ADMITTED` | numerical biological chi returned |
| NEG11 | temporal/inheritance output requested from unordered cross-sectional input | evidence-type admission | `TEMPORAL_EVIDENCE_REQUIRED` | recovery/inheritance/progression output |
| NEG12 | current-development TCGA Atlas family requested as independent Engine validation | Atlas independence | `NON_INDEPENDENT_FOR_ENGINE_VALIDATION` | independent-validation PASS |
| NEG13 | no qualifying Atlas reference exists | Atlas query | `NO_ATLAS_MATCH` / `NOT_KNOWN_HERE` | nearest favorable forced match |
| NEG14 | scalar compression requested where reduction adequacy fails | reduction gate | `SCALAR_NOT_ADEQUATE` or partial admission | scalar emitted as sufficient system description |
| NEG15 | boundary input near admission threshold | refusal behavior at hardest region | deterministic uncertainty/indeterminate/refusal as frozen | unstable flip or forced classification |
| NEG16 | unknown output label injected by stale lookup table | label vocabulary synchronization | semantic validator rejects mismatch | unknown label silently accepted |

## 2. Mutation matrix

Each mutation is intentionally wrong. At least one test above or a dedicated regression must detect it.

| Mutation ID | Deliberate corruption | Required detecting test family |
|---|---|---|
| MUT01 | bypass patient-order check | NEG01 / identity regression |
| MUT02 | replace patient permutation with identity | NEG01 plus null-integrity regression |
| MUT03 | replace label permutation with identity | NEG02 plus label-null integrity |
| MUT04 | weaken construction null so original covariance survives | independent-layer/construction-null regression |
| MUT05 | disable technical mask | NEG04 |
| MUT06 | bypass purity/leukocyte projection when adjusted output requested | NEG03 plus adjusted-output semantic check |
| MUT07 | treat source-missing centered RNA value as raw zero expression | missingness equivalence/state test |
| MUT08 | accept duplicate sample root by first occurrence | NEG08 |
| MUT09 | silently lower n/support gate | NEG07/NEG09 plus frozen-config semantic check |
| MUT10 | remove epistemic-status field from output | output-schema validator |
| MUT11 | enable biological chi output without admitted coordinate | NEG10 |
| MUT12 | admit nonlinear-only dependence | NEG06 |
| MUT13 | ignore Atlas independence grade | NEG12 |
| MUT14 | choose nearest Atlas point when no valid match exists | NEG13 |
| MUT15 | bypass source/hash verification | input-provenance regression |
| MUT16 | change seed namespace without version change | deterministic repeatability regression |
| MUT17 | disable result manifest | release integrity regression |
| MUT18 | mutate `WORKS_HERE`/`STOPS_WORKING_HERE` mapping so a limit is reported as function | Function/Limit semantic validator |
| MUT19 | collapse `PARTIAL_ADMISSION` into PASS | partial-result semantic validator |
| MUT20 | allow `RARE_NATURAL_TESTBED` solely because Engine residual is extreme | rare-selection firewall test |

## 3. Required stored fixtures

A future production test package should include small deterministic fixtures for:

- valid nominal shared structure;
- independent layers;
- pure confounding;
- label-scrambled but globally shared geometry;
- technical artifact concordance;
- nonlinear-only dependence;
- controlled missingness including a zero-information column;
- duplicate patient IDs;
- insufficient mapping;
- insufficient composition-complete support;
- scalar-adequacy boundary case;
- Atlas independent, partially independent, non-independent, and no-match cases;
- rare-case selection metadata with both valid native rarity and invalid Engine-selected rarity.

Synthetic fixtures remain method qualification only.

## 4. v0.7.1A Function/Limit requirements

The production test set must include both sides:

### Function tests

- a supported nominal input returns `WORKS_HERE` with expected scalar/modal/conglomerate components;
- ordinary context perturbation that remains inside validity produces an interpretable changed state rather than immediate refusal;
- partial information loss is reported without falsely declaring failure;
- several internal organizations may map to similar allowed system outcomes where the synthetic ground truth is constructed that way.

### Limit tests

- unsupported model class returns `STOPS_WORKING_HERE` or a specific refusal;
- a boundary case can return `INDETERMINATE`/`PARTIAL_ADMISSION` rather than being forced;
- no-evidence region returns `NOT_KNOWN_HERE`;
- rare-natural-testbed designation cannot be triggered by Engine output alone.

Passing Function tests does not erase Limit failures, and passing Limit/refusal tests does not count as an empirical confirmation about cancer biology.

## 5. Execution order for future P2 candidate

1. freeze System Model/Engine candidate after current sensitivity/comparator disposition;
2. build one production entry point;
3. bind the input/output/refusal schema;
4. run nominal known-truth fixtures;
5. run negative fixtures;
6. run mutation suite and confirm each mutation is caught;
7. run repeatability/resume tests;
8. run clean-room benchmark reproduction;
9. run semantic capability-description synchronization;
10. only then evaluate P2 release qualification.

## 6. Current state

`P2_NEGATIVE_TESTS = SPECIFIED_NOT_EXECUTED`

`P2_MUTATION_TESTS = SPECIFIED_NOT_EXECUTED`

This is intentional. The production Engine object should not be frozen before the pending post-C1 sensitivity and comparator disposition can legitimately narrow its supported scope.