# GRI native comparator candidate survey

**Date:** 2026-09-10  
**Status:** P0-D COMPARATOR-SOURCE SURVEY, NOT A COMPARATOR FREEZE  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Purpose

Identify serious domain-native comparator classes for future GRI questions before any external P1 comparator is selected. This is a good-faith comparator-selection-route input, not a declaration that one method is already the strongest fair comparator for every GRI task.

The comparator must be selected for the **frozen scientific question**, not because it is easy to beat or because another method is globally popular.

Retrieval date: 2026-09-10.

## 1. Comparator question must be task-specific

GRI currently contains at least three distinct comparison questions that must not be conflated:

1. **Structural integration question:** does the GRI architecture add useful audit/refusal/semantic/context information beyond established shared/private multi-omic geometry methods?
2. **Cross-layer prediction question:** can methylation-derived information predict RNA expression/Hallmark state on untouched samples better or more usefully than strong native predictive alternatives?
3. **Selective-prediction / confidence question:** does a predeclared GRI confidence coordinate rank future prediction risk or improve coverage-risk beyond strong non-GRI confidence measures?

A comparator suitable for one question may be irrelevant to another.

## 2. Structural integration comparator family

### Existing GRI evidence

F3 already evaluated:

- AJIVE;
- MOFA2;
- strong simple geometry/prediction baselines;
- DIVAS under a pinned published implementation, which remained `NOT_EVALUABLE` rather than being replaced by a weaker method.

This existing comparison establishes that global geometry and shared/private modal decomposition are established primitives. It does not complete the predictive comparator problem.

### Additional literature context

A cancer multi-omics benchmarking review compared simple early concatenation/PCA with MOFA2, DIABLO, iCluster variants, and moCluster on common tasks. It reported that specialized unsupervised integration did not automatically outperform simple PCA/concatenation, while supervised DIABLO performed strongly when label information was available.

Source of record:

- Picard et al./review: `Machine learning for multi-omics data integration in cancer`, PMC8829812.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8829812/

**Implication:** a future GRI structural added-value claim must include strong simple baselines as well as established integrators. Complexity is not itself evidence of added value.

## 3. Direct methylation-to-expression predictive comparators

These are especially relevant to the current GRI cross-layer predictive task because they directly model gene expression from DNA methylation.

### 3.1 geneEXPLORE / geneEXPLORER family

Source of record:

- `Collective effects of long-range DNA methylations predict gene expressions and estimate phenotypes in cancer`, PMC7054398.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7054398/

Verified methodological facts:

- predicts gene expression from methylation;
- uses high-dimensional penalized regression including elastic-net/ridge behavior after methylation feature screening;
- evaluates held-out prediction;
- includes an independent-cohort test after TCGA training.

**Comparator relevance:** high for a frozen question about whether methylation predicts RNA expression across patients.

**Mismatch to current GRI:** operates primarily gene-by-gene/feature-region rather than on the current 45-Hallmark representation. A fair comparison must decide prospectively whether the target is gene expression, Hallmark state, or both and how outputs are aggregated.

### 3.2 MethCORR

Sources of record:

- `MethCORR infers gene expression from DNA methylation and allows molecular analysis of ten common cancer types using fresh-frozen and formalin-fixed paraffin-embedded tumor samples`, PMC7842045 / PMID 33509261.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7842045/
  https://pubmed.ncbi.nlm.nih.gov/33509261/

Verified methodological facts:

- explicit aim is to infer RNA expression from DNA methylation;
- regression models were developed from matched RNA-seq and HumanMethylation450 data;
- evaluated across multiple cancer types;
- designed in part for transfer to tissue contexts where RNA is harder to measure directly.

**Comparator relevance:** high for external methylation-to-RNA prediction.

**Mismatch to current GRI:** method and output granularity differ from Hallmark PC1 prediction, so a same-task transformation/evaluation protocol would have to be frozen before comparison.

### 3.3 Penalized regression family: Ridge / Lasso / ElasticNet

Source of record:

- `Genomic Effect of DNA Methylation on Gene Expression in Colorectal Cancer`, PMC9598958.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9598958/

Verified methodological facts:

- directly compared Lasso, Ridge, ElasticNet, and Bslmm for prediction of gene expression from CpG methylation;
- evaluated prediction with cross-validation and error/R2 metrics;
- ElasticNet had the strongest median performance in that study's tested setting.

**Comparator relevance:** very high as a transparent standard predictive family.

**Important constraint:** one study's winner is not automatically the strongest comparator for the GRI task. Hyperparameter tuning, feature support, output dimensionality, and training/evaluation splits must be matched prospectively.

## 4. Cross-block association / latent-space comparators

