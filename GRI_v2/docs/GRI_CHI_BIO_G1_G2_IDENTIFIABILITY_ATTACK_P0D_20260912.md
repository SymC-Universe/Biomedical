# GRI Chi_bio G1 versus G2 identifiability attack

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D derivational / identifiability attack  
**Approved primary family:** G1/S1/L3  
**Temporal comparator:** G2  
**Chi_bio promotion state:** `NOT_ADMITTED`  
**Cancer-specific Chi_bio values inspected:** NO

## 1. Why this attack was required

The first G1 hardening run established that a natural unity boundary survives only under explicit restoration/operator conditions. The next question is therefore not merely whether G1 can be computed, but whether the quantities needed to define its numerical coordinate are identifiable from the available temporal architecture.

The key distinction is:

```text
identifying the effective local Jacobian J
is not the same as
identifying the decomposition J = K - R.
```

That distinction matters because the G1 normalized coordinate depends on the restoration structure, while a transition operator can in principle be estimated directly from ordered state transitions after a prospectively frozen dimensional reduction.

## 2. G1 decomposition non-identifiability

Consider the approved local transcriptomic candidate form

```text
dx/dt = P(x) - R x
K = dP/dx
J = K - R.
```

Suppose an ideal temporal experiment identified `J` exactly.

For any admissible perturbation `Delta` to the restoration operator,

```text
R' = R + Delta
K' = K + Delta
```

produces

```text
K' - R' = K - R = J.
```

Therefore the observed local dynamics do not, by themselves, uniquely decompose production/regulatory feedback from restoring/turnover structure.

This is not a numerical weakness. It is an algebraic non-identifiability.

### Consequence for G1A

Under the common-restoration restriction

```text
R = beta I,
```

if `J` is known and `beta` is independently known,

```text
M = I + J/beta
G1A = alpha(M) = 1 + alpha(J)/beta.
```

The **side of unity** follows from the sign of `alpha(J)`, but the **numerical G1A value** depends on `beta`.

Frozen executable example:

```text
J = diag(-0.2, -0.5)

beta = 0.5 -> G1A = 0.6
beta = 1.0 -> G1A = 0.8
beta = 2.0 -> G1A = 0.9
```

All three systems have the same effective Jacobian and the same stable classification, but different G1A values.

Therefore a trajectory that identifies only `J` cannot identify the G1A scalar value unless the common restoration scale is independently measured or licensed.

### Consequence for G1B

The symmetric generalized coordinate

```text
lambda_max(R^-1/2 K R^-1/2)
```

also depends on the decomposition into `K` and `R`. Knowing only `J=K-R` does not identify a unique G1B value.

G1B therefore requires independently justified restoration information in addition to the effective local Jacobian.

## 3. Why this is biologically material for S1

The selected S1 state is transcriptomic. Mammalian mRNA decay/half-life is gene- and context-dependent rather than a demonstrated common scalar restoring rate across the transcriptome. A large mammalian half-life compendium assembled dozens of human and mouse transcriptome-wide decay datasets and treats half-life as a gene-level property affected by sequence and biochemical features.

This does not prove that a reduced module representation cannot have an effective common restoration rate. It does mean that such a rate is an empirical hypothesis requiring evidence, not a default inherited from the Guo-Amir source model.

Likewise, modern GRN literature distinguishes mechanistic regulatory interactions from statistical correlation and emphasizes the difficulty of inferring causal regulatory structure from observational omics alone.

Relevant sources:

- Guo Y, Amir A. Nature Communications 12, 130 (2021). DOI: 10.1038/s41467-020-20472-x.
- Agarwal V, Kelley DR. Genome Biology 23, 245 (2022). DOI: 10.1186/s13059-022-02811-x.
- Badia-i-Mompel P et al. Nature Reviews Genetics 24, 739-754 (2023). DOI: 10.1038/s41576-023-00618-5.
- Maizels RJ, Briscoe J. Nature Reviews Genetics 27, 485-498 (2026). DOI: 10.1038/s41576-026-00939-1.

## 4. G2 identifiability structure

For a discrete ordered state model

```text
x_(k+1) = T x_k + B u_k + c + noise,
```

G2 uses

```text
rho(T).
```

Unlike G1, the candidate scalar does not require a separate decomposition of `T` into production and restoration operators.

