# 6. G1 restoration identifiability: closing the remaining normalization assumption

**Section status:** ACTIVE WORKING SECTION  
**Last evidence reconciliation:** 2026-09-14  
**Source audit:** `GRI_v2/docs/GRI_CHI_BIO_G1_RESTORATION_SOURCE_COMPATIBILITY_AUDIT_20260914.md`

## 6.1 Why restoration matters

The theoretical G1 route separates regulatory interaction from restoration/decay. Standard gene-regulatory ODE formulations can represent transcript degradation as a negative diagonal contribution distinct from off-diagonal regulatory interactions. Chen et al. explicitly treat mRNA decay rates as diagonal terms and regulatory effects as off-diagonal terms in a gene-regulatory Jacobian [1]. This supplies a biologically defensible **structural decomposition**, but it does not by itself supply SCC25-specific numerical restoration rates.

The SCC25 temporal program estimates discrete transition operators `T`. Where a continuous-time embedding is mathematically admissible,

`T = exp(J Delta t)`

links the observed discrete dynamics to an effective continuous-time generator `J`. The effective generator combines regulatory interaction, self-effects, degradation/restoration, and any other dynamics represented by the fitted state coordinates. Thus the existing temporal evidence constrains the **combined generator** but does not automatically identify the decomposition required for normalized empirical G1.

## 6.2 What the SCC25 sources actually contain

The restoration problem is narrower than a generic missing-data statement.

The short-term SCC25 experiment, GEO `GSE114446`, is a 5-day cetuximab-versus-PBS RNA-seq time course generated on Illumina HiSeq 2500. GEO reports raw reads in SRA (`SRP145751`, BioProject `PRJNA471358`) as well as processed counts. Representative SCC25 sample records identify the extracted molecule as poly(A) RNA and report poly(A) enrichment during library preparation [2].

The chronic SCC25 experiment, RNA-seq series `GSE98812` within SuperSeries `GSE98815` / BioProject `PRJNA386291`, followed weekly cetuximab/PBS treatment over the development of resistance. The published methods report Illumina HiSeq `2 x 100 bp` sequencing, MapSplice alignment, and RSEM quantification [3]. The study used the Illumina TruSeq RNA workflow, an mRNA-focused poly(A)-selection protocol [4].

Therefore both temporal programs have raw sequencing lineage, but neither can be treated automatically as an ideal whole-transcriptome total-RNA experiment for premature/mature RNA decomposition. Poly(A) enrichment can deplete intronic/premature signal. A raw-read intronic-signal feasibility audit is therefore required before INSPEcT−-style inference is used.

This closes two assumptions simultaneously: the relevant SCC25 raw RNA-seq **does exist**, but adequate premature-RNA information **cannot be presumed**.

## 6.3 Condition-matched bulk kinetic inference

INSPEcT− was developed to infer RNA synthesis, processing, and degradation kinetics from steady-state or time-course total RNA-seq without metabolic labeling by jointly modeling premature and mature RNA [5]. This makes it a scientifically relevant candidate method for the restoration problem, but not an automatic one.

If the raw SCC25 alignments retain sufficient premature/intronic signal despite poly(A) selection, INSPEcT− or a comparably validated kinetic model could provide **condition-matched inferred degradation constraints**. These constraints would substantially reduce the restoration assumption. They would not constitute independent validation, however, because the kinetic estimate and the transition operator would derive from the same biological experiment.

If the required signal is inadequate, this route is refused rather than reconstructed from gene-level expression summaries.

## 6.4 SCC25 single-cell RNA velocity as a second kinetic channel

The short-term HNSCC program also generated SCC25 single-cell RNA-seq and reported RNA-velocity analysis [6]. RNA-velocity methods use spliced and unspliced RNA to estimate directed transcriptional dynamics; dynamical formulations can estimate transcription, splicing, and degradation-rate parameters [7]. Raw SCC25 single-cell sequencing is available through the study's GEO/SRA lineage.

This creates a second, SCC25-specific kinetic channel that is not available from static TCGA. It is valuable because it can constrain degradation/restoration behavior using spliced/unspliced information rather than bulk expression alone. It is nevertheless model-dependent, and it represents a different measurement design from the bulk time courses. We therefore treat it as a **cross-representation kinetic constraint**, not as a direct genome-wide half-life assay or a plug-in restoration vector.

Agreement between bulk inverse-generator constraints and single-cell kinetic estimates would narrow the restoration family. Disagreement would be retained as representation-dependent Limit-Map evidence.

## 6.5 Independent kinetic evidence as bounds

Genome-wide RNA-stability assays provide an independent evidence role. BRIC-seq determines transcript half-lives by following BrU-labeled RNA decay and can measure RNA stability transcriptome-wide [8,9]. These data can define biologically plausible degradation scales and reject restoration regimes grossly inconsistent with mammalian RNA kinetics. They are not SCC25-specific measurements and therefore are used as **bounds or sensitivity references**, not copied into SCC25 gene-specific restoration values.

