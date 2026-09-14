# NSD Native Comparator Program v0.1

Date: 14 September 2026
Status: PRE-COMPUTE DESIGN

## 1. Purpose

NSD earns value only if it performs a scientifically useful job that a simpler, accepted neurophysiological toolkit does not already perform equally well.

Comparator testing is not a ceremonial final section. It is part of the main claim architecture.

Possible outcomes are:
- `ADDS`
- `EQUIVALENT`
- `SUBTRACTS`
- `INDETERMINATE`
- `NOT_TESTED`

`NO_NATIVE_COMPARATOR` is separate and must be justified rather than assumed.

## 2. Comparator hierarchy

The exact comparator depends on the frozen question. The following hierarchy is the default starting set.

### C0 — Demographic / acquisition baseline

Where relevant:
- age;
- sex/gender variable as collected;
- site;
- device;
- recording duration;
- recording condition.

Purpose: detect whether apparent clinical separation is mainly acquisition or demographic structure.

### C1 — Simple spectral baseline

Candidate features:
- canonical band powers;
- relative/absolute power as appropriate;
- alpha peak frequency;
- simple spectral entropy or other justified conventional summary;
- theta/beta or other disorder-specific conventional ratios only when literature and task justify them.

Purpose: establish whether NSD adds beyond ordinary EEG summaries.

### C2 — Periodic/aperiodic baseline

Candidate features:
- aperiodic exponent;
- aperiodic offset;
- knee where justified;
- periodic peak frequency;
- periodic peak power;
- descriptive bandwidth;
- peak count;
- fit quality.

Purpose: this is the closest native comparator for many proposed NSD features and is mandatory when the Engine uses the same decomposition upstream.

### C3 — Spatial baseline

Candidate features:
- regional means;
- scalp topography;
- posterior-anterior gradients;
- channel-wise conventional spectral features;
- simple covariance/correlation structure.

Purpose: determine whether apparent “conglomerate” value is simply preserved spatial information.

### C4 — Native modal / state-space baseline

Where feasible:
- autoregressive/state-space modes;
- conventional eigenmode or DCM/neural-mass parameters;
- autocorrelation time;
- burst statistics.

Purpose: prevent NSD from claiming novelty for modal dynamics already captured by standard system-identification methods.

### C5 — Clinical baseline

For diagnostic/classification tasks:
- diagnosis priors/demographics as appropriate;
- symptom scales;
- accepted clinical predictors available in the same dataset.

For prediction tasks:
- baseline severity;
- treatment/history covariates;
- conventional EEG predictors supported by the relevant literature.

## 3. NSD comparison layers

NSD should be added progressively rather than only as one all-in model.

Recommended nested sequence:

1. `C0`
2. `C0 + C1`
3. `C0 + C2`
4. `C0 + C2 + spatial`
5. `C0 + C2 + modal`
6. `C0 + C2 + modal + conglomerate`
7. add licensed chi only where available
8. full NSD architecture including categorical refusal/absence states

This allows the source of any incremental value to be located.

## 4. Tasks must remain separate

Comparator performance is task-specific.

Do not merge:
- group difference;
- cross-sectional classification;
- dimensional symptom association;
- longitudinal prediction;
- treatment-response prediction;
- external-dataset transfer;
- reliability.

A feature set can add value for one task and subtract for another.

## 5. Split discipline

For subject-level tasks:
- split by subject, never epoch/session unless the task is explicitly within-subject;
- keep preprocessing/model selection inside training folds where applicable;
- keep the healthy Atlas lock independent of the test cohort;
- external transfer datasets remain untouched until the intended stage.

## 6. Metric discipline

Classification examples:
- AUROC;
- balanced accuracy;
- sensitivity/specificity;
- calibration;
- precision-recall where prevalence makes it important.

Regression/prediction examples:
- MAE/RMSE;
- R-squared where appropriate;
- calibration;
- clinically meaningful decision metrics if a true clinical task is reached.

Reliability:
- ICC with stated model/type;
- within-subject coefficient of variation where meaningful;
- Bland-Altman or equivalent agreement analysis;
- admission/refusal repeatability.

No single metric should be selected after results are viewed because it favors NSD.

## 7. Incremental-value decision rule

The exact statistical threshold will be frozen with the task, but interpretation follows:

### ADDS
NSD provides reproducible improvement over the strongest fair comparator and the improvement survives uncertainty, leakage checks, and external/held-out evaluation appropriate to the stage.

### EQUIVALENT
NSD performs comparably but does not add measurable value. A simpler explanation/tool may be preferred.

### SUBTRACTS
NSD is worse, less stable, more brittle, or less transferable than the comparator.

### INDETERMINATE
Data, power, transfer, or uncertainty are insufficient to decide.

### NOT_TESTED
No fair comparison has yet been run.

## 8. Architecture-specific value claims

A full NSD architecture could still be scientifically useful even if classification accuracy is equivalent, but the added value must be named and tested.

Potential non-classification value:
- better uncertainty calibration;
- interpretable refusal states;
- better test-retest reliability;
- more faithful spatial/modal representation;
- better transfer across sites;
- ability to distinguish mechanistically different signals with similar band power;
- a more informative Function or Limit Map.

These are separate claims and cannot be inferred from an attractive state-space plot.

## 9. Cross-disorder comparator

For transdiagnostic claims, the minimum comparator includes:
- standard periodic/aperiodic feature space;
- dimensional symptom representation where available;
- diagnosis labels;
- simple multivariate models.

NSD must show whether its architecture reveals shared structure **and** preserved disorder-specific structure beyond these baselines.

## 10. Historical safeguard

The 2025 NSD paper visually separated disorder classes in a constructed stability space. Under the current program, visually clean clustering has no privileged status.

The comparator question is now:

> Does the NSD representation recover structure from measured neurophysiology that is reproducible and useful beyond the strongest simpler native representation?

If the answer is no, the correct scientific result is EQUIVALENT or SUBTRACTS.