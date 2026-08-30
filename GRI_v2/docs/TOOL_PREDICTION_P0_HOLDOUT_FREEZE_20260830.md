# GRI v2 predictive holdout and selective-prediction protocol P0

**STATUS: FROZEN BEFORE P0 PREDICTIVE TARGET VALUES OR STAGE C1 BETA-VALUE BIOLOGICAL RESULTS ARE INSPECTED**

Date: 2026-08-30

F4 anchor: `b1fbf9f5b61ae9e94daff7042b6575b789111434`

This protocol implements the next gate required by `TOOL_PREDICTION_PROSPECTIVE_OBJECTIVE_AMENDMENT_20260830.md` after Gate F4 closed `NARROW`.

It is a separate predictive-validation protocol. It does not modify, replace, rescue, or reinterpret the frozen Stage C1 v2 inferential contract.

## 1. Objective

Test the reduced cross-omic architecture / integration-readiness auditor as an integrated predictive and refusal system in three prospectively distinct senses:

1. **P1 direct cross-layer prediction**: predict frozen RNA Hallmark target scores from methylation Hallmark source scores and allowed composition covariates;
2. **P2 replication prediction**: test whether a discovery-partition audit state predicts whether the same cross-layer relationship reproduces in an untouched replication partition;
3. **P3 selective prediction / refusal**: test whether discovery-partition ACCEPT / CAUTION / REFUSE states stratify prediction error in a separately untouched final holdout partition.

The F4-narrowed architecture is the object under test. Regulatory autonomy is not an independent coordinate in P0.

## 2. Frozen upstream identities

P0 may use only the already-approved matched-data and mapping universe:

- C0.1 strict one-to-one methylation / Stage A sample universe: 9,460 tumors across 32 cancers before C1 missingness eligibility;
- methylation source SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- PRIMARY_PUBLICATION probe universe: 22,601 exact probes;
- MASKED_TECHNICAL probe universe: exact primary track minus the frozen 579-probe union mask, nominally 22,022 probes before prediction-specific discovery eligibility;
- probe-gene-region map SHA-256 `78f38d420a486427d67d88f67f5da83d1811003bf578b3c673f1dcbee5912296`;
- probe-flags SHA-256 `5777ff7331c4bae750ed1c87bb6eb93136c56ade6dbf8522829db1f5659ac455`;
- Hallmark membership SHA-256 `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`;
- Stage A Hallmark-union RNA cache SHA-256 `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`;
- B1 ABSOLUTE-purity SHA-256 `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`;
- B1 methylation-derived leukocyte-fraction SHA-256 `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`.

No survival, treatment response, recurrence, subtype, genomic outcome, RPPA result, historical GRI score, biological chi, or preferred SymC pattern may define P0 targets, partitions, features, thresholds, or state rules.

## 3. Leakage firewall and partition assignment

The participant root is the indivisible split unit. Every assay, covariate, technical track, feature representation, and derived quantity for a participant remains in exactly one partition.

Partition assignment is determined from the C0.1 matched identity universe before any P0 target value is inspected.

Seed namespace:

`GRI_V2_PREDICTION_P0_20260830`

For participant root `p` in cancer `c`, compute SHA-256 of

`GRI_V2_PREDICTION_P0_20260830|<cancer>|<participant_root>`.

Interpret the first 8 digest bytes as an unsigned big-endian integer and reduce modulo 10:

- buckets `0..5`: `DISCOVERY` (nominal 60%);
- buckets `6..7`: `REPLICATION` (nominal 20%);
- buckets `8..9`: `FINAL_HOLDOUT` (nominal 20%).

No sample may be reassigned to repair an unfavorable partition count. No split may be regenerated.

### 3.1 Sample eligibility after assignment

The individual PRIMARY_PUBLICATION sample rule remains the frozen C1 rule: at least 95% of the 22,601 primary probes must be finite.

Partition assignment is never changed after this eligibility screen.

A cancer is fully evaluable for P0 only when at least 30 eligible matched participants remain independently in each of DISCOVERY, REPLICATION, and FINAL_HOLDOUT. The value 30 is inherited from the already-frozen C1 fixed-n design so every P0 partition can support at least one independent C1-sized sample set.

A pan-cancer promoted P0 statement requires at least 24 fully evaluable cancers, matching the already-frozen C1 pan-cancer promotion floor. If fewer than 24 remain, P0 is descriptive and cannot support a pan-cancer predictive promotion.

## 4. Discovery-only preprocessing

