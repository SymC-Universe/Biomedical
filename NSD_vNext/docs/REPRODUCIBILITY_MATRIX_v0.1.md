# NSD Reproducibility Matrix v0.1

Status: ACTIVE
Date: 14 September 2026

## R1 — Release integrity and regeneration

Required:
- canonical commit identified;
- archive/checksum generated;
- dependency/environment lock;
- tests separated into scientific tests, software tests, and drift/integrity checks;
- clean-room extraction verified;
- generated figures/tables regenerated from declared parents;
- stale historical artifacts excluded from the active release path.

Current state: NOT YET FROZEN FOR NSD vNext.

## R2 — Scientific recomputation

Required:
- exact dataset/source identity;
- subject/session/trial hierarchy;
- preprocessing configuration;
- feature extraction version;
- model and threshold versions;
- split definitions;
- subject-level resampling/validation logic;
- deterministic or seeded stochastic steps;
- recomputation of every primary manuscript quantity from preserved inputs where licensing permits.

Current state: HISTORICAL NSD PACKAGE RECONSTRUCTION PENDING.

## R3 — Primary evidence and provenance reconstruction

Required:
- dataset provenance and access route;
- clinical-label provenance;
- acquisition metadata;
- covariate provenance;
- literature source identity for external reference values;
- exact transformations and units;
- atlas-source independence mapping;
- privacy-safe subject/session identity preservation where raw IDs cannot be redistributed.

Current state: PENDING DATASET/ATLAS AUDIT.

## Result-by-result matrix

| Result family | R1 | R2 | R3 | Current ceiling |
| --- | --- | --- | --- | --- |
| Historical NSD scalar results | historical package only | pending re-run | pending source reconciliation | provenance only |
| Healthy baseline | not frozen | pending | pending | not yet active |
| ASD phenotype analysis | not frozen | pending | pending | exploratory historical |
| Modal Engine qualification | not frozen | pending | synthetic design pending | not yet qualified |
| Cross-disorder comparison | not frozen | not run | datasets not frozen | hypothesis |
| Comorbidity analysis | not frozen | not run | design pending | hypothesis |
| Predictive clinical endpoint | not frozen | not run | longitudinal evidence not frozen | not tested |

## Release rule

A successful archive hash is not R2. A successfully rerun analysis from local intermediate files is not necessarily R3. Each level is reported separately and only after the corresponding evidence is actually reconstructable.
