# Stage C1 methylation annotation / feature-reduction specification — DRAFT

Date: 2026-08-30

Status: **DRAFT ONLY — NOT FROZEN — NO BIOLOGICAL ASSOCIATION MAY START FROM THIS DOCUMENT**

This draft is prepared after Stage C0.1 closed and before any methylation-RNA, methylation-RPPA, methylation-genomic, outcome, or preferred-pattern association is calculated. It does not change the frozen C0/C0.1 source or sample-identity rules.

## Recommended provenance anchor

Primary annotation lineage:

- Illumina Infinium HumanMethylation450 v1.2 manifest;
- source manifest name: `HumanMethylation450_15017482_v.1.2.csv`;
- genome mapping: hg19 / GRCh37-era Illumina mapping;
- Bioconductor reference implementation: `IlluminaHumanMethylation450kanno.ilmn12.hg19`;
- historically aligned package candidate: version `0.6.0` from the Bioconductor 3.8 era;
- Bioconductor DOI: `10.18129/B9.bioc.IlluminaHumanMethylation450kanno.ilmn12.hg19`.

Rationale: the frozen PanCanAtlas methylation source is a publication-era HM27/HM450 merged matrix. The primary annotation should therefore preserve the corresponding Illumina v1.2/hg19 coordinate system rather than silently remap probes to a newer genome build or gene model after C0/C0.1 results are known.

Before final freeze, the exact acquired annotation artifact must be hashed and its overlap with all 22,601 C0 probe IDs must be inventoried without using methylation beta values.

## Proposed mapping rule

For each C0 probe, preserve the Illumina `UCSC_RefGene_Name`, `UCSC_RefGene_Accession`, and `UCSC_RefGene_Group` information as a many-to-many annotation.

Recommended rule:

1. do not select only the first listed gene, transcript, or region;
2. split the semicolon-aligned gene / accession / group fields into ordered annotation tuples;
3. preserve every distinct probe–gene–region tuple supported by the manifest;
4. collapse exact duplicate tuples only, not biologically distinct transcript/gene mappings;
5. a probe may therefore contribute to more than one gene or regulatory stratum when the frozen manifest says it does;
6. no downstream RNA, RPPA, genomic, outcome, Hallmark, or preferred SymC result may decide which mapping is retained.

This avoids a hidden favorable-gene selection step and preserves the manifest's transcript-level multiplicity.

## Proposed regulatory strata

Keep regulatory compartments separate rather than forcing all gene-associated probes into one methylation score.

Candidate strata derived directly from Illumina's documented `UCSC_RefGene_Group` categories:

- `PROMOTER_CORE`: `TSS200`;
- `PROMOTER_PROXIMAL`: `TSS1500`;
- `PROMOTER_TRANSCRIBED_EDGE`: `5'UTR` and `1stExon`;
- `GENE_BODY`: `Body`;
- `THREE_PRIME_UTR`: `3'UTR`;
- `UNMAPPED_TO_REFGENE`: no RefGene mapping.

For a broader promoter coordinate, the candidate union is `TSS200 + TSS1500 + 5'UTR + 1stExon`, but the component strata should remain recoverable so a broad promoter result cannot hide opposite behavior among its parts.

## Proposed unmapped handling

Unmapped-to-RefGene probes should not be discarded from the mode-resolved probe-space representation merely because they cannot enter a gene/Hallmark map.

Recommended split:

- **modal probe-space analysis:** retain all source-approved probes that pass the separately frozen technical mask, regardless of gene annotation;
- **gene/Hallmark conglomeration analysis:** use only probes with an admissible frozen gene mapping;
- report the number and fraction excluded from gene/Hallmark aggregation because of missing annotation.

## Proposed technical-probe policy

The publication-era C0 matrix is the primary source and is not renormalized. However, known HM450 cross-reactivity and polymorphic-CpG effects can create spurious covariance/association structure.

Recommended two-track policy:

### Primary publication-faithful track

- start from the exact 22,601 C0 source probes as supplied after the PanCanAtlas platform processing;
- apply no result-driven probe filtering;
- retain the original publication-era representation.

### Mandatory technical-mask robustness track

Freeze an external pre-result mask using literature published before the 2018 PanCanAtlas analysis, including HM450 cross-reactive / polymorphic-probe information. The exact mask source, version, criteria, overlap count, and hash must be recorded before any target association is inspected.

Promotion rule candidate: a claimed methylation architecture should not depend qualitatively on known technically problematic probes. Primary and masked results should be reported together where the mask changes the estimand materially.

Candidate technical references include Chen et al. 2013 (`10.4161/epi.23470`) and Zhou, Laird & Shen 2017 (`10.1093/nar/gkw967`). No mask is frozen by this draft.

## Proposed modal + scalar + conglomeration architecture

The three views remain complementary and none is biological chi.

### Modal

Primary carrier: probe-space methylation covariance / correlation structure within each eligible cancer, with mode-resolved eigenvalues/eigenvectors, effective dimensionality / participation quantities, and loading stability assessed under fixed-n resampling.

The modal analysis must not use RNA/Hallmark agreement to choose the number of modes or features.

### Scalar

Any scalar is a compression of the methylation architecture, not a replacement for it and not chi.

Candidate scalar families may include pre-specified effective-rank / participation summaries or module-level coherence summaries, but exact formulas, finite-sample behavior, and nulls must be frozen before calculation. No distance-to-1 or critical-damping interpretation is licensed.

### Conglomeration

Use the frozen many-to-many probe→gene→Hallmark mapping to construct separately reported regulatory-stratum module architecture. Cross-layer comparisons to Stage A/B1/B2 occur only after this representation and its nulls are frozen.

No single master stability score is constructed.

## Proposed finite-sample and construction controls

Recommended minimum controls before cross-layer interpretation:

1. preserve the established cancer eligibility floor `n >= 30`;
2. use the strict 9,460-sample C0.1 one-to-one cohort only;
3. fixed-n resampling where cross-cancer network quantities are compared, using a preselected n no larger than the smallest eligible cohort used for that comparison;
4. probe-label / module-membership construction nulls appropriate to the statistic;
5. patient-label permutation for cross-assay coupling while preserving within-assay structure;
6. report reference vs technical-mask robustness;
7. no favorable mode count, regulatory stratum, Hallmark, or cancer selection after results.

Exact n, resample count, mode-retention rule, null definitions, seeds, and promotion criteria remain to be frozen in the final C1 preregistration.

## Explicit non-claims

This static methylation extension cannot by itself establish:

- temporal inheritance;
- causal substrate control;
- damping or recovery rates;
- a phase/state transition;
- critical slowing;
- treatment response;
- optimality;
- `chi = 1` biology;
- biological chi.

Ordered perturbation/time-course evidence remains required before substrate-inheritance promotion. Same-coordinate dynamic `Gamma` and `Omega` remain required before any biological chi admission test.

## Decision required before freeze

The final preregistration requires explicit approval or revision of the following scientific choices:

1. v1.2 / hg19 as the primary annotation lineage;
2. many-to-many probe→gene mapping rather than first-gene selection;
3. separate regulatory strata plus a recoverable broad-promoter union;
4. unmapped probes retained for modal probe-space analysis but excluded from gene/Hallmark aggregation;
5. publication-faithful primary track plus mandatory pre-result technical-mask robustness track;
6. modal + scalar + conglomeration retained as complementary views;
7. no biological chi or substrate-inheritance claim from static C1.

Until these choices are approved and converted into a machine-readable frozen plan, Stage C1 remains blocked.
