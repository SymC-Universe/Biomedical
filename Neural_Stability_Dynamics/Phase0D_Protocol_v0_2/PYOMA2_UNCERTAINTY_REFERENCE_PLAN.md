# pyOMA2 SSI-Uncertainty External Reference Plan

Date: 2026-09-10/11
Protocol: **General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum**
Status: **P0-Q EXTERNAL CROSS-CHECK. NOT AN ENGINE DEPENDENCY AND NOT A P1 UNCERTAINTY FREEZE.**

## Why this reference is useful

The NSD uncertainty hold cannot be closed by attaching an arbitrary bootstrap interval to final modal estimates. The SSI literature propagates uncertainty from finite-data variation in the identified Hankel/subspace object through the system realization and onward to modal quantities.

`pyOMA_2` version 1.4.2 is a maintained MIT-licensed Operational Modal Analysis package that implements this chain for covariance/data-driven SSI. Its source explicitly:

1. divides the finite record into blocks;
2. estimates block-to-block Hankel variation and constructs a square-root covariance matrix `T`;
3. propagates that uncertainty through the SSI realization;
4. returns standard deviations for modal frequency, damping ratio and mode shape.

This makes it useful as an **independent executable reference**, not merely as literature prose.

## v0.7.1A research role

This is `P0-Q`, not P0-D. It qualifies whether an external SSI uncertainty implementation can serve as a reference for a future NSD uncertainty derivation on known-truth synthetic systems. The current stationary two-mode construction is `NOMINAL_FUNCTION`; future perturbation/transition uncertainty checks, if justified, will be labeled separately.

No Function-Map success here can promote itself to P1. No Limit-Map discrepancy is repaired on the same decisive record.

## Firewall

The external reference runs in a separate GitHub Actions job and separate dependency environment. `pyOMA_2` is not imported by the NSD Engine, main P0 validation suite, or future production selector.

A successful external-reference run means only:

> an independently maintained implementation of the published SSI uncertainty chain can execute on NSD known-truth synthetic records, allowing us to examine calibration and implementation conventions.

It does not mean:

- NSD has implemented analytical SSI uncertainty;
- pyOMA2 assumptions are licensed for EEG;
- its block count, order, confidence convention or hard criteria become NSD defaults;
- its point estimator is byte-for-byte or estimator-covariance identical to the current NSD SSI-COV estimator.

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
2. **Reference executes but calibration is poor or convention-sensitive.** Preserve that result and investigate assumptions/blocking/order effects in P0-D/P0-Q as appropriate.
3. **Reference cannot be made consistent with the present NSD estimator conventions.** Preserve the incompatibility and keep MFR-09 open rather than forcing transfer.

Any estimator-convention discrepancy is pathway-specific method dependence and must remain visible. Similar point estimates cannot erase a covariance-estimator mismatch.

No result from this external job can independently authorize P1.
