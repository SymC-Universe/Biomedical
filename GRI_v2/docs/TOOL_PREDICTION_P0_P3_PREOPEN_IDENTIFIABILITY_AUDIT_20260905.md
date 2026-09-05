# P0 P3 pre-open identifiability audit

**Date:** 2026-09-05  
**Status:** **SCIENTIFIC HOLD — P3 SELECTIVE-PREDICTION PRIMARY TEST IS NON-IDENTIFIABLE UNDER THE FROZEN P0 ARCHITECTURE**

## Firewall status

This audit was performed **before opening FINAL_HOLDOUT molecular values**. It uses only the frozen P0 protocol, frozen DISCOVERY audit outputs, split/eligibility metadata, and already-approved B1 covariate availability.

- FINAL_HOLDOUT methylation numeric values parsed: **false**
- FINAL_HOLDOUT RNA target scores generated: **false**
- model/transform/composition refit: **false**
- participant reassignment or covariate imputation: **false**

D4 result ZIP SHA-256: `b8ed27a43c1d7ee356f465d3ad90d1fda5e8269ee4038a449b9ba70342fc6be6`

## The scientific hold

The frozen P0 protocol defines one discovery audit state and one ACCEPT/CAUTION/REFUSE decision class **per cancer**. Its P3 section then asks for a within-cancer comparison of REFUSE and ACCEPT cancer-Hallmark risks for cancers containing both classes. Under the implemented frozen state granularity, a cancer cannot simultaneously contain both decision classes. The planned primary within-cancer exact sign test therefore has no valid sampling units.

This is not a software failure and it cannot be repaired mechanically. Changing the decision granularity after D4/REPLICATION has been inspected would create a new scientific version. The frozen P0 protocol explicitly prohibits treating the existing FINAL_HOLDOUT as prospective evidence for such a changed rule.

A second, independent identifiability problem makes the current P3 FULL_AUDIT contrast degenerate even if one ignored the granularity mismatch: **all 19 discovery cancers are `GLOBAL_SHARED_ONLY / CAUTION`**. Therefore:

- ACCEPT-only coverage = **0/19 cancers**;
- ACCEPT + CAUTION coverage = **19/19 cancers**;
- all-unit coverage = **19/19 cancers**;
- REFUSE coverage = **0/19 cancers**.

The FULL_AUDIT coverage-risk curve consequently has no selective contrast to estimate.

## Frozen comparator/ablation selectors before FINAL_HOLDOUT

The same pre-open audit applied the already-frozen selector rules to DISCOVERY only:

| Selector | Favorable cancers | Coverage |
|---|---:|---:|
| GLOBAL_ONLY | 19/19 | 100% |
| NAIVE_SEMANTIC | 19/19 | 100% |
| NO_LABEL_NULL | 19/19 | 100% |
| NO_COMPOSITION_ATTACK | 0/19 | 0% |
| NO_TECHNICAL_TRACK | 0/19 | 0% |
| FULL_NARROWED_AUDIT | 0/19 | 0% |

Thus none of the prospectively frozen selector ablations produces a nontrivial cancer-level coverage set for P3. FINAL_HOLDOUT errors cannot fix that fact without post-hoc rule creation.

## FINAL_HOLDOUT metadata closure

The untouched partition contains **1,686** eligible participants across the same 19 cancers. No molecular target values were used for these counts.

Composition-complete participants under the already-frozen B1 attachment rule: **1,534**.

The inherited minimum model-complete case count is **30**. PAAD has **26** complete FINAL_HOLDOUT participants and therefore falls below that pre-existing minimum. No rescue, imputation, or reassignment is permitted. The remaining 18 cancers meet the minimum.

## What remains scientifically valid

The current FINAL_HOLDOUT can still answer the **separately frozen final P1 direct-prediction question** using the unchanged discovery-trained models. That would test whether the D4 predictive advantage generalizes to a second untouched internal partition. It would **not** validate selective prediction/refusal.

If executed under the unchanged P0 rules, P3 must report the FULL_AUDIT selective-prediction result as **NOT_EVALUABLE** rather than inventing a new threshold or Hallmark-level class after D4.

A future selective/refusal claim requires a new prospectively frozen design on independent external or genuinely future data. External validation is already mandatory under the program objective.

## Hold classification

**SCIENTIFIC, not mechanical.**

The unresolved decision is whether to spend the still-sealed FINAL_HOLDOUT now on the valid final P1 prediction evaluation while recording P3 selective refusal as NOT_EVALUABLE, or to leave it sealed. A redesigned P3 selector cannot use this holdout as prospective validation under the existing no-post-result-rescue rule.
