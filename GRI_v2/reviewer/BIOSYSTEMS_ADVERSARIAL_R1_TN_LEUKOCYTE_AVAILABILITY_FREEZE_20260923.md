# BioSystems adversarial Round 1 - tumor-normal leukocyte availability audit freeze

**Date:** 23 September 2026
**Status:** FROZEN BEFORE SOURCE AVAILABILITY AUDIT
**Branch:** `biosystems-adversarial-r1-20260923`
**Immutable parent:** `biosystems-resubmission-20260923-final` @ `18b1e3b6c828626143ac37da3fe279dd605751d5`
**Role:** source/metadata qualification only. No RNA or methylation molecular outcome may be read.

## Question

Does the exact frozen PanCanAtlas methylation-derived leukocyte source contain sample-type-11 values with enough coverage to support a symmetric tumor-normal composition sensitivity for the frozen TN-A1/TN-P20 cancer sets?

The existing ABSOLUTE purity source is tumor-defined and is not considered symmetric for type-11 tissue. This gate therefore tests leukocyte availability only.

## Frozen source

- Leukocyte fraction SHA-256: `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`.
- Source matching/barcode conventions are inherited from the existing B1/P0 lineage.
- Sample type 01 = Primary Solid Tumor.
- Sample type 11 = Solid Tissue Normal.

## Frozen cancer sets

TN-A1:
BRCA, COAD, HNSC, KIRC, KIRP, LIHC, LUAD, LUSC, PRAD, STAD, THCA, UCEC.

TN-P20:
BRCA, COAD, HNSC, KICH, KIRC, KIRP, LIHC, LUAD, LUSC, PRAD, STAD, THCA, UCEC.

## Audit outputs

For every cancer and sample type:
- source rows;
- unique participants;
- duplicate participant count;
- finite leukocyte values;
- minimum/median/maximum where present.

Also report participant overlap between type 01 and type 11 within each frozen cancer.

No RNA/methylation value, tumor-normal architecture quantity, Hallmark score or GRI endpoint may be computed.

## Eligibility for a later symmetric sensitivity

A cancer is `LEUK_TN_SYMMETRIC_ELIGIBLE` only when:
- at least 30 unique finite type-01 participants;
- at least 30 unique finite type-11 participants.

A cancer is `LEUK_PAIRED20_ELIGIBLE` only when at least 20 participants have finite leukocyte fraction in both type 01 and type 11.

These thresholds mirror the existing TN-A1 and TN-P20 sample sizes; they are frozen before inspecting RNA architecture by leukocyte strata.

## Disposition

- `SYMMETRIC_LEUKOCYTE_SENSITIVITY_FEASIBLE`
- `PARTIAL_SYMMETRIC_LEUKOCYTE_COVERAGE`
- `NO_SYMMETRIC_LEUKOCYTE_ROUTE`
- `SOURCE_IDENTITY_HOLD`

A later molecular sensitivity requires a separate freeze and cannot be improvised from this source inventory.

## Claim ceiling

This audit cannot remove composition confounding. It only determines whether the one composition variable with a potentially symmetric biological interpretation is actually available in both tissue states.
