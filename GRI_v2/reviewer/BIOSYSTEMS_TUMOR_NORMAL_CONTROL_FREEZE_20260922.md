# BioSystems tumor-versus-normal control freeze - 22 September 2026

**Status:** PROSPECTIVE / OUTCOME-SEALED  
**Revision branch:** `gri-biosystems-revision-20260922`  
**Canonical science parent:** `gri-conglomerate-v1-integration-20260921`  
**Purpose:** answer the reviewer request for normal controls without changing the frozen tumor architecture after seeing normal molecular outcomes.

## 1. Scientific question

Do the static RNA and methylation-transcriptomic architecture signals reported in TCGA primary tumors also appear in TCGA Solid Tissue Normal samples from the same disease programs, and if so, with what magnitude and representation dependence?

This is a specificity/control question. It does not assume that tumor values are larger, smaller, more stable, less stable, or otherwise directionally ordered in advance.

## 2. Source firewall

Primary comparison uses the same PanCanAtlas source family already used in the rebuild:

- RNA: `EBPlusPlusAdjustPANCAN_IlluminaHiSeq_RNASeqV2.geneExp.tsv`
- methylation: `jhu-usc.edu_PANCAN_merged_HumanMethylation27_HumanMethylation450.betaValue_whitelisted.tsv`

TCGA sample-type codes are interpreted prospectively as:
- `01` = Primary Solid Tumor;
- `11` = Solid Tissue Normal.

No GTEx samples enter the primary analysis because cross-program/platform harmonization would add a new batch/source axis. GTEx may be considered later only as a separately frozen sensitivity or external healthy-reference analysis.

TCGA Solid Tissue Normal is treated as tumor-adjacent/non-tumor reference tissue where applicable, not as a universal healthy-population reference. Field effects, microenvironmental influence, occult tumor contamination, and tissue-composition differences remain explicit limitations.

## 3. TN-C0 metadata-only eligibility gate

Before reading any normal molecular values:

1. parse exact RNA and methylation column/sample identifiers;
2. extract TCGA participant, sample-type, aliquot and cancer/project identity;
3. inventory unique-patient counts for sample types 01 and 11 by cancer;
4. inventory exact RNA+methylation same-patient overlap for 01 and 11;
5. resolve duplicate aliquots by deterministic source/quality rules only;
6. write the eligibility table and cryptographic/source identities;
7. do not calculate expression, methylation, CKA, Hallmark, prediction, tumor-normal effect, or any biological statistic.

Eligibility thresholds below are frozen before TN-C0 outcome inspection.

## 4. Primary multiomic tumor-normal control

A cancer enters the **primary TN-C1 comparison** only when both tumor and normal groups contain at least 30 unique patients with one-to-one eligible RNA+methylation representation after the frozen identity rules.

The inherited fixed sample size is:
- `n = 30` tumor;
- `n = 30` normal;
- 100 deterministic without-replacement draws per group where the group contains >30 participants.

The use of n=30 preserves the finite-sample calibration already established in Stage A1.1 rather than introducing a new normal-specific sample-size regime.

No cancer is rescued by lowering the 30-sample floor after the metadata inventory is opened.

## 5. Primary TN-C1 quantities

The normal analysis mirrors the current static C1 construction wherever the source representation permits it.

For each eligible cancer and tissue state, retain the existing C1 families:

- H1: within-methylation organization relative to its frozen construction/null floor;
- H2: global methylation-RNA patient-geometry correspondence;
- H3a: patient-specific cross-layer Hallmark coupling;
- H3b: same-Hallmark semantic-label advantage;
- primary publication and masked-technical tracks;
- prespecified purity/leukocyte adjustment only where the covariates are valid and available for that tissue state.

The control question is not whether normals “pass” the tumor promotion ladder. The primary contrast is the **paired cancer-level tumor-minus-normal effect** for each admitted quantity under identical construction.

