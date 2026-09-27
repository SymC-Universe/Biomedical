# Stentor cross-system replicate-unit amendment v0.1

**Date:** 26 September 2026  
**Status:** PROSPECTIVE AMENDMENT BEFORE SYMC-SPECIFIC OUTCOME INSPECTION  
**Parent freeze:** `BIO_CHI/control/STENTOR2026_CROSS_SYSTEM_PATH_P0Q_FREEZE_v0_1.md`  
**Authority:** SymC GOM v0.8.6

## Trigger

Source-code inspection shows that each condition's `control_data` matrix is constructed by pooling eligible cells across multiple source experimental folders, then sampling responder/nonresponder columns from that pooled matrix. The source retains `nums_filt`, `folders`, `responders_inds`, and `nonresponders_inds`, allowing the sampled cells to be mapped back to their originating experiment.

A cell-level permutation test would therefore treat nested cells as independent inferential units and could overstate evidence if source-run structure is present.

No Stentor SymC-specific output had been inspected when this amendment was written.

## Amendment

The primary cross-system classifier is changed from cell-level vectors to **source-run median vectors**.

For each condition:

1. preserve the source-controlled cell sample exactly;
2. reconstruct the originating source-run index for every selected cell using the pooled-column indices `responders_inds` then `nonresponders_inds` and the cumulative per-run counts in `nums_filt`;
3. calculate the four frozen cell coordinates unchanged;
4. aggregate eligible selected cells to the median coordinate vector for each source run represented in the source-controlled sample.

A source run represented by at least one source-controlled eligible cell is retained. No minimum cell count is imposed after seeing outcomes; the number of selected cells contributing to each run median is recorded.

## Revised primary test

Treat source-run medians as the independent analysis units.

The frozen leave-one-ITI-out classifier, training-fold standardization, multinomial logistic model, and 2,000 concentration-stratified/path-label permutation procedure remain otherwise unchanged.

Within each ITI, ISI labels are permuted across source-run median vectors, not across individual cells.

The primary decision labels remain:

- `CROSS_SYSTEM_PATH_ORGANIZATION_DETECTED_P0Q`
- `CROSS_SYSTEM_PATH_ORGANIZATION_NOT_DETECTED_P0Q`.

The recovery-only control is also run at source-run level and retains the same exhaustive four-way secondary taxonomy.

## Cell-level result

The originally specified cell-level classifier may still be computed as a **descriptive nested-cell sensitivity**. It has no promotion rights and cannot rescue a failed source-run primary gate.

## Representation adequacy

The 12-condition median PCA test remains unchanged because its unit is already the condition, not the individual cell.

## Failure rule

If the source-controlled indices cannot be mapped unambiguously back to `nums_filt`/source folders, the primary gate returns `SOURCE_RUN_MAPPING_FAILED`; it will not fall back to cell-level inference.

## Claim ceiling

This amendment strengthens the experimental-unit discipline. It does not change the four biological coordinates, the source conditions, or any scientific threshold after result inspection.
