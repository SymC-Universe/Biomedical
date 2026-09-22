# BioSystems tumor-versus-normal source-gate audit - 22 September 2026

**Status:** CLOSED SOURCE/IDENTITY GATE; NO BIOLOGICAL VALUES OPENED  
**Workflow:** GRI BioSystems tumor-normal source gate  
**Run:** 35774748332  
**Artifact:** GRI_BIOSYSTEMS_TUMOR_NORMAL_SOURCE_GATE_V01, artifact 10714969175  
**Artifact digest:** sha256:75ff6f0af67be78f1ce88cbb4680739ae8b52adc3b9c03c585dad26e6c8e5a8d

## Frozen source identities

- RNA: PanCanAtlas `EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.tsv`, exact source lineage SHA-256 `674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658`.
- Methylation: PanCanAtlas merged HM27/HM450 source, exact source lineage SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`.
- Sample type 01 = Primary Solid Tumor.
- Sample type 11 = Solid Tissue Normal.

The gate read source headers and GDC case/project identity only. It did not read RNA or methylation molecular values, calculate features, fit a model, or select cancers from biological outcomes.

## Global source inventory

- RNA header: 11,069 sample columns.
  - type 01: 9,704 columns; 9,700 unique patients with one root.
  - type 11: 737 columns; 737 unique patients with one root.
- methylation header: 12,039 sample columns.
  - type 01: 10,271 columns; 10,265 unique patients with one root.
  - type 11: 1,066 columns; 1,066 unique patients with one root.
- no unparsed header labels.
- no GDC patient-to-project conflicts.
- no type-11 duplicate sample roots in either modality.

## Primary paired-control feasibility

The strongest control is participant-paired tumor versus normal using the same patient, with both sample type 01 and sample type 11 present in both RNA and methylation.

The prospectively chosen primary analysis requires at least 20 complete cross-modal pairs so the existing RNA minimum-finite-sample rule remains usable without inventing a post-result exception.

**Primary paired n=20 cancers (9):**

| Cancer | Complete paired cross-modal participants |
| --- | ---: |
| BRCA | 94 |
| COAD | 28 |
| HNSC | 20 |
| KIRC | 23 |
| KIRP | 23 |
| LIHC | 41 |
| PRAD | 35 |
| THCA | 50 |
| UCEC | 22 |

BLCA (17) and LUAD (19) pass the earlier source-only n=15 screen but are below the final n=20 primary floor and will not be rescued into the primary analysis.

## High-sample unpaired corroboration

A secondary equal-size project-matched control retains the original C1 fixed-n=30 scale but does not require the same patient to supply tumor and normal tissue.

**n=30 cross-modal tumor/normal cancers (5):** BRCA, LIHC, PRAD, THCA, UCEC.

This track is secondary because participant pairing is a stronger control of between-person heterogeneity.

## Source-only exclusions are not biological failures

Cancers with fewer normals or cross-modal normal mismatches are excluded from the control only because the exact source does not support the frozen sample-size rule. No biological result has been used to include, exclude, or reclassify a cancer.

## Next gate

Freeze the exact paired n=20 and corroborating n=30 computations, null streams, feature-intersection rules, effect definitions, multiplicity and refusal logic before opening any normal molecular values.
