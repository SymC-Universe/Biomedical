# Kizilirmak C+D execution failure 01

**Date:** 25 September 2026
**Task:** `GRI_BIOCHI_KIZILIRMAK_C_D_EXECUTION_20260925`
**Workflow run:** `36189395075`
**Job:** `108250571891`
**Disposition:** `MECHANICAL_DEPENDENCY_API_FAILURE`

## Failure

The frozen analysis stopped inside the native-dynamics pre-gate before any RNA values were opened.

Runtime error:

`AttributeError: module 'numpy' has no attribute 'trapz'`

The GitHub runner installed NumPy 2.5.3, in which `np.trapz` is no longer available. The AUC calculation therefore failed before the native B/R oscillation gate could be adjudicated.

## Root cause

Dependency API drift. The intended trapezoidal integration operation is unchanged and is available as `numpy.trapezoid`.

## Outlier / anomaly adjudication

This is an implementation/environment failure, not a biological outlier and not a scientific failure. It does not alter the frozen estimator, source, carrier, endpoint, direction, null, or claim ceiling.

## Scientific exposure

- No Table S3 expression values were opened.
- No chi_GRI values were calculated.
- No A/B/D result was generated.
- The native dynamics loop began reading the frozen source matrices, but no complete clone-level dynamical endpoint was emitted or inspected before the exception.

## Repair

Replace `np.trapz(y, dx=dt_min)` with the API-equivalent `np.trapezoid(y, dx=dt_min)`. Rerun the unchanged frozen analysis.

## Safe resume point

Re-execute the native-dynamics gate from the pinned source hashes under the existing execution freeze.