SCC25 itself has historical evidence that transcript stability is measurable and condition-dependent. Saunders et al. measured E2F1 mRNA stability in SCC25 and showed a different stability response from normal keratinocytes [10]. This establishes proof-of-principle relevance of transcript decay in the cell line, while remaining far too sparse to identify a genome-wide restoration operator.

## 6.6 Prospective inverse-identifiability test

The restoration problem is therefore posed prospectively as an inverse problem:

1. preserve the frozen SCC25 transition operators and sensitivity envelopes;
2. determine the admissible continuous-time generator family, including matrix-log branch/refusal structure;
3. impose only independently justified restoration structure, not convenient numerical values;
4. quantify whether the existing bulk raw reads support condition-matched kinetic inference;
5. use the SCC25 single-cell spliced/unspliced channel as a separate kinetic constraint where its frozen model is valid;
6. use independent transcript-half-life data as biological plausibility bounds rather than substitutions;
7. propagate the entire allowed restoration family through normalized G1.

The decisive criterion is **invariance**, not distance to unity. If materially distinct restoration operators compatible with all available evidence yield the same G1 conclusion within propagated uncertainty, G1 may become identifiable within that stated validity regime. If plausible restoration choices materially change the result, the correct state remains `NOT_IDENTIFIABLE`.

Until that analysis is complete, the manuscript claim is:

> The SCC25 temporal data constrain an effective regulatory generator but do not yet directly measure its genome-wide restoration component. Raw RNA-seq lineage, a separate SCC25 single-cell RNA-velocity channel, and independent transcript-stability measurements make the missing restoration term a bounded inverse-identifiability problem rather than an unconstrained assumption. We therefore test whether these evidence streams narrow the admissible restoration family sufficiently for G1 inference without assigning a common decay constant or tuning normalization toward unity.

## 6.7 Evidence-class firewall

The following evidence classes are kept distinct:

- bulk G2 dynamics: condition-matched, but part of the temporal evidence being decomposed;
- bulk kinetic inference from the same SCC25 experiment: condition-matched, method-derived, not independent validation;
- SCC25 single-cell RNA velocity: cell-line/treatment related and kinetically informative, but representation- and model-dependent;
- historical SCC25 transcript-stability experiments: cell-line matched but sparse and condition-specific;
- BRIC-seq/other mammalian half-life atlases: methodologically independent but biologically non-matched.

No combination is described as a directly measured SCC25 genome-wide restoration operator unless such a dataset is actually identified or generated.

## References for this section

1. Chen Y, et al. *Gene regulatory network stabilized by pervasive weak repressions: microRNA functions revealed by the May–Wigner theory.* PMCID: `PMC8291590`.
2. NCBI GEO `GSE114446`; representative SCC25 sample metadata including `GSM3141833`; SRA `SRP145751`; BioProject `PRJNA471358`.
3. Kagohara LT, et al. *Integrated time course omics analysis distinguishes immediate therapeutic response from acquired resistance.* PMCID: `PMC5966898`; GEO `GSE98812` / `GSE98815`; BioProject `PRJNA386291`.
4. Illumina TruSeq RNA Library Prep v2 documentation: mRNA-focused poly(A)-selection workflow.
5. Furlan M, et al. *Genome-wide dynamics of RNA synthesis, processing, and degradation without RNA metabolic labeling.* *Genome Research* 2020;30:1492–1505. DOI: `10.1101/gr.260984.120`; PMID: `32978246`; PMCID: `PMC7605262`.
6. Kagohara LT, et al. *Integrated single-cell and bulk gene expression and ATAC-seq reveals heterogeneity and early changes in pathways associated with resistance to cetuximab in HNSCC-sensitive cell lines.* PMID: `32362655`; PMCID: `PMC7341752`.
7. Bergen V, et al. *Generalizing RNA velocity to transient cell states through dynamical modeling.* *Nature Biotechnology* 2020;38:1408–1414.
8. Imamachi N, et al. *BRIC-seq: a genome-wide approach for determining RNA stability in mammalian cells.* *Methods* 2014;67(1):55–63. DOI: `10.1016/j.ymeth.2013.07.014`; PMID: `23872059`.
9. Tani H, et al. *Genome-wide determination of RNA stability reveals hundreds of short-lived noncoding transcripts in mammals.* PMCID: `PMC3337439`.
10. Saunders NA, Dicker AJ, Jones SJ, Dahler AL. *E2F1 messenger RNA is destabilized in response to a growth inhibitor in normal human keratinocytes but not in a squamous carcinoma cell line.* *Cancer Research* 1998;58(8):1646–1649. PMID: `9563476`.
