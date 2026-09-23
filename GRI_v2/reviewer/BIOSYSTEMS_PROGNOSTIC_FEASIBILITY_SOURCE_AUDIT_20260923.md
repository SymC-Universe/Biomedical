# BioSystems prognostic-feasibility source audit - 23 September 2026

**Status:** `NOT_TESTABLE_WITH_CURRENT_FROZEN_SOURCE_MAPPING`

## Question

Can an architecture-derived patient-level object be tested prospectively against progression-free survival in the already-used independent Roswell Park prostate cohort without opening a new large analysis program?

## Public source state

Molecular sources:
- RNA: GEO `GSE237995`;
- 450K methylation: GEO `GSE262522`;
- EPIC methylation: GEO `GSE262524`.

The source paper is:
Ramakrishnan S, Cortes-Gomez E, Athans SR, et al. Race-specific coregulatory and transcriptomic profiles associated with DNA methylation and androgen receptor in prostate cancer. Genome Medicine. 2024;16:52. doi:10.1186/s13073-024-01323-6.

The article reports progression-free-survival analyses of pathway scores and clinical variables. It also states that clinical samples were de-identified before analysis and describes Additional File 1 clinical tables as cohort demographic/clinical-characteristic tables.

The currently frozen GEO molecular objects provide molecular sample/participant identities used by the external P1 analysis, but no source-verified participant-level table containing both:
- exact progression-free-survival time;
- censor/event indicator;
- an unambiguous mapping to the frozen `PT-...` molecular participant IDs

has been qualified in the public evidence lineage.

## Disposition

No prognostic model is run.

This is **not** evidence that the molecular architecture lacks prognostic information. It means a valid participant-level prognostic endpoint cannot presently be bound to the frozen external molecular participants without inventing or inferring a clinical crosswalk.

A new prognostic lane may open later if a source-of-record clinical outcome map becomes available.

## Claim consequence

For the current BioSystems revision:

`PROGNOSTIC_UTILITY_NOT_ESTABLISHED__CURRENT_SOURCE_MAPPING_INSUFFICIENT`

This source limitation is kept distinct from the negative frozen prostate diagnostic experiment.
