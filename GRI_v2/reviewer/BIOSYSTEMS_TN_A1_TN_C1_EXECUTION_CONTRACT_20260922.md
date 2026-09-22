# BioSystems TN-A1 / TN-C1 biological execution contract - 22 September 2026

**Status:** FROZEN BEFORE TYPE-11 MOLECULAR VALUE OPENING  
**Parent gate:** `BIOSYSTEMS_TUMOR_NORMAL_CONTROL_FREEZE_20260922.md`  
**Eligibility source:** `../config/biosystems_tn_c0_eligibility_v1.json`  
**Claim ceiling:** static tumor-versus-TCGA-solid-tissue-normal specificity/control evidence only; no causality, temporal progression, healthy-population claim, diagnostic utility, damping, exceptional-point, biological chi, or universal optimum claim.

## 1. Frozen evidence lanes

Three lanes remain separate and cannot rescue one another:

1. **TN-A1 RNA primary:** 12 frozen cancers at n=30 tumor and n=30 normal.
2. **TN-C1 multiomic primary:** 5 frozen cancers at n=30 RNA+methylation overlap in each state.
3. **TN-P20 paired RNA sensitivity:** 13 frozen cancers with >=20 participants carrying both type-01 and type-11 RNA.

The exact cancer lists are the TN-C0 config and may not change after value opening.

## 2. Sample identity and duplicate rule

Quality eligibility is inherited from the exact PanCan sample-quality annotation used in TN-C0. Samples marked `Do_not_use` remain excluded.

State definitions:
- type 01 = Primary Solid Tumor;
- type 11 = Solid Tissue Normal.

Participant is the inferential sampling identity.

If more than one quality-eligible source column exists for the same participant, assay, and state, that participant is excluded from that assay/state rather than choosing an aliquot after seeing values. TN-C0 established no duplicate type-11 participants in either RNA or methylation, so this rule primarily protects the tumor side from fresh aliquot selection.

## 3. RNA source and construction

Source is the exact PanCanAtlas EB++ RNA matrix already frozen in Stage A:
- source SHA-256: `674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658`;
- finite transform: `log2(max(expression,0)+1)`;
- source non-finite cells remain missing;
- Hallmark membership: exact v2026.1.Hs snapshot, deterministic membership SHA-256 `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`.

RNA module metrics are unchanged Stage A definitions:
- `C_in,pair`: median absolute pairwise Pearson correlation;
- `C_in,PC1`: PC1 standardized variance fraction;
- `C_out`: median absolute correlation of oriented Hallmark eigengene to eligible genes outside the module within the frozen Hallmark-union background.

Eligibility/missingness stays unchanged:
- >=95% finite within the current n draw;
- >=20 finite samples;
- nonzero finite variance;
- >=15 mapped genes per Hallmark;
- pairwise overlap >=80% of draw and >=20 samples;
- PCA standardized missing cells may be zero only as within-gene standardized-mean completion.

## 4. TN-A1 deterministic resampling

For every frozen RNA-primary cancer:

- n=30 type-01 participants per draw;
- n=30 type-11 participants per draw;
- 100 without-replacement draws per state;
- seed namespace: `GRI_BIOSYS_TN_A1_20260922`;
- deterministic seed for a state/draw is SHA-256 of `namespace|cancer|state|draw`, first 64 bits reduced modulo 2^32;
- tumor and normal draws are generated independently from their own state tokens.

For each state/draw:
1. compute all three Stage A coordinates for all evaluable Hallmarks;
2. retain module-level outputs;
3. define the draw-level cancer coordinate as the median across evaluable Hallmarks separately for each of the three coordinates.

For each cancer/coordinate:
- state estimate = median of 100 draw-level medians;
- uncertainty = q05/q95 of the 100 draw-level medians;
- tumor-normal effect = median across draw index of `tumor_draw - normal_draw`; draw pairing is only a deterministic Monte-Carlo bookkeeping device and is not treated as independent inference.

Primary pan-cancer inference:
- cancer is the inferential unit;
- two-sided exact sign test on the 12 cancer-level tumor-normal effects;
- exact-zero ties excluded from binomial n;
- BH correction across the three RNA coordinate tests;
- no direction is prespecified;
- q<0.05 may be reported, but a non-significant result remains the frozen result.

