# GRI pathway-specific independence ledger

**Date:** 2026-09-11  
**Protocol:** v0.7.1A Section A.6 + v0.7.1 MFR-10 / Atlas independence  
**Status:** WORKING LEDGER

## Rule

Independence is evaluated against the circularity pathway relevant to the claim. Shared context does not automatically destroy independence, but any shared information capable of forcing the reported agreement weakens or refuses that independence claim.

## Dimensions

For each evidence path record separately:

- `data_independence`
- `cohort_system_independence`
- `outcome_independence`
- `parameter_tuning_independence`
- `method_independence`
- `atlas_independence`
- `source_literature_independence`
- `temporal_independence`

Allowed per-path states for this working ledger:

- `INDEPENDENT`
- `PARTIALLY_INDEPENDENT`
- `NON_INDEPENDENT`
- `NOT_APPLICABLE`
- `UNRESOLVED`

## Current evidence paths

| Evidence path | Data | Cohort/system | Outcome | Tuning/parameters | Method | Atlas | Source/literature | Temporal | Overall use |
|---|---|---|---|---|---|---|---|---|---|
| Stage A/A1.1 RNA architecture within TCGA | NON_INDEPENDENT for later GRI validation | NON_INDEPENDENT | NOT_APPLICABLE/descriptive | Development-informed | PARTIAL | NOT_APPLICABLE | PARTIAL | NON_INDEPENDENT/static | Development / P0-D |
| B1 purity/leukocyte projection within TCGA | NON_INDEPENDENT for later Engine validation | NON_INDEPENDENT | NOT_APPLICABLE/descriptive | Development-fixed before later stages | PARTIAL | NOT_APPLICABLE | PARTIAL | NON_INDEPENDENT/static | P0-D/P0-Q context attack |
| B2 RPPA orthogonal modality within TCGA | PARTIALLY_INDEPENDENT by modality | NON_INDEPENDENT by cohort program | PARTIAL | Development | PARTIAL | NOT_APPLICABLE | PARTIAL | NON_INDEPENDENT/static | Development orthogonal support only |
| B2 genomic branch within TCGA | PARTIALLY_INDEPENDENT by modality | NON_INDEPENDENT | PARTIAL | Development | PARTIAL | NOT_APPLICABLE | PARTIAL | NON_INDEPENDENT/static | Development context only |
| F2 synthetic known-truth | Synthetic independent of TCGA biology | Synthetic system | Known truth constructed | Qualification-tuned across versions allowed in P0-Q | PARTIAL | NOT_APPLICABLE | NOT_APPLICABLE | NOT_APPLICABLE | Method qualification, never empirical validation |
| F3 AJIVE/MOFA2 comparisons | Same synthetic benchmark families | Same synthetic systems | Same known-truth structure | Comparator route frozen for the feasibility test | Method implementations independent of GRI code | NOT_APPLICABLE | External methods | NOT_APPLICABLE | Method-scope comparison |
| P0 DISCOVERY -> REPLICATION | Distinct patient partitions, same TCGA program/source | PARTIALLY_INDEPENDENT | RNA targets same construction family | Discovery-trained transforms; replication untouched by final outcomes | Same method | NOT_APPLICABLE | Same source families | NON_INDEPENDENT/static | Internal replication, not external validation |
| P3-v2 FINAL_HOLDOUT | Distinct untouched patient partition at opening | PARTIALLY_INDEPENDENT, same TCGA program | FINAL outcomes untouched pre-freeze | P3-v2 fixed before FINAL opening, but informed by prior D4 evidence | Same method | NOT_APPLICABLE | Same source families | NON_INDEPENDENT/static | Valid one-shot internal amended holdout, not external P1 |
| Stage C1 | Same TCGA source lineage | NON_INDEPENDENT for external generalization | C1 endpoints frozen, but v2.1/v2.2 science-adjacent missingness amendments occurred pre-effect inspection | Mostly frozen with explicit amendments | Same method lineage | NOT_APPLICABLE | Same source families | NON_INDEPENDENT/static | Historical preregistered-plus-amended internal evidence |
| Post-C1 sensitivity v2.2 | Same C1 state | NON_INDEPENDENT | Same observed lineage | Frozen sensitivity before its own outputs | Same/reconstruction methods | NOT_APPLICABLE | Same source families | NON_INDEPENDENT/static | P0-Q adversarial qualification only |
| Current TCGA-derived future Atlas rows | NON_INDEPENDENT for validating current Engine | NON_INDEPENDENT | May share labels/outcomes | Development history overlaps | Same program | NON_INDEPENDENT_FOR_ENGINE_VALIDATION | Same source family | NON_INDEPENDENT/static | Descriptive historical Atlas context only |
| Future external cohort not used in GRI development | Candidate INDEPENDENT | Candidate INDEPENDENT | Must be untouched | Must freeze before opening | Same frozen Engine allowed | Atlas relation separately graded | Source family independently verified | Depends on design | Candidate P1 evidence |
| Future longitudinal/perturbational cohort | Candidate INDEPENDENT | Candidate INDEPENDENT | Must be untouched | Must freeze before opening | Same frozen Engine allowed | Atlas relation separately graded | Independently sourced | Potentially INDEPENDENT | Required for temporal inheritance/recovery claims |

## Key conclusions

1. FINAL_HOLDOUT has meaningful **patient-partition/outcome independence** relative to the amended P3-v2 test, but it does not have cohort/source independence from the broader TCGA development program.
2. Orthogonal modalities inside TCGA add modality independence, not full cohort independence.
3. Synthetic known-truth evidence can qualify method behavior but cannot validate oncology claims.
4. Current TCGA rows may populate historical/development Atlas context but are `NON_INDEPENDENT_FOR_ENGINE_VALIDATION` for the current Engine.
5. The future external P1 claim must specify exactly which independence dimensions matter for the claim being tested rather than asserting a blanket 'independent dataset' label.

## Future record template

For each external claim, complete:

```text
claim_id:
data_independence:
cohort_system_independence:
outcome_independence:
parameter_tuning_independence:
method_independence:
atlas_independence:
source_literature_independence:
temporal_independence:
shared_information_that_could_force_agreement:
independence_conclusion:
```

No single overall grade substitutes for the pathway map where the dimensions differ.