# BioSystems adversarial Round 1 - public reproducibility index

**Date:** 23 September 2026
**Status:** COMPLETE / ROUND-1 RELEASE INDEX + V23 BIO CHI/TOOL CLOSURE
**Public repository:** `SymC-Universe/Biomedical`
**Round-1 adversarial branch:** `biosystems-adversarial-r1-20260923`  
**Current closure branch:** `biosystems-v23-biochi-tool-closure-20260923`
**Immutable parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Program authority:** SymC General Operations Manual v0.8.4

## Purpose

This index makes the prospective/post-result chronology independently inspectable without publishing the working manuscript.

The manuscript and supplement remain private authoring artifacts. Scientific freezes, configs, code, workflows, source identities, result artifacts, post-result audits, reviewer adjudication and release provenance remain public/versioned.

## Immutable pre-Round-1 parent

The reviewer-response release candidate was snapshotted before adversarial Round 1:

`biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`.

Round-1 work does not rewrite this branch.

## Original external prostate P1

Prospective freeze:
- `GRI_v2/reviewer/BIOSYSTEMS_EXTERNAL_PROSTATE_P1_FREEZE_20260922.md`;
- `GRI_v2/config/biosystems_external_prostate_p1_v1_0.json`.

Outcome-bearing execution:
- workflow run `35801966289`;
- artifact `GRI_BIOSYSTEMS_EXTERNAL_PROSTATE_P1_V01`;
- artifact ID `10726636434`;
- artifact digest `sha256:1d7bbef7a4f8ea0cb254c139879e8ec53b9498f8d95c9c97fa28f21367075cde`.

Post-result audit:
- `GRI_v2/reviewer/BIOSYSTEMS_EXTERNAL_PROSTATE_P1_POSTRESULT_AUDIT_20260922.md`.

The primary endpoints used tumor samples only. Adjacent tissue was not pooled into H1/H2/H3a.

## Round-1 external H1 race attack

Freeze:
- `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_H1_RACE_FREEZE_20260923.md`.

Successful execution:
- run `35812295850`;
- artifact `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_H1_RACE_V01`;
- artifact ID `10730720732`;
- artifact digest `sha256:654ad38c91ae2ba479c20641e06055465220dcf73d4fffe6734a1053f418bd94`.

Audit:
- `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_H1_RACE_AUDIT_20260923.md`.

Disposition:
`R1_H1_RACE_ROBUST` with explicit single-race EPIC refusal.

## Round-1 H1 measured-composition-preserving null

Freeze:
- `BIOSYSTEMS_ADVERSARIAL_R1_H1_COMPOSITION_FREEZE_20260923.md`.

Execution:
- run `35812910672`;
- artifact `BIOSYSTEMS_ADVERSARIAL_R1_H1_COMPOSITION_V01`;
- artifact ID `10730212562`;
- digest `sha256:fce0384e972e0f9646448546afe6bbcec3dda1214dc17460b455651274319e1d`.

Audit:
- `BIOSYSTEMS_ADVERSARIAL_R1_H1_COMPOSITION_AUDIT_20260923.md`.

Disposition:
- 30/30 positive cancer medians;
- pan-cancer median +0.0999769955;
- exact two-sided sign p `1.862645149230957e-09`;
- `R1_H1_MEASURED_COMPOSITION_ROBUST`.

## Round-1 external source metadata audit

Freeze:
- `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_METADATA_FREEZE_20260923.md`.

Execution:
- run `35815335966`;
- artifact `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_METADATA_V01`;
- artifact ID `10731351466`;
- digest `sha256:5d055b08611a8191024efb8337d62ffb87bbd2f14ec8ca66521513abb8d6fb39`.

Audit:
- `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_METADATA_AUDIT_20260923.md`.

Disposition:
`NO_ADDITIONAL_IDENTIFIABLE_TECHNICAL_COVARIATES` beyond race under the frozen source rules. This is a source limitation, not evidence that unrecorded technical structure is absent.

## Round-1 TN composition-source availability

Freeze:
- `BIOSYSTEMS_ADVERSARIAL_R1_TN_LEUKOCYTE_AVAILABILITY_FREEZE_20260923.md`.

