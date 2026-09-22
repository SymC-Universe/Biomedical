# GRI SCC25 joint-information P0-D pilot: RNA local/modal state versus methylation system context

**Date:** 2026-09-22  
**Status:** PRE-RESULT P0-D EXPLORATORY FREEZE FOR ONE BOUNDED PILOT  
**Promotion effect:** NONE  
**Scalar chi:** NOT REQUIRED / NOT ASSUMED  
**Purpose:** test the first empirical `Χ_t -> local/modal_{t+1}` conditional-information question in the paired weekly SCC25 source without manufacturing a biological scalar.

## Native question

Does methylation/epigenetic context at week `t` improve held-out prediction of the next-week RNA modal state beyond the current RNA modal state, treatment arm, and intercept?

This is deliberately narrower than claiming that methylation causes RNA dynamics or that a capital-Chi object has been established.

## Sources

RNA:
- GSE98812 `GSE98812_GEOExprsData.txt.gz`
- frozen SHA-256 `1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5`

Methylation:
- GSE98813 `GSE98813_series_matrix.txt.gz`
- frozen SHA-256 `c5ee581ee6dbb258bb352e86fd1a7aa5ed6f9979550352accaeca8b0d093292e`

State pairing:
- the already frozen 22 paired weekly PBS/100 nM cetuximab states in `config/gri_scc25_paired_timecourse_manifest_p0d_v0_1.json`.

No baseline or stable resistant-clone states enter this pilot.

## RNA local/modal representation

Reuse the already frozen R1 control-only unsupervised construction without changing it:

1. direct hash-bound public processed values;
2. feature gate: source value >= 1 in at least 6 of 11 PBS states;
3. transform `log2(source_value + 1)`;
4. center each retained gene by its eleven-state PBS mean;
5. fit SVD/PCA on PBS states only;
6. project both arms through the fixed PBS basis;
7. evaluate RNA ranks `r = 2` and `r = 3` as coequal representation sensitivities.

This pilot does not reinterpret the G2 spectral radius as scalar biological chi.

## Methylation system/context representation

Use the full processed beta-value matrix without outcome/time-course feature selection.

For each CpG row:

1. require finite numeric values in all 22 main trajectory states;
2. center that CpG by its eleven-state PBS mean;
3. fit a PBS-only sample-space PCA exactly through the PBS Gram matrix;
4. project all 22 states through that fixed PBS basis;
5. evaluate methylation ranks `m = 2` and `m = 3` coequally.

No CpG is selected by treatment separation, resistance timing, RNA prediction, proliferation, or a desired result.

## Predictive comparison

For each `(r,m) in {(2,2),(2,3),(3,2),(3,3)}`, construct twenty one-week transitions:

- ten PBS transitions C1->C2 through C10->C11;
- ten cetuximab transitions C1->C2 through C10->C11.

Local model:

```text
RNA_next = A * RNA_now + b * treatment + c
```

Joint model:

```text
RNA_next = A * RNA_now + C * METH_now + b * treatment + c
```

Both are ordinary least-squares models and are evaluated by leave-one-transition-out prediction. Every omitted-transition fit must have full column rank. No ridge strength or model complexity is tuned from outcomes.

## Primary exploratory statistic

For held-out squared prediction error summed over all RNA modal coordinates:

```text
conditional_improvement = 1 - SSE_joint / SSE_local
```

Also report the fraction of omitted transitions for which joint squared error is lower than local-only squared error.

No positive threshold is used for promotion because this is P0-D.

## Alignment null

To test whether any gain depends on the actual week-to-week pairing rather than merely adding extra predictors, circularly shift the methylation-current-state sequence within each arm.

Use every pair of nonzero arm-specific shifts:

```text
PBS shift = 1..9
CTX shift = 1..9
=> 81 alignment-null configurations
```

For each configuration rerun the identical leave-one-transition-out joint model.

Report:

```text
p_alignment = (1 + count(null_improvement >= observed_improvement)) / 82
```

This p-value is exploratory and is not a confirmatory biological significance claim.

## Interpretation classes

- `SYSTEM_CONTEXT_ADDS_INFORMATION`: observed improvement is positive and exceeds most alignment-null values.
- `LOCAL_MODAL_SUFFICIENT_FOR_THIS_TASK`: joint model does not improve materially over local-only.
- `ALIGNMENT_DEPENDENT_UNRESOLVED`: apparent improvement is not distinct from shifted-context nulls.
- `REPRESENTATION_DEPENDENT`: rank-pair conclusions differ materially.
- `REFUSE_ILL_CONDITIONED`: any required leave-one-out design loses full rank.
- `BOTH_INADEQUATE`: neither model predicts adequately relative to simple source-native baselines.
- `STANDARD_TOOLKIT_SUBSUMES`: later native comparator work shows no distinct SymC increment.

These are P0-D labels only.

## Baselines and limits

Also compute:
- persistence in RNA modal state;
- arm-specific leave-one-transition-out mean next state.

The weekly states are serial pooled measurements, not independent biological replicates. No iid bootstrap is allowed. A positive result would establish only conditional predictive information in this source and representation, not methylation causality, clinical utility, a universal scalar, or a cancer-wide capital-Chi ontology.

## Success condition for this pilot

The computation is successful when all four rank-pair analyses either produce complete held-out/error/null records or transparently refuse. Scientific success does not require a positive effect.

## Next gate

If a reproducible conditional-information effect appears, collide it against source-native CoGAPS/MEFISTO-style temporal multi-view descriptions and then test transport on an independent system. If no effect appears, preserve the negative result and test the reciprocal direction `local/modal_t -> Χ_{t+1}` only under a separately frozen question.
