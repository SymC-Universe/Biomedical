# GRI v2 P3-v2 development-informed final-holdout amendment

**Status: FROZEN BEFORE FINAL_HOLDOUT MOLECULAR VALUES ARE OPENED**

Date: 2026-09-05

## 1. Why this amendment exists

P3-v1 remains part of the provenance record and is not rewritten. Its categorical ACCEPT/CAUTION/REFUSE selective-prediction test is not identifiable in the current TCGA P0 realization because the implemented state is cancer-level while the planned risk unit was cancer-Hallmark, and all 19 discovery cancers collapsed to CAUTION.

That failure does not imply that post-replication learning is scientifically forbidden. D4 is now treated explicitly as a **development/validation partition** for a new version. P3-v2 is therefore a post-D4, development-informed analysis frozen before any FINAL_HOLDOUT methylation value or RNA target score is inspected.

P3-v2 is not described as the original preregistered P3 test. Any evidence from FINAL_HOLDOUT applies only to this v2 question and retains the claim ceiling of an internal TCGA final test.

## 2. Firewall

At this freeze:

- FINAL_HOLDOUT methylation numeric values inspected: false
- FINAL_HOLDOUT RNA target scores generated: false
- discovery model refit: false
- discovery transform refit: false
- composition model refit: false
- participant reassignment: false
- covariate imputation: false
- Stage C1 modification: false

The original P0 split remains unchanged.

## 3. What D4 taught us

The categorical audit state was too coarse for risk stratification: 19/19 discovery cancers were GLOBAL_SHARED_ONLY / CAUTION.

The semantic Hallmark-label branch also failed broadly in D4 and remains a biological-interpretation guardrail rather than being forced into a prediction-risk selector.

A deliberately limited D4 development analysis found that the existing continuous global-geometry primitive retained information lost by the categorical state. Using the minimum raw Delta_CKA across PRIMARY_PUBLICATION and MASKED_TECHNICAL for each discovery cancer, the Spearman association with D4 ALL_METHYLATION_RIDGE cancer-median normalized MSE was approximately rho = -0.689. This is a D4 development observation, not a confirmatory result. Discovery sample count did not show a comparable relationship. PCPG remained an important counterexample/stress case, so no claim is made that global geometry alone fully captures transport risk.

This motivates testing a continuous confidence ordering in FINAL_HOLDOUT without fitting a new threshold or a multivariable score.

## 4. Analysis unit and eligibility

Primary P3-v2 unit: **cancer**.

For each cancer, final predictive risk is the median across evaluable RNA Hallmark targets of:

`normalized_MSE = final MSE / frozen discovery target variance`.

The inherited minimum composition-complete final sample count remains 30. Pre-value metadata closure found PAAD has 26 complete FINAL_HOLDOUT participants. PAAD is therefore excluded from primary P3-v2 and final P1 cancer-level inference without rescue. The other 18 cancers are the primary evaluation set.

No cancer-Hallmark pseudo-replication is used for the primary inferential unit.

## 5. Prediction model remains unchanged

P3-v2 uses the same discovery-trained ALL_METHYLATION_RIDGE predictor, discovery-frozen methylation/RNA transforms, discovery target reference means/variances, composition covariates, and model parameters used in D4.

FINAL_HOLDOUT is projection/scoring only. No refit or recalibration is permitted after final values are opened.

## 6. Primary P3-v2 selector

Define the discovery-only continuous confidence score for cancer c:

`GLOBAL_GEOMETRY_CONFIDENCE(c) = min(Delta_CKA_RAW_PRIMARY(c), Delta_CKA_RAW_MASKED_TECHNICAL(c))`.

Both values come from the already-frozen D3 discovery audit.

Higher confidence is prospectively hypothesized to correspond to lower FINAL_HOLDOUT normalized MSE.

No threshold is fit. No ACCEPT/REFUSE category is created from this score for v2.

## 7. Pre-final comparators

Two comparators are frozen before final access:

1. **D4_REPLICATION_RISK**: D4 ALL_METHYLATION_RIDGE cancer-median normalized MSE. Lower D4 risk predicts lower final risk. This is a strong development-performance baseline and is explicitly not an audit-only score.
2. **DISCOVERY_N**: frozen discovery cancer sample count. Larger discovery n predicts lower final risk as a simple quality-control/sample-size baseline.

The purpose is to learn whether the audit primitive adds prospective ordering information beyond a trivial sample-size proxy and how it compares with the strongest obvious empirical baseline, prior replication performance.

No hybrid fitted score is allowed in P3-v2.

## 8. Primary association test

Across the 18 eligible cancers:

- primary effect: Spearman rho between GLOBAL_GEOMETRY_CONFIDENCE and final cancer risk, with negative rho favorable;
- inferential p-value: deterministic one-sided permutation test with 99,999 permutations;
- seed namespace: `GRI_V2_PREDICTION_P0_20260830|P3V2|SPEARMAN|GLOBAL_GEOMETRY_CONFIDENCE`.

Comparator associations are reported with the same deterministic permutation count and their own selector name appended to the namespace.

Effect sizes and ranks are retained regardless of p-value.

## 9. Coverage-risk analysis

Order the 18 cancers from highest to lowest GLOBAL_GEOMETRY_CONFIDENCE. Let r_i be each cancer's final median normalized MSE.

For each prefix coverage k/N, compute mean selected risk over the first k cancers. Report the full coverage-risk curve and the fixed summary coverages 50%, 75%, and 100%.

Define AURC as the arithmetic mean of the prefix mean risks over k = 1..N. Lower AURC is favorable.

Assess AURC against 99,999 deterministic random cancer orderings using namespace:

`GRI_V2_PREDICTION_P0_20260830|P3V2|AURC|GLOBAL_GEOMETRY_CONFIDENCE`.

This is a continuous ranking test. No post-final coverage threshold may be promoted as an ACCEPT cutoff.

## 10. Final P1 direct-prediction test retained

Separately from P3-v2, FINAL_HOLDOUT will evaluate the unchanged P1 comparison:

`COVARIATE_ONLY median normalized MSE - ALL_METHYLATION_RIDGE median normalized MSE`.

Positive differences favor ALL_METHYLATION_RIDGE. Use the exact one-sided sign test with exact ties excluded, as frozen for D4. With 18 primary eligible cancers the result remains below the 24-cancer pan-cancer promotion floor and is descriptive/internal even if favorable.

## 11. Interpretation rules

P3-v1 categorical selective prediction remains NOT_EVALUABLE and is not retrospectively rescued.

If P3-v2 GLOBAL_GEOMETRY_CONFIDENCE predicts lower final risk, the supported statement is limited to: a D4-informed continuous global-geometry confidence ordering prospectively stratified risk in an untouched internal TCGA final partition.

If it fails, global geometry is not retained as a validated risk selector on the basis of D4 alone.

Semantic Hallmark specificity remains a separate interpretation guardrail. A failure of semantic specificity does not automatically imply poor numerical prediction, and good numerical prediction does not license a semantic mechanism claim.

External independent validation remains mandatory before general tool promotion.

## 12. No post-final rescue

After FINAL_HOLDOUT molecular values are opened, P3-v2 may not change:

- eligible cancers or n>=30 rule;
- confidence-score definition;
- comparator definitions;
- prediction model or transformations;
- risk metric;
- permutation count/seed rule;
- coverage-risk/AURC definition;
- P1 comparator or sign-test rule;
- claim ceiling.

Unexpected failures are retained and become inputs to the next external version, not reasons to rewrite P3-v2.