All feature eligibility beyond the per-sample screen, imputation, centering, scaling, dimensionality reduction, orientation, model selection, and state construction are fit on DISCOVERY only.

REPLICATION and FINAL_HOLDOUT target values may not influence any transformation or fitted parameter.

### 4.1 Methylation probe handling

Within each cancer's DISCOVERY partition:

1. a PRIMARY_PUBLICATION probe is retained if at least 95% of discovery samples are finite;
2. its imputation value is the discovery finite-sample median;
3. MASKED_TECHNICAL is the exact intersection of the discovery-retained primary probes with the frozen mask-retained probe set;
4. REPLICATION and FINAL_HOLDOUT use exactly the discovery-retained probes and discovery medians;
5. no holdout variance, mean, correlation, target relationship, or prediction error may alter probe eligibility or imputation.

### 4.2 PROMOTER_CORE source representation

Use the already-frozen primary regulatory stratum `PROMOTER_CORE = TSS200`.

Per sample and gene, compute the median beta value over unique eligible TSS200 probes mapped to that gene. Annotation-supported multi-gene probes may enter each supported gene. No nearest-gene invention is allowed.

A Hallmark is eligible when it has at least 10 mapped genes and at least 10 contributing methylation probes in DISCOVERY. At least 25 common eligible Hallmarks are required for the full semantic P0 branch in a cancer.

### 4.3 Leakage-free Hallmark eigengenes

For each eligible Hallmark, fit the methylation Hallmark PC1 using DISCOVERY only:

- center gene methylation columns using discovery means;
- fit PC1 in discovery;
- orient it so its discovery correlation with the discovery sample-wise unweighted mean gene methylation is nonnegative; if exactly zero, orient the largest-absolute loading positive;
- project REPLICATION and FINAL_HOLDOUT using the frozen discovery means and loadings.

Build an analogous RNA Hallmark PC1 target representation from the exact frozen Hallmark-union RNA genes, again fitting all centering and PC1 loadings in DISCOVERY only and projecting both held-out partitions with those discovery parameters.

These P0 train-fit RNA target eigengenes exist only to satisfy the predictive no-leakage requirement. They do not replace or alter the independently frozen Stage C1 Stage-A RNA eigengene definition.

## 5. Discovery audit primitives

The P0 auditor uses the F4-narrowed architecture and reuses the synthetic-calibrated F2 decision primitives where applicable. No P0 threshold is selected from biological outcomes.

### 5.1 Global sample geometry

On DISCOVERY, compute linear CKA between source methylation and target RNA sample geometry and 39 deterministic patient-row permutations.

Define:

`Delta_CKA = CKA_observed - median(CKA_patient_null)`.

`GLOBAL_SHARED_DETECTED` requires both:

- empirical one-sided `p <= 0.05`;
- `Delta_CKA >= 0.05`.

These are the already-frozen F2 global-screen thresholds.

### 5.2 Semantic specificity

Using discovery-fit matched Hallmark eigengenes, compute

`A_same = median_H |rho_S(M_H, R_H)|`.

Generate separately:

- 39 deterministic methylation-patient permutations against fixed RNA Hallmarks;
- 39 deterministic methylation-Hallmark-label permutations with patients aligned.

Define discovery effects against the medians of those null families:

- `Delta_A_patient`;
- `Delta_A_label`.

Label-specific semantic detection requires the already-frozen F2 semantic rule:

- label-null empirical `p <= 0.05`;
- `Delta_A_label >= 0.10`.

Patient-specific support requires:

- patient-null empirical `p <= 0.05`;
- `Delta_A_patient > 0`.

The patient effect is sign-gated rather than assigned a new post-F3 biological effect-size cutoff.

### 5.3 Composition attack

Using DISCOVERY only, regress methylation and RNA feature representations on the already-frozen B1 covariates `[intercept, ABSOLUTE purity, methylation-derived leukocyte fraction]` and recompute global and semantic screens on discovery residuals.

Regression coefficients are discovery-only. The composition attack is used to construct the discovery audit state; it is not a fitted transformation of held-out target values.

If the required frozen covariates are unavailable for a cancer, composition robustness is `NOT_EVALUABLE` and the cancer cannot receive the strongest ACCEPT state.

### 5.4 Technical attack

Repeat the discovery global and semantic screens on PRIMARY_PUBLICATION and MASKED_TECHNICAL using identical discovery participants and identical decision logic.

