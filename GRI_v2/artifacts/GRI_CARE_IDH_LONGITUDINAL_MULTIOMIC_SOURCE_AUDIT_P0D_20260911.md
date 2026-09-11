# GRI CARE IDH-mutant longitudinal multi-omic source audit

**Date:** 2026-09-11  
**Mode:** P0-D SOURCE / ORDERING / MODALITY QUALIFICATION  
**Scientific GRI outcome evaluation:** NONE  
**P1 selection/freeze:** NO

## Source family

Publication:

`Acquired genetic and cell-state changes in IDH-mutant glioma progression`

Nature 655, 1048-1059 (2026)  
DOI: `10.1038/s41586-026-10612-6`

CARE consortium cohort.

Public code:

- `Kcjohnson/care_idh_mut` — single-nucleus RNA/ATAC and downstream CARE IDH-mutant analyses;
- `Kcjohnson/care-glass` — DNA-sequencing pipelines for CARE/GLASS.

Public/controlled data named by the source:

- `GSE326221` — processed glioma 10x snRNA-seq count matrices;
- `GSE327580` — processed 10x Multiome ATAC fragments;
- Synapse `care_idh_mutant` — processed single-cell-state annotation and bulk processed DNA-seq;
- EGA `EGAS50000001727` — sequencing for selected contributing cohorts;
- DUOS-000475 and DUOS-000477 — additional controlled sequencing cohorts.

## Longitudinal cohort structure

The primary paper reports:

```text
TOTAL_TUMOR_SAMPLES = 75
TOTAL_PATIENTS = 35
OLIGODENDROGLIOMA_PATIENTS = 13
ASTROCYTOMA_PATIENTS = 22
TIMEPOINTS_PER_PATIENT = 2_OR_3
```

For the paper's main longitudinal analyses, the two earliest samples per patient are designated initial and recurrence.

```text
INITIAL_AT_PRIMARY_DIAGNOSIS = 17_OF_35_PATIENT_PAIRS
INITIAL_AT_LATER_SURGERY = 18_OF_35_PATIENT_PAIRS
TREATMENT_BETWEEN_INITIAL_AND_RECURRENCE = 26_OF_35_PATIENTS
NO_REPORTED_ADJUVANT_TREATMENT_BETWEEN_PAIR = 9_OF_35_PATIENTS
```

This distinction is critical. `initial` in this study does **not** mean treatment-naive primary diagnosis for every patient.

## Transcriptome and chromatin coverage

The paper reports snRNA-seq on the 75 longitudinal tumors and matched bulk DNA/RNA sequencing from the resected samples.

The 10x Multiome RNA+ATAC subset contains:

```text
MULTIOME_RNA_ATAC_TUMORS = 48_OF_75
MATCHED_LONGITUDINAL_MULTIOME_PAIRS = 22
```

### Exact `GSE327580` patient/timepoint gate

The complete GEO sample list for `GSE327580` exposes 48 ATAC records with explicit `Patient <id>, Timepoint <n>` titles.

Those 48 records resolve to **22 unique patient IDs**, and every one has both Timepoint 1 and Timepoint 2:

```text
57, 59, 60, 61, 71, 73, 79, 80, 81, 85, 91,
100, 101, 103, 104, 105, 106, 107, 108, 109, 110, 111
```

Four of the 22 patients also have Timepoint 3:

```text
59, 100, 105, 111
```

Thus the deposit-level arithmetic is exact:

```text
22 patients x T1/T2 = 44 samples
+ 4 T3 samples = 48 samples
```

This independently reproduces the paper's **22 matched longitudinal Multiome pairs** at the deposited-sample identity level and preserves the four third timepoints rather than discarding them.

Current gate:

`MULTIOME_PATIENT_TIMEPOINT_IDENTITY_GATE = PASS`

The public `GSE326221` processed snRNA series represents the 75-sample cohort.

A separate Smart-seq2 branch contains:

```text
SMARTSEQ2_TUMORS = 16_OF_75
```

## DNA methylation status

DNA methylation is genuinely present in the CARE cohort, but its current public source path is materially less complete than the snRNA/ATAC path.

Evidence:

1. the main paper's cohort overview explicitly includes `DNA methylation` among the per-sample data-availability tracks;
2. DNA methylation arrays are used in the paper as one line of evidence for focal PDGFRA amplification in selected samples;
3. the authors' public `scripts/figures/genomic_data_availability.R` defines a curated data-availability table with a `Bulk DNA methylation` data type alongside 10x snRNA, snATAC, SmartSeq2, whole-exome DNA, whole-genome DNA, tumor-only DNA, and bulk RNA-seq.

However:

- the paper's public Data Availability section explicitly names GEO accessions for snRNA and ATAC and Synapse for processed DNA-seq, but does **not** give a dedicated public bulk DNA-methylation accession;
- the public code reads `data/misc/genomic_data_availability_all.csv`, but that curated source table is not present in the tracked public repository tree;
- therefore the exact number of methylation-profiled CARE tumors and exact patient/timepoint overlap with bulk RNA or snRNA cannot be reconstructed from the public code alone in this audit.

Current required status:

```text
BULK_DNA_METHYLATION_PRESENT_IN_STUDY = YES
BULK_DNA_METHYLATION_EXACT_SAMPLE_COUNT = UNRESOLVED
BULK_DNA_METHYLATION_PUBLIC_ACCESSION = UNRESOLVED
BULK_DNA_METHYLATION_PAIRWISE_OVERLAP_WITH_RNA = UNRESOLVED
```

No count is inferred from a figure by eye and no missing accession is invented.

## Public-code audit

`Kcjohnson/care_idh_mut` is public and current. It explicitly encodes patient/timepoint hierarchy.

