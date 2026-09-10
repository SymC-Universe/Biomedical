# GRI Engine P2 qualification gap audit

**Date:** 2026-09-10  
**Status:** WORKING ENGINE-QUALIFICATION AUDIT  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 FINAL  
**Branch:** `gri-v071-protocol-integration-20260910`

## 0. Scope

This audit asks a narrow question:

> What still has to be demonstrated before the current GRI computational lineage may be treated as a versioned, reproducible, production-qualified GRI Engine under the v0.7.1 program architecture?

It does not alter Stage C1, P0, the post-C1 sensitivity freeze, or any biological interpretation. It does not itself validate the Engine.

The current codebase contains many scientifically useful and separately audited routines, but a collection of successful scripts is not automatically a production-qualified Engine. P2 requires the executable implementation of the GRI System Model to behave correctly under valid inputs, invalid inputs, boundary states, mutations, repeated execution, and fresh-environment reproduction, while emitting outputs whose meaning and provenance are explicit.

---

# 1. Existing strengths already present

The current repository and returned C1 package already provide several strong foundations for Engine qualification:

- deterministic seed namespaces are used in major frozen analyses;
- exact input and executable hashes are recorded;
- source identity is separated from processed-membership identity where required;
- checkpoints are hash-bound to frozen input/contract state;
- scientific and mechanical amendments were distinguished rather than silently merged;
- C1 writes atomically and retains large local heavy outputs with sidecar identities;
- C1 v2.2 has a regression/contract suite reported as 32/32 PASS;
- F2 synthetic known-truth testing challenged the general mathematical kernel across 11 prespecified behaviors and retained the nonlinear-only failure;
- F3 compared relevant structural capabilities with simple baselines and established methods including AJIVE and MOFA2;
- the project already contains explicit admission/refusal language and retained negative states;
- P0 partitions and FINAL_HOLDOUT identities were frozen and independently audited;
- the current post-C1 sensitivity package contains a strict 6,400-key state-equivalence gate before adversarial sensitivity execution.

These features mean P2 should be a consolidation and qualification problem rather than a ground-up rewrite.

---

# 2. Primary P2 gap: there is not yet one frozen production Engine object

The current executable scientific lineage is distributed across multiple scripts and historical stages, including:

- Stage A/A1.1 RNA architecture routines;
- B1 context adjustment;
- B2 genomic/RPPA routines;
- general feasibility kernel functions;
- C0/C0.1/C1A data gates;
- Stage C1 execution code;
- P0 prediction-stage code;
- post-C1 sensitivity code.

That lineage is auditable, but a user or external reproducer cannot yet point to one immutable object and say:

> This exact version is the GRI Engine, these are its admitted inputs, these are its outputs, these are its refusal states, and these tests qualify those behaviors.

### Required closure

Create a versioned Engine release only after current internal sensitivity/comparator disposition, with:

1. a single Engine version identifier;
2. a release manifest covering every executable/static file required for Engine operation;
3. an explicit System Model version implemented by that Engine;
4. a machine-readable input schema;
5. a machine-readable output schema;
6. explicit capability and refusal registry;
7. exact dependency/runtime specification;
8. deterministic seed/version behavior;
9. immutable release hash ledger;
10. one entry point or documented API that routes to the required internal modules without changing their frozen scientific meaning.

Do not create the production freeze until the current internal sensitivity/comparator work is dispositioned, because those results may legitimately narrow supported capability or required guardrails.

---

# 3. Input qualification and refusal gaps

A production Engine must refuse unsupported inputs deterministically rather than merely failing somewhere downstream.

## 3.1 Required explicit input classes

The future Engine must classify at least:

- valid supported input;
- missing required modality;
- insufficient sample support;
- duplicate/ambiguous sample identity;
- unsupported platform or unresolved platform mapping;
- excessive or undefined missingness state;
- unsupported feature/membership mapping;
- composition/context covariate unavailable where a requested output requires it;
- malformed dimensions or patient ordering;
- nonfinite state outside an explicitly bound missingness rule;
- unsupported nonlinear-only dependence request;
- request for temporal/causal/inheritance output from unordered static data;
- request for biological chi when no chi coordinate has been admitted;
- Atlas-required query when no qualifying Atlas version is supplied.

