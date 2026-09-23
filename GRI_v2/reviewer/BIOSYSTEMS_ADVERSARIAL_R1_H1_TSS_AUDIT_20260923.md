# BioSystems adversarial Round 1 - H1 composition + TCGA Tissue Source Site audit

**Date:** 23 September 2026
**Status:** CLOSED / R1_H1_COMP_TSS_ROBUST
**Branch:** `biosystems-adversarial-r1-20260923`
**Freeze:** `BIOSYSTEMS_ADVERSARIAL_R1_H1_TSS_FREEZE_20260923.md`
**Workflow:** `35815819898`
**Artifact:** `BIOSYSTEMS_ADVERSARIAL_R1_H1_TSS_V01`
**Artifact ID:** `10731877118`
**Artifact digest:** `sha256:d8d953f7803e8dd048a85a6bb96298315dcfd4c9eff38bd3b400731386cb4e70`

## Question

Does H1 remain above a stronger null that preserves:
- linear CpG structure explained by ABSOLUTE purity;
- linear CpG structure explained by methylation-derived leukocyte fraction; and
- TCGA Tissue Source Site (TSS)-associated CpG mean structure;

while independently destroying residual patient covariance within each CpG?

This is a post-result Round-1 adversarial sensitivity and cannot retroactively promote C1.

## Result

All 30 composition-complete cancers were evaluable.

### H1 spectral concentration

- positive cancer medians: **30/30**
- negative: **0/30**
- ties: **0**
- pan-cancer median `delta_comp_tss_preserved`: **+0.0816210492**
- IQR: **0.0595816872 to 0.0951032242**
- exact two-sided sign-test p: **1.862645149230957e-09**

Disposition:

`R1_H1_COMP_TSS_ROBUST`

### Conventional PCA comparator

The same centered sample-Gram spectrum was summarized by ordinary PC1 variance fraction and compared with the identical composition+TSS-preserving null.

- positive cancer medians: **30/30**
- negative: **0/30**
- ties: **0**
- pan-cancer median raw-minus-null PC1 fraction: **+0.0685775794**
- exact two-sided sign-test p: **1.862645149230957e-09**

Thus the stronger result is not unique to the entropy-derived H1 scalar; a conventional leading-component concentration summary shows the same direction against the same frozen null.

## Interpretation

The original H1 construction floor remains weak by design: independent within-CpG patient permutation destroys all cross-probe covariance.

Round-1 attacks now establish that the H1 direction is not sufficiently explained by:
1. each CpG's marginal sampled distribution;
2. the two measured linear composition axes (ABSOLUTE purity and methylation-derived leukocyte fraction);
3. TCGA TSS-associated CpG mean shifts; or
4. the specific prespecified technical-probe mask.

The H1 signal also has a conventional PCA analogue under the stronger null.

## What remains unresolved

This test does **not** establish full technical or biological independence. It does not preserve or remove:
- plate;
- Sentrix/slide/array position;
- processing batch unavailable in the frozen public lineage;
- within-TSS acquisition differences;
- age/sex effects not source-bound in the external cohort;
- subtype/histology;
- deeper stromal/immune deconvolution;
- unmeasured ancestry;
- nonlinear composition structure.

The separate external metadata audit found that those additional prostate technical covariates were not identifiable from the public GEO metadata under the frozen rules.

## Reviewer consequence

H1 should no longer be defended primarily by the canonical independent-CpG floor. The manuscript should state both layers:

1. canonical C1 H1 is defined relative to an exact independence/construction floor;
2. post-result adversarial controls preserve measured composition and TSS structure and still show a positive 30/30 pan-cancer H1 excess.

This directly addresses the concern that the only externally transported endpoint was also the least protected against measured composition/center-like structure.

## Claim ceiling

The supported claim remains **recurrent within-methylation organization above specified construction and measured-confound-preserving nulls**.

Do not upgrade this to:
- a tumor-cell-intrinsic mechanism;
- complete batch independence;
- complete composition independence;
- causal epigenetic regulation;
- a universal biological stability coordinate.
