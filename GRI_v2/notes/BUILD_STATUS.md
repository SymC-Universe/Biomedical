# GRI v2 build status

Status date: 2026-08-30

## Scientific status

The Cancer Stability Atlas / substrate-architecture program remains a development program, not a validated clinical tool. `CV/2` remains historical only. No biological chi coordinate has been admitted, and `chi = 1` is not presumed to be a cancer optimum, healthy state, therapeutic target, or organization maximum.

Stages A, A1.1, B1, B2 RPPA, B2 genomic, B2 static integration, Stage C0 methylation source identity, and Stage C0.1 one-to-one methylation sample identity are closed. **The Stage C1A annotation specification is now prospectively frozen, and its external source gate has passed. The active operation is the exact 22,601-probe local annotation/mask intersection.** No methylation beta-value biological association has been calculated.

## Stage C0 closure

Canonical audit: `docs/STAGE_C0_METHYLATION_AUDIT_20260830.md`.

The exact frozen PanCanAtlas merged HM27/HM450 source passed cryptographic identity and schema gates:

- source SHA-256 `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`;
- exact GDC MD5 `5cec086f0b002d17befef76a3241e73b`;
- exact size `5,022,150,019` bytes;
- exactly 22,601 unique nonblank probe rows;
- all 12,039 methylation sample columns parse as TCGA sample roots;
- 9,494 / 9,546 Stage A tumors have source presence;
- all 32 / 32 cancers pass n>=30.

C0 exposed 41 primary sample roots represented by more than one methylation source column. Those duplicates were resolved prospectively in C0.1 rather than silently collapsed.

## Stage C0.1 closure

Canonical audit: `docs/STAGE_C0_1_SAMPLE_IDENTITY_AUDIT_20260830.md`.

Frozen duplicate-root rule: **exclude from primary C1**. No beta averaging, first/last selection, platform preference, or value-based replicate choice is allowed.

C0.1 result:

- exact unique-root matches: 9,459;
- unique patient fallback matches: 1;
- strict one-to-one matched Stage A tumors: **9,460 / 9,546 (99.0991%)**;
- duplicate-root Stage A samples excluded: 34;
- no-source Stage A samples: 52;
- all **32 / 32 cancers** remain above the frozen n>=30 gate;
- lowest retained fraction: GBM 125 / 154 (81.17%), still above n>=30;
- beta-value rows read for biological analysis: false;
- biological association performed: false.

## Stage C1A frozen annotation architecture

Explicit approval was given before any C1 beta-value association. The frozen machine-readable contract is:

`config/stage_c1_annotation_feature_plan.json`

Formal preregistration:

`docs/STAGE_C1A_ANNOTATION_PREREGISTRATION_20260830.md`

The approved architecture freezes:

1. Illumina HumanMethylation450 v1.2 / `ilmn12.hg19` as the primary annotation lineage;
2. Bioconductor release 3.8 package `IlluminaHumanMethylation450kanno.ilmn12.hg19` version 0.6.0 as the exact annotation source;
3. positional preservation of all supported probe-gene-accession-region tuples rather than first-gene selection;
4. distinct `TSS200`, `TSS1500`, `5'UTR/1stExon`, `Body`, and `3'UTR` regulatory strata, plus a secondary broad-promoter union;
5. unmapped probes retained in modal probe space but excluded from invented gene/Hallmark assignment;
6. the exact 22,601 PanCanAtlas probes retained as the publication-faithful primary track;
7. a mandatory robustness mask formed from the union of a pinned Chen et al. cross-reactive list and the frozen annotation package's deterministic common-SNP layer;
8. modal + scalar + conglomeration as complementary views, with no biological chi or master stability score admitted.

## Stage C1A external source-gate result

Canonical audit:

`docs/STAGE_C1A_ANNOTATION_SOURCE_AUDIT_20260830.md`

Successful repaired source-gate run: `33318029738`

Source-gate commit: `f334b656df0fb9740cd320783dbd24e6f65fdd32`