Execution:
- run `35815627669`;
- artifact `BIOSYSTEMS_ADVERSARIAL_R1_TN_LEUKOCYTE_AVAILABILITY_V01`;
- artifact ID `10731146689`;
- digest `sha256:ef5f4dd43fcc6ccefc79e61adcfecd618c6164effcd61e4dc2120f824672a227`.

Audit:
- `BIOSYSTEMS_ADVERSARIAL_R1_TN_LEUKOCYTE_AVAILABILITY_AUDIT_20260923.md`.

Disposition:
`NO_SYMMETRIC_LEUKOCYTE_ROUTE`; zero frozen cancers satisfy a symmetric n=30 or same-participant n=20 leukocyte adjustment.

## Round-1 TN Hallmark breadth

Audit:
- `BIOSYSTEMS_ADVERSARIAL_R1_TN_HALLMARK_BREADTH_AUDIT_20260923.md`.

Post-hoc descriptive result:
- TN-A1: 49/50, 47/50, 50/50 Hallmark medians lower in tumor;
- TN-P20: 48/50, 48/50, 50/50.

This attacks concentration in a small immune-module subset but does not remove composition confounding.

## Round-1 external P1 Monte Carlo precision

Freeze:
- `BIOSYSTEMS_ADVERSARIAL_R1_P1_PRECISION_FREEZE_20260923.md`.

Initial mechanical failure:
- run `35815460649`;
- failed before any statistic because of incorrect support-file paths.

Mechanical repair:
- workflow commit `fcba7e11e5c0e46f8ff2d2722190ed6ab91e4b8c`;
- scientific contract unchanged.

Successful execution:
- run `35815566680`;
- artifact `BIOSYSTEMS_ADVERSARIAL_R1_P1_PRECISION_V01`;
- artifact ID `10731477329`;
- digest `sha256:c4a54434de5584be0f2d42defc10b82f5c3af4c9584a941ed6391f01bdaa6c65`.

Audit:
- `BIOSYSTEMS_ADVERSARIAL_R1_P1_PRECISION_AUDIT_20260923.md`.

Disposition:
`R1_P1_PRECISION_CONCORDANT`.
H1 p=0.0001, BH q=0.0003 on both primary platform lanes; H2/H3a remain unresolved/nontransporting.

## Round-1 P0 capacity criticism

Provenance discrepancy:
- `GRI_v2/docs/GRI_POSTFINAL_CAPACITY_CONTROL_PROVENANCE_DISCREPANCY_20260911.md`.

Round-1 feasibility/adjudication:
- `BIOSYSTEMS_ADVERSARIAL_R1_P0_CAPACITY_FEASIBILITY_AUDIT_20260923.md`.

Disposition:
- capacity mismatch criticism valid;
- P0 removed from central Abstract promotion;
- P0 retained only as a bounded internal observation below its frozen 24-cancer promotion floor;
- no Hallmark-specific incremental-value claim;
- no invented historical capacity-control preregistration.

## Reviewer citation adjudication

- `BIOSYSTEMS_ADVERSARIAL_R1_REVIEWER_CITATION_AUDIT_20260923.md`.

Relevant oncology/chromatin references are incorporated with claim limits; unrelated engineering-control citations are explicitly declined because the control-theoretic cancer analogy has been withdrawn.

## Global Round-1 adjudication

- `BIOSYSTEMS_ADVERSARIAL_R1_ADJUDICATION_MATRIX_20260923.md`.

This file records whether each adversarial comment is valid, partly valid, false, not identifiable, closed by a new test, or closed by claim narrowing.

## Continuity checkpoint

- `BIOSYSTEMS_ADVERSARIAL_R1_CHECKPOINT_20260923.md`.

Every long gate is frozen before execution and the checkpoint is updated before the next major run.

## Round-1 H1 composition + TSS attack

Freeze:
- `BIOSYSTEMS_ADVERSARIAL_R1_H1_TSS_FREEZE_20260923.md`.

Execution:
- run `35815819898`;
- artifact `BIOSYSTEMS_ADVERSARIAL_R1_H1_TSS_V01`;
- artifact ID `10731877118`;
- digest `sha256:d8d953f7803e8dd048a85a6bb96298315dcfd4c9eff38bd3b400731386cb4e70`.

