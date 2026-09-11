# GRI external Atlas / validation dataset candidate inventory

**Date:** 2026-09-10  
**Last source-discovery update:** 2026-09-11  
**Status:** P0-D SOURCE DISCOVERY ONLY  
**Not a cohort selection or P1 freeze.**  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Purpose

Identify external data families that may eventually populate the Regulatory Substrate Atlas, support Function/Limit mapping, or serve as untouched/independent validation candidates.

Discovery does not mean selection. No candidate is chosen because it is expected to agree with GRI. Final P1 cohort selection, comparator, inclusion rules, and decision rule require a separate frozen MFR-14 process before decisive outcomes are opened.

## Candidate A: external lung adenocarcinoma methylation + expression cohort

### Source of record

- NCBI GEO methylation series: `GSE66836`
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE66836
- NCBI GEO expression series: `GSE66863`
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE66863
- NCBI BioProject: `PRJNA278125`
  - https://www.ncbi.nlm.nih.gov/bioproject/278125

### Verified source facts

The methylation GEO record describes:

- 164 lung adenocarcinoma tumors;
- 19 matched normal lung samples;
- Illumina Infinium HumanMethylation450 methylation.

The expression companion `GSE66863` contains 121 lung adenocarcinoma tumor samples measured on the Agilent 60K mRNA expression array. GEO explicitly states that the expression sample numbers are matched between `GSE66836` and `GSE66863`.

Therefore the source-declared paired cross-omic tumor subset is **121**, not all 164 methylation tumors. The additional methylation tumors and 19 matched normal lung samples remain useful methylation/reference context but are not assumed to possess matched expression.

### Potential role

- `NOMINAL_FUNCTION`: high-priority external single-cancer static cross-omic architecture cohort;
- `PERTURBED_FUNCTION`: possible smoking/mutation-defined context comparisons, subject to independent prespecification;
- external expression-platform transfer because expression is microarray-based rather than TCGA RNA-seq;
- normal-tissue methylation context from the 19 matched-normal samples, without assuming paired expression for those normals.

### Current state

`CANDIDATE_HIGH_PRIORITY_STATIC_EXTERNAL`

`PAIRED_CROSS_OMIC_TUMORS_SOURCE_DECLARED = 121`

---

## Candidate B: CGGA CCell_4083 multi-omics glioma cohort

### Source of record

- CGGA download portal: https://www.cgga.org.cn/download.jsp

### Verified source facts

The portal lists `CCell_4083` as a 35-sample multi-omics dataset with Methylation_EPIC, RNA-seq, 10X scRNA-seq, phosphoproteomics, proteomics, and associated clinical data.

The portal-level listing establishes the dataset family and total sample count. It does **not by itself prove that all 35 samples are present in every listed modality**. Exact modality overlap still requires manifest-level verification.

### Potential role

- `NOMINAL_FUNCTION`: independent glioma multi-omic architecture;
- cross-modality Atlas test;
- external platform transfer.

### Current state

`CANDIDATE_HIGH_PRIORITY_MULTIOMIC_EXTERNAL`

`EXACT_MODALITY_OVERLAP = TO_BE_VERIFIED`

---

## Candidate C: CGGA legacy glioma methylation / expression resources

### Source of record

- https://www.cgga.org.cn/
- https://www.cgga.org.cn/download.jsp

### Verified source facts

The portal separately lists:

- `methyl_159`: 159 samples, Illumina HumanMethylation27;
- `mRNA-array_301`: 301 samples, Agilent whole-human-genome array;
- RNA-seq cohorts of 325 and 693 samples;
- primary/recurrent LGG and GBM categories.

### Critical gap

The public portal summary does not establish the exact patient overlap between methylation and a specific expression cohort.

### Current state

`CANDIDATE_MEDIUM_PRIORITY_PENDING_OVERLAP_AUDIT`

---

## Candidate D: colorectal primary-to-liver-metastasis paired multi-omic series

### Source of record

