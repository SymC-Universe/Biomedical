# WORKING_INVESTIGATION.md

**Project:** Bio Chi Investigation  
**Status:** ACTIVE - P0-Q / Function + Limit Map / state-regime Limit Map development  
**Current authority:** SymC General Operations Manual v0.8.8 REVIEW, promoted by the principal investigator on 27 September 2026  
**Project branch:** `chi-bio-recovery-p0d-20260922`  
**Branch head at this record update:** `23645fcfacab8e14d0d53e19e240cf500c997f21`  
**Pull request:** #6, draft  
**Working manuscript:** PRIVATE / NOT OPEN in the public repository

## Current scientific state

The biological investigation currently preserves three project-local object labels inherited from the active Bio Chi branch:

- `chi_bio`: biological scalar instance/sublabel of program-wide lowercase chi, if licensed.
- `Chi_bio` / project-local capital-Chi label: biological modal/vector representation under the existing branch nomenclature.
- Bio Chi: biological conglomerate/system stability architecture.

No broad biological scalar, modal representation, or conglomerate/system architecture is admitted by the current evidence. The following narrower results remain live:

- Jaruszewicz-Blońska NF-kB supports a model-specific P0-Q oscillatory-carrier candidate with `chi_bio ~= 0.21311451897468006`; this is qualification evidence only, not broad admission.
- Independent D2FC2 NF-kB closed as `NON_IDENTIFIABLE_MULTIPLE_STABLE_COMPLEX_PAIRS`; a unique transported scalar was refused.
- Blum 2019 ERK B3 closed its unstimulated local-generator route as `REFUSE_LOCAL_GENERATOR_NONDIFFERENTIABLE_AT_SOURCE_EQUILIBRIUM`; no regularized or shifted-equilibrium rescue is licensed by that gate.
- The scalar Function/Limit Map therefore currently contains at least three qualitatively distinct cases rather than a universal scalar construction.

## GOM v0.8.8 alignment

The full v0.8.8 GOM was reviewed before continuation on 27 September 2026.

The following v0.8.8 controls are now active for this investigation:

1. This file is the mandatory live scientific-state record and must be updated immediately after each material scientific development or hold, before the next scientific action.
2. P0-N novelty-first prior-art conglomeration must be backfilled for this mature investigation before any new hypothesis-directed confirmatory experiment or confirmatory interpretation is advanced.
3. Because this project is Atlas-bearing, an A0 Prior-Art Conglomeration Atlas must also be backfilled from the auditable literature/search history before new confirmatory promotion.
4. Existing frozen computations may be inspected, reproduced, or mechanically repaired while that backfill is incomplete, provided no scientific endpoint, frozen representation, hypothesis, threshold, null, comparator, mapping, or interpretation rule is changed.
5. Failures, refusals, nulls, indeterminate outcomes, and representation-dependent behavior remain evidence and are not overwritten by later repairs.
6. Function Map and Limit Map are coequal outputs. A scalar refusal or failure can be a legitimate boundary result and does not force a replacement scalar.
7. Joint meaning among scalar, modal/component, and system/conglomerate organization remains a research target; no layer may be presumed sufficient merely because it is mathematically available.

### Notation hold

GOM v0.8.8 uses program-level capital `Χ` for the broader reconstructed stability architecture, whereas the existing Bio Chi branch uses project-local `Χ_bio / Chi_bio` for the modal/vector layer and Bio Chi for the conglomerate/system layer.

No notation is renamed in this record. Until the principal investigator resolves or supersedes that semantic overlap, continuation will use the neutral phrases **scalar layer**, **modal layer**, and **system/conglomerate layer** in new audit prose whenever the distinction matters. Existing frozen identifiers, filenames, result fields, and branch nomenclature remain unchanged.

This notation hold does not block source audits, failure diagnosis, provenance work, P0-N/A0 backfill, or reproduction of already-frozen analyses. It does block silently redefining a scientific object.

## Frozen and preserved evidence

### Jaruszewicz-Blońska Figure 8 / generator evidence

