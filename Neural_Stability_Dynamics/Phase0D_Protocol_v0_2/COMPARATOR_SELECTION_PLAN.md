# NSD Native Comparator Selection Plan

Status: **P0 EVIDENCE ROUTE NARROWED; P1 COMPARATOR NOT FROZEN.**

The scientific comparison question must be frozen before decisive comparator performance is inspected.

## Comparator question is now split into two non-interchangeable levels

### A. Estimator-at-declared-order question

> On known-truth multichannel stochastic systems within a declared local-linear/output-only scope, how accurately do SSI-COV and the strongest fair independent structural comparator recover pole and carrier structure when the same correct state order/rank is supplied?

P0 evidence now identifies **Subspace DMD** as the leading independent candidate for this question. It was selected through source-of-record review because it explicitly targets random dynamical systems with observation noise and it survived the same already-fixed P0 stress matrix without the stochastic-process mismatch seen in TLS-DMD.

This question isolates estimator behavior. It does **not** test operational order/rank selection.

### B. Operational structural-recovery question

> When truth is unavailable, can the NSD Structural Engine recover or refuse structure more reliably than a fair Subspace-DMD pipeline using a predeclared method-appropriate rank-selection route?

This question remains **BLOCKED ON ORDER/RANK FAIRNESS**.

A comparator is not fair merely because it is given a convenient fixed rank, nor may the NSD selector be allowed to use development-derived information unavailable to the comparator. Conversely, forcing identical selection mathematics onto method families with different native identification structures can itself create an unfair comparator.

## Current comparator hierarchy

- **Subspace DMD:** leading direct independent stochastic structural comparator candidate; P0 stress-supported, not frozen.
- **TLS-DMD:** snapshot/sensor-noise diagnostic control; preserved mismatch on process-driven stochastic families.
- **Exact DMD:** transparent baseline; known observation-noise bias.
- **OMA/SSI family:** domain precedent and internal lineage comparator, not sufficiently independent to serve as the sole external structural baseline.
- **specparam/FOOOF:** later spectral-state comparator; different target object.
- **PLI/wPLI/connectivity architecture:** later system/connectivity baseline; different target object.
- **optimized/robust DMD variants:** remain in the good-faith search space if the final P1 noise/outlier model requires them.

## Next P0 comparator work

Before MFR-05 can be frozen:

1. sweep SSI-COV order and Subspace-DMD rank on the same development records without using truth for selection;
2. preserve all candidate modes, stability/assignment information, singular spectra and refusals;
3. investigate method-native order/rank selection routes, including multi-order stabilization for SSI and established DMD truncation/rank criteria;
4. qualify candidate selection rules on known-truth systems and known-bad weak-observability/noise cases;
5. predeclare whether P1 tests estimator-at-declared-order, operational selection, or both as separate claim families;
6. only then freeze comparator identity, rank/order rule, metric and consequence of failure.

Possible final outcome remains `COMPARATOR_IDENTIFIED` or `NO_NATIVE_COMPARATOR` for a precisely frozen task. A weak or assumption-mismatched baseline will not be manufactured merely to create an ADDS result.
