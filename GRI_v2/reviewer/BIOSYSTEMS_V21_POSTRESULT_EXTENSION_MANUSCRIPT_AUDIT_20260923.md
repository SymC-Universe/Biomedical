# BioSystems v21 post-result extension manuscript audit - 23 September 2026

**Status:** COMPLETE / PRIVATE READ-THROUGH CANDIDATE
**Core scientific spine:** unchanged C1 / TN / prostate P1
**Post-result extension branch:** `biosystems-claim-extension-p0d-20260923`
**Manuscript privacy:** main/supplement remain private authoring artifacts; GitHub records only scientific/provenance/audit state.

## Purpose

Revise the BioSystems manuscript after a bounded, low-cost P0-D extension tested selected prior nonclaims without reopening the heavy TCGA C1 computation.

The universal dynamical-boundary question was deliberately not tested or inserted into the oncology claim set.

## Post-result extension outcomes

### E1 - second external H1 cohort
GSE58999 breast 450K:
- deterministic n=30 primary lane: delta S = +0.150191, p = 0.001;
- masked primary lane: +0.150581, p = 0.001;
- matched metastasis n=30: +0.189381, p = 0.001;
- full n=44 primary: +0.165543, p = 0.005 (B=199 floor);
- full n=44 metastasis: +0.202633, p = 0.005.

Disposition: `PASS_SECOND_EXTERNAL_H1_P0D`.
This is post-result corroboration, not retroactive P1 confirmation.

### E2/E3 - SCC25 cetuximab response/direction
- methylation phase test: p=0.05325, BH q=0.10649;
- RNA phase test: p=0.42489, BH q=0.42489;
- week-ahead methylation-to-RNA versus reverse mean difference = -0.0009029;
- exact one-sided direction-swap p=0.53906.

Disposition:
- treatment-response architecture: unresolved;
- methylation-leading temporal direction: not supported.

### Direct methylation intervention - HCI-005 breast PDX
- C1-carrier methylation delta = -0.002252595;
- exact treatment-assignment p=0.0285714;
- matched promoter/RNA genes = 3,317;
- methylation-delta versus RNA-delta Spearman rho = -0.1073377;
- gene-identity permutation p=0.0001;
- exact synchronous treatment-assignment p=0.0285714.

Disposition: `P0_D_INTERVENTION_CONSISTENT_COUPLING_SUPPORTED`.
Claim ceiling: one directly perturbed model; no per-gene or pan-cancer causal law.

### Recovery - M397 melanoma drug withdrawal
- retained genes: 22,843/22,843;
- post-removal Spearman rho = -0.8857143;
- exact one-sided permutation p=0.0166667;
- Day35 displacement < Day4 and < late drug-on Day59;
- descriptive recovery fraction = 0.6823.

Disposition: `RECOVERY_DYNAMIC_SUPPORTED` at P0-D.
Claim ceiling: realized transcriptomic recovery toward baseline in this model under the frozen distance; not an explanation of the TCGA tumor-normal contrast.

### Clinical-utility extensions
External prostate diagnostic LOPO:
- PC1 concordant pairs = 9/32;
- one-sided binomial p = 0.99650;
- descriptive AUC = 0.25293;
- simple global-mean comparator = 19/32.

Disposition: architecture-derived diagnostic route not supported.

Prognostic lane:
- not run because no source-verified PFS time/event crosswalk to the frozen molecular participant IDs could be qualified.

Disposition: prognostic utility remains unestablished due current source-mapping insufficiency.

## Manuscript changes

Main v21:
- 12 pages;
- compact margins retained;
- 11 pt retained;
- abstract <=150 words (audit count 140 words; conservative source-generation count 144);
- second external breast H1 added as explicitly post-result corroboration;
- direct HCI-005 intervention result added;
- M397 recovery result added;
- SCC25 negative treatment/direction result retained;
- prostate diagnostic negative result retained;
- prognostic source limitation retained;
- universal dynamical-boundary sentence removed rather than tested by assertion;
- Stability Architecture cited only as program lineage/context, with no physical damping/EP inference imported into cancer.

Supplement v16:
- 17 pages;
- new detailed section for all low-cost extension lanes;
- extension outcomes added to failure/reproducibility/current-status records.

## Citation audit

Main bibliography:
- cited unique keys: 23;
- bibliography entries: 23;
- missing cited keys: 0;
- unused bibliography entries: 0.

Reviewer-requested citations remain live:
- Li 2024;
- Malaymar Pinar 2025;
- Chen 2024.

Previously stranded citations remain live:
- Gevaert 2015;
- Kim 2020;
- Ding 2021.

New source citations:
- Reyngold et al. 2014;
- Stein-O'Brien et al. 2018;
- Achinger-Kawecka et al. 2024;
- Su et al. 2026;
- Christensen 2026 Stability Architecture.

**Stability Architecture is the final bibliography entry as requested.**

Verified published Stability Architecture record:
Christensen N. Exceptional-point stability boundaries from quantum dissipation to cosmological acceleration. Scientific Reports. 2026;16(1). doi:10.1038/s41598-026-56887-7.

## Prostate provenance clarification

The independent prostate P1 data are GEO sources GSE237995, GSE262522 and GSE262524. They are not TCGA/PanCan patient data.

The external analysis deliberately reused the frozen 22,601 PanCan C1 probe identity carrier and analysis rules. Thus:
- cohort/data independence from PanCan: YES;
- representation/rule inheritance from PanCan: YES.

## Breast source-verification timing correction

A metadata-only GSE58999 identity-verification workflow added after the UI timeout executed after the breast H1 outcome was already recorded. It is therefore labeled post-result source verification, not pre-value source freezing.

This does not change the breast result's epistemic class. The sample-selection/statistical rules were frozen earlier in the claim-extension protocol and runner before the successful outcome-bearing run, and a separate source/identity audit predated the extension.

## PDF QA

Main and supplement compiled successfully and were rerun until cross-reference warnings cleared.

Main:
- 12 pages;
- searchable/openable/non-encrypted/not scanned;
- rendered all pages at 150 dpi;
- title/abstract, changed discussion/conclusion, and bibliography visually inspected.

Supplement:
- 17 pages;
- searchable/openable/non-encrypted/not scanned;
- rendered all pages at 150 dpi;
- new claim-extension section visually inspected.

No clipping, black boxes, broken glyphs, or material figure/table overflow observed.

## Private file hashes

Main v21 TeX:
`8f968ca2daca053a0cf9feccb399fb1f8c314d33f7916c3875accd78cd723e36`

Main v21 PDF:
`592904c352dbf2dc831abaa91387c3d444058b03a9931886cd39cc432f416e83`

Supplement v16 TeX:
`0343258845af6d0bd2b9819972762902e7ec0e0c52da9a915ddfc8d816d7301c`

Supplement v16 PDF:
`80326bb3a514d7db76c5521b4d0083a3d850eb0dd2e15728ffbda35ee1da78cd`

**STATUS: READY FOR USER READ-THROUGH.**
