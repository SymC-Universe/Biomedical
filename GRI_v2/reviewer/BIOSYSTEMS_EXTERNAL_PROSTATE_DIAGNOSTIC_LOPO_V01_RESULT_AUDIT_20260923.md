# BioSystems external prostate diagnostic LOPO v0.1 result audit

**Date:** 23 September 2026  
**Status:** `P0_D_COMPLETE__TISSUE_STATE_DISCRIMINATION_NOT_SUPPORTED`  
**Workflow run:** `35893167138`  
**Workflow head:** `43193648055024499fae7b8de45bfb2e9091d493`  
**Artifact:** `10765533008`  
**Artifact digest:** `sha256:26aee3e13056e6acb3dd11b71b10cfee52233f08efe5b3b89e2a8fc343a544e2`

## Frozen design

Independent prostate 450K source:
- GEO `GSE262522`;
- exact frozen source SHA-256 `90a7a8c12343831524a9711be7e0b3f33f297fe408662fa68c5efa49a7c862d0`;
- 32 complete tumor/adjacent participant pairs;
- exact frozen 22,601 C1 probe carrier.

Patient-level diagnostic object was defined prospectively as a conventional training-only methylation PC1, not the cohort-level H1 statistic.

Cross-validation:
- leave one participant pair out;
- feature eligibility, imputation, centering, scaling, PC1 loading and orientation fit only on the remaining 31 pairs;
- held-out tumor and adjacent sample projected with the frozen training transform.

Simple comparator:
- global mean methylation over the same training-eligible probes;
- orientation learned in training only.

## Result

PC1:
- concordant held-out pairs: **9/32**;
- exact one-sided Binomial(32,0.5) p = **0.9964998167**;
- descriptive out-of-fold AUC = **0.25293**.

Global mean methylation comparator:
- concordant pairs: **19/32**;
- exact one-sided p = **0.1885427937**.

Direct comparator:
- PC1-only correct pairs: 1;
- mean-only correct pairs: 11;
- one-sided paired discordance p for PC1 superiority = **0.9997558594**.

Frozen primary support rule: **FAIL**.  
PC1 added value over the simple comparator: **FAIL**.

## Interpretation

The current H1 recurrence must not be converted into a patient-level diagnostic-biomarker claim. A straightforward training-only methylation PC1 derived from the same C1 carrier does not discriminate tumor from matched adjacent tissue out of sample in this external prostate cohort.

This negative result does not imply that no methylation biomarker can classify prostate tissue. It specifically rejects the tested architecture-derived PC1 route and prevents post-result classifier shopping in this cohort.

## Claim consequence

- diagnostic utility: **NOT ESTABLISHED**;
- exploratory architecture-derived tissue-state discrimination: **NOT SUPPORTED** in the frozen test;
- no additional classifier is opened on the same cohort for the current revision.