Examples from the source code:

- scripts derive `patient_id` and `timepoint` from CARE identifiers;
- several analyses explicitly restrict to two timepoints rather than treating third surgeries as independent rows;
- `genomic_data_availability.R` computes longitudinal availability per patient and modality from a curated source table;
- that script manually records 29 patients with longitudinal whole-exome-or-genome DNA coverage;
- the same script creates all-sample and longitudinal-patient data-availability summaries by modality.

The code therefore confirms the authors treated modality availability and repeated patient structure explicitly.

Important reproducibility limitation:

The key curated availability file and other processed metadata are referenced through project-local paths and are not all tracked in the public GitHub repository. Public GEO/Synapse/controlled deposits are therefore the source of record for future reconstruction, not local path strings in the analysis scripts.

## v0.7.1A research-role assessment

### PERTURBED_FUNCTION

**VERY HIGH-VALUE CANDIDATE.**

This is a real longitudinal clinical cohort with two or three surgeries per patient and documented treatment exposure between the main paired timepoints.

It can support P0-D questions about:

- preservation versus reorganization of transcriptomic architecture across recurrence;
- treatment-exposed versus no-reported-adjuvant-treatment paired contexts;
- interaction of genetic evolution with cell-state architecture;
- whether global system behavior is stable while component/modal structure changes;
- whether different patients traverse different Function Map routes under disease progression.

### BOUNDARY_OR_TRANSITION

**VERY HIGH-VALUE CANDIDATE.**

The source has genuine temporal ordering and within-patient recurrence. It therefore addresses a major weakness of static TCGA.

The evidence still does **not** automatically license:

- continuous-time dynamics;
- damping parameters;
- critical slowing;
- exceptional-point crossing;
- causal methylation-to-RNA dynamics;
- a universal transition law.

Those require their own native observables and frozen tests.

### NOMINAL_FUNCTION

Within-tumor states can also map ordinary supported architecture. Repeated tumors from one patient require hierarchical handling.

### RARE_NATURAL_LIMIT

Not assigned by this audit.

## Why this source complements rather than replaces the Nomura 2026 dual-capture cohort

The two 2026 IDH-glioma sources answer different P0-D needs.

**Nomura et al. Nature Genetics 2026:**

- smaller patient cohort;
- direct joint single-nucleus DNA methylation + Smart-seq2 RNA capture;
- clean methylation/transcriptome coupling at nucleus level;
- 15 longitudinally matched patients.

**CARE Nature 2026:**

- larger longitudinal clinical cohort;
- 35 patients, 75 tumors;
- full snRNA architecture;
- 48-tumor RNA+ATAC subset with an exact deposited 22-patient T1/T2 longitudinal crosswalk plus four T3 samples;
- treatment and genetic context richer;
- bulk DNA methylation present but exact public sample/accession route unresolved in the current audit.

Therefore they should not be collapsed into one generic `IDH glioma external cohort` record.

## Independence assessment

Relative to current TCGA GRI development:

```text
DATA_INDEPENDENCE = CANDIDATE_INDEPENDENT
COHORT_SYSTEM_INDEPENDENCE = CANDIDATE_INDEPENDENT
OUTCOME_INDEPENDENCE = UNRESOLVED_UNTIL_FUTURE_FREEZE
PARAMETER_TUNING_INDEPENDENCE = UNRESOLVED_UNTIL_FUTURE_FREEZE
METHOD_INDEPENDENCE = PARTIALLY_INDEPENDENT
ATLAS_INDEPENDENCE = UNRESOLVED_UNTIL_ATLAS_FREEZE
SOURCE_LITERATURE_INDEPENDENCE = INDEPENDENT_SOURCE_FAMILY
TEMPORAL_INDEPENDENCE = GENUINE_ORDERED_WITHIN_PATIENT_SOURCE
```

No CARE result has been used to choose a favorable GRI threshold or comparator in this source audit.

## Current source state

```text
CANDIDATE_ID = CARE_IDH_MUT_2026
RESEARCH_MODE = P0_D
PRIMARY_ROLES = PERTURBED_FUNCTION + BOUNDARY_OR_TRANSITION
TOTAL_TUMORS = 75
TOTAL_PATIENTS = 35
TIMEPOINTS = 2_OR_3_PER_PATIENT
MAIN_LONGITUDINAL_PAIRS = 35
MULTIOME_RNA_ATAC_TUMORS = 48
MULTIOME_MATCHED_LONGITUDINAL_PAIRS = 22
MULTIOME_PATIENT_TIMEPOINT_IDENTITY_GATE = PASS
MULTIOME_T3_PATIENTS = 59,100,105,111
SMARTSEQ2_TUMORS = 16
BULK_DNA_METHYLATION_PRESENT = YES
BULK_DNA_METHYLATION_EXACT_COUNT = UNRESOLVED
BULK_DNA_METHYLATION_PUBLIC_ACCESSION = UNRESOLVED
GRI_OUTCOME_STATUS = UNOPENED
P1_STATUS = NOT_SELECTED_NOT_FROZEN
```

## Next source-only gates

1. reconstruct the full 75-sample snRNA patient/timepoint table from public GEO metadata;
2. use the closed 48-sample Multiome identity gate as the source crosswalk for later P0-D RNA+ATAC mapping;
3. locate or explicitly close as unavailable the bulk DNA-methylation sample/accession source;
4. reconstruct treatment-between-timepoint and diagnosis-versus-later-surgery status from Supplementary Table 1 without reading GRI outcomes;
5. preserve third timepoints rather than discarding them, even if a later frozen analysis focuses on T1/T2;
6. keep this candidate P0-D until a future claim/comparator/MFR-14 is deliberately frozen.
