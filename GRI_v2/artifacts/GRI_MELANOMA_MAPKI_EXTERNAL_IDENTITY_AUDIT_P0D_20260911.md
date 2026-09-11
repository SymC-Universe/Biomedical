# GRI melanoma MAPKi ordered external identity audit

**Date:** 2026-09-11  
**Mode:** P0-D SOURCE / IDENTITY / ORDERING QUALIFICATION  
**Scientific GRI outcome evaluation:** NONE  
**P1 selection/freeze:** NO

## Source family

Study: `Non-genomic and Immune Evolution in Melanoma with Acquired MAPKi Resistance`

GEO SuperSeries: `GSE65186`

SubSeries:

- `GSE65183` — Illumina HumanMethylation450;
- `GSE65184` — Affymetrix Human Gene 2.1 ST expression array;
- `GSE65185` — Illumina HiSeq 2000 RNA-seq.

BioProject family: `PRJNA273358` with modality-specific child records.

## Source structure

The SuperSeries contains 218 GEO samples in total:

```text
METHYLATION_ARRAY_SAMPLES = 144
EXPRESSION_ARRAY_SAMPLES = 4
RNASEQ_SAMPLES = 70
TOTAL = 218
```

The source title structure reveals two scientifically distinct groups that must remain separate:

1. human melanoma biopsies sampled before treatment and after acquired resistance;
2. melanoma cell-model conditions.

## Methylation identity structure

The methylation arm contains:

```text
HUMAN_METHYLATION_ARRAYS = 126
CELL_MODEL_METHYLATION_ARRAYS = 18
```

The 126 human arrays resolve into **63 unique patient-state identities**, with two methylation technical/assay replicates per state.

The 18 cell-model arrays resolve into **8 unique condition identities**, with 2-3 methylation replicates depending on condition.

No replicate is counted as a distinct patient or distinct biological timepoint.

## Transcriptome identity structure

### RNA-seq

The RNA-seq series contains 70 samples:

```text
HUMAN_RNASEQ_STATES = 62
CELL_MODEL_RNASEQ_STATES = 8
```

### Expression array

The expression-array series contains four Pt7 samples:

```text
Pt7-baseline
Pt7-baseline.replicate
Pt7-DP1
Pt7-DP1.replicate
```

These collapse to two human biological states:

```text
Pt7-baseline
Pt7-DP1
```

Pt7 therefore has transcriptome coverage through the expression-array branch rather than the RNA-seq branch.

Across RNA-seq plus expression array, the source family contains **64 unique human transcriptome patient-state identities**.

## Source-metadata-supported title reconciliation

Cross-modality matching was performed only after replicate/state naming was separated from patient/timepoint identity.

### Allowed mechanical reconciliation 1: methylation technical replicate suffix

For methylation human biopsy titles:

```text
PtX-STATE-1
PtX-STATE-2
```

are source-described assay replicates of one patient biopsy state.

The final `-1` / `-2` is therefore removed for the source identity comparison only after replicate status is established.

### Allowed mechanical reconciliation 2: `DD-DP` versus `DDP`

Methylation titles use forms such as:

```text
Pt18-DD-DP1-1
```

while RNA-seq uses:

```text
Pt18-DDP1
```

GEO metadata for both identifies patient 18, post BRAFi+MEKi resistance, first biopsy. Equivalent metadata are present for the corresponding double-drug resistant branches in other patients.

Therefore `DD-DP#` and `DDP#` are treated as source naming variants at the identity-audit layer.

### Allowed mechanical reconciliation 3: Pt10 `baseline2` and Pt22 `baseline1`

Methylation titles include:

```text
Pt10-baseline2-1 / -2
Pt22-baseline1-1 / -2
```

GEO descriptions identify both as the respective patient's **pre-MAPKi treatment, first biopsy**. RNA-seq titles `Pt10-baseline` and `Pt22-baseline` are independently described as the same patients' pre-MAPKi first biopsies.

Therefore the trailing `1`/`2` embedded in these two source baseline labels is treated as a source label variant for this cross-modality identity audit, not as a different biological state.

No broader numeric-title stripping rule is inferred from these two cases.

## Cross-modality human-biopsy result

After only the source-supported reconciliations above:

```text
UNIQUE_METHYLATION_HUMAN_STATES = 63
UNIQUE_TRANSCRIPTOME_HUMAN_STATES = 64
SHARED_METHYLATION_TRANSCRIPTOME_HUMAN_STATES = 61
SHARED_PATIENT_IDS = 19
```

Methylation-only human states:

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

