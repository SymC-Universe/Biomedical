# GRI CGGA CCell_4083 modality / overlap source audit

**Date:** 2026-09-11  
**Mode:** P0-D SOURCE / MODALITY QUALIFICATION  
**Scientific GRI outcome evaluation:** NONE  
**P1 selection/freeze:** NO

## Source family

CGGA DataSet ID: `CCell_4083`

Associated publication:

`Protein-based classification reveals an immune-hot subtype in IDH mutant astrocytoma with worse prognosis`, Cancer Cell 2025, DOI 10.1016/j.ccell.2025.08.006.

Public analysis repository:

`Jihong-Tang/Proteomics_IME`

NGDC/OMIX/GSA BioProject family:

`PRJCA044619`

## Why this audit was needed

The CGGA download portal lists:

```text
Data type: Multi-omics
Platform: Methylation_EPIC, RNA-seq, 10X scRNA-seq, Phosphoproteomics, Proteomics
Total number of samples: 35
```

That portal-level `35 samples` label could be misread as meaning that all five listed modalities were measured on the same 35 tumors.

The source-of-record deposits show that this interpretation is false.

## Modality-specific source counts

### Proteomics

OMIX accession `OMIX011526`:

```text
DESCRIPTION = Proteomic dataset of 35 IDH mutant astrocytomas from CGGA
NUMBER_OF_SAMPLES = 35
ACCESS = CONTROLLED
```

### Phosphoproteomics

OMIX accession `OMIX011528`:

```text
DESCRIPTION = Phosphoproteomic dataset of 35 IDH mutant astrocytomas from CGGA
NUMBER_OF_SAMPLES = 35
ACCESS = CONTROLLED
```

### DNA methylation

OMIX accession `OMIX011529`:

```text
DESCRIPTION = DNA methylation dataset of 29 IDH mutant astrocytomas from CGGA
NUMBER_OF_SAMPLES = 29
DATA_TYPE = Methylation profiling by Array
CURRENT_RAW_DOWNLOAD_STATUS = UNAVAILABLE at source because of registration restriction
```

### Bulk RNA-seq

GSA-Human accession `HRA012868`:

```text
TITLE = CGGA - RNA-seq dataset (19 IDHmut astrocytoma)
DESCRIPTION = RNA-seq dataset of 19 IDH-mutant astrocytoma gliomas from CGGA
NUMBER_OF_SAMPLES = 19
ACCESS = CONTROLLED
```

### Single-cell RNA-seq

GSA-Human accession `HRA012903`:

Source title:

```text
CGGA - scRNAseq dataset (18 IDHmut Astrocytoma)
```

The source description separately says `19 sample ... containing 21 tumor`, which is internally inconsistent at the portal text level. The public analysis code reads a Seurat object named:

```text
0316_Merged.Major.18MutA.QC.rds
```

Therefore this audit does **not** silently resolve the discrepancy by choosing one count. For source bookkeeping:

```text
SC_RNA_PATIENT_SAMPLE_COUNT = 18_BY_ACCESSION_TITLE_AND_PUBLIC_ANALYSIS_OBJECT_NAME
SC_RNA_SOURCE_DESCRIPTION_COUNT = 19_SAMPLE_CONTAINING_21_TUMOR
SC_RNA_COUNT_DISCREPANCY = OPEN_SOURCE_METADATA_DISCREPANCY
```

The exact individual/tumor mapping requires the controlled-access/source manifest.

## Immediate conclusion

The five modalities cannot all be complete on the same 35 samples because the source deposits have different modality-specific sample counts:

```text
PROTEOMICS = 35
PHOSPHOPROTEOMICS = 35
METHYLATION = 29
BULK_RNA = 19
SC_RNA = 18_BY_TITLE / 19_BY_DESCRIPTION
```

Therefore:

```text
ALL_FIVE_MODALITIES_COMPLETE_ON_35 = FALSE
PORTAL_35 = STUDY_FAMILY_OR_MAXIMUM_MODALITY_COHORT_SIZE, NOT A COMPLETE_FIVE_MODALITY_INTERSECTION
```

The exact all-modality and pairwise intersections remain to be reconstructed from source identifiers.

## Public-repository cross-modality evidence

The associated public GitHub repository confirms that multiple modality layers are tied through shared cohort identifiers but does not expose a complete processed-data manifest in the tracked code.

### Methylation -> protein-defined cohort relation

`Figure8_Diagnostic_Multiomics/Main_Figure8_Visualization.R`:

- reads a methylation coordinate table;
- renames its first column `Cohort_ID`;
- reads the protein-cluster clinical metadata;
- merges methylation and protein-cluster metadata by `Cohort_ID`;
- elsewhere reads a methylation matrix and filters its columns by the same protein-cluster `Cohort_ID` values.

