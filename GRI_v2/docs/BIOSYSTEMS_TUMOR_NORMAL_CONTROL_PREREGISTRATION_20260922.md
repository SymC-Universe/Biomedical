# BioSystems tumor-versus-normal control preregistration - 22 September 2026

**Status:** FROZEN BEFORE NORMAL MOLECULAR VALUES  
**Purpose:** determine whether the recurrent methylation-transcriptomic architecture reported in tumors is measurably altered relative to TCGA solid-tissue normal controls, without assuming that tumor architecture must be stronger, weaker, or absent in normal tissue.

## 1. Scientific question

The control asks a narrow specificity question:

> Do the cross-layer organizational effects that survive the frozen tumor analysis differ between primary tumors and solid-tissue normal samples from the same TCGA cancer projects?

This is not a diagnostic-classifier task and does not ask whether a model can label individual samples as cancer.

## 2. Source and representation firewall

Use only the exact already-frozen PanCanAtlas sources:

- RNA source SHA-256 `674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658`;
- methylation source SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- the same frozen Hallmark library, methylation annotation/mapping, promoter-core definition, technical mask and RNA transform used by the rebuilt C1 program.

Sample types:
- 01 = primary solid tumor;
- 11 = solid tissue normal.

No GTEx mixing is permitted in this control. Avoiding a cross-program platform mixture is intentional; external confirmation remains a separate gate.

## 3. Primary paired track

### Eligible cancers

Frozen from the outcome-blind source gate at >=20 complete cross-modal tumor-normal participant pairs:

BRCA, COAD, HNSC, KIRC, KIRP, LIHC, PRAD, THCA, UCEC.

### Sampling

- fixed n = 20 participants per cancer;
- 100 deterministic without-replacement participant draws;
- each draw uses the same 20 participants for tumor and normal;
- participant identity therefore pairs the two tissue states;
- if a cancer has exactly 20 complete pairs, the membership set is fixed and only null streams vary;
- no participant can contribute more than one unique sample root per tissue state and modality;
- any identity ambiguity is a refusal, not a value-based selection.

### Feature comparability

For each paired draw, tumor and normal are evaluated on a **shared eligible feature carrier** determined without using effect direction:

- H2 all-probe methylation carrier: a probe must satisfy the frozen finite-data rule in both tissue states;
- RNA Hallmark-union carrier: a gene must satisfy the frozen RNA finite/nonzero-variance rule in both tissue states;
- H3 promoter-core carrier: fixed mapping and Hallmark definitions; a Hallmark must meet the frozen mapping/feature-count requirements in both tissue states.

This intersection rule prevents a tumor-normal difference from being manufactured by comparing different feature inventories.

## 4. Primary endpoints

The primary family contains two endpoints because they directly express the manuscript's cross-layer architecture claim.

### TN-H2: global methylation/RNA patient geometry

Compute centered-kernel CKA separately in tumor and normal on the matched participants and shared carrier.

Use the post-C1 strengthened null treatment rather than the historical single-null shortcut:

- B = 199 deterministic within-group patient permutations per draw;
- record observed CKA, null median, null mean, null dispersion, observed-minus-null effect and headroom-normalized effect;
- primary comparison quantity = tumor minus normal headroom-normalized H2 effect within the same participant draw.

Raw CKA and raw Delta-CKA are not used as a cross-cancer effect-size ranking because the null floor depends on kernel spectra.

### TN-H3a: patient-specific Hallmark correspondence

Compute the frozen same-Hallmark methylation/RNA Hallmark coupling in tumor and normal using the common eligible Hallmark set.

- B = 199 deterministic patient permutations per draw;
- primary comparison quantity = tumor minus normal observed-minus-patient-null H3a effect within the same participant draw.

H3b same-label semantic advantage is **secondary/descriptive only** and cannot rescue TN-H2 or TN-H3a.

## 5. Secondary endpoints

- H1 methylation spectral organization may be reported as a within-layer context control, but it is not required for the tumor-specific cross-layer claim.
- H3b label specificity is descriptive and retains its current support-sensitive ceiling.
- absolute observed tumor and normal values are shown alongside null-corrected effects so a difference cannot be hidden behind a delta alone.

## 6. Cancer-level and pan-cancer inference

The biological inferential unit is cancer, not the 100 resamples.

For each cancer and endpoint:
- summarize the 100 paired draw differences by median and 5th/95th percentiles;
- the resample interval is a construction/stability interval, not 100 independent biological replicates.

Pan-cancer:
- use the 9 cancer-level median tumor-normal differences;
- exact two-sided sign test for TN-H2 and TN-H3a;
- Benjamini-Hochberg correction across the two primary endpoints only;
- report the pan-cancer median difference and all cancer directions;
- no cancer is removed for an unfavorable sign.

## 7. Interpretation / falsifier logic

No direction is prespecified.

- If tumor and normal effects are statistically indistinguishable or mixed after the frozen analysis, **tumor specificity is not supported**. The architecture may still be recurrent tissue organization.
- If tumors reproducibly show larger effects, describe **tumor-associated strengthening/reorganization** of the measured architecture, not causal activation.
- If normals reproducibly show larger effects, describe **tumor-associated weakening/disorganization**, not a failure to obtain the expected answer.
- A statistically detectable but small difference is reported as detectable, not automatically biologically large.
- No result licenses causal methylation-to-RNA direction, a clinical classifier, treatment-response prediction, biological chi, or a healthy/cancer critical boundary.

## 8. Secondary high-sample n=30 corroboration

Frozen eligible cancers: BRCA, LIHC, PRAD, THCA, UCEC.

- sample type 01 and 11 are drawn from the same TCGA project but need not come from the same participant;
- fixed n = 30 per group;
- 100 deterministic equal-n draws;
- use the same shared-carrier and repeated-null rules;
- report only as corroboration of the paired primary track, because it controls sample size more closely to C1 but not participant identity.

This track cannot overturn a failed paired primary result.

## 9. Composition limitation

ABSOLUTE tumor purity is not a symmetric normal-tissue covariate, so the C1 tumor purity/leukocyte projection is not transplanted mechanically onto normals. The paired same-patient design and within-project comparison reduce several confounds but do not make tumor-normal effects cell-intrinsic. Tissue cellular-composition differences remain an explicit limitation.

## 10. Stop rules

Stop and return an indeterminate/refusal result rather than retuning if:

- source identities differ from the frozen hashes;
- sample identities are ambiguous;
- fewer than the frozen eligible cancers survive value-independent finite-data rules;
- shared feature/Hallmark support falls below the frozen minimum for an endpoint;
- a required null stream fails or deterministic reproduction does not match;
- an analysis would require changing n, feature rules, null definitions or endpoint direction after molecular effects are inspected.

No new tumor-normal threshold is chosen after result opening.
