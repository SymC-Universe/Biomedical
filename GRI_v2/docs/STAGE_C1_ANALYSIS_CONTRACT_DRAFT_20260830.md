# Stage C1 methylation architecture contract

**STATUS: DRAFT — NOT FROZEN — AWAITING EXPLICIT USER SCIENTIFIC APPROVAL**

Date drafted: 2026-08-30

No Stage C1 methylation beta-value biological result may be calculated or inspected while this document remains DRAFT.

## 1. Scientific question

Stage C1 asks a deliberately narrow static question:

> Does the exact PanCanAtlas methylation layer contain reproducible multivariate organization beyond its probe-wise marginal distributions, and does that organization align specifically with the independently frozen Stage A RNA Hallmark architecture beyond patient-alignment and Hallmark-label nulls?

This is a static multiomic architecture test. It is **not** a test of temporal inheritance, causal regulation, damping, recovery, criticality, an exceptional point, a phase transition, an optimum, treatment response, or biological chi.

The required representation remains complementary:

1. **modal** — the mode-resolved covariance/eigenspectrum carrier;
2. **scalar** — a compressed coordinate derived explicitly from that modal carrier;
3. **conglomeration** — gene/Hallmark and network organization using the frozen C1A probe-gene-region map.

No one view replaces either of the others.

## 2. Frozen upstream inputs

C1 may use only already-frozen upstream objects:

- exact merged PanCanAtlas methylation source SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- strict one-to-one C0.1 methylation/Stage-A sample universe: 9,460 Stage A tumors before C1 missingness eligibility;
- all 32 cancers initially eligible by n>=30;
- exact Stage C1A annotation/mask representation;
- Stage C1A primary probe track: 22,601 exact probes;
- Stage C1A masked robustness track: 22,022 probes after the frozen 579-probe technical-mask union;
- Stage C1A probe-gene-region map SHA-256 `78f38d420a486427d67d88f67f5da83d1811003bf578b3c673f1dcbee5912296`;
- Stage C1A probe flags SHA-256 `5777ff7331c4bae750ed1c87bb6eb93136c56ade6dbf8522829db1f5659ac455`;
- frozen Hallmark membership SHA-256 `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`;
- frozen Stage A Hallmark-union RNA representation/cache SHA-256 `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`.

No outcome, treatment, subtype, survival, response, historical GRI score, preferred SymC pattern, RPPA result, or genomic result may be used to choose C1 features, strata, thresholds, or nulls.

## 3. Primary and robustness tracks

### 3.1 PRIMARY_PUBLICATION track

Use the exact 22,601 PanCanAtlas probe representation, subject only to the prospectively frozen missingness rules below.

### 3.2 MASKED_TECHNICAL robustness track

Apply the exact frozen C1A union mask:

- Chen cross-reactive overlap: 524 probes;
- common-SNP-at-CpG-or-SBE overlap: 59 probes;
- union overlap: 579 probes;
- nominal remaining probes before missingness eligibility: 22,022.

The same formulas, sample draws, null logic, and inferential rules must be run on both tracks. A favorable robustness track cannot replace or rescue the primary track.

## 4. Beta-value and missingness rules

The supplied publication-era beta values are the primary measurement scale. C1 will not renormalize the source and will not introduce an M-value or other transformation as an alternate discovery path.

For each cancer and probe track, before any resampling:

1. values must either be finite numeric beta values in `[0,1]` or explicit missing values;
2. a sample is eligible only if at least 95% of track probes are finite in that sample;
3. after sample eligibility, a probe is eligible only if at least 95% of eligible samples have finite values for that probe;
4. missing values in an otherwise eligible probe are replaced by that probe's median beta value calculated from finite values among the eligible samples of the same cancer;
5. every excluded sample, excluded probe, and imputed entry count is reported;
6. no cancer proceeds if fewer than 30 eligible one-to-one samples remain.

These are technical completeness rules only. No variance, mean, correlation, outcome, or cross-layer result may determine eligibility.

## 5. Fixed-n resampling

The inferential unit remains the cancer, not the individual resample.

For each eligible cancer and each probe track:

- fixed sample size: `n = 30`;
- resamples: `100`;
- sample without replacement within each resample;
- samples may recur across different resamples;
- the identical patient subset is used for methylation and RNA whenever a cross-layer statistic is calculated.

Deterministic seed namespace:

`GRI_V2_C1_20260830`

Every draw/null seed is generated from SHA-256 of the UTF-8 literal:

`GRI_V2_C1_20260830|<cancer>|<track>|<stratum>|<resample>|<null_type>|<replicate>`

