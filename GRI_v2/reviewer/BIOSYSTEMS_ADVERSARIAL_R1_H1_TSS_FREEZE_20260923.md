# BioSystems adversarial Round 1 - H1 tissue-source-site preserving null freeze

**Date:** 23 September 2026
**Status:** FROZEN BEFORE TSS-PRESERVING OUTCOME
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Role:** post-result P0-Q adversarial sensitivity. Cannot retroactively promote C1.

## Motivation

Round-1 review correctly identifies acquisition center/site and batch-like structure as alternatives capable of inducing cross-probe covariance.

The public PanCan methylation matrix does not expose a complete plate/slide/batch field in the present frozen source lineage. However, every TCGA participant barcode contains a source Tissue Source Site (TSS) code. TSS is therefore a source-identifiable grouping that can be challenged without inventing metadata.

## Question

Does H1 remain above a null that preserves:

1. linear CpG structure explained by ABSOLUTE purity;
2. linear CpG structure explained by methylation-derived leukocyte fraction; and
3. linear CpG mean differences associated with TCGA TSS groups;

while independently destroying residual cross-patient covariance within each CpG?

## Frozen source / cohort

Inherit exactly from the completed Round-1 H1 composition sensitivity:

- exact methylation SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- exact purity SHA-256 `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`;
- exact leukocyte SHA-256 `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`;
- exact 22,601 C1 probe carrier;
- exact quality/source identity logic;
- 30 composition-complete cancers;
- n=30 per draw;
- 20 deterministic draws per cancer.

No cancer, sample, probe or outcome may select the TSS rule.

## TSS encoding

For participant `TCGA-XX-YYYY`, TSS is the exact second barcode token `XX`.

Within each draw:

1. count TSS levels;
2. levels represented by >=3 selected participants receive their own indicator;
3. all levels represented by <3 selected participants are combined into the frozen label `RARE_TSS`;
4. one category is omitted deterministically by lexicographic first category as the reference;
5. design = intercept + standardized purity + standardized leukocyte fraction + TSS indicators;
6. if design rank is deficient or residual degrees of freedom <10, the draw is `NOT_EVALUABLE_TSS_DESIGN`.

The >=3 rule and residual-df floor are frozen before outcome.

## Primary null

Per retained CpG:

- fit the frozen design;
- retain the fitted matrix exactly;
- independently permute residuals across the 30 patients using a deterministic CpG-wise permutation;
- reconstruct `fitted + permuted residual`;
- compute the same spectral concentration.

Primary draw effect:

`delta_comp_tss_preserved = S_raw - S_null(comp+TSS)`.

Cancer summary = median across valid draws.

Global inference = two-sided exact sign test across cancer medians.

## Secondary conventional comparator

Using the same centered sample Gram spectrum, also report ordinary PC1 variance fraction:

`PC1_fraction = lambda_1 / sum(lambda)`.

Compute raw and composition+TSS-preserving-null PC1 fraction and their difference.

This is a standard PCA concentration comparator. It is secondary and does not replace H1.

## Decision

- `R1_H1_COMP_TSS_ROBUST`: primary median >0 and exact sign p<0.05;
- `R1_H1_COMP_TSS_SENSITIVE`: otherwise;
- `R1_H1_COMP_TSS_HOLD`: <20 cancers evaluable or source/identity failure.

## Claim ceiling

A PASS means linear effects of the two measured composition variables plus TSS-associated CpG mean shifts are not sufficient to explain H1 under this null.

It does **not** establish:
- full batch independence;
- plate/slide independence;
- absence of within-TSS technical effects;
- composition independence beyond the two measured axes;
- subtype/age/sex/ancestry independence;
- mechanism.
