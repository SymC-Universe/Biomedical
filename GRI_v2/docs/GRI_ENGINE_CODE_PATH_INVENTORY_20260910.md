# GRI Engine code-path inventory

**Date:** 2026-09-10  
**Status:** P0-Q ENGINE CONSOLIDATION AUDIT  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Purpose

Identify which current executable components can feed a future production GRI Engine, which are historical stage runners/evidence packages, and which evidence paths still have incomplete executable provenance.

This inventory does not create a production Engine and does not change frozen science.

## 1. Reusable computational primitives currently in repository

### `src/tool_feasibility_kernel.py`

Current reusable primitives include:

- deterministic SHA-256-derived seed generation;
- column centering;
- marginal and row permutations;
- sample-space modal decomposition;
- normalized eigenvalues, entropy, effective rank, participation ratio, `S_spec`, mode-feature contributions;
- linear CKA;
- principal angles;
- covariate residualization;
- Spearman/module coupling;
- semantic label permutation effect;
- cross-validated modal predictability;
- permutation calibration.

**Production caution 1:** the generic `_matrix` validator rejects all non-finite values. Stage A/C1 later established explicit source-missingness semantics. Therefore this helper cannot simply become the universal production input path without a declared modality-specific missingness layer.

**Production caution 2:** `predictability_permutation_calibration` still emits `candidate_autonomy_score`. F4 subsequently retired regulatory autonomy as an independent candidate coordinate because it was redundant with ordinary predictive dependence/shared-private structure. The function may remain historical/qualification code, but production output must not expose autonomy as an admitted independent coordinate unless a new version re-earns it.

**Disposition:** `REUSABLE_PRIMITIVE_WITH_SCOPE_WRAPPER_REQUIRED`.

### `src/module_network.py` and `src/module_network_accel.py`

Current functionality includes:

- explicit gene finite-coverage eligibility;
- pairwise-complete correlation handling;
- finite-value z-scoring with standardized missing cells placed at zero after centering;
- Hallmark/module eigengenes;
- `Cin,pair`, `Cin,PC1`, and `Cout` metrics;
- mapped-gene support rules.

The docstring explicitly distinguishes source missingness from zero expression and does not emit a chi or composite criticality score.

**Disposition:** `REUSABLE_STAGE_A_PRIMITIVE`, subject to accelerated/reference equivalence qualification in the production path.

### `src/run_stage_b1.py`

Current functionality includes:

- sample/patient context construction;
- explicit ABSOLUTE purity primary/called filtering;
- leukocyte matching;
- deterministic sample/context permutations;
- finite-row covariate residualization;
- context-specific module effect summaries.

**Production caution:** B1 is a stage runner tied to current source schemas, not yet a general Engine API. Its two-covariate output must continue to be named purity/leukocyte projection, not complete composition adjustment.

**Disposition:** `REUSABLE_LOGIC_STAGE_RUNNER_NOT_PRODUCTION_API`.

### `src/coordinate_registry.py`

Current code defines a ten-gate `ChiCandidate` and explicitly rejects historical `CV/2` as chi.

**Production caution:** the generic G1-G10 gate vocabulary predates the consolidated v0.7.1 epistemic/output architecture. It remains a useful refusal primitive, but any production chi-admission interface must preserve exact/proxy/empirical epistemic class, dynamical licensing, and the current GRI fact that no biological chi has been admitted.

**Disposition:** `REUSABLE_REFUSAL_PRIMITIVE_NEEDS_SCHEMA_ALIGNMENT`.

## 2. Repository stage-runner families

The current repository tree contains executable families for:

- Stage A/A1.1 RNA architecture;
- Stage B1 context decomposition;
- Stage B2 genomic/RPPA source and analysis branches;
- C0 methylation source identity;
- C0.1 sample identity;
- C1A source/annotation/probe inventory;
- tool-feasibility F2/F3 known-truth and established-method comparison;
- legacy predictive P0 split/eligibility/D1/D2 preparation.

These are valuable evidence-lineage executables, but they are not automatically production Engine endpoints.

**Disposition:** `HISTORICAL_OR_DEVELOPMENT_STAGE_RUNNERS` until routed through a consolidated Engine entry point and qualified through that exact production path.

## 3. Stage C1 executable provenance

The completed Stage C1 scientific result is strongly provenance-bound through the returned execution package and repository freeze record, including exact SHA-256 identities for:

- `src/run_stage_c1.py`
- `src/stage_c1_core.py`
- `src/c1a_historical_rebuild.py`
- `src/windows_launcher.py`

The execution package is not being inferred from the current repository branch. Its byte identities are separately preserved in the returned release/provenance package.

**Disposition:** `EXTERNALLY_PRESERVED_EVIDENCE_EXECUTABLE`, not yet consolidated into a production Engine release.

## 4. Post-C1 sensitivity executable provenance

The post-C1 adversarial sensitivity v2.2 exists as a separately frozen read-only Windows package and was previously manifest-checked. It reconstructs the historical C1 state before executing adversarial sensitivity.