### 4.1 sparse / joint sparse CCA

Sources of record:

- `Joint Detection of Associations between DNA Methylation and Gene Expression from Multiple Cancers`, PMC6310112 / PMID 29990049.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6310112/
  https://pubmed.ncbi.nlm.nih.gov/29990049/

Verified methodological facts:

- applies joint sparse canonical correlation analysis to methylation and gene expression across cancers;
- targets shared and cancer-group-specific multivariate methylation-expression associations;
- follows association modules with sparse precision estimation.

**Comparator relevance:** high for the structural/cross-layer association question, potentially less direct for the exact current multi-output prediction task unless a predictive evaluation is specified.

### 4.2 MOFA / MOFA2

Sources of record:

- multi-omics integration reviews and GRI's own already-completed F3 comparison.

**Comparator relevance:** established latent-factor integration/shared-structure comparator.

**Current GRI disposition:** already used to constrain novelty. Not sufficient alone as the strongest comparator for methylation-to-RNA supervised prediction.

### 4.3 DIABLO / supervised sGCCA family

Sources of record:

- multi-omics integration review PMC8829812;
- `A guide to multi-omics data collection and integration for translational medicine`, PMC9747357.

Verified methodological facts:

- DIABLO is a supervised multi-block integration method based on sparse generalized canonical correlation concepts;
- it is designed to maximize cross-block covariance while predicting a supervised response/class.

**Comparator relevance:** potentially high for supervised phenotype/classification tasks involving multi-omics.

**Task mismatch warning:** current GRI P0 prediction is methylation -> RNA Hallmark state, not primarily phenotype classification. DIABLO should not be chosen merely because it is a prominent supervised multi-omics tool if it does not address the frozen task fairly.

## 5. Same-capacity non-Hallmark controls

The September 8 GRI manuscript/supplement already recognized a narrower internal question:

> Does Hallmark-structured methylation representation add predictive information beyond an equal-dimensional non-Hallmark methylation representation?

The exact previously referenced frozen post-FINAL control has not been recovered as an executable identity.

A **new** P0-Q control, if scientifically authorized, could consider transparent same-capacity constructions such as:

- unsupervised methylation PCA with the same retained predictor dimension;
- random orthonormal/projection controls with dimension matched prospectively;
- unsupervised data-driven methylation factors with equal predictor count;
- probe-level or gene-level penalized models constrained to a prospectively matched effective capacity.

This list is an option space, **not a design decision**. Choosing which one is fair, how dimension/effective capacity is matched, and what tuning budget each receives is scientifically consequential and requires a separately documented freeze/review.

## 6. Comparator-selection route recommended by the protocol

Before future P1 external evaluation:

1. freeze the exact scientific question and value axis;
2. conduct/update a good-faith literature/benchmark survey specific to that question;
3. identify the strongest plausible native comparator candidates;
4. document task compatibility and mismatch for each;
5. freeze the selection route before inspecting decisive external performance;
6. give the selected comparator comparable access to training/calibration information and a fair tuning budget;
7. use the same untouched decisive evaluation split where technically possible;
8. predeclare the metric and what result counts as `ADDS`, `EQUIVALENT`, `SUBTRACTS`, `INDETERMINATE`, or `NOT_TESTED`;
9. if no established comparator actually addresses the exact task after the frozen search, use `NO_NATIVE_COMPARATOR` and retain the strongest domain-native null/alternative rather than inventing a straw baseline.

## 7. Current comparator audit conclusion

### Structural integration / audit question

`COMPARATOR_IDENTIFIED = YES`

AJIVE, MOFA2, simple geometry/predictive baselines, and task-appropriate CCA/sCCA families provide established comparisons. Existing F3 already narrows GRI novelty substantially.

### Methylation-to-RNA prediction question

`COMPARATOR_CANDIDATES_IDENTIFIED = YES`

Serious candidates include direct penalized regression, MethCORR/geneEXPLORE-type methylation-to-expression approaches, and task-specific latent/cross-block methods.

`STRONGEST_FAIR_COMPARATOR_FROZEN = NO`

That cannot be resolved until the future external question/output granularity is frozen and the historical equal-dimensional post-FINAL control provenance is either recovered or formally closed.

### Selective-prediction confidence question

`STRONGEST_FAIR_COMPARATOR_FROZEN = NO`

A future test should compare the GRI confidence rule against simple non-GRI confidence/uncertainty measures derived without outcome leakage, but the exact comparator cannot be chosen after external risk-ranking results are seen.

## 8. Current stop boundary

This survey may inform a later comparator freeze. It must not itself be treated as the freeze.

**No new comparator has been selected, tuned, or evaluated against external GRI outcomes by this P0-D survey.**