# P0 D3 DISCOVERY audit-state and P1 model-fitting freeze

**STATUS: FROZEN AFTER D2 PASS AND BEFORE ANY D3 CROSS-LAYER DISCOVERY RESULT IS COMPUTED**

Date: 2026-08-30

Upstream anchors:
- P0 holdout protocol: `GRI_v2/docs/TOOL_PREDICTION_P0_HOLDOUT_FREEZE_20260830.md`
- D1 source audit: `GRI_v2/artifacts/P0_D1_DISCOVERY_SOURCE_AUDIT.md`
- D2 target audit: `GRI_v2/artifacts/P0_D2_RNA_DISCOVERY_TARGET_AUDIT.md`

D3 is a DISCOVERY-only gate. It computes the frozen cross-layer audit primitives and fits the P1 prediction models. It must not generate, inspect, score, or otherwise use REPLICATION or FINAL_HOLDOUT RNA targets or methylation values.

## 1. Frozen data scope

Use only the 4,863 eligible DISCOVERY participants from the 19 P0-evaluable cancers. No split repair, sample reassignment, cancer rescue, or post-result eligibility change is allowed.

Source variables are the D1 methylation Hallmark PC1 scores. Target variables are the D2 RNA Hallmark PC1 scores.

- PRIMARY_PUBLICATION is the primary P1 source track.
- MASKED_TECHNICAL is a frozen technical-robustness attack, not a second model selected by outcome.
- Cross-layer semantic calculations use the exact D1/D2 common-Hallmark intersection, expected to be 45 Hallmarks per cancer/track after D2 audit.
- Global geometry may compare unequal feature counts: each methylation track uses its eligible source Hallmarks and RNA uses all 50 D2-evaluable target Hallmarks.

The B1 composition covariates are the exact frozen PanCanAtlas inputs:
- ABSOLUTE purity SHA-256 `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`;
- methylation-derived leukocyte fraction SHA-256 `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`.

Matching is inherited unchanged from B1: primary sample type 01, ABSOLUTE additionally requires `call status=called` and finite purity, exact sample-root attachment when available, and patient fallback only when the source contains exactly one eligible primary measurement for that patient. Duplicate leukocyte values for an exact sample root are reduced by the median of finite values before attachment.

Because D3 inputs are participant-root features, the B1 sources are reduced to a participant-level value only under the same uniqueness rules. No covariate imputation is allowed.

## 2. Deterministic randomness

All D3 nulls use 39 permutations. A deterministic integer seed is the unsigned little-endian value of the first 8 SHA-256 bytes of:

`GRI_V2_PREDICTION_P0_20260830|D3|<analysis_tag>|<cancer>|<track>|<permutation_index>`

where fields that do not apply are replaced by a stable literal such as `RNA` or `NA`.

The existing P1 cross-validation fold assignment remains:

`SHA256("GRI_V2_PREDICTION_P0_20260830|CV|<cancer>|<participant_root>") first 8 bytes unsigned big-endian mod 5`.

No random seed is selected after results are seen.

## 3. Frozen audit primitives

### 3.1 Global sample geometry

For each cancer and each source technical track, compute linear CKA between the methylation source matrix and the all-50-Hallmark RNA target matrix on the same DISCOVERY participants.

Generate 39 patient-row nulls by jointly permuting source rows while the RNA matrix remains fixed. Define:

- empirical one-sided `p = (1 + count(null >= observed)) / 40`;
- `Delta_CKA = observed - median(null)`.

`GLOBAL_SHARED_DETECTED` requires both `p <= 0.05` and `Delta_CKA >= 0.05`, exactly as frozen in P0/F2.

### 3.2 Semantic specificity

On the exact common Hallmark set, define

`A_same = median_H |Spearman(source_H, RNA_H)|`.

Generate separately:
- 39 patient nulls by jointly permuting source patient rows against fixed RNA;
- 39 label nulls by permuting the source Hallmark labels/columns while keeping patient alignment fixed.

