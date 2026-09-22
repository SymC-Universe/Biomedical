# GRI MFR-14 external-confirmation readiness matrix

**Date:** 2026-09-16  
**Status:** PRE-CONFIRMATORY READINESS ONLY  
**Outcome opening authorized:** NO  
**P1 cohort selected:** NO

## Purpose

This matrix separates **source qualification** from **confirmatory selection**. A biologically attractive or technically rich dataset is not P1 merely because it exists, is external to TCGA, or has multiple modalities. MFR-14 readiness requires a claim-specific frozen task, a fair same-question comparator where one exists, outcome-independent construction/tuning, refusal behavior, uncertainty, and an untouched decisive test.

No row below freezes a final endpoint, threshold, model, representation, or decisive cohort. This is scaffolding only.

## Readiness states

- `SOURCE_QUALIFIED`: identity/modality/order have been established well enough to keep evaluating logistics.
- `SOURCE_QUALIFIED_WITH_GAP`: valuable source, but a deterministic identity/access/modality gap remains.
- `P0_D_ONLY`: useful for development/Function-Limit mapping, not eligible to be called untouched P1 in the present lineage.
- `P1_CANDIDATE_ONLY`: may be independently eligible later, but no confirmatory task has been frozen and no decisive outcome is opened.
- `NOT_SELECTED_NOT_FROZEN`: explicit protection against accidental promotion.

## Candidate matrix

| Candidate/source | Native evidence opportunity | Source/identity state | Outcome status for GRI | Independence notes | Remaining pre-MFR work | Current ceiling |
| --- | --- | --- | --- | --- | --- | --- |
| **Prostate cross-modality family** `GSE262522` + `GSE262524` + `GSE237995` | external static RNA/methylation architecture; 450K↔EPIC transport; tumor/adjacent context | `SOURCE_IDENTITY_CLOSED_FOR_METADATA_SCOPE`; exact MINiML source identities frozen; production 121/121 RNA↔methylation crosswalk exported; platform partition 68 450K + 53 EPIC | unopened for future P1 purpose | external to TCGA lineage; future endpoint/tuning independence still must be frozen | reconstruct/freeze 450K↔EPIC representation compatibility and shared-probe/preprocessing rule; missingness/support; decide future role before outcome opening | `P1_CANDIDATE_ONLY`, not selected/frozen |
| **Paired breast primary/metastasis family** | paired static/ordered primary↔metastasis cross-modality architecture | `SOURCE_IDENTITY_CLOSED_FOR_METADATA_SCOPE`; exact MINiML source identities frozen; deterministic 72-row RNA↔methylation patient/state crosswalk exported across 36 complete expression pairs; 16 methylation-only samples explicitly retained outside that crosswalk | no decisive GRI outcome authorized | potentially external; outcome/tuning independence still must be frozen | freeze exact paired inclusion, modality/preprocessing compatibility, missingness/support, and future role before outcome opening | `P1_CANDIDATE_ONLY`, not selected/frozen |
| **CARE IDH-mutant longitudinal multiomic family** | genuine longitudinal patient-level progression; 35 patients; 22 matched bulk RNA/ATAC Multiome pair set in current source audit | `SOURCE_QUALIFIED_WITH_GAP`; exact methylation overlap with the 35/22 sets is not fully established in the public source record | unopened | independent source family; future outcome/tuning/Atlas independence unresolved until freeze | exact patient/timepoint crosswalk; exact modality overlap; treatment/order inventory; decide whether role is P0-D representation work or untouched claim test | `P1_CANDIDATE_ONLY`, not selected/frozen |
| **IDH glioma dual-capture 2026** `GSE292025` + `GSE291885` | within-patient longitudinal progression with joint single-nucleus XRBS methylation + Smart-seq2 RNA; 32 matched tumors/15 patients; 2,117 matched nuclei | `SOURCE_QUALIFIED_WITH_GAP`; 36 tumor joint-capture branch strong; 10x paper-vs-GEO 32-vs-31 record discrepancy remains | `UNOPENED` | candidate data/cohort independence from TCGA; adapter development on this source would consume some confirmation independence | exact 36-tumor order table; 2,117-nucleus pairing schema; treatment/exposure inventory; resolve/preserve 10x discrepancy; define representation-invariant adapter before GRI computation | presently best treated `P0_D_ONLY` until adapter independence problem is solved |
| **Melanoma acquired-MAPKi family** `GSE65186` | human baseline→acquired-resistance ordering with methylation + transcriptome | `SOURCE_MANIFEST_COMPLETE_WITH_ANOMALIES`; exact MINiML identities frozen; 218 source rows inventoried (192 human, 26 cell-model); three RNA-seq Pt22-DDP title records conflict with source descriptions naming Patient 21 and are quarantined | no GRI outcome opened in source audit | external biological system; future test independence depends on not using outcome to choose state construction; title/description conflicts cannot be silently resolved | prospectively resolve or exclude the three source-identity conflicts; freeze shared-state inclusion, treatment/order handling, cell-model separation, representation compatibility and claim before outcome opening | `P1_CANDIDATE_ONLY`, not selected/frozen |
| **CGGA CCell_4083** | external multi-layer static architecture across proteomics/phosphoproteomics/methylation/bulk RNA/scRNA | `SOURCE_QUALIFIED_WITH_GAP`; modality counts differ: 35 proteomics, 35 phosphoproteomics, 29 methylation, 19 bulk RNA, scRNA 18 by title/19 by description; all-five-on-35 is false | not opened as GRI confirmation | external family, but exact pairwise intersection and controlled-access manifests unresolved | obtain exact cohort crosswalk; resolve scRNA count discrepancy; identify pairwise/all-modality intersections; access/hashes; freeze role before any outcome | `P0_D_ONLY` at present |
| **Chronic SCC25 cetuximab** `GSE98812/GSE98813/GSE98815` | 11-week paired treated/control temporal multiomic architecture | source-qualified and already used in G2 | opened/used in current G2 development/qualification | **not untouched** for later confirmation in this lineage | continue only as P0-D/P0-Q, restoration-identifiability input, or explicit internal challenge | `P0_D/P0_Q_ONLY` |
| **Short-term SCC25/SCC1 cetuximab** `GSE114446` | daily days 0-5 perturbation; same nominal perturbation at finer resolution; SCC25 + SCC1 complete | source-qualified; SCC6 ordered trajectory remains metadata-ambiguous | SCC25 used in short-term G2; SCC1 remains a related source but same program/lab family | not an independent-lab P1 replication of SCC25; same-lab and same-study-family dependencies must remain explicit | SCC6 metadata resolution if used; claim-specific transport rule for SCC1; no post-result operator/state retuning | primarily `P0_D/P0_Q`; not designated P1 |
| **HNSCC day-5 ATAC** `GSE135604` | independent substrate/context endpoint for RNA-state relation; SCC25 has 3 CTX + 3 PBS; SCC1 has one processed-QC exception | source-qualified | no Chi_bio result opened | same HNSCC experimental program, so useful orthogonal modality but not independent-lab confirmation | freeze QC eligibility, region/feature aggregation, cross-modal statistic, and state/operator before relation is opened | `P0_D/P0_Q_ONLY` for current lineage |