Each state must return a named refusal or `NOT_EVALUABLE` code instead of silently substituting data, dropping samples/features, or downgrading the requested task without disclosure.

## 3.2 Existing evidence

The project already has several concrete refusal precedents:

- C0 duplicate source roots were not arbitrarily selected;
- C1 promoter-core Hallmarks with insufficient mapping support were not substituted;
- F2 nonlinear-only capability failed and remained out of scope;
- P0 PCPG remained a stress case rather than being excluded;
- PAAD remained unevaluable in FINAL_HOLDOUT when frozen n=30 composition support was unavailable;
- C1 v2.1 originally hard-failed a zero-finite RNA gene rather than inventing a value, leading to the explicitly approved v2.2 rule before effect inspection.

These precedents should be promoted into production Engine tests.

---

# 4. Negative-test gap

Passing valid synthetic examples is insufficient for P2. The Engine must also demonstrate that known-bad and unsupported conditions do not generate apparently valid scientific outputs.

### Required negative tests

At minimum, create deterministic tests for:

1. patient-label permutation destroys patient-specific cross-layer evidence;
2. semantic-label permutation destroys label-specific evidence without falsely destroying purely global shared geometry;
3. pure measured confounding is reduced by the prescribed context attack and does not remain promoted as independent biology;
4. technical false concordance is exposed by the technical-mask/attack path where the synthetic condition is constructed to require it;
5. independent layers do not become falsely classified as globally shared;
6. nonlinear-only shared dependence produces `UNSUPPORTED_NONLINEAR_SCOPE` or equivalent, not a false calibrated pass;
7. insufficient Hallmark mapping produces structural refusal;
8. duplicate or ambiguous patient identity produces input refusal;
9. impossible composition-complete n produces `NOT_EVALUABLE`, not imputation or hidden sample substitution;
10. biological-chi request returns `CHI_NOT_ADMITTED` unless a future independently frozen version explicitly admits one;
11. temporal/inheritance request from unordered static data returns `TEMPORAL_EVIDENCE_REQUIRED` or equivalent;
12. Atlas-validation request with a non-independent reference family cannot be reported as independent validation.

These tests should operate through the same production Engine entry point used in real execution, not only through isolated helper functions.

---

# 5. Mutation-test gap

A mature release should prove that important guards fail when the implementation is deliberately corrupted.

### Required mutation families

At minimum, mutations should target:

- sample-order integrity check removed or inverted;
- patient-null permutation accidentally replaced by identity;
- label-null permutation accidentally replaced by identity;
- construction-null behavior weakened;
- technical-mask application disabled;
- context projection bypassed;
- missingness rule changed from centered-zero-information to raw zero expression;
- duplicate sample acceptance enabled;
- output epistemic-status field removed;
- biological-chi prohibition removed;
- unsupported nonlinear request incorrectly admitted;
- Atlas independence grade ignored;
- source/hash verification bypassed;
- deterministic seed namespace changed;
- result manifest generation disabled.

For each mutation, at least one required regression/qualification test must fail. A mutation that escapes the suite identifies a real qualification hole.

---

# 6. Repeatability and numerical-stability gap

The project uses deterministic seeds and exact hashes in many places, but the future Engine needs one release-level repeatability test.

### Required checks

1. same supported input + same Engine version + same Atlas version + same prediction record -> identical discrete classifications/refusals;
2. deterministic stochastic procedures -> identical RNG stream or explicitly bounded numerical equivalence;
3. floating-point summaries -> recorded tolerance by output class;
4. content manifests -> identical hashes where byte determinism is expected;
5. numerical equivalence tests -> explicit tolerance where library/platform variation prevents byte identity;
6. output ordering -> deterministic and schema-validated;
7. repeated clean execution -> no dependence on stale checkpoint/cache state.

The C1 S0 6,400-key reconstruction gate is an excellent precedent for this style of equivalence testing and should inform the production design.

---

# 7. Fresh-environment / clean-room gap

The current lineage has extensive internal reproducibility controls, but production qualification still needs a clean-room exercise in which no preexisting hidden working state is trusted.