For each null family use empirical one-sided p-values with the same `(1 + count(null >= observed))/40` rule.

Define effects against null medians:
- `Delta_A_patient = A_same - median(patient_null)`;
- `Delta_A_label = A_same - median(label_null)`.

Patient-specific semantic support requires `p_patient <= 0.05` and `Delta_A_patient > 0`.

Label-specific semantic support requires `p_label <= 0.05` and `Delta_A_label >= 0.10`.

`SEMANTIC_RAW_DETECTED` requires both patient and label support.

### 3.3 Within-layer construction-aware organization

Use the F2 modal primitive `S_spec = 1 - normalized spectral entropy` on centered sample geometry.

For each cancer:
- compute source PRIMARY_PUBLICATION `S_spec`;
- compute RNA target `S_spec`;
- generate 39 construction nulls by independently permuting each feature column across patients, preserving feature marginals while destroying patient-level multivariate organization.

Within-layer detection requires empirical `p <= 0.05` and `Delta_S_spec = observed - median(null) > 0`.

This primitive is used only to distinguish `WITHIN_LAYER_ONLY` from `NO_SHARED_STRUCTURE` when cross-layer global sharing is absent. It is not biological chi, damping, or a new stability scalar.

### 3.4 Composition attack

For each cancer, use only participants with both frozen B1 covariates finite. No covariate imputation is allowed. If fewer than 30 DISCOVERY participants remain, composition robustness is `NOT_EVALUABLE` and the strongest ACCEPT state is impossible.

On the same complete-case participants, residualize each source and RNA feature on `[intercept, standardized ABSOLUTE purity, standardized methylation-derived leukocyte fraction]` using ordinary least squares within cancer.

Recompute global and semantic screens on residuals with unchanged null counts, thresholds, and effect definitions. Permutations operate on the residualized source rows/labels as applicable; covariates are not re-fit inside each null.

### 3.5 Technical attack

Run raw and composition-adjusted global/semantic screens separately on PRIMARY_PUBLICATION and MASKED_TECHNICAL using identical participant sets within the corresponding raw or composition analysis.

Technical-track disagreement is retained as an explicit reason code and cannot receive the strongest robust state.

## 4. Frozen discovery state construction

State assignment is determined without held-out data.

1. If PRIMARY_PUBLICATION global sharing fails:
   - `WITHIN_LAYER_ONLY` if source PRIMARY_PUBLICATION or RNA within-layer organization is detected;
   - otherwise `NO_SHARED_STRUCTURE`.
2. If PRIMARY_PUBLICATION global sharing passes but PRIMARY_PUBLICATION raw semantic detection fails: `GLOBAL_SHARED_ONLY`.
3. If PRIMARY_PUBLICATION raw semantic passes but MASKED_TECHNICAL raw global+semantic does not agree, retain the most appropriate non-robust state and attach `TECHNICAL_TRACK_DISAGREEMENT`; decision class is CAUTION.
4. If raw global+semantic criteria pass on both technical tracks but the composition-adjusted global+semantic criteria fail or are not evaluable on either track: `SEMANTIC_SHARED_CONFOUNDED`.
5. `SEMANTIC_SHARED_ROBUST` requires global and semantic criteria to pass in raw and composition-adjusted analyses on both PRIMARY_PUBLICATION and MASKED_TECHNICAL.

Decision class remains frozen:
- ACCEPT: `SEMANTIC_SHARED_ROBUST` only;
- CAUTION: `GLOBAL_SHARED_ONLY`, `SEMANTIC_SHARED_CONFOUNDED`, or an otherwise favorable state with technical-track disagreement;
- REFUSE: `NO_SHARED_STRUCTURE` or `WITHIN_LAYER_ONLY`.

These are methodological prediction/refusal states, not cancer biological classes.

