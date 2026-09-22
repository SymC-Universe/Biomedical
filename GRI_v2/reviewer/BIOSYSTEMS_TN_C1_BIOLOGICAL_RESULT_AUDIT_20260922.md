# BioSystems TN-C1 tumor-normal biological result audit - 22 September 2026

**Status:** CLOSED / COMPLETE  
**Workflow:** GitHub Actions run `35797400570`  
**Commit:** `d02b94c43ec1c943d1137a4b1d1da1e690ca06fe`  
**Artifact:** `GRI_BIOSYSTEMS_TN_C1_RESULTS_V01`, artifact ID `10725150891`  
**Artifact digest:** `sha256:17c23bc3e5d49d2c7936f6ac5357526fa8a3ed95933dd1d0257f028bf764cf3d`  
**Protocol lineage:** `BIOSYSTEMS_TUMOR_NORMAL_PROTOCOL_LINEAGE_AUDIT_20260922.md`  
**Claim ceiling:** static tumor-versus-TCGA-solid-tissue-normal specificity/control evidence only. No causality, temporal progression, healthy-population claim, diagnostic utility, damping, exceptional-point, biological chi, or universal optimum claim.

## 1. Execution integrity

TN-C1 completed successfully for all five frozen cancers: BRCA, LIHC, PRAD, THCA, and UCEC.

Each state used n=30 with 100 deterministic draws under `GRI_BIOSYS_TN_C1_20260922`. Exact frozen source identities passed:
- RNA SHA-256 `674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658`;
- methylation SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- Hallmark raw SHA-256 `eecaf6dad908334ae885406ec72bdc0646d8917588ed7c219fac92fc5363f596`.

The final execution restored frozen participant order after pandas column selection and added duplicate/order-drift guards. No cancer set, threshold, endpoint, seed, null, track, or interpretation rule changed.

Common primary probe support remained high and symmetric: 22,506-22,582 probes across the five cancers; masked-technical support was 21,929-22,004 probes.

## 2. Primary-publication tumor-minus-normal effects

| Cancer | H1 delta_s | H2 delta_CKA | H3a delta_A_patient | H3b delta_A_label |
|---|---:|---:|---:|---:|
| BRCA | -0.1673 | +0.0226 | -0.0049 | +0.0116 |
| LIHC | -0.1000 | +0.0095 | -0.0287 | ~0.0000 |
| PRAD | -0.1367 | -0.0620 | +0.0438 | +0.0487 |
| THCA | -0.2513 | -0.3256 | -0.0300 | +0.0027 |
| UCEC | -0.1502 | -0.3486 | -0.1364 | +0.0416 |

Effects are tumor minus normal. Negative values therefore indicate lower construction-corrected organization/coupling in tumor.

## 3. H1: shared methylation organization with a consistent tumor-associated decrease

H1 `delta_s` is positive in both tumor and normal states for every cancer, but tumor is lower in 5/5 cancers.

Primary pan-cancer tumor-minus-normal median: **-0.15023**.
Direction count: 0 positive / 5 negative.
Exact two-sided sign-test p = 0.0625; BH q = 0.125.

The per-cancer deterministic-draw q05-q95 intervals for tumor-minus-normal H1 are entirely below zero in all five cancers:
- BRCA: -0.2449 to -0.1041;
- LIHC: -0.1459 to -0.0591;
- PRAD: -0.1696 to -0.0774;
- THCA: -0.2935 to -0.2040;
- UCEC: -0.1760 to -0.1259.

The masked-technical track independently reproduces the direction in 5/5 with median -0.15307.

**Disposition:** strong consistency/effect evidence for **shared architecture with tumor-associated weakening of within-methylation spectral organization**. It is not a q<0.05 pan-cancer specificity result because n=5 limits exact-test resolution.

## 4. H2: global methylation-RNA geometry is shared but directionally heterogeneous

H2 `delta_cka` state medians remain positive in both states across all five cancers, so patient-level cross-layer geometry is present in tumor and normal tissue.

