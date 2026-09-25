# GRI ↔ Bio Chi Harmange carrier-mapping checkpoint

**Date:** 25 September 2026  
**Status:** SOURCE SCHEMA PASS / EXPLICIT LINEAGE-ID JOIN STILL OPEN  
**Branch:** `gri-biochi-bridge-p0q-20260925`

## Passed

The frozen GSE237228 processed source package is reproducibly reachable.

- metadata: 40,021 rows, 26 columns
- processed cell-barcode file: 40,021 rows
- exact source hashes are pinned
- lineage-assay count fields are present
- condition/state fields are present
- no molecular target was computed

## Carrier gap

The exported metadata exposes `nCount_lineage` and `nFeature_lineage`, but those are assay-count fields, not the lineage identity required for a same-carrier bridge.

Therefore the bridge is **not yet allowed** to treat cells with lineage counts as identified clones/lineages.

The paper describes explicit lineage-barcode assignment, and the released analysis ecosystem contains code for dominant-barcode assignment, but the exact Harmange lineage-ID object/source join must be frozen before using it in B2 or B3.

## Next

Resolve the released lineage-ID assignment object or an equivalent source-defined cell-to-lineage table. If it cannot be recovered reproducibly, Harmange remains scientifically useful but is refused as the first direct same-carrier GRI ↔ Bio Chi bridge and the frozen Shaffer backup opens next.