The first 8 digest bytes interpreted as an unsigned big-endian integer, reduced modulo `2^32`, define the RNG seed. No language-runtime hash function is allowed.

## 6. Modal representation

The primary modal analysis operates in **all eligible probe space**, separately for the primary and masked tracks. Regulatory-stratum modal decompositions may be reported secondarily but cannot replace the all-probe primary analysis.

For one cancer/resample/track, let `B` be the `30 x p` beta matrix with samples in rows and eligible probes in columns.

Center each probe across the 30 sampled tumors without variance scaling:

`X_ij = B_ij - mean_i(B_ij)`.

No per-probe SD normalization is applied because the magnitude of methylation variability is part of the measured static covariance structure.

Construct the sample-space Gram matrix:

`G = (X X^T) / p`.

Because probe columns are centered, the matrix has at most 29 nonzero modes. Let the ordered nonnegative eigenvalues be

`lambda_1 >= ... >= lambda_29 >= 0`.

Tiny negative eigenvalues attributable only to numerical roundoff may be clipped to zero if their magnitude is no greater than `1e-10 * sum(abs(lambda))`; anything more negative is a task failure.

Normalize the spectrum:

`q_k = lambda_k / sum_j(lambda_j)`.

A task is invalid if total modal variance is zero.

### 6.1 Required modal outputs

For every valid task report:

- the complete 29-position normalized eigenspectrum `q_k`, with zeros retained;
- leading-mode share `q_1`;
- normalized spectral entropy
  `H_norm = -sum(q_k log q_k) / log(29)`, with `0 log 0 = 0`;
- effective rank
  `r_eff = exp(-sum(q_k log q_k))`;
- participation ratio
  `r_PR = 1 / sum(q_k^2)`;
- the first five sample-space eigenvectors;
- the first five mode-resolved probe contribution vectors.

For mode `k` with `lambda_k > 0`, the normalized contribution of probe `j` is

`L_jk = (X[:,j]^T u_k)^2 / (p * lambda_k)`.

For each mode, `sum_j L_jk = 1` up to numerical tolerance. This makes the scalar and conglomeration summaries traceable back to the modal carrier.

## 7. Scalar compression

The primary scalar coordinate is **spectral concentration**, not chi:

`S_spec = 1 - H_norm`.

Interpretation is strictly descriptive: higher `S_spec` means a larger fraction of static between-tumor methylation variance is concentrated into fewer covariance modes.

Required secondary scalar diagnostic:

`S_PR = 1 - r_PR / 29`.

Neither scalar is a damping ratio, phase coordinate, health score, treatment target, or biological chi. Both must always be reported with the eigenspectrum that generates them.

## 8. Probe-marginal construction null

The primary within-methylation null must preserve each sampled probe's exact 30 beta values while destroying cross-probe sample alignment.

For every observed resample, independently permute the 30 sample positions **within each probe column** using the deterministic null seed and recompute the complete modal/scalar analysis.

This null therefore preserves, within the sampled tumors:

- every probe's exact empirical beta distribution;
- mean;
- variance;
- bounded beta scale;
- any imputed values produced by the frozen missingness rule;

while destroying coordinated cross-probe covariance.

Primary paired construction effect:

`Delta_S = S_spec_observed - S_spec_probe-permuted`.

The full observed and null eigenspectra are retained; `Delta_S` is not allowed to substitute for them.

## 9. Cross-layer modal alignment to frozen RNA

For the same 30 patients, construct the methylation centered matrix `X_M` as above and the frozen Stage A Hallmark-union RNA feature matrix `X_R` using the **existing Stage A representation and preprocessing**, changing only the sample subset and column centering required for this resample. No new RNA feature selection or rescaling is permitted.

Define sample-space Gram matrices

`K_M = X_M X_M^T`

and

`K_R = X_R X_R^T`.

Primary full-modal cross-layer statistic: linear centered-kernel alignment

`CKA = <K_M, K_R>_F / (||K_M||_F ||K_R||_F)`.

Because both feature matrices are column-centered, no additional biological transformation is introduced.

Required modal detail: the principal-angle spectrum between the top-five methylation and top-five RNA sample-mode subspaces. These angles are descriptive mode-resolved evidence; CKA is the primary cross-layer modal statistic.

### 9.1 Patient-alignment null

Within each resample, deterministically permute the methylation patient rows relative to the RNA patient rows and recompute CKA.

Primary paired effect:

`Delta_CKA = CKA_aligned - CKA_patient-permuted`.

This preserves the full within-layer structure of both assays while destroying cross-assay patient identity.

## 10. Conglomeration representation

Conglomeration is built only from the frozen C1A gene/region map and frozen Hallmark membership.

### 10.1 Primary regulatory stratum