## Candidate selection firewall

No dataset in this table may become the decisive P1 merely because it appears strongest after this inventory. Before any P1 selection, create a claim-specific freeze containing at least:

1. the exact claim being tested and the null/refusal outcome;
2. the frozen representation/state construction, including what happens when no coherent scalar exists;
3. the dataset identity and exact inclusion/exclusion manifest;
4. the untouched outcome field or readout and proof it has not been used for construction/tuning;
5. the native same-question comparator or a documented good-faith `NO_NATIVE_COMPARATOR` result;
6. performance/uncertainty metrics and pass/fail criteria frozen before outcome opening;
7. missingness, sample-size, dependence/hierarchical handling, and platform transport rules;
8. all tuning and hyperparameter rules, including a firewall against outcome-based rescue;
9. Function-Map and Limit-Map reporting requirements;
10. code/config/environment identity plus refusal/error behavior;
11. evidence-independence classification and known shared lineage with development evidence;
12. an explicit rule that a failed P1 stays failed rather than becoming a new post hoc discovery cohort;
13. manuscript claim ceiling for pass, fail, indeterminate, and non-identifiable outcomes;
14. a cold-audit package sufficient to reconstruct what was frozen before the decisive result.

## Current strategic implication

There is no shortage of plausible external systems. The bottleneck is **claim and representation maturity**, not source discovery. The current program should therefore continue identity/access qualification in parallel while refusing to name a decisive P1 until the state/claim to be transported is scientifically frozen.

That protects the external cohorts from being slowly consumed as development evidence before a real confirmatory test exists.


## 22 September source-identity update

Workflow run `35733020358` completed source-only GEO MINiML freezing and mechanical identity derivation without computing GRI features or selecting a P1 cohort.

Canonical post-result record:
`GRI_EXTERNAL_GEO_IDENTITY_POSTRESULT_AUDIT_20260922.md`.

This closes a major logistics layer for prostate and breast and exposes a real source-level identity anomaly in the melanoma family. It does **not** alter the candidate-selection firewall or make any dataset P1.

The remaining bottleneck is now even more clearly scientific: freeze a transportable representation and claim before using these sources as outcome-bearing evidence.
