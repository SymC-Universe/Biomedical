# P0 D1 DISCOVERY-only source-preprocessing handoff

Date: 2026-08-30

Status: **READY FOR LOCAL REAL-DATA EXECUTION**

Upstream gate: `P0_ELIGIBILITY_AUDIT_20260830.md` = PASS.

Frozen D1 protocol: `TOOL_PREDICTION_P0_D1_DISCOVERY_SOURCE_FREEZE_20260830.md`.

## Local handoff package

Package name:

`GRI_V2_P0_D1_DISCOVERY_SOURCE_WINDOWS_20260830.zip`

Verified archive SHA-256:

`bd49e6a9f68019d3dfed25ba72b79ce1bb49bea8fd3b02fb68b54ef6d6cac9d6`

The package was built with:

- the audited P0 eligibility summary, sample-level eligibility file, and partition-count file;
- the exact frozen C1A portable annotation export;
- the exact frozen Chen cross-reactive probe-ID export;
- the D1 machine-readable freeze;
- the D1 discovery-only engine and Windows wrapper;
- package-integrity verification;
- synthetic leakage/refusal regression tests.

## Independent package verification

A clean-room extraction was performed after archive creation.

- internal `SHA256SUMS.txt`: **PASS**, 15 files
- D1 tests: **4/4 PASS**
- synthetic integration explicitly changes held-out methylation cells to different nonnumeric sentinels while keeping DISCOVERY fixed; all discovery-derived outputs remain identical, demonstrating that D1 does not parse or use held-out methylation columns.
- zero-variance PC1 behavior is tested as refusal / `NOT_EVALUABLE` rather than replacement.

## User-local inputs

The package intentionally asks for exactly two existing local sources:

1. the already-audited 5.02 GB methylation TSV;
2. the exact Stage-A Hallmark membership snapshot `.gmt`.

The Hallmark file is hash-gated to:

`bc6a9a33d7421dc407d33a66859760ba25e47b2f398e1a43c9156f80c71b3900`

The Stage A RNA cache is deliberately **not** requested by D1 because real RNA predictive target values remain unopened at this gate.

## Expected returned artifact

The Windows wrapper creates one upload artifact:

`P0_D1_DISCOVERY_SOURCE_PREPROCESS_RESULTS.zip`

It contains the D1 summary, probe-retention/imputation map, Hallmark eligibility table, discovery-fitted methylation PC1 transforms, discovery methylation PC1 scores, and checksums.

## Claim ceiling

This handoff licenses DISCOVERY-only methylation source preprocessing only. It does not license cross-layer prediction, replication, final-holdout evaluation, biological chi, clinical, causal, temporal, or pan-cancer promotion claims.
