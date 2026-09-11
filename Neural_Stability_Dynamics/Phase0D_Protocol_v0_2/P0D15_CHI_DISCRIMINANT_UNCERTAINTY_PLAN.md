# P0-D15 Chi and Normalized-Discriminant Uncertainty Plan

Date: 2026-09-11
Status: **P0-D UNCERTAINTY / BOUNDARY MAPPING. NOT P0-Q. NOT P1.**
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum

## Question

Can the NSD-native Hankel sampling-covariance root be propagated directly to the branch-complete second-order coordinate `chi` and to the normalized discriminant

`Delta_chi = chi^2 - 1`,

so that finite-sample uncertainty near the repeated-root boundary is represented as coordinate-placement uncertainty rather than a forced complex/real branch label?

## Why Delta_chi is useful

For a licensed real two-dimensional second-order lineage,

`chi = -tr(B)/(2 sqrt(det(B)))`

and

`Delta_chi = chi^2 - 1 = (tr(B)^2 - 4 det(B))/(4 det(B))`.

Therefore:

- `Delta_chi < 0`: underdamped/complex side;
- `Delta_chi = 0`: repeated-root boundary;
- `Delta_chi > 0`: overdamped/real-split side.

P0-D14 showed that the exact population covariance-Hankel recovers this branch correctly, while finite samples can place the point on the wrong side. The next step is to quantify that uncertainty without freezing a branch threshold.

## Estimator-native propagation

For each finite record:

1. build the exact current NSD lag-specific covariance Hankel `H`;
2. build the current P0-D contiguous-batch Hankel covariance root `T`;
3. fit the fixed-order-2 SSI realization from `H`;
4. reconstruct the supplied two-pole factor invariants `chi`, `gamma`, `omega_n`, and `Delta_chi`;
5. perturb `vec_F(H)` symmetrically along every column of `T`;
6. refit the same order-2 SSI realization;
7. estimate first-order derivatives and variance for `chi` and `Delta_chi`.

No branch is accepted/rejected from the propagated variance in P0-D15.

## Calibration surface

Single known second-order component:

- `omega_n = 2*pi*2 Hz`;
- chi values `[0.80, 0.95, 0.99, 1.00, 1.01, 1.05, 1.20, 1.50]`;
- record lengths `[8000, 32000]`;
- 16 independent process realizations per cell;
- fixed order 2;
- block rows 30;
- 6 fixed output channels;
- no added measurement noise in the primary calibration, because P0-D14 showed 3% independent white noise had negligible effect relative to finite-record variability;
- batch counts `[6,12]`;
- finite-difference epsilons `[0.25,0.50]`.

## Diagnostics

For each chi, duration and batch count, record:

- empirical across-realization variance of fitted chi;
- mean predicted chi variance;
- predicted/empirical chi-variance ratio;
- empirical across-realization variance of `Delta_chi`;
- mean predicted `Delta_chi` variance;
- predicted/empirical discriminant-variance ratio;
- finite-difference epsilon stability;
- fraction of records whose point estimate has the same discriminant sign as truth;
- descriptive `|Delta_chi_est|/SE(Delta_chi)` distribution.

The last quantity is diagnostic only. No cutoff such as 1, 1.96, 2 or 3 is selected here.

## Interpretation logic

A useful outcome is not necessarily perfect branch classification. The desired result is a coherent uncertainty object that grows or becomes weakly separated from zero where P0-D14 showed finite-sample branch ambiguity.

If propagated discriminant variance tracks empirical variability reasonably, a later untouched P0-Q study can qualify a confidence/indeterminacy convention.

If it fails badly, the coordinate uncertainty must be recalibrated before any branch-aware chi map is admitted.

## Nonclaims

- No confidence level is selected.
- No `INDETERMINATE` cutoff is selected.
- No branch threshold is selected.
- No batch count or epsilon is frozen.
- No Atlas value, phenotype or outcome is used.
- No neural chi range or system chi is admitted.
- No P0-Q or P1 rule is changed.
