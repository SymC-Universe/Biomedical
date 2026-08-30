# GRI v2 build status

Status date: 2026-08-30

## Scientific status

The Cancer Stability Atlas / substrate-architecture program remains a development program, not a validated clinical tool. `CV/2` remains historical only. No biological chi coordinate has been admitted, and `chi = 1` is not presumed to be a cancer optimum, healthy state, therapeutic target, or organization maximum.

Stages A, A1.1, B1, B2 RPPA, B2 genomic, B2 static integration, Stage C0 methylation source identity, and Stage C0.1 one-to-one methylation sample identity are closed. **The next active gate is the prospective methylation annotation / feature-reduction specification.** No methylation biological association has been calculated.

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

C0 also exposed 41 primary sample roots represented by more than one methylation source column. Because the frozen C0 plan required stopping on unexpected schema, those duplicates were resolved prospectively in C0.1 rather than silently collapsed.

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

Canonical compact outputs:

- `development_outputs/stage_c0_1_sample_identity/STAGE_C0_1_SAMPLE_IDENTITY_SUMMARY.json`
  - SHA-256 `82d885ea8b1674f18bfda8317398b1f1658c383a351d626f4a793e303edb18a4`
- `development_outputs/stage_c0_1_sample_identity/stage_c0_1_unique_match_coverage.csv`
  - SHA-256 `1fd625b7d575995185bc6d6e9f8dfebdc82abbb89afe553dae121c2ce40e3fc3`
- `development_outputs/stage_c0_1_sample_identity/stage_c0_1_duplicate_primary_roots.csv`
  - SHA-256 `c8a3c0e08a8da5d5364e6b954e4e305406c6dcfcaa9e4038e52215625b4c9c9e`

C0.1 handoff provenance:

- GitHub Actions run `33314518877`;
- package commit `35ca555d073142b7accd705b0fdc67051dd251a7`;
- handoff SHA-256 `9d08b94c4452295522a851501acf7fd341f09b4fd79faca7f180f968f1bce423`.

## Active scientific gate: methylation annotation / feature-reduction freeze

No cross-assay methylation result may be calculated yet.

Before Stage C1 starts, the program must prospectively freeze:

1. exact methylation annotation source and immutable version/hash;
2. genome build;
3. probe-to-gene / transcript resolution;
4. multi-gene and multi-transcript handling;
5. promoter / regulatory-region definitions;
6. gene-body and non-promoter handling;
7. unmapped-probe handling;
8. whether modal analysis operates in all-probe space, regulatory strata, or both;
9. any scalar compression and its construction nulls, without calling it chi;
10. conglomeration/module representation across the already closed static layers;
11. missingness and per-cancer eligibility rules;
12. all nulls and promotion criteria before inspecting methylation-RNA/RPPA/genomic relationships.

The required conceptual architecture remains complementary:

- **modal**: mode-resolved/eigenspectrum and participation structure;
- **scalar**: compressed coordinates only where separately licensed;
- **conglomeration**: module-to-module and whole-system organization across independently measured layers.

The scalar view may not replace modal or conglomeration structure. None of these static methylation quantities is biological chi. Static cross-assay association cannot establish substrate inheritance; ordered or temporal evidence remains required.

## Exact user action

No local computation is currently required. The next user decision is scientific rather than mechanical: approve or revise the proposed annotation/regulatory mapping specification after it is presented. Until that freeze is explicit, Stage C1 remains blocked by design.

Keep the 5.02 GB methylation source and existing B2 task caches local and unchanged.