- Figure 8A nominal damped finite-window status: `PASS_DAMPED_COMPATIBLE`.
- Figure 8B limit-cycle finite-window status: preserved `FAIL_NATIVE_BEHAVIOR` under the frozen finite-window sustained-compatibility rule.
- Figure 8C relaxation finite-window status: preserved `FAIL_NATIVE_BEHAVIOR` under the frozen finite-window sustained-periodicity rule.
- Local-stability v0.4: `PASS_ALL_FROZEN_FIG8_CASES`.
  - Figure 8A equilibrium: STABLE.
  - Figure 8B equilibrium: UNSTABLE.
  - Figure 8C equilibrium: UNSTABLE.
- Six-mode descriptive inventory: four real modes plus one complex-conjugate pair in each stored Figure 8 generator; post-view descriptive evidence only.
- Figure 8A observability qualification: `PASS_P0Q_OSCILLATORY_MODE_OBSERVABILITY`; model-specific candidate only.

### Independent NF-kB transport

- D2FC2 v0.2 repaired execution run: `36042402642`.
- Disposition: `NON_IDENTIFIABLE_MULTIPLE_STABLE_COMPLEX_PAIRS`.
- Two stable complex-pair scalar candidates were present, approximately 0.5753 and 0.9337, while the frozen held-out empirical-frequency rule identified neither as uniquely transportable.
- The Jaruszewicz candidate is therefore not independently transported as a unique D2FC2 scalar.

### ERK limit case

- Blum B3 modal/local-generator run: `36043170485`.
- Disposition: `REFUSE_LOCAL_GENERATOR_NONDIFFERENTIABLE_AT_SOURCE_EQUILIBRIUM`.
- The refusal is preserved as a Limit Map result. No one-sided derivative, equilibrium shift, regularization, or alternate model topology may be introduced as a mechanical repair.

## Latest material development: Jaruszewicz same-system joint response gate

Frozen object:
`BIO_CHI/config/JARUS_JOINT_SCALAR_MODAL_SYSTEM_P0Q_FREEZE_v0_1.json`

Workflow:
`Bio Chi Jaruszewicz joint scalar-modal-system P0-Q v0.1`

Run:
`36044426805`

Head used by the run:
`9fd779c34cd8a8d9dd617ef581862286b00b2122`

Outcome:
**EXECUTION FAILURE BEFORE SCIENTIFIC TRAJECTORY ADJUDICATION**

Exact error:
`BIO_CHI_JARUS_JOINT_COMPLEX_PAIR_COUNT_0_0`

No result artifact was produced. This is not a negative biological result and is not a failed scientific prediction. It is currently classified as:

`RESOLVED_SCIENTIFIC_DEFINITION_CONFLICT_AND_STATE_REGIME_LIMIT`

### Why the failure is material

The frozen joint-response script linearizes the source model at `x_star = [1,0,0,0,0,0]` with `TNF = 0` and requires that generator to reproduce the already inherited complex pair and `chi_bio` candidate.

The earlier Figure 8 local-stability route that supplied the stored complex pair solved the frozen Figure 8 equilibria using `reduced(0,x,1)`, i.e. under `TNF = 1`, and then computed the Jacobian at the accepted positive root. Therefore the prior candidate and the newest joint-response freeze may not share the same equilibrium/input state.

The contradiction audit has now resolved this difference. The exact source equations show that `[1,0,0,0,0,0]` at `TNF=0` is a valid source-native equilibrium, but its local generator does not contain the inherited oscillatory pair. At that exact state, the TNF-dependent couplings are absent and the Jacobian has a real-mode structure; the previously qualified oscillatory carrier instead belongs to the `TNF=1` positive equilibrium used by the Figure 8A local-stability route.

Therefore run `36044426805` is preserved as a **scientific-definition conflict exposed by the frozen gate**, not a mechanical execution failure. Its requirement that the TNF-off baseline reproduce the TNF-on oscillatory carrier was false. No equilibrium swap or rerun is permitted as a mechanical repair. The result adds a state/regime-dependence boundary to the Function/Limit Map: the local carrier and any scalar derived from it are conditional on the operating state and cannot be assumed invariant across TNF-off and TNF-on equilibria.

## Active holds and promotion debt

