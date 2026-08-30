# Stage C1 methylation architecture contract — Draft v2

**STATUS: DRAFT — NOT FROZEN — AWAITING EXPLICIT USER SCIENTIFIC APPROVAL**

Date: 2026-08-30

This v2 supersedes `STAGE_C1_ANALYSIS_CONTRACT_DRAFT_20260830.md` for approval purposes. No Stage C1 methylation beta-value biological result may be calculated or inspected while this document remains DRAFT.

## 1. Primary scientific question

Stage C1 asks:

> Does the exact PanCanAtlas methylation layer contain reproducible multivariate organization beyond its probe-wise marginal distributions, and does that organization align specifically with the independently frozen Stage A RNA Hallmark architecture beyond patient alignment, Hallmark identity, and the already-documented B1 purity/leukocyte composition structure?

This remains a static multiomic architecture test. It cannot establish temporal inheritance, causal regulation, damping, recovery, critical slowing, an exceptional point, a phase transition, an optimum, treatment response, or biological chi.

The required representation is complementary:

- **modal:** mode-resolved covariance/eigenspectrum and mode contributions;
- **scalar:** compression derived explicitly from the modal spectrum;
- **conglomeration:** gene/Hallmark/network organization from the frozen probe-gene-region map.

No one view replaces the others.

## 2. Frozen upstream universe

C1 may use only the already-frozen sources and mappings:

- methylation source SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- C0.1 strict one-to-one methylation/Stage-A sample universe: 9,460 tumors, 32 cancers before C1 missingness eligibility;
- publication-faithful probe track: 22,601 exact probes;
- technical-mask robustness track: 22,022 nominal probes after the frozen 579-probe union mask;
- probe-gene-region map SHA-256 `78f38d420a486427d67d88f67f5da83d1811003bf578b3c673f1dcbee5912296`;
- probe-flags SHA-256 `5777ff7331c4bae750ed1c87bb6eb93136c56ade6dbf8522829db1f5659ac455`;
- Hallmark membership SHA-256 `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`;
- Stage A Hallmark-union RNA cache SHA-256 `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`;
- the already-frozen B1 ABSOLUTE purity and methylation-derived leukocyte-fraction covariates for composition robustness.

No outcome, treatment, subtype, survival, response, historical GRI score, RPPA result, genomic result, or preferred SymC pattern may select C1 features, thresholds, strata, or nulls.

## 3. Probe tracks and shared sample eligibility

### 3.1 PRIMARY_PUBLICATION

Use the exact 22,601-probe PanCanAtlas representation subject only to the technical missingness rule below.

### 3.2 MASKED_TECHNICAL

Use the exact primary track minus the frozen 579-probe technical-mask union. This track is robustness only and may not create a claim absent in the primary track.

### 3.3 Shared sample universe

Sample eligibility is determined **once from the PRIMARY_PUBLICATION track** and inherited unchanged by the MASKED_TECHNICAL track. This prevents the technical mask from changing the patient composition of the robustness comparison.

For each cancer before resampling:

1. values must be finite numeric beta values in `[0,1]` or explicit missing values;
2. a sample is eligible if at least 95% of the 22,601 primary-track probes are finite;
3. after sample eligibility, a primary-track probe is eligible if at least 95% of eligible samples are finite for that probe;
4. the masked track uses the intersection of those eligible probes with the frozen 22,022-probe mask-retained set;
5. missing values in an otherwise eligible probe are replaced by that probe's median among finite values in the same cancer's shared eligible-sample set;
6. all excluded samples, excluded probes, and imputed entries are reported;
7. a cancer cannot proceed if fewer than 30 shared eligible samples remain.

No variance, mean, correlation, or cross-layer result may determine technical eligibility.

The supplied beta scale is primary. No M-value or alternate transform may be introduced as a discovery path.

## 4. Fixed-n resampling and deterministic seeds

The inferential unit is the cancer, not the resample.

For each eligible cancer:

- `n = 30` patients per resample;
- `100` resamples;
- sampling without replacement inside a resample;
- patients may recur across resamples;
- the identical 30-patient draw is used for primary and masked methylation tracks and for every RNA comparison for which the necessary data exist.

Seed namespace: `GRI_V2_C1_20260830`.

Every sampling/null seed is SHA-256 of

