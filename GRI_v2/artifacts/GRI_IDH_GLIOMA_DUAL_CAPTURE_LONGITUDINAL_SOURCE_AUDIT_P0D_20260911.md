# GRI longitudinal IDH-glioma joint DNA-methylation/RNA source audit

**Date:** 2026-09-11  
**Mode:** P0-D SOURCE / IDENTITY / ORDERING QUALIFICATION  
**Scientific GRI outcome evaluation:** NONE  
**P1 selection/freeze:** NO

## Source family

Publication:

`Longitudinal changes in DNA methylation in IDH-mutant glioma fuel disease progression through altered cell state differentiation`

Nature Genetics 58, 1651-1660 (2026)  
DOI: `10.1038/s41588-026-02642-7`

Primary processed-data series:

- `GSE292025` — single-nucleus XRBS DNA methylation;
- `GSE291885` — matched Smart-seq2 single-nucleus transcriptome products from the joint-capture workflow;
- `GSE292130` — 10x 3' snRNA-seq complementary high-throughput transcriptome branch.

Controlled raw human data:

- DUOS-000475;
- DUOS-000476;
- DUOS-000480.

Public analysis code:

- `rr1859/sc_DNAme_RNA_GCIMP_Analysis`;
- Zenodo `10.5281/zenodo.20097728`.

## Cohort structure

The primary paper reports:

```text
TOTAL_FROZEN_TUMOR_SAMPLES = 36
TOTAL_PATIENTS = 19
LONGITUDINALLY_MATCHED_TUMOR_SAMPLES = 32
LONGITUDINALLY_MATCHED_PATIENTS = 15
UNMATCHED_PRIMARY_OR_RECURRENT_TUMORS = 4
```

The 15 longitudinal patients include 11 IDH-mutant astrocytoma patients and 4 IDH-mutant oligodendroglioma patients.

This is genuine within-patient longitudinal sampling. The source is therefore qualitatively different from cross-sectional TCGA ordering and can support P0-D `PERTURBED_FUNCTION` and state-change mapping without inventing pseudo-time.

## Joint-capture methylation + RNA architecture

The core assay is unusually valuable for GRI because methylation and transcription are captured from the **same nuclei**, not merely from separate bulk aliquots from the same tumor.

The paper reports:

- one 96-cell dual-sequencing plate per tumor sample across 36 samples;
- Smart-seq2 full-length transcriptome capture;
- XRBS DNA methylation capture;
- cells retained only after both methylation and transcriptome QC;
- mean 58.8 retained cells per sample, range 24-85;
- `n = 2,117` nuclei with matched transcriptomic measurements in the joint dataset.

`GSE292025` exposes 36 tumor-level GEO sample records and a 2,117-row single-nucleus data table. The GEO row structure links each methylation nucleus/library to the corresponding sample and processed coverage product.

`GSE291885` exposes processed Smart-seq2 products for the matched transcriptome side. GEO represents this series with two top-level records, including an all-cells metadata product, rather than 36 separate tumor-level GEO records. Therefore top-level GEO `Samples (2)` must **not** be misread as two biological tumors.

## Complementary 10x branch

The paper reports high-throughput 10x 3' snRNA-seq retained for:

```text
PAPER_10X_TUMOR_COUNT = 32
PAPER_10X_NUCLEI_AFTER_QC = 158143
```

The current `GSE292130` accession exposes:

```text
GEO_10X_SAMPLE_RECORD_COUNT = 31
```

This creates a source/deposition discrepancy:

`PAPER_10X_TUMOR_COUNT_32 != GEO_CURRENT_RECORD_COUNT_31`

No missing tumor identity is invented in this audit. The discrepancy may reflect deposition packaging, final QC, or an updated source record, but that cause remains unresolved until an exact paper-to-GEO sample manifest is reconstructed.

This discrepancy does **not** affect the existence of the 36-sample joint XRBS+Smart-seq2 branch, which is the cleaner methylation/RNA cross-layer source for current P0-D planning.

## Public-code audit

Repository:

`rr1859/sc_DNAme_RNA_GCIMP_Analysis`

Current public tree contains separate `DNA_methylation/` and `RNA/` analysis scripts.

The DNA-methylation clustering code:

