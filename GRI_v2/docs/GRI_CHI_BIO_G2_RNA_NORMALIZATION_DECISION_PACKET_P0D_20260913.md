# GRI Chi_bio G2 RNA-normalization decision packet

**Date:** 2026-09-13  
**Protocol authority:** General Cross-Project Research Protocol Final v0.7.4  
**Research mode:** P0-D pre-outcome preprocessing qualification  
**Source:** GSE114446 short-term HNSCC bulk RNA-seq  
**Approved rank architecture:** A3 (`r=2` and `r=3`, no rank winner)  
**Chi_bio:** `NOT_ADMITTED`  
**Real G2 trajectory inspected:** NO

## 1. Source fact that controls this decision

The frozen GSE114446 source exposes a processed gene-level count table generated after Salmon transcript quantification and tximport gene-level summarization. The original study used DESeq2 for differential-expression analysis.

The public processed table is therefore **count-scale input**, not a pre-normalized Euclidean state suitable for direct PCA.

The current source record does not preserve the full original `tximport` object with transcript-length/abundance matrices and does not establish from the table alone that the exported counts are `scaledTPM` or `lengthScaledTPM` rather than the original estimated counts.

Consequently, the first G2 state cannot simply call the supplied count columns "expression coordinates" without a prospectively frozen transformation.

## 2. Prior-art constraint

Current Bioconductor guidance distinguishes:

- original tximport estimated counts plus effective-length offsets;
- counts generated from abundance (`scaledTPM` or `lengthScaledTPM`) that can be used without that offset;
- variance-stabilizing/log-scale transformations for sample geometry, clustering or other downstream multivariate analysis.

The DESeq2 variance-stabilizing transformation is explicitly designed to reduce mean-dependent variance and can be frozen/reapplied to new samples. However, a faithful DESeq2/tximport route normally benefits from the original tximport object or a clearly specified count construction.

This matters here because our target is a state geometry, not differential-expression p-values.

## 3. Candidate N1: deterministic per-sample library-size normalization + log transform

Example class:

```text
CPM_i,g = 1e6 * count_i,g / sum_g count_i,g
z_i,g = log2(CPM_i,g + epsilon)
```

with a fixed pseudocount and feature rule frozen before treated-state projection.

### Strengths

- transparent and reproducible from the public processed table alone;
- accepts fractional estimated counts;
- each sample's basic scaling is defined without treatment labels or phenotype;
- easy to transport identically into daily and weekly sources if their inputs are comparable;
- no additional R/Bioconductor runtime required.

### Weaknesses

- simple library-size scaling is sensitive to composition shifts;
- shifted logarithms retain more mean-dependent variance than a dedicated VST, especially for low counts;
- the pseudocount becomes part of the coordinate definition.

### Role

Strong **minimal primary candidate** if provenance simplicity and exact reproducibility from the frozen processed source are prioritized.

## 4. Candidate N2: TMM-style normalization + log-CPM

### Strengths

- established RNA-seq composition normalization;
- more robust than raw library-size scaling when a subset of highly expressed features distorts library composition;
- log-CPM is suitable for continuous multivariate geometry.

### Weaknesses

- normalization factors depend on the sample ensemble/reference rule;
- if the full treated trajectory helps determine normalization factors or the reference, representation independence is weakened;
- TMM assumptions can be stressed by broad global shifts;
- requires a prospectively frozen reference/fitting role.

### Cleanest admissible form

If used, the normalization reference/factors should be constructed under an explicitly frozen control/reference rule rather than silently fitting a transformation to all treated and control states.

## 5. Candidate N3: DESeq2 variance-stabilizing transformation

### Strengths

- specifically addresses RNA-seq mean-variance dependence;
- standard sample-geometry use case;
- official DESeq2 documentation supports freezing a transformation and applying it to new samples;
- asymptotically approaches log2 behavior at high counts.

### Weaknesses for the current public table

- the available table is a processed tximport-derived count matrix, not the preserved original tximport object;
- full tximport effective-length offsets are not available in the frozen public table;
- estimated counts may be fractional whereas the most direct DESeq2 matrix constructor expects count semantics suited to its negative-binomial model;
- using all treatment samples to fit the dispersion transformation would weaken the control-only representation firewall;
- fitting a stable dispersion trend from only six PBS states is possible across many genes but needs an explicit qualification test rather than being assumed.

### Role

Strong **methodological sensitivity or primary candidate only after exact input compatibility is established**.

## 6. Candidate N4: reconstruct the RNA source from raw sequencing

Reprocess the 11 SCC25 bulk samples from SRA with a frozen Salmon + tximport pipeline and preserve the full tximport object.

### Strengths

- resolves ambiguity about count construction and effective transcript lengths;
- permits a fully specified modern import/offset pipeline;
- creates a stronger future cross-source provenance chain.

### Weaknesses

- much larger compute/download burden than using the frozen 3.6 MB processed table;
- introduces a new quantification pipeline/version distinct from the original Salmon 0.8.2 / tximport 1.2.0 analysis unless historical software is reconstructed;
- a new reprocessing pipeline creates additional technical degrees of freedom without necessarily improving the first low-dimensional feasibility test;
- protocol run economy argues against this unless the processed table proves inadequate.

### Role

**Escalation path**, not the default first move.

## 7. Current pre-outcome recommendation

The cleanest first comparison is:

```text
primary candidate for review: N1 transparent fixed log-CPM-like transform
method sensitivity:           N3 frozen VST if input compatibility can be qualified
escalation only if needed:    N4 raw reprocessing
```

N2 remains a defensible alternative if a control/reference-only TMM rule can be frozen cleanly.

This recommendation is based on provenance and leakage control, not on which transformation produces a desired G2 trajectory.

## 8. Feature filtering must be separated from normalization

A normalization method must not silently decide the gene universe.

The feature universe requires its own prospective rule. Candidate classes include:

- externally fixed annotation universe;
- control-only detectability/abundance floor;
- intersection of independently fixed SCC25 and chronic-source gene identifiers;
- a predeclared high-information rule derived only from PBS controls.

Treatment differential expression, proliferation association, candidate spectral radius and unity distance are forbidden feature-selection signals.

## 9. Computational implication

N1-N3 are tiny computational tasks at this source scale. The public file is only a few megabytes and contains approximately 56k genes across 33 columns, of which only 11 SCC25 states enter this first design.

N4 is qualitatively different: raw FASTQ acquisition, reference indexing/quantification and tximport reconstruction would turn a seconds/minutes preprocessing step into an hours-scale, tens-of-gigabytes workflow. It should be earned by a concrete provenance need rather than performed by reflex.

## 10. Exact remaining freeze items

Before real SCC25 G2 execution, the preprocessing record still needs:

```text
normalization class
pseudocount / transform parameters if relevant
normalization fitting/reference role
feature-universe rule
gene-identifier/version rule
missing/zero handling
cross-source transport rule
```

No option is selected by this packet.
