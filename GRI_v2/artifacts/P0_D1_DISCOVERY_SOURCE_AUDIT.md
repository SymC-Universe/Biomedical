# P0 D1 discovery source audit

Status: **CLOSED PASS**

This audit closes the prospectively frozen P0 D1 DISCOVERY-only methylation source-preprocessing gate. It does not promote any biological, cross-layer, predictive, clinical, temporal, causal, or pan-cancer claim.

## Returned artifact integrity

All five returned result artifacts match the run-generated SHA-256 manifest exactly:

- `P0_D1_DISCOVERY_SOURCE_PREPROCESS_SUMMARY.json`: `5be2c44fe1472eda58a77a8c5b1ae54ff25a310621badb1822483a3179337be9`
- `p0_d1_probe_eligibility.csv.gz`: `150d4dcfea6a7ad6696fea3ddae548511bcf4c6337d93cef2467cd4d93034666`
- `p0_d1_hallmark_eligibility.csv`: `3a50c347f5713ca1415c18573736f6ba75a7ae6f347aa62709ae04be8682ab69`
- `p0_d1_methylation_pc1_transforms.csv.gz`: `b85010e31f4506abdf3a77b4a7090d7ea1709808f45040435c26a0edce4236d8`
- `p0_d1_methylation_discovery_scores.csv.gz`: `593d565085b797e8abfcf22c56b406c96edbdba59eac48fb57db62c90ffabed3`

## Frozen identity and scope checks

- Exact methylation source SHA-256 retained: `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`.
- Exact Hallmark membership SHA-256 retained: `bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`.
- 19/19 previously frozen fully evaluable cancers are present and no other cancer is introduced.
- DISCOVERY participants processed: 4,863 exactly.
- Source probe rows: 22,601 exactly.
- Returned guards state that methylation values were read from DISCOVERY only; REPLICATION and FINAL_HOLDOUT methylation values were not read.
- RNA expression/target values were not read.
- No partition reassignment, biological chi, or Stage C1 science modification occurred.

## Probe preprocessing reconstruction

The probe table contains exactly `22,601 x 19 = 429,419` cancer-probe rows.

Independent reconstruction found:

- zero duplicate `(cancer_type, probe_id)` rows;
- discovery sample count is constant within cancer and sums to 4,863 across the 19 cancers;
- zero mismatches against the frozen retention rule `finite_n >= ceil(0.95 * discovery_n)`;
- all retained-probe DISCOVERY imputation medians are finite;
- zero mismatches in `MASKED_TECHNICAL = retained_PRIMARY and not technical_mask_union`;
- exactly 579 technical-mask probes in every cancer;
- exactly 3,999 TSS200-mapped source probes in every cancer.

The returned source-bound C1A counts remain exactly: 22,601 annotated source probes, 524 Chen cross-reactive probes, 59 common-SNP probes, 579 union-mask probes, and 3,999 TSS200 probes.

## Hallmark mapping and refusal reconstruction

The Hallmark table contains exactly `50 x 19 x 2 = 1,900` cancer/track/Hallmark rows across `PRIMARY_PUBLICATION` and `MASKED_TECHNICAL`.

Independent reconstruction found:

- zero duplicate cancer/track/Hallmark rows;
- zero mismatches against the frozen mapping rule `mapped_gene_count >= 10 and contributing_probe_count >= 10`;
- exactly 45 mapping-eligible Hallmarks in every cancer and technical track;
- all 45 mapping-eligible Hallmarks are PC1-evaluable;
- no mapping-ineligible Hallmark receives a PC1;
- no mapping-eligible Hallmark required the pre-result undefined-PC1 refusal rule.

The same five Hallmarks fail the mapping floor in every cancer/track and remain explicitly refused rather than rescued:

- `HALLMARK_ANGIOGENESIS`: 9 mapped genes / 9 contributing probes;
- `HALLMARK_HEDGEHOG_SIGNALING`: 6 / 6;
- `HALLMARK_NOTCH_SIGNALING`: 6 / 6;
- `HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY`: 5 / 5;
- `HALLMARK_WNT_BETA_CATENIN_SIGNALING`: 7 mapped genes / 8 contributing probes.

## PC1 transform and score audit

- Transform groups: exactly `19 x 2 x 45 = 1,710`.
- Every transform group has the same gene count as its Hallmark mapping record.
- No mapping-ineligible Hallmark has a transform.
- All discovery gene means, loadings, and explained-variance fractions are finite.
- Explained-variance fractions lie in `(0, 1]`, observed range approximately `0.14159` to `0.92579`.
- Every loading vector has squared L2 norm 1 to floating-point precision; maximum absolute deviation from 1 was approximately `3.33e-15`.
- All transforms use the frozen orientation method `NONNEGATIVE_CORRELATION_WITH_DISCOVERY_MODULE_MEAN`.
- Discovery score rows: exactly 437,670 = `4,863 participants x 2 tracks x 45 Hallmarks`.
- Zero duplicate `(cancer, participant, track, Hallmark)` score rows.
- All 437,670 PC1 scores are finite.
- Participant sets are identical across all 45 Hallmarks and both tracks within each cancer.
- Every score group has exactly the frozen cancer-specific DISCOVERY participant count.
- Discovery PC1 group means are numerically zero as required by discovery centering; maximum absolute group mean was approximately `7.81e-16`.

## Decision

**D1 PASS.** The source-side methylation preprocessing is mechanically and prospectively coherent under the frozen P0 rules. D1 establishes only a leakage-controlled DISCOVERY source representation. It does not establish cross-layer association or predictive performance.

The frozen P0 pan-cancer promotion floor remains unreachable because only 19 cancers are fully evaluable; all later pan-cancer P0 summaries therefore remain descriptive.

## Next gate

Freeze and regression-test the RNA DISCOVERY target construction before reading real RNA target values, then implement the discovery-only audit and model architecture before any REPLICATION or FINAL_HOLDOUT target evaluation.
