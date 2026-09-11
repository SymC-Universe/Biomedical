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

### Sources of record

- CGGA DataSet ID `CCell_4083`;
- public repository `Jihong-Tang/Proteomics_IME`;
- BioProject family `PRJCA044619`;
- proteomics `OMIX011526`;
- phosphoproteomics `OMIX011528`;
- methylation `OMIX011529`;
- bulk RNA-seq `HRA012868`;
- scRNA-seq `HRA012903`.

### Source audit result

The CGGA portal describes `CCell_4083` as a 35-sample multi-omics family, but modality-specific source deposits prove that **35 is not a complete five-modality intersection**.

Verified modality counts:

```text
PROTEOMICS = 35
PHOSPHOPROTEOMICS = 35
METHYLATION = 29
BULK_RNA = 19
SC_RNA = 18_BY_ACCESSION_TITLE
SC_RNA_SOURCE_DESCRIPTION = 19_SAMPLE_CONTAINING_21_TUMOR
```

Thus:

`ALL_FIVE_MODALITIES_COMPLETE_ON_35 = FALSE`

The scRNA source itself contains a count-description discrepancy, which remains open rather than being silently reconciled.

Public analysis code confirms cohort-identity crosswalks existed between:

- methylation and protein-defined cohort metadata via `Cohort_ID`;
- scRNA samples and protein-defined cohort metadata via `Cohort_ID`.

The exact pairwise modality intersections are not exposed by the public code alone and require processed/controlled manifests.

Dedicated record:

`artifacts/GRI_CGGA_CCELL4083_MODALITY_AUDIT_P0D_20260911.md`

### Potential role

- `NOMINAL_FUNCTION`: independent multi-layer glioma context;
- cross-modal Atlas construction;
- test of bulk versus cellular composition/state organization;
- protein/phosphoprotein context for methylation/RNA relationships;
- external platform and modality-transport mapping.

### Current state

`CANDIDATE_HIGH_PRIORITY_MULTIOMIC_EXTERNAL`

`MODALITY_COUNT_GATE = PASS`

`ALL_FIVE_COMPLETE_ON_35 = FALSE`

`EXACT_PAIRWISE_MODALITY_OVERLAP = UNRESOLVED`

`GRI_OUTCOME_STATUS = UNOPENED`

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

A source-only identity reconstruction compared complete GEO sample-title sets without reading GRI outcomes.

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

The exact GEO title string was the identity key. No fuzzy matching, participant-only fallback, row-order assumption, or biological-value matching was used.

Dedicated record:

`artifacts/GRI_PROSTATE_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

### Potential role

- high-priority external `NOMINAL_FUNCTION` cross-omic architecture;
- tumor-versus-adjacent context mapping;
- AA/EA context robustness;
- explicit methylation-platform transport across 450K and EPIC;
- future Regulatory Substrate Atlas reference family after independent source/file/probe reconstruction.

### Current state

`CANDIDATE_VERY_HIGH_PRIORITY_STATIC_EXTERNAL_AND_PLATFORM_TEST`

`SOURCE_IDENTITY_GATE = PASS`

`CROSS_MODALITY_TITLE_BIJECTION = 121_OF_121`

`PLATFORM_PARTITION = 68_450K_PLUS_53_EPIC`

`OUTCOME_STATUS = UNOPENED_FOR_GRI_P1_PURPOSES`

---

## Candidate G: ICGC ARGO program family

### Sources of record

- ICGC ARGO platform;
- legacy ICGC data portal.

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

- methylation `GSE58999`;
- expression `GSE57968`;
- SuperSeries `GSE59000`;
- expression BioProject `PRJNA248618`;
- Reyngold et al., PLoS ONE 2014, PMCID PMC4118917 / PMID 25083786.

### Source audit result

The methylation branch contains 44 matched primary/metastasis patient pairs = 88 samples. The expression branch contains 36 matched pairs = 72 samples. The published source explicitly states that RNA was available for 36 of the 44 methylation-profiled pairs.

Complete title audit:

```text
EXPRESSION_TITLE_COUNT = 72
METHYLATION_TITLE_COUNT = 88
RAW_EXPRESSION_METHYLATION_TITLE_INTERSECTION = 66
RAW_EXPRESSION_ONLY_TITLES = 6
```

The six raw mismatches are explained by one terminal-`b` source-naming asymmetry. Removing only one terminal lowercase `b` for a diagnostic source crosswalk gives:

```text
TERMINAL_B_NORMALIZED_EXPRESSION_IN_METHYLATION = 72_OF_72
METHYLATION_EXTRA_NORMALIZED_TITLES = 16
```

The 16 extra methylation titles equal eight methylation-only patient pairs, consistent with the 44-versus-36 source design.

Several suffix-discrepant examples were independently checked in GEO metadata and map to the same patient and same primary/metastatic state. A complete 72-row GSM/patient/state export is still required before this diagnostic normalization becomes a production identity rule.

Dedicated record:

`artifacts/GRI_BREAST_PAIRED_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

