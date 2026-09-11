# GRI predictive comparator provenance recovery audit

**Date:** 2026-09-11  
**Status:** OPEN PROVENANCE GAP  
**Protocol:** v0.7.1 MFR-05 / Sections 1.2, 12, 33.3 + v0.7.1A

## Frozen scientific issue

The current internal FINAL_HOLDOUT primary comparison used a 45-Hallmark methylation representation plus purity/leukocyte covariates against a two-covariate baseline. This establishes held-out methylation information beyond those two covariates in the tested internal partitions, but does not by itself establish added value attributable uniquely to Hallmark-structured representation under a capacity-matched comparison.

The September 8 manuscript/supplement lineage states that a post-FINAL equal-dimensional control was frozen separately as an adversarial follow-up. That statement creates a provenance obligation: either recover the exact freeze identity/package or explicitly record that it is unavailable.

## Recovery actions completed in current audit

1. Repository tree audited for an identifiable equal-dimensional/capacity-matched predictive control artifact.
2. GitHub code search for `equal-dimensional control` returned no result.
3. GitHub code search for `capacity matched` did not recover a current GRI v2 comparator freeze; matches were unrelated historical manuscript language.
4. Previously recovered File Library/manuscript text documents the intended control but no runnable exact package/hash has yet been verified.

## Current disposition

`HISTORICAL_EQUAL_DIMENSIONAL_FREEZE = REFERENCED_BUT_NOT_RECOVERED`

This means:

- do not claim the exact control was executed;
- do not invent a historical filename, hash, timestamp, or design detail not present in a source of record;
- do not represent a newly written control as the lost prior freeze;
- retain the current FINAL_HOLDOUT claim ceiling as additional methylation information beyond the specific covariate baseline, not capacity-matched superiority of Hallmark architecture.

## Local archive search target

If local project archives are searched later, the target is any pre-result artifact dated no later than the first execution of the post-FINAL capacity control and containing language/design equivalent to:

- equal-dimensional or dimensionality-matched control;
- capacity-matched non-Hallmark methylation representation;
- post-FINAL adversarial extension;
- frozen before that control's result was inspected.

A candidate is not accepted merely because its filename sounds right. Verify timestamp, content, relation to FINAL_HOLDOUT opening, and hash/commit provenance where available.

## If recovered

1. Hash the artifact/package.
2. Record verifiable timestamp/commit/deposit identity.
3. Confirm it predates result inspection.
4. Compare its design to the manuscript description.
5. Execute unchanged if mechanically runnable.
6. If mechanical repair is required, preserve the original and prove scientific equivalence.
7. Label outcome explicitly `POST_FINAL_ADVERSARIAL` unless the original design itself supports a stronger already-frozen status.

## If not recovered

A new capacity-matched comparator may be designed because it remains scientifically useful, but:

- it is a new P0-Q/post-FINAL adversarial analysis on current internal data;
- it cannot retroactively make FINAL_HOLDOUT prospectively capacity-matched;
- its design must be reviewed before execution if it changes the scientific comparison question, features, metric, or interpretation;
- for future external P1, the scientific task, comparator-selection route, comparator identity/version, metric, failure rule, and evidence basis must be frozen before decisive evidence is opened.

## Future native-comparator route

For external prediction, the comparator search must target the strongest fair native method for the exact frozen prediction task, not simply a model with the same number of predictors. Candidate families may be considered only after a frozen literature/benchmark/domain-expert search establishes relevance. No comparator is designated by this recovery audit.

## Current blocker classification

This provenance gap does **not** block completion of the already-frozen post-C1 sensitivity or P0-D Function/Limit mapping. It does block any claim that the historical internal predictive result has already demonstrated capacity-matched added value of the Hallmark architecture.