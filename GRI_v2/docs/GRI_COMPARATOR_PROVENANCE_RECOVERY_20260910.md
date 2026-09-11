# GRI comparator provenance recovery audit

**Date:** 2026-09-10  
**Status:** PROVENANCE AUDIT, OPEN GAP  
**Protocol mode:** P0-Q / reproducibility and comparator preparation  
**Authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Question

Can the exact previously referenced post-FINAL equal-dimensional / capacity-matched predictive comparator be recovered as a verifiably frozen runnable artifact, so that it can be executed without inventing or rewriting its scientific design?

## Evidence recovered

The current September 8 main manuscript states that the primary predictive comparison has a capacity ceiling because `ALL_METHYLATION_RIDGE` uses 45 methylation Hallmark scores plus two composition covariates while `COVARIATE_ONLY` uses two predictors. It says a dimensionality-matched post-FINAL capacity-control analysis was frozen separately as an adversarial extension.

The September 8 supplement states the same limitation and says a post-FINAL equal-dimensional control can test Hallmark-structured features against a capacity-matched non-Hallmark methylation representation. It correctly states that, because FINAL_HOLDOUT was already opened, this analysis must remain post-FINAL and cannot upgrade the original holdout's prospective status.

Reviewer/disposition records also refer to the control as frozen separately and not yet performed.

## Search performed

Recovery searches were conducted across:

- the `SymC-Universe/Biomedical` GRI repository tree;
- GRI documentation/config/artifact filenames;
- File Library/current-conversation files using `equal-dimensional`, `capacity-matched`, `post-FINAL`, `non-Hallmark`, `methylation ridge`, and related terms.

The searches recovered repeated **references to the intended control**, but no exact runnable package/config/script with a verified freeze identity.

## Current disposition

`HISTORICAL_COMPARATOR_FREEZE_PROVENANCE = UNRESOLVED`

No filename, hash, timestamped commit, archive identity, or executable protocol is being invented.

The statements in the manuscript that the control was "frozen separately" are therefore **not yet independently reconstructable from the recovered artifacts**.

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

Continue archival recovery while the post-C1 sensitivity runs. Do not block Function/Limit mapping, Atlas architecture, independence auditing, or P2 engineering preparation on this search.

**Current comparator status:** structural comparator program PARTIAL/PRESENT; predictive capacity-matched comparator historical freeze UNRESOLVED; future P1 native comparator route NOT YET FROZEN.