Tumor-minus-normal directions are mixed:
- BRCA +0.0226;
- LIHC +0.0095;
- PRAD -0.0620;
- THCA -0.3256;
- UCEC -0.3486.

Primary pan-cancer median = -0.06201; direction count 2 positive / 3 negative; p=1.0, q=1.0.

Masked-technical results are similar in overall interpretation (1 positive / 4 negative, median -0.07058, q=0.375), with BRCA moving very near zero.

**Disposition:** **TN-HETEROGENEOUS** for tumor-normal H2 direction. The result rejects a simple universal claim that global cross-layer geometry is uniquely strengthened or weakened in tumors.

## 5. H3a: patient-specific Hallmark coupling is mostly lower in tumor but not uniform

H3a state medians are positive in both states for all five cancers on the primary track.

Tumor-minus-normal directions:
- BRCA -0.0049;
- LIHC -0.0287;
- PRAD +0.0438;
- THCA -0.0300;
- UCEC -0.1364.

Primary pan-cancer median = -0.02870; direction count 1 positive / 4 negative; p=0.375, q=0.5.

UCEC is the clearest cancer-level decrease, with its q05-q95 tumor-minus-normal interval entirely below zero (-0.2529 to -0.0107). Other cancer intervals cross zero.

**Disposition:** **TN-HETEROGENEOUS / predominantly negative direction**, insufficient for a universal tumor-shift claim.

## 6. H3b: same-Hallmark semantic advantage trends upward in tumor but remains small

H3b tumor-minus-normal is positive in all five cancers on both technical tracks.

Primary pan-cancer median = +0.01157; direction count 5 positive / 0 negative; p=0.0625, q=0.125.
Masked median = +0.01602; 5 positive / 0 negative; p=0.0625, q=0.125.

However, the absolute shifts are small and each cancer's deterministic-draw effect interval crosses zero. This is consistent with the existing C1 finding that H3b is the weakest/support-sensitive layer.

**Disposition:** consistent directional clue only. Do not promote as resolved tumor specificity.

## 7. Joint biological interpretation under GOM

The frozen control does not support a binary model in which regulatory architecture is absent in normal tissue and emerges in cancer. Normal tissue itself shows construction-corrected within-layer and cross-layer organization.

Instead, the evidence supports a narrower multirepresentational interpretation:

1. **Within-layer methylation organization is strongly present in normal tissue and remains present but consistently reduced in tumors (H1).**
2. **Global cross-layer patient geometry persists in both states, but the tumor-normal change is cancer-dependent rather than universal (H2).**
3. **Patient-specific Hallmark coupling also persists in both states and tends to be reduced in tumor, with meaningful heterogeneity (H3a).**
4. **Fine same-label semantic advantage is slightly higher in tumor across all five cancers, but the magnitude is small and unresolved at the frozen pan-cancer inferential resolution (H3b).**

This pattern is compatible with **reorganization of an existing tissue architecture**, rather than de novo appearance of a tumor-only architecture.

The result does not identify a scalar biological chi, does not establish a capital-Chi dynamical state, and does not license collapse of H1-H3b into a master score. The joint chi/Chi question remains a separate target requiring a native dynamical/ordered representation.

## 8. Reviewer-facing consequence

The reviewer request for a normal control is now materially answered for the multiomic lane:

- appropriate same-program normal tissue was compared prospectively under a frozen design;
- normal molecular values were not used to select cancers or thresholds;
- both favorable and unfavorable directions are retained;
- the primary result is not “tumor-specific architecture,” but a **shared architecture with a highly consistent H1 weakening and heterogeneous cross-layer reorganization**.

The manuscript should state the exact finite-sample limitation: with five multiomic cancers, even a 5/5 direction yields exact two-sided p=0.0625, so the result provides effect/consistency evidence rather than a q<0.05 pan-cancer specificity declaration.

TN-A1/TN-P20 RNA biological execution remains a separate frozen lane and must be incorporated when complete.
