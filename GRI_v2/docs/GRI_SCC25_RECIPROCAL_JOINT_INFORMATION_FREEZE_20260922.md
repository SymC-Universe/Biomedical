# GRI SCC25 reciprocal joint-information challenge: RNA local/modal state -> methylation context

**Date:** 2026-09-22  
**Status:** FROZEN PRE-RESULT P0-Q RECIPROCAL CHALLENGE  
**Trigger:** the frozen forward-direction time-conditioned challenge did not yield a representation-robust `CONTEXT_ADDS_BEYOND_TIME` result  
**Promotion effect:** NONE  
**Scalar chi:** REFUSED for the current SCC25 R1/A3 representation; not assumed here

## Why this is the next question

The joint-meaning program predeclared both directions:

```text
partial-system/context_t -> local/modal_(t+1)
local/modal_t -> partial-system/context_(t+1)
```

The forward SCC25 pilot tested the first direction using methylation as a bounded partial system/context representation and RNA modal state as the local object. Explicit week and treatment-by-week conditioning weakened that result so that no coequal rank pair earned the frozen `CONTEXT_ADDS_BEYOND_TIME` label.

This challenge tests the reciprocal direction. It is not allowed to rescue the forward result.

## Question

Does current RNA local/modal state improve held-out prediction of next-week methylation organization beyond current methylation organization, treatment arm, linear week, and treatment-by-week trend?

This tests information in the `local/modal -> partial-X` direction only. The methylation coordinate set is not declared to be the complete capital-Chi architecture.

## Frozen representations

Use exactly the already frozen source bindings and unsupervised control-derived bases from the forward SCC25 challenge:

- RNA: GSE98812, PBS-only R1 basis, ranks `r in {2,3}`;
- methylation: GSE98813, complete-case CpGs, PBS-only sample-space PCA, ranks `m in {2,3}`;
- paired states: the frozen 22-state PBS/cetuximab weekly manifest;
- no baseline or resistant-clone states;
- no outcome/time-course feature selection;
- no scalar biological chi.

No representation is changed in response to the forward result.

## Frozen models

For each coequal rank pair `(r,m)`:

System-history/time comparator:

```text
METH_next = B*METH_now + b*treatment + g*week + h*(treatment*week) + c
```

Joint reciprocal model:

```text
METH_next = B*METH_now + D*RNA_now + b*treatment + g*week + h*(treatment*week) + c
```

Week is current-state week 1..10, centered over the 20 transitions. Estimator is OLS. Evaluation is leave-one-transition-out. Every omitted-transition training design must retain full column rank.

## Primary statistic

```text
conditional_improvement_reciprocal =
    1 - SSE_joint_reciprocal / SSE_system_history
```

Also report:
- joint-versus-system-history transition win fraction;
- both models versus methylation persistence;
- both models versus arm-specific leave-one-transition-out mean next methylation state.

## Alignment null

Circularly shift the current RNA sequence independently within each arm while leaving:
- current methylation,
- next methylation,
- treatment,
- week,
- treatment-by-week

unaltered.

Use every pair of nonzero within-arm shifts:

```text
PBS shift = 1..9
CTX shift = 1..9
=> 81 null configurations
```

For each configuration rerun the identical leave-one-transition-out joint model.

```text
p_alignment =
    (1 + count(null_improvement >= observed_improvement)) / 82
```

This is exploratory P0-Q qualification, not a confirmatory p-value.

## Frozen labels

Per rank pair:

- `LOCAL_ADDS_TO_SYSTEM_BEYOND_TIME`: improvement > 0, joint beats persistence and arm-mean baselines, and alignment p <= 0.10.
- `SYSTEM_HISTORY_SUFFICIENT_FOR_THIS_TASK`: improvement <= 0.
- `LOCAL_INCREMENT_UNRESOLVED_BEYOND_TIME`: improvement > 0 but the alignment screen is not cleared.
- `REFUSE_ILL_CONDITIONED`: any required leave-one-out design loses full rank.
- `BOTH_INADEQUATE`: both fitted models fail to beat the better simple baseline.

Cross-representation disposition is `REPRESENTATION_DEPENDENT` unless all four coequal rank pairs yield the same material label.

## Claim ceiling

A positive result would mean only that the tested RNA local/modal representation contains held-out predictive information about the tested future methylation representation beyond methylation history and the frozen linear time terms in this SCC25 source.

It would not establish:
- RNA -> methylation causality;
- a biological scalar chi;
- a complete capital-Chi object;
- clinical prediction;
- cancer-wide generality;
- cross-domain SymC validity.

## Stop rule

After this reciprocal challenge, do not add another covariate or representation to chase a favorable SCC25 result. Adjudicate both directions together. Any next SCC25 extension must answer a different predeclared question, such as an external phenotype/interaction test, or be motivated by an independently identified methodological flaw.
