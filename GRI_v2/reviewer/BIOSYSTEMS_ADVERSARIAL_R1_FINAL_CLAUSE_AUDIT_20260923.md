# BioSystems adversarial Round 1 final-clause audit - 23 September 2026

**Status:** COMPLETE / POST-REVIEWER FINAL TIGHTENING
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Previous Round-1 snapshot:** `biosystems-adversarial-r1-final-20260923`
**Program authority:** SymC General Operations Manual v0.8.4

## Purpose

Close the final four non-blocking reviewer observations after v11_R1 without reopening scientific discovery, changing any frozen endpoint, or publishing the private manuscript.

The final tightening addresses:
1. explicit identity of the 30/30 H1 denominator;
2. explicit attenuation sequence as stronger null structure is preserved;
3. per-cancer TSS support/granularity;
4. scope of the missingness-projection branch and interpretation of the external paired RNA near-miss.

A visual-QA pass also exposed and repaired one pre-existing LaTeX source bug in Supplement S3 (`50%` had not been escaped and therefore truncated the rendered line).

## 1. H1 30/30 denominator

The 30-cancer Round-1 H1 composition-complete universe is the frozen n>=30 composition-complete set.

The two canonical C1 cancers that do not enter this Round-1 denominator are:
- **DLBC**: composition-complete pool n=0;
- **THYM**: composition-complete pool n=0.

These exclusions are source/eligibility based and were not outcome selected.

The current private main and supplement now name DLBC and THYM directly wherever the 30/30 stronger-null result is introduced.

## 2. Matched stronger-null attenuation sequence

The reviewer correctly noted that stronger nulls absorb part of the raw H1 excess. The initially suggested sequence mixed a 32-cancer canonical median with 30-cancer post-result medians, so the final manuscript instead uses the matched 30-cancer Round-1 universe.

On that same 30-cancer universe:
- matched raw H1 excess median: **0.1233163**;
- purity/leukocyte-preserving null excess median: **0.0999770**;
- purity/leukocyte+TSS-preserving null excess median: **0.0816210**.

Interpretation now frozen in the private manuscript:

> Measured composition/site structure explains part of the original excess. The remaining excess is only an upper bound on structure not explained by the specific preserved terms; it is not evidence that the remainder is covariate-free.

No claim of full batch/composition independence is permitted.

## 3. Exact stronger-null construction

The private Supplement now states the construction explicitly.

### Measured-composition null

For every retained CpG j in each frozen n=30 draw:

`beta_ij = alpha_j + b_Pj z(P_i) + b_Lj z(L_i) + epsilon_ij`

where P is ABSOLUTE purity and L is methylation-derived leukocyte fraction.

The fitted CpG matrix is held fixed. Residuals are independently permuted across patients within each CpG and the null matrix is reconstructed as:

`beta*_ij = fitted_ij + epsilon_{pi_j(i),j}`

Thus the null preserves linear CpG structure attributable to the two measured composition axes while destroying residual cross-CpG patient alignment.

### Composition+TSS null

The design adds deterministic one-hot TCGA Tissue Source Site indicators. Within each n=30 draw:
- TSS categories represented by fewer than three patients are collapsed to `RARE_TSS`;
- the lexicographically first modeled category is the reference;
- the design must remain full rank;
- at least 10 residual degrees of freedom are required.

The fitted CpG matrix is again preserved and only per-CpG residuals are permuted before reconstruction.

All 600 planned TSS draws were evaluable.

## 4. TSS support/granularity

Across all 600 evaluable frozen n=30 draws:
- raw distinct TSS count range: **2 to 20**;
- overall median raw distinct TSS count: **11**.

Cancer-level support:

| Cancer | Raw TSS min | Raw TSS median | Raw TSS max | Modeled TSS median |
|---|---:|---:|---:|---:|
| ACC | 2 | 3 | 4 | 2 |
| BLCA | 12 | 14 | 18 | 5 |
| BRCA | 12 | 15 | 18 | 5 |
| CESC | 9 | 13 | 16 | 5 |
| CHOL | 7 | 8 | 9 | 4 |
| COAD | 9 | 12.5 | 14 | 4.5 |
| ESCA | 8 | 10.5 | 12 | 5 |
| GBM | 9 | 11 | 13 | 6 |
| HNSC | 8 | 12 | 16 | 5 |
| KICH | 4 | 4 | 4 | 4 |
| KIRC | 8 | 11 | 13 | 6 |
| KIRP | 13 | 16 | 19 | 5 |
| LGG | 11 | 13 | 15 | 5 |
| LIHC | 9 | 12 | 15 | 3 |
| LUAD | 12 | 15 | 20 | 4.5 |
| LUSC | 13 | 16 | 20 | 5 |
| MESO | 10 | 11 | 13 | 6.5 |
| OV | 9 | 10 | 13 | 5 |
| PAAD | 10 | 12 | 15 | 5 |
| PCPG | 9 | 11 | 13 | 5 |
| PRAD | 10 | 13 | 17 | 5 |
| READ | 7 | 8.5 | 11 | 5 |
| SARC | 8 | 12 | 15 | 2 |
| SKCM | 7 | 9 | 12 | 3 |
| STAD | 6 | 9 | 13 | 5 |
| TGCT | 8 | 9 | 13 | 4 |
| THCA | 9 | 12 | 15 | 6 |
| UCEC | 10 | 13 | 17 | 5 |
| UCS | 9 | 10 | 11 | 6 |
| UVM | 3 | 5 | 6 | 4 |

