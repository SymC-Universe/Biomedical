# BioSystems adversarial Round 1 H1 measured-composition audit

**Date:** 23 September 2026  
**Status:** COMPLETE / POST-RESULT P0-Q ADVERSARIAL SENSITIVITY  
**Parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`  
**Round-1 branch:** `biosystems-adversarial-r1-20260923`  
**Workflow:** `35812910672`  
**Artifact:** `BIOSYSTEMS_ADVERSARIAL_R1_H1_COMPOSITION_V01`  
**Artifact ID:** `10730212562`  
**Artifact SHA-256:** `fce0384e972e0f9646448546afe6bbcec3dda1214dc17460b455651274319e1d`

## Question

Round-1 adversarial review correctly challenged canonical H1 because its independent within-CpG patient-permutation null destroys all cross-probe covariance and therefore does not distinguish H1 from covariance induced by measured sample composition.

A stronger post-result test was frozen before execution:

> Does raw H1 remain above a null that preserves the cross-probe covariance linearly explained by ABSOLUTE purity and methylation-derived leukocyte fraction?

This is P0-Q reviewer-round sensitivity evidence only. It cannot retroactively promote C1 or P1.

## Source and eligibility integrity

Exact sources were independently rebound at execution:

- TCGA merged methylation SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- ABSOLUTE purity SHA-256 `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`;
- methylation-derived leukocyte fraction SHA-256 `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`;
- sample-quality annotation observed SHA-256 `e3190253ccb55f9f5ccc558b7f994577b2e90c2ee306814231b7d5f077364deb`;
- inherited full RNA source identity `674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658` was used to preserve the shared-assay participant universe; only its public source header was needed for this H1-only sensitivity.

The predeclared composition-complete set reproduced exactly:

- **30 eligible cancers**;
- **DLBC and THYM below the frozen n>=30 composition-complete gate**.

No cancer entered or left based on H1 outcome.

## Construction

For each eligible cancer:

- n=30 primary tumors;
- 20 deterministic draws;
- exact 22,601 C1 probe carrier;
- within-draw >=95% finite-probe rule;
- median imputation only for retained probe missing cells;
- cancer remains the inferential unit.

For each draw every retained CpG was fit simultaneously to:

`beta = intercept + z(purity) + z(leukocyte) + residual`.

The primary null preserved the fitted composition matrix exactly, independently permuted only the per-CpG residuals across patients, then reconstructed:

`beta_compnull = fitted_composition + permuted_residual`.

The primary effect is:

`delta_comp_preserved = S_raw - S_compnull`.

Thus the null retains the patient covariance that the two measured composition covariates explain linearly and asks whether additional cross-probe patient organization remains.

## Primary result

**Disposition: `R1_H1_MEASURED_COMPOSITION_ROBUST`.**

Across the 30 frozen composition-complete cancers:

- positive cancer medians: **30/30**;
- negative: **0/30**;
- ties: **0**;
- pan-cancer median `delta_comp_preserved`: **0.0999769955**;
- IQR: **0.0727836524 to 0.1097330090**;
- exact two-sided sign-test p: **1.862645149230957e-09**.

All 30 cancers therefore remained above the measured-composition-preserving null.

The cancer-level effects are not numerically trivial. Examples include:

- KICH: +0.02101;
- THCA: +0.03237;
- READ: +0.06094;
- PRAD: +0.11406;
- ESCA: +0.15753;
- STAD: +0.16268;
- TGCT: +0.53331.

The test therefore does not depend on one extreme cancer.

## Secondary residual-only result

The separately reported residual-only H1 retained a pan-cancer median **108.6%** of the original canonical H1 excess after linear purity/leukocyte removal.

This quantity is secondary and cannot rescue the primary composition-preserving-null test.

The greater-than-100% median retention is not interpreted as biological enhancement. Removing measured composition can redistribute covariance/eigenvalue concentration and thereby alter the spectral statistic.

## Interpretation

The Round-1 reviewer concern is **partially answered, not erased**.

Supported:

> ABSOLUTE purity and methylation-derived leukocyte fraction are not sufficient to explain recurrent H1 under the tested linear composition model. H1 remained positive in 30/30 composition-complete cancers against a null that explicitly preserved covariance attributable to those two measured axes.

Not supported:

- H1 is composition independent;
- all immune/stromal variation is removed;
- batch, center, plate, array, age, sex, ancestry, molecular subtype, or other latent sample structure is excluded;
- H1 is mechanistic;
- canonical independent-CpG permutation is a comprehensive biological null;
- this post-result sensitivity upgrades the original P1 classification.

The canonical H1 construction null remains appropriately described as an **independence/construction floor**. This new P0-Q sensitivity provides a harder measured-composition attack, not a replacement history for the original C1 freeze.

## Reviewer-facing consequence

The revision should no longer defend H1 solely with the independent-CpG null.

The main paper should report both layers:

1. canonical H1 tests spectral concentration above an independence/construction floor;
2. a separately frozen post-result Round-1 sensitivity shows the effect remains above a null preserving the covariance linearly explained by ABSOLUTE purity and leukocyte fraction in 30/30 composition-complete cancers.

External prostate H1 remains a separate independent transport result. Its large magnitude is not treated as an effect-size replication claim. Pooled tissue state is excluded because external H1 was tumor-only, and the separately frozen race sensitivity shows the AA/EA source axis is not sufficient to explain the external magnitude. Other external composition and batch structure remain unresolved.