### Potential role

- `PERTURBED_FUNCTION`: primary -> regional-metastatic reorganization;
- `BOUNDARY_OR_TRANSITION`: paired state-change architecture without claiming continuous dynamics;
- Function Map preservation/redistribution analysis;
- Limit Map transport/refusal analysis.

### Current state

`CANDIDATE_HIGH_PRIORITY_PAIRED_PERTURBED_FUNCTION`

`SOURCE_CROSS_MODALITY_PATIENT_SUBSET = PASS`

`RAW_TITLE_MATCH = 66_OF_72`

`TERMINAL_B_NORMALIZED_TITLE_MATCH = 72_OF_72`

`PER_SAMPLE_GSM_PATIENT_STATE_CROSSWALK = PENDING_FINAL_MECHANICAL_EXPORT`

`GRI_OUTCOME_STATUS = UNOPENED`

---

## Candidate I: melanoma baseline -> acquired MAPKi resistance multi-omic SuperSeries

### Sources of record

- SuperSeries `GSE65186`;
- methylation `GSE65183`;
- expression array `GSE65184`;
- RNA-seq `GSE65185`;
- BioProject `PRJNA273358`.

### Source audit result

The 218-sample SuperSeries contains:

```text
METHYLATION_ARRAY_SAMPLES = 144
EXPRESSION_ARRAY_SAMPLES = 4
RNASEQ_SAMPLES = 70
```

After separating methylation assay replicates from biological states and applying only source-metadata-supported naming reconciliations:

```text
UNIQUE_HUMAN_METHYLATION_STATES = 63
UNIQUE_HUMAN_TRANSCRIPTOME_STATES = 64
SHARED_HUMAN_PATIENT_STATES = 61
SHARED_HUMAN_PATIENT_IDS = 19
STRICT_SHARED_BASELINE_PLUS_POST_PATIENTS = 18
SHARED_CELL_MODEL_STATES = 8_OF_8
```

Human methylation-only states:

```text
Pt14-baseline
Pt14-DP1
```

Transcriptome-only human states:

```text
Pt19-DDP2
Pt24-baseline
Pt24-DDP1
```

Pt21 has shared resistant states but no shared baseline and therefore must be refused from a strict paired baseline-to-resistance analysis unless a different source rule is prospectively justified.

Dedicated record:

