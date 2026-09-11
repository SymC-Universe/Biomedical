# P0-D13 Chi Lineage Through the Repeated-Root Boundary Plan

Date: 2026-09-11
Status: **P0-D LINEAGE / BOUNDARY MAPPING. NOT ATLAS CALIBRATION. NOT P0-Q. NOT P1.**
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum

## Question

Can a data-only continuity rule preserve the identity of one supported two-dimensional second-order lineage as it moves from `chi<1` through the repeated-root boundary `chi=1` and into `chi>1`, allowing the pair-invariant chi coordinate to remain branch-complete without arbitrary static pairing of real poles?

## Why lineage is required

For a licensed real 2D block `B`,

`chi = -tr(B) / (2 sqrt(det(B)))`

and

`chi^2 - 1 = (tr(B)^2 - 4 det(B)) / (4 det(B))`.

Thus chi is a normalized discriminant coordinate on a second-order lineage. The mathematical coordinate remains defined when the eigenvalue representation changes from a complex conjugate pair to two real poles.

The practical problem is **identity**. Once a complex pair splits into two real poles in a multi-component system, static pairing of arbitrary real poles is not licensed. A lineage established before the boundary may provide that pairing if continuity can preserve the 2D object through the transition.

## Synthetic system

Two independent 2D second-order components are present in every record.

### Tracked target lineage

- `omega_n = 2*pi*2 Hz`;
- chi path:
  `[0.50, 0.70, 0.85, 0.93, 0.97, 0.99, 1.00, 1.01, 1.03, 1.07, 1.15, 1.30, 1.50]`.

### Companion lineage

- `omega_n = 2*pi*7 Hz`;
- fixed `chi = 0.55`.

The companion remains underdamped and frequency separated. P0-D12 showed that a high-frequency component around this damping level becomes recoverable when participation is balanced.

## Visibility conditions

### V1: fixed reference balance

Compute output-trace-balanced process scales at target `chi=0.70` and then keep those scales fixed across the entire chi path. This allows the target's natural stationary participation to change as its dynamics change.

### V2: pointwise output balance

At each chi point, independently compute process scales that give the two components equal stationary output covariance trace. This is a controlled observability condition used only to separate branch sensitivity from fading participation.

V2 is not a real-data weighting rule.

## Data-only lineage algorithm

No truth is available to the lineage tracker.

At the first point, where both components are underdamped:

1. enumerate the three possible partitions of four fitted poles into two pairs;
2. choose the partition minimizing conjugacy mismatch;
3. label the lower- and higher-natural-scale pair from their pair invariants.

At each subsequent point:

1. enumerate all three pair partitions and both assignments to the two previous lineages;
2. compute a relative complex-plane set distance from each candidate pair to its previous pair;
3. choose the assignment with minimum total continuity cost;
4. retain the chosen pair identities without using truth chi, truth frequency labels, Atlas values, phenotype or outcome.

The chosen low-frequency lineage is then evaluated with the pair-invariant chi formula. Truth is used only after tracking for P0-D scoring.

## Static ambiguity diagnostic

At every point, independently count how many of the three static four-pole partitions yield two algebraically valid stable second-order factors. If multiple static pairings are valid above the boundary, this demonstrates why continuity/lineage information is scientifically relevant rather than cosmetic.

## Replicates and estimator

- 8 independent lineage paths per visibility condition;
- each point is an independently simulated stationary record, so continuity is not aided by reusing the same noise realization;
- current SSI-COV;
- fixed development order 4;
- same 3% channel-SD white measurement-noise stress used in P0-D11/P0-D12;
- truth matching occurs only for retrospective scoring of tracked identity.

## Primary diagnostics

No pass threshold is defined. Record:

- successful lineage continuation fraction at each chi;
- target chi estimate and absolute error;
- retrospective target-identity correctness;
- branch representation of the tracked pair;
- continuity cost;
- number of algebraically valid static pairings;
- target/companion observable participation fractions;
- singular support `s4/s1`;
- stability of the fitted four-pole model.

## Interpretation

Evidence for the lineage hypothesis would be a coherent target identity and chi path across or beyond the repeated-root transition, particularly when multiple static real-pole pairings are algebraically possible.

Failure is equally informative. It may show that:

- the current estimator loses the 2D lineage before/at the EP;
- the low-frequency target becomes unobservable on the real branch;
- continuity based only on pole geometry is insufficient and the observable carrier subspace must enter lineage tracking;
- a branch-complete neural chi requires stronger state-space/subspace objects rather than static poles.

## Nonclaims

- No neural empirical chi is estimated.
- No Atlas value is used.
- No biological visibility balancing is proposed.
- No continuity-cost threshold is selected.
- No real-data pole-pairing rule is frozen.
- No `chi_system` admission is granted.
- No P0-Q or P1 rule is changed.
