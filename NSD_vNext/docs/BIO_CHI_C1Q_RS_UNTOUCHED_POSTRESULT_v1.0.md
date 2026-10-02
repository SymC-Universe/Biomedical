# Bio Chi C1Q-RS Untouched Qualification Postresult v1.0

**Status:** COMPLETE / IMPLEMENTATION-LEVEL QUALIFICATION SUPPORTED  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Plan:** `NSD_vNext/docs/BIO_CHI_C1Q_RS_UNTOUCHED_PLAN_v0.1.md`  
**Freeze:** `NSD_vNext/docs/BIO_CHI_C1Q_RS_UNTOUCHED_FREEZE_v1.0.md`

## Provenance

- Workflow: `NSD C1Q-RS Untouched Qualification`
- Run: `36371426674`
- Source head: `d29864608da27b36cc3f5132f60c86426287eb17`
- Complete artifact: `nsd-c1q-rs-untouched-complete`
- Artifact ID: `10949372282`
- Digest: `sha256:7cfa8b5bda2e72ada855fda2b1afd6b9db724d6b86a9662173cb5a549820d946`

All four frozen mechanical preflight jobs passed. All 16 untouched full-map cell jobs passed. Merge completed successfully.

The complete artifact contains exactly 96 rate-level rows and 48 same-path fine/coarse paired units.

## Untouched result

C1Q-RS satisfied strict non-worsening in **96/96** rows.

Relative to unchanged legacy C1Q:

- lower NLL was found in 35/96 rows at numerical scale;
- material NLL improvement greater than (10^{-3}) occurred in 33/96 rows;
- recurrence-derived starts supplied winning lower basins across multiple independent cells, seeds, and both sampling rates;
- no strict-containment regression occurred.

The largest untouched NLL improvement was approximately **222.91**.

### Local chi recovery

Across all 96 untouched rows:

- legacy median absolute chi error: **0.04947**;
- C1Q-RS median absolute chi error: **0.02990**;
- legacy maximum absolute chi error: **0.69676**;
- C1Q-RS maximum absolute chi error: **0.31378**.

C1Q-RS improved absolute chi recovery in 34 rows, tied legacy within numerical tolerance in 60 rows, and was worse in only two rows. The two worse rows were tiny numerical-scale differences: approximately (5.7	imes10^{-7}) and (7.38	imes10^{-5}) in absolute chi error.

### g recovery

Across all 96 untouched rows:

- legacy median absolute g error: **0.19264**;
- C1Q-RS median absolute g error: **0.14159**;
- legacy maximum absolute g error: **1.56049**;
- C1Q-RS maximum absolute g error: **0.80844**.

C1Q-RS improved absolute g recovery in 34 rows, tied in 60, and was worse in two rows. No reproducible new g-recovery failure mechanism appeared.

### Natural-frequency recovery

Across all 96 untouched rows:

- legacy median absolute natural-frequency error: **1.08216 Hz**;
- C1Q-RS median absolute natural-frequency error: **0.75923 Hz**;
- legacy maximum absolute error: **112.54 Hz**;
- C1Q-RS maximum absolute error: **26.34 Hz**.

C1Q-RS improved natural-frequency recovery in 36 rows and tied legacy in 60. It was not worse in any row.

### Rate structure

At 256 Hz:

- legacy median absolute chi error: **0.03108**;
- C1Q-RS median absolute chi error: **0.02677**;
- legacy median absolute g error: **0.11529**;
- C1Q-RS median absolute g error: **0.10354**.

At 128 Hz:

- legacy median absolute chi error: **0.17745**;
- C1Q-RS median absolute chi error: **0.03555**;
- legacy median absolute g error: **0.38918**;
- C1Q-RS median absolute g error: **0.18781**.

The improvement is therefore not confined to a single realization, cell, sign of g, or sampling rate. As in the development map, the largest practical benefit appears in rows where the legacy start family misses a better likelihood basin.

### Same-path rate sensitivity

Median same-path chi drift changed from **0.02086** under legacy C1Q to **0.01925** under C1Q-RS. Median same-path g drift was **0.08634** for both routes, while the maximum g drift was reduced from approximately **1.727** to **0.802**.

These are practical estimator-rate diagnostics, not the exact mathematical sampling-invariance theorem.

## Recovery versus likelihood tension

The APQ-required tension check does not identify a new reproducible conflict.

Only one row had a lower C1Q-RS NLL with visibly worse chi recovery above numerical noise: cell 4, seed 161803, coarse rate. The NLL improvement was only about (1.88	imes10^{-5}), while absolute chi error increased by approximately (7.38	imes10^{-5}). Another fine-rate row differed only at roughly (10^{-7}) error scale.

This is numerical-scale tradeoff, not a new scientific failure class.

## Promotion-rule disposition

The frozen promotion condition is satisfied:

1. lower-NLL rescue occurs on more than a single isolated realization;
2. it occurs across multiple cells, seeds, and rates;
3. strict containment passes 96/96;
4. no reproducible new recovery or numerical failure mechanism appears;
5. full parameter-recovery distributions improve or remain effectively unchanged.

Therefore C1Q-RS is supported as the **preferred qualification search implementation for future C-family work**.

This is an implementation-level supersession only.

## What is superseded

For new C-family qualification runs, the legacy C1Q start-search route should no longer be the default when C1Q-RS is available.

Legacy C1Q remains preserved as:

- historical baseline;
- regression comparator;
- provenance for previously frozen artifacts;
- a useful demonstration of the basin-selection failure that motivated the repair.

No historical artifact is rewritten.

## What is not promoted

The following remain explicitly unlicensed:

- C1Q-RS as a production biological estimator;
- C1Q-RS fit quality as evidence that truth belongs to C;
- real-EEG local chi;
- any empirical admission threshold;
- biological prevalence;
- reinterpretation of colored, D\C, S\D, multimode, closure, or alias Limit Map results.

The semantic admission problem remains open.

## Post-execution deviation audit

The untouched scientific plan was followed.

- frozen 16-cell coordinates preserved;
- frozen three new seeds preserved;
- fine/coarse same-path design preserved;
- legacy and RS implementations unchanged during execution;
- strict non-worsening evaluated on all 96 rows;
- no unfavorable row excluded;
- no outcome-derived threshold introduced;
- no semantic Limit Map claim relabeled.

No material plan deviation occurred.

## Next scientific requirement

The search-route defect is now sufficiently characterized and repaired for qualification use. Further optimizer tuning is not the current bottleneck.

The next unresolved Bio Chi gate is semantic and inferential: determine whether a finite-data admission architecture can distinguish a valid local continuous-lineage mode from incompatible higher-order/memory/family-scope cases while quantifying uncertainty on the recovered pole/chi coordinate.

That next plan should use C1Q-RS as the preferred C-family search route but must preserve the independent C/D/S, colored-process, multimode, closure, sampling, and uncertainty refusal layers.
