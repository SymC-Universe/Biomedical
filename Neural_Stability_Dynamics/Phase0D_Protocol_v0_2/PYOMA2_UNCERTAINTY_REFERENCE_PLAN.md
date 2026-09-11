# pyOMA2 SSI-Uncertainty External Reference Plan

Date: 2026-09-10/11
Status: **P0 EXTERNAL CROSS-CHECK. NOT AN ENGINE DEPENDENCY AND NOT A P1 UNCERTAINTY FREEZE.**

## Why this reference is useful

The NSD uncertainty hold cannot be closed by attaching an arbitrary bootstrap interval to final modal estimates. The SSI literature propagates uncertainty from finite-data variation in the identified Hankel/subspace object through the system realization and onward to modal quantities.

`pyOMA_2` version 1.4.2 is a maintained MIT-licensed Operational Modal Analysis package that implements this chain for covariance/data-driven SSI. Its source explicitly:

1. divides the finite record into blocks;
2. estimates block-to-block Hankel variation and constructs a square-root covariance matrix `T`;
3. propagates that uncertainty through the SSI realization;
4. returns standard deviations for modal frequency, damping ratio and mode shape.

This makes it useful as an **independent executable reference**, not merely as literature prose.

## Firewall

The external reference runs in a separate GitHub Actions job and separate dependency environment. `pyOMA_2` is not imported by the NSD Engine, main P0 validation suite, or future production selector.

A successful external-reference run means only:

> an independently maintained implementation of the published SSI uncertainty chain can execute on NSD known-truth synthetic records, allowing us to examine calibration and implementation conventions.

It does not mean:

- NSD has implemented analytical SSI uncertainty;
- pyOMA2 assumptions are licensed for EEG;
- its block count, order, confidence convention or hard criteria become NSD defaults;
- its point estimator is byte-for-byte identical to the current NSD SSI-COV estimator.

## Initial reference construction

The first cross-check uses the established stationary two-mode stochastic linear construction with:

- 4 channels;
- 3 Hz and 8 Hz planted complex modes;
- fixed true order 4 for uncertainty isolation;
- 3600 samples at `dt=0.02`;
- 12 covariance block rows;
- 12 uncertainty blocks;
- 6 independent replicates.

For each planted positive complex mode, the external reference records:

- estimated natural frequency;
- reported frequency standard error;
- absolute frequency error divided by standard error;
- descriptive truth coverage under `estimate ± 1.96 SE`;
- corresponding damping-ratio quantities.

The `1.96` coverage calculation is a familiar descriptive reference only. It is **not** a frozen NSD confidence level.

## Decision after execution

Three outcomes are acceptable:

1. **Reference executes and uncertainty is directionally calibrated.** We may then reproduce the required mathematics locally, with independent tests against the reference, before considering any P1 uncertainty rule.
2. **Reference executes but calibration is poor or convention-sensitive.** Preserve that result and investigate assumptions/blocking/order effects.
3. **Reference cannot be made consistent with the present NSD estimator conventions.** Preserve the incompatibility and keep MFR-09 open rather than forcing transfer.

No result from this external job can independently authorize P1.
