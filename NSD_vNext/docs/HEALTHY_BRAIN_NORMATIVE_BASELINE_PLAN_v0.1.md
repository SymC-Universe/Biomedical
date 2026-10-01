# NSD Healthy-Brain Normative Baseline Plan v0.1

**Status:** DEVELOPMENT / NORMATIVE BASELINE DESIGN  
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Purpose:** establish the reference architecture against which pain, BPD, MDD, ADHD-I, ADHD-HI, autism, Parkinson's disease, and addiction will later be compared.  
**Scientific ceiling:** no universal "healthy chi," no diagnostic threshold, and no claim that health is a single dynamical point.

## 1. Baseline principle

The healthy brain is not represented by one mean, one threshold, or one coordinate.

The normative target is a conditional distribution:

\[
P(X \mid \text{age, sex, state, task, sleep/arousal, recording context, site/device, relevant covariates})
\]

where \(X\) may be a native EEG feature, a licensed local \(\chi\), a modal/vector \(\Chi\), or a later qualified \(\Chi_{\mathrm{arc}}\).

The reference object is therefore a normative manifold / family of distributions, not a scalar healthy point.

## 2. Three distinct baselines are required

### A. Population normative baseline

Purpose:
- establish age/development-conditioned distributions;
- estimate expected between-person variability;
- quantify centiles/deviation scores;
- prevent disorder effects from being confused with ordinary development or aging.

Primary native quantities:
- canonical band power;
- peak/center frequencies;
- aperiodic exponent/offset/knee where valid;
- connectivity/cross-spectral descriptors;
- microstate/state-transition descriptors where available;
- variability/reliability measures.

Only after stability qualification:
- local \(\chi\) distributions;
- modal/vector \(\Chi\) distributions;
- system architecture components where operationally defined.

### B. Within-person state baseline

Purpose:
- distinguish trait-like organization from ordinary state movement.

Required repeated conditions where data allow:
- eyes open vs eyes closed;
- pre-task vs post-task;
- rest vs cognitive/sensory challenge;
- repeated day/session;
- sleep/arousal state;
- medication/caffeine/substance state where documented;
- fatigue/circadian context where available.

The baseline asks:

\[
\Delta X_{\mathrm{within}} = X_{\mathrm{state\ 2}} - X_{\mathrm{state\ 1}}
\]

before interpreting between-group deviations.

### C. Longitudinal baseline

Purpose:
- establish how much healthy architecture changes over months/years;
- distinguish disease progression from ordinary development/aging;
- quantify within-person drift and reorganization.

Longitudinal change is not treated as pathology by default.

## 3. Reference-cohort eligibility

A "healthy" or normative reference cohort is a data contract, not a metaphysical category.

Required documentation includes, where available:
- neurological diagnoses;
- psychiatric diagnoses;
- current major medications;
- substance use;
- sleep state;
- acute illness;
- major pain condition;
- developmental/cognitive status;
- sensory impairment;
- age;
- sex;
- handedness where relevant;
- recording site/device/reference/montage;
- task/rest condition;
- data-quality exclusions.

Unknown fields remain unknown. They are not silently treated as healthy.

## 4. Reference hierarchy

### Tier H0: acquisition and quality reference

Establish:
- channel quality;
- artifact burden;
- usable duration;
- sampling rate;
- reference/montage;
- preprocessing stability;
- session reliability.

No biological interpretation occurs before H0.

### Tier H1: native EEG normative baseline

Construct age/state-conditioned distributions for:
- spectral power;
- peak frequency;
- aperiodic structure;
- connectivity/cross-spectrum;
- variability;
- microstate/state-transition measures where data support them.

This is the strongest native comparator for later stability-added tests.

### Tier H2: qualified local stability baseline

Only if local \(\chi\) passes the Bio-\(\chi\) admission/refusal architecture:
- estimate normative distribution by age/state;
- estimate within-subject repeatability;
- estimate site/reference sensitivity;
- estimate state movement;
- calculate uncertainty/deviation scores.

No universal healthy \(\chi=1\) or other preferred value is presumed.

### Tier H3: modal/vector baseline

For data supporting a qualified \(\Chi\):
- modal frequency/damping structure;
- eigenspaces/subspaces;
- participation/coupling;
- non-normal/transient descriptors;
- state transitions;
- observation sensitivity;
- uncertainty.

### Tier H4: system/recovery baseline

Only where operationally supported:
- perturbation response;
- return/recovery trajectories;
- state transition/reorganization;
- history dependence;
- longitudinal architecture.