- **P0-N:** CLOSED_FOR_CURRENT_RESIDUAL_QUESTION in `BIO_CHI/artifacts/P0N_NOVELTY_SYNTHESIS_v0_1.md`. Historical backfill only; no earlier result is retroactively prospective.
- **A0 Prior-Art Conglomeration Atlas:** CLOSED_FOR_CURRENT_RESIDUAL_TARGET in `BIO_CHI/artifacts/A0_PRIOR_ART_CONGLOMERATION_ATLAS_v0_1.md`.
- **Latest joint-response gate:** CLOSED_AS_STATE_REGIME_LIMIT. No rerun with a changed equilibrium, input state, mode identity, or scalar definition is licensed as a mechanical repair. A differently posed TNF-on joint test would be a new scientific object and requires a new prospective freeze after P0-N/A0 backfill.
- **Notation:** HOLD_FOR_SEMANTIC_RECONCILIATION only when a rename/redefinition becomes necessary. Neutral layer names may be used meanwhile.
- **Broad admission:** CLOSED for scalar, modal, and system/conglomerate layers.
- **Working manuscript:** remains private.

## Exact next actions

1. Execute a P0-D exploratory continuation of the native Jaruszewicz equilibrium/generator from TNF=0 to TNF=1 to map where real modes become a complex pair and whether mode multiplicity or stability changes across the input coordinate. This is Function/Limit mapping, not confirmation.
2. Preserve the TNF-off/TNF-on state-regime boundary without promoting a replacement scalar.
3. Use the resulting map only to formulate future prospective boundary tests; do not retune a confirmatory gate from it.
4. After exploratory mapping, identify untouched independent evidence capable of a P1 test. A new TNF-on joint response test on already-inspected Jaruszewicz Figure-8 evidence remains qualification, not independent confirmation.
5. Update this file before every subsequent material scientific action and continue mechanically where no scientific choice is required.

## Resume pointers

- `BIO_CHI/control/AUTORUN_CHECKPOINT.md`
- `BIO_CHI/control/WORK_QUEUE.json`
- `BIO_CHI/config/JARUS_JOINT_SCALAR_MODAL_SYSTEM_P0Q_FREEZE_v0_1.json`
- `BIO_CHI/src/run_jarus_joint_scalar_modal_system_p0q_v0_1.m`
- `BIO_CHI/config/JARUS_OSCILLATORY_MODE_OBSERVABILITY_P0Q_V01_RESULT_PIN.json`
- `BIO_CHI/config/JARUS_LOCAL_STABILITY_V04_RESULT_PIN.json`
- `BIO_CHI/config/JARUS_MODAL_INVENTORY_V01_RESULT_PIN.json`
- PR #6

## Development log

### 2026-09-27 - v0.8.8 full reload and live-state reconstruction

The complete 91-page SymC General Operations Manual v0.8.8 REVIEW was reloaded and reviewed before continuation. The active Bio Chi branch, PR #6, queue, checkpoint, current head, recent workflow runs, and current frozen Jaruszewicz joint-response gate were then audited.

Material findings:

- the branch had no mandatory `WORKING_INVESTIGATION.md`, so this live record was created before further scientific action;
- P0-N and A0 backfill artifacts were not present at the current branch head;
- the current project-local capital-Chi modal nomenclature overlaps semantically with the v0.8.8 program-level capital `Χ` architecture definition, so neutral layer labels are being used until a deliberate reconciliation is made;
- the latest Jaruszewicz same-system joint-response run `36044426805` failed before scientific output with `BIO_CHI_JARUS_JOINT_COMPLEX_PAIR_COUNT_0_0`;
- the failed gate's `TNF=0`, hard-coded `x_star` linearization does not obviously match the `TNF=1` accepted Figure 8 equilibrium route that supplied the inherited oscillatory pair, creating a material discrepancy that must be diagnosed before rerun;
- governance and reviewer smoke tests at the branch head remain passing.

No scientific endpoint, threshold, null, comparator, mode rule, equilibrium, mapping, or interpretation rule was changed during this reconstruction.


### 2026-09-27 - Jaruszewicz joint-gate contradiction resolved

The source-native equation audit resolved the failed joint-response gate without changing any frozen object.