A primary-only favorable result that does not agree on MASKED_TECHNICAL is technically unstable and cannot receive the strongest ACCEPT state.

## 6. Frozen discovery states

The methodological state is fixed from DISCOVERY only and is never revised using REPLICATION or FINAL_HOLDOUT.

- `NO_SHARED_STRUCTURE`: global sharing is not detected on PRIMARY_PUBLICATION and no stronger cross-layer state is licensed.
- `WITHIN_LAYER_ONLY`: at least one layer shows construction-aware within-layer organization, but cross-layer global sharing is not detected.
- `GLOBAL_SHARED_ONLY`: global sharing is detected, but the semantic label-specific and patient-specific criteria are not both met.
- `SEMANTIC_SHARED_CONFOUNDED`: raw semantic criteria are met on both technical tracks, but the composition-adjusted semantic criteria fail or are not evaluable.
- `SEMANTIC_SHARED_ROBUST`: global and semantic criteria are met on raw and composition-adjusted analyses and agree in direction/status on both PRIMARY_PUBLICATION and MASKED_TECHNICAL.

A technical-track disagreement is retained as a reason code and is mapped to CAUTION rather than promoted to robust sharing.

Decision class:

- `ACCEPT`: `SEMANTIC_SHARED_ROBUST` only;
- `CAUTION`: `GLOBAL_SHARED_ONLY`, `SEMANTIC_SHARED_CONFOUNDED`, or a technically unstable otherwise-favorable state;
- `REFUSE`: `NO_SHARED_STRUCTURE` or `WITHIN_LAYER_ONLY`.

These are methodological prediction/refusal states, not cancer classes, disease stages, or treatment labels.

## 7. P1 direct cross-layer prediction

### 7.1 Prediction task

Within each fully evaluable cancer, use all discovery-fit methylation Hallmark PC1 scores as source variables and the two allowed B1 composition covariates as additional predictors.

Predict the vector of discovery-fit RNA Hallmark PC1 target scores.

The primary model is multi-output ridge regression.

### 7.2 Model fitting

- standardize source variables using discovery means and standard deviations only;
- retain zero-variance discovery predictors only as zero-information columns or remove them deterministically before fitting, with the removed list recorded;
- fixed ridge alpha grid: `[1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100, 1000]`;
- select alpha by 5-fold discovery-only cross-validation;
- discovery folds are assigned by SHA-256 of `GRI_V2_PREDICTION_P0_20260830|CV|<cancer>|<participant_root>` modulo 5;
- no REPLICATION or FINAL_HOLDOUT value may choose alpha, features, scaling, or dimensionality.

### 7.3 P1 baselines

Score the same held-out targets with:

1. `MEAN_ONLY`: discovery target mean;
2. `COVARIATE_ONLY`: ridge using only the two frozen B1 covariates;
3. `SAME_HALLMARK_ONLY`: separate ridge models using the matched methylation Hallmark score plus the two covariates for each RNA Hallmark;
4. `ALL_METHYLATION_RIDGE`: the primary all-Hallmark source model.

The audit/refusal state does not alter the fitted predictor. Its value is tested separately in P3 by selective prediction.

### 7.4 P1 scoring

For every cancer and Hallmark, report held-out `R2` relative to the discovery target mean and normalized mean squared error using the discovery target variance as denominator. Negative R2 is retained.

Aggregate within cancer by the median across eligible Hallmarks. Pan-cancer comparison uses cancer as the inferential unit and an exact paired one-sided sign test for improvement over `COVARIATE_ONLY`, separately in REPLICATION and FINAL_HOLDOUT.

No positive-effect-size minimum is invented after inspection. Fewer than 24 evaluable cancers makes the pan-cancer result descriptive only.

## 8. P2 prospective replication prediction

The DISCOVERY audit state is a frozen prediction of what will reproduce in REPLICATION.

Recompute the same state machinery independently on REPLICATION using discovery-frozen feature sets/loadings and the same thresholds/null counts. REPLICATION is evaluation only and may not refit discovery transformations or change state rules.

Primary P2 outputs:

- exact five-state agreement rate;
- ACCEPT versus non-ACCEPT replication confusion matrix;
- precision, recall, specificity, balanced accuracy, and Matthews correlation for discovery ACCEPT predicting replication ACCEPT;
- per-cancer fraction of Hallmark-level semantic relationships preserving positive patient and label effects.

If a metric is mathematically undefined because only one class occurs, record `NOT_EVALUABLE`; do not invent smoothing to make it finite.

