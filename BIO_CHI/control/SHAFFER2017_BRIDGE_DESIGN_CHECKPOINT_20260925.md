# Shaffer 2017 bridge design freeze

**Date:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Status:** SOURCE PASS / PRE-ANALYSIS DESIGN FROZEN

## Source gate

The GSE97679 processed RNA source passed the automated schema/timepoint audit.

No gene-effect statistic was used for admission.

## Evidence roles

### Development
WM989 GSE97679 RNA plus GSE97680 ATAC.

Purpose: define the GRI-compatible RNA regulatory architecture and modal response to vemurafenib.

### Source-internal validation
WM989 GSE97681 subclone, drug, and drug-holiday trajectories.

This is a distinct experiment but the same publication/source lineage. It is internal validation, not independent external confirmation.

### Same-source cross-cell-line transfer
WM983B records in GSE97681.

These may test transport after the WM989 definitions are frozen, but remain same-source evidence.

### External confirmation
Unopened.

## Batch firewall

The two GSE97679 processed RNA tables come from separate sequencing runs and do not contain a complete identical time series within each run.

Therefore:
- sequencing run is a blocking/nuisance factor;
- cross-run raw-count distance is forbidden as a biological trajectory measure;
- the primary modal construction must use a frozen common-gene universe and batch-aware normalization/contrast;
- development decisions cannot use resistance outcomes.

## Next

Freeze preprocessing, common-gene universe, unsupervised modal construction, and native/simple comparator before opening B2 molecular results.
