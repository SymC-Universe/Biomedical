# P0-D11 Pre-Atlas Chi Reconstruction and Conglomeration Result

Date: 2026-09-11
Status: **P0-D RESULT. NOT ATLAS CALIBRATION. NOT P0-Q. NOT P1.**
Workflow run: `34615042400`
Job: `103314729489`
Artifact ID: `10269963528`
Artifact ZIP SHA256: `69d68a0ad5eb68d5c836c148f2b73f000f256fee556144789fd8f09ed6a4fb6b`

## Question

Can the current NSD SSI-COV engine reconstruct a known second-order chi coordinate before any Neurostability Atlas value is used, and can a simple multi-component conglomerate chi be reconstructed when two second-order components are forced into the fitted model?

## Mathematical construction

The synthetic component was generated from

`A_chi = omega_n * [[0,1],[-1,-2 chi]]`

with dimensionless state `u=q'/omega_n`, giving characteristic polynomial

`s^2 + 2 chi omega_n s + omega_n^2`.

For one licensed two-pole factor,

`chi = -(lambda_1 + lambda_2) / (2 sqrt(lambda_1 lambda_2))`.

This pair-invariant formula applies on the complex, repeated-root and real branches when the two poles genuinely belong to the same second-order factor.

The developmental two-component candidate was

`chi_C = sqrt(sum_j (chi_j omega_n,j)^2) / sqrt(sum_j omega_n,j^2)`

with equal component weights.

No Atlas value, phenotype, outcome, target zone or historical SymC value was used to choose or tune these formulas.

## Surface A: single component

All 8 replicates completed from chi 0.20 through 0.99. The exact critical point completed in 7/8. Overdamped completion became less reliable at larger chi.

| chi truth | branch | successful | median chi estimate | median absolute chi error | complex-pair fraction |
|---:|---|---:|---:|---:|---:|
| 0.20 | under | 8/8 | 0.206 | 0.019 | 1.000 |
| 0.50 | under | 8/8 | 0.504 | 0.018 | 1.000 |
| 0.80 | under | 8/8 | 0.812 | 0.072 | 1.000 |
| 0.95 | under | 8/8 | 0.877 | 0.073 | 0.875 |
| 0.99 | under | 8/8 | 0.954 | 0.088 | 0.500 |
| 1.00 | critical | 7/8 | 1.046 | 0.111 | 0.429 |
| 1.01 | over | 8/8 | 0.962 | 0.192 | 0.500 |
| 1.05 | over | 8/8 | 1.027 | 0.249 | 0.500 |
| 1.20 | over | 4/8 | 1.215 | 0.083 | 0.250 |
| 1.50 | over | 6/8 | 1.068 | 0.432 | 0.333 |
| 2.00 | over | 4/8 | 1.106 | 0.894 | 0.250 |

All successful fits were stable.

### Interpretation

The current engine can recover the constructed scalar coordinate with useful fidelity through a substantial underdamped range **without Atlas calibration**. Resolution degrades as the system approaches the repeated-root boundary and becomes substantially less reliable on the overdamped branch under this fixed sampling, excitation, observation map and order-2 estimator.

This is consistent with an identifiability mechanism rather than failure of the pair-invariant formula itself. For chi > 1,

`lambda_fast,slow = -omega_n (chi +/- sqrt(chi^2-1))`.

The magnitude ratio between the fast and slow roots is

`(|lambda_fast|/|lambda_slow|) = (chi + sqrt(chi^2-1))^2`,

which grows with chi. The fast real branch can therefore become increasingly difficult to resolve from finite-rate lag-covariance data while the slow branch dominates longer-lag structure. This mechanism is a P0-D interpretation to test, not yet a qualified neural rule.

## Normalized-discriminant interpretation

For a tracked real 2D invariant block `B`,

`p(s)=s^2-tr(B)s+det(B)`.

If the block is licensed as one second-order lineage,

`gamma=-tr(B)` and `omega_n=sqrt(det(B))`, giving

`chi = -tr(B)/(2 sqrt(det(B)))`.

Therefore