- GEO `GSE213402`
- https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE213402

### Verified source facts

- 20 samples;
- paired primary cancer and liver metastases from 10 colorectal cancer patients;
- RRBS methylation;
- RNA-seq expression.

### Potential role

- `PERTURBED_FUNCTION` P0-D state-change mapping;
- candidate architecture reorganization from primary to metastatic state.

Too small to import the current n=30 C1 design unchanged.

### Current state

`P0_D_PERTURBED_FUNCTION_CANDIDATE_SMALL_N`

---

## Candidate E: acquired ALK-inhibitor resistance cell-model series

### Sources of record

- `GSE139388`
- `GSE139387`
- `GSE179326`

### Verified source facts

The GEO family describes an H3122 ALK-positive lung-cancer model with parental versus acquired ceritinib-resistant states and methylation/RNA-related measurements.

### Potential role

- controlled `PERTURBED_FUNCTION` P0-D mechanism/response mapping;
- Engine qualification of restructuring versus ordinary shared structure.

### Current state

`P0_D_MECHANISM_TESTBED_NOT_EXTERNAL_POPULATION_VALIDATION`

---

## Candidate F: prostate tumor / adjacent-tissue multi-omic study family

### Sources of record

- RNA-seq `GSE237995`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE237995
- HumanMethylation450 `GSE262522`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262522
- MethylationEPIC `GSE262524`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262524
- published study: Ramakrishnan et al., Genome Medicine (2024), PMID 38566104 / PMCID PMC10988846

### Verified source facts

The three GEO series belong to the same published multi-omics prostate study and carry the same 58 African American + 63 European American tumor/adjacent-tissue study design.

Source counts:

- `GSE237995`: **121 RNA-seq samples**;
- `GSE262522`: **68 HumanMethylation450 samples**;
- `GSE262524`: **53 MethylationEPIC samples**.

The two methylation series therefore contain **121 methylation arrays in total (68 + 53)**. The published methods explicitly state that the 450K and EPIC arrays were normalized and then merged with `combineArrays`, retaining the **449,636 probes shared between the platforms** for subsequent analysis.

Individual identifiers are demonstrably shared across methylation and RNA series. Examples visible in source records include participant-style IDs such as `PT-00162955` on the 450K/RNA side and `PT-00193829` on the EPIC/RNA side.

### What is now stronger than the previous inventory

The prior inventory treated the study as only 68 methylation samples against 121 RNA samples. That was incomplete because it omitted the 53-sample EPIC arm.

The correct source-level picture is now:

`121 RNA-seq + 121 methylation arrays split across 450K/EPIC`

with a published common-probe harmonization route.

### Remaining identity gate

The matching counts and shared study design strongly support near/full cross-omic coverage, but **exact title-level one-to-one methylation↔RNA sample bijection has not yet been mechanically enumerated from all 121 identifiers** in this source-discovery record.

Therefore:

`METHYLATION_TOTAL = 121_SOURCE_VERIFIED`

`RNA_TOTAL = 121_SOURCE_VERIFIED`

`EXACT_CROSS_MODALITY_BIJECTION = TO_BE_ENUMERATED`

No unmatched sample is silently assumed paired.

### Potential role

- high-priority external `NOMINAL_FUNCTION` cross-omic prostate architecture;
- tumor-versus-adjacent `PERTURBED_FUNCTION`/context mapping;
- population/context robustness across the study's AA/EA design;
- explicit **methylation-platform transport** test because the study contains both 450K and EPIC arrays;
- possible future Atlas reference family after independent D1 reconstruction and frozen harmonization rules.

### Important platform implication

This source is especially useful under v0.7.1A because GRI's current TCGA methylation lineage itself carries HM27/HM450 platform-history limitations. A study that independently spans 450K and EPIC, with a published shared-probe harmonization route, can help map **where platform changes preserve versus reorganize the representation**. That is P0-D/qualification value, not yet confirmation.

### Current state

