# BioSystems adversarial Round 1 final release audit - 23 September 2026

**Status:** PASS / SUBMISSION READY
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Program authority:** SymC General Operations Manual v0.8.4

## Scientific adjudication closure

Round 1 substantive criticisms were resolved by one of four allowed routes: code/source audit, prospectively frozen post-result sensitivity, claim narrowing, or explicit unresolved limitation.

Closed findings include:
- external H1/H2/H3a use tumor samples only; no tumor/adjacent pooling artifact;
- external H1 source-declared AA/EA axis is not sufficient to explain the effect;
- H1 remains positive in 30/30 composition-complete cancers under a null preserving linear ABSOLUTE-purity and methylation-derived leukocyte structure;
- H1 remains positive in 30/30 after additionally preserving TCGA Tissue Source Site mean structure;
- conventional PCA PC1 fraction shows the same 30/30 direction under the same stronger null;
- higher-resolution B=9,999 external P1 sensitivity preserves H1 and leaves H2/H3a nontransporting;
- H2 is described as no detectable external transport, not a power-limited positive replication;
- `P1_REPRESENTATION_DEPENDENT` is retained only as the preregistered procedural conflict label and is not interpreted as a real nonzero platform-specific effect;
- the TCGA/external RNA representation difference is explicit and remains an unresolved contributor to H2/H3a nontransport;
- TN-A1/TN-P20 remain composition-unadjusted tissue-state contrasts because no symmetric frozen leukocyte route exists;
- TN Hallmark breadth shows the RNA direction is not concentrated in a small immune-module subset;
- P0 is below its 24-cancer promotion floor and its 47-vs-2 predictor comparison is not used to claim Hallmark-specific incremental value;
- reviewer-suggested cancer-regulation citations are engaged; unrelated engineering-control citations are explicitly declined;
- active biological-chi / exceptional-point / recovery framing is removed from the current claim set.

No original P1 result, sample set, endpoint, threshold, null, seed, multiplicity family, or sensitivity role was retuned after outcome inspection.

## Private release candidate

Private main:
- `GRI_BioSystems_working_v12_R1_2026-09-23.tex`
- `GRI_BioSystems_working_v12_R1_2026-09-23.pdf`
- 19 pages

Private supplement:
- `GRI_BioSystems_supplement_working_v10_R1_2026-09-23.tex`
- `GRI_BioSystems_supplement_working_v10_R1_2026-09-23.pdf`
- 14 pages

Private response:
- `BioSystems_Response_to_Reviewers_v4_R1_2026-09-23.md`
- `BioSystems_Response_to_Reviewers_v4_R1_2026-09-23.pdf`
- 6 pages

Private cover letter:
- `BioSystems_Cover_Letter_v4_R1_2026-09-23.md`
- `BioSystems_Cover_Letter_v4_R1_2026-09-23.pdf`
- 2 pages

Private package:
- `BioSystems_Resubmission_R1_v12_Final_20260923.zip`
- SHA-256 `2531ca4e3e1a72e1473c97cb4c7a402f217ed2d2068753e5a8780b1d94ee8226`
- 17 packaged files

## Byte identities

- main v12 TeX: `29c25e0ebf7040e88e67c723392f87fd59a74fcc79116e82a1b5c4a43b69d67e`
- main v12 PDF: `fdf1170705fdf86ab4ae665a855c5c974cedc2971e53fe611c51ff62a20fdf6b`
- supplement v10 TeX: `d6fa4b26a0d378c325b652adc059a1eebe958e2acd2c5bb536f889a522ee6de4`
- supplement v10 PDF: `35edb01a1220ba91459ef5fa91eb175bd9db0e2d5050bfa06f932b4fc6914007`
- reviewer response v4 Markdown: `df55df867aba491acea1eeed397744c48e0ad986913d4f47d1d607e4e72732a3`
- reviewer response v4 PDF: `40b6edb573f04597342adef02c9364fcbaa818b8f0963db1f8421b58943fceaa`
- cover letter v4 Markdown: `d2f112a78b86f0e2f886a695068e8cbb51fa8264713ed119aebaafbd1156cb3b`
- cover letter v4 PDF: `3ab257cbeaa6dd3b33e12e6cb61ffb5fb8f819b9445ed5548726d550c2c11857`

The complete private per-file SHA-256 manifest is retained in:
`SHA256SUMS_BIOSYSTEMS_R1_V12_FINAL_20260923.txt`.

## PDF QA

All final private PDFs were rendered after candidate assembly:
- main: 19/19 pages rendered, openable, non-encrypted, text PDF;
- supplement: 14/14 pages rendered, openable, non-encrypted, text PDF;
- response: 6/6 pages rendered;
- cover letter: 2/2 pages rendered.

The final-clause pass additionally verified the stronger-null equations, 30-cancer TSS longtable, 15.6%/84.4% missingness-scope sentence, and corrected a legacy unescaped `50%` LaTeX source line in Supplement S3.

Montage inspection found no material clipping, overlap, broken figure placement, or page-flow defect requiring correction.

## Public/private boundary

Public in GitHub:
- scientific freezes and amendments;
- source identities;
- configs;
- executable code;
- workflows;
- result artifacts/run identities;
- post-result audits;
- adversarial adjudication;
- reproducibility index;
- release audit.

Private:
- editable manuscript and supplement text;
- reviewer/cover authoring files and assembled submission package.

The private boundary does not conceal any analysis decision, workflow identity, result value, or audit outcome.

## Final disposition

`ROUND1_SCIENTIFIC_GATES = CLOSED`

`ROUND1_REPORTING_GATES = CLOSED`

`ROUND1_VISUAL_QA = PASS`

`ROUND1_PRIVATE_PACKAGE = FROZEN_V12_FINAL_CLAUSES`

Final-clause details and exact TSS support are bound in `BIOSYSTEMS_ADVERSARIAL_R1_FINAL_CLAUSE_AUDIT_20260923.md`.

**FINAL STATUS: SUBMISSION READY AFTER ADVERSARIAL ROUND 1 / V12 FINAL-CLAUSE RELEASE.**
