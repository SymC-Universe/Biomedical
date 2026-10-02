# NSD State-Space Lineage and Sampling Qualification Suite v0.1

Status: prospective qualification infrastructure only

GOM baseline: SymC General Operations Manual v0.8.6

Branch: `nsd-rebuild-gom-v0.8.0`

## Scope

This suite records and tests analytic lineage/sampling contracts discovered during NSD Bio Chi predecision work. It does not alter A0/A1/A2, does not license real-EEG local chi, and does not select among continuous-time embeddable (C), discrete exact-image (D), or scalar-positive (S) model families.

## Core coordinates

For the positive-lag recurrence

[
\gamma_{k+2}=a\gamma_{k+1}-b\gamma_k,
]

define

[
\rho=\sqrt{b},\qquad \xi=\frac{a}{2\rho},
]

and the regular covariance representation

[
\gamma_k=\rho^k\left[A T_k(\xi)+H U_{k-1}(\xi)\right].
]

The exact discrete white-Q image D obeys

[
0\le A\le1,\qquad |H|\le A\sinh L,\qquad L=-\ln\rho.
]

The continuous-time embeddable image C uses the sampling-invariant coordinate

[
g=\frac{G}{A\alpha},
]

with C defined by `|g|<=1` on a prospectively licensed alias-safe branch.

## Contracts currently implemented

1. Exact m-fold decimation preserves the covariance sequence under

[
A_m=A,\quad \rho_m=\rho^m,\quad \xi_m=T_m(\xi),\quad H_m=H U_{m-1}(\xi).
]

2. The continuous-time nuisance coordinate g is invariant under alias-safe exact decimation.

3. The normalized discrete exact-image coordinate

[
h=\frac{H}{A\sinh L}
]

contracts under nontrivial canonical coarsening.

4. The positive-lag Hankel determinant

[
\Delta_H=\rho^4\left[A^2(\xi^2-1)-H^2\right]
]

obeys

[
\Delta_{H,m}=\rho^{4(m-1)}U_{m-1}(\xi)^2\Delta_H.
]

5. Exact underdamped decimation may create rank collapse only when `U_{m-1}(xi)=0`, equivalent to `sin(m theta)=0`; critical and stable positive-real overdamped cases do not acquire rank loss by exact decimation alone.

6. A constructive scalar-positive fine-rate law can lie outside D and C yet enter D after coarse decimation while remaining outside C. This demonstrates that coarse D compatibility cannot be back-projected as evidence of fine-rate D semantics.

7. Existing isotropic A1 truth with H=G=0 lies inside C, D, and S and therefore cannot adjudicate family scope.

## Explicit non-claims

- No real EEG local chi is licensed.
- No new estimator family is authorized.
- No model-selection threshold, conditioning cutoff, or truth grid is frozen.
- No continuous-frequency branch may be changed post hoc to rescue an embedding.
- Raw H and raw Hankel magnitude are not sampling-rate-invariant biological quantities.
- Coarse-rate D membership does not prove fine-rate D membership.

## Current implementation

Test module:

`NSD_vNext/engine/tests/test_state_space_lineage_sampling.py`

Dedicated CI:

`.github/workflows/nsd-state-space-lineage-sampling-contracts.yml`

The suite is deliberately separate from the frozen A0/A1/A2 likelihood implementation.

## Decision bearings

The next scientific decision is family scope for N-B1:

- C: continuous-time modal lineage shared across sampling rates.
- D: sample-rate-specific exact white-Q state-space semantics.
- S: broad observable scalar-equivalence semantics.
- refusal-only: retain current estimator families and refuse unresolved cases.

Current cross-project evidence from Substrate Inheritance, chemistry, and GRI motivates testing C as the strongest candidate for biological local chi because it preserves dynamical lineage through representation changes. This motivation is not itself a family-selection result.

## Next prospective experiments if C is authorized

1. Paired exact-decimation metamorphic test using one fine-rate known-truth realization and deterministic coarse sampling.
2. Continuous-embeddable interior truths with both signs of g and multiple distances from |g|=1.
3. D\\C truths to verify refusal of continuous lineage despite valid discrete exact-state-space representation.
4. S\\D truths to verify refusal of latent white-Q semantics.
5. Alias/order-collapse controls placed prospectively at and away from `sin(m theta)=0`.
6. Near-critical conditioning cells with uncertainty propagated from `(rho,xi)` into chi.
7. A2 mode-collision controls separated from genuine multimodal truths.
8. Colored-process controls retained as out-of-family refusals.

No numerical grid or threshold is frozen by this document.
