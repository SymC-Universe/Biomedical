# Harmange 2023 direct GRI ↔ Bio Chi bridge source refusal

**Date:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Disposition:** REFUSED_FOR_DIRECT_SAME_CARRIER_BRIDGE_AT_CURRENT_REPRODUCIBILITY_LEVEL  
**Failure class:** source-materialization/access limitation, not scientific contradiction

## What passed

- GSE237228 processed metadata and cell barcodes are reproducibly reachable.
- 40,021 cells and the source metadata schema were independently reproduced.
- The authors' experiment-3 analysis script was recovered and hash-pinned.
- The source-native lineage-assignment algorithm was frozen before outcome analysis.
- The publication reports 19,740 accepted lineages with at least 3 cells and 49% represented across all four conditions.
- No B2 or B3 target statistic was opened during source qualification.

## What failed

The public processed GEO RNA export does not contain the lineage-feature rows needed to reconstruct explicit lineage identity.

The authors' public Drive contains the expected lineage-derived object/table names, including `All_lin_BC_3readMin.rds` and `10X3_ModelingData.csv`, but the publicly retrievable copies resolve as zero-byte placeholders in the accessible repository state.

Therefore the exact per-cell/per-lineage carrier cannot currently be materialized from the lightweight released processed objects.

## Why this is a refusal rather than a repair target

A reconstruction from raw SRA/Feature Barcode sequencing remains possible in principle, but would reopen a large raw-sequencing pipeline and Cell Ranger/barcode-processing lineage rather than repair a small mechanical defect.

That work is not required to answer the current bridge question because a pre-frozen backup source exists.

No lineage identity will be inferred from `nCount_lineage`, `nFeature_lineage`, aggregate published percentages, or figure extraction.

## Scientific meaning

Harmange remains admissible as:
- external biological evidence for memory/state switching;
- a Limit Map example of a scientifically strong source that is not presently reproducible at the carrier granularity required by this bridge;
- a possible future raw-data reconstruction target.

It is **not** used as the first direct GRI ↔ Bio Chi same-carrier test.

## Next

Open the already-frozen Shaffer 2017 melanoma backup for outcome-blind B2/B3 source qualification.
