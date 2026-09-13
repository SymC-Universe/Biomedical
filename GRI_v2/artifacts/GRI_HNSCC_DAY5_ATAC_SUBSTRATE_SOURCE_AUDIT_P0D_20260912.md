# GRI HNSCC day-5 ATAC substrate/context source audit

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research role:** P0-D substrate/context / perturbational source qualification  
**GEO series:** `GSE135604`  
**Publication:** Kagohara et al., *British Journal of Cancer* (2020), DOI `10.1038/s41416-020-0851-5`  
**Chi_bio status:** `NOT_ADMITTED`  
**Chi_bio outcomes on this source:** `UNOPENED`

## 1. Why this source is important under the approved G1/S1/L3 plan

The approved S1 state is transcriptomic. Methylation and other epigenetic structure are therefore retained as substrate/context rather than naively concatenated into the RNA state.

`GSE135604` provides a second substrate/context modality: chromatin accessibility measured by ATAC-seq after five days of cetuximab or PBS treatment in the same HNSCC experimental program that generated the short-term bulk and single-cell RNA sources.

This is valuable because it can later test whether a frozen transcriptomic operator/state change is accompanied by a separately measured reorganization of accessible chromatin without treating accessibility as the transcriptomic state itself.

## 2. Source identity

GEO identifies:

```text
series = GSE135604
organism = Homo sapiens
experiment type = genome binding/occupancy profiling by high-throughput sequencing
platform = GPL11154, Illumina HiSeq 2000
cell lines = SCC1, SCC6, SCC25
treatment = 100 nM cetuximab versus PBS
exposure = daily treatment for 5 days
design = 3 cell lines x 2 conditions x 3 nominal replicates = 18 ATAC libraries
```

Processed resources on the series record include:

```text
GSE135604_ATACpeakset.csv.gz
GSE135604_RAW.tar
```

The series record reports global transcriptional and epigenetic changes during the first five days of cetuximab exposure. That published interpretation is retained as source context, not as a Chi_bio result.

## 3. Exact accession manifest

### SCC1

```text
CTX replicate 1  GSM4021913
CTX replicate 2  GSM4021914
CTX replicate 3  GSM4021915
PBS replicate 1  GSM4021916
PBS replicate 2  GSM4021917
PBS replicate 3  GSM4021918
```

### SCC6

```text
CTX replicate 1  GSM4021919
CTX replicate 2  GSM4021920
CTX replicate 3  GSM4021921
PBS replicate 1  GSM4021922
PBS replicate 2  GSM4021923
PBS replicate 3  GSM4021924
```

### SCC25

```text
CTX replicate 1  GSM4021925
CTX replicate 2  GSM4021926
CTX replicate 3  GSM4021927
PBS replicate 1  GSM4021928
PBS replicate 2  GSM4021929
PBS replicate 3  GSM4021930
```

## 4. QC exception that must remain visible

GEO explicitly reports that **SCC1 PBS replicate 2 (`GSM4021917`) did not yield good-quality processed sequencing and has no processed peak file supplied on the sample record.**

This means the nominal 3x2x3 experimental design cannot automatically be treated as an 18-sample processed-peak panel.

Frozen rule:

```text
nominal library exists != processed peak profile is usable
```

No replicate may be silently dropped only after a candidate result is inspected. Source-level QC eligibility must be established before any cross-modal Chi_bio relation is computed.

## 5. SCC25-specific compatibility

For the highest-priority SCC25 source, all six ATAC accession roles are explicit on GEO:

```text
3 CTX + 3 PBS at day 5
```

This aligns naturally with:

- SCC25 short-term bulk RNA in `GSE114446` over days 0-5;
- SCC25 day-5 single-cell RNA in `GSE137524`;
- chronic SCC25 weekly RNA/methylation in `GSE98812/GSE98813/GSE98815`.

The ATAC data are not a daily ATAC trajectory. They are a replicated day-5 substrate/context endpoint.

## 6. Frozen role in the GRI architecture

Under the approved plan:

```text
transcriptomic regulatory state x
        |
        +--> candidate regulatory generator/operator

ATAC accessibility a
        |
        +--> independently measured substrate/context organization
```

The future question is relational:

> Does the transcriptomic state/operator reorganization under cetuximab co-occur with a reproducible change in substrate accessibility, and does that relation transport across cell lines or temporal regimes?

This is not equivalent to defining a state vector `[RNA, ATAC]` by concatenation.

## 7. Anti-leakage rules

The ATAC source may not be used to:

- choose an RNA state dimension because it maximizes ATAC agreement;
- choose a G1/G2 formula because it yields a desired ATAC association;
- manufacture a unity crossing;
- select only accessibility regions that agree with a favored RNA trajectory and then claim independent substrate support;
- use the same cross-modal association both to define and validate the coordinate.

A future ATAC relation test must freeze region/feature aggregation, state/operator estimate, and cross-modal statistic before the relevant result is opened.

## 8. Candidate substrate summaries that remain available for future freeze

Without choosing among them here, legitimate outcome-independent ATAC summaries could include:

- global accessible-region geometry;
- fixed promoter accessibility over an externally defined promoter set;
- fixed regulatory-element modules defined from an external atlas;
- cell-line-specific accessibility change after a predeclared QC/filter rule;
- projection of fixed transcriptomic-regulon targets into accessibility space;
- low-dimensional ATAC representation trained independently of Chi_bio outcome.

The exact summary remains scientifically open.

## 9. Local-versus-embedded interpretation

ATAC accessibility can inform the substrate in which a local transcriptomic regulatory map is realized. It does not by itself prove that chromatin change causes the RNA transition or that the same regulatory generator is preserved after embedding.

Future outputs must therefore keep separate:

```text
RNA operator/state estimate
ATAC substrate/context estimate
cross-modal relationship
uncertainty / identifiability
```

## 10. Current disposition

```text
GSE135604 identity:             SOURCE-QUALIFIED P0-D
SCC25 nominal ATAC panel:       3 CTX + 3 PBS
SCC1 nominal ATAC panel:        3 CTX + 3 PBS, with GSM4021917 processed-QC failure
SCC6 nominal ATAC panel:        3 CTX + 3 PBS
role:                           DAY5 SUBSTRATE/CONTEXT ENDPOINT
longitudinal ATAC claim:        NOT LICENSED
RNA+ATAC concatenated state:    PROHIBITED BY CURRENT S1 PLAN
Chi_bio outcome:                NOT COMPUTED
P1 status:                      NOT EXTERNAL P1
```

This source materially strengthens the local-versus-embedded and substrate-inheritance test architecture without changing the Chi_bio promotion state.
