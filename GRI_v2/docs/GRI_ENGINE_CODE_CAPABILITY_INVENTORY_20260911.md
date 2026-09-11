# GRI Engine code-to-capability inventory

**Date:** 2026-09-11  
**Status:** WORKING P2 CONSOLIDATION INVENTORY  
**Protocol:** v0.7.1 + v0.7.1A

## Purpose

Map the current repository's executable scientific components to the future consolidated GRI Engine without changing any frozen scientific definition. This is an inventory, not a production release.

## Current executable lineages

### Input/source qualification

- `src/probe_stage_c0_methylation.py`
  - methylation source discovery/probing
  - future role: input provenance and source qualification

- `src/validate_stage_c0_cache.py`
  - source/cache identity validation
  - future role: input integrity guard

- `src/run_stage_c0_1_sample_identity.py`
  - one-to-one sample identity / duplicate-root handling
  - future role: sample-identity admission/refusal

- `src/fetch_stage_c1a_sources.py`
- `src/export_stage_c1a_annotation.R`
- `src/run_stage_c1a_probe_inventory.py`
  - annotation/source/probe mapping
  - future role: annotation/feature-support gate

### RNA within-layer architecture

- `src/module_network.py`
- `src/module_network_accel.py`
- `src/run_stage_a1_1.py`
  - within-Hallmark correlation, PC1 structure, between-Hallmark coupling, fixed-n calibration
  - future role: RNA conglomerate/modal context; any production inclusion must preserve current claim ceiling

### Context adjustment

- `src/run_stage_b1.py`
- `src/run_stage_b1_windows.py`
- `src/summarize_stage_b1.py`
  - purity/leukocyte projection and context comparison
  - future role: measured-context attack, explicitly not comprehensive deconvolution

### Orthogonal context layers

- `src/run_stage_b2_rppa.py`
- `src/run_stage_b2_genomic.py`
- `src/run_stage_b2_genomic_resume.py`
  - RPPA and genomic integration/context
  - future role: development/Atlas context unless separately qualified for production inference

### General cross-omic mathematical kernel

- `src/tool_feasibility_kernel.py`
  - global geometry, subspaces, same-module coupling, projection, prediction-related primitives
  - future role: core Engine mathematical library
  - qualification constraint: global geometry/modal decomposition are established primitives, not novelty claims

### Known-truth and comparator qualification

- `src/run_tool_feasibility_f2.py`
- `src/run_tool_feasibility_f2_repaired.py`
- `src/run_tool_feasibility_f3_simple.py`
- `src/run_tool_feasibility_f3_established_python.py`
- `src/run_tool_feasibility_f3_divas.R`
- `src/f3_established_runtime_compat.py`
  - future role: benchmark/qualification harness, not runtime oncology inference

### Prediction lineage

- `src/build_tool_prediction_p0_split_manifest.py`
- `src/run_tool_prediction_p0_eligibility.py`
- `src/run_tool_prediction_p0_d1_discovery_source.py`
- `src/run_tool_prediction_p0_d2_rna_target.py`
  - plus frozen configs/docs for D3/D4/P3-v2 and FINAL_HOLDOUT
  - future role: evidence lineage and candidate production prediction module after external comparator/P1 qualification
  - current status: internal predictive evidence only

### Stage C1 biological execution

The completed C1 v2.2 execution package was external/local relative to the repository lineage and is hash-bound by the returned record. Repository files include the frozen C1 contract/config and implementation concretization.

Future role:

- preserve C1 as immutable evidence lineage;
- extract reusable supported calculations into the consolidated Engine only if semantics and numerical equivalence are demonstrated;
- do not make the future Engine depend on historical C1 WORKING_STATE as hidden mutable input.

### Post-C1 sensitivity

The post-C1 adversarial sensitivity v2.2 package remains a separate frozen P0-Q qualification run using completed C1 state read-only.

Future role:

- informs supported capability/limits after disposition;
- not part of the production Engine runtime by default;
- selected stable diagnostics may become Engine outputs only after explicit scope freeze.

## Future consolidated Engine modules

The current code can be reorganized conceptually into these production modules:

1. `input_gate`
   - source identity
   - sample identity
   - feature/annotation support
   - modality/platform validation
   - missingness admission

2. `within_layer`
   - scalar spectral organization where admitted
   - modal/eigenspectrum structure
   - module/conglomerate organization

3. `cross_layer`
   - global patient geometry
   - principal-angle/subspace diagnostics
   - patient-specific module coupling
   - semantic-label specificity as a separate layer

4. `context_attacks`
   - purity/leukocyte projection
   - technical-mask track
   - additional prospectively qualified nuisance attacks

5. `reduction_adequacy`
   - scalar adequacy
   - leading-mode dominance
   - null-floor/headroom diagnostics
   - identifiability and support thresholds

6. `admission_refusal`
   - explicit supported/partial/refused/not-evaluable decisions

7. `function_limit_map`
   - Function Map output
   - Limit Map output
   - `WORKS_HERE`, `STOPS_WORKING_HERE`, `NOT_KNOWN_HERE`

8. `atlas_interface`
   - read-only query against explicit Atlas version/hash
   - pathway-specific independence metadata
   - `NO_ATLAS_MATCH` permitted

9. `prediction`
   - only activated with a frozen prediction record
   - binds comparator identity, metric, uncertainty, falsifier, and epistemic state

10. `provenance_release`
    - System Model/Engine/Atlas versions
    - input/output hashes
    - environment
    - seed namespace
    - semantic manifest

## Components that must not silently enter production

- historical `CV/2` biological chi;
- rank-as-time inference;
- nonlinear-only calibrated coverage;
- regulatory autonomy scalar as independent novelty coordinate;
- universal/raw Delta_CKA scalar bridge;
- strong general Hallmark semantic promotion;
- clinical/causal/treatment claims;
- automatic temporal inheritance from static data;
- current TCGA Atlas rows as independent validation of the same Engine.

## Consolidation risks

1. **Semantic drift:** helper functions reused under new names may be described more strongly than their historical evidence.
2. **Hidden-state dependence:** C1/local cache paths may accidentally become implicit runtime requirements.
3. **Duplicated scientific logic:** multiple stage scripts may implement closely related transforms differently.
4. **Validation drift:** tests may exercise helper copies rather than the future production entry point.
5. **Version ambiguity:** current files span different historical stages and are not one immutable Engine release.
6. **Output collapse:** a unified API must not compress distinct scalar/modal/conglomerate/refusal states into one score.

## Safe next engineering actions

Before scientific scope freeze:

- define production API/schema without choosing new scientific thresholds;
- identify duplicate implementations of the same transform and compare numerically;
- create wrappers around existing supported code rather than rewriting algorithms prematurely;
- draft refusal codes and validate that every unsupported request maps to one;
- prepare known-truth/mutation harnesses against the wrapper interface;
- ensure Atlas interface is read-only and optional for Engine measurement/inference;
- create a capability-description index.

## Freeze condition

Do not declare a production Engine version until the post-C1 sensitivity and comparator-provenance issues are dispositioned because they may narrow which diagnostics/claims are safe to expose. The consolidation work can proceed; the scientific capability freeze cannot.