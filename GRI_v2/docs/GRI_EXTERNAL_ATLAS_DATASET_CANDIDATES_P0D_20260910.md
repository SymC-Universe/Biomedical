# GRI external Atlas / validation dataset candidate inventory

**Created:** 2026-09-10  
**Last source-discovery update:** 2026-09-11  
**Status:** P0-D SOURCE DISCOVERY ONLY  
**P1 cohort selected:** NO  
**GRI scientific outcomes opened on candidates:** NO  
**Protocol authority:** General Cross-Project Research Protocol v0.7.1 FINAL + v0.7.1A Addendum

## Purpose and firewall

This is the canonical working inventory of external source families that may later support the Regulatory Substrate Atlas, Function/Limit mapping, method qualification, or a separately frozen untouched P1 test.

Source discovery is **not** confirmation. Candidates are ranked by source architecture, identity quality, modality coverage, perturbation/ordering value, access, and fit to a research role. They are not ranked by agreement with GRI outcomes.

Every candidate remains:

```text
research_mode = P0_D
gri_outcome_status = UNOPENED
p1_status = NOT_SELECTED_NOT_FROZEN
selection_basis = SOURCE_ARCHITECTURE_NOT_GRI_AGREEMENT
```

Machine-readable source gate ledger:

`config/gri_external_source_gate_ledger_20260911.json`

Representation firewall:

`config/gri_external_representation_compatibility_20260911.json`

---

# A. Static / near-current-representation candidates

## A1. Prostate tumor / adjacent-tissue multi-omic family

**Accessions:** `GSE262522` 450K methylation, `GSE262524` EPIC methylation, `GSE237995` RNA-seq.  
**Publication:** Ramakrishnan et al., Genome Medicine 2024, PMID 38566104 / PMCID PMC10988846.

### Source facts

```text
450K = 68 samples
EPIC = 53 samples
methylation union = 121 samples
RNA-seq = 121 samples
published 450K/EPIC shared-probe set = 449,636
```

The published workflow normalizes and combines the two methylation platforms on the 449,636 probes shared between them.

### Exact source identity gate

Complete GEO sample-title reconstruction gives:

```text
450K ∩ EPIC titles = 0
methylation union titles = 121
RNA titles = 121
methylation ∩ RNA titles = 121
methylation-only = 0
RNA-only = 0
EXACT_CROSS_MODALITY_TITLE_BIJECTION = PASS
```

No fuzzy matching, row-order matching, biological-value matching, or participant-only fallback was used.

Dedicated audit:

