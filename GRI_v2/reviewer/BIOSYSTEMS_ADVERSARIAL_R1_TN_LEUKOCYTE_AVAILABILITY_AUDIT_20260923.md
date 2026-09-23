# BioSystems adversarial Round 1 - tumor-normal leukocyte availability audit

**Date:** 23 September 2026
**Status:** CLOSED / NO SYMMETRIC LEUKOCYTE ROUTE
**Branch:** `biosystems-adversarial-r1-20260923`
**Freeze:** `BIOSYSTEMS_ADVERSARIAL_R1_TN_LEUKOCYTE_AVAILABILITY_FREEZE_20260923.md`
**Workflow:** `35815627669`
**Artifact:** `BIOSYSTEMS_ADVERSARIAL_R1_TN_LEUKOCYTE_AVAILABILITY_V01`
**Artifact ID:** `10731146689`
**Artifact digest:** `sha256:ef5f4dd43fcc6ccefc79e61adcfecd618c6164effcd61e4dc2120f824672a227`
**Source SHA-256:** `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`

## Question

Can the frozen PanCanAtlas methylation-derived leukocyte fraction provide a symmetric type-01/type-11 composition sensitivity for the tumor-normal RNA result?

No RNA or methylation architecture values were opened in this source-availability gate.

## Result

Under the prospectively frozen availability rules:

- TN-A1 cancers with >=30 finite tumor and >=30 finite normal leukocyte values: **0/12**;
- TN-P20 cancers with >=20 same-participant tumor/normal finite leukocyte values: **0/13**.

Machine disposition:

`NO_SYMMETRIC_LEUKOCYTE_ROUTE`

## Interpretation

The only existing composition variable with a plausible symmetric interpretation across tumor and adjacent tissue is not available with the coverage required by the frozen TN designs.

ABSOLUTE purity is tumor-defined and cannot be transplanted to type-11 adjacent tissue as though it represented the same biological quantity.

Therefore a composition-adjusted TN-A1/TN-P20 contrast cannot be constructed honestly from the existing frozen PanCanAtlas composition sources.

This does **not** remove the confound. It establishes that the requested adjustment is not identifiable from the current source.

## What can still be said

The tumor-normal RNA result remains:

- a strong unadjusted tissue-state contrast;
- reproduced directionally across all 12 primary cancers and the 13-cancer paired sensitivity;
- broad across Hallmarks in the post-hoc breadth audit;
- not established as tumor-cell-intrinsic;
- not established as composition-independent.

The paired-patient lane controls participant identity, not tissue composition.

## Manuscript consequence

Use language equivalent to:

> Tumor-normal RNA contrasts were not composition-adjusted because the frozen tumor composition covariates do not have a symmetric type-11 interpretation, and the exact methylation-derived leukocyte source did not provide sufficient type-11 coverage for a matched adjustment. The observed shift therefore remains an unadjusted tissue-state association. Its broad Hallmark distribution argues against concentration in a small immune-module subset but does not exclude broader tissue-composition effects.

## Future route

A deeper deconvolution method may be evaluated in a separately frozen analysis only if:
- it is valid on both type-01 and type-11 tissue;
- the same source/feature model is applied symmetrically;
- the deconvolution is not tuned to reproduce the current TN direction.

It is not required to rescue this revision if the present claim is kept at the unadjusted-state-contrast ceiling.

## Final disposition

`SYMMETRIC_TN_COMPOSITION_ADJUSTMENT_FROM_FROZEN_SOURCE = NOT_IDENTIFIABLE`

`TN_RNA_COMPOSITION_INDEPENDENCE = NOT_CLAIMED`
