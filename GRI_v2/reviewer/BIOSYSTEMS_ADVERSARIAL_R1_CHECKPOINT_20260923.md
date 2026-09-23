# BioSystems adversarial Round 1 checkpoint

**Date:** 23 September 2026
**Status:** ACTIVE
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Program authority:** SymC General Operations Manual v0.8.4

## Purpose

Adjudicate two independent adversarial reviews of the v10 submission package without post-result retuning. The v10 release remains preserved and unchanged. Round 1 additions are explicitly post-release reviewer-round corrections/sensitivities.

## Closed Round 1 findings

### External P1 tissue-state ambiguity
**RESOLVED / REVIEWER HYPOTHESIS FALSE.**

Inspection of `run_biosystems_external_prostate_p1.py` confirms primary H1/H2/H3a are computed on tumor samples only:
- methylation input = `m30["tumor"]`;
- RNA input = `r30["tumor"]`;
- adjacent samples are used for symmetric probe eligibility and the separately declared tumor-normal contrast.

The external H1 magnitude is therefore not a pooled tumor/adjacent state-separation artifact.

### External H1 AA/EA axis
**CLOSED / R1_H1_RACE_ROBUST.**

Freeze:
`GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_H1_RACE_FREEZE_20260923.md`

Successful run:
- workflow `35812295850`;
- artifact `BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_H1_RACE_V01`;
- artifact ID `10730720732`;
- artifact SHA-256 `654ad38c91ae2ba479c20641e06055465220dcf73d4fffe6734a1053f418bd94`.

Primary 450K n=30 (25 AA/5 EA):
- raw H1 +0.303090;
- per-CpG race-residualized H1 +0.316952;
- 104.6% effect retention;
- AA-only n=25 +0.306226;
- empirical p=0.001 for each.

EPIC is 26/26 EA and retains raw H1 +0.358394, p=0.001.

Race is not a sufficient explanation. Purity, broader composition, batch/center/plate, subtype, age and other structured covariance remain unresolved.

Audit:
`GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_EXTERNAL_H1_RACE_AUDIT_20260923.md`.

### Tumor-normal RNA Hallmark breadth
**POST-HOC ADVERSARIAL SENSITIVITY COMPLETE.**

Using already frozen TN RNA outputs:
- TN-A1 pairwise: 49/50 Hallmark pan-cancer medians lower in tumor;
- TN-A1 PC1: 47/50 lower;
- TN-A1 C_out: 50/50 lower;
- TN-P20 paired: 48/50, 48/50 and 50/50 lower.

The direction is not concentrated in a small immune/inflammatory module set. This does not remove tissue-composition confounding and must remain labeled post-hoc.

### P0 promotion/capacity issue
**CLAIM NARROWED; NO RETROACTIVE CONTROL CLAIM.**

Repository provenance audit establishes that an exact historical executable equal-capacity freeze was not recovered. v10 wording that the control was already frozen is inaccurate.

Round 1 disposition:
- only 19 cancers met the frozen 24-cancer pan-cancer promotion floor;
- P0 therefore remains a bounded internal held-out observation;
- remove P0 from Abstract central evidence;
- 47-predictor versus 2-predictor result is not used to claim Hallmark-specific incremental value;
- no retrospective claim that a capacity control was preregistered.

A future equal-capacity P0-Q test is optional and cannot upgrade the original holdout.

### External H2/H3a interpretation
**CLAIM NARROWED.**

Primary external H2 = +0.019724, approximately 8.6% of internal median H2 +0.2295, q=0.4065.

Round 1 wording:
- no detectable external H2 transport;
- not described as a power-limited positive result;
- H3a also no transport;
- `P1_REPRESENTATION_DEPENDENT` is retained because it was the preregistered conflict label, but it is explicitly procedural and does not establish a true representation-specific sign reversal when both platform estimates are null-compatible.

### External RNA representation
**EXPLICIT LIMIT ADDED.**

