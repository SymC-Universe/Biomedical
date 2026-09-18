# GRI Conglomerate Chi C1 E/G/P fragment closure

**Date:** 2026-09-18  
**Branch:** `gri-conglomerate-chi-tool-v1-20260918`  
**Workflow run:** `35338519850`  
**Head commit:** `8ebc0735b0e49e9833ef0dc980efc3b8f46c6724`  
**Conclusion:** `success`  
**Artifact:** `gri-conglomerate-chi-c1-egp-fragment-20260918`  
**Artifact ID:** `10544167378`  
**Artifact SHA-256:** `4a65582987f3d18e1454cfab7e5c66b66b187c9ecdd501b764f8f3c92f898805`

## Materialized carrier fragment

```text
status = C1_EGP_RAW_BLOCK_FRAGMENT_MATERIALIZED
blocks = E,G,P
entities_total = 10,262
features_total = 196
rows_total = 1,444,026
E rows = 19,354
G rows = 48,374
P rows = 1,376,298
fragment_sha256 = ea42ddbb874de8928f8ba6aa0c4fcdc7fb26b23fe4888ca36a766c213b4b0ca4
```

The fragment uses the exact frozen five primary genomic coordinates and the exact frozen 189-feature RPPA common panel. All five smaller public source files re-matched their frozen SHA-256 identities during execution.

## Cancer-identity reconciliation

The first E/G/P attempt correctly hard-stopped when RPPA `TumorType=CORE` disagreed with the PanCanAtlas cancer labels `COAD` and `READ`. This was diagnosed as source-label granularity, not a biological conflict: the frozen Stage-B2 lineage inherited `cancer_type` from Stage A rather than from RPPA `TumorType`.

The repaired run therefore used the leukocyte PanCanAtlas source as the temporary cancer-label authority for this raw fragment, retained RPPA `TumorType` only as audited source metadata, and recorded the 493 label-granularity disagreements (`COAD::CORE=364`, `READ::CORE=129`). Stage-A identity remains the final authority once its cache identity is rematerialized.

## Claim ceiling

This closes only raw block materialization for E/G/P. No cross-block aggregation, diagnostic or predictive fit, temporal interpretation, scalar Chi value, unity boundary, causal claim, or clinical claim was created.

## Next

Complete R/S/M/Q materialization and Stage-A identity/cache reconciliation, then combine validated fragments under the frozen C1 carrier schema.