**Proposed primary stratum: `PROMOTER_CORE` = `TSS200`.**

Reason for the prospective choice: it is the narrowest frozen promoter-proximal region and therefore minimizes post hoc mixing of distinct regulatory contexts when the first biological question is methylation-to-RNA architectural coupling.

The following are prespecified secondary/robustness strata and may not rescue a failed `PROMOTER_CORE` primary result:

- `PROMOTER_PROXIMAL` = `TSS1500`;
- `PROMOTER_TRANSCRIBED_EDGE` = `5'UTR` / `1stExon`;
- `GENE_BODY` = `Body`;
- `THREE_PRIME_UTR` = `3'UTR`;
- `BROAD_PROMOTER_SECONDARY` = union of `TSS200`, `TSS1500`, `5'UTR`, `1stExon`.

### 10.2 Gene-level methylation representation

For sample `i`, gene `g`, and stratum `s`:

`M_igs = median(beta_ij for unique probes j mapping to gene g in stratum s)`.

Rules:

- a probe is counted at most once within a given gene/stratum score even if the frozen map contains multiple accessions/duplicate biological tuples for that same probe-gene pair;
- a genuinely multi-gene probe may contribute once to each supported gene because the frozen annotation explicitly supports those mappings;
- no nearest-gene invention is allowed;
- the 132 RefGene-unmapped probes never enter gene/Hallmark conglomeration.

### 10.3 Hallmark module representation

A Hallmark/stratum is eligible only if it contains at least:

- 10 distinct mapped gene symbols; and
- 10 distinct contributing probes

after the frozen technical/missingness rules for that cancer/track.

For each eligible Hallmark, center its gene-level methylation features across the 30 tumors and take PC1 as the methylation module eigengene.

Orient PC1 deterministically so its correlation with the sample-wise unweighted mean of the module's gene methylation scores is nonnegative. If that correlation is exactly zero, orient so the loading with the largest absolute magnitude is positive.

At least 25 Hallmark modules must be eligible in a cancer/resample for the primary conglomeration statistic. Otherwise that cancer/resample is ineligible for conglomeration inference and is reported rather than substituted.

## 11. Same-Hallmark RNA coupling

For each eligible Hallmark in the `PROMOTER_CORE` primary stratum, pair the methylation module eigengene with the **same Hallmark's frozen Stage A RNA eigengene** on the identical 30 patients.

Because PC orientations and methylation-expression direction can be context-dependent, the primary coupling strength is absolute Spearman correlation rather than a forced positive or negative biological direction.

For one cancer/resample:

`A_same = median_H |rho_S(ME_methylation,H, ME_RNA,H)|`.

Signed per-Hallmark correlations are retained as secondary diagnostics but cannot determine promotion.

### 11.1 Patient-alignment null

Permute methylation patient rows relative to RNA while preserving Hallmark identity:

`A_patient_null`.

Primary paired effect:

`Delta_A_patient = A_same - A_patient_null`.

### 11.2 Hallmark-label null

Keep patients correctly aligned but deterministically permute the Hallmark labels of the methylation eigengenes before pairing them with RNA Hallmarks:

`A_label_null`.

Primary paired effect:

`Delta_A_label = A_same - A_label_null`.

A same-Hallmark coupling claim must exceed **both** nulls. Patient alignment alone is insufficient, and semantic Hallmark identity alone is insufficient.

## 12. Secondary conglomeration topology test

For eligible common Hallmarks, compute absolute Hallmark-to-Hallmark Spearman correlation matrices separately for methylation and RNA.

Define topology similarity as the Spearman correlation between their upper-triangle vectors:

`T_topology = rho_S(vec_upper(|R_M|), vec_upper(|R_RNA|))`.

Its null is a deterministic permutation of Hallmark labels in the methylation matrix. This topology test is prespecified secondary support and is not allowed to rescue failure of the primary CKA or same-Hallmark coupling tests.

## 13. Inferential unit and promotion statistics

The 100 resamples are stability estimators, **not 100 independent biological replicates**.

For every primary effect and every cancer, take the median paired effect across its valid resamples. The cancer-level median is the inferential unit.

Minimum pan-cancer eligibility for promotion: at least **24 cancers** with valid cancer-level effects for that hypothesis. If fewer than 24 cancers are eligible, the result is descriptive only and cannot be promoted as pan-cancer evidence.

Across eligible cancers, use an exact one-sided sign test for positive cancer-level effects.

### 13.1 Primary inferential family

Four preregistered global hypotheses:

