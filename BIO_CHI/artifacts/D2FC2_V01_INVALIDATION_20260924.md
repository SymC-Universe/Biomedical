# D2FC2 independent modal v0.1 invalidation

**Date:** 24 September 2026
**Status:** INVALID_TEST_SOURCE_PARTITION
**Scientific result reviewed before invalidation:** NO

The v0.1 freeze inherited the fitting/validation row grouping used by the repository convenience script `RunAverageIKKTrajectory.m`: rows 1-4 as fitting and rows 5-9 as validation.

Before any v0.1 scientific result was retrieved or inspected, the peer-reviewed Nature Communications article was checked. The publication states that the four optimization conditions were **Control, 1x6 min, 1x30 min, and 4x1.5 min**. The other five mean conditions were validation data not used for PSO.

That published partition conflicts with the row-based plotting grouping in the repository script. Under the GOM, the publication-defined training/validation lineage controls the scientific independence claim. The v0.1 test is therefore invalidated before result review.

Runs associated with the invalid v0.1 path:
- `36031923478`: mechanical path-resolution failure before analysis.
- `36032366722`: launched after path repair under the still-incorrect source-partition freeze. Its scientific output, if any, is not to be used for admission or threshold changes.

No threshold, pair-selection rule, scalar definition, or expected result is altered in response to outcome. v0.2 changes only the source-native partition to match the peer-reviewed publication and addresses conditions by name rather than row number.

This invalidation preserves the evidence-blind timing of the correction: the discrepancy was identified from the publication, not from the v0.1 result.
