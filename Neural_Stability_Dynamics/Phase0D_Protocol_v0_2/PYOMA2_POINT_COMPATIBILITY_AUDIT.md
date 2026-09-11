# pyOMA2 Point-Estimator Compatibility Audit

Date: 2026-09-10/11
Status: **P0 EXTERNAL-REFERENCE COMPATIBILITY TEST. NO UNCERTAINTY TRANSFER AUTHORIZED.**

## Why this audit is necessary

The pyOMA2 reference demonstrated that an independently maintained covariance-SSI implementation can propagate finite-record uncertainty to modal frequency and damping on the NSD synthetic construction. That is useful, but its uncertainty matrix describes **its own finite-sample Hankel estimator**, not automatically ours.

The NSD and pyOMA2 covariance Hankels have the same block dimensions and expected positive-lag structure, but their finite-sample covariance estimators differ:

- NSD currently estimates lag `k` with all `n-k` available sample pairs and denominator `n-k`.
- pyOMA2 `method='cov'` aligns every future/past block to one common interval of length `N = n-(2b-1)` and divides every covariance block by the same `N`.

Both target the same population lag covariance under stationarity, but equality in expectation does not imply equal finite-sample covariance.

## P0 test

On the same stationary two-mode stochastic system, at fixed order 4 and 12 block rows, the external-reference workflow compares across 1800, 3600 and 7200 samples:

1. relative Frobenius difference between the two Hankel matrices;
2. difference between their normalized singular spectra;
3. NSD-versus-pyOMA2 positive-complex pole estimates;
4. each implementation's pole error against known truth.

Six independent replicates are used at each duration.

## Interpretation firewall

No compatibility cutoff is chosen before or after this run.

If point estimates converge closely with duration, that supports using pyOMA2 as a **cross-check and derivational reference**, but it still does not justify copying its uncertainty matrix `T` into NSD because `T` is tied to pyOMA2's specific Hankel estimator.

If the point estimates diverge materially, the uncertainty transfer route is even less defensible and MFR-09 remains open.

The likely mathematically clean route, if local analytical uncertainty is pursued, is to derive or implement block-to-block covariance for **the exact NSD Hankel estimator**, then validate the propagated modal uncertainty against both known-truth repetition and the external reference where conventions overlap.

No result from this audit authorizes P1 or EEG analysis.
