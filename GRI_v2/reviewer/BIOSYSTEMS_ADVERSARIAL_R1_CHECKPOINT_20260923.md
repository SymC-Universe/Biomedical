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

## Active scientific run

### H1 measured-composition-preserving null

Freeze:
`GRI_v2/reviewer/BIOSYSTEMS_ADVERSARIAL_R1_H1_COMPOSITION_FREEZE_20260923.md`

Runner:
`GRI_v2/src/run_biosystems_adversarial_r1_h1_composition.py`

Workflow:
`.github/workflows/biosystems-adversarial-r1-h1-composition.yml`

Active workflow run:
`35812910672`

Scientific question:
Does raw H1 remain above a null that preserves the cross-probe structure linearly explained by ABSOLUTE purity and methylation-derived leukocyte fraction?

Expected composition-complete C1 set:
30 cancers; DLBC and THYM below n=30 gate.

Primary effect:
`S_raw - S_composition_preserving_null`.

No result-dependent change to source, cohort, n, probe carrier, covariates, draw count, null, or decision rule is permitted.

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

1. Finish run 35812910672 and audit it.
2. Integrate H1 composition result without exceeding its claim ceiling.
3. Decide whether a second external cancer is scientifically necessary after the composition result; do not add one merely because it is favorable.
4. Finish main/supplement/response/cover synchronization.
5. Replace TeX en-dash markup and single-author pronoun inconsistencies.
6. Recompile main and supplement.
7. Render/visually inspect PDFs under the PDF QA workflow.
8. Run cross-file claim/value/citation audit.
9. Freeze Round-1 public adjudication matrix and provenance manifest.
10. Cut a new private resubmission candidate only if all Round-1 issues close.

## Stop rule

Do not reopen chi_bio, recovery dynamics, SCC25, or a new clinical endpoint in this manuscript.
Do not redesign P1.
Do not call H1 composition-independent unless a test actually supports that much; the active test can only address the two measured covariates.
