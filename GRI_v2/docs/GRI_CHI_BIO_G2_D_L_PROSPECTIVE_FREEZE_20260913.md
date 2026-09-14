# GRI Chi_bio short-term G2 D-L prospective freeze

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.5  
**Empirical source:** GSE114446 SCC25 daily bulk RNA  
**State architecture:** approved A3 + B3 + C3 retained  
**Chi_bio:** `NOT_ADMITTED`

## 1. Purpose

This document closes the D-L design gate for the first outcome-bearing short-term G2/R1 pilot before real SCC25 candidate coordinates, transition radii, or unit-circle outcomes are opened.

Machine-readable freeze:

`config/gri_Chi_bio_shortterm_g2_r1_A3_empirical_freeze_20260913_v1.json`

The freeze does not admit biological Chi, normalized empirical G1, or a biological unity boundary. It licenses only a controlled temporal-operator pilot under the already approved A3 architecture.

## 2. Evidence used before freezing

The adjudication uses only source identity, known study design, mathematical identifiability, numerical-stability analysis and synthetic known-truth calibration.

The short-term source has six SCC25 PBS states at days 0-5 and five SCC25 CTX states at days 1-5. The measured PBS day-0 state is therefore available as one shared pretreatment origin.

The P0-D D2 calibration established that formal full rank is not enough. In the 10-transition treatment-interaction design, r=3 can be extremely ill-conditioned and spectral classification degrades quickly under synthetic perturbation.

The subsequent D1-versus-D2 leave-one-transition calibration materially changed the earlier model ordering. In the exact 5+5 short-term geometry, D1 generally predicted omitted transitions better than D2 once even small synthetic perturbations were introduced, including when D2 generated the truth. This effect was particularly strong at r=3.

A separate architecture-scaling calibration showed that this is not a universal rejection of D2. With 10 transitions per arm, D2 recovers useful predictive advantage in several true-reorganization scenarios. The correct conclusion is therefore geometry-specific: the short-term experiment should earn extra operator complexity rather than assume it, while the chronic source receives a separate later freeze.

## 3. D: operator model

### Frozen short-term primary: D1

```text
x_(k+1) = T x_k + B u_k + c
```

Role: feasibility model for whether a coherent low-order shared local operator plus treatment forcing is supported at all.

D1 cannot establish treatment-associated operator reorganization because T is shared by construction. Its output must not be worded as though CTX changed the operator.

### Gated secondary: D2

```text
x_(k+1) = T0 x_k + u_k DeltaT x_k + B u_k + c
```

D2 is not automatically interpreted. It must earn escalation at both r=2 and r=3 through all-refit identifiability/conditioning, lower aggregate LOTO NRMSE than D1, and lower per-transition error on at least six of ten omitted transitions.

If one A3 rank earns D2 and the other does not, the result is representation-dependent and does not transfer.

### D3

Separate-arm operators remain a stress sensitivity only. They are not a default rescue when D1 or D2 fails.

## 4. E: RNA transformation

Freeze a deterministic sample-wise transform:

```text
library_total_j = sum_g count(g,j)
CPM(g,j) = 1e6 * count(g,j) / library_total_j
x(g,j) = log2(CPM(g,j) + 1)
```

Requirements:

- finite, nonnegative counts;
- positive finite library totals;
- identical rule for PBS and CTX;
- no group-aware fitting;
- no response-informed normalization.

This is chosen for the first pilot because it introduces no parameters trained on treated outcomes and is reproducible from the frozen processed count table. It is not asserted to be uniquely optimal. Under v0.7.5, a later bounded foundational robustness challenge may use a frozen alternative such as an independently specified variance-stabilizing transform before heavy downstream inheritance.

## 5. F: feature universe

Use the source gene-row universe as delivered by the frozen GSE114446 processed source.

Refuse missing or duplicate gene identifiers rather than silently aggregate.

Detectability is determined from PBS controls only:

```text
retain gene iff CPM >= 1 in at least 3 of 6 SCC25 PBS states
```

CTX is forbidden from feature selection. The resulting feature set is frozen once and reused for both A3 ranks and every refit in this pilot.

No differential-expression screen, treatment-effect screen, proliferation screen, Atlas agreement, distance-to-unity criterion or later outcome is allowed to select genes.

## 6. G: shared day-0 initialization

The measured SCC25 PBS day-0 state is the common pretreatment state for both branches.

```text
PBS: d0->d1, d1->d2, d2->d3, d3->d4, d4->d5
CTX: d0->CTX d1, d1->d2, d2->d3, d3->d4, d4->d5
```

This produces ten transitions while preserving the fact that day 0 is one observation reused as an origin, not two independent baseline replicates.

## 7. H: conditioning refusal

Full rank is necessary but not sufficient.