`CANDIDATE_VERY_HIGH_PRIORITY_STATIC_EXTERNAL_AND_PLATFORM_TEST`

---

## Candidate G: ICGC ARGO program family

### Sources of record

- https://platform.icgc-argo.org/
- https://dcc.icgc.org/

### Potential role

- materially external cohort/system validation;
- multi-cancer transfer/generalization where required modalities exist;
- possible longitudinal clinical context depending on program.

### Current gap

No selected ARGO program has yet been source-verified as containing the exact paired methylation + expression modalities required for the current GRI task.

### Current state

`SOURCE_FAMILY_LEAD_ACCESS_AND_MODALITY_AUDIT_REQUIRED`

---

## Candidate H: paired primary breast tumor -> regional metastasis methylation + expression

### Sources of record

- DNA methylation: `GSE58999`
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE58999
- expression: `GSE57968`
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE57968
- SuperSeries: `GSE59000`
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE59000
- expression BioProject: `PRJNA248618`

### Verified source facts

The source describes a matched primary-breast-tumor/regional-metastasis study from MSKCC:

- DNA methylome profiled for **44 matched primary tumors and metastases** using HumanMethylation450;
- transcriptome profiled for **36 matched primary tumors and metastases** using Affymetrix U133A 2.0;
- the SuperSeries combines the methylation and expression subseries;
- samples were pathologist-reviewed and microdissected to >70% tumor content according to the GEO description;
- individual GEO sample records expose both a `unique patient id` and a `sample type` such as primary tumor or lymph-node metastasis, enabling an exact future identity reconstruction.

The wording indicates paired primary/metastasis architecture for both omics, but exact cross-modality patient intersection still should be enumerated before a future paired multi-omic analysis.

### Potential role

This is a particularly useful v0.7.1A source because it provides a **natural paired state change** rather than only static between-patient variation.

Potential roles:

- `PERTURBED_FUNCTION`: primary -> regional-metastatic reorganization;
- candidate `BOUNDARY_OR_TRANSITION` P0-D architecture study, without claiming a dynamical transition from two sampled states alone;
- test of whether scalar/modal/conglomerate relationships are preserved, redistributed, or reorganized across a clinically meaningful state change;
- possible future external confirmation after an independent prediction is frozen.

### Current state

`CANDIDATE_HIGH_PRIORITY_PAIRED_PERTURBED_FUNCTION`

`METHYLATION_PAIRED_CASES_SOURCE_DECLARED = 44`

`EXPRESSION_PAIRED_CASES_SOURCE_DECLARED = 36`

`EXACT_CROSS_MODALITY_PATIENT_INTERSECTION = TO_BE_ENUMERATED`

---

## Candidate I: melanoma baseline -> acquired MAPKi resistance multi-omic SuperSeries

### Sources of record

- SuperSeries `GSE65186`
  - https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE65186
- methylation `GSE65183`
- expression array `GSE65184`
- RNA-seq `GSE65185`
- BioProject `PRJNA273358`

### Verified source facts

GEO describes `GSE65186` as `Non-genomic and Immune Evolution in Melanoma with Acquired MAPKi Resistance` and combines:

- HumanMethylation450 methylation;
- Affymetrix Human Gene 2.1 ST expression;
- Illumina HiSeq 2000 RNA-seq.

The source explicitly describes the RNA-seq branch as a comparative analysis of **temporal transcriptomes from patient-matched tumor biopsies**. Sample records encode states such as baseline/pre-MAPKi and post-BRAFi or BRAFi+MEKi resistance. Examples include `Pt7-BASELINE` and resistant `Pt7-DP1`, as well as multiple sequential resistant biopsies such as `Pt10-DP5` through `Pt10-DP9`.

This establishes genuinely ordered treatment-state information in the source family. It does not establish that every timepoint has every omic modality.

### Potential role

