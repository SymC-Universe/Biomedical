# GRI external Atlas / validation dataset candidate inventory

**Date:** 2026-09-10  
**Last source-discovery update:** 2026-09-11  
**Status:** P0-D SOURCE DISCOVERY ONLY  
**Not a cohort selection or P1 freeze.**  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 + v0.7.1A

## Purpose

Identify external data families that may eventually populate the Regulatory Substrate Atlas, support Function/Limit mapping, or serve as untouched/independent validation candidates.

Discovery does not mean selection. No candidate is chosen because it is expected to agree with GRI. Final P1 cohort selection, comparator, inclusion rules, and decision rule require a separate frozen MFR-14 process before decisive outcomes are opened.

---

## Candidate A: external lung adenocarcinoma methylation + expression cohort

### Source of record

- NCBI GEO methylation series: `GSE66836`
- NCBI GEO expression series: `GSE66863`
- NCBI BioProject: `PRJNA278125`

### Verified source facts

- 164 lung adenocarcinoma tumors and 19 matched normal lung samples in the 450K methylation series;
- 121 lung adenocarcinoma tumor samples in the Agilent expression companion;
- GEO explicitly states that expression sample numbers are matched between `GSE66836` and `GSE66863`.

Therefore the source-declared paired cross-omic tumor subset is 121. Additional methylation tumors/normals are not assumed to possess matched expression.

### Potential role

- `NOMINAL_FUNCTION`: high-priority external single-cancer static cross-omic architecture;
- expression-platform transfer relative to TCGA RNA-seq;
- possible context/perturbation work only after separate prespecification.

### Current state

`CANDIDATE_HIGH_PRIORITY_STATIC_EXTERNAL`

`PAIRED_CROSS_OMIC_TUMORS_SOURCE_DECLARED = 121`

---

## Candidate B: CGGA CCell_4083 multi-omics glioma cohort

### Source of record

- CGGA download portal: https://www.cgga.org.cn/download.jsp

### Verified source facts

The portal lists `CCell_4083` as a 35-sample multi-omics dataset with Methylation_EPIC, RNA-seq, 10X scRNA-seq, phosphoproteomics, proteomics, and associated clinical data.

The portal-level listing establishes the dataset family and total sample count. It does **not** establish that every one of the 35 samples occurs in every modality.

### Potential role

- `NOMINAL_FUNCTION`: independent glioma multi-omic architecture;
- cross-modality Atlas context;
- external platform transfer.

### Current state

`CANDIDATE_HIGH_PRIORITY_MULTIOMIC_EXTERNAL`

`EXACT_MODALITY_OVERLAP = TO_BE_VERIFIED`

---

## Candidate C: CGGA legacy glioma methylation / expression resources

### Source of record

- CGGA portal and download page.

### Verified source facts

The portal separately lists:

- `methyl_159`: 159 samples, Illumina HumanMethylation27;
- `mRNA-array_301`: 301 samples, Agilent whole-human-genome array;
- RNA-seq cohorts of 325 and 693 samples;
- primary/recurrent LGG and GBM categories.

### Critical gap

Public summary pages do not establish exact patient overlap between methylation and a particular expression cohort.

### Current state

`CANDIDATE_MEDIUM_PRIORITY_PENDING_OVERLAP_AUDIT`

---

## Candidate D: colorectal primary-to-liver-metastasis paired multi-omic series

### Source of record

- GEO `GSE213402`

### Verified source facts

- 20 samples;
- paired primary cancer and liver metastases from 10 colorectal cancer patients;
- RRBS methylation;
- RNA-seq expression.

### Potential role

- `PERTURBED_FUNCTION` P0-D state-change mapping;
- candidate architecture reorganization from primary to metastatic state.

The cohort is too small to import the current n=30 C1 design unchanged.

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

- RNA-seq `GSE237995`
- HumanMethylation450 `GSE262522`
- MethylationEPIC `GSE262524`
- Ramakrishnan et al., Genome Medicine (2024), PMID 38566104 / PMCID PMC10988846

### Verified source facts

The three GEO series belong to the same published multi-omics prostate study and carry the same 58 African American + 63 European American tumor/adjacent-tissue study design.

