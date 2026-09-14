# GRI Chi_bio G1 restoration source-compatibility audit

**Date:** 2026-09-14  
**Status:** SOURCE FEASIBILITY AUDIT; NO G1 REOPENING YET  
**Program authority:** SymC General Operations Manual v0.8.0  
**Parent plan:** `GRI_CHI_BIO_G1_RESTORATION_IDENTIFIABILITY_PLAN_20260914.md`

## Question

Do the already-qualified SCC25 datasets contain enough kinetic information to reduce the missing G1 restoration assumption without importing an arbitrary common decay constant?

## Result in one sentence

**Yes, partially:** the SCC25 program has raw high-throughput RNA-seq and a separate SCC25 single-cell RNA-velocity channel that can constrain restoration, but the bulk time-course libraries are poly(A)-enriched rather than ideal whole-transcriptome total-RNA designs, so transcript-degradation inference must be treated as a feasibility/identifiability analysis rather than assumed to be directly measurable from the existing bulk matrices.

## 1. Short-term SCC25 bulk time course: GSE114446

NCBI GEO identifies GSE114446 as a 5-day SCC25/SCC1/SCC6 cetuximab-versus-PBS time-course with expression profiling by high-throughput sequencing on Illumina HiSeq 2500. Raw reads are available in SRA under BioProject `PRJNA471358` / SRA study `SRP145751`; processed counts are also available.

The SCC25 samples include PBS day 0 through day 5 and cetuximab day 1 through day 5.

A representative SCC25 GEO sample record (for example GSM3141833) describes the extracted molecule as `polyA RNA` and reports poly(A)-enrichment during library preparation. Therefore this source is genuine RNA-seq with recoverable raw reads, but it is not an ideal whole-transcriptome total-RNA design for methods that depend strongly on premature/intronic RNA abundance.

**Disposition:**

```text
raw_reads_available = YES
condition_matched = YES
bulk_time_course = YES
polyA_enriched = YES
INSPEcT_minus_primary_compatibility = NOT_ASSUMED
intron_signal_feasibility_audit = REQUIRED_BEFORE_USE
```

## 2. Chronic SCC25 time course: GSE98812 / GSE98815

The published chronic cetuximab-resistance experiment collected SCC25 weekly over 11 weeks and generated RNA-seq on Illumina HiSeq with `2 x 100 bp` sequencing. Reads were aligned with MapSplice and quantified with RSEM; the RNA-seq source is GEO `GSE98812`, part of SuperSeries `GSE98815` / BioProject `PRJNA386291`.

The study reports use of the Illumina TruSeq RNA Sample Prep Kit. The TruSeq RNA v2 workflow is an mRNA-focused poly(A)-selection protocol. This makes the chronic source valuable for discrete temporal dynamics but again means precursor/intronic signal cannot be presumed adequate for INSPEcT−-style premature/mature decomposition without checking the actual raw alignments.

**Disposition:**

```text
raw_RNAseq_source = YES
condition_matched = YES
longitudinal_weekly_structure = YES
paired_end_2x100 = YES
polyA_selection_risk = YES
INSPEcT_minus_primary_compatibility = NOT_ASSUMED
intron_signal_feasibility_audit = REQUIRED_BEFORE_USE
```

## 3. SCC25 single-cell kinetic channel

The short-term multi-omics study also generated SCC25 single-cell RNA-seq and reported RNA-velocity analysis. Raw single-cell data are available through the study's GEO/SRA lineage, including SCC25 treatment and control samples.

RNA-velocity methods distinguish unspliced and spliced RNA and, in dynamical formulations, estimate transcription, splicing, and degradation-rate parameters. This provides a **SCC25-specific kinetic constraint** that is more directly related to restoration than static expression alone.

However, it is not a direct transcript-half-life assay and it is not independent of model assumptions. It also represents a different measurement design from the bulk time courses. Therefore it is best used as a cross-representation kinetic constraint/sensitivity rather than as a plug-in genome-wide restoration vector.

Reference basis:

- Kagohara et al. / Fertig group short-term HNSCC study, PMID `32362655`, PMCID `PMC7341752`.
- Bergen et al. scVelo dynamical framework, *Nature Biotechnology* 2020.

**Disposition:**

```text
SCC25_specific = YES
spliced_unspliced_information = AVAILABLE_IN_PRINCIPLE_FROM_RAW_scRNAseq
can_constrain_degradation = YES_WITH_MODEL_DEPENDENCE
fully_independent_restoration_measurement = NO
role = CROSS_REPRESENTATION_KINETIC_CONSTRAINT
```

## 4. Independent transcript-stability evidence

Genome-wide BRIC-seq and related transcript-stability assays provide an independent kinetic scale for mammalian RNA half-lives:

- Imamachi et al., DOI `10.1016/j.ymeth.2013.07.014`, PMID `23872059`;
- Tani et al., PMCID `PMC3337439`.

SCC25-specific historical evidence also exists for E2F1 mRNA half-life and its altered response to growth inhibition:

- Saunders et al., PMID `9563476`.

These data constrain plausibility but do not become SCC25 genome-wide truth by substitution.

## 5. What assumptions can now be closed without new wet-lab data

The following assumptions no longer need to remain vague:

1. **Whether SCC25 temporal RNA-seq exists:** closed. Both short-term and chronic programs are genuine RNA-seq with raw-read lineage.
2. **Whether degradation/restoration is biologically measurable in SCC25:** closed at proof-of-principle level by historical SCC25 transcript-stability work.
3. **Whether a SCC25-specific kinetic representation exists beyond bulk expression:** closed. The short-term study contains a single-cell RNA-velocity channel.
4. **Whether INSPEcT− can be assumed to work directly on the existing bulk matrices:** closed negatively. It cannot be assumed; poly(A) enrichment makes a raw-read intronic/premature-RNA feasibility audit mandatory.
5. **Whether generic mammalian half-lives can be copied into SCC25:** closed negatively. They are bounds/sensitivity references only.

## 6. Remaining computational questions

These require computation rather than further conceptual choice:

- quantify exonic/intronic or premature/mature signal retained in the GSE114446 and GSE98812 raw reads;
- determine whether INSPEcT− input requirements are met sufficiently for a bounded SCC25 kinetic estimate;
- reconstruct or reanalyze SCC25 spliced/unspliced single-cell counts under a frozen RNA-velocity model and quantify degradation-rate uncertainty;
- compute admissible continuous-time generator families from the frozen G2 operators, including matrix-log branch/refusal handling;
- propagate kinetic/restoration uncertainty through normalized G1 and test invariance.

No threshold, solver setting, branch selection, or restoration prior should be chosen based on distance to unity or downstream cancer behavior.

## 7. Current scientific state

```text
G1_restoration_problem = NARROWED
matched_restoration_direct_measurement = STILL_ABSENT
matched_bulk_kinetic_inference = FEASIBILITY_TESTABLE
matched_single_cell_kinetic_constraint = AVAILABLE_IN_PRINCIPLE
independent_genomewide_half_life_evidence = AVAILABLE_AS_BOUNDS_ONLY
G1_normalized_empirical_status = NOT_YET_REOPENED
```

The remaining uncertainty is now a finite computational/identifiability problem rather than an unspecified missing-data assumption.
