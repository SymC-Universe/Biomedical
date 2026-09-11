# P0-D13 Chi Lineage Through the Repeated-Root Boundary Result

Date: 2026-09-11
Status: **P0-D RESULT. NOT ATLAS CALIBRATION. NOT P0-Q. NOT P1.**
Workflow run: `34616178290`
Job: `103318559137`
Artifact ID: `10271315114`
Artifact ZIP SHA256: `5d0444c4f3fdee538e66b551d879d562c966221f68b0f75a95b057c33e5a327e`

## Question

Can a truth-blind pole-continuity rule preserve the identity of a supported low-frequency second-order lineage as its true chi crosses `chi=1`, and does the current SSI-COV estimator reconstruct the corresponding branch-complete chi coordinate?

## Mechanical result

Twelve dedicated chi, participation and lineage tests passed. Exact-pole tests confirmed that the continuity algorithm can, in principle, carry a low-frequency conjugate pair through a repeated root into a real split without truth labels.

## Central result

**Lineage identity was preserved extremely well, but the current finite-sample SSI-COV reconstruction did not reliably follow the true underdamped-to-overdamped branch transition.**

This separates two problems that were previously entangled:

1. **which dynamical object is being followed?**
2. **has the estimator correctly reconstructed that object's pole branch and chi?**

The first problem performed well. The second remains open.

## Lineage identity

After the initial `chi=0.50` record, retrospective target-identity correctness was `1.0` for every successful point from `chi=0.70` through `chi=1.50` in both visibility conditions.

At the first point under fixed-reference balance, identity correctness was `0.875`; under pointwise 50/50 output balance it was `1.0`.

Thus the continuity tracker did not generally jump from the low-frequency target to the high-frequency companion when the target approached or crossed the repeated-root boundary.

## Chi reconstruction near the boundary

### Fixed-reference output balance

Target observable participation remained roughly `0.48-0.54` across the path.

Representative median chi estimates/errors:

| truth chi | successful | median estimate | median abs error | estimated complex-pair fraction |
|---:|---:|---:|---:|---:|
| 0.50 | 8/8 | 0.466 | 0.037 | 0.875 |
| 0.70 | 7/8 | 0.723 | 0.031 | 1.000 |
| 0.85 | 7/8 | 0.806 | 0.080 | 0.857 |
| 0.93 | 7/8 | 0.939 | 0.016 | 1.000 |
| 0.97 | 7/8 | 0.875 | 0.095 | 0.714 |
| 0.99 | 7/8 | 0.973 | 0.075 | 0.571 |
| 1.00 | 7/8 | 0.896 | 0.104 | 0.714 |
| 1.01 | 7/8 | 0.957 | 0.093 | 0.571 |
| 1.03 | 7/8 | 0.936 | 0.094 | 0.857 |
| 1.07 | 6/8 | 0.998 | 0.084 | 0.500 |
| 1.15 | 7/8 | 0.942 | 0.215 | 0.714 |
| 1.30 | 7/8 | 0.900 | 0.401 | 0.571 |
| 1.50 | 6/8 | 1.249 | 0.527 | 0.333 |

### Pointwise 50/50 output balance

Holding observable participation exactly at 50/50 did not remove the branch problem.

| truth chi | successful | median estimate | median abs error | estimated complex-pair fraction |
|---:|---:|---:|---:|---:|
| 0.50 | 8/8 | 0.495 | 0.031 | 1.000 |
| 0.70 | 8/8 | 0.684 | 0.034 | 1.000 |
| 0.85 | 8/8 | 0.812 | 0.057 | 1.000 |
| 0.93 | 7/8 | 0.867 | 0.126 | 0.714 |
| 0.97 | 8/8 | 0.907 | 0.063 | 1.000 |
| 0.99 | 8/8 | 0.982 | 0.040 | 0.750 |
| 1.00 | 7/8 | 0.944 | 0.056 | 0.714 |
| 1.01 | 8/8 | 0.848 | 0.162 | 1.000 |
| 1.03 | 8/8 | 0.908 | 0.122 | 0.875 |
| 1.07 | 6/8 | 0.947 | 0.124 | 0.667 |
| 1.15 | 7/8 | 1.007 | 0.143 | 0.429 |
| 1.30 | 6/8 | 0.924 | 0.376 | 0.833 |
| 1.50 | 7/8 | 0.896 | 0.623 | 0.571 |

Every successful fit in the summaries remained stable. The issue is therefore not simple instability. The fitted target lineage is frequently represented as a stable complex pair when the known truth has already split into two stable real poles.

## Interpretation

P0-D13 supports four bounded conclusions.

1. **Lineage continuity is useful and separable from branch estimation.** The tracker can preserve the identity of the target dynamical family even when the pole representation becomes noisy near the repeated-root boundary.
2. **Equal observable participation does not cure the branch problem.** The failure above chi=1 is not explained solely by the target fading from the record.
3. **The current finite-sample SSI-COV implementation exhibits strong branch ambiguity/compression near and above the boundary under this synthetic design.** Estimated chi is often pulled toward the neighborhood of 1 and can remain on the complex side when truth is overdamped.
4. **A branch-complete mathematical chi does not automatically imply a branch-complete estimator.** The invariant formula is exact for a correctly reconstructed licensed 2D factor; the current bottleneck is identifying that factor's finite-sample dynamics accurately enough.

## Relation to perturbation theory

Repeated/defective eigenvalues are intrinsically sensitive to perturbations, while invariant-subspace formulations are the natural objects for clustered/multiple eigenvalues. P0-D13 is consistent with that distinction: identity of the larger dynamical object can remain coherent while the internal eigenvalue representation fluctuates strongly near the boundary.

This does not establish that a subspace-restricted trace/determinant estimator will solve the problem. That is a testable next candidate.

## Static pairing limitation of this surface

The high-frequency companion remained a complex pair, so the median number of algebraically valid static second-order partitions was `1` throughout the successful records. P0-D13 therefore demonstrates **lineage identity through branch ambiguity**, but it does not yet demonstrate that lineage resolves an otherwise ambiguous four-real-pole pairing problem.

A separate dual-real-lineage stress is required before making that stronger claim.

## Next P0-D question

Determine whether the overdamped compression is:

- a finite-record sampling effect;
- a measurement-noise effect;
- a covariance-SSI realization bias under weak second-root support;
- or a limitation already present in the population covariance-Hankel representation.

The clean next experiment is to compare exact population covariance-Hankel recovery against finite-sample recovery over record length and noise on the same single second-order systems.

## Nonclaims

- No real-data lineage rule is frozen.
- No continuity threshold is selected.
- No neural chi range is inferred.
- No Atlas evidence is used.
- No system chi is admitted.
- No P0-Q or P1 rule is changed.
