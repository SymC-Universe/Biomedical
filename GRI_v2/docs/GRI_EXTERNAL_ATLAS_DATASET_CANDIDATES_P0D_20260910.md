# GRI external Atlas / validation dataset candidate inventory

**Date:** 2026-09-10  
**Status:** P0-D SOURCE DISCOVERY ONLY  
**Not a cohort selection or P1 freeze.**  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Purpose

Identify external data families that may eventually populate the Regulatory Substrate Atlas, support Function/Limit mapping, or serve as untouched/independent validation candidates.

Discovery does not mean selection. No candidate is chosen because it is expected to agree with GRI. Final P1 cohort selection, comparator, inclusion rules, and decision rule require a separate frozen MFR-14 process before decisive outcomes are opened.

Retrieval date for sources below: 2026-09-10.

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

- methylation `GSE262522`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE262522
- RNA-seq `GSE237995`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE237995
- BioProject `PRJNA997353`: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA997353

### Verified source facts

Both GEO series carry the same study title.

- `GSE237995`: 121 RNA-seq samples under the study's 58 African American + 63 European American design;
- `GSE262522`: 68 HumanMethylation450 samples;
- individual participant-style identifiers demonstrably occur in both series;
- complete cross-series overlap has not yet been enumerated.

### Potential role

- external `NOMINAL_FUNCTION` cross-omic prostate architecture;
- tumor-versus-adjacent context;
- population/context robustness.

### Current state

`CANDIDATE_HIGH_PRIORITY_STATIC_EXTERNAL_PENDING_EXACT_ID_OVERLAP`

`RNA_SAMPLE_COUNT = 121_SOURCE_VERIFIED`

`METHYLATION_SAMPLE_COUNT = 68_SOURCE_VERIFIED`

`EXACT_PAIRED_COUNT = TO_BE_ENUMERATED`

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
- samples were pathologist-reviewed and microdissected to >70% tumor content according to the GEO description.

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

The sample records contain repeated patient-linked states such as baseline/pre-MAPKi and post-BRAFi or BRAFi+MEKi resistance. For example, patient 20 has source records for a baseline methylation biopsy and a baseline RNA-seq biopsy, while later methylation/RNA records identify resistant states. This establishes that the SuperSeries contains genuinely ordered treatment-state information, although the exact cross-modality/timepoint intersection must be reconstructed before analysis.

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

1. `GSE66836 + GSE66863` lung adenocarcinoma: 121 source-declared matched tumor expression/methylation sample numbers.
2. `GSE262522 + GSE237995` prostate study family: 68 methylation samples within a 121-sample RNA study; exact paired overlap pending.
3. `CGGA CCell_4083`: 35-sample multi-omics dataset with EPIC methylation, RNA-seq, proteomics/phosphoproteomics, and scRNA-seq listed; exact overlap pending.
4. CGGA legacy methylation/expression families: larger individual cohorts, exact pairing unresolved.

### Function/perturbation mapping candidates

1. `GSE58999 + GSE57968 / GSE59000`: 44 matched primary/metastatic methylation pairs and 36 matched primary/metastatic expression pairs, high-value natural paired-state architecture.
2. `GSE65186`: baseline -> acquired MAPKi-resistance melanoma with methylation + expression array + RNA-seq and repeated patient-linked states.
3. `GSE213402`: paired primary/metastatic colorectal RRBS + RNA-seq, scientifically clean pairing but only 10 patients.
4. `GSE139388` family: acquired drug-resistance cell-model perturbation, useful mechanism testbed but not population validation.
5. CGGA primary/recurrent categories: potentially useful after exact pairing/temporal relationship verification.

### Rare-natural-limit candidates

Among the **external source candidates in this file**, none is admitted as a P1 rare-natural testbed merely because it is unusual or expected to stress GRI.

Separately, the existing TCGA PCPG stress case is now source-qualified as a **post-result P0-D rare-natural testbed** in `artifacts/GRI_PCPG_RARE_NATURAL_TESTBED_P0D_20260910.md`. It carries no confirmatory weight and is not an external validation cohort.

# Next source-discovery actions

Safe P0-D actions:

1. retain the source-declared 121 matched lung tumor subset as a high-priority static external candidate without evaluating GRI outcomes;
2. enumerate exact title/identifier overlap for the 68 prostate methylation samples against the 121 RNA samples;
3. reconstruct exact patient/timepoint/modality overlap for `GSE59000` breast primary/metastasis data;
4. reconstruct exact patient/timepoint/treatment/modality overlap for `GSE65186` melanoma data;
5. inspect `CCell_4083` downloadable manifests for exact modality overlap and raw/processed availability;
6. determine paired overlap between CGGA `methyl_159` and each expression cohort;
7. inventory whether selected ARGO programs actually provide paired methylation + expression;
8. preserve candidates that fail overlap/access criteria rather than replacing them silently.

**No external P1 dataset has been chosen or opened for decisive GRI evaluation by this discovery record.**