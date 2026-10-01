# NSD Spectrum-to-Stability Comparison Test Matrix v0.1

**Status:** DEVELOPMENT / PRIOR-ART COLLISION MAP  
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Purpose:** convert the known-spectrum literature map into explicit discriminating tests against \(\chi\), \(\Chi\), and \(\Chi_{\mathrm{arc}}\).

## Core rule

A stability variable is not useful merely because it correlates with a diagnosis, symptom score, EEG feature, or network measure.

For every comparison, the native spectrum is entered first. Stability adds only if it contributes reproducible held-out information, mechanistic discrimination, state tracking, or longitudinal sensitivity beyond the strongest native comparator under a frozen analysis.

## Comparison matrix

| Existing spectrum / construct | Native measures | Closest stability object | Main redundancy/confound risk | Minimum discriminating test | Admissible outcomes |
| --- | --- | --- | --- | --- | --- |
| autism symptom/trait severity | ADOS/CARS/SRS/AQ-type dimensions | \(\chi\), \(\Chi\), later \(\Chi_{\mathrm{arc}}\) | diagnosis/severity may absorb all apparent association | held-out symptom/trait prediction: native phenotype + demographics vs native phenotype + stability | REDUNDANT; INCREMENTAL; SUBGROUP_SPECIFIC; NEED_MORE_INFO |
| social communication | clinical subscales, task performance | \(\Chi\), \(\Chi_{\mathrm{arc}}\) | global severity masquerading as domain relation | residualize/global-severity-controlled held-out prediction | DOMAIN_SPECIFIC; GLOBAL_ONLY; REFUSED |
| rigidity/repetitive behavior | clinical scales, task switching/flexibility | \(\Chi\), recovery architecture | trait score may be unrelated to dynamical rigidity | perturbation/state-transition response vs behavioral rigidity after age/IQ controls | CONDITIONAL; INCREMENTAL; NO_RELATION |
| sensory reactivity | sensory profiles, evoked EEG/MEG | local \(\chi\), \(\Chi\) | power/ERP amplitude may explain everything | predict trial/state recovery or sensory profile beyond standard evoked/spectral features | REDUNDANT; INCREMENTAL; STATE_SPECIFIC |
| canonical EEG spectrum | delta/theta/alpha/beta/gamma power, peak frequency | local \(\chi\) | \(\chi\) may simply encode frequency/power/peak width | compare native spectrum-only vs spectrum + qualified \(\chi\) on held-out state/trait target | REDUNDANT; ORTHOGONAL; CONDITIONAL |
| aperiodic EEG | exponent, offset, knee | local \(\chi\) | both may reflect timescale/E-I related structure | direct dependence + partial-information + held-out incremental test | REDUNDANT; MEDIATED; ORTHOGONAL; REFUSED |
| E/I continuum | MRS GABA/glutamate, TMS, pharmacologic challenge, circuit models | local \(\chi\), possibly \(\Chi\) | unlicensed assumption that damping equals E/I | model-specific mapping only; cross-modal validation required | MECHANISTIC_LINK; CORRELATED_ONLY; INDEPENDENT; REFUSED |
| EEG microstates | duration, occurrence, coverage, transition matrix | \(\Chi\) | \(\Chi\) may repackage state-transition organization | native microstate model vs microstate + \(\Chi\) on held-out phenotype/state target | REDUNDANT; INCREMENTAL; NONIDENTIFIABLE |
| functional/effective connectivity | coherence, phase metrics, FC/EC, graph measures | \(\Chi\), \(\Chi_{\mathrm{arc}}\) | modal/vector organization may duplicate connectivity | target-specific nested comparison plus invariance/observation sensitivity | REDUNDANT; MODAL_ADDS; SYSTEM_ADDS; REFUSED |
| neural variability | trial-to-trial, spectral, response variability, entropy | \(\chi\), \(\Chi\) | instability may be mislabeled variability | jointly model variability and stability; test conditional independence | SAME_AXIS; SEPARABLE_AXES; STATE_SPECIFIC |
| criticality/metastability | avalanche statistics, critical slowing, metastability, synchrony, Lyapunov-like descriptors | \(\chi\), \(\Chi\), \(\Chi_{\mathrm{arc}}\) | stability language may duplicate established dynamical-systems measures | explicit mathematical mapping + counterexamples + incremental target | EQUIVALENT; CONDITIONAL; DISTINCT; REFUSED |
| developmental/normative position | centiles, normative z/deviation scores, developmental trajectories | all three levels | pooled thresholds can manufacture group differences | age/development-conditioned norms first, then stability deviations | NORMATIVE_DEVIATION_ADDS; AGE_EXPLAINS; NEED_MORE_INFO |
| state/context | sleep, arousal, medication, task, fatigue, sensory load | all three levels | trait/state conflation | within-person repeated-state model vs between-person model | TRAIT_LIKE; STATE_SPECIFIC; MIXED |
| longitudinal/progression | symptom/cognitive change, intervention response | \(\Chi\), \(\Chi_{\mathrm{arc}}\) | cross-sectional association cannot establish tracking | repeated-measures change prediction and recovery/reorganization analysis | MONITORING_VALUE; PROGNOSTIC_VALUE; NO_ADDED_VALUE |

## Required analysis order

1. verify stability object is licensed for the data;
2. establish native comparator;
3. freeze target and covariates;
4. split subject-level train/development/holdout where sample size permits;
5. fit native comparator alone;
6. fit native + stability;
7. report held-out incremental information, calibration, and uncertainty;
8. inspect subgroup/state interactions only if prospectively authorized;
9. refuse any relationship unsupported by identifiability or sample size;
10. preserve nulls and redundancy as valid results.

## Priority hypotheses to test after v0.2 qualification

### H1: \(\chi\) versus standard EEG spectral structure
If qualified local \(\chi\) is almost completely predicted by band power, peak frequency, or aperiodic structure, treat it as redundant unless a mechanistic or predictive difference remains.

### H2: \(\Chi\) versus microstate/connectivity organization
If the modal/vector representation reconstructs the same information as native network/microstate metrics, retain native terminology and do not claim a new stability spectrum.

### H3: stability versus phenotype
A stability object may still be scientifically useful even if it does not separate ASD from TD, provided it reproducibly maps onto a transdiagnostic symptom/state dimension or longitudinal response.

### H4: normative placement
No universal healthy threshold is presumed. Stability objects should eventually be interpreted relative to age/development/state-conditioned normative distributions.

### H5: state versus trait
A within-person shift in stability with sleep/arousal/task/medication must not be confused with a stable subject-level architecture. Both may exist and must be estimated separately.

## OG NSD falsifier

The broad OG NSD thesis is weakened if, after proper licensing and native comparison:
- local \(\chi\) is consistently redundant with ordinary EEG features;
- \(\Chi\) adds nothing beyond native modal/network dynamics;
- \(\Chi_{\mathrm{arc}}\) cannot be constructed reproducibly without outcome-driven choices;
- stability deviations do not replicate across sessions or fail to relate to any declared phenotype/state/recovery target.

It is strengthened only by held-out, reproducible, level-specific incremental information, not by visually separated diagnostic clouds.
