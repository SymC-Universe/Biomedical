# GRI HNSCC short-term cetuximab time-course source audit

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research role:** P0-D temporal / perturbational source qualification  
**Primary GEO series:** `GSE114446`  
**Related single-cell series:** `GSE137524`  
**Publication:** Kagohara et al., *British Journal of Cancer* (2020), DOI `10.1038/s41416-020-0851-5`  
**Chi_bio status:** `NOT_ADMITTED`

## 1. Why this source matters

A targeted source-collision pass uncovered a second cetuximab temporal experiment from the Fertig/Kagohara program that is distinct from the 11-week acquired-resistance series.

`GSE114446` contains daily bulk RNA-seq during the first five days of 100 nM cetuximab exposure and PBS control in HNSCC cell lines. This creates a short-timescale perturbation source that can be contrasted with the chronic 11-week SCC25 source (`GSE98812/GSE98815`).

The combination is unusually useful for the v0.7.4 program because it permits future questions about:

- early response versus chronic adaptation;
- temporal-scale transfer of a frozen state coordinate;
- same-cell-line recurrence across distinct experiments;
- cross-cell-line recurrence versus system specificity;
- whether one fixed transition operator is even adequate;
- whether local regulatory structure reorganizes before stable resistance.

None of those outcomes have been inspected through Chi_bio.

## 2. GSE114446 design

GEO describes the study as a time-course RNA-seq experiment in three HNSCC cell lines treated with 100 nM cetuximab and PBS controls.

Processed gene-level counts are available as:

```text
GSE114446_STCCountsCG.txt.gz
```

GEO reports transcript quantification with Salmon 0.8.2 and gene-level count estimation with tximport 1.2.0 using Gencode v26 annotations, genome build hg19/GRCh37.

### SCC25

The SCC25 bulk series is complete for:

```text
PBS: day 0,1,2,3,4,5
CTX: day 1,2,3,4,5
```

with day-0 PBS available as the common pre-treatment state if that role is prospectively frozen.

### SCC1

The SCC1 bulk series is likewise complete for:

```text
PBS: day 0,1,2,3,4,5
CTX: day 1,2,3,4,5
```

### SCC6 metadata issue

The GEO listing exposes:

```text
PBS: day 0,1,2,3,4,5
CTX: day 2, day 2, day 3, day 4, day 5
```

Two SCC6 CTX samples are labeled day 2 and no CTX day-1 sample is shown in the accession list. This may be a source metadata issue, but it is not corrected by inference here.

**Disposition:** SCC6 is `METADATA_AMBIGUOUS_FOR_ORDERED_DAILY_TRAJECTORY` until the original processed matrix/paper metadata or authors' code resolves the duplicate-day labeling.

## 3. Exact SCC25 accession identity

```text
PBS day 0  GSM3141829
PBS day 1  GSM3141832
PBS day 2  GSM3141830
PBS day 3  GSM3141831
PBS day 4  GSM3141836
PBS day 5  GSM3141833

CTX day 1  GSM3141834
CTX day 2  GSM3141835
CTX day 3  GSM3141838
CTX day 4  GSM3141837
CTX day 5  GSM3141840
```

The non-monotonic GSM ordering is preserved exactly rather than re-sorted by accession number.

## 4. Exact SCC1 accession identity

```text
PBS day 0  GSM3141839
PBS day 1  GSM3141841
PBS day 2  GSM3141842
PBS day 3  GSM3141843
PBS day 4  GSM3141844
PBS day 5  GSM3141846

CTX day 1  GSM3141845
CTX day 2  GSM3141848
CTX day 3  GSM3141847
CTX day 4  GSM3141850
CTX day 5  GSM3141852
```

## 5. Relation to the chronic SCC25 source

The earlier qualified chronic source uses SCC25, 100 nM cetuximab, PBS controls, and weekly RNA/methylation states over 11 weeks.

The short-term source uses the same named SCC25 cell line and same nominal cetuximab concentration but is a distinct experiment with daily bulk RNA sampling during days 0-5.

Therefore it is not an independent laboratory replication, but it is not the same trajectory reused under a new label.

Potential future source roles must distinguish:

```text
short-term perturbation recurrence
same-lab / same-cell-line experiment recurrence
cross-timescale transfer
cross-cell-line recurrence (SCC25 vs SCC1; SCC6 if metadata resolved)
```

from true external P1 confirmation.

## 6. Related single-cell source

`GSE137524` contains cetuximab/PBS single-cell RNA-seq for SCC1, SCC6 and SCC25, each in duplicate after five days of treatment. The publication also reports RNA-velocity analysis based on spliced/unspliced transcriptional structure.

For SCC25 the GEO accessions are:

```text
CTX replicate 1: GSM4080894
CTX replicate 2: GSM4080895
PBS replicate 1: GSM4080900
PBS replicate 2: GSM4080901
```

The single-cell data are not an ordered five-day single-cell trajectory. Their proper roles are instead potential endpoint heterogeneity, state-support, and local carrier/flow diagnostics at day 5.

They must not be described as longitudinal single-cell observations of the same cells.

## 7. New G2 opportunity

For each complete daily bulk cell line, a shared-arm transition design has only five transitions per arm if day 0 is used as the common initial state.

Thus an unconstrained transition operator is even more dimension-limited than the 11-week source.

However, the source has a unique advantage: **same nominal perturbation, finer sampling, and an additional complete cell line (SCC1).**

A future low-dimensional G2 test could therefore ask prospectively:

1. can a control-frozen state representation support a coherent daily transition operator in SCC25?
2. does the same frozen representation/operator family transport to SCC1?
3. does the SCC25 daily coordinate transport to the independent chronic SCC25 experiment after an explicitly tested interval convention?
4. do short-term and chronic dynamics reject a single semigroup interpretation?

The fourth outcome is scientifically useful even if the answer is no.

## 8. New G1 opportunity and limit

The daily bulk series increases temporal resolution for estimating an effective `J` or transition structure, but it does **not** solve the G1 decomposition problem:

```text
J = K - R
```

still does not identify `K` and `R` separately.

Therefore the newly found source strengthens dynamic identifiability but does not license a common transcriptomic restoration rate.

## 9. Proliferation independence

The publication includes proliferation measurements under cetuximab/PBS and reports rapid transcriptional response. Those phenotype measurements are valuable future response axes.

They are not to be used to select the state basis, operator dimension, or unity threshold in a first Chi_bio temporal test.

## 10. Source hierarchy after this audit

```text
GSE98812/GSE98815 chronic SCC25 weekly RNA:       high-priority chronic temporal source
GSE98813 chronic SCC25 weekly methylation:        paired substrate/context source
GSE114446 daily bulk RNA:                         high-priority short-term temporal source
GSE137524 day-5 scRNA duplicate conditions:       heterogeneity / carrier / endpoint source
SCC6 GSE114446 ordered daily trajectory:          metadata-ambiguous pending resolution
```

## 11. Epistemic status

This source discovery expands the temporal test architecture materially, but does not change promotion state.

```text
Chi_bio:                    NOT_ADMITTED
G1 empirical restoration:   STILL UNRESOLVED
G2 temporal testability:    STRENGTHENED
external P1 independence:   NOT SATISFIED
```