Source facts:
- `species0 = [1,0,0,0,0,0]`;
- TNF is binary in the source, with `TNF=0` off and `TNF=1` on;
- at the TNF-off source state, every right-hand side evaluates to zero, so it is a valid equilibrium;
- the TNF-off linearization removes the TNF-driven IKK coupling and the feedback products vanish at the zero-background state;
- the resulting local generator has no nonreal conjugate pair under the frozen gate, exactly matching the observed `COMPLEX_PAIR_COUNT_0_0` failure;
- the earlier Figure 8 local-stability computation instead solved and linearized `reduced(0,x,1)` at the accepted positive TNF-on equilibrium.

Adjudication:
`RESOLVED_SCIENTIFIC_DEFINITION_CONFLICT_AND_STATE_REGIME_LIMIT`.

Scientific consequence:
the previously qualified Jaruszewicz oscillatory carrier and candidate scalar are operating-state dependent. They are not properties that can be transported unchanged from the TNF-on equilibrium to the source-native TNF-off equilibrium. This is retained as a Limit Map result and narrows the scalar claim. It also strengthens the need to investigate the modal and system/conglomerate layers jointly rather than treating a local scalar as the entire biological stability architecture.

No rerun, equilibrium substitution, threshold change, or carrier reselection was performed.


### 2026-09-27 - P0-N and A0 backfill closed for current residual target

GOM v0.8.8 novelty debt was reconstructed from the two completed deep searches and the outcome-blind/targeted source-qualification record.

Created:
- `BIO_CHI/artifacts/P0N_NOVELTY_SYNTHESIS_v0_1.md`;
- `BIO_CHI/artifacts/A0_PRIOR_ART_CONGLOMERATION_ATLAS_v0_1.md`.

P0-N disposition:
- established biology already includes recovery, memory, hysteresis, metastability, substrate-conditioned state behavior, NF-kB input/history dependence, ERK temporal encoding, and p53 representation/population caveats;
- none of those phenomena is claimed as novel here;
- current residual novelty is classified primarily as `NEW_INTEGRATION` + `NEW_BOUNDARY_TEST`, with `NEW_CONGLOMERATED_INFERENCE` retained only as a candidate until prospectively tested;
- the residual target is the domain of validity/failure of scalar, modal/component, and system/conglomerate representations under matched native conditions, plus later tests of whether substrate/carrier state predicts transitions among those domains.

The backfill does not retroactively change earlier exploratory provenance or make post-view results confirmatory.

### P0-D purpose tag - Jaruszewicz TNF operating-state continuation

**PURPOSE:** exploratory Function/Limit mapping of how the native equilibrium and local spectrum change as the source TNF input coordinate varies from 0 to 1.

**OPERATION:** solve the native six-state equilibrium across a fixed TNF grid using continuation plus independent residual checks; compute the complete six-mode centered-finite-difference Jacobian at each accepted equilibrium; record stability, real/nonreal mode counts, conjugate-pair identity where present, and candidate scalar values only where mathematically licensed.

**EXPECTED_INFORMATION:** identify whether the oscillatory carrier emerges only beyond a finite input/state transition, whether multiple complex pairs appear, and whether local stability or modal identity changes with TNF.

**DECISION ENABLED:** refine the state-regime Function/Limit Map and define what an untouched future boundary test would have to discriminate.

**EPISTEMIC CLASS:** P0-D exploratory only. No confirmatory admission, no threshold tuning to a desired transition, and no use of this map as untouched evidence in a later P1 test.


### 2026-09-27 - P0-D TNF continuation coarse-grid development

The first deterministic exploratory continuation used the exact published six-state Jaruszewicz equations and parameter values, a fixed TNF grid from 0 to 1 in increments of 0.01, nonnegative equilibrium solves with continuation plus fixed independent seeds, the complete six-mode centered-finite-difference Jacobian, and no target-driven adaptive search.

Material result:
- at exact `TNF=0`, the source-native equilibrium `[1,0,0,0,0,0]` has no nonreal pair and is nonhyperbolic in one local direction;
- at the sampled `TNF=0.01` through `0.06` equilibria, the local spectrum contains **two** complex-conjugate pairs;
- at sampled `TNF=0.07` through `1.00`, the spectrum contains **one** complex-conjugate pair;
- the continued positive-equilibrium branch is locally stable at every sampled `TNF>0`;
- at `TNF=1`, the exploratory calculation reproduces the stored Figure 8A equilibrium and oscillatory pair, including `chi ~= 0.213114519`.

