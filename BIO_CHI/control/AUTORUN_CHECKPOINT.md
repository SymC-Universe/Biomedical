# Bio Chi autonomous continuation checkpoint

**Created:** 22 September 2026  
**Status:** ACTIVE  
**Branch:** `chi-bio-recovery-p0d-20260922`  
**Authority:** SymC General Operations Manual v0.8.4  
**Purpose:** allow continuation after chat, polling, workflow, timeout, or tool interruptions without requiring the user to push the project forward manually.

## Non-negotiable resume rule

Every continuation run must:

1. read this checkpoint first;
2. verify branch/head and relevant workflow/search/artifact state;
3. continue from the first incomplete item in **Current execution queue**;
4. perform all safe mechanical work that does not alter a frozen scientific decision;
5. update durable GitHub records before ending;
6. preserve failures, nulls, refusals, indeterminate states, and representation dependence;
7. never retune a cohort, endpoint, state representation, threshold, seed, null, comparator, mapping, or boundary because of a result;
8. keep working manuscript text private;
9. treat timers, polling limits, queued jobs, stale sessions, and packaging failures as mechanical interruptions, not scientific stop conditions;
10. resume from the latest committed checkpoint after any such interruption.

## Mechanical continuation authority

Without asking the user again, continuation runs may:

- search and audit literature;
- inspect source metadata and public dataset structure;
- verify accessions, file identities, hashes, licenses, and schemas;
- write or improve acquisition scripts;
- write tests and known-bad fixtures;
- run synthetic/known-truth validation;
- execute already-frozen analyses;
- rerun mechanically failed workflows when the scientific contract is unchanged;
- repair syntax, packaging, path, environment, dependency, or schema errors that do not change science;
- regenerate figures/tables from frozen results;
- update manifests, provenance, reviewer navigation, claim maps, and ledgers;
- create checkpoints and machine-readable status records;
- narrow claims automatically when frozen evidence fails;
- document NOT_EVALUABLE / INDETERMINATE outcomes.

## Scientific stop conditions

Stop and surface the issue only when proceeding would require one of the following:

- selecting or changing a scientific hypothesis after viewing the decisive result;
- changing a frozen endpoint, cohort, threshold, boundary, state representation, null, comparator, or mapping;
- choosing among materially different native biological models when the choice changes interpretation;
- opening decisive evidence before required freeze/independence controls are complete;
- redefining χ, Χ_bio, Bio Chi, or an inheritance criterion;
- overriding a failed/refused result;
- making a publication-level causal or universal claim not already licensed;
- a source defect that makes the frozen task scientifically non-evaluable and cannot be repaired mechanically.

## Current execution queue

### Q0 — governance and reproducibility spine
**STATUS: COMPLETE / MAINTAIN**

### Q1 — literature collision and candidate expansion
**STATUS: OPENING COLLISION COMPLETE / TARGETED UPDATES CONTINUE**

### Q2 — dataset eligibility and source qualification
**STATUS: ACTIVE / SOURCES FROZEN; QUALIFICATION CONTINUES**

### Q3 — known-truth / qualification system
**STATUS: PENDING Q2**

### Q4 — cancer recovery system
**STATUS: PENDING Q2**

### Q5 — χ_bio scalar track
**STATUS: ACTIVE NATIVE-BEHAVIOR EXECUTION / NO ADMISSION**

### Q6 — Χ_bio modal track
**STATUS: PENDING NATIVE-BEHAVIOR + Q2/Q3**

### Q7 — Bio Chi conglomerate track
**STATUS: PENDING Q3/Q4/Q6**

### Q8 — Stability Inheritance biological test
**STATUS: PENDING CARRIER-QUALIFIED DATA**

### Q9 — manuscript
**STATUS: NOT OPEN / PRIVATE**

## Completion condition for this checkpoint

This checkpoint remains ACTIVE until:
- Q1-Q2 yield a qualified testbed set;
- at least one known-truth/qualification path and one cancer path are dispositioned;
- χ_bio, Χ_bio, and Bio Chi each have a supported or refused status;
- the cross-level relation has been tested prospectively;
- all promoted results have reproducible GitHub paths and immutable provenance.

A polling timeout, chat timeout, workflow queue, or interrupted tool call never satisfies a stop condition.

## Durable history retained

- Public reproducibility spine established under `BIO_CHI/`.
- Draft PR **#6** opened: `WIP: Bio Chi P0-D recovery, modal and conglomerate investigation`.
- Working manuscript remains private.
- Opening literature collision completed; broad searches are complete and literature work is targeted-only.
- External GEO/S1 source freeze completed and pinned.
- Jaruszewicz S1 Code archive/member hashes frozen.
- Initial untouched-source runtime failure preserved; one MATLAB API compatibility repair was frozen and audited rather than hidden.

