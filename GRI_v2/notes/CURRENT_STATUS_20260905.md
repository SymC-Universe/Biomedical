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

## P3-v1 outcome

The original categorical P3 selective-prediction test is **NOT_EVALUABLE** in this P0 realization. The discovery state was cancer-level while the planned primary risk comparison required within-cancer ACCEPT-versus-REFUSE units, and all 19 discovery cancers were GLOBAL_SHARED_ONLY/CAUTION.

This result is preserved as a genuine design failure. It is not rewritten into a pass.

Canonical audit:

`docs/TOOL_PREDICTION_P0_P3_PREOPEN_IDENTIFIABILITY_AUDIT_20260905.md`

## Active gate

**P3-v2 development-informed final-holdout test, frozen before final molecular access.**

D4 is treated explicitly as a development/validation partition. Because FINAL_HOLDOUT molecular values remain untouched, a new post-D4 version can be frozen now and tested on FINAL_HOLDOUT with transparent provenance. It is not described as the original preregistered P3 test.

Canonical amendment:

`docs/TOOL_PREDICTION_P3_V2_POST_D4_AMENDMENT_20260905.md`

Machine-readable config:

`config/tool_prediction_p3_v2_20260905.json`

P3-v2 uses a cancer-level continuous confidence ordering rather than inventing post-hoc Hallmark ACCEPT/REFUSE labels. The primary selector is the minimum discovery raw Delta_CKA across PRIMARY_PUBLICATION and MASKED_TECHNICAL. D4 development analysis motivated this choice because it retained risk-ordering information lost by the categorical state. No fitted threshold or hybrid score is permitted.

The original P1 final direct-prediction comparison is retained unchanged.

## FINAL_HOLDOUT firewall

FINAL_HOLDOUT remains sealed at this status update. No final methylation numeric values or RNA target scores have been inspected.

Metadata-only closure:

- eligible participants: 1,686 across the same 19 cancers;
- composition-complete participants: 1,534;
- inherited minimum model-complete n: 30;
- PAAD has 26 complete final participants and is excluded from primary final inference without rescue;
- the other 18 cancers meet the minimum.

## Interpretation discipline

P3-v1 categorical refusal remains NOT_EVALUABLE even if P3-v2 succeeds.

P3-v2 can establish only whether a D4-informed continuous global-geometry confidence ordering prospectively stratifies prediction risk in the untouched internal TCGA final partition. Good numerical prediction does not rescue failed Hallmark semantic specificity, and semantic failure does not automatically imply poor numerical prediction.

External independent validation remains mandatory before general biomedical tool promotion.

## Exact next operation

Build and regression-test the FINAL_HOLDOUT projection/scoring package against the frozen P3-v2 contract, then execute once on the unchanged local methylation source and Hallmark RNA cache. Mechanical failures are to be repaired without changing the frozen P3-v2 science.