TCGA RNA = EB++ batch-adjusted RSEM transformed by log2(max(x,0)+1).
External RNA = raw counts normalized by frozen median-ratio method then log2(normalized+1).

H2/H3a are RNA-dependent and their external nontransport cannot be assigned uniquely to cohort biology versus RNA representation.

### Reviewer-suggested citations
**ADJUDICATED.**

Reviewer 1 cancer-regulation citations are relevant and added:
- PMID 39485254;
- PMID 39617063;
- PMID 38409266.

Reviewer 2 boost-converter / EV-control / drilling-control papers are outside the scope of the revised static oncology manuscript after the control-theoretic cancer analogy was withdrawn. The response letter explicitly and respectfully declines them instead of silently ignoring them.

### Lingering control/chi vocabulary
**REMOVED FROM CURRENT CLAIM FRAME.**

Main v11 conclusion no longer invokes biological chi, exceptional-point behavior or substrate/recovery lineage.
Supplement candidate removes the candidate-chi section and unnecessary exceptional-point reminders.

## Closed H1 measured-composition gate

### H1 measured-composition-preserving null
**CLOSED / R1_H1_MEASURED_COMPOSITION_ROBUST.**

Freeze:
`GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_H1_COMPOSITION_FREEZE_20260923.md`

Successful run:
- workflow `35812910672`;
- artifact `BIOSYSTEMS_ADVERSARIAL_R1_H1_COMPOSITION_V01`;
- artifact ID `10730212562`;
- artifact SHA-256 `fce0384e972e0f9646448546afe6bbcec3dda1214dc17460b455651274319e1d`.

Across the 30 frozen composition-complete cancers:
- positive cancer medians 30/30;
- pan-cancer median `delta_comp_preserved = 0.0999769955`;
- IQR 0.0727836524 to 0.1097330090;
- exact two-sided sign-test p = 1.862645149230957e-09.

This closes only the two measured linear composition axes (ABSOLUTE purity and methylation-derived leukocyte fraction). It does not remove batch, plate, center, array, subtype, age, sex, ancestry, stromal structure, or other latent covariance.

Audit:
`GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_H1_COMPOSITION_AUDIT_20260923.md`.

## Private candidate manuscript state

The v10 release remains the immutable parent.

Current Round-1 private candidates in local working state:
- `GRI_BioSystems_working_v11_R1_2026-09-23.tex`;
- `GRI_BioSystems_supplement_working_v9_R1_2026-09-23.tex`;
- `BioSystems_Response_to_Reviewers_v3_R1_2026-09-23.md`;
- `BioSystems_Cover_Letter_v3_R1_2026-09-23.md`;
- `BioSystems_Submission_Metadata_v2_R1_2026-09-23.md`.

Candidate title:
*Recurrent Methylation Organization Across Human Cancers with Context-Dependent Methylation-RNA Coupling*

The candidates are not final until the active H1 composition test is incorporated and PDF/reviewer-package QA is repeated.

## Remaining queue

