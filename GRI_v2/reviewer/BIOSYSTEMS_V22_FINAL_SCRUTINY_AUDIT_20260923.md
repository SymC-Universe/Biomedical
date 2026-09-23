# BioSystems v22 final-scrutiny audit - 23 September 2026

**Status:** COMPLETE / FINAL READ-THROUGH CANDIDATE  
**Branch:** `biosystems-v22-final-scrutiny-20260923`  
**Scientific parent:** BioSystems v21 post-result extension state  
**Change class:** editorial / cross-document consistency / schematic repair only  
**New scientific computation:** NONE

## Scope

This pass adjudicated the final external scrutiny against the actual v21 main, v16 supplement, response v9, cover v8, frozen evidence contracts, and post-result extension audits.

No endpoint, cohort, statistic, null, threshold, denominator rule, multiplicity family, result, or scientific promotion state was changed.

## Corrections applied

1. **Evidence architecture schematic**
   - Removed the visual implication that tumor-normal control and external prostate P1 descend from P0.
   - P0 is now explicitly a self-contained parallel internal branch.
   - Stage A/B1 and Stage C1 feed the tumor-normal control according to the actual coordinate lineage.
   - External prostate P1 is shown as transport of C1.
   - Post-result breast/perturbation/recovery/clinical extensions are shown separately as non-confirmatory P0-D evidence.

2. **Stronger-H1 denominator transparency**
   - Main text now explicitly names **DLBC and THYM** as the two cancers excluded from the frozen n>=30 cancer-level composition-complete Round-1 H1 gate.
   - The reviewer example "DLBC and OV" was rejected because it conflicts with the frozen denominator.
   - The distinct projected-C1 per-draw all-complete gate remains explicit: COAD, DLBC, KIRC, OV, THYM.

3. **Missingness scope**
   - Main text now states that the direct missingness-projection sensitivity was informative in only 5/32 cancers because 27/32 lacked variation in one or both burden vectors.
   - It explicitly states that the broader missingness bound comes from complete-case and related sensitivities, not a pan-cancer missingness-projection test.

4. **External prostate procedural verdict**
   - Abstract now records that H2/H3a showed no detectable transport while the frozen procedural label `P1_REPRESENTATION_DEPENDENT` was triggered by sign change among null-compatible subset estimates.
   - Main and supplement continue to state that this label is a frozen conflict state, not evidence of a real nonzero platform-specific effect.

5. **H2 headroom cross-reference**
   - Main Methods now points directly to Supplementary Eq. (6), which defines the post-C1 headroom normalization.

6. **H3a/H3b statistic clarification**
   - Supplement now states explicitly that H3a and H3b share the same observed same-Hallmark association statistic and differ in the null attack: patient identity versus Hallmark label identity.

7. **External H1 composition ceiling**
   - Main explicitly states that comparable source-bound composition covariates were unavailable externally and that external H1 is therefore not composition-adjusted.

8. **HCI-005 inferential hierarchy**
   - Main and supplement identify the synchronous treatment-assignment p-value as the primary design-level inferential test.
   - The gene-identity permutation is labeled a secondary gene-correspondence test.

9. **Supplement table semantics**
   - Independent prostate result table now has the explicit caption: "Independent prostate transport results by lane and endpoint."
   - Numbering is produced by LaTeX and currently renders as Table 7.

10. **M397 provenance**
    - Supplement records the current GEO relationship: GSE134459 is listed as a SubSeries of GSE255671 and cites the 2026 Su et al. trajectory publication used here.

11. **Abstract wording**
    - Replaced the stronger phrase "test causal and recovery hypotheses" with "probe selected causal and recovery hypotheses."
    - Final abstract length: **138 words**, below the 150-word ceiling.

## Scrutiny items verified as extraction/layout artifacts or already corrected

No source edit was manufactured for the following because the live TeX was already correct:
- no "2023-2024" title/header text;
- no "AbstractBulk" concatenation;
- no "Multicommunic tumor-normal control" heading;
- no duplicated "RPPA branchThe" heading;
- no duplicated "SCC25 ... testThe source" heading;
- no duplicated "Projection-conditioning ... limitationA" heading;
- no stale "Comparison of the performance of the proposed method..." caption;
- MOFA DOI already correct as `10.15252/msb.20178124`.

## Citation audit

Main manuscript:
- unique cited keys: **23**
- bibliography entries: **23**
- missing cited keys: **0**
- unused bibliography entries: **0**
- Reviewer-1 Li/Pinar/Chen references remain live in text.
- Gevaert/Kim/Ding remain live in text.
- post-result source citations remain live.
- Stability Architecture remains the **last bibliography entry**.

## Final files

Main v22:
- TeX SHA-256: `96d8641522ddc92199cb60d2387888cf7235d043daefd1d28ef4a7e532f5357f`
- PDF SHA-256: `1e053d073e54dfb86e966d54bfea926ff71bf6b2333c00b2fb683c3ee672351a`
- 12 pages
- compact margins retained
- 11 pt retained

Supplement v17:
- TeX SHA-256: `88688a121cd32fd809d2872b5f4efa2a2c350fcf41fcda212cef7ae848220f2a`
- PDF SHA-256: `ee5be69dca9a50f201d2735dbf8fcdd01a88d0673c377425aff88bc22e08cc40`
- 17 pages

Response v10:
- MD SHA-256: `7280d5bc0b832a2f61ebe89d5399cd4c80021d331a84654412802502a94c7ffd`
- PDF SHA-256: `235d0aa3fb5eb44d244d0a03f184332c93f34f5487670c2b9e53d954adf3c2b3`
- 10 pages

Cover v9:
- MD SHA-256: `191c76693cd73aae88c6309f15031035ead1a67b6cb39c4bc235a5471593dca0`
- PDF SHA-256: `0152bc3a63d509e6bdbbe20a55e43c1dd4407fd9cfdda9e9f5deb0dbaf4694a7`
- 3 pages

Package:
- `BioSystems_Resubmission_v22_FinalScrutiny_20260923.zip`
- SHA-256: `3de3ab0c7f12736b7e1c53703422c105b77c4671aa664e8cfd06035b718a370f`
- internal SHA-256 manifest independently returns OK for every shipped file.

## PDF QA

All four PDFs:
- openable;
- searchable;
- non-encrypted;
- not scanned.

Main and supplement were rendered in full. Corrected evidence architecture, main abstract, H1/H2/H3 denominators, external-prostate figure/discussion, extension discussion, prostate supplement table, extension sections, and final bibliography were visually inspected. No clipping, black boxes, broken glyphs, or material table/figure overflow were observed.

## Scientific disposition

**NO SCIENTIFIC CHANGE.**

The final scientific hierarchy remains:
- H1: strongest cross-source result, with prostate P1 and post-result breast corroboration;
- H2/H3a: recurrent TCGA-internal coupling, no detectable external prostate transport;
- H3b: small/support-sensitive;
- tumor-normal: unadjusted state contrasts, not a recovery mechanism;
- direct HCI-005 intervention: one-model intervention-consistent coupling;
- M397: one-model realized transcriptomic recovery;
- SCC25 treatment/direction: unresolved/negative;
- tested prostate diagnostic route: negative;
- prognosis: source-limited and untested.

**STATUS: READY FOR FINAL AUTHOR READ-THROUGH / SUBMISSION SYNCHRONIZATION.**
