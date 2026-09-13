# P0-D20 Recovery Transformation Geometry Plan

Date: 2026-09-13
Status: **P0-D exploratory. Synthetic mechanism/function/limit mapping. Not P0-Q or P1.**
Purpose: `FUNCTION_MAPPING`

## Question
With local subsystem dynamics and directed edge norms held fixed, does the *transformation geometry* of reciprocal feedback change asymptotic recovery and finite-time transient amplification?

P0-D17 established that matched-norm feedback transformations can reorganize global lineages differently. P0-D19 established that reciprocal feedback can alter recovery non-monotonically even when local subsystem dynamics are fixed. P0-D20 asks whether those two observations join: does what the receiving subsystem does to the signal materially change recovery, even when the scalar coupling magnitude is matched?

## Frozen-for-this-run synthetic construction
- subsystem 0: chi `0.55`, frequency `3 Hz`;
- subsystem 1: chi `0.85`, frequency `5 Hz`;
- same dimensionless second-order realization used by P0-D17/P0-D19;
- reciprocal edge templates each have spectral norm 1 before multiplication by `g`;
- feedback variants: position->position, position->velocity, velocity->position, velocity->velocity, mixed->mixed;
- coupling rates: `0, 4, 8, 12, 14, 18, 22`;
- transient metric: induced Euclidean 2-norm of `exp(A t)` over `t in [0,5] s`, 2001 points, licensed only for this dimensionless synthetic state representation.

## Outputs
For each transformation and coupling rate:
- spectral abscissa;
- asymptotic stability;
- dominant local asymptotic scale `tau=-1/alpha` when `alpha<0`;
- worst-case finite-time induced gain and peak time;
- directed edge norms;
- global poles.

## Function/Limit interpretation
Function Map: identify how different matched-strength feedback transformations organize recovery while the full system remains stable.

Limit Map: preserve any approach to instability, instability, large transient amplification, or transformation-dependent divergence. No threshold is chosen in advance.

## Falsification-bearing exploratory possibilities
- If matched-norm feedback transformations produce indistinguishable recovery surfaces, the stronger claim that transformation geometry adds recovery information is weakened for this construction.
- If they differ, the result supports only the synthetic architectural proposition that feedback geometry can matter beyond coupling magnitude; it does not establish a neural mechanism.

## Firewalls / nonclaims
- no Atlas labels or outcomes;
- no empirical neural inference;
- no biological coupling magnitude;
- no `chi_system` construction;
- no recovery threshold;
- no equation of `chi=1` with recovery failure;
- no use of the prospective `chi~1.2-1.3` note as a target, bin, stopping criterion, or interpretation rule;
- no P1 promotion.

## Why now
This is the cheapest direct bridge between P0-D17 and P0-D19 and tests a central v0.7.4 relational-stability proposition before adding empirical complexity.