# NSD claim-specific P0-Q proposal package

**Date:** 2026-09-14  
**Status:** PROPOSAL ONLY — NO NEW SCIENTIFIC FREEZE, NO EXECUTION AUTHORIZATION  
**Authority:** General Cross-Project Research Protocol v0.8.0  
**Prerequisite closure:** `NSD_P0D_CLOSURE_AUDIT_V080_20260914.md`

## Purpose

Translate the completed P0-D Function/Limit evidence into a small set of claim-specific P0-Q candidates without selecting thresholds, final comparators, Atlas zones, confidence rules, or P1 designs from inspected P0-D outcomes.

## Recommended order

### P0-QA — identifiability / observation-geometry qualification

**Recommendation:** highest priority.

**Why:** P0-D22 shows that latent truth can remain invariant while observation geometry deteriorates, modal support changes, and estimated chi/recovery quantities drift even though the estimator continues returning finite outputs.

**Proposed claim object:**

> A recovery/chi estimate is eligible for interpretation only when its observation geometry and modal identifiability satisfy a prospectively defined qualification rule independent of the downstream recovery relationship.

**What must be frozen before execution:**

- observability/identifiability diagnostic family;
- calibration systems and independent known-truth construction;
- admissible versus indeterminate versus refused semantics;
- uncertainty propagation;
- treatment of unmatched or changing modal support;
- fair comparator diagnostics;
- success/failure rule;
- multiplicity accounting.

**What is explicitly not selected here:** any singular-value ratio, effective-rank, modal-chi-error, recovery-error or other numerical threshold.

### P0-QB — bounded recovery / hierarchy qualification

**Recommendation:** second priority, conditional on P0-QA architecture.

**Why:** P0-D19–D21 resolve several recovery objects that should not be conflated: asymptotic return, recovery timescale, finite-time amplification, transformation geometry, exact state-preserving grouping, and lossy truncation.

**Proposed claim object:**

> Under a prospectively qualified representation, selected recovery observables remain distinguishable and hierarchy-preserving regrouping retains declared outer-system behavior within the validity regime, while lossy truncation can alter realized recovery as internal coupling strengthens.

**Candidate observables:**

- asymptotic stability / return status;
- recovery time constant or native equivalent;
- finite-time transient amplification;
- hierarchy-preservation error under exact versus lossy grouping;
- transformation-geometry sensitivity.

The final subset must be selected prospectively for a precise claim. P0-D effect magnitudes may inform feasibility but may not set the confirmatory threshold.

### P0-QC — refusal specificity redevelopment

**Recommendation:** do not execute as a qualification claim yet; development redesign required first.

**Why:** P0-D23 refuses all structural-switch targets but also all stationary controls overall. This demonstrates conservative refusal but not discriminating refusal.

A future P0-QC lineage would first need a prospectively defined target for what refusal is supposed to discriminate, fresh known-truth calibration families, and controls not already inspected under the revised rule. P0-D23 cannot be recycled as untouched confirmation.

Current disposition:

`CURRENT_REFUSAL_SPECIFICITY = LIMIT_MAP_ONLY`

## Comparator posture

The strongest fair native baseline/final comparator remains a science-changing freeze and is not selected in this proposal. Historical SSI-COV/Subspace-DMD evidence retains its prior status; later comparator choice must follow the current protocol and cannot be chosen merely because it makes the NSD object look favorable.

## Atlas posture

The Neurostability Atlas remains independent and read-only relative to Engine construction. No empirical Atlas zone, preferred chi range, or `chi ~ 1.2-1.3` note may set P0-Q thresholds, calibration regions, stopping rules, or success criteria.

## MFR-14 and promotion posture

This package does not satisfy MFR-14. Any later P1 proposal must separately close the applicable MFR-14 components, multiplicity, independence, frozen implementation, challenge-set identity and scoring/adjudication rules.

## Recommended scientific decision

Recommended next scientific choice:

```text
APPROVE P0-QA architecture development
APPROVE P0-QB architecture development conditional on P0-QA
DEFER P0-QC qualification; retain refusal specificity as an open Limit-Map problem
KEEP chi_system and empirical Atlas boundary unadmitted
```

Approval would authorize prospective design and freezing work only within the chosen claims. It would not authorize outcome-driven threshold selection or P1 execution.