`GRI_V2_C1_20260830|<cancer>|<track>|<stratum>|<resample>|<null_type>|<replicate>`

with the first 8 digest bytes interpreted as unsigned big-endian integer modulo `2^32`. Runtime-specific hash functions are forbidden.

## 5. Modal carrier

Primary modal analysis uses all eligible probes, separately on PRIMARY_PUBLICATION and MASKED_TECHNICAL.

For a 30-patient draw with `p` eligible probes, let `B` be the `30 x p` beta matrix. Center each probe across the sampled tumors, without variance scaling:

`X_ij = B_ij - mean_i(B_ij)`.

Construct

`G = (X X^T) / p`.

Let its 29 ordered nonnegative centered modes be

`lambda_1 >= ... >= lambda_29 >= 0`.

Numerical negatives may be clipped only when their magnitude is at most `1e-10 * sum(abs(lambda))`; otherwise the task fails.

Normalize

`q_k = lambda_k / sum_j(lambda_j)`.

Zero total modal variance is an invalid task.

Required modal record:

- complete 29-position normalized eigenspectrum;
- `q_1`;
- normalized spectral entropy `H_norm = -sum(q log q)/log(29)` with `0 log 0 = 0`;
- effective rank `r_eff = exp(-sum(q log q))`;
- participation ratio `r_PR = 1/sum(q^2)`;
- first five sample-space eigenvectors;
- first five normalized probe-contribution vectors.

For eigenmode `k`, probe `j` contributes

`L_jk = (X[:,j]^T u_k)^2 / (p * lambda_k)`

for `lambda_k > 0`, with mode contributions summing to one up to numerical tolerance.

## 6. Scalar compression

Primary scalar:

`S_spec = 1 - H_norm`.

Secondary diagnostic:

`S_PR = 1 - r_PR/29`.

These are static spectral-concentration coordinates only. They are not chi, damping ratios, phase coordinates, health scores, or treatment targets. Every scalar result must remain traceable to the full eigenspectrum.

## 7. Probe-marginal construction null

For every observed 30-patient resample, independently permute the 30 sampled values **within each probe column**, using the deterministic null seed, then recompute the modal/scalar analysis.

This preserves each sampled probe's exact empirical beta values, mean, variance, bounded scale, and frozen imputations while destroying cross-probe sample alignment.

Primary paired construction effect:

`Delta_S = S_spec_observed - S_spec_probe-permuted`.

The observed and null eigenspectra are both retained.

## 8. Full-modal methylation/RNA alignment

For the identical 30 patients, use:

- methylation matrix `X_M` as above;
- the exact frozen Stage A Hallmark-union RNA feature representation `X_R`, with no new feature selection or biological rescaling, restricted to the same patients and column-centered for the resample.

Define

`K_M = X_M X_M^T`

`K_R = X_R X_R^T`.

Primary full-modal alignment statistic:

`CKA = <K_M,K_R>_F / (||K_M||_F ||K_R||_F)`.

Mode-resolved secondary output: principal-angle spectrum between the top-five methylation and top-five RNA sample-mode subspaces.

### 8.1 Patient-alignment null

Deterministically permute methylation patient rows relative to RNA and recompute CKA.

`Delta_CKA = CKA_aligned - CKA_patient_null`.

This preserves each layer's internal architecture while destroying patient identity across assays.

## 9. Conglomeration

Conglomeration uses only the frozen C1A probe-gene-region map and frozen Hallmark membership.

### 9.1 Primary regulatory stratum

**Primary: `PROMOTER_CORE = TSS200`.**

Rationale: it is the narrowest frozen promoter-proximal stratum and avoids mixing biologically distinct methylation contexts in the first RNA-coupling test.

Prespecified secondary views, forbidden from rescuing a failed primary stratum:

- `PROMOTER_PROXIMAL = TSS1500`;
- `PROMOTER_TRANSCRIBED_EDGE = 5'UTR / 1stExon`;
- `GENE_BODY = Body`;
- `THREE_PRIME_UTR = 3'UTR`;
- `BROAD_PROMOTER_SECONDARY = TSS200 + TSS1500 + 5'UTR + 1stExon`.

### 9.2 Gene methylation score

For sample `i`, gene `g`, stratum `s`:

`M_igs = median(beta_ij over unique eligible probes j mapped to g in s)`.