## 5. Frozen P1 DISCOVERY model fitting

### 5.1 Participant set

P1 fitting uses the complete-case B1 covariate participants within each cancer because the two covariates are frozen predictors. If fewer than 30 DISCOVERY participants remain, P1 is `NOT_EVALUABLE`; no sample substitution or partition repair occurs.

### 5.2 Primary model

`ALL_METHYLATION_RIDGE` uses:
- all PRIMARY_PUBLICATION D1 source Hallmark scores available in that cancer, expected 45;
- ABSOLUTE purity;
- methylation-derived leukocyte fraction;
- all 50 D2 RNA Hallmark targets jointly.

The primary model is multi-output ridge regression with fixed alpha grid:

`[0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]`.

### 5.3 Cross-validation preprocessing

Within each of the five deterministic discovery folds, predictor means and standard deviations are fit on the four training folds only and applied unchanged to the validation fold. Predictors with non-finite or zero training-fold standard deviation are removed deterministically for that fold and recorded.

For the final model, predictor means/standard deviations and zero-variance removal are fit on the complete DISCOVERY set only.

The ridge intercept is the training target mean after predictor centering. RNA targets are not standardized.

Alpha is selected by minimizing the mean target-wise validation normalized MSE across all fold predictions. Each target MSE is divided by that target's full-DISCOVERY variance, a fixed discovery-only denominator common to all alphas. Targets with non-finite or zero DISCOVERY variance make the affected model task not evaluable rather than triggering a replacement target.

An exact tie selects the smallest alpha because the grid is traversed in ascending order.

### 5.4 Baselines

- `MEAN_ONLY`: the full-DISCOVERY target mean for all 50 targets.
- `COVARIATE_ONLY`: multi-output ridge using only the two B1 covariates, with its own independent alpha selection on the same fixed grid/folds.
- `SAME_HALLMARK_ONLY`: separate ridge model for each of the 45 common Hallmarks using matched methylation Hallmark score plus the two B1 covariates. Each target receives its own alpha selection on the same grid/folds. The five source-ineligible RNA targets are `NOT_EVALUABLE_SOURCE_MAPPING` for this baseline; no replacement source feature is invented.
- `ALL_METHYLATION_RIDGE`: primary model above.

Discovery cross-validation error is a model-selection diagnostic only. It is not held-out predictive performance and cannot be used to promote P0.

### 5.5 Frozen model outputs

D3 records, for later untouched projection:
- complete-case participant identities/counts;
- predictor names;
- full-discovery predictor means/scales and removed zero-variance predictors;
- selected alpha;
- fitted intercept and coefficients;
- per-alpha discovery CV diagnostics;
- SAME_HALLMARK_ONLY parameters for the common targets;
- discovery audit state and all primitive/null summaries.

No REPLICATION or FINAL_HOLDOUT target score is generated in D3.

## 6. Traceability-only modal information

Eigen/spectral summaries may be retained as traceability context for the source and RNA feature spaces. They do not create a new promotion coordinate, do not replace the scalar/semantic audit primitives, and do not license biological chi. Regulatory autonomy is not computed in P0 D3, consistent with F4 NARROW.

## 7. Claim ceiling

D3 may establish only DISCOVERY audit states, confound/technical diagnostics, and frozen DISCOVERY-trained model parameters. It cannot establish held-out prediction, replication, selective prediction, clinical utility, causality, temporal dynamics, biological damping, an exceptional point, biological chi, or a promoted pan-cancer result.

The P0 pan-cancer promotion floor remains 24 fully evaluable cancers; P0 has 19. Any pan-cancer D3 summary is descriptive only.

## 8. Next gate

After an independent D3 audit, freeze the held-out projection/evaluation implementation before opening any REPLICATION target values. The frozen D3 architecture may not be changed in response to REPLICATION performance while preserving the current FINAL_HOLDOUT as if it remained prospectively untouched.
