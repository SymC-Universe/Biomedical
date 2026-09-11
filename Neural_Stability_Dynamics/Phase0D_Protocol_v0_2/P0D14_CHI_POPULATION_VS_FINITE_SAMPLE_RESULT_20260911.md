# P0-D14 Population vs Finite-Sample Chi Branch Diagnosis Result

Date: 2026-09-11
Status: **P0-D RESULT. NOT ATLAS CALIBRATION. NOT P0-Q. NOT P1.**
Workflow run: `34616553178`
Job: `103319816905`
Artifact ID: `10271061257`
Artifact ZIP SHA256: `e4d1a82439af7b172866b497d2b46d08285a819a9e0ba302d0dcda5fcd7794d8`

## Question

Does the chi branch compression seen in P0-D11/P0-D13 already exist in the exact population covariance-Hankel representation, or is it a finite-record structural-resolution problem?

## Mechanical result

Two dedicated population-covariance chi tests passed. The exact-population Hankel uses the same positive-lag block geometry and fixed-order SSI realization as the current NSD SSI-COV engine.

## Central result

**The exact population covariance-Hankel recovers the constructed chi essentially to machine precision on both sides of the repeated-root boundary. The branch-compression problem is therefore finite-sample/conditioning related, not a structural inability of the current covariance-SSI realization to represent branch-complete chi.**

## Exact population recovery

| chi truth | chi estimate | pair branch | population `s2/s1` | fast/slow pole ratio |
|---:|---:|---|---:|---:|
| 0.80 | 0.800000000000001 | complex | 0.2297 | N/A |
| 0.99 | 0.990000000000000 | complex | 0.1076 | N/A |
| 1.00 | 1.000000000000002 | repeated real root | 0.1035 | 1.000 |
| 1.01 | 1.010000000000001 | real split | 0.0996 | 1.327 |
| 1.20 | 1.199999999999997 | real split | 0.0503 | 3.472 |
| 1.50 | 1.500000000000007 | real split | 0.02084 | 6.854 |
| 2.00 | 1.999999999999996 | real split | 0.007194 | 13.928 |

The population third singular direction remained at numerical scale, about `6.6e-16` to `9.6e-16` of the leading singular value. Thus the population object remains genuinely rank 2 throughout the surface.

## Structural-support mechanism

Although the exact population rank remains two, its **second supported direction becomes progressively weaker relative to the first** as chi moves deeper onto the overdamped branch:

- `s2/s1 ≈ 0.1035` at chi=1;
- `0.0503` at chi=1.2;
- `0.02084` at chi=1.5;
- `0.00719` at chi=2.0.

At the same time the two real pole timescales separate strongly. The theoretical magnitude ratio grows from `1` at the repeated root to about `3.47`, `6.85`, and `13.93` at chi 1.2, 1.5 and 2.0 respectively.

Therefore deeper overdamping does not remove chi mathematically. It makes the second dynamical direction increasingly difficult to resolve against finite-sample covariance error.

## Finite-sample length effect

Increasing record length from 8000 to 32000 samples materially improved recovery for moderate overdamping.

### chi=1.20

At 8000 clean samples:

- `7/8` successful;
- median chi estimate `0.916`;
- median absolute error `0.284`;
- complex-pair fraction `0.714`.

At 32000 clean samples:

- `8/8` successful;
- median chi estimate `1.135`;
- median absolute error `0.068`;
- complex-pair fraction `0.125`.

### chi=1.50

At 8000 clean samples:

- `6/8` successful;
- median chi estimate `1.156`;
- median absolute error `0.344`;
- complex-pair fraction `0.167`.

At 32000 clean samples:

- `8/8` successful;
- median chi estimate `1.459`;
- median absolute error `0.062`;
- complex-pair fraction `0.375`.

The longer record therefore greatly improves the scalar estimate, although branch classification can remain noisy near weak support.

### chi=2.00

The deeper overdamped case remains difficult even at 32000 samples:

- 8000 samples: `3/8` successful, median chi `0.844`, median absolute error `1.156`;
- 32000 samples: `5/8` successful, median chi `1.142`, median absolute error `0.858`.

This is consistent with the very weak population second direction (`s2/s1 ≈ 0.0072`) and large true pole-timescale ratio (`~13.93`).

## Measurement-noise comparison

Adding independent 3% channel-SD white measurement noise changed the finite-sample results negligibly across the surface. This matches the expectation that independent measurement noise does not alter the population positive-lag covariance, although it can contribute finite-sample variance.

Within this stress, ordinary measurement noise is not the dominant cause of branch compression.

## Interpretation

P0-D14 supports the following bounded conclusions:

1. **A branch-complete chi coordinate exists in the current model/estimator architecture.** Exact population covariance recovers underdamped, repeated-root and overdamped chi correctly.
2. **The practical limit is information/resolution, not algebraic definition.** The second supported covariance-Hankel direction shrinks sharply as overdamped timescales separate.
3. **Finite-sample estimates can be biased toward the neighborhood of chi≈1 or even the wrong complex/real representation while the underlying population chi is well defined.**
4. **Longer records can recover moderate overdamping substantially better.** No record-length threshold is licensed from this development surface.
5. **A point estimate alone is insufficient near the branch boundary or under weak second-direction support.** The next useful object is uncertainty on chi and on the normalized discriminant `delta_n = chi^2 - 1`, not an immediate hard branch label.

## Consequence for pre-Atlas mapping

The Atlas is not needed to define the component coordinate. For an admitted supported second-order lineage, chi can be derived independently from its dynamical invariants. What remains to be earned before neural system-level mapping is:

- reliable lineage/component admission;
- participation architecture for conglomeration;
- uncertainty/resolution on chi and branch placement;
- explicit refusal when the second structural direction is not sufficiently resolved.

The Atlas can then evaluate where those independently derived coordinates correspond to function, perturbation, boundaries and natural limits without having selected the coordinate formula.

## Nonclaims

- No neural record length is selected.
- No minimum `s2/s1` or `s2/s3` support threshold is selected.
- No confidence or branch-indeterminate rule is frozen.
- No biological participation weight is selected.
- No neural chi range or target zone is inferred.
- No P0-Q or P1 rule is changed.
