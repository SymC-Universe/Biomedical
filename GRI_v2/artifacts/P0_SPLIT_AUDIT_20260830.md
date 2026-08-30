# GRI v2 P0 pre-eligibility split audit

**Status:** PASS

Date: 2026-08-30
Branch anchor before audit: `6f2a80e97e151f09cb6d6d6470e0f6f31c8321a5`

## Returned local artifacts

- `P0_SPLIT_MANIFEST_SUMMARY.json` SHA-256: `a9ffd1a5210b7d4f23ad5e2aca2c7f2bb9e01f540df2d912795adb11763a37b2`
- `p0_preeligibility_split_manifest.csv` SHA-256: `12b85d67d06e57c6d1be914444c65aa526f2b821e117725dd036142cc6b0a825`
- `p0_preeligibility_partition_counts.csv` SHA-256: `1bf8d02df15e2ed0b0aebd66330b96e3c275a5eaea3b7f6596d7b421b761a144`

The full manifest is a deterministic local derivative of the frozen P0 split rule and the locked C0.1 matched identity inputs. Its exact hash is recorded above rather than duplicating the 1.4 MB participant-level CSV in the repository.

## Audit checks passed

- summary status: `P0_PREELIGIBILITY_SPLIT_MANIFEST_COMPLETE`
- matched participants: 9,460
- cancers: 32
- partitions: DISCOVERY 5,643; REPLICATION 1,888; FINAL_HOLDOUT 1,929
- all 9,460 participant assignments independently reconstruct from `sha256_first_8_bytes_unsigned_big_endian_mod_10`
- no duplicate participant roots
- no duplicate methylation sample roots among retained matched records
- returned manifest hash matches summary
- returned partition-count hash matches summary
- methylation source SHA-256 remains `5934c497882fbe8178d128a3a7f71e765480af6bbd460e0398de3428cd075b77`
- Stage A Hallmark/RNA cache SHA-256 remains `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`
- `methylation_rows_read = false`
- `beta_value_rows_read_for_biological_analysis = false`
- `predictive_target_values_read = false`
- `partition_reassignment_performed = false`
- `biological_chi_used = false`
- `stage_c1_science_modified = false`

## Frozen-rule consequence observed before eligibility

Under the already-frozen requirement that a cancer retain at least 30 eligible participants independently in DISCOVERY, REPLICATION, and FINAL_HOLDOUT, no more than 19 of the 32 cancers can be fully evaluable from this fixed split even before the 95% finite-probe eligibility screen. Therefore the frozen P0 pan-cancer promotion floor of 24 fully evaluable cancers is unreachable in P0.

This is recorded as a pre-result design consequence, not repaired post hoc. The split is not regenerated, the per-partition minimum is not changed, and the 24-cancer promotion floor is not changed. Cancer-level P0 evaluation may proceed where eligible; any pan-cancer aggregate under this P0 version is descriptive only.

## Next gate

Proceed to the frozen per-sample eligibility screen and DISCOVERY-only preprocessing. No REPLICATION or FINAL_HOLDOUT target values may be used to select probes, imputation values, centering/scaling, Hallmark feature eligibility, PC1 loadings/orientations, ridge hyperparameters, or audit-state thresholds.
