# BioSystems adversarial Round 1 - external prostate metadata/technical audit

**Date:** 23 September 2026
**Status:** CLOSED / NO ADDITIONAL IDENTIFIABLE TECHNICAL COVARIATES
**Branch:** `biosystems-adversarial-r1-20260923`
**Freeze:** `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_METADATA_FREEZE_20260923.md`
**Workflow:** `35815335966`
**Artifact:** `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_METADATA_V01`
**Artifact ID:** `10731351466`
**Artifact digest:** `sha256:5d055b08611a8191024efb8337d62ffb87bbd2f14ec8ca66521513abb8d6fb39`

## Question

Round-1 review identified age, sex, center, batch, plate, Sentrix/slide position and related structured metadata as possible explanations for the large external H1 effect. This gate asked which of those variables are actually exposed by the public GEO source metadata with enough coverage to support a prespecified sensitivity.

No methylation beta values, RNA counts or GRI outcomes were opened in this audit.

## Identity closure

All frozen tumor samples were recovered uniquely from source metadata:

- primary 450K n=30: 30/30;
- complete 450K n=32 sensitivity: 32/32;
- EPIC n=26 sensitivity: 26/26.

No frozen participant was missing and no frozen participant had a nonunique tumor metadata match.

## Adjustment-candidate result

Under the prospectively frozen metadata eligibility rules, the only primary-n30 field qualifying as an adjustment candidate was:

- `race`: 100% coverage, two supported categories.

Race had already been challenged independently in the completed Round-1 H1 race sensitivity.

The public GEO series-matrix metadata did **not** expose an additional age, sex, center/site, plate, Sentrix/slide, array-position, scan-batch or comparable technical field that satisfied the frozen source-meaning, coverage and support rules.

Final disposition:

`NO_ADDITIONAL_IDENTIFIABLE_TECHNICAL_COVARIATES`

## Interpretation

This is a source limitation, not evidence that such confounding is absent.

What is now ruled out as a sufficient explanation:
- pooled tumor/adjacent state in the primary P1 endpoint;
- the source-declared AA/EA race label;
- the two measured TCGA composition axes in the independent internal H1 composition attack.

What remains unresolved for the external cohort:
- unrecorded or unavailable processing batch;
- plate/slide/array position;
- collection center/site;
- age/sex if not exposed in the frozen public metadata;
- molecular subtype;
- latent cell-state composition;
- unmeasured ancestry structure;
- other structured covariance.

Therefore the manuscript may state that no further **source-identifiable** external technical covariate was available under the frozen audit, but it may not state that H1 is batch-independent or fully composition-independent.

## Reviewer consequence

The correct response is not to invent covariates or fit undocumented sample groupings. The external H1 claim remains bounded to:

> within-methylation spectral organization above the frozen construction floor transported to an independent prostate cohort and a second methylation platform; the effect is not explained by pooled tissue state or source-declared race, while broader latent technical and biological covariance remains a limitation.

## Claim ceiling

This audit does not explain why the external H1 effect magnitude exceeds the internal C1 median, and it does not upgrade the biological interpretation of H1.
