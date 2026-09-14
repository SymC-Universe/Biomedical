# NSD post-P0-D closure audit under General Protocol v0.8.0

**Date:** 2026-09-14  
**Status:** P0-D CLOSURE AUDIT COMPLETE; P1 REMAINS CLOSED  
**Branch:** `neural-stability-dynamics-phase0d-v0.2-protocol-v0.7.1` (historical branch identifier)  
**Current protocol authority:** General Cross-Project Research Protocol v0.8.0, `Definitive Active Baseline`

## 1. Purpose

This audit closes the non-computational bookkeeping required after P0-D22 and P0-D23 and after repair of the stale protocol-authority regression test. It does not change scientific thresholds, estimators, solvers, comparator definitions, Atlas coordinates, frozen assumptions, or historical dispositions.

P0-D is treated as discovery / functional-and-limit mapping. This audit determines which objects, if any, are mature enough to be **proposed** for claim-specific P0-Q qualification. Proposal eligibility is not admission, confirmation, or a P1 freeze.

## 2. Mechanical closure

The only current-head mechanical blocker was a stale protocol-baseline assertion in `tests/test_protocol_v071a_compliance.py`. The scientific code compiled and the remaining regression suite passed; the stale test still required historical v0.7.1/v0.7.1A wording after `PROTOCOL_BASELINE.md` had legitimately advanced to v0.8.0.

The test was repaired at commit `adeb6f4281dc7d880f9715b931c4104292c8ded0` to validate:

- General Cross-Project Research Protocol v0.8.0 as current authority;
- `Definitive Active Baseline` status;
- preservation of the prior v0.7.7 pointer as historical lineage;
- preservation of historical runs, artifacts, freezes, failures, survival states and evidence tiers;
- the documented v0.7.8 lineage-artifact gap;
- unchanged P0-D/P0-Q and P1-closed semantics.

No scientific setting changed.

