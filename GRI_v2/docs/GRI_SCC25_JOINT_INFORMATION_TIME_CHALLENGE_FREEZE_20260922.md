# GRI SCC25 time-conditioned joint-information challenge

**Date:** 2026-09-22  
**Status:** FROZEN POST-RESULT P0-Q QUALIFICATION CHALLENGE  
**Trigger:** representation-dependent P0-D result from run 35728155463  
**Promotion effect:** NONE

## Challenge question

Does the methylation-context increment survive after explicit trajectory time is included in both the local-only and joint models?

## Frozen models

For each existing coequal rank pair `r in {2,3}`, `m in {2,3}`:

Time-conditioned local comparator:

```text
RNA_next = A*RNA_now + b*treatment + g*week + h*(treatment*week) + c
```

Time-conditioned joint model:

```text
RNA_next = A*RNA_now + C*METH_now + b*treatment + g*week + h*(treatment*week) + c
```

Week is the integer current-state week `1..10`, centered across the 20 transitions before fitting. No polynomial degree, spline, breakpoint, or resistance-phase boundary is selected from the observed result.

Estimator and evaluation remain OLS and leave-one-transition-out. Every omitted-transition fit must retain full column rank.

## Primary qualification statistic

```text
conditional_improvement_beyond_time = 1 - SSE_joint_time / SSE_local_time
```

Also report:
- joint-vs-local transition win fraction;
- both models versus persistence and arm-specific mean baselines;
- the same 81 within-arm methylation circular-shift configurations, with time terms left unshifted.

## Adjudication

This challenge is not allowed to rescue a particular rank pair.

Per-rank labels:
- `CONTEXT_ADDS_BEYOND_TIME`: positive improvement, joint beats both simple baselines, and alignment p <= 0.10.
- `TIME_SUBSUMES_CONTEXT_INCREMENT`: improvement <= 0.
- `CONTEXT_INCREMENT_UNRESOLVED_BEYOND_TIME`: positive improvement but alignment screen not cleared.
- `REFUSE_ILL_CONDITIONED`: any required leave-one-out design loses full rank.

Cross-representation conclusion remains `REPRESENTATION_DEPENDENT` unless all coequal rank pairs produce the same material label.

## Interpretation ceiling

A positive result means only that the tested methylation representation contains held-out predictive information not captured by current RNA modal state, treatment arm, linear week, or arm-specific linear week trend in this SCC25 source. It is not evidence of methylation causality or a universal capital-Chi relation.
