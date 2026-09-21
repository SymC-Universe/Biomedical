# GRI SCC25 G2 scalar-admission eigenstructure post-result audit

**Date:** 2026-09-21  
**Status:** COMPLETE P0-D POST-RESULT DIAGNOSTIC  
**Historical chronic G2 result:** unchanged  
**Workflow run:** `35668341037`  
**Head SHA:** `6fe7571c1c42f1c148d88c1ea1557eb2c565158a`  
**Artifact:** `GRI_SCC25_G2_SCALAR_ADMISSION_EIGENSTRUCTURE_V01`  
**Artifact ID:** `10670490883`  
**Artifact digest:** `sha256:c78c9309c57f95363d9783b7c6a92b07071b2b4a484d7975c6f1197e89c1dfa0`

## Result

The historical weekly G2 spectral radius `rho(T)` does **not** earn scalar-`chi` status.

### Rank r=2

All 33 required operator fits were admissible, but **0/33** contained a complex-conjugate eigenvalue pair.

The point-fit eigenvalues were:

```text
mu_1 = -0.1140823492
mu_2 =  0.8552726371
```

The negative discrete eigenvalue carries wrapped phase `pi`; it cannot simply be treated as a real continuous-time relaxation pole. The rank-2 object therefore does not supply the complex second-order factor that would license the canonical oscillatory `chi` construction, and no alternate native scalar derivation has been established here.

Disposition:

`DISCRETE_EIGENSTRUCTURE_ONLY_NO_PAIR`

### Rank r=3

The point fit contains one complex-conjugate pair plus one real mode:

```text
mu_pair = -0.2131820884 +/- 0.4029754626 i
|mu_pair| = 0.4558901472
wrapped phase = +/- 2.0573895268 rad

mu_real = 0.8658280631
```

However, the pair is present in **32/33** required operator fits, not all 33.

The failure is not a numerical-refit failure. In `BASIS_LOO_2`, the admissible r=3 operator has three real discrete eigenvalues:

```text
-0.3124315410
-0.0690446149
 0.7642733934
```

Therefore the presence of the apparent oscillatory pair is itself basis-sensitive under an already established sensitivity family.

Disposition:

`PAIR_STRUCTURE_REPRESENTATION_DEPENDENT`

### Branch ambiguity

Even in the r=3 point fit, mapping the discrete pair to a continuous-time pole is not unique without an independently licensed branch/generator assumption.

For the same positive-imaginary discrete eigenvalue, the diagnostic branch demonstration gives:

```text
k = -1: derived ratio = 0.1827524907
k =  0: derived ratio = 0.3566836031
k = +1: derived ratio = 0.0937636639
```

These values are explicitly `derived_ratio_not_licensed_chi`. No branch was selected.

## Cross-rank adjudication

`REPRESENTATION_DEPENDENT_SCALAR_ELIGIBILITY`

This is stronger than merely saying "chi has not been calculated." In the **current frozen R1/A3 weekly representation**, scalar admission fails the transfer requirement:

- r=2 offers no complex pair;
- r=3 offers a pair that is not fully robust to the existing basis sensitivity;
- continuous-time generator and logarithm-branch assumptions remain unlicensed.

Therefore the current SCC25 joint-meaning program must not use `rho(T)` or the r=3 principal-log ratio as biological `chi`.

## Consequence for the joint investigation

The active local object for the current SCC25 joint test is now the **native modal/discrete-time dynamical structure**, denoted generically `z_local`, not scalar `chi`.

The primary relationship becomes:

[
P(z_{local,t+1} | z_{local,<=t}, X_t, u_t)
]

versus

[
P(z_{local,t+1} | z_{local,<=t}, u_t),
]

with the reciprocal direction for broader capital-`Chi` organization.

This is not a retreat from the joint-meaning requirement. It is its refusal branch: the project tests what the local/modal representation and broader architecture say to one another **without manufacturing a scalar that the current representation has not earned**.

A future scalar route is not forbidden. It would be a new, separately justified representation/derivation lineage and could not retroactively overwrite this refusal.