### Required clean-room sequence

1. start from a frozen Engine release/archive or commit;
2. verify release manifest before execution;
3. install the documented dependency set in a fresh environment;
4. acquire or mount authorized external data separately;
5. verify source identities before analysis;
6. execute the Engine without importing old WORKING_STATE/checkpoints unless the test is specifically a resume test;
7. reproduce a frozen benchmark/synthetic qualification set;
8. reproduce at least one real-data non-confirmatory reference computation from source to final machine-readable outputs;
9. compare outputs with the expected semantic and numerical tolerances;
10. archive environment/version/OS/runtime metadata and output hashes.

A second machine/environment is preferred for the final P2 claim because repeatedly executing the same code on one workstation does not supply computational independence.

---

# 8. Resume/checkpoint qualification gap

Because GRI handles very large matrices, resumability is part of scientific reliability rather than a convenience.

The production Engine should test:

- interruption after a completed atomic checkpoint;
- interruption during an uncheckpointed write;
- restart from a valid checkpoint;
- rejection of a checkpoint whose input hash changed;
- rejection of a checkpoint whose Engine/System Model version changed incompatibly;
- deterministic migration only when an explicit equivalence gate proves the new version is a no-op for completed calculations;
- corruption detection through sidecar/manifest mismatch;
- no double counting or skipped resamples after restart.

The C1 v2.1/v2.2 migration records provide useful precedents but should not be assumed to qualify every future Engine path automatically.

---

# 9. Output-schema gap

The future GRI Engine should not output one generic `PASS` or one generic stability score.

A minimum machine-readable output should separate:

```text
measurement_status
system_model_version
engine_version
atlas_version
input_provenance
scalar_outputs
modal_outputs
conglomerate_outputs
cross_component_outputs
reduction_adequacy
context_attack_results
atlas_comparison
classification_state
refusal_state
prediction_record_id
prediction_result
epistemic_status
uncertainty
claim_ceiling
failure_boundary
warnings
output_manifest
```

Important rules:

- `atlas_version` may be null when no Atlas comparison is requested;
- `prediction_record_id` must be null unless a frozen prediction record exists;
- `prediction_result` must never be populated merely because a descriptive association exists;
- `mechanism` is not inferred automatically from structural agreement;
- `biological_chi` remains absent or explicitly `NOT_ADMITTED` in the present model version;
- a refusal state is a scientifically valid output, not a runtime error unless execution integrity itself failed.

---

# 10. Atlas-interface gap

The current code does not yet constitute a qualified read-only interface to an independently versioned Regulatory Substrate Atlas.

The future Engine/Tool boundary should enforce:

1. Engine calculations complete without Atlas values tuning their internal thresholds;
2. Atlas is supplied by explicit version/hash;
3. Atlas query returns reference/context information separately from Engine inference;
4. each decisive Atlas reference carries an independence grade;
5. `NON_INDEPENDENT_FOR_ENGINE_VALIDATION` entries may be descriptive but cannot satisfy an independent-validation requirement;
6. missing Atlas match is allowed and reported as `NO_ATLAS_MATCH`, not forced to nearest favorable reference;
7. Atlas changes require a version change and do not silently alter Engine rules.

---

# 11. Comparator-interface gap

A predictive Engine release should expose the comparator identity used for any claimed added value.

For the current internal P0 lineage, the established comparison is not capacity matched. Therefore the production Engine cannot encode a blanket statement such as `HALLMARK_ARCHITECTURE_SUPERIOR` from those results.

Future external predictive qualification must record:

- scientific comparison question;
- native comparator search/selection procedure;
- chosen comparator and version;
- feature/capacity matching rationale where relevant;
- tuning/evaluation split;
- exact metric and decision rule;
- failure result if the native comparator equals or beats GRI.

If no defensible native comparator exists after a frozen good-faith search, use the protocol state `NO_NATIVE_COMPARATOR`; do not invent a weak benchmark.

---

# 12. Capability-to-prose synchronization gap

The repository currently contains historical documents written at different stages of the investigation. Once a production Engine version is frozen, every user-facing capability description must be synchronized to the actual qualified behavior.

Before release, search and disposition stale language involving at least:

