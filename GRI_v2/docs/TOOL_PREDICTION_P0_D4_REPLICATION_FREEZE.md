# P0 D4 untouched REPLICATION projection and evaluation freeze

**STATUS: FROZEN AFTER D3 PASS AND BEFORE ANY REPLICATION METHYLATION VALUE OR RNA TARGET SCORE IS COMPUTED**

Date: 2026-08-30

Upstream anchors:
- P0 holdout protocol: `GRI_v2/docs/TOOL_PREDICTION_P0_HOLDOUT_FREEZE_20260830.md`
- D1 source audit: `GRI_v2/artifacts/P0_D1_DISCOVERY_SOURCE_AUDIT.md`
- D2 target audit: `GRI_v2/artifacts/P0_D2_RNA_DISCOVERY_TARGET_AUDIT.md`
- D3 discovery audit/model audit: `GRI_v2/artifacts/P0_D3_DISCOVERY_AUDIT_MODEL_AUDIT.md`
- D3 freeze and pre-compute seed correction remain authoritative for discovery architecture.

D4 opens **REPLICATION only**. FINAL_HOLDOUT remains sealed. D4 is evaluation, not training: no D1/D2 transform, D3 model, threshold, null count, state rule, feature definition, covariate regression, or decision class may be refit or tuned from REPLICATION.

## 1. Frozen REPLICATION cohort

Use only participants that:
1. belong to one of the frozen 19 P0-evaluable cancers;
2. were deterministically assigned `REPLICATION` under P0;
3. passed the already-frozen per-sample >=95% primary-probe methylation eligibility rule.

Pre-value reconstruction from the already-audited split/eligibility manifests yields 1,625 eligible REPLICATION participants:

- BLCA 83
- BRCA 205
- CESC 58
- COAD 90
- HNSC 91
- KIRC 110
- KIRP 44
- LGG 94
- LIHC 69
- LUAD 101
- LUSC 103
- OV 66
- PAAD 36
- PCPG 34
- PRAD 101
- SARC 51
- STAD 73
- THCA 109
- UCEC 107

No participant may be moved, replaced, or borrowed from FINAL_HOLDOUT.

The already-frozen B1 covariate matching rules yield 1,478 REPLICATION participants with both ABSOLUTE purity and methylation-derived leukocyte fraction available, before any REPLICATION target score is generated. Cancer-specific complete-case counts are:

BLCA 82, BRCA 195, CESC 55, COAD 78, HNSC 83, KIRC 72, KIRP 42, LGG 89, LIHC 66, LUAD 95, LUSC 99, OV 49, PAAD 35, PCPG 30, PRAD 95, SARC 49, STAD 68, THCA 97, UCEC 99.

All 19 remain evaluable for the frozen P1 model-comparison branch. Covariate missingness is not imputed.

## 2. Frozen methylation source projection

