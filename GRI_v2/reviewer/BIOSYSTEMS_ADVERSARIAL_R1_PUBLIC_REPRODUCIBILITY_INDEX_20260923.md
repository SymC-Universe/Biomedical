# BioSystems adversarial Round 1 - public reproducibility index

**Date:** 23 September 2026
**Status:** COMPLETE / ROUND-1 RELEASE INDEX
**Public repository:** `SymC-Universe/Biomedical`
**Adversarial branch:** `biosystems-adversarial-r1-20260923`
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

Private package:
- `BioSystems_Resubmission_R1_Final_20260923.zip`;
- SHA-256 `7a27d9942e9566ec4eb563dfd71c0db27b9f9924d928f573b672cb5fb963aeef`.

Private main PDF SHA-256:
`1920411994aa18cd60533e042c5d90dad9eac9ad9c219f12b9a423294ca1f91a`.

Private supplement PDF SHA-256:
`ae59d743d130e371306c00466ce8b94c0e3f84546dcb8d4babf4cb16c248b14a`.

The manuscript text remains private; these hashes bind the private submission artifacts to the public chronology without exposing the authoring files.

**INDEX STATUS: COMPLETE.**
