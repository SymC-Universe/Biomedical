# GRI v2 current status

Status date: 2026-09-05

## Closed gates

- F2 synthetic challenge: complete.
- F3 baseline competition: complete.
- F4: closed NARROW.
- P0 split and prediction protocol: frozen.
- D1 methylation discovery transforms: closed.
- D2 RNA discovery targets: closed.
- D3 discovery audit/model: closed PASS as discovery-only gate.
- D4 untouched REPLICATION: closed and independently audited.

D4 key result: the all-methylation ridge model improved over the covariate-only comparator in 18/19 cancers in untouched REPLICATION; exact one-sided sign test p = 3.81e-5, but the frozen 24-cancer promotion floor was not met. The semantic Hallmark-label-specific branch did not promote. PCPG was the single model-comparison loss and the only audit-state disagreement, moving from discovery GLOBAL_SHARED_ONLY/CAUTION to replication WITHIN_LAYER_ONLY/REFUSE.

## Active gate

**P3 pre-open scientific hold.**

Canonical audit:

`docs/TOOL_PREDICTION_P0_P3_PREOPEN_IDENTIFIABILITY_AUDIT_20260905.md`

Machine-readable snapshot:

`config/tool_prediction_p0_p3_preopen_identifiability_20260905.json`

FINAL_HOLDOUT remains sealed. No final methylation numeric values or RNA target scores have been inspected.

## Hold reason

The frozen discovery decision class is one class per cancer, while the frozen P3 primary test asks for within-cancer ACCEPT-versus-REFUSE risk comparisons. No cancer can contain both classes under that state granularity. In addition, all 19 discovery cancers are GLOBAL_SHARED_ONLY/CAUTION, so FULL_AUDIT has zero ACCEPT and zero REFUSE coverage. The prospectively frozen comparator selectors are also all-or-none across the 19 cancers.

Therefore the primary P3 selective-prediction/refusal contrast is non-identifiable without changing the frozen scientific rule after REPLICATION was inspected. That would create a new predictive version and cannot use the current FINAL_HOLDOUT as if it remained prospective for the changed rule.

## Still-valid downstream work

The unchanged discovery-trained predictors can still be evaluated on FINAL_HOLDOUT for the separately frozen final P1 direct-prediction question. If that is executed, P3 selective/refusal must be reported as NOT_EVALUABLE rather than rescued post hoc.

FINAL_HOLDOUT metadata-only closure before opening molecular values:

- eligible participants: 1,686 across the same 19 cancers;
- composition-complete participants: 1,534;
- inherited minimum model-complete n: 30;
- PAAD has 26 complete final participants and is below the inherited primary model-evaluation minimum;
- the other 18 cancers meet the minimum.

External independent validation remains mandatory before general biomedical tool promotion.

## User decision required

This is a scientific, not mechanical, decision point: either execute the existing FINAL_HOLDOUT strictly for the valid frozen final P1 direct-prediction evaluation while recording P3 selective refusal as NOT_EVALUABLE, or leave FINAL_HOLDOUT sealed. A redesigned P3 selective rule requires a new prospectively frozen external/future-data validation path.
