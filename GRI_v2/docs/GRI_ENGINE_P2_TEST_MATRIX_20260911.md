# GRI Engine P2 negative / mutation / refusal test matrix

**Date:** 2026-09-11  
**Status:** DESIGN AUDIT, NOT RELEASE QUALIFICATION  
**Protocol:** v0.7.1 Sections 10, 14, 32.2, 33, 34, 51 + v0.7.1A Function/Limit extensions

## Purpose

Define the production-path tests required before the current computational lineage can be called a P2-qualified GRI Engine. This matrix does not change scientific thresholds or C1/P0 results.

## Production-path principle

Every qualification check must call the same production Engine entry point used for real analysis. Re-implementing a local copy of the scientific rule inside a test does not qualify the production code.

## A. Input/refusal tests

| ID | Known-bad / boundary input | Required production outcome | Must not happen |
|---|---|---|---|
| R01 | Missing required modality for requested cross-layer output | `MISSING_REQUIRED_MODALITY` | Silent single-layer substitution |
| R02 | Duplicate/ambiguous patient identity | `AMBIGUOUS_SAMPLE_IDENTITY` | First-row-wins selection |
| R03 | n below frozen minimum for requested estimator | `INSUFFICIENT_SAMPLE_SUPPORT` / `NOT_EVALUABLE` | Hidden imputation or threshold lowering |
| R04 | Unsupported platform / unresolved mapping | `UNSUPPORTED_PLATFORM_OR_MAPPING` | Treat as equivalent without audit |
| R05 | Unmapped required Hallmark feature support | `INSUFFICIENT_FEATURE_MAPPING` | Substitute a different pathway/feature |
| R06 | Nonfinite values outside admitted missingness rule | `UNSUPPORTED_MISSINGNESS_STATE` | Coerce before validation |
| R07 | No complete purity/leukocyte support for requested adjusted output | `CONTEXT_ADJUSTMENT_NOT_EVALUABLE` | Return raw output labeled adjusted |
| R08 | Nonlinear-only dependence request under current linear v0.1 scope | `UNSUPPORTED_NONLINEAR_SCOPE` | Claim calibrated coverage |
| R09 | Temporal/inheritance request from unordered static data | `TEMPORAL_EVIDENCE_REQUIRED` | Produce temporal prediction |
| R10 | Biological-chi request | `CHI_NOT_ADMITTED` | Compute historical CV/2 as biological chi |
| R11 | Atlas-independent-validation request using non-independent TCGA Atlas family | `ATLAS_NONINDEPENDENT_FOR_VALIDATION` | Report independent confirmation |
| R12 | Valid Engine output with no matching Atlas row | `NO_ATLAS_MATCH` while retaining Engine result | Force nearest favorable match |

## B. Known-truth semantic tests

| ID | Constructed scenario | Expected behavior |
|---|---|---|
| K01 | Independent layers | No promoted global cross-layer sharing |
| K02 | One genuine shared linear mode | Recover global sharing/modal evidence |
| K03 | Pure common measured confounder | Raw sharing attenuates after correct projection; no independent-biology promotion |
| K04 | Shared patient geometry with scrambled semantic labels | Global geometry may remain; label-specific promotion should fail |
| K05 | Module-specific matched sharing | Patient/module coupling recovers relative to null |
| K06 | Technical concordance removable by technical mask | Mask/attack reveals dependence on technical feature set |
| K07 | Controlled missingness | Admitted missingness behavior remains bounded and explicit |
| K08 | Nonlinear-only shared dependence | Current Engine returns unsupported-scope/refusal behavior |
| K09 | High-private / low-shared construction | Shared/private output reflects private dominance |
| K10 | Strong shared / low-private construction | Shared structure recovered |
| K11 | Zero-information centered feature | Does not inflate linear CKA and is explicitly tagged zero-information |

## C. Mutation tests

Each mutation is temporary and must be detected by at least one qualification test.

| ID | Mutation | Expected caught-by |
|---|---|---|
| M01 | Replace patient-null permutation with identity | K01/K02/K04 and null-integrity tests |
| M02 | Replace label-null permutation with identity | K04/K05 |
| M03 | Disable duplicate-root refusal | R02 |
| M04 | Disable technical mask | K06 |
| M05 | Bypass context projection | K03/R07 |
| M06 | Interpret missing RNA as raw zero expression | K07/K11 |
| M07 | Permit biological CV/2 chi | R10 |
| M08 | Admit nonlinear-only case | R08/K08 |
| M09 | Ignore Atlas independence grade | R11 |
| M10 | Remove output epistemic status | schema validator |
| M11 | Change deterministic RNG seed namespace | repeatability validator |
| M12 | Disable source/hash verification | integrity validator |
| M13 | Allow stale/incompatible checkpoint | resume/hash validator |
| M14 | Remove refusal status from output | schema/refusal validator |
| M15 | Replace canonical tolerance with hidden library default | tolerance single-source validator |

## D. Repeatability tests

1. Same input + System Model version + Engine version + Atlas version + prediction record -> identical discrete output/refusal classes.
2. Deterministic stochastic streams -> identical seeded sequence or explicitly bounded equivalent output.
3. Output row order deterministic.
4. Fresh execution independent of stale cache/checkpoint.
5. Valid checkpoint resume equals uninterrupted execution to the declared numerical tolerance.
6. Changed source/input hash invalidates incompatible checkpoint.
7. Changed Engine/System Model version invalidates incompatible checkpoint unless an explicit migration equivalence test passes.

## E. Semantic release tests

Release semantic validator must cross-check at least:

- advertised supported domains against capability registry;
- advertised unsupported domains against refusal registry;
- exact emitted label vocabulary against README/manuscript/repro guide;
- test counts against test results;
- claimed Engine/System Model/Atlas versions against output metadata;
- biological chi status remains `NOT_ADMITTED` unless a future scientific freeze changes it;
- nonlinear scope remains unsupported in current version;
- current predictive evidence labeled internal, not external/clinical;
- Function Map and Limit Map fields represented separately;
- `WORKS_HERE`, `STOPS_WORKING_HERE`, `NOT_KNOWN_HERE` vocabulary emitted exactly where implemented.

## F. Clean-room qualification

Required before P2 claim:

1. fresh environment;
2. manifest/hash verification before execution;
3. declared dependencies only;
4. no hidden local WORKING_STATE except in an explicit resume test;
5. benchmark/known-truth suite from source inputs;
6. at least one real-data non-confirmatory reference run from authoritative source or immutable frozen parent state;
7. semantic and numerical comparison to expected outputs;
8. environment/OS/runtime provenance archived;
9. release archive re-extracted and revalidated;
10. mutation/drift detection demonstrated against shipped artifacts.

## Current status

This matrix is a specification. Existing F2/F3/C1/P0 tests satisfy portions of it, but P2 qualification is not earned until the tests are routed through the consolidated production Engine and a release-level clean-room run passes.