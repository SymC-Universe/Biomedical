# NSD Candidate Dataset Triage for Spectrum-vs-Stability Mapping v0.1

**Status:** DATASET DISCOVERY / NO OUTCOME OPENING  
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum

## Purpose

Identify datasets that can compare qualified NSD stability objects against already-established clinical, EEG, developmental, and network dimensions. Dataset suitability is based on subject-level identity, phenotype depth, repeated-state structure, channel quality, and ability to support native comparators.

## Tier A: strongest immediate candidates

### SFARI EEG multi-paradigm dataset, OpenNeuro ds006780

- groups: 44 TD, 66 ASD, 28 siblings;
- age: 8-13 years;
- 64-channel BioSemi EEG, 512 Hz;
- seven complementary paradigms;
- resting-state includes repeated 1-minute eyes-open blocks over two sessions/days where available;
- autism diagnosis is clinically characterized and participant metadata/phenotype files are available;
- same acquisition platform across participants.

Why it matters:
- same participant can contribute multiple state/task measurements;
- supports local spectral/aperiodic, modal/network, state-specific, and test-retest questions;
- ASD + sibling + TD structure is more informative than a binary case-control split;
- direct comparison to established oscillatory measures is possible.

Primary prospective use:
- first serious autism spectrum-vs-stability validation after estimator qualification;
- state vs trait decomposition;
- native spectral/aperiodic/microstate/connectivity comparator stack;
- symptom/trait mapping where available.

### Healthy Brain Network EEG

- >3000 participants, ages approximately 5-21 years across releases;
- resting state plus multiple active/passive tasks;
- broad behavioral/clinical phenotyping in the parent HBN project.

Why it matters:
- best current candidate for developmental normative modeling;
- transdiagnostic rather than autism-only;
- suitable for learning age-conditioned native EEG distributions before testing NSD stability deviations;
- large enough for subject-level development/holdout splits.

Primary prospective use:
- normative centiles/deviation models;
- transdiagnostic symptom dimensions;
- age/state/task dependence;
- external validation of relationships first found in smaller ASD-specific data.

## Tier B: targeted validation candidates

### BCIAUT-P300 / NEMAR nm000210

- ASD P300/joint-attention dataset;
- 15 participants;
- 8 channels, 250 Hz;
- seven sessions;
- repeated-session structure is valuable despite small N.

Why it matters:
- excellent for within-subject/test-retest and intervention/repeated-session stability behavior;
- poor choice for broad population inference because of small subject count.

Primary prospective use:
- repeatability, state/intervention sensitivity, and refusal behavior;
- not a prevalence or normative dataset.

### ABIDE I/II

- large public autism resting-state fMRI resource, not EEG.

Why it matters:
- does not validate local EEG \(\chi\);
- potentially useful later for \(\Chi\)/\(\Chi_{\mathrm{arc}}\) network-level and normative cross-modality questions;
- should remain secondary until the EEG stability object is established.

## Dataset admission checklist

Before any dataset becomes a decisive NSD spectrum-comparison source:

1. subject identity, not trial count, is the independent sampling unit;
2. diagnosis/phenotype source is documented;
3. age, sex, IQ/developmental level, medication, and task/state metadata are inventoried where available;
4. repeated sessions/runs are modeled as repeated measures, not independent subjects;
5. reference/montage/sample-rate/data-quality differences are frozen as covariates or site effects;
6. native EEG features are computed before stability-added comparisons;
7. stability estimators pass the appropriate data/model admission gate;
8. development/holdout identities are frozen before outcome opening;
9. no clinical threshold is learned from an exposed test set;
10. missing phenotype fields are preserved rather than imputed opportunistically.

## Recommended order

1. use HBN to construct age/development/state normative native EEG baselines;
2. use SFARI EEG as the first focused ASD/sibling/TD spectrum-vs-stability experiment;
3. use BCIAUT-P300 as a repeated-session/test-retest challenge;
4. use ABIDE only for later network/system-level cross-modality questions;
5. seek additional independent ASD EEG cohorts before clinical interpretation.

## Key refusal

The old OG NSD mistake must not recur: sessions, trials, windows, or task blocks may increase repeated measurements, but they do not increase the number of independent participants.