`artifacts/GRI_PROSTATE_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

### Current role

- very-high-priority `NOMINAL_FUNCTION` external bulk candidate;
- tumor-versus-adjacent context mapping;
- AA/EA context robustness;
- direct platform-transport test across 450K and EPIC;
- candidate future Atlas family.

### Remaining source gates

- verify downloadable file identities/hashes;
- independently reconstruct the 449,636 shared-probe gate from source files or a frozen documented equivalent;
- verify RNA identifier/preprocessing convention;
- preserve tumor/adjacent and AA/EA metadata separately.

**Representation class:** closest current bulk match, but not directly P1-ready.

---

## A2. Lung adenocarcinoma static cross-omic cohort

**Accessions:** `GSE66836` methylation, `GSE66863` expression, BioProject `PRJNA278125`.

### Source facts

- `GSE66836`: 164 lung adenocarcinoma tumors + 19 matched normal lung samples, 450K methylation;
- `GSE66863`: 121 lung adenocarcinoma tumor samples, Agilent expression array;
- GEO explicitly states expression sample numbers are matched between the two series.

Therefore:

```text
SOURCE_DECLARED_MATCHED_TUMOR_SUBSET = 121
```

The remaining methylation tumors/normals are not assumed to have matched expression.

### Current role

- high-priority external `NOMINAL_FUNCTION` candidate;
- useful RNA-platform transport because expression is microarray rather than TCGA RNA-seq.

### Remaining source gates

- mechanically reconstruct the 121-sample cross-modal identity table;
- verify source file identities/hashes;
- define the expression-platform adapter in P0-D/P0-Q before any claim of current-Engine replication.

---

## A3. CGGA `CCell_4083` multi-omic IDH-mutant astrocytoma family

**Sources:** CGGA `CCell_4083`, `OMIX011526`, `OMIX011528`, `OMIX011529`, `HRA012868`, `HRA012903`, public analysis repository `Jihong-Tang/Proteomics_IME`.

### Modality count audit

The CGGA portal's `35 samples` label is **not** a 35-sample complete five-modality intersection.

Verified source-deposit counts:

```text
proteomics = 35
phosphoproteomics = 35
methylation = 29
bulk RNA = 19
scRNA accession title = 18 IDH-mut astrocytomas
scRNA source description = 19 samples containing 21 tumors
```

Therefore:

```text
ALL_FIVE_MODALITIES_COMPLETE_ON_35 = FALSE
EXACT_PAIRWISE_MODALITY_OVERLAP = UNRESOLVED
SC_RNA_SOURCE_COUNT_DISCREPANCY = OPEN
```

Public code confirms the authors used `Cohort_ID` crosswalks between protein-defined cohort metadata and methylation/scRNA layers, but the exact pairwise presence matrix is not exposed by the tracked public code alone.

Dedicated audit:

`artifacts/GRI_CGGA_CCELL4083_MODALITY_AUDIT_P0D_20260911.md`

### Current role

- high-value external multi-layer `NOMINAL_FUNCTION` / Atlas context;
- protein/phosphoprotein context for methylation/RNA architecture;
- bulk-versus-cellular organization comparison.

### Remaining source gate

Build exact `Cohort_ID x modality` presence matrix from processed/controlled manifests. Do not infer an intersection from the maximum arm size.

---

## A4. CGGA legacy methylation/expression families

Portal-level resources include:

```text
methyl_159 = 159 HM27 samples
mRNA-array_301 = 301 samples
RNA-seq cohort = 325 samples
RNA-seq cohort = 693 samples
```

Exact patient overlap is unresolved.

**Status:** `CANDIDATE_MEDIUM_PRIORITY_PENDING_OVERLAP_AUDIT`.

---

## A5. ICGC ARGO family

Potentially useful for independent multi-cancer external validation, but no exact ARGO program has yet been source-qualified as providing the paired methylation + expression structure needed for a current GRI question.

**Status:** `SOURCE_FAMILY_LEAD_ACCESS_AND_MODALITY_AUDIT_REQUIRED`.

---

# B. Paired / ordered bulk perturbation candidates

## B1. Melanoma baseline -> acquired MAPKi resistance

**SuperSeries:** `GSE65186`.  
**SubSeries:** `GSE65183` methylation, `GSE65184` expression array, `GSE65185` RNA-seq.

### Source structure

```text
methylation arrays = 144
expression-array samples = 4
RNA-seq samples = 70
```

After separating assay replicates from biological states and applying only source-metadata-supported naming reconciliations:

```text
unique human methylation states = 63
unique human transcriptome states = 64
shared human patient-states = 61
shared human patient IDs = 19
strict shared baseline + >=1 post-resistance patients = 18
shared cell-model states = 8/8
```

Preserved asymmetries:

```text
methylation-only = Pt14-baseline, Pt14-DP1
transcriptome-only = Pt19-DDP2, Pt24-baseline, Pt24-DDP1
strict paired baseline->post refusal = Pt21
```

Pt21 has shared resistant states but no shared baseline, so it cannot enter a strict baseline-to-post paired analysis under the present source gate.

Dedicated audit:

`artifacts/GRI_MELANOMA_MAPKI_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

### Current role

- very-high-value bulk `PERTURBED_FUNCTION` candidate;
- `BOUNDARY_OR_TRANSITION` state-change mapping;
- repeated-resistance-state Function Map;
- separate 8-state cell-model P0-D mechanism/qualification branch.

### Remaining source gate

Build full patient/state/modality/replicate manifest before any biological computation.

---

## B2. Breast primary tumor -> regional metastasis

**Accessions:** `GSE58999` methylation, `GSE57968` expression, SuperSeries `GSE59000`.  
**Publication:** Reyngold et al., PLoS ONE 2014, PMID 25083786 / PMCID PMC4118917.

### Source structure

```text
methylation = 44 matched patient pairs = 88 samples
expression = 36 matched patient pairs = 72 samples
```

