# Healthy-Brain Native Baseline Reproduction Plan v0.1

**Status:** ACTIVE DEVELOPMENT / EXTERNAL NATIVE BASELINE  
**Date:** 2026-10-01  
**Governance:** SymC GOM v1.1 + Continuity Hardening Addendum  
**Scientific authority:** independent healthy/reference neuroscience only. No NSD-derived value defines the baseline.

## Goal

Construct a reproducible healthy-brain reference from independent literature and public data before comparing any disorder or any NSD stability coordinate.

The baseline has four layers:

1. population/lifespan position;
2. within-person state displacement;
3. short- and long-term repeatability;
4. longitudinal drift.

Perturbation/recovery envelopes are a later layer and will use sustained-capture trajectory classes rather than first crossing.

## Lane H1 — HarMNqEEG lifespan norm

Source:
- Li et al. 2022, NeuroImage 256:119190, PMID 35398285.
- Official toolbox: tperezdevelopment/HarMNqEEG.
- traditional log-spectrum norm Git-LFS SHA-256:
  `dba25f3172b04fb5627083274e8871ef2058bc872217c617fd7cd3bd0859b484`.

Current development task:
- `NSD_HARMN_LOG_NORM_INTROSPECT_V02`;
- Kaggle kernel: `symcuniverse/nsd-harmn-baseline-introspect-v0-2`;
- verify norm object checksum;
- extract MATLAB/HDF5 regression-object structure;
- identify mean and variance factors, response variables, batch levels, and gridded interpolation objects;
- do not alter or refit the published norm.

Next action:
- reproduce age/frequency normative means/variances from the published model or, if exact non-MATLAB reproduction is not numerically faithful, freeze MATLAB-toolbox scoring as the native reference implementation and wrap it without changing the model.

## Lane H2 — Dortmund healthy state/longitudinal reference

Source:
- OpenNeuro ds005385 v1.0.3;
- Getzmann et al. 2024, Scientific Data, PMID 39256413;
- Park et al. 2026, Front Aging Neurosci, PMID 42395346.

Published pipeline to reproduce:
- EEG only;
- 1–40 Hz band-pass;
- average reference;
- Welch PSD 1–40 Hz;
- posterior alpha relative power;
- alpha peak frequency;
- theta/beta ratio;
- aperiodic exponent using fixed spectral parameterization over 2–40 Hz, peak widths 1–8 Hz, max six peaks, minimum peak height 0.1;
- pre/post files averaged within participant/session/eye condition for state analysis;
- paired EO/EC Cohen's d;
- five-year ICC(A,1) for longitudinal stability.

Current development task:
- `NSD_DORTMUND_NATIVE_PREFLIGHT_V01`;
- Kaggle kernel: `symcuniverse/nsd-dortmund-native-preflight-v0-1`;
- deterministic 12-person age/sex-stratified sample;
- session 1 only;
- four files per person: EC/EO × pre/post;
- no NSD variable;
- no normative inference from n=12.

Pilot selection rule:
- target ages 20, 30, 40, 50, 60, 70;
- separately for F and M;
- require session1 and `late_ses1=0`;
- choose minimum absolute age distance, then participant ID for ties.

Pilot purpose:
- verify OpenNeuro transport;
- verify EDF reading and preprocessing;
- verify feature extraction;
- verify directions of EO/EC effects are coherent with the published full-sample reference;
- preserve any access/implementation/data failure.

## Promotion rule

Neither H1 nor H2 becomes the definitive healthy baseline merely because code runs.

Promotion requires:
- exact source identity;
- reproducible method;
- native published comparator reproduced within declared tolerance where feasible;
- reliability and state dependence explicitly separated;
- no disorder outcome used to choose thresholds;
- no NSD quantity used to define healthy reference regions.

## Current interpretation ceiling

This lane can establish independent native healthy reference distributions and movement envelopes.

It cannot:
- diagnose;
- set a disease cutoff;
- define a universal recovery threshold;
- define a universal healthy (chi);
- infer (Chi) or (Chi_{mathrm{arc}});
- claim baseline migration from cross-sectional data.