This does **not** make G2 automatically identifiable. It changes the problem to estimating a transition operator at the frozen state resolution.

### Sampling interval

If a time-invariant continuous system has

```text
T_Delta = exp(J Delta),
```

then

```text
rho(T_Delta) = exp(alpha(J) Delta).
```

The unity boundary is preserved for any positive `Delta`, but the numerical radius changes with the sampling interval.

A prospectively fixed reference interval can be used only when the time-invariant semigroup interpretation is justified:

```text
rho_ref = rho(T_Delta)^(Delta_ref / Delta).
```

This preserves the unity boundary and prevents different sampling intervals from being compared as though they were the same coordinate.

## 5. SCC25 rank ceiling

The source-qualified SCC25 cetuximab series has 11 ordered states per arm, hence 10 one-step transitions per arm.

Two simple estimation architectures illustrate the raw rank limitation:

### Shared transition operator plus treatment input

Using both arms gives 20 transitions. With one treatment input and an intercept, the predictor count is

```text
d + 2.
```

A best-case unregularized full-rank design therefore requires

```text
d + 2 <= 20
=> d <= 18.
```

At `d=18`, the model already contains

```text
18 * (18 + 1 + 1) = 360
```

free transition coefficients.

### Separate operator per arm

Each arm has only 10 transitions. With an intercept,

```text
d + 1 <= 10
=> d <= 9.
```

At `d=9`, each arm has 90 free transition coefficients.

These are only algebraic best-case ceilings. They do not account for serial dependence, pooled molecular states, collinearity, measurement noise, model checking, or held-out validation. Practical dimensionality must therefore be much more conservative and prospectively frozen.

The full transcriptome is categorically not identifiable as an unconstrained transition matrix from this series.

## 6. Current G1 versus G2 disposition

### G1 strengths retained

- strongest native theoretical connection to a unity boundary;
- explicit scalar/modal/conglomerate relation;
- meaningful biological separation between regulatory interaction and restoring structure;
- can remain a mechanistically richer target if independent turnover/restoration information exists.

### G1 new blocker

The numerical normalized coordinate is not identified by an effective temporal Jacobian alone. The restoration structure must be independently constrained.

### G2 strengths after identifiability attack

- transition operator is closer to what ordered temporal data directly constrain;
- no separate K/R decomposition is required;
- asymptotic unity boundary is exact for a frozen discrete operator;
- treated/control input can be represented explicitly rather than hidden.

### G2 remaining limits

- requires prospectively frozen low-dimensional state;
- numerical value depends on time interval unless converted under a licensed semigroup assumption;
- 11-state-per-arm SCC25 series is small and serially dependent;
- non-normal transients still require companion diagnostics;
- one cell line cannot establish pan-cancer transport.

## 7. CB7 implication

The current identifiability attack **does not yet pass CB7**. It does materially sharpen it.

Current result:

```text
G1A/G1B numerical coordinate:
    NOT IDENTIFIABLE FROM J ALONE
    needs independent restoration information

G2 reduced transition coordinate:
    POTENTIALLY IDENTIFIABLE FROM ORDERED DATA
    only after prospective state reduction and model-rank controls
```

This means G2 has become more than a generic comparator. It is now the leading empirical route against which G1 must justify its extra decomposition burden.

The approved G1-first plan is not silently reversed by this document. A change in primary candidate would be a new scientific decision unless G1 fails a precommitted criterion in the approved MFR/failure branch.

## 8. Precommitted next test

Before any real Chi_bio value is computed:

1. search for an independent restoration/turnover measurement route compatible with the intended S1 representation;
2. determine whether a reduced transcriptomic state can support G1A or G1B without outcome-driven construction;
3. freeze an outcome-blind reduced-state candidate for G2 feasibility testing;
4. evaluate G1 versus G2 on synthetic systems where both the effective dynamics and restoration decomposition are known;
5. prefer refusal or candidate narrowing over forced normalization.

## 9. Current stop status

**G1 family/state/scope approval:** preserved.  
**G1 exact general transcriptomic coordinate:** not derived.  
**G1 numerical identifiability from SCC25 trajectory alone:** fails algebraically without independent restoration information.  
**G2 status:** strengthened as the leading empirical comparator/fallback route.  
**Next scientific boundary:** empirical state reduction plus independent restoration-measurement strategy.  
**Chi_bio:** `NOT_ADMITTED`.