This table is derived directly from artifact `BIOSYSTEMS_ADVERSARIAL_R1_H1_TSS_V01`, workflow `35815819898`, artifact ID `10731877118`, digest `sha256:d8d953f7803e8dd048a85a6bb96298315dcfd4c9eff38bd3b400731386cb4e70`.

## 5. Missingness scope

The post-C1 S2 missingness-projection branch is not a pan-cancer test.

- informative cancers: **5/32 (15.6%)**;
- degenerate/uninformative because one or both burden vectors lack variation: **27/32 (84.4%)**.

The final manuscript now states that the broader bound on the missingness alternative comes from the complete-case restriction S3 and the remaining v2.2 sensitivities, not from treating degenerate S2 projections as negative evidence.

## 6. External paired RNA interpretation

The external prostate paired RNA secondary analysis remains **not confirmed** at the frozen threshold.

The first two coordinates are directionally concordant with the internal tumor-normal result but attenuated:
- C_in,pair: -0.01348 external versus about -0.0561 internal, approximately 4-fold smaller;
- C_in,PC1: -0.00864 external versus about -0.0730 internal, approximately 8-fold smaller;
- C_out: approximately unchanged at +0.00099.

With n=30 pairs, this pattern cannot distinguish a genuinely attenuated effect from insufficient resolution. The final wording therefore reports **nonconfirmation**, not successful replication and not evidence of absence.

## 7. Private release identities

Private main:
- `GRI_BioSystems_working_v12_R1_2026-09-23.tex`
- SHA-256 `29c25e0ebf7040e88e67c723392f87fd59a74fcc79116e82a1b5c4a43b69d67e`
- PDF SHA-256 `fdf1170705fdf86ab4ae665a855c5c974cedc2971e53fe611c51ff62a20fdf6b`
- 19 pages

Private supplement:
- `GRI_BioSystems_supplement_working_v10_R1_2026-09-23.tex`
- SHA-256 `d6fa4b26a0d378c325b652adc059a1eebe958e2acd2c5bb536f889a522ee6de4`
- PDF SHA-256 `35edb01a1220ba91459ef5fa91eb175bd9db0e2d5050bfa06f932b4fc6914007`
- 14 pages

Private response:
- Markdown SHA-256 `df55df867aba491acea1eeed397744c48e0ad986913d4f47d1d607e4e72732a3`
- PDF SHA-256 `40b6edb573f04597342adef02c9364fcbaa818b8f0963db1f8421b58943fceaa`

Private cover letter:
- Markdown SHA-256 `d2f112a78b86f0e2f886a695068e8cbb51fa8264713ed119aebaafbd1156cb3b`
- PDF SHA-256 `3ab257cbeaa6dd3b33e12e6cb61ffb5fb8f819b9445ed5548726d550c2c11857`

Private package:
- `BioSystems_Resubmission_R1_v12_Final_20260923.zip`
- SHA-256 `2531ca4e3e1a72e1473c97cb4c7a402f217ed2d2068753e5a8780b1d94ee8226`

## 8. Visual QA

The v12 main and v10 supplement compiled successfully.

Render inspection specifically verified:
- Abstract denominator clause renders correctly;
- external RNA attenuation sentence renders correctly;
- H1 attenuation/TSS paragraph renders without overflow;
- stronger-null equations render correctly;
- 30-cancer TSS longtable spans pages cleanly with repeated header;
- missingness 15.6% / 84.4% sentence renders correctly;
- legacy Supplement S3 source bug corrected from unescaped `50%` to rendered `50%`.

No scientific rerun was performed for these four final clauses.

## Final disposition

All four final reviewer observations are closed by disclosure/clarification from already returned evidence.

No new evidence-bearing gate is open.

**STATUS: COMPLETE / SUBMISSION READY**