- `PERTURBED_FUNCTION`: response/reorganization from pretreatment to acquired resistance;
- possible `BOUNDARY_OR_TRANSITION` mapping of representation changes under therapy-driven state change;
- P0-D test of whether global geometry, modal concentration, and module organization are preserved or reorganized;
- candidate future S2/S4-style prediction family source only after a separate prospective rule/freeze.

### Critical caution

Repeated biopsies, replicates, treatment differences, and patient-specific timelines mean `sample != patient != timepoint`. No simple row-level independence assumption is allowed. A future analysis must reconstruct patient/timepoint/treatment metadata first.

### Current state

`CANDIDATE_HIGH_PRIORITY_ORDERED_PERTURBED_FUNCTION`

`EXACT_CROSS_MODALITY_TIMEPOINT_INTERSECTION = TO_BE_RECONSTRUCTED`

---

# Initial priority by research purpose

This ranking is by **data architecture and research role**, not by agreement with GRI results.

### Static external cross-layer validation candidates

1. `GSE262522 + GSE262524 + GSE237995` prostate study: 121 methylation arrays across 450K/EPIC plus 121 RNA-seq samples, with published 449,636-shared-probe harmonization; exact cross-omic title bijection still to enumerate.
2. `GSE66836 + GSE66863` lung adenocarcinoma: 121 source-declared matched tumor expression/methylation sample numbers.
3. `CGGA CCell_4083`: 35-sample multi-omics dataset with EPIC methylation, RNA-seq, proteomics/phosphoproteomics, and scRNA-seq listed; exact per-modality overlap pending.
4. CGGA legacy methylation/expression families: larger individual cohorts, exact pairing unresolved.

The prostate source moves ahead of the lung cohort for **source-architecture richness**, not because any GRI result has been inspected on it. Lung remains cleaner for an immediately obvious source-declared 121-patient static pair.

### Function/perturbation mapping candidates

1. `GSE58999 + GSE57968 / GSE59000`: 44 matched primary/metastatic methylation pairs and 36 matched primary/metastatic expression pairs, high-value natural paired-state architecture.
2. `GSE65186`: baseline -> acquired MAPKi-resistance melanoma with methylation + expression array + RNA-seq and repeated patient-linked states.
3. `GSE262522 + GSE262524 + GSE237995`: tumor-versus-adjacent prostate context plus explicit 450K/EPIC platform variation.
4. `GSE213402`: paired primary/metastatic colorectal RRBS + RNA-seq, scientifically clean pairing but only 10 patients.
5. `GSE139388` family: acquired drug-resistance cell-model perturbation, useful mechanism testbed but not population validation.
6. CGGA primary/recurrent categories: potentially useful after exact pairing/temporal relationship verification.

### Rare-natural-limit candidates

Among the **external source candidates in this file**, none is admitted as a P1 rare-natural testbed merely because it is unusual or expected to stress GRI.

Separately, the existing TCGA PCPG stress case is source-qualified as a **post-result P0-D rare-natural testbed** in `artifacts/GRI_PCPG_RARE_NATURAL_TESTBED_P0D_20260910.md`. It carries no confirmatory weight and is not an external validation cohort.

# Next source-discovery actions

Safe P0-D actions:

1. enumerate the exact 121-title methylation/RNA identifier relation across `GSE262522`, `GSE262524`, and `GSE237995` without evaluating any GRI outcome;
2. retain the source-declared 121 matched lung tumor subset as a high-priority static external candidate without evaluating GRI outcomes;
3. reconstruct exact patient/timepoint/modality overlap for `GSE59000` breast primary/metastasis data;
4. reconstruct exact patient/timepoint/treatment/modality overlap for `GSE65186` melanoma data;
5. inspect `CCell_4083` downloadable manifests for exact modality overlap and raw/processed availability;
6. determine paired overlap between CGGA `methyl_159` and each expression cohort;
7. inventory whether selected ARGO programs actually provide paired methylation + expression;
8. preserve candidates that fail overlap/access criteria rather than replacing them silently.

**No external P1 dataset has been chosen or opened for decisive GRI evaluation by this discovery record.**