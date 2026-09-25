# Shaffer 2017 GRI ↔ Bio Chi source checkpoint

**Date:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Status:** BACKUP OPEN / SOURCE-SCHEMA QUALIFICATION

Harmange has been refused as the first direct same-carrier bridge at the current reproducibility level because the required explicit lineage identity objects cannot be materialized from the accessible processed release without reopening the raw sequencing pipeline.

The pre-frozen backup, Shaffer et al. 2017, is now active.

## Why this source

The same WM989 melanoma system has:
- source-defined untreated, 1-week, and 4-week vemurafenib RNA states;
- biological replicates;
- matched ATAC-seq time-course structure;
- public processed RNA count tables;
- a direct cancer-resistance phenotype lineage in the published experiment.

Selection is based on source structure, not target molecular results.

## Frozen interpretation

- RNA may instantiate a GRI-compatible regulatory-organization layer.
- ATAC is chromatin-accessibility context and is not methylation.
- no `chi_bio` scalar is authorized from timepoint ordering alone;
- B2/B3 may open only after exact source/sample mapping is frozen;
- no outcome-selected genes or thresholds are allowed.

## Immediate next action

Download the two processed GSE97679 RNA tables, hash them, inspect schema/sample identifiers only, and freeze the exact timepoint/population/replicate carrier before any modal or resistance-target calculation.