1. `H1`: `Delta_S > 0` — modal-derived spectral concentration exceeds the probe-marginal construction null;
2. `H2`: `Delta_CKA > 0` — methylation/RNA full-modal alignment exceeds the patient-alignment null;
3. `H3a`: `Delta_A_patient > 0` — same-Hallmark conglomeration coupling exceeds the patient-alignment null;
4. `H3b`: `Delta_A_label > 0` — same-Hallmark conglomeration coupling exceeds the Hallmark-label null.

Apply Benjamini-Hochberg FDR at `q < 0.05` across these four primary global p-values.

Report for every hypothesis:

- eligible cancer count;
- positive cancer count;
- cancer-level median effect distribution;
- median and IQR across cancers;
- exact sign-test p-value;
- BH q-value.

No arbitrary minimum effect-size threshold is imposed after seeing the data.

## 14. Mandatory technical robustness gate

The complete four-hypothesis primary family is evaluated separately on:

- `PRIMARY_PUBLICATION`;
- `MASKED_TECHNICAL`.

For a primary scientific statement to be promoted, the relevant hypothesis/hypotheses must satisfy the same direction and `q < 0.05` criterion on **both** tracks. The masked track cannot create a positive claim that the publication-faithful primary track does not support, and the primary track cannot ignore a reversal under the frozen technical mask.

## 15. Secondary-stratum multiplicity

The five non-primary regulatory views are a separate prespecified secondary family:

- `PROMOTER_PROXIMAL`;
- `PROMOTER_TRANSCRIBED_EDGE`;
- `GENE_BODY`;
- `THREE_PRIME_UTR`;
- `BROAD_PROMOTER_SECONDARY`.

Their same-Hallmark coupling tests are corrected together by BH FDR. They are interpreted as context decomposition only. No secondary stratum may be renamed the primary stratum or used to rescue a failed `PROMOTER_CORE` result.

## 16. Promotion ladder

### Level C1-0 — source/representation only

Already closed by C1A.

### Level C1-1 — organized static methylation geometry

May be stated only if `H1` passes the full primary + masked robustness gate.

Allowed language: the methylation matrix contains reproducible static covariance concentration beyond an exact probe-marginal-preserving null.

### Level C1-2 — specific static methylation/RNA architecture

May be stated only if `H2`, `H3a`, and `H3b` all pass, with H1 retained as the within-methylation organization foundation, on both primary and masked tracks.

Allowed language: independently measured methylation and RNA layers show specific patient-aligned and Hallmark-identity-aligned static organization beyond the frozen nulls.

### Not promotable in C1 regardless of result

C1 cannot establish:

- methylation causes RNA change;
- RNA causes methylation change;
- substrate inheritance;
- temporal progression or irreversibility;
- damping or recovery rates;
- critical slowing;
- an exceptional point;
- a phase transition;
- a cancer optimum;
- treatment response;
- biological chi;
- `chi = 1` as a biological boundary;
- a master stability score.

## 17. Failure policy

If any primary hypothesis fails:

- retain the failure/null result;
- do not change the primary stratum;
- do not change the scalar formula;
- do not change feature scaling;
- do not substitute a secondary stratum;
- do not introduce a new mask;
- do not retune the missingness thresholds;
- do not change null direction or test family;
- do not use RPPA/genomic/outcome layers to rescue the failed hypothesis.

Any later alternative must be explicitly labeled post hoc and must be validated prospectively on independent data before promotion.

## 18. What follows C1

A successful C1 would justify a separately preregistered extension to the already-frozen RPPA and genomic layers as orthogonal static tests. It still would not establish substrate inheritance.

The inheritance question remains blocked until ordered perturbation, longitudinal, or otherwise temporally informative data can test whether organization is transmitted or recovered across layers in a directional sequence.

Biological chi remains blocked until a genuine same-coordinate dynamical pair analogous to `Gamma` and `Omega` satisfies the separate chi-admission rules.

## Approval record

This document becomes frozen only after explicit user approval of the scientific choices above, especially:

- raw beta scale with the 95% missingness/median-imputation rule;
- all-probe unscaled modal Gram representation;
- `S_spec = 1 - H_norm` as the primary scalar compression;
- independent within-probe permutation construction null;
- CKA as the primary cross-layer modal statistic;
- `PROMOTER_CORE/TSS200` as the primary conglomeration stratum;
- median unique-probe gene aggregation;
- PC1 Hallmark methylation eigengenes;
- absolute Spearman same-Hallmark coupling;
- patient-alignment and Hallmark-label nulls;
- n=30, 100 deterministic resamples;
- cancer-level sign tests, minimum 24 eligible cancers, and four-test BH family;
- mandatory agreement of publication-faithful and frozen technical-mask tracks.

Until approval, implementation may be prepared mechanically but no beta-value biological output may be generated.