P2 comparators:

- `GLOBAL_ONLY`: discovery global CKA screen without semantic, composition, or technical logic;
- `NAIVE_SEMANTIC`: discovery same-Hallmark correlation with patient alignment but without the Hallmark-label null;
- the full narrowed audit state.

REPLICATION does not authorize architecture tuning. Any architecture change after P2 requires a new version and the current FINAL_HOLDOUT remains sealed for that new version unless its rules were frozen before access.

## 9. P3 selective prediction / refusal

Use the unchanged discovery-trained `ALL_METHYLATION_RIDGE` predictor on FINAL_HOLDOUT.

Group cancer-Hallmark prediction errors by the discovery-frozen decision class ACCEPT / CAUTION / REFUSE.

Primary risk for a cancer-Hallmark unit is final-holdout mean squared error divided by the discovery target variance. Report the full distribution and retain extreme/negative-performance cases.

Fixed coverage-risk views:

1. ACCEPT only;
2. ACCEPT + CAUTION;
3. all units.

Primary selective-prediction question:

> Does the frozen audit state place lower-risk cross-layer predictions in ACCEPT and higher-risk predictions in REFUSE, without using final-holdout target values to construct the state?

For cancers containing both classes, compare the cancer-median REFUSE risk with cancer-median ACCEPT risk using an exact one-sided sign test. A pan-cancer promoted selective-prediction statement requires at least 24 evaluable cancers; otherwise the result is descriptive.

Comparator selectors:

- `ALWAYS_PREDICT`: no refusal;
- `GLOBAL_ONLY`: accept when the frozen discovery global CKA screen passes;
- `NAIVE_SEMANTIC`: accept using same-Hallmark patient-aligned correlation without the Hallmark-label null;
- `FULL_AUDIT`: the frozen ACCEPT / CAUTION / REFUSE state above.

No acceptance threshold may be changed after final-holdout errors are inspected.

## 10. Prospectively frozen component ablations

Because F4 closed NARROW, P0 must test whether retained guardrails earn their complexity.

Run these discovery-state ablations without refitting prediction targets or using held-out values to select among them:

1. `GLOBAL_ONLY`;
2. `NO_LABEL_NULL` - remove the Hallmark-label semantic attack only;
3. `NO_COMPOSITION_ATTACK` - remove B1 composition robustness only;
4. `NO_TECHNICAL_TRACK` - ignore MASKED_TECHNICAL agreement only;
5. `FULL_NARROWED_AUDIT`.

Compare each ablation on P2 replication forecasting and P3 selective-prediction risk/coverage.

A component is retained in the next tool version only if its removal worsens prospective replication prediction, selective-prediction risk, robustness, or scientifically useful traceability. A component is not retained merely because it was historically important.

Regulatory autonomy is absent from this ablation list because F4 already classified it `AUTONOMY_REDUNDANT_NARROW`.

## 11. Final-holdout firewall

FINAL_HOLDOUT may be opened only after:

- this protocol and its machine-readable config are committed;
- split-manifest generation is implemented and hash-verified;
- discovery-only preprocessing/model code passes regression tests;
- audit-state code passes synthetic/regression tests;
- P1/P2/P3 scoring code is fixed;
- the repository records that REPLICATION results did not alter the frozen P0 architecture.

If any scientific rule is changed after REPLICATION is inspected, the change creates a new predictive version. The current final holdout cannot be used as if it had remained prospective for the changed rule.

## 12. No post-result rescue

After any P0 target values are inspected, do not change:

- participant partition assignments;
- source or target molecular definitions;
- PROMOTER_CORE primary stratum;
- Hallmark/probe mappings;
- discovery probe-completeness or imputation rules;
- global or semantic decision thresholds;
- null counts;
- composition covariates;
- technical mask;
- model family or ridge alpha grid;
- CV fold rule;
- audit states or ACCEPT / CAUTION / REFUSE mapping;
- P1/P2/P3 metrics;
- component ablation definitions;
- 24-cancer promotion floor.

Failures remain failures.

## 13. Claim ceiling

P0 can establish only prospective cross-layer prediction, replication forecasting, selective-prediction/refusal behavior, and component utility within the frozen matched PanCanAtlas setting.

It cannot establish clinical utility, treatment response, causality, substrate inheritance, temporal dynamics, recoverability, damping, an exceptional point, a cancer optimum, biological chi, or generalization beyond TCGA.

External independent validation remains mandatory before general tool promotion.
