# GRI P2 clean-room and reproducibility plan

**Date:** 2026-09-10  
**Status:** P0-Q/P2 PREPARATION, NOT AN R1/R2/R3 PASS  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Purpose

Define the exact reproducibility work that a future GRI Engine/Tool release must pass. This plan distinguishes integrity checking from regeneration and from evidence-source reconstruction.

No current release level is upgraded by writing this plan.

## 1. R1 release reproducibility

R1 must report separately:

### R1-I integrity verification

A fresh environment verifies:

- release archive/commit identity;
- manifest completeness;
- every file hash;
- dependency specification;
- schema validity;
- semantic metadata against result records;
- expected test inventory/counts;
- declared System Model/Engine/Atlas versions;
- capability/refusal labels against emitted vocabulary.

Passing R1-I does not prove scientific quantities were regenerated.

### R1-R regeneration

A fresh environment regenerates every release artifact claimed regenerable from its documented frozen parent/input state.

Required controls:

1. builder names exact build input state;
2. external source acquisition is separate from project-owned files;
3. sources are hash/version validated before preprocessing;
4. no hidden local WORKING_STATE is assumed unless the release explicitly declares it as a frozen parent;
5. derived tables/figures are rebuilt programmatically;
6. output hashes are compared when byte determinism is expected;
7. numerical/semantic equivalence is checked under explicit tolerance when byte identity is not portable;
8. stale local cache cannot change outputs.

## 2. R2 calculation reproducibility

R2 independently recomputes scientific quantities from stored raw/intermediate inputs rather than rereading final summary tables.

Candidate GRI R2 checks after production consolidation:

- recompute Stage A `Cin,pair`, `Cin,PC1`, `Cout` from preserved expression inputs;
- recompute methylation `S_spec` from centered data/eigenspectrum;
- recompute linear CKA from methylation/RNA matrices;
- recompute principal angles;
- recompute same-Hallmark patient coupling and null effects;
- recompute context-projected quantities from preserved covariates;
- recompute predictive residuals/nMSE/R2 from preserved held-out predictions and observed targets;
- recompute confidence/risk rank association from frozen cancer-level records;
- recompute analytic CKA null-floor quantities used in the final interpretation;
- recompute Function/Limit classifications from the production Engine outputs rather than a prose table.

Each check must state exact input identity, algorithm, tolerance, and expected result.

## 3. R3 evidence reconstruction

R3 reconstructs the evidence provenance, not prior validation of the new conclusion.

For GRI this includes:

- authoritative identity of TCGA/PanCanAtlas data sources;
- exact methylation source identity and merged HM27/HM450 provenance;
- exact RNA source/transform lineage;
- MSigDB Hallmark source/version and membership identity;
- purity/leukocyte source identities;
- RPPA/genomic source identities where carried into released context;
- platform/sample identity rules;
- external Atlas source extraction and condition matching;
- external comparator method/version/literature basis;
- source independence judgments.

No numerical source/citation detail enters from AI recall. Each released provenance item must be traceable to a retrieved authoritative source.

## 4. Clean-room environment sequence

For the final P2 candidate:

```text
1. Obtain frozen release candidate.
2. Verify archive/commit hash.
3. Create fresh Python environment on a clean workspace.
4. Install only declared dependencies.
5. Run package self-audit before loading scientific data.
6. Acquire/mount documented source data.
7. Verify source identities.
8. Run production Engine on bundled synthetic/known-truth benchmark.
9. Run known-bad/refusal fixtures.
10. Run mutation suite separately.
11. Rebuild one real-data non-confirmatory benchmark from source/intermediate state.
12. Run Atlas interface tests using independent/non-independent/no-match fixtures.
13. Run Function/Limit output semantic checks.
14. Regenerate declared release tables/figures.
15. Compare hashes and semantic values with frozen expectations.
16. Archive environment, OS, dependency, command, seed, runtime, and output manifest.
```

A second machine/environment is preferred for the final P2 qualification claim.

## 5. Resume/checkpoint clean-room tests

Because GRI uses large matrices and long computations, interruption recovery must itself be qualified:

- stop after a valid atomic checkpoint and resume;
- interrupt during a non-atomic candidate write and verify it is rejected/recovered safely;
- mutate input hash and prove checkpoint rejection;
- mutate Engine/System Model version and prove incompatible checkpoint rejection;
- prove no duplicate/missing resample rows after resume;
- corrupt a checkpoint sidecar and prove detection;
- resume from a compatible prior implementation only when an explicit equivalence gate licenses it.

## 6. Semantic validation matrix

Hashes are necessary but insufficient. At minimum verify:

- stage/test counts;
- input/output row counts;
- admitted cancer/module counts;
- refusal counts;
- current exact label vocabulary;
- biological chi remains absent/not admitted;
- nonlinear-only scope remains refused in current version;
- Atlas independence grades control validation semantics;
- Function Map and Limit Map do not overwrite one another;
- method-scope PASS never becomes empirical confirmation;
- prediction output cannot exist without a valid frozen prediction record;
- manuscript/release metadata do not imply capacity-matched predictive superiority unless actually tested.

## 7. Current historical gaps to carry into clean-room planning

- current Stage C1 executable bytes are preserved in a separate returned execution package rather than fully represented by the current branch;
- the complete later legacy predictive P0/FINAL_HOLDOUT historical executable chain has not yet been recovered as one exact repaired package;
- the equal-dimensional post-FINAL comparator historical freeze is referenced but not recovered as an exact executable identity;
- the Regulatory Substrate Atlas does not yet exist as an independently locked release object;
- the production GRI Engine has not yet been consolidated.

These are explicit gaps, not inferred passes.

## 8. What can be prepared now

Safe now:

- dependency inventory;
- production schema drafts;
- known-truth/negative/mutation fixtures design;
- source-of-record checklist;
- command/regeneration map;
- semantic validator requirements;
- clean-room expected-output contract design.

Wait for sensitivity/comparator disposition before:

- freezing the final production System Model scope;
- freezing the Engine release candidate;
- setting any new scientifically consequential admission threshold;
- freezing the decisive external P1 task/Atlas/comparator.

**Current reproducibility status:** substantial historical provenance and stage-specific reproducibility evidence exists, but no consolidated GRI production release currently holds a complete P2 R1/R2/R3 qualification claim.