Thus the source family is highly overlapping but **not** a complete one-to-one modality bijection.

## Paired ordered-state support

Among the 19 patients with at least one shared methylation/transcriptome state:

```text
PATIENTS_WITH_SHARED_BASELINE_AND_AT_LEAST_ONE_SHARED_POST_RESISTANCE_STATE = 18
```

Those patients are:

```text
Pt1, Pt2, Pt3, Pt4, Pt5, Pt6, Pt7, Pt8, Pt9, Pt10,
Pt15, Pt16, Pt17, Pt18, Pt19, Pt20, Pt22, Pt23
```

Patient `Pt21` has shared resistant states but no shared baseline in the source family and therefore cannot be treated as a paired baseline-to-resistance case under a strict two-state gate.

The shared-state architecture is not uniform. Some patients have one post-resistance biopsy; others have multiple ordered resistant biopsies. For example Pt10 has baseline plus DP1-DP9 shared across methylation and RNA-seq.

A future analysis must therefore preserve patient and state hierarchy rather than pretending every row is independent.

## Cell-model cross-modality result

After collapsing methylation replicate suffixes, the eight cell-model condition identities match the RNA-seq condition titles exactly:

```text
METHYLATION_CELL_MODEL_STATES = 8
RNASEQ_CELL_MODEL_STATES = 8
SHARED_CELL_MODEL_STATES = 8
METHYLATION_ONLY = 0
RNASEQ_ONLY = 0
```

These cell-model states remain a separate P0-D mechanism/qualification family and are not pooled with human biopsy evidence.

## v0.7.1A interpretation

This source family provides unusually useful coverage of an existing GRI gap:

### `PERTURBED_FUNCTION`

Strong candidate. It contains source-ordered baseline and acquired-resistance states within the same patients.

### `BOUNDARY_OR_TRANSITION`

Candidate for state-change/representation-boundary mapping, but two or several biopsy states do **not** automatically establish a continuous dynamical trajectory, tipping point, critical slowing, recovery law, or exceptional-point crossing.

### Function Map questions it can support in P0-D

- which scalar/modal/conglomerate/cross-layer features are preserved under acquired resistance;
- which features redistribute rather than disappear;
- whether multiple resistance states within a patient traverse similar or distinct architecture regions;
- whether global geometry remains stable while module/modal organization changes;
- whether different treatment contexts occupy different supported regions.

### Limit Map questions it can support in P0-D

- which current GRI representations cease to transport across acquired resistance;
- whether reduction adequacy degrades before global failure;
- whether specific patient/state structures should produce partial admission or refusal;
- whether transcriptome-platform differences alter cross-layer interpretability.

## Important nonclaims

This source audit does not:

- inspect GRI architecture values in any external melanoma sample;
- make the cohort a P1 confirmation set;
- freeze any GRI prediction or threshold;
- treat post-resistance state labels as proof of causal methylation-to-RNA regulation;
- infer continuous dynamics from discrete biopsies;
- admit biological chi;
- use the published biological findings as a test of GRI;
- pool human biopsies and cell-model evidence.

## Current state

```text
RESEARCH_STATUS = P0_D_SOURCE_QUALIFIED_ORDERED_PERTURBATION_CANDIDATE
TOTAL_GEO_SAMPLES = 218
METHYLATION_SAMPLES = 144
EXPRESSION_ARRAY_SAMPLES = 4
RNASEQ_SAMPLES = 70
UNIQUE_HUMAN_METHYLATION_STATES = 63
UNIQUE_HUMAN_TRANSCRIPTOME_STATES = 64
SHARED_HUMAN_PATIENT_STATES = 61
SHARED_HUMAN_PATIENT_IDS = 19
STRICT_SHARED_BASELINE_PLUS_POST_PATIENTS = 18
SHARED_CELL_MODEL_STATES = 8_OF_8
GRI_OUTCOME_STATUS = UNOPENED
P1_STATUS = NOT_SELECTED_NOT_FROZEN
```

## Next mechanical source gate

Before any future biological GRI computation:

1. export a sample-level source manifest for all 218 GSM records;
2. record patient/model ID, biological state, treatment class, biopsy order, modality, and replicate status;
3. explicitly refuse Pt21 from strict baseline-to-post paired analyses unless a justified source rule says otherwise;
4. preserve Pt14 and Pt24 modality-only states rather than dropping them silently;
5. preserve Pt19-DDP2 as transcriptome-only;
6. freeze the exact human versus cell-model analysis role separately;
7. only after the source manifest is complete decide whether the family is used for P0-D mapping, Atlas construction, or a separately designed future P1 test.
