# GRI Chi_bio G2 candidate derivation: discrete transition-operator spectral radius

**Date:** 2026-09-12  
**Status:** P0-D CANDIDATE DERIVATION, NOT FROZEN  
**Chi_bio status:** `NOT_ADMITTED`  
**Cancer-specific candidate values inspected:** NO  
**Unity placement inspected:** NO

## 1. Native model class

For an ordered biological state sampled at fixed interval `Delta t`, a local linear input/state model can be written

```text
x_(k+1) = T x_k + B u_k + eta_k
```

where:

- `x_k` is the state representation;
- `T` is the autonomous transition operator over one sampling interval;
- `u_k` is measured exogenous input/forcing;
- `B` maps that input into the state;
- `eta_k` represents innovations/noise/model mismatch.

For the autonomous system `x_(k+1) = T x_k`, local asymptotic stability requires all eigenvalues to lie inside the unit disk:

```text
rho(T) = max_k |lambda_k(T)| < 1.
```

The natural boundary is therefore

```text
rho(T) = 1.
```

No post-result centering or scaling is required to create unity.

## 2. Candidate system coordinate

A direct scalar candidate is

```text
G2 = rho(T).
```

Within a correctly specified local sampled-dynamics model:

```text
G2 < 1   perturbations decay asymptotically in the autonomous linear model
G2 = 1   marginal unit-circle boundary
G2 > 1   at least one autonomous linear mode grows
```

This is a mathematical/model-class interpretation only. It is not yet a GRI biological regime label.

## 3. Scalar/modal/conglomerate relationship

### Scalar

`rho(T)` is dimensionless and has a natural unity boundary.

### Modal/vector

The full eigenvalue/eigenvector structure of `T` remains available. A scalar value is explicitly a compression of the transition spectrum.

### Conglomerate/system

`T` represents coupled state evolution. If exogenous inputs and environmental variables are included explicitly, the model can distinguish autonomous organization from realized behavior under forcing.

This aligns well with v0.7.4's local-versus-embedded stability requirement, provided that `u_k` and any omitted environment are handled honestly.

## 4. Sampling-interval dependence

A major difference from the G1 normalized-interaction candidate is that `T` depends on sampling interval.

If a continuous generator `J` is locally valid and forcing is absent, then ideally

```text
T(Delta t) = exp(J Delta t).
```

and

```text
lambda_T = exp(lambda_J Delta t).
```

The stable/unstable boundary remains the unit circle, but numerical distance from 1 depends on `Delta t`.

Therefore a G2 value cannot be compared across datasets with different sampling intervals unless the interval dependence is explicitly modeled, transformed to a common continuous generator, or the comparison is otherwise justified.

## 5. Critical issue: forced dynamics

The SCC25 cetuximab series is continuously treated. A model

```text
x_(k+1) = T x_k
```

would conflate autonomous dynamics with drug forcing.

At minimum, a treatment-aware model requires an explicit input term or separate treated/control operator interpretation. The time-matched PBS trajectory is scientifically valuable precisely because it provides a control path, but it does not by itself solve operator identifiability.

No transition operator may be called an intrinsic stability operator if persistent forcing is silently absorbed into it.

## 6. Identifiability and dimensionality

### Full high-dimensional operator

With roughly 11 ordered states per arm in the SCC25 series, an unconstrained high-dimensional `T` is unidentifiable.

### Reduced-state operator

A reduced representation may make estimation possible, but the reduction is science-changing because it determines what state the operator governs. Any reduction must therefore be selected/frozen before candidate G2 outcomes are inspected.

Potential classes to review, not select yet:

- frozen Hallmark/module state vectors;
- independently defined leading latent factors;
- joint methylation/RNA state coordinates;
- predeclared domain-native regulator panels;
- other reduced states justified independently of unity placement.

A reduction learned specifically to maximize separation at G2=1 is prohibited.

## 7. Non-normality and transient response

`rho(T) < 1` guarantees asymptotic decay in the linear autonomous model but does not imply monotonic decay. A non-normal operator can exhibit large transient amplification before eventually decaying.

Because the broader GRI program cares about resilience, reorganization, and transient response, G2 cannot be treated as a complete system description even if admitted.

Companion quantities may be required, such as:

- singular-value amplification over finite horizons;
- pseudospectral/condition information;
- left/right mode non-orthogonality;
- observed transient gain under perturbation.

These remain modal/conglomerate descriptors, not terms to be averaged into G2 after the fact.

## 8. Relationship to dynamic-network-biomarker theory

Discrete critical-transition theory often writes local stochastic dynamics with a dominant eigenvalue whose modulus approaches 1 at the tipping point. This supports the mathematical relevance of a unit-circle boundary and of covariance/fluctuation early-warning signatures.

However, DNB signatures are not direct estimates of `T` unless the model and noise assumptions make that inverse problem identifiable.

## 9. Candidate falsifiers before freeze

G2 should be rejected or narrowed if:

- no state representation can be chosen independently of candidate outcome;
- exogenous treatment/embedded context cannot be separated sufficiently for the target claim;
- operator estimation is rank-deficient or dominated by regularization choices;
- inferred `rho(T)` is unstable to reasonable sampling/model choices;
- held-out dynamic systems do not recover known operator stability;
- non-normal transient behavior carries the biological regime change while `rho(T)` does not;
- a simpler established early-warning statistic performs equally well under the same information budget;
- representation transport to patient tumors is unsupported.

## 10. Current decision status

```text
CB2 native generator/derivation: CANDIDATE-SPECIFICALLY STRONG
CB3 natural normalization: CANDIDATE-SPECIFICALLY STRONG
CB5 modal/conglomerate traceability: STRONG IN MODEL CLASS
CB7 identifiability: OPEN / HIGH-RISK WITH CURRENT 11-WEEK SINGLE-LINEAGE SOURCE
CB8 uncertainty: OPEN
CB9 known-truth recovery: NOT YET IMPLEMENTED
CB10 internal P0-Q: NOT STARTED
CB14 unity basis: MATHEMATICALLY NATURAL IN MODEL CLASS, NOT BIOLOGICALLY ADMITTED FOR GRI
```

**G2 is not frozen.** The next science-changing choices are the GRI state representation, treatment/input model, and dimensional reduction used to estimate `T`.