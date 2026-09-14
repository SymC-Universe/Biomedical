# GRI Chi_bio chronic SCC25 provenance reconciliation

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Chi_bio status:** `NOT_ADMITTED`  
**Outcome-bearing analysis performed:** NO

## Finding

The repository's earlier chronic acquisition narrative and source manifest did not match the machine-captured GitHub Actions artifact they cited. This was detected before any state reduction, transition fit, or Chi_bio calculation.

The discrepancy is provenance-level, not a biological result.

## Repeated machine evidence

Two independent executions of the same chronic source probe were inspected:

- workflow run #3, run id `34738887992`;
- workflow run #13, run id `34739241355`.

The normalized `sources` objects from the two artifacts were byte-identical after canonical JSON serialization, with SHA-256:

`fa8772da77054785ff2fb384d336ff6821ed32e65172708a92a975ba1321e70b`

This rules out an intervening public-source drift between those two probe runs as the explanation for the repository mismatch.

## Reconciled public-source identities

| Source | SHA-256 | Structure relevant to source identity |
|---|---|---|
| `GSE98812_GEOExprsData.txt.gz` | `1ce13bae71bd38f619261ec0ca5dcef5dd70b967083cee059e94758aaaf6abb5` | 37 tab-delimited fields; header `GENE` + 36 sample columns; 20,531 data rows |
| `GSE98812_series_matrix.txt.gz` | `f8d826be56083ac6edcaf5d62d046e58908cbef38fdc29d16105fbef0a5441` | 36 sample titles/accessions; value-table header present; 37 fields |
| `GSE98813_series_matrix.txt.gz` | `c5ee581ee6dbb258bb352e86fd1a7aa5ed6f9979550352accaeca8b0d093292e` | 36 sample titles/accessions; value table present; 37 fields |
| `GSE98813_filelist.txt` | `0128c39ced68ee3a2136faa7d2354415eb18af95a2d589a5065a2b4adae49ca9` | 6,234 bytes; 78 lines |

The decompressed RNA expression table is additionally bound as:

- bytes: `5,576,986`;
- SHA-256: `1f718bc27a93d6520cc2966bb8dbe1a87e9e3a29db2021ade6242cad230696f5`.

## Main trajectory is unchanged

The 36-sample source containers include baseline and resistant-clone source roles in addition to the prospectively declared chronic trajectory. The analysis target remains exactly 22 weekly states:

- 11 PBS states;
- 11 cetuximab states;
- weeks 1 through 11;
- baseline and stable resistant-clone samples excluded from the main trajectory.

No sample was added to or removed from that frozen main trajectory as a consequence of this provenance repair.

## Authority rule

For source-byte identity, repeated machine-generated acquisition artifacts outrank stale narrative prose. The reconciled source lock is now:

`config/gri_scc25_chronic_source_provenance_lock_v0_2.json`

Future byte drift must produce an explicit refusal and a new provenance reconciliation. It may not be repaired by silently replacing a hash.

## Scientific consequence

None of the corrected source bindings admits Chi_bio, selects features, chooses an empirical state dimension, fits a transition operator, or tests unity. The repair only restores the chain from public source bytes to the frozen source manifest.

The first outcome-bearing G2/R1 calculation remains blocked behind the explicit empirical design freeze, including rank, transformation/normalization, feature-universe, initialization, adequacy/refusal, uncertainty, and transport rules.