A probe counts at most once within a gene/stratum score. A genuinely multi-gene probe may enter each annotation-supported gene. The 132 RefGene-unmapped probes never enter gene/Hallmark conglomeration.

### 9.3 Hallmark methylation eigengene

A Hallmark/stratum is eligible when it has at least 10 distinct mapped genes and 10 distinct contributing probes after frozen technical/missingness rules.

Center gene methylation features across the 30 tumors and use PC1 as the methylation Hallmark eigengene. Orient PC1 so its correlation with the module's sample-wise unweighted mean gene methylation is nonnegative; if exactly zero, orient the largest-absolute loading positive.

At least 25 Hallmarks must be eligible in a cancer/resample for primary conglomeration inference.

## 10. Same-Hallmark methylation/RNA coupling

For each eligible PROMOTER_CORE Hallmark, pair its methylation eigengene with the same Hallmark's Stage A RNA eigengene on the identical 30 patients.

Primary coupling strength is absolute Spearman correlation because methylation-expression direction and PC sign can be context dependent:

`A_same = median_H |rho_S(ME_M,H, ME_RNA,H)|`.

Signed Hallmark correlations are retained only as secondary diagnostics.

### 10.1 Patient null

Permute methylation patient rows relative to RNA while keeping Hallmark identity:

`Delta_A_patient = A_same - A_patient_null`.

### 10.2 Hallmark-label null

Keep patients aligned but permute methylation Hallmark labels before pairing to RNA:

`Delta_A_label = A_same - A_label_null`.

A same-Hallmark claim must exceed both nulls.

## 11. Mandatory B1 composition robustness

B1 already established that purity/leukocyte context explains a concentrated portion of the RNA architecture. Therefore the strongest C1 cross-layer claim must also survive the already-frozen joint B1 composition covariates.

For cancers/resamples with both frozen covariates available, construct the `30 x 3` design matrix

`Z = [intercept, ABSOLUTE_purity, methylation-derived_leukocyte_fraction]`.

Use the residual-maker

`R_Z = I - Z (Z^T Z)^+ Z^T`,

where `+` is the Moore-Penrose pseudoinverse.

Apply the same projection to methylation and RNA feature matrices before cross-layer statistics:

`X_M,adj = R_Z X_M`

`X_R,adj = R_Z X_R`.

Recompute:

- adjusted CKA and its patient-alignment null;
- adjusted PROMOTER_CORE gene/Hallmark methylation eigengenes from residualized methylation gene features;
- adjusted RNA Hallmark eigengenes using the exact same residual projection;
- adjusted same-Hallmark coupling and both patient and label nulls.

The within-methylation H1 construction test is not composition-adjusted because H1 asks whether static methylation organization exists, not what causes it.

Composition-adjusted cross-layer effects:

- `Delta_CKA_adj`;
- `Delta_A_patient_adj`;
- `Delta_A_label_adj`.

If fewer than 24 cancers are jointly eligible for the composition-adjusted family, composition robustness is reported as limited/descriptive and no claim of composition-independent alignment is permitted.

## 12. Secondary topology

For eligible common Hallmarks, compute absolute Hallmark-to-Hallmark Spearman correlation matrices separately for methylation and RNA.

`T_topology = rho_S(vec_upper(|R_M|), vec_upper(|R_RNA|))`.

Hallmark-label permutation supplies its null. This is secondary support only and cannot rescue primary failure.

## 13. Inference

The 100 resamples are stability estimators, not independent biological replicates.

For each effect and cancer, take the median paired effect across valid resamples. Cancer-level medians are the inferential units.

Minimum pan-cancer eligibility for a promoted global claim: **24 cancers**. Fewer than 24 makes the result descriptive only.

Across eligible cancers use an exact one-sided sign test for positive cancer-level effects.

### 13.1 Raw primary family

Four global hypotheses:

1. `H1`: `Delta_S > 0`;
2. `H2`: `Delta_CKA > 0`;
3. `H3a`: `Delta_A_patient > 0`;
4. `H3b`: `Delta_A_label > 0`.

Apply BH FDR across these four p-values at `q < 0.05`, separately for PRIMARY_PUBLICATION and MASKED_TECHNICAL.

### 13.2 Composition-adjusted cross-layer family

Three global robustness hypotheses:

