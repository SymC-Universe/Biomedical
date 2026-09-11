# NSD P0-D5 Native-Hankel Sampling-Covariance Result

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Status: **P0-D SAMPLING-COVARIANCE CALIBRATION. PROMISING FOUNDATION; SCALE BIAS UNRESOLVED. NO MODAL INTERVAL OR P1 RULE FROZEN.**

## Purpose

The pyOMA2 external-reference audit showed that direct transfer of its finite-sample SSI uncertainty covariance to NSD is not licensed because pyOMA2 and NSD use different finite-sample covariance/Hankel estimators.

P0-D5 therefore tested one level lower than modal uncertainty: whether a single-record batch estimate of sampling covariance for the **exact NSD lag-specific covariance Hankel** reproduces the empirical across-realization variance structure of that Hankel.

## Candidate estimator

For each NSD record, contiguous equal-length batches were converted into Hankels using the same NSD lag-specific covariance denominators. If `h_k = vec(H_k)`, the exploratory single-record covariance estimate was

`Sigma_H_batch = [1/(K(K-1))] sum_k (h_k-h_bar)(h_k-h_bar)^T`.

This was explicitly treated as an approximation because contiguous batches are not generally independent, full-record covariance pairs cross batch boundaries, and finite-batch edge effects are lag dependent.

## Calibration design

- fixed known-truth two-mode stochastic linear system;
- four observed channels;
- 12 covariance block rows;
- record lengths 3600 and 7200 samples;
- batch counts 6 and 12;
- 24 independent process realizations;
- nominal and 10% white-sensor-noise conditions;
- 2304 nonzero/finite Hankel-entry variance comparisons per condition × duration × batch-count cell.

No batch count, duration, correction factor, confidence level or pass threshold was selected from the map.

## Results

| Condition | n | batches | median predicted / empirical variance | p10 | p90 | log-variance correlation | median |log ratio| |
|---|---:|---:|---:|---:|---:|---:|---:|
| nominal | 3600 | 6 | 1.0344 | 0.7628 | 1.2540 | 0.9684 | 0.1336 |
| nominal | 3600 | 12 | 0.8990 | 0.6921 | 1.0864 | 0.9709 | 0.1408 |
| nominal | 7200 | 6 | 1.2633 | 1.0365 | 1.5983 | 0.9751 | 0.2339 |
| nominal | 7200 | 12 | 1.2164 | 0.9852 | 1.5851 | 0.9717 | 0.1967 |
| white sensor 10% | 3600 | 6 | 1.0357 | 0.7650 | 1.2675 | 0.9673 | 0.1418 |
| white sensor 10% | 3600 | 12 | 0.9014 | 0.7029 | 1.1016 | 0.9699 | 0.1332 |
| white sensor 10% | 7200 | 6 | 1.2579 | 1.0142 | 1.6035 | 0.9725 | 0.2315 |
| white sensor 10% | 7200 | 12 | 1.2115 | 0.9708 | 1.5870 | 0.9695 | 0.1950 |

## Interpretation

The candidate captures the **shape of the Hankel sampling-variance field strongly** across both nominal and white-noise perturbation conditions: log-variance correlations are approximately `0.967–0.975` in every tested cell.

The variance scale is not yet stable enough to treat the candidate as calibrated. At 3600 samples, six batches are close to unit median scale while twelve batches modestly underestimate. At 7200 samples, both tested batch counts overestimate median empirical variance by roughly 21–26%.

The similarity of the nominal and white-noise patterns suggests that the dominant unresolved issue is not simply the added white sensor noise. Duration/batch structure and dependence/edge effects remain plausible contributors.

## Consequence

P0-D5 supports continuing the NSD-native uncertainty route, but **does not support propagating the present covariance estimate into authoritative modal standard errors yet**.

The next uncertainty step is therefore:

1. map variance-scale behavior against duration and batch geometry without selecting a correction on the same evidence;
2. investigate the analytical source of the scale drift, especially temporal dependence and cross-batch pair omission;
3. version any resulting correction/estimator;
4. qualify it on new independent P0-Q known-truth evidence;
5. only after Hankel-level qualification propagate uncertainty into poles/carriers/subspaces and calibrate those downstream objects.

A simple empirical multiplicative correction fitted to P0-D5 is **not** authorized.

## Reproducibility identity

GitHub Actions workflow: `NSD Phase0D P0-D5 Native Hankel Uncertainty`
Workflow run: `34566463681`
Job: `103159490225`
Source commit: `4ee20c3199ffb4188753c54e554747343fcd5d6d`
Artifact ID: `10186186058`
Artifact ZIP SHA-256: `d879dd78443b6780eafd6baee2bd292d8b48ad7bdc311cb37b4010b8ab7a7103`

## Disposition

**P0-D5 COMPLETE. FUNCTION-MAP FOUNDATION SUPPORTED; CALIBRATION LIMIT EXPOSED.**

This narrows the uncertainty problem without falsely closing it and does not reopen System Model v1.0.
