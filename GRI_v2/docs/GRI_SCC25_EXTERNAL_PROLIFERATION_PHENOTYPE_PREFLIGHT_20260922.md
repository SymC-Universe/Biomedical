# GRI SCC25 external proliferation phenotype preflight

**Date:** 2026-09-22  
**Status:** P0-Q SOURCE QUALIFICATION / QUANTITATIVE OUTCOME REFUSED FOR CURRENT EXECUTION  
**Promotion effect:** NONE  
**Trigger:** reciprocal joint-information post-result audit identified the external phenotype interaction test as the next distinct SCC25 question.

## Candidate outcome

The candidate external outcome is weekly SCC25 cellular proliferation measured during the 11-generation PBS versus 100 nM cetuximab time course from Stein-O'Brien et al., Genome Medicine 10, 37 (2018), DOI 10.1186/s13073-018-0545-2.

The paper states that the same weekly culture harvest supplied:
- RNA,
- DNA methylation,
- proliferation assay material,
- storage material.

Proliferation was measured with the Click-iT Plus EdU flow-cytometry assay. The paper defines cetuximab resistance phenotypically by higher proliferating-cell frequency in the cetuximab generation than in the time-matched PBS generation.

## Provenance result

The authors' public SourceForge repository contains the exact Fig. 1 analysis script:

`CellSurivalDataAnalysis.R`

The script reads the quantitative proliferation values from:

`R01 COMPILED DATA.xlsx`

sheet:

`Flow data analysis`

starting at row 2, and plots:
- `Flow$Clone.generation`,
- `Flow$treatment`,
- `Flow$proliferation`.

The public repository tree exposes the analysis script but does not expose `R01 COMPILED DATA.xlsx` in the current root tree or listed cache tree. The paper and GEO deposits expose the qualitative/time-ordered phenotype interpretation but the GEO omics containers are not the source of the EdU proliferation measurements.

## What is source-licensed now

The following source facts are adequately supported:

- PBS proliferation is described as stable through the longitudinal series.
- CTX proliferation progressively increases.
- CTX is below PBS through G1-G3.
- the paper identifies G4 as the resistance-onset generation.
- later G8-G11 states show sustained/stabilized growth advantage.
- G10 resistance is additionally supported by an anchorage-independent growth assay.

These statements are appropriate for interpretation and phase annotation.

## What is not source-licensed now

The exact weekly numerical EdU proliferation vector is not machine-bound to a public source file in the materials currently located.

Therefore the following is refused for the present interaction test:

`EXACT_WEEKLY_PROLIFERATION_NUMERIC_OUTCOME = NOT_LICENSED`

Digitizing Fig. 1 is not accepted as a substitute for the raw workbook for an outcome-bearing joint-information analysis because it would:
- introduce avoidable measurement error,
- convert plotting geometry into pseudo-raw data,
- obscure replicate/point structure,
- make the outcome less authoritative than the molecular source bindings.

## Why the categorical resistance phase is not substituted

A binary or three-phase label could be reconstructed from the paper text, but it is not an adequate replacement for the intended external-outcome interaction challenge:

- resistance onset is nearly deterministic in week and treatment in this single trajectory;
- the sensitive/early-resistant/late-resistant grouping is also discussed alongside molecular clustering;
- only 20 one-week transitions exist;
- using a phase label would substantially collapse phenotype information and create a different question from the frozen continuous-outcome design.

Therefore no categorical outcome is inserted merely to keep the SCC25 branch moving.

## Disposition

```text
quantitative proliferation provenance = SOURCE_SCRIPT_FOUND
raw quantitative workbook            = NOT_PUBLICLY_BOUND_IN_LOCATED_REPOSITORY
figure digitization                   = REFUSED_FOR_OUTCOME-BEARING_TEST
categorical substitution              = REFUSED_AS_DIFFERENT/WEAKER QUESTION
interaction outcome test              = DEFERRED_SOURCE_GATED
SCC25 result chasing                  = PROHIBITED
```

## Program consequence

The SCC25 joint-meaning branch is now paused at a legitimate source boundary rather than being forced.

Current SCC25 evidence remains:

1. scalar chi is refused under the current R1/A3 representation;
2. methylation-to-RNA incremental prediction weakens materially after explicit time conditioning and remains unresolved/representation-dependent;
3. RNA-to-methylation prediction contains one strong predeclared r=3,m=2 signal but is representation-dependent overall;
4. the independent continuous phenotype interaction test is not authorized until the raw proliferation vector is source-qualified.

Under the cross-domain ordering, the next safe investigation is the predeclared **power-grid transport test**, using the same conditional-information outcome classes against a system with licensed modal damping and explicit network embedding.