Source counts:

- `GSE237995`: 121 RNA-seq samples;
- `GSE262522`: 68 HumanMethylation450 samples;
- `GSE262524`: 53 MethylationEPIC samples.

The two methylation series therefore contain 121 methylation arrays in total. The published methods state that the 450K and EPIC arrays were normalized and merged with `combineArrays`, retaining 449,636 probes shared between platforms.

### Exact cross-modality identity gate, closed 2026-09-11

A source-only identity reconstruction compared the complete GEO sample-title sets without reading GRI outcomes.

Exact results:

```text
GSE262522_450K_TITLE_COUNT = 68
GSE262524_EPIC_TITLE_COUNT = 53
METHYLATION_UNION_TITLE_COUNT = 121
GSE237995_RNA_TITLE_COUNT = 121

METHYLATION_450K_EPIC_TITLE_OVERLAP = 0
METHYLATION_RNA_INTERSECTION = 121
METHYLATION_ONLY = 0
RNA_ONLY = 0

EXACT_CROSS_MODALITY_TITLE_BIJECTION = PASS
```

The exact GEO title string was the identity key. No fuzzy matching, participant-only fallback, row-order assumption, or biological-value matching was used. The 450K and EPIC arms are disjoint by title and together partition the 121 methylation samples.

Dedicated record:

`artifacts/GRI_PROSTATE_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

### Potential role

- high-priority external `NOMINAL_FUNCTION` cross-omic architecture;
- tumor-versus-adjacent context mapping;
- AA/EA context robustness;
- explicit methylation-platform transport because the study contains both 450K and EPIC;
- future Regulatory Substrate Atlas reference family after independent source/file/probe reconstruction.

### Important platform implication

Current GRI TCGA methylation carries HM27/HM450 platform-history limitations. This independent study spans 450K and EPIC and provides a published shared-probe harmonization route. It is therefore especially informative for mapping where platform changes preserve versus reorganize the representation.

That is P0-D / qualification value. It is **not** yet external GRI confirmation.

### Current state

`CANDIDATE_VERY_HIGH_PRIORITY_STATIC_EXTERNAL_AND_PLATFORM_TEST`

`SOURCE_IDENTITY_GATE = PASS`

`CROSS_MODALITY_TITLE_BIJECTION = 121_OF_121`

`PLATFORM_PARTITION = 68_450K_PLUS_53_EPIC`

`OUTCOME_STATUS = UNOPENED_FOR_GRI_P1_PURPOSES`

---

## Candidate G: ICGC ARGO program family

### Sources of record

- ICGC ARGO platform
- legacy ICGC data portal

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

- methylation `GSE58999`
- expression `GSE57968`
- SuperSeries `GSE59000`
- expression BioProject `PRJNA248618`

### Verified source facts

The source describes a matched primary-breast-tumor/regional-metastasis study from MSKCC:

- methylation for 44 matched primary-tumor/metastasis patient pairs using HumanMethylation450;
- transcriptome for 36 matched primary-tumor/metastasis patient pairs using Affymetrix U133A 2.0;
- the SuperSeries combines the two subseries;
- samples were pathologist-reviewed and microdissected to >70% tumor content according to the source description;
- sample records expose patient identity and sample state, permitting an exact future cross-modality reconstruction.

### Potential role

This is a high-information natural paired-state source:

- `PERTURBED_FUNCTION`: primary -> regional-metastatic reorganization;
- candidate `BOUNDARY_OR_TRANSITION` P0-D architecture study, without converting two sampled states into a continuous dynamical trajectory;
- test of whether scalar/modal/conglomerate relationships are preserved, redistributed, or reorganized across a clinically meaningful state change.

### Current state

`CANDIDATE_HIGH_PRIORITY_PAIRED_PERTURBED_FUNCTION`

`METHYLATION_PAIRED_CASES_SOURCE_DECLARED = 44`

`EXPRESSION_PAIRED_CASES_SOURCE_DECLARED = 36`

`EXACT_CROSS_MODALITY_PATIENT_INTERSECTION = ACTIVE_IDENTITY_AUDIT`

---

## Candidate I: melanoma baseline -> acquired MAPKi resistance multi-omic SuperSeries

### Sources of record

- SuperSeries `GSE65186`
- methylation `GSE65183`
- expression array `GSE65184`
- RNA-seq `GSE65185`
- BioProject `PRJNA273358`

### Verified source facts

GEO describes `GSE65186` as a multi-omic acquired-MAPKi-resistance study combining HumanMethylation450, Affymetrix expression, and RNA-seq. The source explicitly describes temporal transcriptomes from patient-matched tumor biopsies and sample records encode baseline/pre-MAPKi and resistant states.

This establishes genuinely ordered treatment-state information in the source family. It does not establish that every timepoint contains every modality.

### Potential role

- `PERTURBED_FUNCTION`: pretreatment -> acquired resistance;
- possible `BOUNDARY_OR_TRANSITION` mapping under therapy-driven state change;
- P0-D mapping of preservation/reorganization across scalar, modal, and module structure.

### Critical caution

Repeated biopsies, replicates, treatment differences, and patient-specific timelines imply `sample != patient != timepoint`. A future analysis must reconstruct patient/timepoint/treatment metadata before any biological computation.

### Current state

`CANDIDATE_HIGH_PRIORITY_ORDERED_PERTURBED_FUNCTION`

`EXACT_CROSS_MODALITY_TIMEPOINT_INTERSECTION = TO_BE_RECONSTRUCTED`

---

# Initial priority by research purpose

This ranking is by source/data architecture and research role, not by agreement with GRI results.

## Static external cross-layer candidates

1. `GSE262522 + GSE262524 + GSE237995` prostate: exact 121/121 cross-modality title bijection, dual 450K/EPIC methylation platforms, published 449,636-shared-probe harmonization.
2. `GSE66836 + GSE66863` lung adenocarcinoma: 121 source-declared matched tumor expression/methylation sample numbers.
3. `CGGA CCell_4083`: 35-sample multi-omics family, exact per-modality overlap pending.
4. CGGA legacy methylation/expression families: larger individual cohorts, exact pairing unresolved.

The prostate source ranks first for source-architecture richness and its now-closed identity gate, not because any GRI result has been inspected on it.

## Function/perturbation candidates

1. `GSE58999 + GSE57968 / GSE59000`: 44 methylation primary/metastasis pairs and 36 expression pairs; exact cross-modality identity reconstruction now the active source gate.
2. `GSE65186`: baseline -> acquired MAPKi resistance with multiple omic branches and ordered patient-linked states.
3. prostate `GSE262522 + GSE262524 + GSE237995`: tumor/adjacent context plus 450K/EPIC platform variation.
4. `GSE213402`: paired colorectal primary/metastasis RRBS + RNA-seq, scientifically useful but n=10 patients.
5. `GSE139388` family: acquired drug-resistance cell-model perturbation.
6. CGGA primary/recurrent categories after identity/ordering audit.

## Rare-natural-limit candidates

None of the external source candidates above is admitted as a P1 rare-natural testbed merely because it is unusual or may stress GRI.

Separately, existing TCGA PCPG is source-qualified as a **post-result P0-D rare-natural testbed** in `artifacts/GRI_PCPG_RARE_NATURAL_TESTBED_P0D_20260910.md`. It carries no confirmatory weight and is not an external validation cohort.

# Next source-discovery actions

Safe P0-D actions:

1. reconstruct exact breast patient/state/cross-modality overlap for `GSE59000`;
2. reconstruct exact melanoma patient/timepoint/treatment/modality overlap for `GSE65186`;
3. inspect `CCell_4083` manifests for exact modality overlap and source-file availability;
4. determine paired overlap between CGGA `methyl_159` and expression cohorts;
5. audit whether any ARGO program actually supplies paired methylation + expression for a GRI-compatible question;
6. verify prostate downloadable file identities/hashes and reconstruct the 449,636-shared-probe gate before any biological use;
7. preserve candidates that fail identity, access, modality, or source-provenance gates rather than replacing them silently.

**No external P1 dataset has been chosen or opened for decisive GRI evaluation by this source-discovery record.**