Audit:
- `BIOSYSTEMS_ADVERSARIAL_R1_H1_TSS_AUDIT_20260923.md`.

Disposition:
- `R1_H1_COMP_TSS_ROBUST`;
- H1 composition+TSS-preserved median +0.0816210492;
- 30/30 positive cancers;
- exact two-sided sign p `1.862645149230957e-09`;
- conventional PCA PC1-fraction comparator also 30/30 positive, median +0.0685775794, same exact p.

This post-result attack preserves linear purity/leukocyte effects and TCGA TSS mean structure; it does not establish full batch/composition independence.

## V23 Bio Chi / predictive-tool reintegration

The intentionally separate Bio Chi P0-D investigation was selectively reintegrated onto the final-scrutiny submission spine at commit `fac4e3ed6f57122d93cd8a7fc25c8e2dd67fed44`. The divergent Bio Chi history was **not** merged wholesale. The reintegration copied the current `BIO_CHI/` evidence tree, dedicated Bio Chi workflows, and the two GRI/Bio-Chi bridge documents without replacing the v22 submission lineage.

Durable continuation records:
- `GRI_v2/control/BIOSYSTEMS_V23_BIOCHI_TOOL_CLOSURE_CHECKPOINT_20260923.md`;
- `GRI_v2/config/gri_biochi_tool_reintegration_v1_20260923.json`.

Current bounded dynamic evidence includes:
- executable NF-kB local/modal evidence in which a complex-conjugate pair exists but is not automatically the slowest/stability-setting mode in the nominal stable case;
- full-state smooth-coordinate numerical invariance as a necessary-not-sufficient control;
- a prospectively frozen M397 melanoma withdrawal analysis supporting return toward the pre-treatment transcriptomic state under the frozen simple distance (rho = -0.8857142857; exact one-sided p = 0.0166666667; descriptive recovery fraction approximately 0.6823).

These results reopen the dynamic-response lineage without restoring the historical static CV/2 damping interpretation. They do not establish a universal biological scalar chi, a general cancer oscillator, or an externally validated recovery predictor.

### Predictive-tool status at submission closure

The original P0 all-methylation predictor remains a bounded internal predictive result. Its stronger promotion is restricted by the existing capacity/eligibility limits and by failure of H2/H3a cross-layer transport in the independent prostate study. H1 within-methylation organization does transport independently. Accordingly, the current submission does not claim a general predictive or clinical cancer tool. The public record preserves the internal predictor, the external transport boundary, the Conglomerate Chi-bio carrier contract, and the newly reunited dynamic evidence as one auditable lineage rather than relabeling an unfinished external-validation step as success.

## Public/private boundary

Public:
- source identities/hashes;
- scientific contracts;
- code/configs/tests;
- workflows;
- machine result artifacts;
- post-result audits;
- reviewer adjudication;
- final public reproducibility index.

Private until journal submission:
- editable main-manuscript TeX;
- editable supplement TeX;
- intermediate authoring PDFs.

The private boundary does not conceal any scientific decision rule or result identity.


## Final Round-1 release binding

Final public release audit:
- `GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_FINAL_RELEASE_AUDIT_20260923.md`.

Final-clause audit:
- `GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_FINAL_CLAUSE_AUDIT_20260923.md`.

Private package:
- `BioSystems_Resubmission_R1_v12_Final_20260923.zip`;
- SHA-256 `2531ca4e3e1a72e1473c97cb4c7a402f217ed2d2068753e5a8780b1d94ee8226`.

Private main v12 PDF SHA-256:
`fdf1170705fdf86ab4ae665a855c5c974cedc2971e53fe611c51ff62a20fdf6b`.

Private supplement v10 PDF SHA-256:
`35edb01a1220ba91459ef5fa91eb175bd9db0e2d5050bfa06f932b4fc6914007`.

The manuscript text remains private; these hashes bind the private submission artifacts to the public chronology without exposing the authoring files.

The final-clause audit also binds the 30/30 exclusions (DLBC/THYM), matched 0.12332 -> 0.09998 -> 0.08162 attenuation sequence, per-cancer TSS support, 5/32 missingness-projection scope, and external paired-RNA attenuation language.

**INDEX STATUS: COMPLETE / V12 FINAL-CLAUSE RELEASE.**