The publication states RNA was available for 36 of the 44 methylation-profiled patient pairs.

Complete title audit:

```text
raw expression/methylation title intersection = 66/72
```

The six raw discrepancies are a terminal-`b` naming asymmetry. Removing only one terminal lowercase `b` diagnostically gives:

```text
terminal-b normalized expression in methylation = 72/72
methylation-extra normalized titles = 16 = 8 patient pairs
```

Several discrepant cases were independently verified at patient/state level. This normalization is **not yet a production identity rule** until the full GSM/patient/state crosswalk is exported.

Dedicated audit:

`artifacts/GRI_BREAST_PAIRED_EXTERNAL_IDENTITY_AUDIT_P0D_20260911.md`

### Current role

- high-value paired `PERTURBED_FUNCTION` source;
- candidate `BOUNDARY_OR_TRANSITION` architecture map;
- RNA-platform transport because expression is microarray.

### Remaining source gate

Export the complete 72-row expression-to-methylation GSM/patient/state crosswalk.

---

## B3. Colorectal primary tumor -> liver metastasis

**Accession:** `GSE213402`.

Source-declared:

```text
patients = 10
samples = 20
paired primary + liver metastasis
methylation = RRBS
RNA = RNA-seq
```

### Current role

- clean paired-state P0-D `PERTURBED_FUNCTION` candidate;
- useful methylation-platform limit case.

### Limitation

Small N and RRBS representation differ materially from the current array-based bulk GRI. A representation adapter is required and cannot confirm itself.

---

## B4. ALK-positive acquired ceritinib-resistance cell-model family

**Accessions:** `GSE139388`, `GSE139387`, `GSE179326`.

Parental versus acquired resistant cell states with methylation/RNA-related measurements.

**Role:** controlled P0-D `PERTURBED_FUNCTION` mechanism/qualification testbed, not population validation.

---

# C. 2026 longitudinal IDH-glioma candidates

These two source families materially improve the v0.7.1A biological perturbation/ordering coverage. They are deliberately kept separate because their measurement architectures are different.

## C1. Nomura et al. 2026 joint single-nucleus DNA methylation + RNA

**Paper:** `Longitudinal changes in DNA methylation in IDH-mutant glioma fuel disease progression through altered cell state differentiation`, Nature Genetics 58, 1651-1660 (2026), DOI `10.1038/s41588-026-02642-7`.

**Processed data:** `GSE292025` XRBS DNA methylation, `GSE291885` Smart-seq2 RNA, `GSE292130` complementary 10x snRNA.  
**Raw human data:** DUOS-000475 / 000476 / 000480.  
**Public code:** `rr1859/sc_DNAme_RNA_GCIMP_Analysis` plus Zenodo code deposit.

### Verified cohort/source structure

```text
total tumors = 36
total patients = 19
longitudinally matched tumors = 32
longitudinally matched patients = 15
unmatched tumors = 4
joint XRBS + Smart-seq2 matched nuclei = 2,117
GSE292025 tumor records = 36
```

The key measurement advantage is direct **same-nucleus joint capture** of DNA methylation and RNA. This is not merely two matched bulk aliquots.

### 10x discrepancy preserved

The paper reports:

```text
10x retained tumors = 32
10x nuclei after QC = 158,143
```

The current `GSE292130` record exposes 31 top-level GEO sample records.

```text
TENX_PAPER_VS_GEO_COUNT_DISCREPANCY = OPEN
```

No missing sample identity is invented.

`GSE291885` top-level `Samples (2)` reflects processed-deposit packaging and must not be interpreted as only two biological tumors.

Dedicated audit:

`artifacts/GRI_IDH_GLIOMA_DUAL_CAPTURE_LONGITUDINAL_SOURCE_AUDIT_P0D_20260911.md`

### Current role

- **very-high-value `PERTURBED_FUNCTION` candidate**;
- **very-high-value `BOUNDARY_OR_TRANSITION` candidate**;
- unique source for reduction-adequacy analysis because same-nucleus structure can be compared with tumor-level aggregation;
- direct testbed for whether similar system-level states hide different nucleus-level/modal organizations.

### Representation firewall