## 6. Primary inference

For every quantity:

1. report cancer-level tumor and normal estimates side by side;
2. report tumor-minus-normal effect sizes with uncertainty from the fixed draws;
3. use cancer as the inferential unit, not resample draw;
4. use a two-sided paired cancer-level test because no direction is prespecified;
5. preserve sign, magnitude, heterogeneity and individual cancer exceptions;
6. apply multiplicity control across the small prespecified primary family rather than across post-hoc subgroups.

A statistically null tumor-minus-normal contrast is scientifically admissible and must not be rescued by changing thresholds, cancers, Hallmarks or representations.

## 7. Broader RNA-only coverage control

Because normal methylation overlap may be sparse, a second **coverage control** is frozen independently.

A cancer is eligible for RNA-only TN-A1 when it has:
- >=30 unique primary-tumor RNA samples;
- >=30 unique Solid Tissue Normal RNA samples.

TN-A1 uses the already frozen Stage A / A1.1 RNA construction:
- identical source transformation;
- identical Hallmark library;
- identical eligibility rules;
- n=30 balanced draws;
- 100 deterministic draws;
- the same static RNA coordinates `C_in,pair`, `C_in,PC1`, and `C_out`.

This broader analysis asks whether the RNA architecture that seeded the rebuild is generic to tissue, shifted in tumor, or heterogeneous by cancer.

It cannot substitute for the primary multiomic normal control when the latter is eligible.

## 8. Paired-patient sensitivity

Where at least 20 participants have both sample type 01 and sample type 11 RNA from the same patient, a paired-patient sensitivity may be run using the frozen participant mapping.

This is sensitivity evidence only because paired normal availability is non-random and cancer-specific.

No paired threshold is lowered after counts are known.

## 9. Composition and adjacent-normal limitations

The analysis will not call sample type 11 “healthy control” without qualification.

The manuscript must state that TCGA adjacent/solid-tissue normals may carry:
- field cancerization;
- tumor-associated microenvironmental changes;
- occult tumor contamination;
- tissue-composition differences from tumor;
- selection bias because normal collection differs sharply by cancer.

Therefore:
- a tumor-normal difference supports tumor association, not necessarily tumor-cell intrinsic causality;
- a null difference does not prove the architecture is artifactual, because adjacent normal tissue can share disease-field structure;
- GTEx/independent healthy tissue remains a distinct later sensitivity question.

## 10. Promotion rules

Possible outcomes are predeclared:

### TN-SPECIFIC
The tumor architecture differs reproducibly from same-cancer normal reference under the frozen primary quantity.

### TN-SHARED_WITH_SHIFT
The architecture exists in both states but differs quantitatively.

### TN-SHARED_NO_RESOLVED_SHIFT
Both states show similar architecture and the frozen comparison does not resolve a tumor-specific shift.

### TN-HETEROGENEOUS
Direction or magnitude materially differs across cancers.

### TN-NOT_EVALUABLE
Coverage, representation or covariate requirements fail.

None of these states may be renamed after results are known.

## 11. Relationship to internal and external validation

This tumor-normal control is **not** independent external validation. It is an internal same-program specificity/control analysis using TCGA source material.

The revised paper will distinguish three separate evidentiary functions:

1. **internal held-out validation:** DISCOVERY -> REPLICATION -> FINAL_HOLDOUT within TCGA;
2. **tumor-versus-normal specificity control:** sample type 01 versus sample type 11 under the present freeze;
3. **genuinely independent confirmation:** future untouched external cohort under a separately frozen MFR-14-compatible transport design.

These three layers are complementary and must not be collapsed into one use of the word “validation.”

## 12. Stop boundary

The next safe action is TN-C0 metadata-only inventory.

Do not open normal molecular values until:
- this freeze is committed;
- exact source identities are bound;
- the metadata inventory script is contract-tested to demonstrate that it cannot calculate biological outcomes.