D4 uses the exact 5.02 GB C0 methylation source (SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`). The file may be fully hashed for provenance, but numeric beta values are parsed only for the 1,625 eligible REPLICATION columns. FINAL_HOLDOUT numeric methylation values are never parsed or used.

For each cancer:
1. use the exact D1 DISCOVERY-retained probes;
2. replace a non-finite REPLICATION beta cell with that probe's frozen D1 DISCOVERY imputation median;
3. use the exact frozen TSS200 probe-to-gene mapping;
4. compute each gene score as the median across its unique retained TSS200 probes;
5. PRIMARY_PUBLICATION uses D1 `retained_primary_95pct`;
6. MASKED_TECHNICAL uses D1 `retained_masked_technical`;
7. apply the exact D1 DISCOVERY gene means and PC1 loadings without refitting to generate the 45 source Hallmark scores per technical track.

For compact projection, D4 uses `TSS200_Probe_Gene_Map.csv.gz`, mechanically regenerated before REPLICATION from the frozen C1A annotation and independently reconciled to D1 `tss200_gene_count` for all 22,601 source probes. It contains 4,125 unique probe-gene rows, 3,999 unique TSS200 probes, and 3,949 genes. SHA-256: `5d42e66a205bdb8579b5edacc465c9dc74a86d6d185d28b9287fc232226a58b6`.

## 3. Frozen RNA target projection

Use the exact Stage A Hallmark-union RNA cache (SHA-256 `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`). Select only the exact eligible REPLICATION participant/cancer rows for target construction.

For each cancer/Hallmark:
1. use the exact D2 DISCOVERY-retained RNA genes;
2. replace a non-finite REPLICATION expression cell with that gene's frozen D2 DISCOVERY mean;
3. subtract that same frozen discovery mean;
4. apply the exact D2 PC1 loading vector without refitting;
5. generate all 50 REPLICATION RNA Hallmark targets.

The Stage A cache is a previously frozen multi-partition artifact. D4 may decompress/access that cache as required by its storage format, but only REPLICATION participant rows are selected into any D4 target transformation, statistic, model score, or output. No FINAL_HOLDOUT target score is generated or inspected.

## 4. Covariates and complete-case rule

Use the same exact B1 sources and matching rules as D3:
- ABSOLUTE purity SHA-256 `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`;
- methylation-derived leukocyte fraction SHA-256 `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`.

No covariate imputation. P1 model evaluation and composition-adjusted P2 audit use only REPLICATION participants with both covariates finite. Raw P2 audit screens use all 1,625 eligible REPLICATION participants.

## 5. P1 REPLICATION prediction scoring

Project the frozen D3 models without any refit.

Models:
- `MEAN_ONLY`: frozen D3 target intercepts;
- `COVARIATE_ONLY`: frozen D3 predictor means/scales, alpha-selected coefficients, and intercepts;
- `SAME_HALLMARK_ONLY`: frozen D3 per-target models for the 45 source-mapping-eligible Hallmarks; the five source-ineligible targets remain `NOT_EVALUABLE_SOURCE_MAPPING`;
- `ALL_METHYLATION_RIDGE`: frozen D3 PRIMARY_PUBLICATION source + B1 covariate model for all 50 targets.

For each cancer/target/model report:

`MSE = mean((y_rep - yhat_rep)^2)`.

`normalized_MSE = MSE / discovery_target_variance`, where the denominator is the exact D3 `Target_Reference.csv` variance.

Held-out R2 is explicitly frozen as relative to the discovery target mean:

`R2 = 1 - sum((y_rep - yhat_rep)^2) / sum((y_rep - discovery_target_mean)^2)`.

If the R2 denominator is zero/non-finite, record `NOT_EVALUABLE`; do not alter the target.

Negative R2 and extreme normalized MSE are retained.

Within cancer, aggregate each model by the median across its evaluable target Hallmarks. The primary paired REPLICATION model-comparison quantity is cancer-median normalized MSE; lower is better. Compare `ALL_METHYLATION_RIDGE` versus `COVARIATE_ONLY` with an exact one-sided paired sign test across the 19 cancers. Because 19 < the frozen 24-cancer promotion floor, this pan-cancer comparison is descriptive only regardless of p-value.

## 6. P2 REPLICATION audit-state evaluation

Recompute the same F2/P0 audit machinery on REPLICATION using only frozen D1/D2 projections and frozen D3 rules.

D4 null namespace:

`GRI_V2_PREDICTION_P0_20260830|D4|REPLICATION`

The seed algorithm is the already-established F2 algorithm: join namespace and parts with `|`, SHA-256 UTF-8, first 8 bytes unsigned big-endian, modulo `2**32`.

All null families retain 39 permutations and the unchanged D3 thresholds.

### 6.1 Raw screens

For each technical track:
- global linear CKA uses projected source scores versus all 50 RNA targets;
- semantic patient and Hallmark-label screens use the exact 45 common Hallmarks;
- source PRIMARY_PUBLICATION and RNA target within-layer `S_spec` use the same independent-feature marginal-permutation construction null.

### 6.2 Composition-adjusted screens

Do **not** fit composition regressions in REPLICATION.

Use the exact D3 discovery-fitted `Composition_Parameters.csv.gz` coefficients, covariate means, and covariate scales to project residuals into REPLICATION complete cases:

`residual = observed - [intercept + beta_purity_scaled * ((purity - discovery_purity_mean)/discovery_purity_scale) + beta_leukocyte_scaled * ((leukocyte - discovery_leukocyte_mean)/discovery_leukocyte_scale)]`.

Then run the unchanged global/semantic null machinery on those frozen-projection residuals. This is evaluation of the discovery-fitted confound attack, not refitting.

### 6.3 Replication state

Apply the exact D3 five-state logic unchanged to produce one REPLICATION state and decision class per cancer.

Primary P2 outputs:
- exact five-state agreement between D3 DISCOVERY and D4 REPLICATION;
- ACCEPT versus non-ACCEPT confusion matrix;
- precision, recall, specificity, balanced accuracy, and Matthews correlation where mathematically defined;
- undefined metrics are `NOT_EVALUABLE`, with no smoothing or continuity correction.

## 7. Hallmark-level semantic effect preservation

For the PRIMARY_PUBLICATION common 45 Hallmarks, reconstruct per-Hallmark discovery and replication semantic effects under their respective frozen patient- and label-null permutations.

For a Hallmark, define a positive patient effect when its observed absolute Spearman correlation exceeds the median of its patient-null absolute correlations. Define a positive label effect analogously against its label-null median.

A Hallmark has `PRESERVED_POSITIVE_BOTH` only when both effects are positive in DISCOVERY and both are positive again in REPLICATION.

Report per cancer:
- discovery positive-both count;
- replication positive-both count;
- preserved positive-both count;
- preserved fraction over the 45 common Hallmarks.

This is a sign/effect preservation diagnostic, not a new significance threshold.

## 8. Frozen P2 comparators and guardrail ablations

All comparator/ablation rules are fixed before REPLICATION target scores are generated.

Binary favorable status for P2 forecasting:

- `GLOBAL_ONLY`: PRIMARY_PUBLICATION raw global CKA gate passes. Ignores semantic, composition, and technical-track requirements.
- `NAIVE_SEMANTIC`: PRIMARY_PUBLICATION raw global gate and PRIMARY_PUBLICATION raw patient-semantic gate pass. It intentionally omits the Hallmark-label null and the composition/technical guardrails.
- `NO_LABEL_NULL`: requires raw and composition-adjusted global + patient-semantic gates to pass on both technical tracks; the Hallmark-label gate alone is removed.
- `NO_COMPOSITION_ATTACK`: requires raw global + full patient-and-label semantic gates on both technical tracks; composition adjustment alone is removed.
- `NO_TECHNICAL_TRACK`: requires PRIMARY_PUBLICATION raw and adjusted global + full semantic gates; MASKED_TECHNICAL agreement alone is removed.
- `FULL_NARROWED_AUDIT`: favorable only when the unchanged full state is `SEMANTIC_SHARED_ROBUST` / ACCEPT.

For each rule, reconstruct the DISCOVERY favorable flag from frozen D3 outputs and independently compute the REPLICATION favorable flag. Report agreement and the same binary confusion metrics, preserving `NOT_EVALUABLE` where a class is absent.

These ablations do not authorize architecture changes after REPLICATION. Component-retention decisions remain deferred until the preregistered P3 FINAL_HOLDOUT selective-prediction evidence is also available.

## 9. FINAL_HOLDOUT firewall

D4 must not:
- parse FINAL_HOLDOUT methylation beta columns;
- generate FINAL_HOLDOUT RNA Hallmark target scores;
- project D3 models into FINAL_HOLDOUT;
- compute FINAL_HOLDOUT errors;
- alter D3 transforms/models/states based on REPLICATION;
- change thresholds, null counts, state logic, source mapping, covariate rules, or model architecture after seeing REPLICATION.

If a software defect is discovered, document it, add a regression test, repair only the defect, preserve the superseded output, and rerun the minimum required stage without changing scientific definitions.

## 10. Claim ceiling and next gate

D4 may establish REPLICATION predictive performance and prospective replication of the discovery audit state under the frozen P0 design. It cannot establish FINAL_HOLDOUT selective-prediction performance, external-cohort portability, clinical utility, causality, temporal dynamics, biological damping, exceptional points, or biological chi.

The pan-cancer P0 promotion floor remains 24 cancers and is unreachable with 19 P0-evaluable cancers; any P0 pan-cancer statement remains descriptive.

After an independently clean D4 audit, freeze the P3 FINAL_HOLDOUT projection/evaluation implementation before opening FINAL_HOLDOUT. The current D3/D4 architecture may not be retuned from REPLICATION while treating the existing final partition as a prospective validation of that modified architecture.
