# Stage C0.1 DNA-methylation sample-identity audit

Date: 2026-08-30

Verdict: **PASS - ONE-TO-ONE SAMPLE IDENTITY CLOSED; METHYLATION BIOLOGICAL ANALYSIS REMAINS NOT STARTED**

## Purpose

Stage C0.1 was prospectively frozen after Stage C0 detected 41 primary TCGA sample roots represented by multiple methylation columns. Its only purpose was to resolve source-to-Stage-A sample identity without reading methylation beta-value rows for biological analysis.

The frozen primary rule was conservative: one Stage A tumor may enter primary C1 only when it maps to exactly one eligible primary-tumor methylation column, with patient fallback allowed only when exactly one eligible primary methylation measurement exists for that patient. Duplicate-root measurements are excluded rather than averaged, selected by order, selected by platform, or selected from methylation values.

## Input lineage

- Stage A profile-cache SHA-256: `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`
- Stage C0 source SHA-256: `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`
- Stage C0 compact-summary SHA-256: `b89e5987e50ddec4ec432a511eeb80052c1ce607dafae8c743eae204354c6bcd`
- C0.1 plan version: `0.1-post-c0-pre-association`

## Header/schema result

The source header reproduced the C0 inventory:

- 12,040 total columns;
- 12,039 methylation sample columns;
- 12,039 parseable TCGA sample roots;
- 10,317 primary-tumor columns;
- 10,271 unique primary sample roots;
- 10,268 unique primary patients;
- 41 duplicated primary sample roots.

Among the 41 duplicate roots, 39 have two source columns, one has three source columns, and one has six source columns. No replicate was selected or averaged for the primary C1 map.

## Stage A one-to-one coverage

Frozen Stage A universe: 9,546 unique-patient primary tumors across 32 cancers.

C0.1 result:

- exact unique-root matches: **9,459**;
- unique patient fallback matches: **1**;
- total one-to-one matched Stage A tumors: **9,460 / 9,546 (99.0991%)**;
- Stage A samples excluded because their root is duplicated in the methylation source: **34**;
- Stage A samples with no eligible source match: **52**;
- total excluded or unmatched: **86 / 9,546 (0.9009%)**;
- cancers passing the frozen `n >= 30` gate: **32 / 32**.

The lowest retained fraction is GBM: 125 / 154 Stage A tumors remain one-to-one matched (81.17%), still well above the preregistered n=30 gate. No cancer threshold was relaxed and no source replicate was rescued to increase coverage.

## Output integrity

Canonical compact outputs:

- `development_outputs/stage_c0_1_sample_identity/STAGE_C0_1_SAMPLE_IDENTITY_SUMMARY.json`
  - SHA-256 `82d885ea8b1674f18bfda8317398b1f1658c383a351d626f4a793e303edb18a4`
- `development_outputs/stage_c0_1_sample_identity/stage_c0_1_unique_match_coverage.csv`
  - SHA-256 `1fd625b7d575995185bc6d6e9f8dfebdc82abbb89afe553dae121c2ce40e3fc3`
- `development_outputs/stage_c0_1_sample_identity/stage_c0_1_duplicate_primary_roots.csv`
  - SHA-256 `c8a3c0e08a8da5d5364e6b954e4e305406c6dcfcaa9e4038e52215625b4c9c9e`

The tested Windows handoff was built by GitHub Actions run `33314518877` from commit `35ca555d073142b7accd705b0fdc67051dd251a7`; artifact SHA-256 `9d08b94c4452295522a851501acf7fd341f09b4fd79faca7f180f968f1bce423`.

## Scientific firewall

C0.1 read only source identity/header information required for mapping. The returned summary explicitly records:

- `beta_value_rows_read_for_biological_analysis = false`;
- `biological_association_performed = false`;
- `chi_present = false`;
- `composite_score_present = false`;
- `substrate_inheritance_claim = false`.

Therefore C0.1 establishes only one-to-one sample identity and coverage. It does not establish a methylation-RNA relationship, regulatory mechanism, causal control, state transition, damping, criticality, treatment response, substrate inheritance, or biological chi.

## Closure

Stage C0.1 is **CLOSED PASS**. The primary downstream methylation cohort is restricted to the 9,460 one-to-one matched Stage A tumors under the frozen mapping rule. The 41 duplicate roots remain visible in the diagnostic ledger and are not silently collapsed.

The next scientific gate is the prospective methylation annotation and feature-reduction freeze. No methylation biological association may be calculated until the exact annotation source/build, gene/transcript and multi-mapping rules, regulatory-region definitions, unmapped handling, feature-reduction architecture, and construction nulls are fixed before results.