This source is **REPRESENTATION_CHANGING** relative to the current TCGA bulk-array/RNA model. It requires a new P0-D/P0-Q single-nucleus representation or explicit aggregation model before any GRI scientific evaluation. Such an adapter cannot confirm itself on the same evidence.

### Remaining source gates

- reconstruct the exact 36-tumor patient/order table;
- verify the 32 matched tumors/15 patients from source metadata;
- reconstruct the 2,117-nucleus methylation↔RNA pairing schema;
- resolve or preserve the 32-paper-versus-31-GEO 10x discrepancy;
- inventory treatment/exposure between paired surgeries.

---

## C2. CARE IDH-mutant longitudinal multi-omic cohort

**Paper:** `Acquired genetic and cell-state changes in IDH-mutant glioma progression`, Nature 655, 1048-1059 (2026), DOI `10.1038/s41586-026-10612-6`.

**Public code:** `Kcjohnson/care_idh_mut`, `Kcjohnson/care-glass`.  
**Public/controlled sources:** `GSE326221` snRNA, `GSE327580` Multiome ATAC, Synapse CARE processed resources, EGA/DUOS controlled sequencing.

### Verified longitudinal structure

```text
total tumors = 75
total patients = 35
oligodendroglioma patients = 13
astrocytoma patients = 22
timepoints = 2 or 3 per patient
main longitudinal patient pairs = 35
initial sample at primary diagnosis = 17/35
initial sample at later surgery = 18/35
treated between main pair = 26/35
no reported adjuvant treatment between main pair = 9/35
```

`initial` therefore must not be silently equated with treatment-naive primary diagnosis.

### Exact Multiome patient/timepoint gate

The complete `GSE327580` title list contains exactly 48 ATAC records and resolves to 22 unique patients. Every one has T1 and T2. Four also have T3.

```text
22 patients x T1/T2 = 44 records
+ T3 for patients 59, 100, 105, 111 = 4 records
TOTAL = 48
MULTIOME_PATIENT_TIMEPOINT_IDENTITY_GATE = PASS
```

The 22 patient IDs are:

```text
57, 59, 60, 61, 71, 73, 79, 80, 81, 85, 91,
100, 101, 103, 104, 105, 106, 107, 108, 109, 110, 111
```

This independently reconstructs the paper's 22 matched longitudinal Multiome pairs at deposit level while preserving third timepoints.

A separate Smart-seq2 branch contains 16 tumors.

### DNA-methylation source gap

DNA methylation is genuinely present in the study:

- the paper's sample-availability landscape includes DNA methylation;
- DNA-methylation arrays are used in a specific genomic validation context;
- public CARE code contains a `Bulk DNA methylation` data-availability class.

But:

```text
BULK_DNA_METHYLATION_EXACT_SAMPLE_COUNT = UNRESOLVED
BULK_DNA_METHYLATION_PUBLIC_ACCESSION = UNRESOLVED
BULK_DNA_METHYLATION_PAIRWISE_OVERLAP_WITH_RNA = UNRESOLVED
```

The paper's public Data Availability section names snRNA/ATAC and DNA-sequencing resources but not a dedicated bulk-methylation accession. The public code reads a curated `genomic_data_availability_all.csv` that is not tracked in the public repository.

No methylation count is inferred from a figure and no accession is invented.

Dedicated audit:

`artifacts/GRI_CARE_IDH_LONGITUDINAL_MULTIOMIC_SOURCE_AUDIT_P0D_20260911.md`

### Current role

- **very-high-value `PERTURBED_FUNCTION` source** with richer clinical/treatment/genetic context than C1;
- **very-high-value `BOUNDARY_OR_TRANSITION` source**;
- 48-tumor RNA+ATAC state-change subset with 22 exact deposited longitudinal pairs;
- useful treatment-context Function Map.

### Representation firewall

This is a multi-layer representation-changing family, not a direct drop-in current-Engine replication. Bulk methylation remains unresolved, and snRNA/ATAC/bulk RNA/Smart-seq2 must not be collapsed into one input representation by convenience.

### Remaining source gates

- reconstruct full 75-sample snRNA patient/timepoint table;
- retain the closed 48-sample/22-patient Multiome identity gate;
- locate or explicitly close as unavailable the bulk methylation sample/accession path;
- reconstruct treatment and diagnosis-versus-later-surgery metadata from source tables;
- preserve all third timepoints even if a later frozen question focuses on T1/T2.

