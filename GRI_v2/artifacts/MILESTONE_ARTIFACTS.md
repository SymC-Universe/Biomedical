# Milestone artifact registry

Full milestone suites are retained in ChatGPT when useful for clean handoff. GitHub stores their hashes and the reproducible source/config spine.

## 2026-08-29 Cancer Stability Atlas v0.1.1 Stage A1 non-finite hotfix

- File: `CANCER_STABILITY_ATLAS_v0_1_1_A1_NONFINITE_HOTFIX_20260829.zip`
- SHA-256: `9cca6b8c818360ba8f50ac5135ec257f16e439dc4c9cddf5035edfb748bc1d66`
- Role: pre-result Stage A1 execution repair after the exact PanCanAtlas source triggered the non-finite guard before any network statistic was computed. Freezes explicit missing-data handling and adds synthetic missingness regression tests. This supersedes v0.1 only for Stage A1 execution; it does not alter Stage A0 results or the predictive-tool objective.

## 2026-08-26 Cancer Stability Atlas v0.1 development suite

- File: `CANCER_STABILITY_ATLAS_v0_1_DEV_20260826.zip`
- SHA-256: `e9225b5a2cf0484af8ab13a688ecb3529dab40d406a2cadee8031f8f32ae79aa`
- Role: first post-GRI scalar redirection package; contains Stage A0 outputs, initial Stage A1 launcher, configs, tests, archive notes, and epistemic firewall. Its Stage A1 launcher is superseded by v0.1.1 because it halted on source non-finite cells before an explicit missing-data policy existed.

## 2026-08-26 GRI v1.1.6 post-run audit

- File: `GRI_v1_1_6_POSTRUN_AUDIT_20260826.zip`
- SHA-256: `2e62c2b677e4a574e39e74fd419d003854a6304b3cce3249e5203b4957ec493c`
- Role: frozen audit of the historical scalar experiment; retained as the closed `CV/2` branch and not as evidence for the new engine.

## Source result archive used by Stage A0

- File: `GRI_v1_1_results_20260826_182833.zip`
- SHA-256: `8d1f16a7cc3dd5184995b7f26c30ee40cd286b47ad8b62a33935651d8a6a4172`

Any future substantial suite should be added here with filename, SHA-256, date, role, and the Git commit/branch state it corresponds to.
