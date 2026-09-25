# Harmange exact lineage-mapping freeze

**Date:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Status:** FROZEN BEFORE LINEAGE RECONSTRUCTION

The exact authors' experiment-3 analysis script has been recovered from the paper's public Drive and hash-pinned.

## What is frozen

The source-native lineage assignment is reconstructed from the lineage Feature Barcode assay only:

1. keep cells with 1-19 detected lineage features;
2. keep lineage features with raw total count >1;
3. threshold lineage counts at >=3 reads;
4. reject lineage features spanning both source well groups;
5. reject lineages >273 cells;
6. apply the source multi-barcode combination collapse rule;
7. retain cells with exactly one surviving barcode;
8. retain lineages with 3-273 cells;
9. reapply the single-barcode cell gate;
10. use the retained source feature identity as lineage ID.

No primed-state fraction, drug-response outcome, B2 statistic, or B3 statistic is opened at this stage.

## Source-native reproduction checks

The paper reports:
- 40,021 cells in experiment 3;
- 19,740 lineages, each with at least 3 cells;
- approximately 49% of lineages represented in all four treatment conditions.

These are frozen as reproduction checks, not tuning targets. If the reconstruction does not match closely enough to establish source fidelity, the discrepancy is investigated rather than thresholds changed.

## Next

Inspect the GEO feature schema to identify the exact lineage-feature rows, then execute the frozen carrier reconstruction.
