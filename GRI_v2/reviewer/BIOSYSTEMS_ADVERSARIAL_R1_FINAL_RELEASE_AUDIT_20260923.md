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
- `GRI_BioSystems_working_v11_R1_2026-09-23.tex`
- `GRI_BioSystems_working_v11_R1_2026-09-23.pdf`
- 19 pages

Private supplement:
- `GRI_BioSystems_supplement_working_v9_R1_2026-09-23.tex`
- `GRI_BioSystems_supplement_working_v9_R1_2026-09-23.pdf`
- 13 pages

Private response:
- `BioSystems_Response_to_Reviewers_v3_R1_2026-09-23.md`
- `BioSystems_Response_to_Reviewers_v3_R1_2026-09-23.pdf`
- 9 pages

Private cover letter:
- `BioSystems_Cover_Letter_v3_R1_2026-09-23.md`
- `BioSystems_Cover_Letter_v3_R1_2026-09-23.pdf`
- 2 pages

Private package:
- `BioSystems_Resubmission_R1_Final_20260923.zip`
- SHA-256 `7a27d9942e9566ec4eb563dfd71c0db27b9f9924d928f573b672cb5fb963aeef`
- 17 packaged files

## Byte identities

- main v11 TeX: `2c0335ea7e6087375348d44f154ee60e8fc2edf1465602da45e6cb943cde8ca4`
- main v11 PDF: `1920411994aa18cd60533e042c5d90dad9eac9ad9c219f12b9a423294ca1f91a`
- supplement v9 TeX: `0a4aaf7118d5da78294511a06ffe0e0ec54ed47f6396ae55a6bce8133540238f`
- supplement v9 PDF: `ae59d743d130e371306c00466ce8b94c0e3f84546dcb8d4babf4cb16c248b14a`
- reviewer response Markdown: `06eaac2b614b2fc68f464269e735c368a3095fc000c3970d8642a546f0c4b152`
- reviewer response PDF: `db0511aff466646f70dc9f9fd4e2ea6a6b1b63b3c17936a7cc076f0d6869a083`
- cover letter Markdown: `6920f47e3d4ed07cddce2f5c195768b60dd428a5ed09930dbf7ab664cbabae4e`
- cover letter PDF: `5dadbe49ff4efa95e9b6a4e733d89ceddf7ce391b405fe73b7e162201a7b2cff`

The complete private per-file SHA-256 manifest is retained in:
`SHA256SUMS_BIOSYSTEMS_R1_FINAL_20260923.txt`.

## PDF QA

All final private PDFs were rendered after candidate assembly:
- main: 19/19 pages rendered, openable, non-encrypted, text PDF;
- supplement: 13/13 pages rendered, openable, non-encrypted, text PDF;
- response: 9/9 pages rendered;
- cover letter: 2/2 pages rendered.

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

`ROUND1_PRIVATE_PACKAGE = FROZEN`

**FINAL STATUS: SUBMISSION READY AFTER ADVERSARIAL ROUND 1.**
