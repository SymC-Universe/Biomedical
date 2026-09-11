# GRI breast paired primary/metastasis external identity audit

**Date:** 2026-09-11  
**Mode:** P0-D SOURCE / IDENTITY QUALIFICATION  
**Scientific GRI outcome evaluation:** NONE  
**P1 selection/freeze:** NO

## Source family

Study: `Methylome remodeling in regional breast cancer metastasis`

Source series:

- `GSE58999` — Illumina HumanMethylation450;
- `GSE57968` — Affymetrix U133A 2.0 expression;
- `GSE59000` — SuperSeries joining the two branches;
- published study: Reyngold et al., PLoS ONE 2014, PMCID PMC4118917 / PMID 25083786.

## Source-declared paired design

The methylation source contains:

- 44 matched primary breast tumors and regional/lymph-node metastases;
- 88 methylation samples total.

The expression source contains:

- 36 matched primary breast tumors and regional/lymph-node metastases;
- 72 expression samples total.

The published study states that RNA from frozen primary tumor and matched regional metastasis was available for **36 patients of the 44 pairs used for methylation profiling**.

Therefore the expression cohort is source-declared as a patient-pair subset of the methylation cohort.

## Raw GEO title audit

The complete SuperSeries sample lists expose the following source title counts:

```text
EXPRESSION_TITLE_COUNT = 72
METHYLATION_TITLE_COUNT = 88
RAW_EXPRESSION_METHYLATION_TITLE_INTERSECTION = 66
RAW_EXPRESSION_ONLY_TITLES = 6
```

The six expression-only raw title strings are:

```text
33
67
95b
96b
99b
100b
```

The corresponding methylation source contains:

```text
33b
67b
95
96
99
100
```

Thus all six raw mismatches are explainable by one source-naming feature: presence/absence of a terminal `b`.

## Conservative normalized-title crosswalk

For source-audit purposes only, define the diagnostic normalization:

```text
normalized_title = raw_numeric_title with one terminal lowercase 'b' removed if present
```

No other character substitution, fuzzy matching, edit-distance matching, patient inference, row-order matching, or biological-value matching is allowed.

Under that single diagnostic normalization:

```text
NORMALIZED_EXPRESSION_TITLE_COUNT = 72
NORMALIZED_EXPRESSION_IN_METHYLATION = 72_OF_72
NORMALIZED_EXPRESSION_ONLY = 0
METHYLATION_EXTRA_NORMALIZED_TITLES = 16
```

The 16 extra methylation titles correspond to eight methylation-only patient pairs, consistent with the source-declared 44-versus-36 patient-pair design.

## Direct metadata checks on suffix-discrepant cases

Source metadata independently verifies several of the terminal-`b` discrepancies at patient/state level:

- RNA title `33` and methylation title `33b` identify patient `R`, primary tumor;
- RNA title `67` and methylation title `67b` identify patient `AI`, primary tumor;
- RNA title `95b` and methylation title `95` identify patient `AX`, primary tumor;
- RNA title `99b` and methylation title `99` identify patient `AO`, primary tumor;
- RNA title `100b` and methylation title `100` identify patient `AO`, lymph-node metastasis.

The series-level study design and published 36-of-44 subset statement are consistent with the same interpretation for the remaining title pair `96b` versus `96`, but a full per-GSM patient/state export has not yet been reconstructed in this repository artifact.

## Identity disposition

Two gates are deliberately distinguished:

### Source-cohort subset gate

`SOURCE_CROSS_MODALITY_PATIENT_SUBSET = PASS`

Reason: the primary source explicitly states that expression was obtained from 36 of the 44 methylation-profiled matched patient pairs.

### Exact production-style per-sample identity gate

`PER_SAMPLE_GSM_PATIENT_STATE_CROSSWALK = PENDING_FINAL_MECHANICAL_EXPORT`

Reason: the raw title lists require a documented terminal-`b` naming reconciliation in six samples, and the full 72-row patient/state crosswalk has not yet been committed as a source table.

The normalized 72/72 result is therefore strong source qualification but is **not silently promoted into a final Engine identity rule**.

## Potential v0.7.1A role

This cohort is especially useful because it contains paired natural states rather than only unrelated cross-sectional patients.

Candidate roles:

- `PERTURBED_FUNCTION`: primary tumor -> regional metastasis;
- `BOUNDARY_OR_TRANSITION`: architecture reorganization across a clinically meaningful paired state change, without inferring a continuous dynamical transition from two observations;
- Function Map: preservation versus redistribution of scalar/modal/conglomerate/cross-layer organization;
- Limit Map: identify components that fail to transport between the paired states;
- possible future Atlas reference family after a frozen source/preprocessing gate.

## Important nonclaims

This audit does not:

- inspect any GRI output or biological effect in the cohort;
- select the cohort for decisive P1 confirmation;
- turn primary/metastasis pairing into a time-resolved dynamical trajectory;
- infer causality;
- admit biological chi;
- use the original paper's biological conclusions as GRI confirmation;
- define a new GRI sample-identity normalization rule for production analysis.

## Current state

```text
RESEARCH_STATUS = P0_D_SOURCE_QUALIFIED_PERTURBED_FUNCTION_CANDIDATE
SOURCE_PAIR_DESIGN = 44_METHYLATION_PAIRS_36_EXPRESSION_PAIRS
SOURCE_CROSS_MODALITY_PATIENT_SUBSET = PASS
RAW_TITLE_MATCH = 66_OF_72
TERMINAL_B_NORMALIZED_TITLE_MATCH = 72_OF_72
PER_SAMPLE_GSM_PATIENT_STATE_CROSSWALK = PENDING_FINAL_MECHANICAL_EXPORT
GRI_OUTCOME_STATUS = UNOPENED
P1_STATUS = NOT_SELECTED_NOT_FROZEN
```

## Next mechanical source step

Export all 160 SuperSeries sample records into a compact table with:

- GSM accession;
- modality;
- raw title;
- normalized diagnostic title;
- patient ID;
- sample state;
- source series;
- pairing status.

That table must confirm all 72 expression samples map to exactly one methylation sample with the same patient and sample state before any future cross-omic biological calculation uses the normalized title relation.