1. **External prostate metadata/technical audit: COMPLETE.** Run `35815335966`, artifact `10731351466`, digest `sha256:5d055b08611a8191024efb8337d62ffb87bbd2f14ec8ca66521513abb8d6fb39`. Only race qualified as an adjustment candidate; race was already attacked successfully. Disposition `NO_ADDITIONAL_IDENTIFIABLE_TECHNICAL_COVARIATES`. Broader unrecorded batch/plate/site/age/sex structure remains an explicit limitation.
2. **P0 equal-capacity issue: CLOSED BY CLAIM COMPRESSION / RUN-ECONOMY AUDIT.** The criticism is valid. P0 is removed from Abstract central evidence and cannot claim Hallmark-specific incremental value. A fair 45-dimensional generic-methylation comparator would require rebuilding the full 5.02 GB methylation / 1.88 GB RNA source-projection chain as a new post-FINAL experiment because participant-level FINAL matrices and a historical executable capacity-control freeze are not preserved. `BIOSYSTEMS_ADVERSARIAL_R1_P0_CAPACITY_FEASIBILITY_AUDIT_20260923.md` records why that rebuild is not warranted after withdrawing the stronger claim.
3. **Tumor-normal composition attack: CLOSED WITH LIMIT.** Hallmark breadth is 49/50, 47/50, 50/50 lower in TN-A1 and 48/50, 48/50, 50/50 in TN-P20. Source-only leukocyte audit run `35815627669`, artifact `10731146689`, digest `sha256:ef5f4dd43fcc6ccefc79e61adcfecd618c6164effcd61e4dc2120f824672a227` found zero cancers meeting symmetric n=30 or paired-n20 leukocyte coverage. Disposition `NO_SYMMETRIC_LEUKOCYTE_ROUTE`. TN must remain an unadjusted tissue-state contrast; composition independence is not claimed.
4. **External permutation precision: COMPLETE.** Repaired run `35815566680`, artifact `10731477329`, digest `sha256:c4a54434de5584be0f2d42defc10b82f5c3af4c9584a941ed6391f01bdaa6c65`. Disposition `R1_P1_PRECISION_CONCORDANT`. Primary 450K and EPIC H1 each remain at the finer B=9,999 floor (`p=0.0001`, BH `q=0.0003`); H2/H3a remain unresolved/nontransporting. Original P1 classification unchanged.
5. **External RNA representation.** Do not apply DESeq median-ratio normalization to TCGA EB++ RSEM because those are not raw counts. Instead, explicitly test any legitimate same-object transform sensitivity available from the existing TCGA representation, or retain RNA-representation mismatch as an unresolved external limitation.
6. **Standard-toolkit / technical comparator: COMPLETE MATCHED ATTACK.** Run `35815819898`, artifact `10731877118`, digest `sha256:d8d953f7803e8dd048a85a6bb96298315dcfd4c9eff38bd3b400731386cb4e70`. H1 remains positive in 30/30 composition-complete cancers after preserving linear purity/leukocyte and TCGA Tissue Source Site mean structure (median +0.0816210; exact p=1.86e-9). Ordinary PCA PC1 concentration is also positive 30/30 against the identical stronger null (median +0.0685776; exact p=1.86e-9). MOFA/SNF/DIABLO are not run merely for optics because they do not answer this exact within-layer null question and no superiority claim is made over them.
7. **Reporting fixes.** Name all TN-A1/TN-P20 cancers; remove stale shared-missingness text; distinguish “no gate remains for this revision” from future P0-Q controls; remove first-person abstract language; normalize single-author pronouns; remove unnecessary en-dash markup; correct title/abstract/response wording.
8. **Reviewer citation response: COMPLETE.** Bibliographic and scope adjudication is frozen in `BIOSYSTEMS_ADVERSARIAL_R1_REVIEWER_CITATION_AUDIT_20260923.md`: PMIDs 39485254, 39617063, 38409266 are relevant with limits; unrelated engineering-control references are explicitly declined after withdrawal of the control-theory analogy.
9. **Public reproducibility.** Keep freeze contracts, configs, workflows, result audits, reviewer adjudication, and release provenance in GitHub. Keep only manuscript/supplement text private. Prepare a public reproducibility index suitable for Zenodo snapshotting before resubmission.
10. **Private release candidate.** After scientific controls close, rebuild the private main/supplement, compile, render, visually inspect, cross-audit all claims/values/citations, and cut a new Round-1 resubmission package.

Every completed gate must update this checkpoint before the next long workflow begins.

### H1 technical gate closure

`BIOSYSTEMS_ADVERSARIAL_R1_H1_TSS_AUDIT_20260923.md` closes the composition+TSS-preserving H1 attack as `R1_H1_COMP_TSS_ROBUST`. This remains a post-result adversarial sensitivity and cannot retroactively promote C1.

## Stop rule

Do not reopen chi_bio, recovery dynamics, SCC25, or a new clinical endpoint in this manuscript.
Do not redesign P1.
Do not call H1 composition-independent unless a test actually supports that much; the active test can only address the two measured covariates.
