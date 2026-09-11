# NSD P0Q1 Rank-Signal Prospective Result

Date: 2026-09-10/11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL
Status: **PROSPECTIVE P0Q1 SPLIT RESULT. SSI-COV SURVIVES; SUBSPACE DMD FAILS. P1 REMAINS CLOSED.**

## Frozen identity

Freeze/result commit: `a1432f006c9191e742240d50c341730e3cd4b440`
P0Q1 workflow run: `34563668927`
P0Q1 artifact: `nsd-phase0d-p0q1-rank-signal-result`
Artifact SHA-256: `1bfdb57ce0a9aceec1df8aa7a4968a1ae18bfa7297b557c2a2b0cad8444a00b7`
Freeze schema: `nsd-phase0d-v0.2-p0q1-rank-signal-freeze-v1`
Hypothesis provenance: `DATA_DERIVED_POST_RESULT_FROM_P0_RANK_NULL_STRESS`
Promotion debt: `NSD-DEBT-004`

The rule, seed base, channel count, systems, null families, expected directions and failure consequence were committed before the P0Q1 workflow generated a result.

## Prospective verdict

### SSI-COV

`SURVIVES_P0Q1`

- mechanical exceptions: `0`
- all 7 oscillatory families met the frozen admission floor
- all 8 refusal families met the frozen zero-false-admission ceiling
- oscillatory records admitted: `35/35`
- refusal records false-admitted: `0/40`

Candidate ranks followed the planted/observable construction in the intended direction:

- single oscillator: rank `2` in `5/5`
- ordinary two-mode systems: rank `4` in `5/5` per family
- weak-observability system: rank `2` in `5/5`, which was explicitly acceptable because latent order 4 was not required
- three-mode system: rank `6` in `5/5`

This is a **P0 method-qualification result only**. It does not establish the rule for EEG or pay promotion debt for P1.

### Subspace DMD

`FAILS_P0Q1`

- mechanical exceptions: `0`
- all 7 oscillatory families met the frozen admission floor
- 7 of 8 refusal families had zero false admissions
- oscillatory records admitted: `35/35`
- false admissions occurred only in `real_pole_only_linear_system`: `2/5`

For that real-pole-only family, Subspace DMD chose rank `4` in all five replicates. Three replicates were refused because the selected model contained unstable poles. Two replicates produced only stable estimated poles including complex pairs and were therefore false-admitted by the frozen candidate gate.

The failure is **scientific, not mechanical**. It cannot be repaired by changing the P0Q1 rule on these records.

## What the result means

The P0Q1 experiment falsifies the proposition that the same simple conjunction

`largest singular gap + gap >= 3 + interior rank + stable poles + >=1 stable complex mode`

is already adequate as a common operational rank-signal gate for both SSI-COV and Subspace DMD.

It does **not** falsify Subspace DMD as an estimator-at-declared-rank comparator. Subspace DMD previously completed the fixed stochastic recovery matrix with strong conditional recovery. The failure is specifically in the truth-blind operational rank-signal route.

This sharpens the comparator firewall:

1. conditional estimator recovery at a supplied rank can remain strong;
2. operational rank selection/refusal can still fail;
3. the two claims may not be merged.

## Required failure consequence applied

- P0Q1 remains a preserved failure for Subspace DMD.
- The P0Q1 gate will not be retuned or rescored on these records.
- `NSD-DEBT-004` is not paid.
- SSI-COV survival is recorded as one prospective P0 installment, not P1 confirmation.
- Any new Subspace-DMD operational rule is a new version, post-P0Q1, with its own provenance and new untouched evidence.

## Immediate diagnostic question

The next P0 investigation is:

> Why does the Subspace-DMD projected-future rank signal favor rank 4 for a two-real-mode stochastic generator, and can a method-native operational rule distinguish stochastic innovation dimension from persistent oscillatory generator structure without truth access?

The answer must be sought through the retained singular spectra, lower-rank fits, cross-rank persistence and the published Subspace-DMD rank conventions. No new P0Q2 rule is frozen until that diagnostic is complete.

## Nonclaims

No P1 comparator, rank selector, neural threshold, chi coordinate, regime boundary, phenotype, mechanism, prediction or clinical result is established by P0Q1.