1. `H2_adj`: `Delta_CKA_adj > 0`;
2. `H3a_adj`: `Delta_A_patient_adj > 0`;
3. `H3b_adj`: `Delta_A_label_adj > 0`.

Apply BH FDR across these three p-values at `q < 0.05`, separately for PRIMARY_PUBLICATION and MASKED_TECHNICAL.

For every hypothesis report eligible cancers, positive cancers, cancer-level effect distribution, median/IQR, exact sign-test p, and BH q.

No effect-size threshold may be invented after inspection.

## 14. Secondary regulatory family

The five non-primary regulatory strata form one prespecified secondary family. Same-Hallmark coupling tests across these strata are BH-corrected together. Secondary strata are context decomposition only and cannot replace PROMOTER_CORE.

## 15. Promotion ladder

### C1-1: organized static methylation geometry

Requires H1 to pass `q < 0.05` on both PRIMARY_PUBLICATION and MASKED_TECHNICAL.

Allowed statement: static methylation covariance is more spectrally concentrated than expected after destroying cross-probe alignment while preserving exact probe marginals.

### C1-2: specific static methylation/RNA architecture

Requires H1, H2, H3a, and H3b to pass on both probe tracks.

Allowed statement: methylation and RNA show specific patient-aligned and Hallmark-identity-aligned static organization beyond the frozen raw nulls.

### C1-3: composition-robust specific static methylation/RNA architecture

Requires C1-2 plus H2_adj, H3a_adj, and H3b_adj to pass on both probe tracks with at least 24 jointly eligible cancers.

Allowed statement: the specific static methylation/RNA alignment persists after projection of the already-frozen ABSOLUTE purity and methylation-derived leukocyte-fraction covariates.

If C1-2 passes but C1-3 fails, the result remains a raw specific static alignment whose relationship to known composition cannot be separated. It must not be described as composition-independent.

## 16. Forbidden promotion regardless of outcome

Stage C1 cannot establish:

- methylation causes RNA change;
- RNA causes methylation change;
- substrate inheritance;
- temporal progression, memory, or irreversibility;
- damping/recovery rates;
- critical slowing;
- an exceptional point;
- a phase transition;
- a cancer optimum or therapy target;
- biological chi;
- `chi = 1` as a cancer boundary;
- a master stability score.

## 17. Failure policy

If a primary hypothesis fails, retain the failure and do not retune:

- primary regulatory stratum;
- scalar formula;
- feature scaling;
- missingness thresholds;
- technical mask;
- null construction;
- test direction;
- multiplicity family;
- sample size/resample count.

Secondary strata, RPPA, genomics, outcomes, or post hoc transformations may not rescue a failed Stage C1 primary hypothesis. Any later alternative must be labeled post hoc and validated prospectively on independent data before promotion.

## 18. Downstream sequence

After C1 closes, RPPA and genomic extensions may be preregistered as orthogonal static tests. Even a C1-3 success does not establish substrate inheritance.

Inheritance remains blocked until ordered perturbation/longitudinal data test whether organization propagates or recovers across layers in a directional sequence.

Biological chi remains blocked until a legitimate same-coordinate dynamic pair analogous to Gamma and Omega satisfies the separate chi-admission rules.

## 19. Approval record

Explicit approval of this v2 freezes, as one package:

- shared PRIMARY-derived sample eligibility;
- raw beta scale and 95% missingness/median-imputation rule;
- all-probe unscaled sample-space modal Gram matrix;
- complete eigenspectrum plus top-five mode contributions;
- `S_spec = 1 - H_norm` primary scalar and `S_PR` secondary scalar;
- independent within-probe permutation construction null;
- CKA full-modal RNA bridge plus patient null;
- PROMOTER_CORE/TSS200 primary conglomeration stratum;
- median unique-probe gene aggregation;
- PC1 methylation Hallmark eigengenes;
- absolute Spearman same-Hallmark coupling;
- patient and Hallmark-label nulls;
- mandatory B1 joint purity/leukocyte robustness for the strongest cross-layer claim;
- n=30, 100 deterministic resamples;
- cancer-level exact sign tests;
- minimum 24 eligible cancers for promotion;
- separate four-test raw and three-test composition-adjusted BH families;
- mandatory agreement of publication-faithful and technical-mask tracks;
- the failure and claim ceilings above.

Until explicit approval, implementation may be prepared mechanically, but no beta-value biological output may be generated.
