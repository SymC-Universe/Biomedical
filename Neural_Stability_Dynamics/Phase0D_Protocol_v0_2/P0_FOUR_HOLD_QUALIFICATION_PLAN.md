# NSD Phase 0D v0.2 P0 Four-Hold Qualification Plan

Date: 2026-09-10
Status: **ACTIVE P0 QUALIFICATION. NOT A P1 FREEZE.**
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL

## Purpose

Qualify the newly evidence-supported P0 components before any science-adjacent P1 choice is frozen. This stage is allowed to expose measurements, failure behavior, ambiguity, and known-truth error. It is not allowed to choose a comparator winner, pass threshold, confidence convention, neural regime boundary, phenotype interpretation, or chi boundary.

## Qualification objects

### 1. Direct structural comparator plumbing

DMD remains the leading direct neural structural comparator candidate, but P1 comparator identity remains unfrozen. P0 qualification must first demonstrate that the implementation recovers exact known complex modes in a full-rank deterministic case and fails transparently under invalid rank/numerical conditions.

### 2. SSI-COV model adequacy

The existing pole extractor now exposes the same discrete realization `(F, C)` used internally for pole calculation. Model adequacy is kept separate from pole stability.

The primary new method-aligned diagnostic reconstructs the positive-lag covariance sequence through

`R_y(k) ~= C F^(k-1) G`

with `G` fitted only from declared fit lags and evaluated on declared held-out lags. This avoids pretending that process and measurement noise covariances are separately identifiable from the present SSI-COV implementation.

Residual serial structure and independent one-step output prediction remain separate diagnostics. No aggregate adequacy score is created.

### 3. Uncertainty / INDETERMINATE

P0 now has stricter interval validation, explicit indeterminate semantics, and descriptive known-truth calibration helpers. These do **not** implement Reynders-style analytical SSI single-record uncertainty and must never be described as doing so.

The analytical SSI uncertainty route remains an open scientific implementation hold until it can be reproduced faithfully and tested on known-truth systems.

### 4. Unequal-order structure

Cross-order Hungarian matching is demoted to bookkeeping. It reports candidate pairs, assignment costs/margins, and cardinality-unmatched modes. It does not label them scientifically as shared, lost, or added.

Exact ties must remain visibly ambiguous. Any later rule converting candidate pairs into shared/lost/added claims requires an uncertainty-aware frozen adjudication rule and new untouched evidence.

## Known-good / known-bad checks

The P0 suite now requires, at minimum:

- exact DMD recovery of a full-rank deterministic two-oscillator system;
- exact covariance-sequence recovery for a mathematically correct state-space realization;
- poor held-out covariance reconstruction from an intentionally wrong but stable realization;
- strong residual serial-structure response for a deliberately autocorrelated residual process;
- invalid/reversed uncertainty intervals returning indeterminate rather than silently adjudicating;
- exact assignment ambiguity being surfaced as zero margin rather than arbitrarily resolved scientifically.

These are method/implementation qualification tests. Their numerical constants are synthetic test construction values, not neural thresholds.

## Machine-readable qualification record

`scripts/run_p0_four_hold_qualification.py` writes:

`results/p0_qualification/four_hold_summary.json`

The record is explicitly `P0_DESCRIPTIVE_NOT_CONFIRMATORY`, carries `p1_authorized = false`, and includes nonclaims. CI uploads it as an artifact for inspection.

## P1 remains closed

P1 remains blocked until a later milestone audit confirms that the remaining science-adjacent choices are sufficiently justified to freeze, including:

- the exact P1 comparator identity and comparison question;
- model-adequacy adjudication rules and declared lag/search space;
- a justified SSI uncertainty procedure and INDETERMINATE rule;
- unequal-order scientific matching/adjudication logic;
- complete MFR-14, multiplicity, freeze identity, and untouched holdout definition.

No P1 seed, P1 system list, threshold set, or decisive holdout is created in this qualification step.
