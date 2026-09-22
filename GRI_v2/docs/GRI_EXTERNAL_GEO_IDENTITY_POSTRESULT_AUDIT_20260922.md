# GRI external GEO identity freeze post-result audit - 22 September 2026

**Status:** COMPLETE SOURCE-IDENTITY / NO BIOLOGICAL OUTCOME OPENED  
**Program authority:** SymC General Operations Manual v0.8.3  
**Canonical branch:** `gri-conglomerate-v1-integration-20260921`  
**Workflow run:** `35733020358`  
**Artifact:** `GRI_EXTERNAL_GEO_SOURCE_MANIFEST_SET_V01`  
**Artifact ID:** `10696736434`  
**Artifact ZIP SHA-256:** `f133746616509943ba385f4964b70ee66e4c3b8c028c909ef98382e61a362d36`

## Purpose

Close source-identity and sample-crosswalk gaps for the already-audited breast, prostate, and melanoma external candidate families without computing any GRI feature, selecting a P1 cohort, or opening an outcome-bearing test.

The run freezes exact GEO MINiML archive/XML identities and derives only mechanical identity tables from source metadata.

## Breast paired source family

Sources:
- GSE57968 expression;
- GSE58999 methylation.

Result:
- 72/72 expression samples matched exactly to one methylation sample by source-declared patient ID plus primary/metastasis state;
- 36 complete expression patient pairs;
- 16 methylation-only samples remain outside the paired expression crosswalk;
- no biological GRI quantity was computed.

Production crosswalk identities:
- `breast_crosswalk.csv` SHA-256 `bac049aa1b0ef99c8929e7ea515699b850b908b1b169bc888a85189f9ef0dfb9`
- `breast_crosswalk.json` SHA-256 `3003ff7e35c7847eaae5b0c19241f6e87975b77276856a62b72bab01a2caf258`

Disposition:
`BREAST_SOURCE_IDENTITY_CROSSWALK = CLOSED_FOR_METADATA_SCOPE`.

This does not select breast as the P1 cohort and does not establish representation compatibility for the new carrier.

## Prostate cross-modality source family

Sources:
- GSE237995 RNA-seq;
- GSE262522 450K methylation;
- GSE262524 EPIC methylation.

Result:
- 121/121 RNA samples matched exactly one methylation sample by source title;
- 68 matches use 450K;
- 53 matches use EPIC;
- no collisions were detected in the frozen matching rule;
- no biological GRI quantity was computed.

Production crosswalk identities:
- `prostate_crosswalk.csv` SHA-256 `620f532cd3578d0deedbc08b42176e9f6c7a05c7249fe7ec6a7edca21bd82947`
- `prostate_crosswalk.json` SHA-256 `585d5657e5d4f78a16892bad905cd9395475a5b2936178d1d71b4fa1b16f86fa`

Disposition:
`PROSTATE_SOURCE_IDENTITY_CROSSWALK = CLOSED_FOR_METADATA_SCOPE`.

Platform harmonization/shared-probe and preprocessing compatibility remain later representation questions. This run does not answer them.

## Melanoma MAPKi source family

Sources:
- GSE65183 methylation;
- GSE65184 expression array;
- GSE65185 RNA-seq.

Result:
- 218 source samples inventoried;
- 192 source rows parse as human-patient records under the frozen title rule;
- 26 source rows are retained as cell-model records;
- three title-versus-description patient-identity conflicts were found and preserved.

Conflicting source records:

| GSM | title | description | disposition |
|---|---|---|---|
| GSM1588907 | Pt22-DDP1 | Patient 21 melanoma, post BRAFi+MEKi resistance, 1st biopsy | QUARANTINE |
| GSM1588908 | Pt22-DDP2 | Patient 21 melanoma, post BRAFi+MEKi resistance, 2nd biopsy | QUARANTINE |
| GSM1588909 | Pt22-DDP3 | Patient 21 melanoma, post BRAFi+MEKi resistance, 3rd biopsy | QUARANTINE |

Production manifest identities:
- `melanoma_source_manifest.csv` SHA-256 `abaf177c92efeecc414e4c8c5ccecfdb1acd07c479cff8983e3cab084c7a3f32`
- `melanoma_source_manifest.json` SHA-256 `0f76b9b1e27eed1cb353b129e234184401150fbcd51487058a7c996097fc1a78`

Disposition:
`MELANOMA_SOURCE_MANIFEST = COMPLETE_WITH_IDENTITY_ANOMALIES`.

The three conflicts may not be silently resolved from the sample title. A future melanoma task must either resolve the discrepancy from primary/source records prospectively or exclude/quarantine those records under a frozen rule.

## GEO source archive identities

The run also froze exact MINiML archive/XML SHA-256 values for all eight source series. These identities are stored in the uploaded artifact and are source/provenance records only.

## Scientific firewall

This run:
- computed no GRI feature;
- created no lowercase chi;
- created no capital-Chi score;
- selected no P1 cohort;
- inspected no diagnostic/predictive endpoint;
- changed no scientific threshold.

## Next gate

Mechanical identity is now sufficiently closed to design a future external task without discovering sample-join defects afterward.

Before any external outcome-bearing test:
1. choose the claim/task;
2. freeze representation compatibility;
3. freeze cohort inclusion/exclusion and handling of source anomalies;
4. freeze standard/native comparators;
5. freeze falsifier/effect-size rule;
6. complete MFR-14;
7. only then open decisive outcomes.
