# P0-D10 Dependence-Aware Lag-Covariance Sampling Uncertainty Plan

Date: 2026-09-11
Status: P0-D METHOD DIAGNOSIS / CALIBRATION. NOT P0-Q. NOT P1.
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum

## Problem narrowed by P0-D5/P0-D7/P0-D9

The estimator-native uncertainty chain now works mechanically from the NSD covariance Hankel to pole coordinates and carrier-subspace projectors. Local finite-difference propagation is highly stable. The remaining recurring defect is scale calibration of the sampling covariance root, especially as record duration and batch geometry change.

The current P0-D root treats contiguous disjoint record segments as repeated Hankel estimates. This is convenient but does not directly estimate the long-run covariance of the serially dependent lagged products that define each sample autocovariance.

## Statistical lineage

For a stationary multivariate time series, the joint sample autocovariances have a nontrivial asymptotic covariance structure (multivariate Bartlett-type formulas). More generally, heteroskedasticity-and-autocorrelation-consistent (HAC) estimators estimate the long-run covariance of dependent score/statistic-contribution sequences. Bartlett/Newey-West weighting provides a positive-semidefinite covariance construction under its standard formulation.

This suggests a natural NSD-specific diagnostic: treat the exact contributions to the native lag-covariance estimates as a multivariate time series and estimate their long-run variance rather than assuming disjoint batches are independent.

## Exact contribution representation

For NSD lag `l`, the current estimator is

`R_l = 1/(n-l) sum_{t=0}^{n-l-1} y_(t+l) y_t^T`.

Define an n-row contribution sequence for this lag by

`g_t(l) = [n/(n-l)] vec_F(y_(t+l) y_t^T)` for `t < n-l`, and zero otherwise.

Then, exactly,

`mean_t g_t(l) = vec_F(R_l)`.

Stacking all lags used by the Hankel therefore creates a contribution vector `g_t` whose sample mean is exactly the vector of native NSD lag-covariance coordinates. The zero-padded edge representation is finite-sample nonstationary near the final l samples; this is retained as a stated approximation rather than hidden.

## P0-D10 estimators compared

### A. Current disjoint-batch variance

For K equal contiguous segments, calculate the same native lag-covariance vector in each segment and use sample covariance of segment estimates divided by K. This mirrors the current P0-D5 logic at the unique-lag level.

### B. Bartlett HAC diagonal long-run variance

For each coordinate of the centered contribution sequence, estimate

`Omega = Gamma_0 + 2 sum_(h=1)^L [1 - h/(L+1)] Gamma_h`

and sampling variance of the sample mean as `Omega/n`.

P0-D10 initially evaluates **diagonal variance only**. That is sufficient to diagnose scale behavior without prematurely engineering a full high-dimensional covariance root.

## Development bandwidth surface

Evaluate fixed descriptive bandwidths:

- 0 samples (IID/zero-lag reference only)
- 8 samples
- 32 samples
- 128 samples

No bandwidth is selected or frozen from these post-result P0-D records. The purpose is to determine whether serial-dependence correction changes the duration-dependent scale behavior in the expected direction.

## Synthetic calibration

Use the same two-mode, four-channel architecture as the native uncertainty program:

- 3 Hz decay 0.6;
- 8 Hz decay 1.0;
- dt 0.02;
- block rows 12, hence native Hankel lags 1..23;
- durations 3600 and 7200;
- 24 independent process realizations;
- nominal, 10% white-sensor, and 10% colored-sensor (`rho=0.8`) conditions;
- disjoint batch counts 6 and 12.

For each method/bandwidth compare predicted diagonal sampling variance against empirical across-realization variance of the exact native lag-covariance coordinates:

- log-variance correlation;
- median predicted/empirical ratio;
- ratio p10/p90;
- median absolute log ratio;
- nonpositive predicted-variance count.

## Nonclaims

- No HAC bandwidth is selected.
- No full HAC covariance root is licensed.
- No neural-data stationarity assumption is asserted.
- No confidence convention is selected.
- No P0-Q/P1 uncertainty rule is frozen.
- The exact edge-padded contribution representation is algebraically exact for the sample mean, but its use in a stationary long-run covariance approximation remains a P0-D method hypothesis.

## Decision after mapping

If one or more dependence-aware surfaces reduce duration-dependent scale distortion without sacrificing variance-shape agreement, the next step is to construct and test a positive-semidefinite full covariance root for that class, then qualify it on untouched evidence. If not, preserve the failure and move to block-bootstrap or another estimator-native route.