This is the appropriate baseline for domains such as pain flare, BPD affective challenge, Parkinson's medication/DBS state, or addiction cue/withdrawal recovery.

## 5. Primary normative datasets

### HarMNqEEG

- 1,564 neurologically healthy participants;
- ages 5-97;
- 9 countries;
- 12 EEG devices;
- 14 contributing studies;
- eyes-closed resting-state qEEG;
- cross-spectral tensors and harmonized developmental equations;
- explicit batch/site harmonization.

Primary role:
- lifespan native EEG normative backbone;
- age/sex/site/device conditioning;
- cross-spectral/connectivity norms;
- later comparison of stability deviation against standard qEEG deviation.

Important limitation:
- eyes-closed resting state is not a complete state baseline.

### Dortmund Vital Study resting-state EEG dataset

- 608 healthy participants;
- ages 20-70;
- 64-channel EEG;
- eyes-open and eyes-closed;
- measured before and after approximately two hours of cognitive tasks;
- 208 participants have approximately 5-year follow-up.

Primary role:
- adult within-person state effects;
- pre/post cognitive-load recovery/reorganization;
- healthy aging;
- longitudinal drift.

### LEMON

- 213 healthy participants;
- young group 20-35;
- older group 55-80;
- resting-state EEG.

Primary role:
- independent adult replication;
- external validation of age effects;
- preprocessing/pipeline robustness.

### SFARI EEG TD participants

- locally matched TD reference for the ASD-focused experiment;
- same acquisition family as ASD/sibling participants.

Primary role:
- local matched control distribution;
- not the universal normative backbone.

### Healthy Brain Network

Use as a developmental/transdiagnostic cohort, not as a strict "healthy control" source merely because of the project name.

Primary role:
- developmental dimensional modeling;
- symptom/behavior relationships;
- broad age/task variation;
- transdiagnostic validation.

## 6. Healthy reference outputs

For every native or stability variable, report:

- conditional mean/median;
- variance and robust spread;
- centiles;
- individual deviation score / normative z-score where justified;
- test-retest reliability;
- within-person state variance;
- between-person variance;
- age/development effect;
- sex effect where supported;
- site/device/reference effect;
- uncertainty interval;
- refusal rate;
- missingness/data-quality rate.

A variable that is not reproducible in healthy/reference data cannot become a disorder biomarker.

## 7. Baseline versus disorder comparison

For disorder/domain D and feature X:

\[
Z_D(X) = \frac{X_D - E[X \mid C]}{\sigma[X \mid C]}
\]

where \(C\) is the frozen normative conditioning set.

The actual model may be nonlinear/non-Gaussian; the z-score expression is only conceptual shorthand.

Comparisons are performed first against the native normative model, then against native + stability.

The primary question is not:

> Is disorder D different from healthy controls?

It is:

> Does disorder D show a reproducible deviation from the appropriate normative architecture, and does a stability object explain additional held-out information beyond established native measures?

## 8. Cross-domain use

All mapped domains must reference the same baseline logic but may require different state baselines.

- pain: healthy sensory response and recovery;
- BPD: healthy affective/stress perturbation and recovery;
- MDD: healthy reward/cognitive/arousal state dynamics;
- ADHD-I: healthy sustained-attention engagement and variability;
- ADHD-HI: healthy inhibition/reward-control dynamics;
- autism: healthy developmental sensory/network organization;
- Parkinson's: healthy aging motor/basal-ganglia/cortical dynamics;
- addiction: healthy reward/stress/control response and recovery.

No domain is forced onto one shared scalar scale.

## 9. Falsifiers

The healthy-baseline program fails operationally if:
- normative distributions are dominated by site/device artifacts;
- within-person state variation is as large as or larger than purported disorder deviations without a state model;
- candidate stability variables show poor test-retest reliability;
- age/development explains apparent case-control separation;
- stability deviations are reducible to native EEG deviations;
- no stable normative reference can be constructed without outcome-driven thresholds.

These failures must be preserved rather than repaired post hoc.

## 10. Immediate work order

1. reproduce HarMNqEEG native age-conditioned norms using provided/open code where feasible;
2. reproduce basic Dortmund healthy age/state effects;
3. establish the native EEG comparator feature set;
4. build harmonization/site/reference audit;
5. freeze the normative-model evaluation metrics;
6. after Bio-\(\chi\) qualification closes, add local \(\chi\) without changing the native baseline;
7. only then compare the disorder-spectrum cohorts.