The resulting `NSD Phase0D v0.2 P0 validation` workflow run `34843463223` (run #226) completed successfully and uploaded:

- artifact ID `10346933443`;
- artifact name `nsd-phase0d-v02-p0-qualification`;
- SHA-256 `dbbf8e0d1a0d4509a1868aaa859c5d81c1f6caa475fc9fd6b18c3e83eb7d0cb3`.

Therefore the previous runs 224/225 are superseded mechanical failures and no recovery chain is currently stopped.

## 3. Function Map / Limit Map balance

### Function-side evidence retained

P0-D11 through P0-D21 established bounded functioning relationships including:

- conglomeration as directed coupled interaction rather than arithmetic pooling;
- separation of participation, observability and identifiability;
- branch lineage, finite-sample uncertainty and population-recoverability distinctions;
- reorganization of embedded/global dynamics under reciprocal coupling and feedback while local dynamics can remain fixed;
- exact hierarchy-preserving regrouping in the declared synthetic construction;
- separation of asymptotic return, recovery timescale and finite-time transient amplification;
- preservation of outer recovery under exact state-preserving grouping, with growing recovery error under lossy truncation as internal coupling strengthens.

These remain P0-D architecture results, not empirical neural confirmation.

### Limit-side evidence retained

The Limit Map is comparably populated and may not be suppressed:

- historical Phase 0C FAIL / FAIL / FAIL remains authoritative for that prospective lineage;
- Subspace DMD remains `FAILS_P0Q1`; SSI-COV remains `SURVIVES_P0Q1` at the level previously earned;
- finite-sample, observability, order/rank, model-adequacy and uncertainty limits remain explicit;
- P0-D22 demonstrates that estimated modal-chi and recovery-related coordinates can drift as observation geometry collapses while latent truth remains invariant;
- P0-D23 demonstrates conservative refusal but inadequate refusal specificity because all structural-switch targets and all stationary controls were refused overall.

**Audit disposition:** `FUNCTION_LIMIT_BALANCE = SATISFIED_FOR_P0D_CLOSURE`.

This does not imply equal numbers of positive and negative findings; it means functioning regions and failure/refusal/unknown regions are both explicitly preserved.

## 4. Foundational-dependency robustness activation review

### Identifiability / observation geometry

Activation conditions are met for a bounded downstream robustness requirement:

1. later recovery/chi interpretation materially depends on estimated modal structure;
2. P0-D22 demonstrates a scientifically legitimate vulnerability under invariant latent truth;
3. a proportional qualification opportunity exists before any P1 claim.

Therefore any recovery-related P0-Q proposal using estimated modal chi, spectral-abscissa-derived recovery, or related coordinates must include an explicit identifiability / observation-geometry control.

P0-D22 does **not** select its threshold. Its six observation scales are development evidence and cannot be reused as untouched proof of a later selected rule.

### Refusal specificity

P0-D23 does not support inheritance of the current refusal machinery as a qualified discriminator. Universal refusal among stationary controls creates a direct foundational vulnerability. The current rule may continue as a conservative development guard, but claim-specific refusal performance requires a new prospectively defined P0-Q construction with fresh calibration evidence.

**Audit disposition:**

```text
IDENTIFIABILITY_FOUNDATION = ROBUSTNESS_CHALLENGE_REQUIRED_IN_P0Q
CURRENT_REFUSAL_SPECIFICITY = NOT_MATURE_FOR_PROMOTION
```

## 5. Promotion-debt inventory

Open promotion debt includes:

- no empirical neural Atlas reference zone is frozen;
- no final recovery comparator identity is frozen;
- the prospective `chi ~ 1.2-1.3` note remains firewalled from tuning, binning, stopping and interpretation;
- no claim-specific identifiability/null-floor threshold has been prospectively frozen;
- refusal specificity is unresolved after P0-D23;
- the recovery framework remains synthetic/developmental and has not completed MFR-14;
- experimental-opportunity literature collision identifies a residual prospective question but does not certify novelty;
- no P1 system/seed/challenge/scoring freeze exists;
- no clinical, EEG diagnostic, treatment or predictive utility claim is licensed.

No debt is silently discharged by the successful branch validation.

## 6. Reproducibility and provenance audit

### Strongly preserved

P0-D22:

- workflow run `34807746168`;
- artifact `10333193921`;
- artifact SHA-256 `41ef01992f3b81a30a3f2eb0d498d100e33416e4185352feca0facd1a40a4692`;
- scientific JSON SHA-256 `f99c88d9a21486ed27dd83ef88d650a63d55900c0bdec770d89a2b1a163c0761`;
- environment JSON SHA-256 `07fce4cb6553ee33132f5519f6459eba2523ce2e38c354ef85f17db2db98d75d`.

P0-D23:

- workflow run `34807746382`;
- artifact `10333577281`;
- artifact SHA-256 `f498149490f3a36bce63e5708ed7de90f23312a4e1686d059646e1b08809d2db`;
- scientific JSON SHA-256 `ef9405f0e9b2e5833d8d4fe82bfcb43febf7b0f73ac5972bda3d1e17fc7624c2`;
- environment JSON SHA-256 `07fce4cb6553ee33132f5519f6459eba2523ce2e38c354ef85f17db2db98d75d`.

Branch validation / qualification artifact:

- run `34843463223`;
- artifact `10346933443`;
- SHA-256 `dbbf8e0d1a0d4509a1868aaa859c5d81c1f6caa475fc9fd6b18c3e83eb7d0cb3`.

### Remaining reproducibility gaps

Historical source records with known discrepancies or older evidence tiers remain at their previously recorded level. This audit does not retroactively promote them. Any P0-Q proposal must identify the exact executable/config/environment identities it inherits and must not substitute prose reconstruction for frozen executable identity where that identity is materially required.

**Audit disposition:** `REPRODUCIBILITY_SUFFICIENT_FOR_P0D_CLOSURE; CLAIM_SPECIFIC_RECHECK_REQUIRED_AT_P0Q_FREEZE`.

## 7. Monitor-coverage audit

For the immediately preceding high-dependency executions:

- P0-D22 and P0-D23 reached valid terminal success and preserved artifact identities;
- the branch-wide validation failure was detected as mechanical governance-test drift rather than scientific failure;
- the repeated identical failure signature in runs 224/225 was not allowed to trigger repeated scientific computation;
- the current-head repair triggered run 226 and reached valid terminal success with an artifact;
- no P0-D22/P0-D23 rerun was launched to repair the unrelated governance assertion.

**Audit disposition:** `MONITOR_COVERAGE_ADEQUATE_FOR_CURRENT_P0D_CLOSURE`.

Future P0-Q executions must establish their own dependency-proportional watchdog/checkpoint coverage before launch.

## 8. Candidate objects eligible for P0-Q proposal

### Eligible to PROPOSE, not yet freeze

1. **Observation-geometry / identifiability qualification object.**  
   Scientific basis: P0-D22 shows an estimator can remain finite while modal information is progressively removed and derived chi/recovery coordinates drift. A prospective control is therefore scientifically necessary before cross-system recovery interpretation.

2. **Recovery / hierarchy architecture object, bounded to already supported observables.**  
   Scientific basis: P0-D19–D21 distinguish asymptotic return, finite-time amplification, transformation geometry and exact versus lossy hierarchy preservation. A P0-Q proposal may test a narrowly defined subset, provided the comparator, identifiability control, adjudication rules and uncertainty treatment are prospectively frozen.

### Not mature enough to propose as an admitted discriminator

3. **Current refusal specificity rule.**  
   P0-D23 is a Limit-Map result, not a promotion basis. A future refusal-specificity development version may be designed, but the present selector cannot be presented as discriminating structural switch from nominal stationary control.

4. **Whole-system scalar `chi_system`.**  
   Not licensed. Conglomeration remains a coupled interaction object with lineage-level chi coordinates where individually licensed.

5. **Empirical Atlas/preferred-chi regime boundary.**  
   Not licensed and remains independent/read-only relative to Engine construction.

## 9. Science-changing stop

The non-computational closure work is complete. The next step is a **claim-specific P0-Q proposal package**, not immediate execution.

That package may define candidate controls/rules prospectively, but freezing a new scientific threshold, final comparator identity, confidence/adjudication convention, empirical Atlas reference zone, complete P1 design or MFR-14 package remains a science-changing decision.

## Final closure state

```text
P0D_THROUGH_D23 = COMPLETE
BRANCH_VALIDATION = GREEN_RUN_226
P0D_FUNCTION_LIMIT_CLOSURE = COMPLETE
IDENTIFIABILITY_CONTROL = ELIGIBLE_FOR_P0Q_PROPOSAL
RECOVERY_HIERARCHY_OBJECT = ELIGIBLE_FOR_BOUNDED_P0Q_PROPOSAL
CURRENT_REFUSAL_SPECIFICITY = NOT_MATURE_FOR_PROMOTION
WHOLE_SYSTEM_CHI = NOT_ADMITTED
EMPIRICAL_ATLAS_BOUNDARY = NOT_FROZEN
P1 = CLOSED
NEXT = CLAIM_SPECIFIC_P0Q_PROPOSAL_FOR_USER_SCIENTIFIC_REVIEW
```
