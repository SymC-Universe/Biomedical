# BioSystems resubmission reviewer index - 23 September 2026

**Manuscript:** BIOSYS-D-26-00267  
**Revised title:** *Regulatory Architecture Across Human Cancers: Multiomic Evidence for Recurrent Methylation–Transcriptomic Organization*  
**Revision branch:** `gri-biosystems-revision-20260922`  
**Program authority:** SymC General Operations Manual v0.8.4  
**Status:** FINAL REVIEWER INDEX / SUBMISSION-READY RELEASE

## Reading rule

This index links each reviewer-facing claim family to its prospective definition/freeze, implementation/result, post-result audit, and final manuscript disposition. The private manuscript and submission files are intentionally not committed to the public Biomedical repository.

## 1. Static TCGA architecture

**Claim:** recurrent within-methylation organization and internally recurrent methylation-RNA architecture across TCGA cancers, with H3b smaller/support-sensitive.

Public provenance:
- C1 source/annotation and frozen execution lineage under `GRI_v2/docs/`, `GRI_v2/config/`, `GRI_v2/src/`, and `GRI_v2/tests/`;
- `GRI_v2/docs/GRI_POST_C1_SENSITIVITY_V22_RESULT_AUDIT_20260912.md`;
- `GRI_v2/docs/GRI_POST_C1_V22_FOUNDATIONAL_ROBUSTNESS_AUDIT_20260913.md`.

Manuscript disposition:
- static architecture only;
- cancer is the inferential unit;
- no biological damping ratio, causal direction, recovery, or universal boundary.

## 2. Internal held-out TCGA transport

**Claim:** discovery-fitted methylation information transports internally within TCGA better than the frozen covariate-only baseline in 17/18 FINAL_HOLDOUT cancers.

Public reviewer map:
- `GRI_v2/reviewer/BIOSYSTEMS_REVIEWER_RESPONSE_MATRIX_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_SUBMITTED_TO_REVISED_CLAIM_MAP_20260922.md`.

Manuscript disposition:
- explicit internal validation;
- not called independent external validation;
- PCPG remains the named held-out loss.

## 3. Tumor-versus-adjacent-normal control

Prospective/final records:
- `GRI_v2/reviewer/BIOSYSTEMS_TUMOR_NORMAL_CONTROL_FREEZE_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_TN_A1_TN_C1_EXECUTION_CONTRACT_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_TUMOR_NORMAL_PROTOCOL_LINEAGE_AUDIT_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_TUMOR_NORMAL_BIOLOGICAL_CLOSEOUT_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_TN_C1_BIOLOGICAL_RESULT_AUDIT_20260922.md`.

Result:
- TN-A1: all three RNA architecture quantities lower in tumor in 12/12 cancers, BH q=0.000488 each;
- TN-P20: same-participant sensitivity preserves direction in 13/13, 13/13, and 12/13 cancers, q<=0.00342;
- TN-C1 H1: lower in tumor in 5/5 cancers; H2/H3a heterogeneous; H3b small unresolved upward tendency.

Manuscript disposition:
- tumor-associated weakening/reorganization of pre-existing architecture;
- adjacent/non-tumor reference, not universal healthy baseline;
- no static-to-recovery promotion.

## 4. Independent external prostate P1

Prospective records:
- `GRI_v2/reviewer/BIOSYSTEMS_EXTERNAL_PROSTATE_P1_FREEZE_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_EXTERNAL_PROSTATE_P1_EXECUTION_CLARIFICATION_20260922.md`;
- `GRI_v2/config/biosystems_external_prostate_p1_v1_0.json`.

Outcome-bearing execution:
- workflow run `35801966289`;
- head `e410257c95fddc50b39bc147b4780d214f731d0e`;
- artifact `GRI_BIOSYSTEMS_EXTERNAL_PROSTATE_P1_V01`;
- artifact ID `10726636434`;
- artifact SHA-256 `1d7bbef7a4f8ea0cb254c139879e8ec53b9498f8d95c9c97fa28f21367075cde`.

