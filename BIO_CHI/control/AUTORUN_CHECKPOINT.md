# GRI ↔ Bio Chi autonomous continuation checkpoint

**Last updated:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Status:** ACTIVE SOURCE/CARRIER QUALIFICATION  
**Authority:** SymC General Operations Manual v0.8.6 + GRI controls + Bio Chi three-object nomenclature.

## Resume here

Do not resume from the closed Su oncology stop. The active program is the GRI ↔ Bio Chi bridge.

### Completed in this bridge
- bridge question and anti-collapse rules frozen before new outcomes;
- automated bridge-feasibility audit: PASS;
- no prospective B1 scalar bridge candidate currently available;
- Harmange 2023 selected prospectively for B2/B3 based on design/source structure;
- first Harmange schema run failed mechanically on Python Boolean syntax and is preserved;
- exact repair rerun passed;
- GSE237228 metadata: 40,021 rows / 26 columns, SHA-256 `f22aaf6947d38a018c0c4d13ceedacbd3bdffc296f727e171b66a21b7a06434b`;
- processed cell-barcode file: 40,021 rows, SHA-256 `3e2fdc6d8ab9100c0fa45916fd000c4e541b83810ce449911679c3f03d26403a`;
- lineage-assay and condition/state fields are present;
- no target molecular outcome has been computed.

### Current carrier gap
The GEO metadata exposes lineage-assay counts but not the final explicit dominant lineage identity required for the same-carrier bridge.

The source paper states that lineage barcodes are recovered and linked to 10x cell barcodes through the Feature Barcode pipeline, followed by additional lineage filtering/assignment in `10X1_r1_r2_Analysis_unorm_sctrans.Rmd`.

Do not infer lineage identity from `nCount_lineage` or `nFeature_lineage`.

### Immediate next action
Recover and freeze the exact released cell-to-lineage assignment object/script path or an equivalent reproducible table.

If recovered:
1. freeze cell ↔ lineage ↔ condition mapping;
2. define the first B2 static-RNA-to-modal/state-switching test before outcome values are opened;
3. define B3 held-out/native comparator;
4. execute without opening scalar B1.

If not recoverable:
- record source-carrier refusal;
- preserve Harmange as useful biological/context evidence;
- open Shaffer 2017 as the already-frozen backup B2/B3 source.

No user intervention is required for these mechanical/source steps.
