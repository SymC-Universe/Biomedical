# GRI SCC25 G2 scalar-admission eigenstructure diagnostic

**Date:** 2026-09-21  
**Status:** P0-D POST-RESULT DIAGNOSTIC / NO SCALAR CHI ADMISSION  
**Historical G2 result:** immutable  
**Purpose:** determine whether the already-fitted weekly D1 operator contains eigenstructure that could even be eligible for a later scalar-chi derivation under GOM v0.8.2 REVIEW Section 2.2.

## Why this diagnostic is necessary

The historical G2 program reports `rho(T)`, the spectral radius of a discrete-time one-week transition operator. Under the current GOM, a stability diagnostic is not automatically scalar `chi`.

A licensed scalar `chi` requires a defensible second-order factor or a separately derived native equivalent. A single pole does not define `chi`, and pairing modes is itself a modeling claim.

Therefore:

`rho(T) != chi` by naming or convenience.

The first task is to expose the operator eigenstructure that the historical diagnostic compressed away.

## Scope

Reconstruct the exact frozen chronic R1/A3 D1 operators using:

- the exact hash-bound GSE98812 source;
- the historical `log2(source_value + 1)` transform;
- the exact PBS-only feature gate;
- the exact PBS-only basis;
- coequal ranks `r=2` and `r=3`;
- the same 20 one-week transitions;
- the same D1 model.

Inspect:

1. point-fit eigenvalues;
2. every historical leave-one-transition-out D1 refit;
3. the historical paired-earliest-transition block refit;
4. all eleven leave-one-PBS-state basis refits.

No D2 scalar is considered because D2 failed its frozen predictive-support gate.

## Diagnostic objects

For every admissible D1 operator, record:

- full discrete-time eigenvalues;
- modulus and wrapped phase;
- number of real eigenvalues;
- number of complex-conjugate pairs;
- whether a nonreal pair is present.

Where a complex pair exists, record a **branch-sensitivity demonstration** for the mathematical mapping

[
lambda_k = log |mu|/Delta t + i(arg mu + 2pi k)/Delta t
]

for `k=-1,0,1` and `Delta t=1 week`.

The resulting ratio

[
-Re(lambda_k)/|lambda_k|
]

is recorded only as `derived_ratio_not_licensed_chi`. It is **not** promoted to biological or physical `chi`, because continuous-generator validity, alias/branch selection, and second-order-factor licensing have not been earned.

## Before-result diagnostic categories

The diagnostic may return:

- `PAIR_STRUCTURE_PERSISTENT_DERIVATION_REQUIRED`
- `PAIR_STRUCTURE_REPRESENTATION_DEPENDENT`
- `DISCRETE_EIGENSTRUCTURE_ONLY_NO_PAIR`
- `INDETERMINATE_REQUIRED_REFIT_FAILURE`

None is scalar admission.

The strongest possible result from this pass is:

`ELIGIBLE_FOR_PROSPECTIVE_SCALAR_DERIVATION_REVIEW`

not `CHI_ESTABLISHED`.

## Scientific firewall

This diagnostic cannot:

- change the frozen G2 predictive result;
- reinterpret the G2 unit circle as biological `chi=1`;
- choose a logarithm branch post hoc;
- assume a continuous-time semigroup from weekly samples;
- promote `rho(T)` to `chi`;
- select r=2 or r=3 because one is more convenient;
- use proliferation, methylation, or other reserved channels to rescue scalar admission.

If the pair structure is unstable or the continuous-generator assumptions remain unresolved, the joint `chi <-> Chi` program proceeds through the local/modal branch without manufacturing a scalar.
