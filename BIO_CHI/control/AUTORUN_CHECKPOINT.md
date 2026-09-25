# GRI ↔ Bio Chi autonomous continuation checkpoint

**Last updated:** 25 September 2026  
**Branch:** `gri-biochi-bridge-p0q-20260925`  
**Status:** ACTIVE SHAFFER PRE-ANALYSIS FREEZE  
**Authority:** SymC General Operations Manual v0.8.6 + GRI controls + Bio Chi three-object nomenclature.

## Resume here

The Harmange direct same-carrier bridge is closed at the current reproducibility level because the decisive per-lineage identity objects cannot be materialized from the lightweight public processed release without reopening the raw SRA / Feature Barcode pipeline. Preserve that refusal. Do not infer lineage identity from lineage-count metadata.

The active bridge source is Shaffer et al. 2017.

### Completed
- Harmange source schema PASS, exact lineage algorithm recovered, direct carrier materialization refused;
- Shaffer backup opened under pre-frozen rules;
- GSE97679 processed RNA source audit PASS;
- processed RNA file 1: 509,456 rows, SHA-256 `7bb7296f36d32e71e8b63bf7e813351f058e92ab9cda81ec9fd9b67d81f674f3`;
- processed RNA file 2: 636,820 rows, SHA-256 `a1c6180334d037c002b173faf8cdd2162b4d8563cc93e0eb0014cbfe222c4cd8`;
- untreated, week-1, week-4, EGFR-high, and mixed source labels reproduced;
- no gene-effect target statistic opened;
- evidence roles frozen:
  - GSE97679/GSE97680 WM989 = development;
  - GSE97681 WM989 = source-internal validation;
  - GSE97681 WM983B = same-source cross-cell-line transfer;
  - external confirmation = unopened.

### Batch rule
GSE97679 processed RNA is split across sequencing runs. Run identity is a nuisance/blocking factor.

Do not:
- use raw cross-run count distance as biological trajectory;
- choose genes from resistance outcomes to define the primary modal object;
- relabel ATAC as methylation;
- call same-paper transfer external confirmation.

### Immediate next action
Freeze and implement the preanalysis contract:
1. exact common-gene universe;
2. count filtering independent of outcome;
3. normalization and batch handling;
4. unsupervised modal construction;
5. B2 statistic;
6. simple/native comparators;
7. GSE97681 internal-validation endpoint.

Only after those are frozen may target expression values be analyzed.

### Parallel nonblocking review
Harmange's published stochastic two-state model contains `k_on`, `k_off`, growth, and death terms. Review it separately to determine what dynamical object it licenses. Do not infer scalar `chi_bio` unless a qualifying complex mode exists.

No user intervention is required for the current mechanical/preanalysis steps.
