# BioSystems adversarial Round 1 - external H1 race sensitivity freeze

**Date:** 23 September 2026
**Status:** FROZEN BEFORE ROUND-1 SENSITIVITY OUTCOME OPENING
**Branch:** `biosystems-adversarial-r1-20260923`
**Parent release:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Program authority:** SymC General Operations Manual v0.8.4
**Role:** post-result adversarial sensitivity only; cannot upgrade, rescue, or rewrite the original frozen P1 classification.

## Motivation

Adversarial Round 1 correctly notes that the only externally transported endpoint, H1 methylation spectral organization, is vulnerable to sample-level covariance not destroyed by the probe-marginal construction null.

The original external prostate primary 450K set contains 25 AA and 5 EA paired participants, and the source study was designed around race-specific molecular structure. The original P1 H1/H2/H3a architecture lane used **tumor samples only**; adjacent samples were used for symmetric probe eligibility and the separately declared tumor-normal contrast. Therefore pooled tumor/normal state is not a candidate explanation for the external H1 magnitude, but race-associated sample structure remains a legitimate measured alternative.

## Frozen question

Does the external tumor-only H1 signal remain detectable after removing the known AA/EA sample-level axis from every retained CpG, and within the AA-only subset where the race axis is absent by construction?

## Frozen lanes

1. **PRIMARY_450K_N30**
   - same 30 participants as original P1;
   - same tumor samples;
   - same state-symmetric common-probe eligibility;
   - same 22,601 C1 carrier and technical mask.

2. **SENSITIVITY_450K_N32**
   - same complete 32-pair pool as original mandatory sensitivity.

3. **SENSITIVITY_EPIC_N26**
   - same 26 complete EPIC pairs;
   - same C1-compatible intersected carrier.

Each lane retains:
- PRIMARY_PUBLICATION probe track;
- MASKED_TECHNICAL probe track.

## Frozen analyses

For each lane/track report:

### A. Raw H1 reconstruction
Recompute the original tumor-only H1 using the existing B=999 deterministic column-permutation null. This is a regression check only.

### B. Race-residualized H1
Parse race only from exact source sample titles (`_AA`, `_EA`). Fit, independently for each retained CpG across tumor samples,

`beta_probe = intercept + I(EA) + residual`.

No outcome, Hallmark, clinical, purity, batch, age, or other variable enters this residualization.

Apply the same H1 spectral-concentration statistic to the residual matrix. The B=999 null independently permutes the residual values within each CpG, preserving each residual marginal multiset while destroying residual cross-probe patient covariance.

### C. AA-only H1
Within each lane, if at least 20 AA tumor participants are present, compute H1 on AA tumors only using the same retained-probe carrier and B=999 independent within-probe patient permutations.

AA-only is a supporting sensitivity because n differs from the original n=30 calibration and therefore its raw S_spec magnitude is not directly compared to the original value.

## Frozen interpretation

Primary race-sensitivity decision is based only on PRIMARY_450K_N30 race-residualized H1:

- `R1_H1_RACE_ROBUST`: effect > 0 and empirical upper-tail p <= 0.05.
- `R1_H1_RACE_SENSITIVE`: effect <= 0 or p > 0.05.
- `R1_H1_RACE_NOT_EVALUABLE`: race labels or source identity fail.

Cross-platform race robustness is supported only if the EPIC race-residualized lane also has effect > 0 and p <= 0.05.

AA-only results are descriptive/supporting and cannot rescue a failed race-residualized primary result.

## Nonclaims

This sensitivity does **not**:
- adjust tumor purity or stromal/immune mixture;
- adjust age, sex, center, plate, Sentrix position, or batch unless those covariates are independently source-bound in a later separately frozen test;
- convert H1 into a biological mechanism;
- strengthen H2/H3a;
- alter the original `P1_REPRESENTATION_DEPENDENT` classification;
- make the B=999 Monte Carlo floor more precise.

The original P1 remains the publication lineage. This test exists solely to determine whether one known source-level sample axis explains H1.


## Pre-outcome implementation amendment v1.1

Workflow run `35812072624` failed after completing the 450K calculations but before writing or printing any endpoint result because the EPIC subset contains only EA-labeled participants. The failure was:

`ValueError: race residualization requires AA+EA, got ['EA']`.

No numerical H1 sensitivity outcome was opened from that run.

This is a source-structure implementation defect, not a scientific outcome. The source identity already establishes that the EPIC subset is race-homogeneous. The following rule is therefore frozen before retry:

- if a lane contains both AA and EA, perform the frozen per-CpG race residualization;
- if a lane contains only one race, mark `H1_RACE_RESIDUAL` as `NOT_IDENTIFIABLE_SINGLE_RACE` and do not fabricate a regression coefficient;
- a single-race lane is reported as a race-homogeneous supporting sensitivity using its raw H1 result, because the between-race axis is absent by construction;
- the primary decision remains based only on mixed-race `PRIMARY_450K_N30` race-residualized H1;
- the EPIC lane cannot rescue a failed primary and cannot be described as a successful race-adjusted regression.

The cross-platform wording is correspondingly narrowed: if primary race-residualized H1 passes and the race-homogeneous EPIC raw H1 remains positive/significant under its original frozen null, the result is described as `PRIMARY_RACE_ROBUST_WITH_SINGLE_RACE_EPIC_SUPPORT`, not as two-platform race residualization.

No participant, probe, endpoint, null, B, threshold, source, or original P1 interpretation changes.
