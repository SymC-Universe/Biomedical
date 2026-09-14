# GRI Chi_bio G2 operator-model attack

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome derivational attack  
**Approved rank architecture:** A3, co-equal `r=2` and `r=3` robustness  
**Chi_bio:** `NOT_ADMITTED`  
**Real candidate trajectories inspected:** NO

## 1. Hidden issue exposed before empirical execution

The earlier operational G2 template used

```text
x_(k+1) = T x_k + B u_k + c
```

with one binary treatment input `u`.

This is a valid controlled linear model, but it has an important limitation for the present scientific question:

```text
T is shared between PBS and cetuximab.
```

Therefore the treatment input can shift the forcing/equilibrium through `B u`, but it cannot by itself establish that cetuximab reorganizes the transition operator or changes `rho(T)`.

If the target question is only whether one common low-order operator plus exogenous forcing can describe both arms, the shared-T model is appropriate.

If the target question is whether treatment changes the stability architecture itself, the shared-T additive-input model is insufficient by construction.

## 2. Minimal treatment-dependent operator model

A treatment-interaction model can represent operator reorganization directly:

```text
x_(k+1) = T0 x_k + u_k DeltaT x_k + B u_k + c + noise
```

For binary `u`:

```text
PBS:  T_PBS = T0
CTX:  T_CTX = T0 + DeltaT
```

This gives two explicit operator objects whose spectral properties can be compared without fitting a separate coordinate system for each arm.

The model is implemented only as outcome-blind mechanics in:

`src/chi_bio_g2_empirical_preflight.py::fit_treatment_interaction_transition`

No real SCC25 molecular matrix is read by that implementation or its regression tests.

## 3. Short-term algebraic feasibility under A3

If the shared pretreatment day-0 state is prospectively licensed for the cetuximab arm, SCC25 contributes:

```text
5 PBS transitions + 5 CTX transitions = 10 total transitions.
```

The treatment-interaction design with an additive treatment term and intercept has

```text
2d + 2 predictor columns.
```

Therefore:

```text
r=2 -> 6 columns against 10 transitions
r=3 -> 8 columns against 10 transitions
```

Both A3 ranks are algebraically possible before considering conditioning, serial dependence, model adequacy or uncertainty.

These are only formal design counts. They do not guarantee reliable estimation.

## 4. Why the interaction form is preferable to two independently fitted bases

The approved R1 representation fits the transcriptomic basis from PBS controls only and projects treated states without refitting.

Within that same frozen coordinate system, the interaction form estimates

```text
T_PBS
T_CTX = T_PBS + DeltaT
```

so a difference in operator behavior cannot be attributed to rotating the representation separately for the treated arm.

That is cleaner than fitting a treated-specific PCA basis and then comparing spectral radii in incomparable coordinate systems.

## 5. Remaining competition

Three operator models remain scientifically distinct:

### M1: shared T plus additive treatment input

Tests whether one common operator plus treatment forcing is adequate.

It is a useful null/restricted model but cannot directly test operator reorganization.

### M2: treatment-interaction operator

```text
T_CTX = T_PBS + DeltaT
```

Directly tests treatment-associated operator reorganization in one frozen state basis.

### M3: separate-arm operators

Fits independent `T_PBS` and `T_CTX` in the same frozen basis.

This is flexible but sacrifices parameter sharing and is more vulnerable to tiny-sample instability.

## 6. Current recommendation for later freeze

Use:

```text
primary model candidate: M2 treatment-interaction operator
restricted/null comparator: M1 shared T + additive input
stress sensitivity: M3 separate-arm T only if identifiability/conditioning remain adequate
```

This recommendation is based on what each model can identify, not on any observed SCC25 candidate value.

## 7. What is not yet frozen

The user approved A3/B3/C3, not the exact G2 operator model. Therefore this document does not silently select M2.

The full empirical G2 freeze still must explicitly state:

- operator model;
- day-0 initialization convention;
- count normalization/transformation;
- feature universe;
- conditioning refusal;
- model-adequacy refusal;
- uncertainty procedure;
- cross-timescale transport rule;
- A3 material-conclusion agreement schema.

Until those are frozen, the empirical preflight template remains non-executing.

## 8. Claim ceiling

The treatment-interaction form is mathematically and mechanically qualified on known-truth synthetic fixtures. No claim is made that SCC25 is linear, that treatment changes its spectral radius, that `rho=1` is a biological resistance boundary, or that a GRI `Chi_bio` has been admitted.
