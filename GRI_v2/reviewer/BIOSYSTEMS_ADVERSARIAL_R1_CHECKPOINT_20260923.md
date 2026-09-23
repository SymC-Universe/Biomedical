# BioSystems adversarial Round 1 checkpoint

**Date:** 23 September 2026
**Status:** COMPLETE / SUBMISSION READY
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

Final Round-1 private release after final-clause tightening:
- `GRI_BioSystems_working_v12_R1_2026-09-23.tex/.pdf`;
- `GRI_BioSystems_supplement_working_v10_R1_2026-09-23.tex/.pdf`;
- `BioSystems_Response_to_Reviewers_v4_R1_2026-09-23.md/.pdf`;
- `BioSystems_Cover_Letter_v4_R1_2026-09-23.md/.pdf`;
- `BioSystems_Submission_Metadata_v2_R1_2026-09-23.md`.

Candidate title:
*Recurrent Methylation Organization Across Human Cancers with Context-Dependent Methylation-RNA Coupling*

The final-clause pass is complete. Exact denominator identities, matched stronger-null attenuation, per-cancer TSS support, missingness-scope limits, and the external RNA attenuation wording are now incorporated. PDF/reviewer-package QA was repeated.

## Final Round-1 completion state

All Round-1 queue items are complete.

### Scientific controls
- external P1 tissue-state ambiguity: reviewer hypothesis false; primary H1/H2/H3a are tumor-only;
- external H1 race sensitivity: complete / robust to source-declared AA/EA axis;
- H1 measured-composition-preserving null: complete / 30 of 30 positive;
- H1 composition + TCGA TSS-preserving null: complete / 30 of 30 positive;
- conventional PCA matched comparator: complete / 30 of 30 positive under the stronger null;
- external metadata/technical source audit: complete / no additional source-identifiable covariate beyond race;
- TN leukocyte availability: complete / no symmetric frozen-source route;
- TN Hallmark breadth: complete / direction broad, not composition-independent;
- external P1 B=9,999 precision: complete / H1 retained, H2/H3a nontransport retained;
- P0 capacity criticism: closed by claim compression; no retroactive capacity-control claim;
- reviewer citation audit: complete;
- standard-toolkit framing/comparator: complete with matched PCA comparator and no superiority claim;
- biological chi / exceptional-point / recovery wording removed from active claim frame.

### Private release candidate
- main: `GRI_BioSystems_working_v12_R1_2026-09-23.tex/.pdf`;
- supplement: `GRI_BioSystems_supplement_working_v10_R1_2026-09-23.tex/.pdf`;
- reviewer response: `BioSystems_Response_to_Reviewers_v4_R1_2026-09-23.md/.pdf`;
- cover letter: `BioSystems_Cover_Letter_v4_R1_2026-09-23.md/.pdf`;
- private package: `BioSystems_Resubmission_R1_v12_Final_20260923.zip`;
- package SHA-256: `2531ca4e3e1a72e1473c97cb4c7a402f217ed2d2068753e5a8780b1d94ee8226`.

### Visual / release QA
- main: 19 pages rendered and inspected;
- supplement: 14 pages rendered and inspected;
- response: 6 pages rendered and inspected;
- cover letter: 2 pages rendered and inspected;
- no material clipping, overlap, broken figure placement, or page-flow defect found.

### Public closure
- `BIOSYSTEMS_ADVERSARIAL_R1_FINAL_CLAUSE_AUDIT_20260923.md`;
- `BIOSYSTEMS_ADVERSARIAL_R1_PUBLIC_REPRODUCIBILITY_INDEX_20260923.md`;
- `BIOSYSTEMS_ADVERSARIAL_R1_ADJUDICATION_MATRIX_20260923.md`;
- `BIOSYSTEMS_ADVERSARIAL_R1_FINAL_RELEASE_AUDIT_20260923.md`.

## Stop rule

Round 1 is complete. Do not reopen chi_bio, recovery dynamics, SCC25, a new clinical endpoint, or a new external cohort inside this frozen revision unless the user explicitly opens a new scientific branch.

Final-clause release hashes and exact TSS support are frozen in `BIOSYSTEMS_ADVERSARIAL_R1_FINAL_CLAUSE_AUDIT_20260923.md`.

**STATUS: COMPLETE / SUBMISSION READY**