- loads a cell-level methylation matrix;
- loads an annotation object;
- tracks sample identity in `sample_final`;
- retains primary/recurrent occurrence in `Occurence`;
- carries G-CIMP, methylation, cell-state, stemness, and other annotations;
- performs Harmony using sample identity rather than silently assuming all nuclei are independent biological tumors.

The RNA code constructs Seurat objects from separate count and metadata files and performs cell-state analyses.

Important reproducibility limitation:

The public repository README still says `IN DEVELOPMENT` and states that final data would be added after manuscript finalization. The scripts reference local/institutional data paths and metadata objects that are not all tracked in the repository. Therefore the GitHub repository is useful analysis provenance but is **not by itself a complete clean-room data package**.

Processed study data are instead available through GEO, with raw human sequence data controlled under DUOS.

## v0.7.1A research-role assessment

### PERTURBED_FUNCTION

**VERY HIGH-VALUE CANDIDATE.**

The cohort contains longitudinally paired tumors from 15 patients and direct joint methylation/RNA measurements at single-nucleus resolution.

Potential P0-D questions include:

- which cross-layer relationships persist within patient across progression;
- which modal/conglomerate structures redistribute at recurrence;
- whether different nuclei within the same tumor occupy distinct internal states while sharing a tumor-level methylation background;
- whether similar system-level states arise from different cell-state mixtures;
- where a bulk-style reduction loses information relative to joint single-nucleus structure.

### BOUNDARY_OR_TRANSITION

**HIGH-VALUE CANDIDATE, WITH A FIREWALL.**

Longitudinal sampling licenses ordered state comparisons. It does **not** automatically establish continuous dynamics, tipping points, damping, critical slowing, exceptional-point crossing, or causal transition laws.

### NOMINAL_FUNCTION

Each sampled tumor can also contribute within-state Function Map information, but repeated tumors from the same patient cannot be treated as independent cohort members without explicit hierarchical handling.

### RARE_NATURAL_LIMIT

Not assigned by this audit. IDH-mutant glioma subtype status does not automatically make a sample a GRI rare-natural limit testbed.

## Independence assessment

Relative to the current TCGA GRI development lineage:

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

The same GRI Engine could eventually be applied to this external source without destroying data independence, provided no outcome-dependent tuning is performed on the decisive evidence.

## Representation issue for GRI

This source does not use TCGA bulk 450K methylation and bulk RNA-seq. It uses single-nucleus XRBS and matched Smart-seq2 RNA.

Therefore it should **not** be forced directly through a TCGA-specific input representation merely to claim external replication.

P0-D must first determine:

- what GRI architecture is representation-invariant across bulk-array and joint single-nucleus measurements;
- whether a native single-nucleus System Model adapter is required;
- what is lost by aggregating nuclei to tumor-level quantities;
- whether tumor-level and nucleus-level Function Maps tell the same or different stories.

Any adapter/calibration developed on these data remains P0-D/P0-Q and cannot confirm itself.

## Current source state

```text
CANDIDATE_ID = IDH_GLIOMA_NOMURA_2026_DUAL_CAPTURE
RESEARCH_MODE = P0_D
PRIMARY_ROLES = PERTURBED_FUNCTION + BOUNDARY_OR_TRANSITION
TOTAL_TUMORS = 36
TOTAL_PATIENTS = 19
MATCHED_LONGITUDINAL_TUMORS = 32
MATCHED_LONGITUDINAL_PATIENTS = 15
JOINT_XRBS_SS2_MATCHED_NUCLEI = 2117
GSE292025_TUMOR_RECORDS = 36
PAPER_10X_TUMORS = 32
GSE292130_CURRENT_SAMPLE_RECORDS = 31
TENX_COUNT_DISCREPANCY = OPEN
GRI_OUTCOME_STATUS = UNOPENED
P1_STATUS = NOT_SELECTED_NOT_FROZEN
```

## Next source-only gates

1. reconstruct the exact 36-tumor identity/order table from `GSE292025` and publication metadata;
2. verify the exact 32 matched tumors / 15 patient pairs in source metadata;
3. reconstruct the 2,117-nucleus methylation↔Smart-seq2 pairing schema from GEO processed metadata;
4. resolve or preserve the paper-32 versus GEO-31 10x discrepancy;
5. inventory treatment/exposure between paired surgeries without using any GRI result;
6. define a P0-D single-nucleus representation plan before any GRI computation;
7. keep this source separate from any future untouched P1 cohort until a claim and MFR-14 are deliberately frozen.
