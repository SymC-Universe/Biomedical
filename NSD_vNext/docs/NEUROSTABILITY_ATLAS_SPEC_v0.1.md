# Neurostability Atlas Specification v0.1

Date: 14 September 2026
Status: DESIGN SPECIFICATION / NOT YET POPULATED

## 1. Purpose

The Neurostability Atlas is the independent reference layer against which NSD structural outputs are interpreted. It is not allowed to tune the Structural Engine and it is not rebuilt separately for each disorder to maximize separation.

Primary purpose:

> describe ordinary variation, reproducibility, state dependence, demographic/acquisition structure, and clinically relevant departures in the same feature space produced by a frozen Engine.

## 2. Atlas unit hierarchy

Every record must preserve:
- dataset;
- site/device;
- subject;
- session;
- recording condition;
- trial/epoch where applicable;
- channel/region;
- mode identifier where applicable;
- Engine version;
- preprocessing/configuration version.

Atlas tables may expose aggregated views, but raw hierarchy keys cannot be discarded from the provenance chain.

## 3. Atlas layers

### A. Spectral reference layer

For each qualified recording condition:
- aperiodic exponent distribution;
- aperiodic offset distribution;
- knee distribution where used;
- periodic peak counts;
- complete peak-frequency distributions;
- peak power/amplitude distributions;
- descriptive bandwidth distributions;
- fit-quality and failure distributions;
- zero-peak prevalence.

### B. Modal reference layer

Where the Engine can identify modes:
- modal frequency distributions;
- decay-rate distributions;
- pole/eigenvalue distributions;
- mode-order distributions;
- mode-shape/participation distributions;
- estimator disagreement rates;
- refusal rates.

### C. Licensed scalar layer

For every mode-specific scalar:
- exact derivation version;
- admissible operating region;
- estimate distribution;
- uncertainty distribution;
- fraction of sessions/subjects admitted;
- fraction refused and reasons;
- within-subject repeatability;
- between-subject variance;
- condition sensitivity.

No atlas cell is required to contain a chi value. Missingness because a scalar is scientifically inadmissible is meaningful.

### D. Spatial and conglomerate layer

Candidate reference structures:
- regional gradients;
- posterior/anterior organization;
- hemispheric organization;
- channel participation;
- mode co-occurrence;
- interregional relationships;
- network/relational summaries;
- spatial heterogeneity distributions.

### E. Open-channel layer

Population-level distribution of:
- no-peak states;
- rejected fits;
- ambiguous metadata;
- low-quality recordings;
- model disagreement;
- out-of-domain recordings;
- scalar refusals.

The Atlas does not hide the rate at which the preferred architecture fails.

## 4. Healthy reference lock

The first healthy reference release should be treated as a versioned object.

A proposed lock record includes:

```text
atlas_version
engine_version
dataset_versions
subject_inclusion_hash
recording_conditions
age_range
sex/gender variables available
site/device variables
medication/state exclusions if available
preprocessing_hash
feature_definition_hash
reference_model_hash
```

After locking, disease analyses consume the same reference object unless a scientifically necessary scope change is documented as a new Atlas version.

## 5. Covariate strategy

The Atlas should describe rather than erase ordinary structure.

Priority covariates where available:
- age/development;
- sex/gender variable as actually collected;
- site;
- hardware/amplifier;
- reference scheme;
- eyes-open/eyes-closed/task state;
- recording duration;
- time of day;
- sleep/vigilance state;
- medication status;
- substance/caffeine/nicotine status where available;
- major neurological/psychiatric exclusions in healthy cohorts.

Covariate handling must be frozen by question. A residualized feature is not interchangeable with the raw feature and should be stored separately.

## 6. Trait/state decomposition target

Repeated-session data should be used to estimate, where feasible:
- within-session variance;
- between-session within-subject variance;
- between-subject variance;
- state/condition shifts;
- site/device variance;
- long-term drift.

The Atlas should answer not only “what is normal?” but:

> Which parts of the architecture are stable enough to function as person-level reference features, which are state-sensitive, and which are too measurement-sensitive for current use?

## 7. Function Map integration

The healthy Atlas is a major input to the Function Map.

Target ordinary-state axes include:
- resting eyes closed;
- resting eyes open;
- task engagement where available;
- sleep/wake or vigilance changes where available;
- repeated sessions;
- age/development;
- recovery after ordinary perturbation where data exist.

This avoids defining “health” merely as the absence of disorder or proximity to a preconceived chi value.

## 8. Limit Map integration

Atlas failure regions must be explicit:
- channels/regions with systematically poor fits;
- recording conditions with unreliable periodic parameterization;
- frequencies where instrumentation/filtering limits inference;
- populations outside the training/reference range;
- modes with high estimator disagreement;
- covariate strata with insufficient sample size;
- scalar-admission regimes with poor reliability.

## 9. Disorder overlays

Clinical cohorts are overlays on the same Atlas architecture.

A disorder overlay may describe:
- shift in an empirical feature distribution;
- change in variability;
- altered spatial organization;
- altered mode count/participation;
- different refusal/absence pattern;
- changed longitudinal stability;
- changed relation among layers.

It must not redefine the healthy reference so the disorder appears more distinct.

## 10. Shared-instability test

A cross-disorder shared-architecture claim requires more than both disorders differing from controls.

At minimum, evaluate:
1. whether the same frozen features are measurable in both cohorts;
2. which deviations are shared;
3. which deviations are disorder-specific;
4. whether system/modal organization differs even when scalar/spectral summaries overlap;
5. whether similarities survive site/acquisition/covariate control;
6. whether a native transdiagnostic baseline explains the pattern equally well or better.

## 11. Release tiers

Proposed Atlas maturity:

- **Atlas-P0-D**: exploratory reference maps, broad function/limit discovery.
- **Atlas-P0-Q**: frozen feature definitions, qualified Engine, audited healthy hierarchy, uncertainty characterization.
- **Atlas-P1**: confirmatory transfer to untouched healthy and clinical datasets.
- **Atlas-P2**: reproducible reference artifact with documented scope and versioning.

## 12. Immediate population order

Without waiting on new computations, the intended population sequence is now frozen conceptually:

1. reconstruct and audit existing healthy datasets and hierarchy;
2. populate basic spectral state;
3. map reliability and ordinary-state effects;
4. qualify modal/dynamical estimators independently;
5. add licensed scalar distributions only where admissible;
6. build spatial/conglomerate healthy organization;
7. lock first healthy reference;
8. overlay ASD and later disorders without retuning the baseline.

The Atlas exists specifically to prevent the historical mistake of defining an “adaptive window” first and then making observations conform to it.