Post-result audit:
- `GRI_v2/reviewer/BIOSYSTEMS_EXTERNAL_PROSTATE_P1_POSTRESULT_AUDIT_20260922.md`.

Result:
- primary 450K n=30: H1 +0.303090, q=0.003; H2 +0.019724, q=0.4065; H3a -0.040489, q=0.813;
- full n=32 450K sensitivity concordant;
- EPIC n=26: H1 +0.358394, q=0.003; H2/H3a unresolved with sign reversal;
- final frozen class: `P1_REPRESENTATION_DEPENDENT`;
- secondary external tumor-normal RNA comparison not confirmed.

Manuscript disposition:
- independent cross-platform external support claimed for H1 only;
- H2/H3a external universality explicitly not established;
- no post-result rescue.

## 5. Biological chi / recovery firewall

Records:
- `GRI_v2/docs/GRI_CHI_BIO_ADMISSION_CYCLE_CLOSURE_20260913.md`;
- `GRI_v2/docs/GRI_CHI_BIO_FINAL_COMPLETION_AUDIT_20260913.md`;
- `GRI_v2/docs/GRI_CHI_BIO_DISTANCE_TO_ADMISSION_20260922.md`.

Disposition:
- historical scalar `Chi_bio`: NOT_ADMITTED;
- current manuscript does not claim failed recovery;
- recovery-first oncology stability is a separate future lineage and did not delay this revision.

## 6. Reviewer-response and submission closure

Public reviewer records:
- `GRI_v2/reviewer/BIOSYSTEMS_REVIEWER_RESPONSE_MATRIX_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_RESUBMISSION_CLOSEOUT_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_REVISED_NONCLAIM_LEDGER_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_FIGURE_TABLE_REGEN_INVENTORY_20260922.md`;
- `GRI_v2/reviewer/BIOSYSTEMS_SUBMISSION_PROVENANCE_MANIFEST_20260922.md`.

Private final submission package:
- main source: `GRI_BioSystems_working_v10_2026-09-23.tex`;
- main PDF: `GRI_BioSystems_working_v10_2026-09-23.pdf`;
- supplement source/PDF: `GRI_BioSystems_supplement_working_v8_2026-09-23.*`;
- reviewer response: `BioSystems_Response_to_Reviewers_v2_2026-09-23.*`;
- cover letter: `BioSystems_Cover_Letter_v2_2026-09-23.*`;
- five deterministic release figures plus source-value table/generator;
- bundle: `BioSystems_Resubmission_Package_20260923.zip`.

Private bundle SHA-256:
`125a5432355835cd5fdc4f835cb3ad3cc3665c27e4ae30f7f3f332cae620e431`.

Key final byte identities:
- main v10 TeX: `494d74e6622bf5b4f827086cb8aec9159ad6d6c186b16aa126462e10fe5fc5e2`;
- main v10 PDF: `1809245173dabb6744472541f40b36c8b7aff03dfb0f1d84c4d363919e41ac99`;
- supplement v8 PDF: `636b8cc720e3240d4bbb8a697507b2b36adf66775fe27b012f45208c96e41974`;
- response Markdown: `04110891cc9c0287a9e752e1966c0224ccf66b204a2cc67584772b20c622b911`;
- cover-letter Markdown: `77972f9473318cb1339dd33e7906a67f2ee9ee6be98feac01b6bf02c1ec42236`.

## 7. Final claim ceiling

The release supports:
- recurrent static molecular organization within TCGA;
- internal TCGA held-out transport;
- tumor-associated weakening/reorganization under adjacent-normal controls;
- strong independent cross-platform external support for methylation H1;
- explicit platform/context limits for H2/H3a.

The release does not claim:
- biological chi;
- a universal chi=1 cancer boundary;
- temporal collapse or failed recovery;
- causal methylation-to-RNA direction;
- diagnostic/prognostic/treatment-response utility;
- a universal cross-layer architecture across external cohorts.

**Final reviewer-index status: COMPLETE.**