---

# D. Current source-architecture ranking

This ranking is for **P0-D planning only**. It does not choose a P1 validation cohort.

## Static / closest-to-current GRI

| Priority | Source | Why it is useful | Main unresolved gate |
|---|---|---|---|
| 1 | Prostate `GSE262522 + GSE262524 + GSE237995` | exact 121/121 cross-modal identity; bulk RNA; dual 450K/EPIC platform test | source files/hashes + shared-probe reconstruction |
| 2 | LUAD `GSE66836 + GSE66863` | 121 source-declared matched tumors; 450K methylation | exact sample table + RNA microarray adapter |
| 3 | `CCell_4083` | methylation/RNA/protein/phosphoprotein/scRNA in one external study family | exact pairwise modality matrix |
| 4 | CGGA legacy | larger historical glioma cohorts | exact methylation-expression overlap |

## Perturbed / ordered biological-state mapping

| Priority | Source | Why it is useful | Main unresolved gate |
|---|---|---|---|
| 1 | Nomura IDH glioma 2026 | direct same-nucleus methylation+RNA, 15 longitudinal patients | new single-nucleus representation + exact source manifest |
| 2 | CARE IDH glioma 2026 | 35 longitudinal patients, 75 tumors, rich treatment/genetic context, exact 22-patient RNA+ATAC Multiome subset | bulk-methylation source path + full modality table |
| 3 | Melanoma `GSE65186` | 18 strict baseline-to-resistance cross-modal patients, repeated resistant biopsies | full patient/state/modality manifest |
| 4 | Breast `GSE59000` family | 36 source-declared paired cross-omic primary/metastasis patients | final 72-row production-style crosswalk |
| 5 | Prostate family | tumor/adjacent and platform perturbation context | source files/probe gate |
| 6 | CRC `GSE213402` | clean paired primary/metastasis RRBS+RNA | n=10 and RRBS representation |
| 7 | ALK resistance family | controlled acquired-resistance cell model | condition/modality manifest |

Nomura and CARE move ahead of melanoma **for the biological-ordering program** because they provide independent 2026 longitudinal glioma cohorts with stronger within-patient temporal structure. This ranking change is based on source architecture alone, not GRI outcome performance.

The two IDH cohorts are complementary rather than interchangeable:

- **Nomura:** cleaner direct methylation↔RNA coupling at the same-nucleus level.
- **CARE:** larger longitudinal cohort and richer treatment/genetic/RNA+ATAC context, but methylation source path currently unresolved.

---

# E. Rare-natural-limit status

No external source in this inventory is promoted to a P1 rare-natural testbed merely because the disease or state is unusual.

Separately, existing TCGA PCPG is source-qualified as a **post-result P0-D rare-natural limit testbed** in:

`artifacts/GRI_PCPG_RARE_NATURAL_TESTBED_P0D_20260910.md`

It remains nonrepresentative, nonconfirmatory, and carries open promotion debt.

---

# F. Immediate safe P0-D source sequence

1. reconstruct the Nomura 36-tumor longitudinal identity/order table and 2,117-nucleus cross-modal pairing schema;
2. reconstruct CARE's full 75-sample patient/timepoint source table and continue searching for the bulk-methylation accession/manifest without inferring it;
3. finish the breast 72-row GSM/patient/state crosswalk;
4. build the melanoma full patient/state/modality/replicate manifest;
5. obtain `CCell_4083` processed manifests and build the exact `Cohort_ID x modality` presence matrix;
6. verify prostate files/hashes and independently reconstruct the 449,636 shared-probe platform gate;
7. reconstruct the LUAD 121-sample identity table;
8. retain every access/identity/modality failure in the ledger rather than silently replacing it with a more convenient source.

None of these steps opens an external GRI scientific outcome or chooses a decisive P1 cohort.

**Current source-program state:** external source discovery has moved from generic candidate hunting to source-qualified coverage across static function, real paired/ordered perturbation, multi-layer context, and known representation boundaries. The next scientific transition remains a deliberate freeze, not an automatic consequence of finding better data.
