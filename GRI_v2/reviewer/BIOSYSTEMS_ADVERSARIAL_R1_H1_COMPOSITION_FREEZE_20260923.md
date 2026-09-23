# BioSystems adversarial Round 1 - H1 measured-composition-preserving null freeze

**Date:** 23 September 2026  
**Status:** FROZEN BEFORE OUTCOME OPENING  
**Branch:** `biosystems-adversarial-r1-20260923`  
**Parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`  
**Program authority:** SymC General Operations Manual v0.8.4  
**Evidence role:** post-result P0-Q adversarial sensitivity only. It cannot retroactively promote C1 or P1.

## 1. Reviewer question

Round-1 adversarial review correctly identifies that canonical H1 uses an independent within-probe patient-permutation null. That null destroys all cross-probe covariance and therefore cannot by itself distinguish biological organization from covariance induced by measured sample composition.

The frozen question is:

> Does H1 remain above a null that explicitly preserves the cross-probe structure explained by the two measured C1 composition covariates, ABSOLUTE purity and methylation-derived leukocyte fraction?

## 2. Source identities

Use the same public TCGA/GDC sources already bound in the program:

- methylation: `jhu-usc.edu_PANCAN_merged_HumanMethylation27_HumanMethylation450.betaValue_whitelisted.tsv`, GDC UUID `d82e2c44-89eb-43d9-b6d3-712732bf6a53`, SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`, 22,601 probes;
- ABSOLUTE purity: GDC UUID `4f277128-f793-4354-a13d-30cc7fe9f6b5`, SHA-256 `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`;
- leukocyte fraction: GDC UUID `6f75c9d7-5134-4ed1-b8f3-72856c98a4e8`, SHA-256 `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`;
- sample-quality annotation: GDC UUID `1a7d7be8-675d-4e60-a105-19d4121bdebf`; bind observed SHA-256 at execution.

The C1 cancer roster is frozen as:

`ACC BLCA BRCA CESC CHOL COAD DLBC ESCA GBM HNSC KICH KIRC KIRP LGG LIHC LUAD LUSC MESO OV PAAD PCPG PRAD READ SARC SKCM STAD TGCT THCA THYM UCEC UCS UVM`.

The pre-existing post-C1 S11 composition-complete audit established that 30 cancers meet a >=30 composition-complete participant gate, with DLBC and THYM below the gate. This test must reproduce that eligibility set before any H1 result is interpreted. Any mismatch is `SOURCE_ELIGIBILITY_HOLD`.

## 3. Participant identity and eligibility

For each cancer:

1. retain primary tumor sample type 01 only;
2. require an active/non-do-not-use sample-quality annotation;
3. require exactly one usable methylation source column for the cancer/participant after the same duplicate-exclusion rule used by TN-C1;
4. require finite methylation-derived leukocyte fraction;
5. require one unambiguous called ABSOLUTE purity value under the existing B0 source rule;
6. require the sample/cancer identity derived from annotation and leukocyte source to agree;
7. cancer must have at least 30 eligible participants.

No outcome value may change eligibility.

## 4. Fixed-n draws

- n = 30 participants per cancer;
- 20 deterministic draws per cancer;
- seed namespace: `GRI_BIOSYS_R1_H1_COMPOSITION_20260923`;
- no replacement;
- draws are made only from the frozen composition-complete pool;
- draw membership is stored.

Twenty draws are a reviewer-round robustness sample, not biological replication. Cancer remains the inferential unit.

## 5. Probe rule

Use the exact 22,601-probe C1 carrier.

Within each n=30 draw:

- retain probes with >=95% finite beta values;
- require at least 20,000 retained probes; otherwise the draw is `NOT_EVALUABLE`;
- impute the at-most-one missing retained value by that probe's within-draw median;
- no outcome-guided probe filtering;
- primary-publication probe track only. The already-reported technical mask remains a separate sensitivity and is not needed to answer this composition question.

## 6. H1 statistic

Use the canonical C1 spectral concentration:

1. center each retained CpG across the 30 participants;
2. form the patient Gram matrix divided by retained probe count;
3. use the first n-1 nonnegative eigenvalues;
4. normalize them to q;
5. compute `S_spec = 1 - H(q)/log(n-1)`.

## 7. Three frozen constructions per draw

### A. Canonical independence reference

Compute:
- `S_raw`;
- independently permute participant values within every retained CpG;
- `S_independent_null`;
- `delta_raw = S_raw - S_independent_null`.

This is a reconstruction/reference quantity only.

### B. Measured-composition-preserving null - PRIMARY

Let X contain:
- intercept;
- z-scored ABSOLUTE purity;
- z-scored leukocyte fraction.

For all retained CpGs simultaneously fit OLS:

`B = X A + R`.

Then:
- preserve the fitted matrix `X A` exactly;
- independently permute residual values within each CpG;
- reconstruct `B_compnull = X A + permuted(R)`;
- compute `S_compnull`;
- primary effect: `delta_comp_preserved = S_raw - S_compnull`.

This null preserves all cross-probe covariance captured linearly by the two measured composition covariates while destroying residual patient-specific cross-probe covariance.

### C. Residual-only H1 - SECONDARY

Compute:
- `S_residual` from R;
- independently permute residual values within every CpG;
- `S_residual_null`;
- `delta_residual = S_residual - S_residual_null`.

Also report:
`retention = delta_residual / delta_raw`
when `delta_raw > 0`.

## 8. Frozen inference

For each cancer, take the median across its evaluable 20 draws.

Primary cross-cancer inferential quantity:
`delta_comp_preserved`.

Report:
- number positive / negative / ties;
- pan-cancer median;
- IQR;
- exact two-sided sign-test p across cancer medians.

No per-draw p-value is produced. Draws are not treated as independent biological observations. No BH family is created because there is one primary reviewer-round endpoint.

Frozen disposition:

- `R1_H1_MEASURED_COMPOSITION_ROBUST`: pan-cancer median > 0 and exact two-sided sign-test p < 0.05.
- `R1_H1_MEASURED_COMPOSITION_SENSITIVE`: otherwise.
- `R1_H1_MEASURED_COMPOSITION_HOLD`: frozen source/eligibility/identity rule fails.

Secondary residual-H1 quantities cannot rescue a failed primary composition-preserving-null result.

## 9. Claim ceiling

A PASS means only:

> The two measured TCGA composition axes, ABSOLUTE purity and methylation-derived leukocyte fraction, are not sufficient to explain the recurrent H1 covariance under this post-result sensitivity.

A PASS does **not** mean:
- H1 is composition independent;
- batch/plate/center/array effects are removed;
- stromal/immune composition is fully deconvolved;
- subtype, age, sex, ancestry, or other sample structure is eliminated;
- H1 is causal or mechanistic;
- P1 is upgraded;
- the canonical independence null becomes a comprehensive null.

A failure narrows H1 accordingly and must be retained.
