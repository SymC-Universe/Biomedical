# GRI v2 build status

Status date: 2026-08-30

## Scientific status

The Cancer Stability Atlas / substrate-architecture program remains a development program, not a validated clinical tool. `CV/2` remains historical only. No biological chi coordinate has been admitted, and `chi = 1` is not presumed to be a cancer optimum, healthy state, therapeutic target, or organization maximum.

Stages A, A1.1, B1, B2 RPPA, B2 genomic, B2 static integration, Stage C0 methylation source identity, Stage C0.1 one-to-one sample identity, and **Stage C1A annotation/exact-probe inventory are closed**. No Stage C1 methylation beta-value biological association has been calculated.

The active gate is now the **prospective Stage C1 modal + scalar + conglomeration formula/null/promotion freeze**. Beta-value biology remains blocked until that scientific contract is explicitly approved and regression-tested.

## Closed upstream state

### Stage C0

Canonical audit: `docs/STAGE_C0_METHYLATION_AUDIT_20260830.md`.

- exact PanCanAtlas merged HM27/HM450 source SHA-256: `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`
- exact GDC MD5: `5cec086f0b002d17befef76a3241e73b`
- exact size: `5,022,150,019` bytes
- exact unique probes: 22,601
- methylation sample columns: 12,039
- Stage A tumors with source presence: 9,494 / 9,546
- cancers passing n>=30: 32 / 32

### Stage C0.1

Canonical audit: `docs/STAGE_C0_1_SAMPLE_IDENTITY_AUDIT_20260830.md`.

Frozen duplicate-root rule: **exclude from primary C1**.

- exact unique-root matches: 9,459
- unique patient fallback matches: 1
- strict one-to-one matched Stage A tumors: 9,460 / 9,546
- duplicate-root Stage A samples excluded: 34
- no-source Stage A samples: 52
- cancers remaining above n>=30: 32 / 32
- beta-value biological analysis performed: false

## Stage C1A annotation freeze

Machine-readable contract: `config/stage_c1_annotation_feature_plan.json`

Preregistration: `docs/STAGE_C1A_ANNOTATION_PREREGISTRATION_20260830.md`

External-source audit: `docs/STAGE_C1A_ANNOTATION_SOURCE_AUDIT_20260830.md`

Exact-probe audit: `docs/STAGE_C1A_PROBE_INVENTORY_AUDIT_20260830.md`

The frozen annotation architecture uses:

- Illumina HumanMethylation450 v1.2 / `ilmn12.hg19`;
- Bioconductor 3.8 package `IlluminaHumanMethylation450kanno.ilmn12.hg19` version 0.6.0;
- all distinct supported probe-gene-accession-region tuples rather than first-gene selection;
- distinct `TSS200`, `TSS1500`, `5'UTR/1stExon`, `Body`, and `3'UTR` strata plus a secondary broad-promoter union;
- unmapped probes retained only where an all-probe modal calculation does not require invented gene assignment;
- all 22,601 PanCanAtlas probes as the publication-faithful primary track;
- a mandatory robustness mask equal to the union of the pinned Chen cross-reactive list and the frozen common-SNP-at-CpG/SBE layer;
- modal + scalar + conglomeration as complementary views, with no biological chi or master score admitted.

### C1A external source result

- annotation package SHA-256: `249b8fd62add3c95b5047b597cff0868d26a98862a47cebd656edcd175a73b15`
- deterministic common-SNP object: `SNPs.147CommonSingle`
- portable annotation rows / unique probe IDs: 485,512 / 485,512
- portable annotation SHA-256: `a7f83233f97c3933752d74b8042e967de88df20eba2cf477a536136631a8da17`
- pinned Chen source SHA-256: `4e962d36821f6f6fcd8b81cc0558090c028e54fbdb2c039a5712f9b471d9d89e`
- compact Chen-ID export: 29,233 unique IDs
- compact Chen-ID SHA-256: `078e95716af2b20c3515f59d09310d20c43deb5ed8ba8d1b70885810acde2179`

### C1A exact local probe-inventory result

Canonical compact outputs:

- `development_outputs/stage_c1a_probe_inventory/STAGE_C1A_PROBE_INVENTORY_SUMMARY.json`
  - SHA-256 `04632061a28570f5eefcd41bd4abca230cd42e63538e02a9ab941b3cecf88168`
- `development_outputs/stage_c1a_probe_inventory/stage_c1a_regulatory_stratum_counts.csv`
  - SHA-256 `603b96ac879c4c58517479bc5dbee10bf89a0f47c374abd653c492d928de1cbc`

Gate result: **STAGE_C1A_PROBE_INVENTORY_PASS**.

- source probe rows: 22,601
- unique source probe IDs: 22,601
- exact annotation overlap: **22,601 / 22,601**
- missing annotation probes: 0
- RefGene-mapped probes: 22,469
- RefGene-unmapped probes: 132
- preserved probe-gene-accession-region tuples: 46,287
- tuple-length mismatch probes: 0
- mapped probes lacking a frozen regulatory stratum: 0

Regulatory-stratum unique-probe counts:

- `PROMOTER_CORE`: 3,999
- `PROMOTER_PROXIMAL`: 8,157
- `PROMOTER_TRANSCRIBED_EDGE`: 9,455
- `GENE_BODY`: 4,983
- `THREE_PRIME_UTR`: 152
- `BROAD_PROMOTER_SECONDARY`: 19,362

The strata overlap and are not a partition.

Technical-mask overlap:

- Chen cross-reactive: 524
- common SNP at CpG or SBE: 59
- union mask: 579
- mandatory masked robustness track: **22,022 probes**

The local C1A engine reverified the complete 5.02 GB source SHA-256 and extracted probe IDs only. `methylation_beta_values_parsed_for_biological_analysis=false` and `biological_association_performed=false`.

## Active scientific gate: Stage C1 analysis freeze

The next contract must be approved before opening beta values for biological analysis. It will prospectively freeze:

1. the exact all-probe modal representation and normalization;
2. scalar compression derived from and traceable to the modal spectrum, without calling it chi;
3. probe-to-gene and Hallmark conglomeration rules using the frozen C1A map;
4. the primary regulatory stratum versus prespecified secondary strata;
5. missingness and sample/probe eligibility;
6. fixed-n resampling and deterministic seed construction;
7. a probe-marginal-preserving construction null;
8. patient-alignment and Hallmark-label cross-assay nulls;
9. primary inferential families, multiple-testing control, and promotion rules;
10. the exact claim ceiling.

The first biological C1 question is intentionally static: whether methylation has reproducible organization beyond probe-marginal construction and whether that organization aligns specifically with the independently frozen RNA Hallmark architecture. Even a positive result would not establish causality, temporal inheritance, damping, a phase boundary, or biological chi.

## Exact user action

Review and explicitly approve or revise the proposed Stage C1 scientific contract. No local computation is required until that approval is recorded.

Keep the 5.02 GB methylation source, the C1A generated mapping/flags `.csv.gz` files, the Stage A cache, and existing B2 task caches unchanged.
