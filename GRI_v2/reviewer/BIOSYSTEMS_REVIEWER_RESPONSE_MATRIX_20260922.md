# BioSystems reviewer-response matrix - 22 September 2026

**Manuscript ID:** BIOSYS-D-26-00267  
**Submitted title:** *Collapse of Regulatory Capacity Drives Convergent Phenotypes in Human Cancer*  
**Provisional revised title:** *Regulatory Architecture Across Human Cancers: Multiomic Evidence for Recurrent Methylation–Transcriptomic Organization*  
**Revision branch:** `gri-biosystems-revision-20260922`  
**Canonical science parent:** `gri-conglomerate-v1-integration-20260921` @ `0f471d32940386052da2b8da3b34cd4fc2b064b4`  
**Journal deadline:** 21 November 2026

## Reading rule

This matrix distinguishes reviewer requests that are already satisfied by the rebuilt analysis from requests that remain genuinely open. TCGA discovery, replication, sensitivity, and FINAL HOLDOUT partitions are **internal evidence** even when held out. They are not called external validation.

Status vocabulary:
- **CLOSED**: current frozen work directly addresses the request.
- **CLOSED WITH LIMIT**: addressed, but the manuscript must preserve the stated evidence ceiling.
- **OPEN**: a new evidence-bearing result is still required.
- **DECLINED / NOT CLAIMED**: the reviewer requested a stronger translational claim that the revision will not make.

## Reviewer 1

| Reviewer issue | Revision status | Current disposition |
| --- | --- | --- |
| Verify expression units and preprocessing | **CLOSED** | Source/preprocessing provenance is explicitly audited; historical CV/2 is no longer interpreted as a biological damping coordinate. Final manuscript must state the exact upstream TCGA representation and transformations used. |
| Analyze cancers separately rather than relying on pooled pan-cancer behavior | **CLOSED** | Cancer-specific construction and evaluation are built into the current program; Stage C1 historically closed across 32 cancers. |
| Remove mean-variance dependence / show the signal is not merely CV-vs-mean structure | **CLOSED WITH LIMIT** | The biological-damping interpretation of CV/2 has been withdrawn. Modern mean-variance scrutiny, construction-aware nulls, finite-sample calibration and composition controls now bound the remaining static claims. |
| Replace toy Poisson logic with realistic nulls | **CLOSED** | The current architecture uses construction-aware resampling/permutation/null controls rather than treating a Poisson anchor as mechanistic validation. |
| Include normal controls / establish tumor specificity | **DESIGN + ELIGIBILITY CLOSED; BIOLOGICAL RESULT OPEN** | TN-C0 is frozen and closed without opening molecular values. Primary RNA control has 12 eligible cancers; primary RNA+methylation control has 5; paired RNA sensitivity has 13. TN-A1/TN-C1 molecular execution remains the evidence-bearing step. |
| Control purity / stromal / immune composition | **CLOSED WITH LIMIT** | Purity and methylation-derived leukocyte fraction are explicitly modeled. The revision will state that measured composition is bounded and does not equal complete microenvironment removal. |
| Replace subjective zones with objective change-point/statistical rules | **CLOSED / HISTORICAL CLAIM RETIRED** | The revised paper does not depend on the submitted Warning/Confirmation/Collapse zoning as a biological phase sequence. Unsupported phase-boundary language is retired rather than cosmetically re-thresholded. |
| Validate in an independent dataset | **OPEN** | External breast/prostate/melanoma source identities are qualified, but no outcome has been opened and no decisive P1 cohort has been frozen. TCGA FINAL HOLDOUT remains internal validation only. |
| Remove temporal language unsupported by cross-sectional data | **CLOSED** | Static TCGA results are explicitly firewalled from recovery, damping, inheritance, treatment-response and causal temporal claims. |
| Keep therapeutic implications hypothetical | **CLOSED / CLAIM WITHDRAWN** | No actionable treatment-state rule is claimed. Perturbation/recovery and treatment response require separate prospective evidence. |
| Add direct methylation/chromatin/ATAC evidence | **CLOSED WITH LIMIT** | Methylation is now a measured cross-layer component with frozen source, identity and analysis contracts. Static methylation-RNA organization does not establish causal chromatin control or temporal substrate inheritance. ATAC/ordered perturbational evidence remains a separate lane. |

## Reviewer 2

| Reviewer issue | Revision status | Current disposition |
| --- | --- | --- |
| Independent cohort validation | **OPEN** | Same publication-critical external-confirmation gate as Reviewer 1. Source discovery/identity work is complete enough to choose a prospective task, but decisive P1 selection and outcome opening remain unfrozen. |
| Additional omics validation | **CLOSED WITH LIMIT** | RNA, methylation, genomic and protein/phosphoprotein layers provide multiomic internal qualification. Shared TCGA lineage prevents relabeling these as independent external confirmation. |
| Cancer-specific robustness | **CLOSED** | Cancer-specific analyses, fixed finite-sample calibration and held-out evaluation are part of the rebuilt program. |
| Reproducibility / method detail | **CLOSED IN ARCHITECTURE; RELEASE PACKAGING OPEN** | Frozen configs, tests, hashes, source audits and reviewer maps exist. Submission-specific immutable tag, final figure/table provenance map and final clean-room package remain release tasks. |
| Biological mechanism grounding | **CLOSED WITH LIMIT** | The revision is recast around measured regulatory architecture and explicit representation limits. Association is not presented as causal mechanism where causality was not measured. |
| Demonstrate clinical utility beyond existing predictors | **DECLINED / NOT CLAIMED** | The revision will not promote the method to a clinical diagnostic, prognostic or treatment-response tool. Incremental clinical utility would require a separate preregistered endpoint and external validation. |
| Explain failures / heterogeneity rather than presenting only favorable cancers | **CLOSED** | Null, failed, representation-dependent and non-identifiable branches are retained in the Function/Limit framework and cannot be silently rescued after outcome inspection. |