For the full fit and every LOTO fit:

1. require full declared-design rank;
2. scale each nonzero design column to unit Euclidean norm solely for the condition-number diagnostic;
3. compute the SVD condition number;
4. refuse zero required predictors, nonfinite singular values, rank loss, or

```text
kappa_scaled > 67,108,864 = 1/sqrt(epsilon_float64)
```

This threshold is a numerical-resolution guard derived from float64 arithmetic, not an empirical tuning parameter. Model adequacy is evaluated separately.

## 8. I: model adequacy and D2 escalation

For each A3 rank, D1 is evaluated with leave-one-transition-out one-step prediction over all ten transitions.

Aggregate error is:

```text
NRMSE = sqrt( sum ||y-pred||^2 / sum ||y||^2 )
```

D1 must beat both frozen simple comparators:

1. persistence: `pred = x_now`;
2. arm-specific leave-one-out mean-next-state prediction from the remaining transitions in that arm.

D1 is adequate only when all LOTO fits remain admissible and its aggregate NRMSE is strictly lower than both comparators at both A3 ranks. The only tolerance permitted in the comparison is `32*epsilon_float64*max(1,abs(comparator_NRMSE))`, which guards floating-point ties rather than defining a biological effect size.

D2 may escalate only after D1 passes at both ranks. D2 must then pass every LOTO rank/conditioning check, beat D1 aggregate NRMSE, and beat D1 on at least six of the ten omitted transitions, independently at r=2 and r=3.

No model may be selected because its spectral radius is closer to, farther from, or crosses 1.

## 9. J: uncertainty and sensitivity

Days are serial descendants, not iid biological replicates. Therefore the first pilot does not use an iid bootstrap and does not report a pseudo-biological confidence interval.

The frozen model-conditional sensitivity envelope is:

- every admissible leave-one-transition refit;
- one shared-origin block refit removing both day-0-to-day-1 transitions together;
- six leave-one-PBS-state basis refits, with the feature set held fixed, the PBS basis refit on five controls, and all states reprojected before operator fitting.

These are sensitivity analyses, not replacement biological replicates.

If the mathematical unit-circle side changes within the admissible envelope, the result is `INDETERMINATE` and `REFUSE_UNCERTAINTY_SPANS_BOUNDARY`.

## 10. K: cross-timescale transport

Daily and weekly transition operators are source-native objects at different intervals.

The first program explicitly forbids:

```text
rho_week = rho_day^7
rho_day = rho_week^(1/7)
T_week = T_day^7
T_day = matrix_root(T_week, 7)
```

unless a separate semigroup/time-homogeneity program earns that relation.

The first daily-versus-weekly comparison may only compare source-native categorical findings such as adequacy/refusal, mathematical side, D2 escalation and non-normal warning disposition.

## 11. L: A3 material-conclusion schema

The following conclusions are frozen as material before outcome opening:

1. D1 adequacy: `PASS` or `REFUSE`;
2. D1 mathematical unit-circle side after the sensitivity envelope: `BELOW`, `ABOVE`, or `INDETERMINATE`;
3. non-normal warning: `PRESENT`, `ABSENT`, or `INDETERMINATE`;
4. D2 escalation: `EARNED`, `NOT_EARNED`, or `INDETERMINATE`.

If D2 is earned at both ranks, two further conclusions become material:

5. sign of `rho(T_CTX)-rho(T_PBS)`;
6. control and treated mathematical unit-circle side categories.

Any material r=2/r=3 disagreement returns:

`REPRESENTATION_DEPENDENT_NO_TRANSFER`

There is no post-outcome rank winner.

## 12. Unit-circle language

The unit circle in this pilot is a mathematical discrete-time stability boundary only.

`BELOW` means every admissible fit has rho < 1.  
`ABOVE` means every admissible fit has rho > 1.  
Mixed or boundary-touching envelopes are `INDETERMINATE`.

Nothing in this freeze identifies rho=1 with a biological critical boundary or admits Chi_bio.

## 13. Reserved evidence

The following remain outside construction and model selection:

- proliferation;
- ATAC;
- scRNA;
- resistant-clone labels;
- Atlas placement;
- survival or clinical outcomes;
- methylation as a concatenated state variable.

They remain available for later post-construction relational/falsification tests under their separately frozen roles.

## 14. Immediate execution consequence

The design gate for the first short-term G2 pilot is now closed prospectively.

The next safe computational action is to implement an empirical runner that enforces this record mechanically, verifies the exact GSE114446 source hash and SCC25 columns, constructs the frozen control-only state basis at r=2 and r=3, executes D1 plus the prespecified sensitivity/refusal logic, and evaluates D2 only through its frozen escalation gate.

The runner must emit a refusal rather than improvise when any frozen rule cannot be satisfied.