## Resume update — 23 September 2026 05:34 CDT

**Verified state**
- PR #6 remains the active draft Bio Chi PR on branch `chi-bio-recovery-p0d-20260922`.
- The two Undermind deep searches remain COMPLETE; no broad literature rerun is warranted.
- Machine-readable queue has been advanced to Q5 native-behavior execution while retaining Q2 qualification and manuscript privacy.
- No χ_bio, Χ_bio, or Bio Chi quantity has been constructed.

**Native-model progress completed this run**
- MATLAB compatibility reproduction run **35836946074** is durably pinned in `BIO_CHI/config/JARUS_MATLAB_COMPAT_PIN_v0_1.json`. It establishes executable model recovery after exactly one documented API repair, not untouched-source reproduction and not χ_bio admission.
- Before reviewing target behavior output, the authors-native behavior targets were prospectively frozen in `BIO_CHI/config/JARUS_NATIVE_BEHAVIOR_FREEZE_v0_1.json`:
  - Figure 8A nominal damped regime;
  - Figure 8B limit-cycle regime with `a2=0.02`, `c5a=0.00001`, `i1a=0.0001` s^-1;
  - Figure 8C relaxation-like regime with `a2=0.01`, `c5a=0.00001`, `i1a=0.0001` s^-1.
  No post-view damping threshold was introduced.
- Native output capture v0.1 run **35848534891** completed PASS with 7 figures and 42 numeric line series. Because v0.1 lacked authored semantic metadata, no positional biological mapping was inferred.
- Native output capture v0.2 run **35848998108** completed PASS and added authored axis semantics. Artifact **10745210753**, digest `sha256:c084a415e60a339e9703a0591c15c16d5feb0cb47251b6e7a1c824c7b2327ab8`. It confirms each published-driver figure contains the authored axes TNF, IKK_a, free nuclear NF-kappaB, A20, free cytoplasmic IkappaBalpha, and IkappaBalpha_t. Pin: `BIO_CHI/config/JARUS_NATIVE_OUTPUT_CAPTURE_PIN_v0_2.json`.
- Source-structure audit run **35849088543** completed PASS. Artifact **10744627896**, digest `sha256:88eef313259e4237facf816b47d2e38de21023e1f11d30d8009f3793876264b3`. Pin: `BIO_CHI/config/JARUS_SOURCE_STRUCTURE_PIN_v0_1.json`.
- The source audit resolved a key execution ambiguity: the supplied `run_simulate_reduced.m` driver executes seven protocol figures (continuous, five pulse protocols, on-off), but it does **not** encode the Figure 8 parameter-override regimes. Therefore the seven captured figures are not being relabeled as Figure 8A-C.
- The paper/code nominal parameter values remain explicitly preserved, including the known paper-rounding discrepancy; executable source values control reproduction and no silent reconciliation is allowed.

**New prospective execution gate**
- `BIO_CHI/config/JARUS_FIG8_EXECUTION_FREEZE_v0_1.json` freezes the next Figure 8 execution before outcome review: MATLAB R2023b, the pinned Reduced2023 equations, `ode23s`, the authors supplied initialization/equilibration helper, one continuous TNF pulse beginning at 1 h, 9 h nominal and 30 h B/C windows, exact paper parameter overrides, no behavior classification, no damping threshold, no mode selection, and no χ/Χ construction.
- Frozen case preparation and execution code has been committed:
  - `BIO_CHI/src/prepare_jarus_fig8_cases.py`
  - `BIO_CHI/src/jarus_fig8_execute.m`
  - `.github/workflows/bio-chi-jarus-fig8-execution.yml`
- Figure 8 trajectory execution run **35849437099** was queued at checkpoint time. This run is execution/provenance only; it cannot classify the trajectories or license χ_bio.

**Exact next safe resume**
1. Inspect run **35849437099**. If it fails mechanically, preserve the failure and repair only the execution layer under the frozen contract.
2. If it passes, pin the artifact/hashes and inspect all three frozen trajectories without changing parameters or windows.
3. Before calling any trajectory damped/sustained/relaxation-like or computing modal poles, freeze a separate adjudication/stability method. Do not create a post-hoc amplitude threshold.
4. Reproduce the authors' native behavior claim first; only after that may the Q5/Q6 modal-generator analysis ask whether a coherent χ_bio coordinate exists.
5. Continue Q2 source/testbed qualification in parallel when it does not cross the evidence firewall.
6. Preserve all nulls/failures/refusals and keep working manuscript text private.