`chi^2 - 1 = (tr(B)^2 - 4 det(B)) / (4 det(B))`.

So chi is a normalized discriminant coordinate on a licensed two-dimensional lineage:

- negative discriminant -> chi < 1 -> complex-conjugate branch;
- zero discriminant -> chi = 1 -> repeated-root boundary;
- positive discriminant -> chi > 1 -> real-pole branch.

This makes the critical boundary algebraically continuous even though the observable representation changes from oscillatory to non-oscillatory.

## Surface B: forced two-component conglomeration

The fixed latent-order-4 reconstruction was not generally reliable.

Representative results:

| case | true component chi | true chi_C | successful | median chi_C estimate | median abs chi_C error |
|---|---|---:|---:|---:|---:|
| both under | 0.35, 0.55 | 0.538 | 7/8 | 1.245 | 0.707 |
| common subcritical | 0.75, 0.75 | 0.750 | 1/8 | 0.817 | 0.067 |
| mixed cross-boundary | 0.65, 1.25 | 1.215 | 5/8 | 0.946 | 0.269 |
| both over | 1.25, 1.50 | 1.483 | 2/8 | 1.016 | 0.466 |
| wide heterogeneity | 0.25, 1.75 | 1.684 | 7/8 | 0.546 | 1.138 |
| near-boundary mixed | 0.95, 1.05 | 1.043 | 4/8 | 1.143 | 0.100 |

The second, higher-natural-frequency component was usually the weaker reconstruction and truth-assignment distances were large.

### Interpretation of the multi-component failure

P0-D11 **does not support** using the equal-component forced-order conglomerate as an operational NSD system chi.

The failure is informative for the architecture:

1. A latent component is not automatically a supported observable component.
2. Forcing all latent components into the fit can corrupt the conglomerate coordinate even when one component is reconstructed well.
3. System-level chi therefore needs a resolution/participation architecture before aggregation.
4. Model adequacy, rank support, crowding and uncertainty should gate which components may enter a coordinate rather than being numerically mixed into the chi value itself.
5. Equal component weights are not justified by these results.

A specific hypothesis for follow-up is that the fixed isotropic process-noise scale and frequency-separated components create strongly unequal stationary participation, so the higher-frequency component can be weak in the output covariance even when it exists in the latent generator. That hypothesis requires a controlled excitation/participation diagnosis before any weighting rule is proposed.

## Surface C: scalar information loss

The analytic construction confirmed that different modal architectures can share the same chi_C. For equal natural frequency, `[0.8,0.8]` and `[0.4,sqrt(1.12)]` both have `chi_C=0.8` under equal weighting.

This is not a defect if the scalar is treated correctly. It demonstrates why the full NSD picture must retain:

**modal structure + scalar coordinate + conglomerate/system organization.**

The scalar locates the system; it does not uniquely specify the route by which the system occupies that location.

## Strongest P0-D conclusion

P0-D11 supports a revised research hypothesis:

> **A pre-Atlas chi coordinate is mathematically reconstructable from supported second-order dynamical lineages, but system-level chi should be formed only from the observable/participating structure that the Engine can actually support. The Atlas should then map where those independently derived coordinates correspond to function, perturbation, transition and natural limits.**

This is a hypothesis architecture, not yet a frozen system-level chi definition.

## Next non-science-breaking tests

1. Track one two-dimensional lineage continuously through chi < 1 -> chi = 1 -> chi > 1 and test whether lineage preserves the pole pairing needed for branch-complete chi.
2. Diagnose the multi-component failure under equal-frequency and excitation-balanced constructions before introducing any participation weight.
3. Compare forced latent order against supported observable-rank representations without using Atlas or phenotype information.
4. Only after those tests propose candidate participation weights, with underlying component structure always retained.

## Nonclaims

- No neural empirical chi range is inferred.
- No healthy/optimal/pathological zone is defined.
- No Atlas calibration was used.
- No operational real-pole pairing rule is frozen.
- No component weighting rule is frozen.
- No `chi_system` admission is granted.
- No P0-Q or P1 rule is changed.