`artifacts/GRI_MELANOMA_MAPKI_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

### Potential role

- strong `PERTURBED_FUNCTION` candidate with genuinely ordered treatment states;
- candidate `BOUNDARY_OR_TRANSITION` mapping under acquired resistance;
- patient-level Function Map of preservation versus reorganization;
- separate 8-state cell-model P0-D mechanism/qualification branch.

### Critical caution

`sample != patient != timepoint`. Repeated biopsies, assay replicates, and treatment-state structure must remain explicit. Human and cell-model evidence are not pooled.

### Current state

`P0_D_SOURCE_QUALIFIED_ORDERED_PERTURBATION_CANDIDATE`

`SHARED_HUMAN_PATIENT_STATES = 61`

`STRICT_SHARED_BASELINE_PLUS_POST_PATIENTS = 18`

`SHARED_CELL_MODEL_STATES = 8_OF_8`

`GRI_OUTCOME_STATUS = UNOPENED`

`P1_STATUS = NOT_SELECTED_NOT_FROZEN`

---

# Initial priority by research purpose

This ranking is by source/data architecture and research role, not by agreement with GRI results.

## Static external cross-layer candidates

1. `GSE262522 + GSE262524 + GSE237995` prostate: exact 121/121 cross-modality title bijection, dual 450K/EPIC methylation platforms, published 449,636-shared-probe harmonization.
2. `GSE66836 + GSE66863` lung adenocarcinoma: 121 source-declared matched tumor expression/methylation sample numbers.
3. `CCell_4083`: unusually rich modality family, but exact intersections are smaller than 35 and still require manifest reconstruction; current verified counts are 35 protein, 35 phosphoprotein, 29 methylation, 19 bulk RNA, and approximately 18 scRNA source cases.
4. CGGA legacy methylation/expression families: larger individual cohorts, exact pairing unresolved.

The prostate source ranks first for source-architecture richness and its closed identity gate, not because any GRI result has been inspected on it.

## Function/perturbation candidates

1. `GSE65186` melanoma: source-qualified ordered treatment-state family with 61 shared human patient-states, 18 strict baseline+post patients, and a separate 8/8 cell-model branch.
2. `GSE58999 + GSE57968 / GSE59000` breast: source-declared 36-patient-pair expression subset inside 44 methylation pairs; 72/72 diagnostic title crosswalk after a narrowly documented terminal-`b` reconciliation.
3. prostate `GSE262522 + GSE262524 + GSE237995`: tumor/adjacent context plus 450K/EPIC platform variation.
4. `GSE213402`: paired colorectal primary/metastasis RRBS + RNA-seq, scientifically useful but n=10 patients.
5. `GSE139388` family: acquired drug-resistance cell-model perturbation.
6. CGGA primary/recurrent categories after identity/ordering audit.

The melanoma family now ranks first for `PERTURBED_FUNCTION` source architecture because it contains genuinely ordered patient-linked baseline/resistance states and repeated resistant biopsies, not because any GRI outcome has been inspected.

## Rare-natural-limit candidates

None of the external source candidates above is admitted as a P1 rare-natural testbed merely because it is unusual or may stress GRI.

Separately, existing TCGA PCPG is source-qualified as a **post-result P0-D rare-natural testbed** in `artifacts/GRI_PCPG_RARE_NATURAL_TESTBED_P0D_20260910.md`. It carries no confirmatory weight and is not an external validation cohort.

# Next source-discovery actions

Safe P0-D actions:

1. obtain/inspect `CCell_4083` processed manifests and reconstruct the `Cohort_ID x modality` presence matrix; preserve the scRNA source-count discrepancy;
2. complete the breast 72-row GSM/patient/state crosswalk before any biological use of the terminal-`b` normalization;
3. produce a full melanoma patient/state/modality/replicate manifest and preserve Pt14, Pt19-DDP2, Pt21, and Pt24 exceptions;
4. determine paired overlap between CGGA `methyl_159` and expression cohorts;
5. audit whether any ARGO program actually supplies paired methylation + expression for a GRI-compatible question;
6. verify prostate downloadable file identities/hashes and reconstruct the 449,636-shared-probe gate before any biological use;
7. preserve candidates that fail identity, access, modality, or source-provenance gates rather than replacing them silently.

**No external P1 dataset has been chosen or opened for decisive GRI evaluation by this source-discovery record.**
