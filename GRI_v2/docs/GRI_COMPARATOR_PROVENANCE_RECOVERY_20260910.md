# GRI comparator provenance recovery audit

**Date:** 2026-09-10  
**Last recovery search:** 2026-09-11  
**Status:** PROVENANCE AUDIT, OPEN GAP  
**Protocol mode:** P0-Q / reproducibility and comparator preparation  
**Authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Question

Can the exact previously referenced post-FINAL equal-dimensional / capacity-matched predictive comparator be recovered as a verifiably frozen runnable artifact, so that it can be executed without inventing or rewriting its scientific design?

## Evidence recovered

The current September 8 main manuscript states that the primary predictive comparison has a capacity ceiling because `ALL_METHYLATION_RIDGE` uses 45 methylation Hallmark scores plus two composition covariates while `COVARIATE_ONLY` uses two predictors. It says a dimensionality-matched post-FINAL capacity-control analysis was frozen separately as an adversarial extension.

The September 8 supplement states the same limitation. In Section 6.2 it records that the held-out comparison tests whether the frozen methylation representation adds predictive information beyond the two measured covariates, **not** whether an equal-capacity Hallmark architecture outperforms an equal-capacity non-Hallmark representation. It then says a post-FINAL dimensionality-matched capacity-control protocol is retained separately as adversarial follow-up.

In the supplement's residual predictive-capacity limitation section, the same distinction is preserved: a post-FINAL equal-dimensional control can test Hallmark-structured features against a capacity-matched non-Hallmark methylation representation, but because FINAL_HOLDOUT has already been opened that analysis must remain post-FINAL and cannot upgrade the original holdout's prospective status.

Reviewer/disposition records also refer to the control as frozen separately and not yet performed. Those reviewer-derived records are supporting lineage only; they do not substitute for an exact source-of-record freeze artifact.

## Search performed

Recovery searches have been conducted across:

- the `SymC-Universe/Biomedical` GRI repository tree;
- GRI documentation/config/artifact filenames;
- File Library/current-conversation files using `equal-dimensional`, `capacity-matched`, `post-FINAL`, `non-Hallmark`, `methylation ridge`, `same-capacity`, `methylation PCA control`, and related terms.

### 2026-09-11 re-search

A fresh File Library search again recovered:

- the September 8 supplement describing the intended post-FINAL dimensionality-matched capacity control;
- pasted reviewer/adversarial-review records discussing the same intended control;
- no exact comparator config, script, BAT, archive, manifest, hash ledger, or frozen protocol package attributable to that control.

The search also returned unrelated uses of the phrase `equal-dimensional` from other SymC projects. Those are not GRI comparator evidence and are excluded from this provenance path.

## Current disposition

`HISTORICAL_COMPARATOR_FREEZE_PROVENANCE = UNRESOLVED`

More specifically:

`PROTOCOL_INTENT_REFERENCED = YES`

`EXACT_EXECUTABLE_FREEZE_RECOVERED = NO`

`RESULT_RECOVERED = NO`

No filename, hash, timestamped commit, archive identity, executable protocol, model design, or result is being invented.

The statements in the manuscript that the control was "frozen separately" or "retained separately" are therefore **not yet independently reconstructable as an executable freeze from recovered artifacts**.

## Why this matters under v0.7.1

The protocol requires the scientific comparison question and comparator-selection route to be frozen before decisive evaluation for any prospective incremental-value claim.

The current FINAL_HOLDOUT comparison remains valid for the narrower task it actually tested:

> Does the frozen methylation representation add held-out predictive information beyond the two prespecified composition covariates?

It does not establish:

> Does Hallmark-structured methylation outperform an equal-capacity non-Hallmark methylation representation?

That second question needs its own comparator design/evidence status.

## Allowed branches

### Branch A: exact historical freeze is recovered

If an exact artifact is found later:

1. verify timestamp predates its result exposure;
2. verify the design matches the manuscript description;
3. hash/archive the recovered artifact;
4. inspect only enough to establish provenance before execution;
5. execute unchanged;
6. report it as the previously frozen **post-FINAL adversarial extension**;
7. do not call it part of the pristine FINAL_HOLDOUT.

### Branch B: exact historical freeze cannot be recovered

Then:

1. preserve `UNRESOLVED` provenance for the historical freeze claim;
2. design a new capacity-matched comparator transparently;
3. label it **new post-FINAL P0-Q adversarial work**;
4. do not represent it as the lost historical freeze;
5. use already-viewed/internal TCGA evidence for qualification only;
6. freeze the strongest fair native comparator route separately before future P1 external evaluation.

A new post-FINAL control can still improve the current paper's scientific completeness. It cannot retroactively create prospective status.

## Scientific design choices that require user review before a new freeze

If Branch B is reached, the following are science-adjacent/scientific rather than mechanical:

- exact non-Hallmark representation;
- dimensionality/capacity matching rule;
- feature selection rule;
- model family and tuning;
- target set;
- performance metric;
- multiplicity family;
- primary decision rule;
- null/alternative;
- which current result would count against Hallmark-specific added value.

These are not to be filled from convenience or from whichever design produces the desired answer.

## Current action

Repository and File Library recovery have now been pushed to the point where no exact historical runnable comparator freeze is visible in the available project records.

Do not convert absence of recovery into proof that no local artifact ever existed. A local archive could still contain it. Until such an artifact is produced, however, the project treats the exact historical freeze as unresolved rather than operative.

This gap does not block Function/Limit mapping, Atlas architecture, independence auditing, post-C1 sensitivity, or P2 protocol-neutral engineering preparation.

**Current comparator status:** structural comparator program PARTIAL/PRESENT; predictive capacity-matched comparator historical freeze UNRESOLVED; future P1 native comparator route NOT YET FROZEN.