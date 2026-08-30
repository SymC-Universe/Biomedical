# Stage C1A methylation annotation and technical-mask preregistration

Date: 2026-08-30

Status: **FROZEN AFTER EXPLICIT USER APPROVAL AND BEFORE ANY C1 METHYLATION BETA-VALUE BIOLOGICAL ASSOCIATION**

Machine-readable contract: `config/stage_c1_annotation_feature_plan.json`.

## Purpose

Stage C1A closes the annotation and technical-mask provenance problem before the methylation layer is allowed to participate in biological relationship testing. It is deliberately separate from C1 biological analysis. C1A may identify which probes can be mapped to genes/regulatory strata and which probes fall into a prespecified technical-robustness mask, but it may not inspect whether any of those choices improve agreement with RNA, RPPA, genomic burden, outcomes, treatment response, historical GRI coordinates, or any preferred SymC pattern.

The upstream source and sample identity are already fixed by C0/C0.1. The exact methylation source SHA-256 remains `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`, and the primary C1 cohort is the strict one-to-one C0.1 cohort of 9,460 Stage A tumors across all 32 cancers.

## Frozen primary annotation lineage

The primary annotation is the publication-era-compatible Illumina HumanMethylation450 v1.2 / `ilmn12.hg19` lineage, represented by:

- Bioconductor package: `IlluminaHumanMethylation450kanno.ilmn12.hg19`;
- Bioconductor release: `3.8`;
- package version: `0.6.0`;
- source filename: `IlluminaHumanMethylation450kanno.ilmn12.hg19_0.6.0.tar.gz`;
- underlying Illumina annotation: `HumanMethylation450_15017482_v.1.2.csv`;
- DOI: `10.18129/B9.bioc.IlluminaHumanMethylation450kanno.ilmn12.hg19`.

The source gate will try only the enumerated Bioconductor 3.8 URLs in the machine-readable plan. Whichever resolves successfully must install as package version 0.6.0. The resolved URL, bytes, MD5, and SHA-256 are recorded. No current hg38 or current SeSAMe annotation silently replaces this primary representation.

## Frozen many-to-many mapping rule

For each probe, the Illumina fields `UCSC_RefGene_Name`, `UCSC_RefGene_Accession`, and `UCSC_RefGene_Group` are parsed as positionally aligned semicolon-delimited tuples.

The rule is:

1. preserve empty tokens while splitting;
2. trim whitespace;
3. require equal tuple lengths across gene name, accession, and regulatory-group fields;
4. preserve every distinct supported nonblank probe-gene-accession-region tuple;
5. collapse exact duplicate tuples only;
6. never select the first gene/transcript as a convenience rule;
7. never choose a mapping because a downstream association is stronger.

If the three fields cannot be aligned without heuristic repair, the affected probe is excluded from gene/Hallmark conglomeration and reported. It remains eligible for modal probe-space analysis if otherwise admissible.

## Frozen regulatory strata

The following Illumina v1.2 categories remain distinct:

- `PROMOTER_CORE`: `TSS200`;
- `PROMOTER_PROXIMAL`: `TSS1500`;
- `PROMOTER_TRANSCRIBED_EDGE`: `5'UTR`, `1stExon`;
- `GENE_BODY`: `Body`;
- `THREE_PRIME_UTR`: `3'UTR`.

A secondary `BROAD_PROMOTER` union may combine `TSS200 + TSS1500 + 5'UTR + 1stExon`, but the component strata must remain separately recoverable and reported. A broad-promoter result cannot replace or hide the component results.

Probes with no admissible RefGene mapping remain in the modal probe-space representation but do not receive an invented nearest-gene assignment for gene/Hallmark conglomeration.

## Frozen technical-mask robustness track

The exact 22,601-probe PanCanAtlas matrix remains the **primary publication-faithful track**. Stage C1A does not retroactively redefine the primary source by deleting probes.

A mandatory robustness track is frozen as the union of two external, pre-result technical components.

### Cross-reactive component