This proves that the authors had a cohort-identity crosswalk between methylation and protein-defined samples in the working analysis.

It does **not** expose the exact 29 IDs in a tracked text manifest.

### scRNA -> protein-defined cohort relation

`Figure3_TME_scRNA/Main_Figure3_Visualization.R`:

- reads the `18MutA` merged scRNA object;
- reads `data/scRNA_cluster.txt`;
- assigns protein-cluster labels by matching scRNA `orig.ident` against `Cohort_ID`.

This proves that the authors had a cohort-identity crosswalk between the scRNA samples used for Figure 3 and protein-defined cohort metadata.

Again, the required source table is referenced by code but not exposed through the public repository search as a tracked text file.

## Raw and processed availability

The public repository README records:

- sequencing deposits at `HRA012868`, `HRA012869`, `HRA012870`, `HRA012903`;
- proteomics, phosphoproteomics, and methylation deposits at `OMIX011526`, `OMIX011528`, `OMIX011529`, respectively;
- processed level-3 data at the CGGA download portal under `CCell_4083`.

The CGGA portal exposes separate download entries for:

- Clinical Data;
- Methylation_EPIC;
- STAR+RSEM FPKM expression;
- scRNAseq Seurat object;
- Phosphoproteomics_MS;
- Proteomics_MS.

This is sufficient to establish modality availability but not exact pairwise identity overlap without the downloaded manifests.

## GRI relevance under v0.7.1A

### NOMINAL_FUNCTION

Potentially strong external multi-layer context because protein, phosphoprotein, methylation, bulk RNA, and single-cell information come from one study family.

### PERTURBED_FUNCTION / BOUNDARY_OR_TRANSITION

Not automatically licensed from the 35-sample cross-sectional subset. The broader publication includes longitudinal initial/recurrent analyses, but those cannot be assumed to be the same complete CCell_4083 multi-omic subset without an explicit source crosswalk.

### Cross-layer / conglomerate architecture

Potentially high value because a future Atlas could preserve:

- bulk methylation architecture;
- bulk RNA architecture;
- protein/phosphoprotein state;
- single-cell composition/state;
- shared cohort identity where genuinely present.

This is especially valuable for testing whether apparently similar bulk system-level states hide different cellular compositions or protein-layer organizations.

## Independence / access implications

This is materially external to the current TCGA GRI development lineage, but independence must remain pathway-specific.

Current source-audit state:

```text
DATA_INDEPENDENCE_FROM_TCGA_GRI = CANDIDATE_INDEPENDENT
COHORT_SYSTEM_INDEPENDENCE = CANDIDATE_INDEPENDENT
OUTCOME_INDEPENDENCE = UNRESOLVED_UNTIL_FUTURE_USE_IS_FROZEN
PARAMETER_TUNING_INDEPENDENCE = UNRESOLVED_UNTIL_FUTURE_USE_IS_FROZEN
ATLAS_INDEPENDENCE = UNRESOLVED_UNTIL_ATLAS_CONSTRUCTION_FREEZE
SOURCE_LITERATURE_INDEPENDENCE = PARTIALLY_INDEPENDENT_FROM_GRI_DEVELOPMENT
TEMPORAL_INDEPENDENCE = NOT_APPLICABLE_FOR_CURRENT_STATIC_MODALITY_AUDIT
```

Controlled-access raw data and the unavailable raw methylation download may limit immediate full reconstruction. That is an access state, not a reason to invent pairwise overlap.

## Current state

```text
RESEARCH_STATUS = P0_D_SOURCE_QUALIFIED_MULTIOMIC_CANDIDATE
CGGA_PORTAL_TOTAL = 35
PROTEOMICS_N = 35
PHOSPHOPROTEOMICS_N = 35
METHYLATION_N = 29
BULK_RNA_N = 19
SC_RNA_N = 18_BY_TITLE_WITH_19_SAMPLE_SOURCE_DESCRIPTION_DISCREPANCY
ALL_FIVE_COMPLETE_ON_35 = FALSE
EXACT_PAIRWISE_MODALITY_OVERLAP = UNRESOLVED
PUBLIC_CODE_CONFIRMS_COHORT_ID_CROSSWALKS_EXIST = YES
GRI_OUTCOME_STATUS = UNOPENED
P1_STATUS = NOT_SELECTED_NOT_FROZEN
```

## Next source gate

The next useful source-only step is to obtain or inspect the processed CCell_4083 modality manifests and build a compact `Cohort_ID x modality` presence matrix.

Required columns:

```text
Cohort_ID
clinical_present
proteomics_present
phosphoproteomics_present
methylation_present
bulk_rna_present
scrna_present
initial_recurrent_status_if_source_verified
source_accession
```

Until that matrix is reconstructed, no statement about a 19-, 18-, 29-, or 35-sample exact cross-modality intersection is licensed.
