# GRI Chi_bio temporal prediction / falsification freeze

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome prediction freeze  
**Sources reserved:** chronic SCC25 GSE98812/GSE98815; short-term bulk GSE114446; day-5 scRNA GSE137524  
**Chi_bio outcomes inspected:** NO  
**Biological unity boundary:** NOT_ADMITTED

## 1. Purpose

The source inventory now contains two distinct temporal resolutions of cetuximab response in the same named SCC25 cell line plus a second complete bulk cell line and a day-5 single-cell endpoint. Before choosing an empirical state reduction or computing any candidate Chi_bio value, the scientifically useful cross-source questions are frozen here so the analysis cannot later be rewritten around whichever trajectory looks most attractive.

These are candidate-level falsification questions. They do not assume Chi_bio exists.

## 2. PRED-T1: short-versus-chronic temporal-scale transfer

### Frozen question

After one state representation and time convention are prospectively frozen, can the same SCC25 candidate coordinate be transported between:

```text
GSE114446: daily early response, days 0-5
GSE98812:  weekly chronic adaptation, weeks 1-11
```

without retuning its definition?

### G2-specific prediction

If a time-homogeneous semigroup interpretation is valid over the compared regime,

```text
T_Delta = exp(J Delta)
```

then reference-interval normalization of `rho(T_Delta)` should be mutually compatible within predeclared uncertainty.

### Falsifier

Systematic incompatibility after representation, batch/source, and uncertainty controls counts against a single time-homogeneous G2 interpretation. The result is then reported as time-varying/regime-dependent dynamics or representation non-transfer, not repaired by changing the reference interval post hoc.

### Non-claim

Failure does not imply biological instability; early response and acquired resistance may genuinely occupy different generators.

## 3. PRED-T2: treatment-versus-control generator organization

### Frozen question

Within each temporal experiment, does cetuximab require a different effective transition organization from its time-matched PBS control after the state representation is frozen?

### Allowed outcomes

```text
PRESERVED_OPERATOR_RELATION
TREATMENT_REORGANIZES_OPERATOR
NO_SINGLE_OPERATOR_FOR_ONE_OR_BOTH_ARMS
NOT_IDENTIFIABLE
```

### Falsifier of oversimplified model

If one constant operator cannot reproduce the ordered state transitions within frozen residual/uncertainty rules, the model must refuse time-homogeneity rather than average the nonstationarity away.

No preferred direction of the scalar relative to unity is specified here.

## 4. PRED-T3: cross-cell-line transport

### Frozen question

For the short-term daily source, does a representation and operator family frozen without SCC1 outcome tuning transport from SCC25 to the complete SCC1 daily series?

### Allowed outcomes

```text
REPRESENTATION_AND_OPERATOR_FAMILY_TRANSFER
REPRESENTATION_TRANSFERS_BUT_OPERATOR_REORGANIZES
REPRESENTATION_DEPENDENT_NO_TRANSFER
NOT_IDENTIFIABLE
```

The test concerns structural transport, not equality of candidate scalar values.

### Independence ceiling

SCC25 and SCC1 are different systems but come from the same laboratory program and experiment family. This is internal/cross-system qualification, not external P1.

## 5. PRED-T4: modal/transient information must survive scalar compression

For any G2 analysis, a scalar `rho(T)` below one cannot by itself close the dynamics if:

- the largest singular value indicates one-step transient amplification;
- leading modes are near-degenerate;
- left/right carrier structure is unstable;
- the fitted operator is non-normal;
- one shared operator is rejected.

A future result must therefore report scalar, modal/vector, and system/representation diagnostics together.

## 6. PRED-T5: day-5 single-cell endpoint as carrier/heterogeneity check

The `GSE137524` SCC25 PBS/CTX duplicate single-cell datasets are not a longitudinal same-cell trajectory.

After a bulk state representation is frozen, they may test whether the implicated state dimensions/carriers are:

```text
broadly represented across cells,
restricted to a subpopulation,
or absent/nontransportable at single-cell resolution.
```

They may not be used to retroactively choose the bulk state dimensions and then be claimed as independent confirmation.

## 7. PRED-T6: phenotype timing remains unopened for first operator construction

The proliferation trajectories in the chronic and short-term studies remain response axes, not construction inputs.

The first temporal operator/state freeze must be completed without choosing dimensions, thresholds, or signs based on when proliferation changes.

Only afterward may a frozen prospective question ask whether a candidate coordinate change precedes, coincides with, or follows the independent proliferation transition.

This is the future route to a recovery/resilience/early-warning question. Such a claim is not licensed yet.

## 8. Cross-scale recurrence firewall

Same-cell-line recurrence across daily and weekly experiments is potentially informative but is not automatically evidence of a universal cross-scale law.

Any apparent recurrence must be tested against:

- shared laboratory/source lineage;
- same drug and nominal dose;
- batch and processing differences;
- different temporal regimes;
- state-representation dependence;
- simple exponential/semigroup explanations;
- generic low-rank smoothness.

## 9. Decision table

| Prediction | Pass would support | Failure would imply | Promotion effect |
|---|---|---|---|
| T1 cross-timescale transfer | candidate temporal transport within tested regime | time-varying/regime-dependent or nontransportable dynamics | none by itself |
| T2 treated/control organization | meaningful perturbational system distinction | same organization or model refusal | none by itself |
| T3 SCC25->SCC1 transport | cross-system representation/operator-family robustness | system specificity/refusal | none by itself |
| T4 modal companion | compression does not erase material dynamics | scalar inadequate | narrows candidate |
| T5 single-cell carrier check | cellular support for bulk carrier structure | subpopulation/representation mismatch | narrows interpretation |
| T6 phenotype timing | prospective temporal association after freeze | no timing relation | no rescue/retuning |

## 10. Current stop condition

The questions are now frozen without candidate outcomes. Execution requires an empirical transcriptomic state-reduction freeze and source-file acquisition/verification.

No real Chi_bio value may be computed merely because the temporal sources are now identified.