Primary annotation source:

- resolved Bioconductor 3.8 URL exactly matched the frozen source;
- size `57,839,020` bytes;
- MD5 `2f569646ca8adc49863224b1cd076a79`;
- SHA-256 `249b8fd62add3c95b5047b597cff0868d26a98862a47cebd656edcd175a73b15`;
- package/version validated directly from the tarball `DESCRIPTION`;
- extraction mode: direct frozen tarball `DataFrame` objects, no historical package installation.

The deterministic common-SNP rule selected `SNPs.147CommonSingle`, the numerically highest available `CommonSingle` object in the frozen package.

Portable annotation export:

- 485,512 rows;
- 485,512 unique probe IDs;
- 0 duplicate probe IDs;
- 365,860 RefGene-mapped rows;
- 17,120 rows with a common SNP at CpG or SBE;
- SHA-256 `a7f83233f97c3933752d74b8042e967de88df20eba2cf477a536136631a8da17`.

Pinned Chen cross-reactive source:

- exact Git blob SHA-1 `f5bff6dee26f8d05ccd2d0bcfaf8ff1c0afb6e11`;
- size `569,533` bytes;
- MD5 `f2f8a7e69f53eb44ea9ecc7842cdc845`;
- SHA-256 `4e962d36821f6f6fcd8b81cc0558090c028e54fbdb2c039a5712f9b471d9d89e`;
- compact export: 29,233 unique TargetIDs;
- compact export SHA-256 `078e95716af2b20c3515f59d09310d20c43deb5ed8ba8d1b70885810acde2179`.

The original C1A source workflow encountered a mechanical current-R dependency cycle before frozen source use. The repaired implementation extracts only the required frozen `DataFrame` objects directly from the exact 0.6.0 tarball with a minimal `S4Vectors` runtime. Scientific settings and source bytes were unchanged. The repaired general CI and source-gate workflow passed.

## Active gate: exact 22,601-probe local intersection

The exact PanCanAtlas 22,601 probe IDs exist in the already-audited local 5.02 GB source. Re-downloading that matrix solely to recover row IDs is unnecessary.

The final C1A local gate therefore:

- reuses the existing source;
- verifies its complete SHA-256 while streaming;
- reads only the first tab-delimited field from each data row as the probe ID;
- never parses beta values for biological analysis;
- requires exactly 22,601 unique source probe IDs;
- requires exact overlap with the frozen annotation export;
- reports RefGene mapped/unmapped counts, positional tuple mismatches, regulatory strata, Chen overlap, common-SNP overlap, mask union, and robustness remaining-probe count.

C1 biological beta-value analysis remains blocked until this exact-probe inventory passes and is audited.

## What follows the local C1A gate

If the 22,601-probe gate passes, the next operation is still **not** immediate biological analysis. First the exact C1 analysis specification must be frozen prospectively, including:

- modal representation and normalization;
- scalar compression formulas and construction behavior without calling them chi;
- conglomeration representation using the frozen probe-gene-region mapping;
- missingness and eligibility rules;
- fixed-n resampling if retained;
- deterministic seeds;
- construction nulls;
- cross-assay alignment nulls;
- promotion criteria.

Only after those rules are frozen and regression-tested may methylation beta values be used in C1 biological relationship testing.

## Exact user action

The active user action is to run the tested Stage C1A exact-probe inventory handoff once the final packaging verification is complete. It requires selecting only the already-audited local 5.02 GB methylation TSV; all compact frozen annotation inputs are bundled and selected automatically.

At completion return only:

- `stage_c1a_probe_inventory_outputs/STAGE_C1A_PROBE_INVENTORY_SUMMARY.json`
- `stage_c1a_probe_inventory_outputs/stage_c1a_regulatory_stratum_counts.csv`

Keep the generated `.csv.gz` mapping and flags files local for Stage C1. Keep the 5.02 GB methylation source and existing B2 task caches unchanged.