Interpretation ceiling:
this is P0-D Function/Limit mapping only. The coarse-grid transition brackets are not promoted as bifurcation coordinates. The `TNF=0` numerical multistart root multiplicity from unconstrained least-squares is not interpreted because the source provides an exact equilibrium and the zero-input point is nonhyperbolic; the next implementation must pin the exact source equilibrium at zero rather than use numerical root multiplicity there.

Current exploratory pattern:
`NO_COMPLEX_PAIR -> TWO_COMPLEX_PAIRS -> ONE_COMPLEX_PAIR` as TNF operating state increases on the sampled native branch.

Scientific implication:
scalar availability and scalar uniqueness are separate operating-state properties. The local modal layer changes topology before the TNF=1 scalar candidate is reached, which strengthens the Function/Limit target and further rules out treating the Jaruszewicz candidate as a state-independent system constant.

Next exact action:
commit a reproducible P0-D script with the exact `TNF=0` source equilibrium pinned, rerun a denser **predeclared fixed grid** only to localize the two observed coarse-grid topology changes, and preserve all mode branches rather than selecting a preferred pair. No confirmatory threshold or claim will be created from that refinement.


### 2026-09-27 - Analytic-Jacobian cross-check of TNF spectral topology

The coarse P0-D spectral result was independently recomputed using an analytic Jacobian generated directly from the published six source equations, rather than the centered finite-difference Jacobian. The same material topology was recovered, so the observed modal multiplicity is not attributable to finite-difference error.

On the predeclared 0 to 0.1 grid with step 0.001:
- `TNF=0`: zero nonreal modes, exact source equilibrium, max real eigenvalue exactly 0;
- `TNF=0.001-0.002`: one complex-conjugate pair;
- `TNF=0.003`: two complex-conjugate pairs, with the second pair having very small imaginary magnitude;
- `TNF=0.004-0.009`: one complex-conjugate pair;
- `TNF=0.010-0.062`: two complex-conjugate pairs;
- `TNF>=0.063` through 0.1: one complex-conjugate pair.

At `TNF=0.062`, the second pair is close to the real axis; by `TNF=0.063` it is real. The dominant oscillatory pair remains stable throughout this sampled interval. These are grid-defined brackets, not bifurcation estimates.

A further fixed-grid refinement may localize the observed real/complex transitions for descriptive mapping only. It must not convert those coordinates into confirmatory thresholds or use outcome-driven adaptive optimization.


### 2026-09-27 - Fixed-window TNF topology refinement

Two predeclared fixed descriptive windows were evaluated with the analytic Jacobian:
- low-input window: `TNF=0..0.015`, step `0.0001`;
- upper transition window: `TNF=0.055..0.070`, step `0.0001`.

Observed grid brackets:
1. 0 -> 1 complex pair: `(0, 0.0001]`;
2. 1 -> 2 complex pairs: between `0.0020` and `0.0021`;
3. 2 -> 1 complex pair: between `0.0035` and `0.0036`;
4. 1 -> 2 complex pairs: between `0.0092` and `0.0093`;
5. 2 -> 1 complex pair: between `0.0621` and `0.0622`.

At transitions involving the second pair, its imaginary component is small near the bracket, consistent with a real/complex eigenvalue collision. No bifurcation class is assigned from this grid scan.

Current descriptive modal sequence over the sampled native equilibrium branch:
`REAL_ONLY at TNF=0 -> ONE_PAIR -> TWO_PAIRS -> ONE_PAIR -> TWO_PAIRS -> ONE_PAIR`.

Claim ceiling:
these coordinates are descriptive grid brackets only. They are not universal thresholds, not confirmatory boundaries, and not evidence that the same transitions occur in cells or independent NF-kB models.

Next action:
package the exact source equations, fixed grids, analytic-Jacobian construction, equilibrium residual gates, all eigenvalues, and transition-bracket output into a reproducible GitHub P0-D workflow and pin the resulting artifact. No further scientific interpretation is required before that mechanical packaging.