This is qualification code, not production Engine code and not P1 confirmation.

**Disposition:** `P0_Q_FROZEN_QUALIFICATION_PACKAGE`.

## 5. Legacy predictive P0 executable provenance gap

The repository preserves substantial P0 configs, preparation runners, audit artifacts, and FINAL_HOLDOUT results. However, the current branch does not expose an obvious complete checked-in executable chain for the later D3/D4/FINAL_HOLDOUT prediction evaluation.

A separate D4 recovery report establishes that local historical packages contained:

- `src/run_discovery_model.py`
- `src/run_replication.py`
- `tests/test_replication.py`

and that exact small scientific inputs were recovered by hash. It also records that **no complete repaired execution package was recovered automatically** at that recovery point.

Recovered historical source hashes include:

- pre-repair `run_discovery_model.py`: `b1d98f941599936d9332bd278cce72b4cc7c1784f0028b4baa688df881013e6a`
- pre-repair `run_replication.py`: `f6a02bb39f6cfedb8fd034b0f2ea3f0bb84dddff019c891c20a1725ee73efdbe`
- fixed-folder `run_replication.py`: `f2f2b1807e49523d99bb378f9a0b6ca1987f83b7dff7e26423642ee471420246`
- `tests/test_replication.py`: `20a512362192bab26f8373ca86212683ea8cb1ac75f32dd9be90403875094b55`

Current archival search did not recover an exact later P3-v2/FINAL_HOLDOUT execution source package from the File Library or current repository tree.

**Disposition:** `REPRODUCIBILITY_GAP_EXECUTABLE_CHAIN_PARTIAL`.

This does **not** erase the audited FINAL_HOLDOUT result. It means P2/R1-R2 claims must not pretend that the complete predictive execution chain is currently reconstructable from the checked-in repository alone.

### Required closure

1. preserve the D4 recovery report and known hashes;
2. search the user's local historical package locations only when needed, using exact filenames/hashes rather than broad manual hunting;
3. if later executable bytes are recovered, hash and bind them to the FINAL_HOLDOUT artifact lineage;
4. if not recoverable, state the calculation-reproducibility gap explicitly in the release and rebuild the production predictor from frozen scientific definitions only as a **new Engine implementation**, with equivalence tests against preserved outputs where possible;
5. never represent a reconstructed implementation as the lost historical bytes.

## 6. Scientific definitions versus implementation reuse

A future production Engine should be assembled around **frozen scientific behavior**, not around preserving every historical runner interface.

Allowed implementation consolidation may:

- factor common deterministic hashing/seeding;
- centralize input validation;
- centralize refusal codes;
- standardize result schemas;
- provide one Engine entry point;
- separate Atlas query from Engine inference;
- make Function/Limit outputs explicit.

It must not silently change:

- frozen C1 scientific quantities;
- missingness semantics;
- thresholds/admission rules that are scientifically committed;
- P0 historical outcomes;
- comparator definitions;
- claim ceilings.

Any equivalence-preserving refactor requires direct tests against preserved reference outputs.

## 7. Proposed future production module boundaries

Do not implement/freeze until sensitivity/comparator disposition, but the following separation is architecture-safe:

```text
gri_engine/
  input_contract.py
  provenance.py
  missingness.py
  module_structure.py
  modal_structure.py
  cross_layer_geometry.py
  context_projection.py
  reduction_adequacy.py
  admission_refusal.py
  function_map.py
  limit_map.py
  prediction.py
  output_schema.py

gri_tool/
  atlas_interface.py
  comparator_metadata.py
  report.py
```

The Engine must not require Atlas labels to construct basic measurements. The Tool layer may query a separately frozen Atlas after Engine inference.

## 8. Current highest-priority code risks before consolidation

1. **Missingness policy fragmentation:** generic feasibility kernel is finite-only while later Stage A/C1 has explicit biologically appropriate source-missingness handling.
2. **Retired output still in helper API:** `candidate_autonomy_score` exists in development code despite F4 retirement of autonomy as an independent coordinate.
3. **Stage-runner coupling:** many routines are source/stage-specific rather than one validated Engine interface.
4. **Predictive executable-chain incompleteness:** later P0/FINAL_HOLDOUT historical execution source is not fully recovered in the current repository/archive search.
5. **No production Atlas boundary:** current code does not yet enforce read-only, versioned, independence-graded Atlas queries.
6. **No production Function/Limit API:** v0.7.1A behavior is currently specified in control/schema artifacts, not implemented.
7. **No production mutation suite:** negative/mutation behavior is specified but not executable against a production entry point yet.

## 9. Current conclusion

The scientific program has enough reusable computation to justify consolidation, but it would be premature to call the current source tree the GRI Engine.

**Current code status:** `DEVELOPMENT_COMPONENTS_PRESENT / PRODUCTION_ENGINE_NOT_YET_CONSOLIDATED`.

The next safe code step after sensitivity/comparator disposition is to create a versioned production Engine wrapper around the surviving supported components, then prove equivalence/refusal behavior before P2 release qualification.