# NSD P0-Q pyOMA2 SSI-Uncertainty External Reference Result

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Status: **P0-Q EXTERNAL REFERENCE EXECUTED. DIRECT UNCERTAINTY TRANSFER NOT AUTHORIZED. P1 RULE NOT FROZEN.**

## Purpose

The goal was not to adopt pyOMA2 as the NSD Engine. The goal was to determine whether an independently maintained covariance-SSI implementation of published analytical uncertainty machinery could serve as an executable reference for the NSD uncertainty derivation.

The external job also compared the finite-sample Hankel/point-estimator convention with the current NSD SSI-COV implementation before any uncertainty transfer was considered.

## Execution identity

GitHub Actions workflow: `NSD Phase0D pyOMA2 SSI-Uncertainty Reference`
Run: `34565920493`
Job: `103157903293`
Source commit: `7e980435ef694081280ea4a9a3843cf806f1b512`
External package: `pyOMA_2==1.4.2`
External environment observed in the run: NumPy `2.5.3`, SciPy `1.18.1`, Python `3.13.15`
Artifact ID: `10186000704`
Artifact ZIP SHA-256: `5421575706d9f0325341305501842d077dd0a0f9dbe12f84320ffea845fa9257`
Artifact contents: `pyoma2_uncertainty_reference.json`, `pyoma2_point_compatibility.json`.

## Mechanical result

The external implementation completed its covariance-SSI Hankel assembly, covariance-of-Hankel calculation, increasing-order SSI realization, uncertainty propagation, modal-parameter calculation, and the independent point-estimator compatibility audit without a mechanical failure.

This establishes that the external uncertainty route is executable on the current NSD known-truth synthetic construction.

## Uncertainty reference result

Across six independent records and twelve matched positive-frequency modes:

- median frequency `|error| / SE`: `0.9368357788`;
- 90th percentile frequency `|error| / SE`: `1.9931702460`;
- descriptive frequency coverage under `estimate ± 1.96 SE`: `10/12 = 0.8333333333`;
- median damping `|error| / SE`: `0.8475438835`;
- 90th percentile damping `|error| / SE`: `1.7677160537`;
- descriptive damping coverage under `estimate ± 1.96 SE`: `11/12 = 0.9166666667`.

The familiar `1.96` multiplier was used only as a descriptive calibration probe. It is not an NSD confidence convention and is not frozen.

The finite standard errors and order-one error/SE ratios show that the uncertainty machinery is informative enough to remain a serious reference candidate. The small sample, however, does not establish nominal confidence coverage. In particular, two frequency estimates and one damping estimate exceeded the descriptive ±1.96-SE interval across the twelve matched mode observations.

## Point-estimator / Hankel compatibility result

The two implementations use the same broad covariance-SSI block geometry but not the same finite-sample covariance estimator.

Current NSD `output_covariances` uses, for lag `l`, all available pairs and divides by `n-l`.

The pyOMA2 covariance-Hankel implementation uses a common aligned interval with `N = n-(2b-1)` across the Hankel blocks. Therefore the finite-sample Hankel matrices and their covariance structures are not identical even when the asymptotic target is closely related.

The observed discrepancy shrank with record length:

### n = 1800
- median relative difference between the NSD and pyOMA2 matched pole estimates: `0.0007898`;
- maximum matched-pole difference: `0.0019573`;
- median relative Frobenius Hankel difference: `0.0048487`;
- median normalized singular-spectrum difference: `0.0013343`.

### n = 3600
- matched-pole median: `0.0003150`;
- matched-pole maximum: `0.0006269`;
- Hankel difference median: `0.0020849`;
- singular-spectrum difference median: `0.0008768`.

### n = 7200
- matched-pole median: `0.00016684`;
- matched-pole maximum: `0.00024448`;
- Hankel difference median: `0.0011379`;
- singular-spectrum difference median: `0.00032748`.

These results are consistent with a small finite-sample convention difference that diminishes with longer records. They do **not** establish equality of the estimators.

## Critical consequence

The pyOMA2 uncertainty matrix/covariance propagation is tied to the finite-sample Hankel estimator used by pyOMA2. Close point estimates are therefore insufficient to authorize direct reuse of its uncertainty matrix for the current NSD variable-denominator covariance estimator.

The scientifically defensible result is:

> pyOMA2 provides a useful external mathematical and executable reference for covariance-SSI uncertainty, but direct transfer of its finite-sample uncertainty object to NSD is not licensed. NSD must derive or otherwise justify uncertainty for the estimator it actually computes, and then calibrate that implementation against known truth and an external reference.

## v0.7.1A interpretation

This is P0-Q qualification evidence for a `NOMINAL_FUNCTION` uncertainty-reference pathway. It does not establish a universal uncertainty rule, a P1 interval convention, or neural-data validity.

The estimator-method pathway is only **partially independent**: pyOMA2 is independently maintained and independently implemented, but it belongs to the same covariance-SSI methodological family. The finite-sample estimator mismatch is explicitly retained rather than hidden.

## MFR-09 consequence

MFR-09 remains open. Its unresolved work is now narrower:

1. derive/implement uncertainty for the actual NSD finite-sample covariance/Hankel estimator, or change the point estimator only through a separately justified versioned scientific decision;
2. verify propagation into poles/frequencies/decay/carrier quantities;
3. calibrate marginal and, where needed, simultaneous uncertainty on new known-truth P0-Q evidence;
4. incorporate model-order/crowding ambiguity rather than representing all uncertainty as a single standard error;
5. only then propose a P1 `INDETERMINATE` adjudication convention for review and freeze.

No confidence level, coverage target, multiplicity correction, P1 threshold, or `INDETERMINATE` boundary is frozen by this result.

## Disposition

**P0-Q EXTERNAL REFERENCE COMPLETE; DIRECT TRANSFER REFUSED.**

This is progress, not a failed route: the external reference has successfully reduced MFR-09 from an undefined-method hold to a concrete NSD-native derivation-and-calibration problem.
