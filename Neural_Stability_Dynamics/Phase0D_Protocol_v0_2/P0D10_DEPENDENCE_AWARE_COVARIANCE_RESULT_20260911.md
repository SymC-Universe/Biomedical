# P0-D10 Dependence-Aware Lag-Covariance Sampling Uncertainty Result

Date: 2026-09-11
Status: P0-D RESULT. METHOD DIAGNOSIS / CALIBRATION. NOT P0-Q. NOT P1.
Workflow run: `34612489422`
Job: `103306180257`
Artifact ID: `10268963492`
Artifact ZIP SHA256: `34a816fbf1e70b8529dcc094d8a867bf02c5eb2e031c1b73552d985fd5ef5d68`

## Question

Is the duration/batch-dependent scale error seen in the NSD-native uncertainty chain primarily explained by serial dependence in the lagged products used to estimate output autocovariances, and does a simple Bartlett-HAC correction solve it?

## Mechanical verification

Three dedicated tests passed:

1. the constructed lag-product contribution sequence has a sample mean exactly equal to the current native NSD lag-covariance vector;
2. zero-bandwidth HAC reproduces the ordinary IID variance-of-the-mean diagonal;
3. the FFT implementation agrees with a direct Bartlett-weighted autocovariance calculation.

Thus the P0-D10 comparison is mechanically tied to the exact native lag-covariance coordinates rather than a surrogate estimator.

## Central result

**Serial dependence is a major component of the sampling variance, but the tested finite-bandwidth Bartlett-HAC estimators do not yet replace the current disjoint-batch route.**

The zero-bandwidth/IID approximation severely underestimates empirical variance. Increasing the HAC bandwidth from 0 to 8 to 32 to 128 samples consistently increases predicted variance and, in most cells, strongly improves variance-shape agreement. This is the expected qualitative behavior if temporally extended covariance in the lag-product sequence is material.

However, bandwidth 128 still underestimates scale in many cells, while the existing disjoint-batch estimator is often closer to empirical variance.

## Representative results

### Nominal

At 3600 samples:

- disjoint batches K=6: median predicted/empirical ratio `0.830`, log-variance correlation `0.959`, median absolute log ratio `0.222`;
- disjoint batches K=12: `0.799`, `0.962`, `0.242`;
- HAC bandwidth 0: ratio `0.057`, correlation `0.659`;
- HAC bandwidth 32: ratio `0.311`, correlation `0.971`;
- HAC bandwidth 128: ratio `0.592`, correlation `0.975`, median absolute log ratio `0.524`.

At 7200 samples:

- batch K=6: ratio `0.637`, correlation `0.991`;
- batch K=12: `0.660`, `0.990`;
- HAC bandwidth 128: `0.531`, `0.989`.

### White sensor noise, 10%

At 3600 samples:

- batch K=6: ratio `1.258`;
- batch K=12: `1.178`;
- HAC bandwidth 128: `0.844`.

At 7200 samples:

- batch K=6: `1.003`;
- batch K=12: `1.023`;
- HAC bandwidth 128: `0.809`.

Here the batch estimator is particularly well-scaled at the longer duration. HAC 128 is competitive in shape but remains low in scale.

### Colored sensor noise, 10%, rho=0.8

At 3600 samples:

- batch K=6: ratio `0.998`, correlation `0.983`;
- batch K=12: `0.893`, `0.969`;
- HAC bandwidth 128: `0.607`, `0.966`.

At 7200 samples:

- batch K=6: `0.840`, `0.973`;
- batch K=12: `0.846`, `0.969`;
- HAC bandwidth 128: `0.637`, `0.971`.

## Interpretation

P0-D10 supports three bounded conclusions.

1. **An IID treatment is unacceptable for these lag-covariance sampling variances.** The missing temporal dependence is large, not a small correction.
2. **Dependence-aware long-run covariance is scientifically well-motivated and moves in the correct direction**, but the tested fixed Bartlett bandwidths do not yet provide a generally calibrated replacement.
3. **The current disjoint-batch root remains a viable development candidate.** P0-D10 does not justify discarding it. Its shortcomings should be compared against longer-bandwidth/automatic-HAC and block-resampling alternatives rather than assumed away.

The fact that HAC variance-shape correlations can become very high while scale remains low reinforces the P0-D5/P0-D7 distinction between recovering the geometry of uncertainty and calibrating its absolute magnitude.

## What is not licensed

- bandwidth 128 is not selected;
- no automatic bandwidth rule is selected;
- no full HAC covariance matrix/root is licensed;
- no batch count is selected;
- no confidence convention or multiplicity rule is selected;
- no P0-Q or P1 uncertainty rule is frozen;
- no neural-data stationarity claim is made.

## Next method candidates

The next P0-D comparison should not merely extend one bandwidth until it happens to fit these records. It should compare principled dependence-aware candidate classes under a frozen development surface, including:

- longer-bandwidth Bartlett/HAC behavior and data-independent scaling surfaces;
- an established automatic bandwidth-selection rule evaluated as a method, not tuned to these outcomes;
- moving-block or stationary-bootstrap covariance estimates preserving temporal dependence;
- the existing disjoint-batch estimator as the incumbent comparator.

A candidate should advance only if it improves calibration without sacrificing estimator identity, positive-semidefinite covariance structure, reproducibility, or independence requirements.