# GRI Chi_bio SCC25 restoration / RNA-turnover source audit addendum

**Date:** 2026-09-13  
**Mode:** P0-D literature-collision extension before empirical G1 qualification  
**Candidate family:** G1-S1-L3  
**Chi_bio:** `NOT_ADMITTED`

## Purpose

The 2026-09-12 restoration-source audit found SCC25 gene-specific mRNA-stability experiments but no transcriptome-wide SCC25 decay resource adequate to identify the restoration operator required by the G1 normalization. This addendum broadens the targeted collision specifically across genome-wide RNA-turnover technologies and SCC25 search terms before treating that absence as a practical design constraint.

## Search families checked

The expanded pass explicitly combined `SCC25` with:

- 4-thiouridine / 4sU metabolic labeling;
- SLAM-seq;
- TimeLapse-seq;
- TUC-seq;
- BRIC-seq / BrU chase;
- transcriptome-wide RNA decay / half-life / stability;
- RNA turnover / degradation-rate sequencing.

The pass also checked methodological genome-wide turnover papers to verify what evidence would actually be sufficient if an SCC25 dataset were found.

## Result

No transcriptome-wide SCC25 RNA-turnover dataset was located in this expanded targeted pass.

The result remains deliberately scoped:

```text
NO TRANSCRIPTOME-WIDE SCC25 RESTORATION SOURCE LOCATED IN TWO TARGETED PASSES
```

This is not an existence proof that no such source is present anywhere.

## SCC25 evidence that was recovered again

The search recovered multiple SCC25 or SCC25-family studies using actinomycin-D/qPCR-style stability assays on particular transcripts, including examples involving c-MYC, FGFR3, PKM2, ACSL3/GPX4 and PD-L1-related systems. These reinforce two points already in the primary audit:

1. RNA restoration/decay is experimentally measurable in SCC25-family cells.
2. The available evidence is gene-specific and itself demonstrates transcript/context heterogeneity rather than licensing a universal transcriptomic restoration constant.

Examples include:

- METTL3/YTHDF1 and c-MYC stability in SCC25/CAL27, PMCID `PMC7057159`;
- METTL3 and FGFR3 stability in SCC25/SCC9, PMCID `PMC9516809`;
- FTO and ACSL3/GPX4 stability in SCC25/SCC1, PMCID `PMC10671523`;
- FTO/YTHDF2 and PKM2 stability in SCC25/CAL27, PMCID `PMC12542365`;
- FTO/PD-L1 stability in SCC25-derived arecoline-exposed cells, PMCID `PMC9459271`.

## Genome-wide turnover methods confirmed as suitable evidence classes

The literature collision confirmed that transcriptome-scale restoration could in principle be measured rather than inferred from static expression.

- BRIC-seq was developed specifically for genome-wide RNA-stability measurement from chronological loss of BrU-labeled RNA. Imamachi et al., *Methods* 2014, PMID `23872059`, DOI `10.1016/j.ymeth.2013.07.014`.
- A systematic comparison of 4sU enrichment, SLAM-seq, TimeLapse-seq and TUC-seq estimated decay rates with uncertainty for more than 11,600 human genes, PMID `34228787`.
- Dyrec-seq combines metabolic-labeling approaches to measure RNA synthesis and degradation genome-wide, but its demonstrated human system was HeLa rather than SCC25.

Thus the G1 restoration problem is not technologically impossible; the missing item is a qualified measurement in the relevant SCC25/state/context or a defensible transfer model.

## Consequence for the approved G1 route

The second targeted pass strengthens the existing pre-outcome disposition without changing the candidate family:

```text
full/transcriptome-scale SCC25 G1A common-beta route:  NOT LICENSED
full/general directed SCC25 G1B route:                 NOT LICENSED
reduced-state effective restoration hypothesis:       STILL TESTABLE
G2 temporal comparator:                               REMAINS PRIORITY
```

A future reduced regulon/module state may have an effective restoration scale that is more coherent than gene-wise turnover. That possibility must be tested prospectively. It cannot be inferred from the absence of full-transcriptome decay data or from the desire to preserve a unity coordinate.

## Next efficient experimental opportunity if public evidence remains absent

If literature/source discovery is exhausted, the efficient experiment is not automatically a whole-transcriptome decay atlas. The protocol-compatible design is:

1. freeze the low-dimensional regulatory state independently;
2. perturb the system under a controlled condition;
3. measure state relaxation at enough timepoints to identify state-specific restoration or reject a common-restoration approximation;
4. estimate uncertainty before calculating any normalized G1 coordinate;
5. retain G2 as a decomposition-free comparator on the same perturbational series.

This experiment remains a future opportunity, not an authorized requirement.

## Current stop

No additional public-source evidence from this pass licenses a numerical SCC25 G1 normalization. The unresolved scientific burden has now been narrowed to the **reduced-state representation and its restoration model**, not a generic search for more static RNA data.