- scientific reference: Chen et al. 2013, *Epigenetics*, DOI `10.4161/epi.23470`;
- retrieval repository: `sirselim/illumina450k_filtering`;
- frozen commit: `eac47812dce5d4d1340caeafb92d80dd4d8273a5`;
- file: `48639-non-specific-probes-Illumina450k.csv`;
- Git blob SHA-1: `f5bff6dee26f8d05ccd2d0bcfaf8ff1c0afb6e11`;
- mask rule: every `TargetID` in that file.

The source gate records an independent SHA-256 for the acquired file.

### Common-SNP component

The common-SNP mask is derived from the same pinned Bioconductor annotation package rather than from a modern genome build.

The object-selection rule is deterministic: among objects named `SNPs.<build>CommonSingle` contained in the pinned package, use the numerically highest dbSNP build present. That choice depends only on the frozen package contents, not on methylation results.

A probe enters this mask when either `CpG_rs` or `SBE_rs` is nonblank in the selected object. `Probe_rs` alone does not trigger exclusion. No extra MAF threshold is applied beyond membership in the package's CommonSingle annotation. This corresponds to the standard minfi logic of dropping CpG- or SBE-overlapping common variants with `maf=0` against the selected pinned SNP annotation.

The robustness mask is the union of the cross-reactive and common-SNP components. Primary and masked analyses must both be reported. A claim cannot be promoted solely because one track looks favorable.

## C1A local probe inventory

The exact PanCanAtlas 22,601-probe subset is present only in the already-audited 5.02 GB local methylation matrix. Re-downloading that matrix solely to recover its row IDs would add cost without new evidence.

Therefore C1A has two mechanical parts:

1. GitHub Actions acquires, hashes, validates, and exports the frozen annotation and mask sources to a compact portable annotation artifact.
2. A local header/row-ID inventory reuses the existing C0 methylation TSV and intersects its 22,601 row IDs with that compact artifact. It may stream the source file, but it must not parse beta values into a biological analysis.

The local inventory reports at minimum:

- 22,601 expected source probes and exact uniqueness;
- annotation overlap count;
- RefGene-mapped vs unmapped count;
- tuple-length mismatch count;
- counts by regulatory stratum;
- cross-reactive overlap;
- common-SNP overlap;
- union technical-mask overlap;
- remaining primary/robustness probe counts.

These are source/schema quantities, not biological results.

## Modal + scalar + conglomeration boundary

The approved arc remains binding: **modal + scalar + conglomeration are complementary views of the substrate architecture**.

- Modal analysis will carry the mode-resolved methylation structure.
- Scalar coordinates will be compressed summaries only after their formulas and construction behavior are frozen.
- Conglomeration will carry gene/module/system organization using the frozen many-to-many mapping.

No scalar may replace the modal carrier or the conglomeration-level organization. None of these static methylation quantities is biological chi.

The exact C1 formulas, fixed-n resampling, missing-data handling, construction nulls, deterministic seeds, module eligibility, and cross-layer tests are frozen only **after** C1A reports annotation/schema coverage and **before** any beta-value biological result is inspected. This sequencing allows source-schema facts to inform whether a proposed feature is technically defined without allowing biological outcomes to tune the model.

## Explicit non-claims

C1A cannot establish:

- methylation-RNA coupling;
- protein/genomic coupling;
- causal regulation;
- substrate inheritance;
- temporal ordering;
- damping or recovery;
- critical slowing;
- a state/phase transition;
- treatment response;
- an optimum;
- `chi = 1` biology;
- biological chi.

Static C1 itself will also remain insufficient for substrate-inheritance promotion. Ordered or temporal evidence is still required. Any future biological chi test still requires genuine same-coordinate `Gamma` and `Omega` under the separate admission rules.

## Gate rule

C1 biological computation remains **BLOCKED** until:

1. the annotation package and cross-reactive source are acquired and hashed;
2. the portable annotation export passes schema checks;
3. the exact 22,601 PanCanAtlas probe IDs are inventoried against the frozen mapping and mask;
4. C1A is audited;
5. the full C1 analysis formulas/nulls/seeds are frozen and regression-tested.

Only then may methylation beta values be opened for the biological Stage C1 run.