Module-specific tumor-normal differences are secondary descriptive outputs and cannot rescue the three primary coordinate tests.

## 5. TN-P20 paired RNA sensitivity

For each frozen paired-sensitivity cancer:

- use only participants having both type-01 and type-11 RNA;
- if paired n >=20, run 100 deterministic without-replacement paired draws of exactly n=20 participants;
- seed namespace: `GRI_BIOSYS_TN_P20_20260922`;
- the same participant set is used in tumor and normal for a given draw;
- compute the same three Stage A coordinates;
- summarize exactly as TN-A1;
- pan-cancer exact two-sided sign tests with BH across three coordinates.

This is sensitivity evidence and cannot replace TN-A1.

## 6. TN-C1 multiomic construction

For each frozen multiomic-primary cancer, use n=30 independent participants per tissue state per draw who are quality-eligible in both RNA and methylation.

Methylation source and Stage C1 definitions remain inherited:
- exact beta source SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- exact 22,601-probe order;
- frozen Stage C1 technical mask / probe-gene-region mapping;
- frozen v2.1/v2.2 RNA missingness behavior;
- PROMOTER_CORE remains the primary stratum;
- PRIMARY_PUBLICATION remains the primary probe track;
- MASKED_TECHNICAL is a robustness track and cannot rescue the primary track;
- minimum common Hallmarks = 25.

Seed namespace for tissue-state C1 resampling/nulls: `GRI_BIOSYS_TN_C1_20260922`, using the already-frozen C1 `stable_seed` tokenization with tissue state appended to the cancer token.

For each state/draw/track, retain:
- H1: `delta_s = s_spec - null_s_spec`;
- H2: `delta_cka = CKA - patient-null CKA`;
- H3a: `delta_a_patient = same-Hallmark coupling - patient-null coupling`;
- H3b: `delta_a_label = same-Hallmark coupling - label-null coupling`.

Composition-adjusted C1 quantities are **not primary tumor-normal tests** because the frozen purity/leukocyte covariates were defined for primary tumors and are not symmetrically available/valid for type-11 normal tissue. They may be shown for the tumor state only as inherited context evidence, never as a tumor-normal adjusted contrast.

For each cancer/hypothesis:
- state estimate = median across 100 valid draws;
- tumor-normal effect = median of deterministic draw-index differences;
- q25/q75 and q05/q95 retained as construction uncertainty.

Pan-cancer inference across the five multiomic cancers:
- two-sided exact sign test, cancer as unit;
- BH across H1/H2/H3a/H3b;
- with n=5, the design is explicitly recognized as effect/consistency evidence with limited exact-test resolution; lack of q<0.05 cannot be redefined as failure of the control itself.

No C1 promotion ladder is applied to normal tissue. The question is state contrast, not whether normals satisfy the tumor C1 promotion hierarchy.

## 7. Outcome classes

After opening values, each primary quantity is assigned without changing the rules:

- `TN-SPECIFIC`: reproducible tumor-normal shift with direction/effect reported.
- `TN-SHARED_WITH_SHIFT`: architecture above its construction floor in both states with a quantitative shift.
- `TN-SHARED_NO_RESOLVED_SHIFT`: architecture present in both with no resolved primary shift.
- `TN-HETEROGENEOUS`: cancer-level directions materially mixed.
- `TN-NOT_EVALUABLE`: frozen representation/coverage rules fail.

## 8. Required outputs

At minimum:
- exact participant/sample manifest per lane/state/cancer;
- all deterministic resample memberships;
- RNA module-level metrics;
- RNA cancer-level state/effect summary;
- RNA global inference table;
- paired-sensitivity summary/inference;
- C1 state-level resample metrics for H1-H3b;
- C1 cancer-level state/effect summary;
- C1 global inference table;
- exclusions/refusals;
- source/code/config hashes;
- machine-readable run summary;
- reviewer-ready plain-language result paragraph.

## 9. Stop / amendment rule

After this file is committed, type-11 molecular values may be opened.

No cancer set, n, seed namespace, module definition, C1 primary stratum, technical track status, null type, effect definition, inferential unit, multiplicity family, or outcome vocabulary may change in response to observed tumor-normal results. Any necessary post-open correction must be explicit, versioned, justified as mechanical/scientific, and may not silently rescue an unfavorable result.