## Internal validation to retain prominently in the revised paper

The internal validation is an independent evidentiary layer within the same TCGA source program and should be shown rather than buried:

- deterministic DISCOVERY -> REPLICATION -> FINAL_HOLDOUT partitions were established before their target values were opened;
- discovery-fitted methylation transforms/loadings were transported unchanged;
- FINAL_HOLDOUT was opened once under the frozen P3-v2 formulation;
- 18 cancers were primary-evaluable; the frozen all-methylation-plus-covariate model beat the same two-covariate baseline in 17/18 cancers;
- median normalized MSE was 0.444 versus 0.702 and median held-out R2 was 0.507 versus 0.188;
- the result establishes internal transport/generalization within TCGA, not external cohort confirmation;
- PCPG remains the reproducible loss/stress case and is retained rather than excluded.

The revised manuscript should present this layer explicitly alongside, but not conflated with, the new tumor-versus-normal specificity control and the later genuinely independent external confirmation.

## Cross-reviewer revision state

### Convergent internal validation retained in the paper

The revised manuscript will explicitly retain both frozen TCGA systems rather than treating the held-out program as disposable once external confirmation is added:

- **C1 architecture system:** prospectively frozen static methylation/RNA organization, construction-null, patient-shuffle, semantic-label, composition, missingness and technical attacks across 32 cancers.
- **P0 transport system:** separately frozen DISCOVERY/REPLICATION/FINAL_HOLDOUT prediction/transport machinery; discovery-fitted methylation information outperformed the frozen two-covariate baseline in 17/18 FINAL_HOLDOUT cancers while stronger semantic promotion failed.

These systems are nonredundant in task and failure criteria, so their agreement is reported as **convergent internal validation**. Because both inherit TCGA acquisition/processing history, they are not described as independent external cohorts and do not replace P1 external confirmation.

### Already locked without new user science decisions

- Historical `CV/2` demoted to a descriptive/development comparator.
- No universal biological `chi = 1` cancer boundary.
- Static versus temporal/causal firewall.
- Cancer-specific analysis and finite-sample calibration.
- Purity/leukocyte context controls.
- Construction-aware null/sensitivity structure.
- Multiomic RNA/methylation/genomic/protein architecture.
- Internal TCGA held-out result labeled **internal**, not external.
- Clinical/therapeutic claims capped below diagnostic, prognostic or treatment-rule status.
- Provisional revised title approved.
- Exact R and S source byte identities independently stream-verified; workflow run `35733676268` passed both jobs.

### Remaining evidence-bearing revision gates

1. **Tumor-versus-normal control.** Design and TN-C0 eligibility are closed under `BIOSYSTEMS_TUMOR_NORMAL_CONTROL_FREEZE_20260922.md` and `BIOSYSTEMS_TN_C0_ELIGIBILITY_AUDIT_20260922.md`. Frozen sets are 12 RNA-primary cancers, 5 multiomic-primary cancers, and 13 paired-sensitivity cancers. No normal molecular values were opened during eligibility. TN-A1/TN-C1 execution remains open.
2. **Genuinely external confirmation** under a prospectively frozen transported claim, representation, comparator, inclusion/exclusion rule, metric, falsifier and MFR-14 package.

The SCC25 A-H joint-meaning decision packet is scientifically important to the wider GRI program but is not automatically required to answer the BioSystems reviewers. It must not be allowed to expand the paper merely because it is available.

## Manuscript-source integrity issue

Several historical status/reviewer files refer to `GRI_v2/manuscript/LIVING_MANUSCRIPT_DRAFT.md` and a manuscript reconciliation ledger. Those paths are not present on the current canonical branch or the cited historical branch checked on 22 September 2026. They therefore cannot be treated as current repository sources-of-record.

Until a current editable manuscript source is explicitly committed, reviewer work may update the revision ledger, response matrix, source/claim maps and reproducibility records, but must not pretend that manuscript wording has been edited in Git.

## Next safe work

Proceed mechanically on:
- figure/table retirement and regeneration inventory;
- old submitted claim -> revised claim -> evidence -> target section map;
- submission hash/source manifest;
- non-claim ledger synchronization;
- point-by-point response prose that does not depend on the two open evidence results;
- journal disclosure/availability/contribution boilerplate after current policy verification.

Stop before:
- choosing or opening the decisive external P1 outcome;
- inventing a tumor-normal definition or threshold after seeing the result;
- changing a frozen scientific representation merely to satisfy reviewer wording.
