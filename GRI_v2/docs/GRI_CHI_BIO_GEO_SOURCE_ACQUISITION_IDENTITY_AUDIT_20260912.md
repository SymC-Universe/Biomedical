# GRI Chi_bio public GEO source acquisition and identity audit

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D source acquisition / provenance / identity validation  
**Chi_bio outcomes computed:** NO  
**Feature selection performed:** NO

## 1. Execution identity

GitHub Actions workflow `GRI Chi_bio GEO source probe` run **#7** (`34738639210`) successfully downloaded the frozen public GEO supplementary files and executed the cross-file identity validator after a purely mechanical repair for capitalization-only gene-symbol differences.

The repaired validator preserves both source strings and only accepts row-wise casefold identity for that specific expression/feature comparison. Any difference beyond capitalization remains a hard failure.

Final validation status:

```text
PASS_ALL_SOURCE_IDENTITY_RELATIONS
```

Uploaded provenance artifact:

```text
name:   gri-chi-bio-geo-source-probe
ID:     10311861962
SHA256: cc6f0ad8529ced4310e52dc7c202711b9a05b99793b2873299f8cfd759ea2a01
files:  GRI_CHI_BIO_GEO_SOURCE_PROBE.json
        GRI_CHI_BIO_GEO_SOURCE_IDENTITY_VALIDATION.json
```

The downloaded molecular matrices themselves were deliberately not uploaded as a repository artifact. Only the provenance/identity reports were preserved.

## 2. GSE114446 short-term bulk RNA

Verified public processed file:

```text
GSE114446_STCCountsCG.txt.gz
SHA256: c1318f5ad3b62d26c043de370cdca7300548337918f4543b13769bbe7a08a6c2
compressed bytes:   3,802,045
uncompressed bytes: 9,620,387
gene rows:          56,470
fields:             34 = gene + 33 sample columns
```

The source file uses opaque sequencing-library IDs rather than biological labels in its header. The frozen 33-column GEO title/accession mapping matched the processed matrix **exactly as a set**.

No column was inferred from expression values or candidate outcomes.

Current ordered-trajectory disposition remains:

```text
SCC25: complete PBS day 0-5 + CTX day 1-5
SCC1:  complete PBS day 0-5 + CTX day 1-5
SCC6:  source metadata ambiguous: duplicate CTX day 2, no CTX day 1
```

The SCC6 ambiguity remains preserved. No correction has been manufactured.

## 3. GSE135604 day-5 ATAC substrate/context panel

Verified public processed file:

```text
GSE135604_ATACpeakset.csv.gz
SHA256: 00bc414c58ad9ca999614669c81ec9081c0b9b058e00ad1194b88ce15d30e29c
compressed bytes:   10,196,690
uncompressed bytes: 38,049,117
peak rows:          115,087
fields:             23 = 6 coordinate fields + 17 processed sample columns
```

The 17 processed sample columns matched the frozen source manifest exactly after excluding the source-declared failed processed replicate `SCC1PBS2` / `GSM4021917`.

Verified processed panel:

```text
SCC1CTX1 SCC1CTX2 SCC1CTX3 SCC1PBS1 SCC1PBS3
SCC6CTX1 SCC6CTX2 SCC6CTX3 SCC6PBS1 SCC6PBS2 SCC6PBS3
SCC25CTX1 SCC25CTX2 SCC25CTX3 SCC25PBS1 SCC25PBS2 SCC25PBS3
```

`SCC1PBS2` is absent from the processed peakset as expected.

ATAC remains frozen as a **substrate/context endpoint**, not part of the S1 transcriptomic state vector.

## 4. GSE137524 SCC25 day-5 single-cell RNA

### Expression matrix

```text
GSE137524_exprsSCC25Matrix.csv.gz
SHA256: 58a4f9eb2289eb14f4d33974a62c3e3a762631b28c3fad6bbd4bdb192e8f4057
compressed bytes:   44,654,039
uncompressed bytes: 605,731,285
gene rows:          33,538
cell columns:        8,920
```

### Phenotype table

```text
GSE137524_phenoDataSCC25.csv.gz
SHA256: 9162650519a9e4c22d7bf7fe208e041a40c7608e3b994fee5843af18aaace943
rows: 8,920
```

Verified cell counts:

```text
CTX R1: 1,999
CTX R2: 2,027
PBS R1: 2,318
PBS R2: 2,576
total:  8,920
```

The expression-matrix cell IDs and phenotype row IDs are an **exact order match**.

### Feature table

```text
GSE137524_featureData.csv.gz
SHA256: 4b7fb2e96fe11b0c1bc856fdec87dcb10eb264ee2aa18d2802813731e861ac41
rows: 33,538
```

The expression gene sequence and `featureData.gene_short_name` sequence match row-for-row after casefolding. There are **404 capitalization-only differences**, principally legacy `C#orf` versus `C#ORF` style symbols.

Disposition:

```text
CASE_ONLY_ORDER_MATCH
source strings rewritten: NO
non-case identity mismatch: NONE OBSERVED
```

This distinction is preserved in the manifest and validator rather than silently normalizing gene names.

## 5. Source-identity findings that changed the workstate

The acquisition pass closed several previously mechanical uncertainties:

1. the 33 opaque bulk-RNA matrix columns now have exact frozen biological identities;
2. the ATAC processed panel is exactly known and the source-QC exclusion is confirmed in the processed header;
3. the SCC25 scRNA expression/pheno identity is exact at the cell level;
4. the SCC25 scRNA expression/feature identity is exact in row order apart from explicitly recorded capitalization only;
5. public source files are now hash-bound for reproducibility.

None of these results defines a Chi_bio coordinate.

## 6. Remaining source gates

The following remain open before any real candidate trajectory:

- freeze exact bulk-RNA state reduction and dimension rule;
- freeze count transformation/normalization for the temporal state;
- freeze low-count/feature-universe rule independently of Chi outcomes;
- freeze transition architecture and residual/refusal criteria;
- freeze ATAC feature aggregation and cross-modal statistic;
- freeze scRNA carrier/projection rule;
- preserve proliferation as an unopened response axis until construction is complete;
- acquire/hash chronic GSE98812/GSE98813 files under the same source gate if used in the cross-timescale analysis.

## 7. Epistemic disposition

```text
public-source acquisition:        PASS for current short-term RNA / day-5 ATAC / SCC25 scRNA files
cross-file identity:              PASS
source provenance:                HASH-BOUND
feature selection:                NOT PERFORMED
state reduction:                  NOT FROZEN
candidate Chi_bio computation:    NOT PERFORMED
biological unity boundary:        NOT_ADMITTED
```
