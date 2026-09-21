# GRI conglomerate v0.1 native comparator candidate map

**Date:** 2026-09-21  
**Status:** PRE-SELECTION / LITERATURE-INFORMED COMPARATOR MAP  
**Rule:** this document maps fair comparator families; it does not select the final MFR-05 comparator before the exact task is frozen.

## 1. Comparator principle

A comparator is fair only if it answers the same frozen question with the same information budget. A method that performs clustering is not a fair one-step forecast comparator merely because it is famous, and a supervised classifier is not a fair unsupervised representation comparator.

## 2. Task-by-task candidate map

| Frozen function to be tested | Minimum simple comparator | Established native candidates | Current GRI candidate | Key fairness issue |
| --- | --- | --- | --- | --- |
| unsupervised multi-view representation | scaled concatenation + PCA | MCIA / RGCCA, MOFA2; SNF if the task is similarity-network clustering | capital-Chi block carrier / geometry | same samples, same preprocessing, no outcome leakage |
| cross-view association / geometry | CCA or regularized CCA; permutation-tested RV/CKA | MCIA/RGCCA, kernel alignment | CKA + modal/conglomerate relations | compare debiased as well as current CKA in low-n/high-p settings |
| supervised diagnostic classification | concatenation + regularized logistic/elastic-net model | DIABLO/sGCCA; other task-specific supervised integrators after literature freeze | task-specific Chi head | labels used only inside training folds; identical outer splits |
| continuous cross-omic prediction | covariate-only + ridge/elastic net | PLS/regularized CCA/multiblock PLS where same-question appropriate | retained all-methylation ridge plus future blocks | identical target, split, feature availability and tuning budget |
| missing-view representation | complete-case simple baseline plus explicit missingness indicator analysis | MOFA2 or another method explicitly supporting missing values/views | explicit missing-block carrier | complete-case result cannot be called unbiased without missingness assumptions |
| temporal pattern description in SCC25 | source paper's reported CoGAPS structure | CoGAPS / other prespecified time-course factor method | R/M/T partial Chi architecture | source-native question is description of evolving molecular programs |
| one-step temporal prediction/system ID | persistence + arm-specific mean | DMD/DMDc, reduced-rank/state-space model | G2 D1/D2 | forecast on the same left-out transitions, same state representation |
| treatment-associated operator reorganization | shared-T restricted model | DMDc / time-varying or interaction state-space alternative | G2 D2 | "no support" is model-specific, not no biological reorganization |
| predictive confidence / selective risk | sample size, model residual/uncertainty, conventional calibration/selective-risk statistic | task-specific uncertainty method chosen before test | GLOBAL_GEOMETRY_CONFIDENCE | CKA is not natively a calibrated uncertainty measure |
| tumour composition sensitivity | ABSOLUTE purity + leukocyte as existing simple attack | benchmark-qualified deconvolution such as EPIC/CIBERSORTx/BayesPrism family | E block | one method must be frozen from data compatibility and benchmark evidence, not favorable output |

## 3. Literature basis

- Rappoport & Shamir 2018, DOI 10.1093/nar/gky889: no single multi-omic clustering/integration method dominated all criteria.
- Cai et al. 2022, DOI 10.1016/j.isci.2022.103798: early concatenation and PCA can match or outperform specialized integrators depending on the task; DIABLO was strong for supervised cancer-type classification while early concatenation led their drug-response benchmark.
- Singh et al. 2019, DOI 10.1093/bioinformatics/bty1054: DIABLO is a supervised multi-omics latent-component method.
- MOFA/MOFA2 documentation and Argelaguet et al. 2020, DOI 10.1186/s13059-020-02015-1: unsupervised latent-factor multi-view integration and missing-value support.
- Stein-O'Brien et al. 2018, DOI 10.1186/s13073-018-0545-2: the exact SCC25 chronic source was originally analyzed with CoGAPS.
- Schmid 2010, DOI 10.1017/S0022112010001217 and Proctor et al. 2016, DOI 10.1137/15M1013857: reduced operator/DMD and controlled operator identification are established prior art.

## 4. Freeze rule

The final comparator suite is chosen only after the task is explicit:

`input modalities -> target -> split/holdout -> missingness mode -> preprocessing -> tuning budget -> metric -> comparator family`.

Only then can the project use the GOM outcome labels:

`ADDS_OVER_STANDARD_TOOLKIT`, `EQUIVALENT_TO_STANDARD_TOOLKIT`, `SUBTRACTS_FROM_STANDARD_TOOLKIT`, or `NOT_TESTED_AGAINST_STANDARD_TOOLKIT`.

At the present state, capital-Chi v0.1 is:

`NOT_TESTED_AGAINST_STANDARD_TOOLKIT`.
