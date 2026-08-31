# P0 D4 pre-compute concretization

**STATUS: FROZEN BEFORE ANY REPLICATION TARGET SCORE IS GENERATED**

Date: 2026-08-30

This note closes two purely statistical implementation details that were not numerically consequential in the D4 freeze text but must be explicit before REPLICATION is opened.

## Paired sign-test ties

The D4 primary paired model comparison uses the cancer-level difference

`COVARIATE_ONLY median normalized MSE - ALL_METHYLATION_RIDGE median normalized MSE`,

so positive values favor the all-methylation model.

The exact one-sided sign test excludes exact zero differences as ties, uses the remaining non-tied cancers as `n`, and computes the exact Binomial(n, 0.5) upper-tail probability for the observed number of positive differences. No continuity correction or smoothing is used.

## Binary comparator metrics

For P2 comparator/ablation forecasting, DISCOVERY favorable status is the prediction and REPLICATION favorable status is the evaluation label. Confusion counts are therefore TP/FP/TN/FN in that direction.

Precision, recall, specificity, balanced accuracy, and Matthews correlation are emitted only when their mathematical denominators are nonzero. Undefined metrics are recorded as `NOT_EVALUABLE`/non-finite in machine-readable output; no pseudocount is added.

These rules change no participant, transform, threshold, null, state definition, model, target, or claim boundary and were frozen before any REPLICATION target score was generated.
