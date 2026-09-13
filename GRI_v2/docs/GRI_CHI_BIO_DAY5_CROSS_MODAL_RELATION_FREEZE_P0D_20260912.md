# GRI Chi_bio day-5 RNA / scRNA / ATAC relational test freeze

**Date:** 2026-09-12  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome relational-test freeze  
**Bulk RNA source:** `GSE114446`  
**Single-cell RNA source:** `GSE137524`  
**ATAC source:** `GSE135604`  
**Chi_bio outcomes opened:** NO  
**Chi_bio status:** `NOT_ADMITTED`

## 1. Purpose

The short-term cetuximab program provides three complementary day-5 views:

```text
bulk RNA:   transcriptomic state trajectory endpoint
scRNA:      cell-level heterogeneity / carrier support endpoint
ATAC:       chromatin accessibility substrate/context endpoint
```

The v0.7.4 relational-stability rules make this more useful than collapsing all modalities into one vector. The test is therefore frozen as a relationship among independently represented layers.

## 2. Pairing ceiling

The three GEO series are aligned by experimental program, cell-line identity, treatment condition, and approximately the same five-day exposure design. They are **not declared to be one-to-one sample-paired biological replicates** unless direct source provenance demonstrates that identity.

Frozen rule:

```text
condition/cell-line alignment != sample-pair identity
```

No paired-sample statistic is licensed merely because SCC25/PBS/CTX labels match across series.

## 3. Frozen architecture

### State layer

The approved S1 state remains transcriptomic. A future bulk-RNA reduction must be frozen without ATAC, scRNA, proliferation, or Chi_bio outcomes choosing its basis/dimension.

### Carrier / heterogeneity layer

Day-5 scRNA may test whether a bulk-defined transcriptomic direction or module is broadly supported across cells, restricted to a subpopulation, or not transportable to single-cell representation.

It may not be used to retroactively choose the bulk basis and then counted as independent confirmation.

### Substrate/context layer

ATAC accessibility may test whether a frozen transcriptomic state/operator reorganization is accompanied by substrate/context reorganization.

It remains external to the transcriptomic state under the current approved plan.

## 4. Frozen questions

### XM1: transcriptomic representation transport to single cells

After the bulk RNA state reduction is frozen, does the corresponding fixed gene/module representation remain observable in the day-5 SCC25 single-cell data?

Allowed dispositions:

```text
BROADLY_OBSERVABLE
SUBPOPULATION_RESTRICTED
REPRESENTATION_DEPENDENT_NO_TRANSFER
NOT_IDENTIFIABLE
```

No preferred answer is specified.

### XM2: RNA-state change versus ATAC substrate reorganization

After both an RNA summary and an ATAC summary are independently frozen, does cetuximab induce a reproducible relationship between the two across the available cell lines/conditions?

Allowed dispositions:

```text
COHERENT_RELATIONAL_REORGANIZATION
RNA_CHANGE_WITH_WEAK_OR_NO_ATAC_RELATION
ATAC_CHANGE_WITH_WEAK_OR_NO_RNA_RELATION
CELL_LINE_SPECIFIC_RELATION
NOT_IDENTIFIABLE
```

The relation does not establish causal direction.

### XM3: local versus embedded preservation

Does the candidate RNA operator/state retain its qualitative organization when interpreted alongside cell-level heterogeneity and chromatin context, or does embedding expose a representation failure?

Allowed dispositions:

```text
LOCAL_RELATION_PRESERVED_UNDER_EMBEDDING
EMBEDDING_REORGANIZES_REALIZED_STATE
LOCAL_OBJECT_NOT_IDENTIFIABLE
NO_COHERENT_CROSS_MODAL_RELATION
```

## 5. Cross-modal independence rules

The following are prohibited:

- using ATAC to choose RNA dimensions and then calling ATAC agreement validation;
- using scRNA treatment separation to choose bulk RNA dimensions and then calling scRNA transport confirmation;
- choosing ATAC peaks because they correlate with the candidate scalar and then treating that correlation as substrate evidence;
- using proliferation response to tune any cross-modal statistic;
- choosing signs/orientations merely to make modalities agree;
- dropping a cell line because it weakens cross-modal agreement after outcomes are opened.

## 6. Source-specific QC and imbalance

The modalities have different replication structures:

- daily bulk RNA has one ordered bulk state per cell line/condition/day in the accession architecture;
- day-5 scRNA has duplicate libraries per cell line/condition;
- ATAC nominally has triplicate libraries per cell line/condition, with at least one explicit processed-QC failure (`GSM4021917`, SCC1 PBS replicate 2).

Therefore a future cross-modal uncertainty model must not pretend equal replication or sample pairing.

## 7. Cross-cell-line role

SCC25 is the primary continuity bridge because it also has the chronic 11-week multiomic series. SCC1 provides a second complete short-term system. SCC6 remains usable for day-5 ATAC/scRNA roles, but its bulk daily ordered trajectory has a GEO day-label ambiguity that must be resolved before longitudinal use.

No cell line is promoted or excluded on the basis of future Chi_bio agreement.

## 8. Scalar / modal / conglomerate reporting rule

A future day-5 analysis must report at least:

```text
scalar candidate coordinate or refusal
modal/vector carrier information
state-representation diagnostics
ATAC substrate/context result
single-cell carrier/heterogeneity result
cross-modal relationship with uncertainty
```

A scalar match cannot erase a modal or substrate mismatch.

## 9. Causal ceiling

Even a strong aligned RNA/ATAC/scRNA result would support a reproducible relational architecture under the tested perturbation. It would not by itself prove:

- chromatin causes the RNA operator change;
- RNA causes the chromatin change;
- a universal substrate-inheritance law;
- patient-level transport;
- a biological `Chi_bio = 1` boundary.

## 10. Execution gate

This relational test remains frozen but unopened until:

1. exact source files are acquired and hashed;
2. the bulk RNA state reduction is scientifically frozen;
3. the ATAC feature/summary rule is frozen independently;
4. the scRNA projection/carrier rule is frozen independently;
5. missingness/QC and cross-source batch rules are frozen;
6. only then are cross-modal outcomes computed.

Current result: **test architecture frozen; no outcome inspected.**