- biological chi;
- damping/criticality/exceptional points in cancer;
- `CV/2`;
- causal methylation-to-RNA regulation;
- temporal inheritance/recovery;
- universal pan-cancer selector;
- robust Hallmark-semantic sharing;
- regulatory autonomy as an independent coordinate;
- novelty of CKA/global geometry/shared-private modes;
- clinical or diagnostic claims;
- capacity-matched predictive superiority.

Freshly rewritten prose is itself unverified until checked against the executable release and claim ledger.

---

# 13. P2 qualification matrix

| Qualification area | Present evidence | Current state | Required closure |
|---|---|---|---|
| Exact source/executable provenance | Strong C0/C1/P0 hashes and manifests | **STRONG** | Consolidate at Engine release level |
| Deterministic core calculations | Strong precedent | **STRONG/PARTIAL** | One Engine-level repeatability suite |
| Valid-input regression | Many stage-specific tests | **SUBSTANTIAL** | Route through production Engine entry point |
| Known-truth behavior | F2 10/11, retained nonlinear failure | **SUBSTANTIAL** | Re-express supported/unsupported behavior in production release |
| Explicit refusal states | Strong scientific precedents | **PARTIAL** | Machine-readable production refusal registry/tests |
| Negative tests | Present in pieces | **PARTIAL** | Complete production negative suite |
| Mutation tests | Not established for GRI production release | **OPEN** | Add required mutation families and prove test sensitivity |
| Resume/checkpoint integrity | Strong C1 precedent | **SUBSTANTIAL** | Generalize and qualify production resume behavior |
| Fresh-environment reproduction | Internal lineage is reproducible but not final clean-room | **OPEN** | Fresh environment/machine reproduction |
| Output schema / epistemic separation | Present conceptually in docs | **OPEN/PARTIAL** | Machine-readable release schema |
| Atlas read-only interface | Not yet built | **OPEN** | Versioned Atlas interface + independence enforcement |
| Comparator binding | Structural comparators strong; predictive capacity gap unresolved | **PARTIAL** | Comparator metadata + future frozen external native comparator |
| Capability/prose synchronization | Historical docs contain superseded claims | **OPEN** | Release-wide semantic audit |
| Immutable release packaging | Stage-specific manifests exist | **PARTIAL** | One production Engine archive/commit + manifest + semantic audit |

**Current P2 verdict: NOT QUALIFIED YET.**

This is expected. The project has substantial qualification infrastructure, but the production Engine object has not yet been consolidated or clean-room qualified.

---

# 14. Recommended closure order

The shortest defensible route is:

1. finish/disposition post-C1 sensitivity v2.2;
2. resolve or explicitly close the historical equal-dimensional comparator provenance gap;
3. freeze the supported GRI System Model scope after those internal attacks;
4. consolidate the existing computation into a versioned GRI Engine release without changing the supported scientific definitions;
5. implement machine-readable refusal/output schemas;
6. run production negative and mutation suites;
7. run deterministic repeatability/resume tests;
8. perform fresh-environment clean-room reproduction;
9. build/version the independent Regulatory Substrate Atlas interface;
10. freeze external MFR-14 prediction + native comparator + Atlas/System Model/Engine versions;
11. execute untouched external confirmation.

Steps 4-8 are P2 Engine qualification. Step 9 creates the Tool-level independent reference layer. Steps 10-11 are required before predictive qualification.

---

# 15. Parallel work classification

### Safe to continue now while post-C1 sensitivity runs

- inventory the current code paths that would feed the consolidated Engine;
- draft the machine-readable output/refusal schema;
- design negative and mutation tests against already supported/refused behaviors;
- prepare clean-room instructions;
- prepare Atlas interface contract;
- search for stale capability prose and comparator provenance.

### Wait for sensitivity/comparator disposition before freezing

- exact production System Model scope;
- exact production Engine release version;
- any threshold or admission change motivated by sensitivity results;
- any new biological coordinate;
- any new comparator scientific design;
- any external MFR-14 prediction record.

This preserves the v0.7.1 rule that documentation/audit work may proceed autonomously while scientific changes and confirmatory freezes require explicit review.