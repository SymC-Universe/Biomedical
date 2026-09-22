# GRI SCC25 reciprocal joint-information P0-Q post-result audit

**Date:** 2026-09-22  
**Run:** 35731765085  
**Head:** `140a629d56a9e1e8e287501d75a1d74f49ab67dd`  
**Artifact:** `GRI_SCC25_RECIPROCAL_JOINT_INFORMATION_P0Q_V01`, ID `10695383871`  
**Artifact ZIP SHA-256:** `1899ce8b25ab33519097df2edf8658852097fc54d8d636b47a7af7fead98f941`  
**Status:** P0-Q POST-RESULT AUDIT  
**Promotion effect:** NONE

## Reciprocal result

The prospectively frozen reciprocal challenge completed on the same hash-bound SCC25 RNA and methylation sources and the same coequal rank grid used in the forward challenge. Scalar biological chi remained refused and was not constructed.

| RNA rank | methylation rank | reciprocal improvement | joint transition win fraction | alignment p | frozen label |
| ---: | ---: | ---: | ---: | ---: | --- |
| 2 | 2 | +0.002596 | 0.50 | 0.2073171 | LOCAL_INCREMENT_UNRESOLVED_BEYOND_TIME |
| 2 | 3 | +0.034056 | 0.65 | 0.2926829 | BOTH_INADEQUATE |
| 3 | 2 | +0.416459 | 0.60 | 0.0121951 | LOCAL_ADDS_TO_SYSTEM_BEYOND_TIME |
| 3 | 3 | +0.343216 | 0.60 | 0.0243902 | BOTH_INADEQUATE |

Cross-representation disposition:

`REPRESENTATION_DEPENDENT`

## What is supported

For the RNA-rank-3 / methylation-rank-2 representation, current RNA modal state contains substantial held-out information about next-week methylation state beyond current methylation state, treatment arm, linear week and treatment-by-week trend. The joint model also beats both frozen simple baselines and the observed increment exceeds every one of the 81 nonzero within-arm RNA-alignment shifts.

This is a legitimate P0-Q directional signal in one predeclared representation.

## Why it is not a general reciprocal relation

The result does not survive the coequal representation grid as a common label.

- RNA rank 2 adds essentially no resolved increment for methylation rank 2.
- Both methylation-rank-3 tasks are classed `BOTH_INADEQUATE` because even where adding RNA reduces the fitted system-history SSE, the joint model does not beat the stronger simple baseline.
- Selecting the favorable RNA-rank-3 / methylation-rank-2 result alone would violate the frozen representation-sensitivity rule.

Therefore the SCC25 reciprocal conclusion remains representation-dependent.

## Joint adjudication with the forward direction

The time-conditioned forward challenge produced:

- methylation-rank-2 residual increments for RNA ranks 2 and 3, but neither cleared the frozen alignment threshold after explicit time;
- methylation-rank-3 increments were negative;
- no coequal rank pair retained `CONTEXT_ADDS_BEYOND_TIME`.

The reciprocal challenge therefore gives a directional asymmetry in the current bounded representation:

```text
methylation context_t -> RNA modal_(t+1):
    unresolved / time-sensitive / representation-dependent

RNA modal_t -> methylation context_(t+1):
    one strong predeclared r=3,m=2 signal,
    but representation-dependent overall
```

This does not establish a one-way causal mechanism. It establishes only that predictive information is not symmetric under the tested reductions.

## GOM interpretation

The result should be carried as a Function/Limit finding, not compressed into a favorable scalar narrative:

- scalar chi is refused in the current SCC25 representation;
- local/modal and broader-system coordinates can still be jointly investigated;
- the direction and amount of incremental information depend on representation;
- time/progression explains part of the apparent forward relation;
- a reduced methylation representation can retain information that is forecastable from richer RNA modal state in one rank choice;
- the current data do not license a universal capital-Chi ontology.

## Stop-rule consequence

Do not add ranks, covariates, nonlinear time terms or alternate filters to rescue either direction.

The next SCC25 extension, if executed, must ask a distinct frozen question. The highest-value remaining joint-meaning question is the external-outcome interaction test:

```text
Y_(t+1) ~ local_t
Y_(t+1) ~ system_t
Y_(t+1) ~ local_t + system_t
Y_(t+1) ~ local_t + system_t + local_t:system_t
```

where `Y` must be an outcome not used to construct either representation, such as the source proliferation/resistance phenotype if its temporal alignment and provenance pass an independent preflight.

No such outcome-bearing interaction computation should start before that phenotype is separately qualified and the interaction test is frozen.
