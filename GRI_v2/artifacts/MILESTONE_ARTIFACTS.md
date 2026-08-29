# Milestone artifact registry

Full milestone suites are retained in ChatGPT when useful for clean handoff. GitHub stores hashes and the reproducible source/config spine.

## 2026-08-29 Stage A1.1 Windows launcher hotfix

- File: `CSA_A1_1_CALIBRATION_WINDOWS_HOTFIX_20260829.zip`
- SHA-256: `56416dc9d8025ddb31da200dd3c75049b89c587b42ae79c51d9d6905c350690f`
- Role: execution-only replacement for the original A1.1 handoff after Windows `cmd.exe` mangled the nested `for /f` file-picker quoting before either input file was selected. Calibration specification and scientific code are unchanged. The repaired launcher uses a temporary-file path handoff and adds a regression test forbidding the failed quoting pattern.

## 2026-08-29 Stage A1.1 fixed-n calibration runner

- File: `CSA_A1_1_CALIBRATION_20260829.zip`
- SHA-256: `7b27ced053d5cb83fc68b17005fa6075619be5ee9c22e520bc637f30c77145d0`
- Role: original compact post-A1/pre-calibration handoff. Superseded for Windows execution by the launcher hotfix above. Uses only the completed A1 cache and membership snapshot; does not reread the 1.88 GB source matrix. Performs the frozen n=30, 100-resample construction calibration with no chi, CV/2, or composite stability score.

## 2026-08-29 Cancer Stability Atlas v0.1.1 Stage A1 non-finite hotfix

- File: `CANCER_STABILITY_ATLAS_v0_1_1_A1_NONFINITE_HOTFIX_20260829.zip`
- SHA-256: `9cca6b8c818360ba8f50ac5135ec257f16e439dc4c9cddf5035edfb748bc1d66`
- Role: pre-result Stage A1 execution repair after the exact PanCanAtlas source triggered the non-finite guard before any network statistic was computed. Freezes explicit missing-data handling and adds synthetic missingness regression tests.

## 2026-08-26 Cancer Stability Atlas v0.1 development suite

- File: `CANCER_STABILITY_ATLAS_v0_1_DEV_20260826.zip`
- SHA-256: `e9225b5a2cf0484af8ab13a688ecb3529dab40d406a2cadee8031f8f32ae79aa`

## 2026-08-26 GRI v1.1.6 post-run audit

- File: `GRI_v1_1_6_POSTRUN_AUDIT_20260826.zip`
- SHA-256: `2e62c2b677e4a574e39e74fd419d003854a6304b3cce3249e5203b4957ec493c`

## Source result archive used by Stage A0

- File: `GRI_v1_1_results_20260826_182833.zip`
- SHA-256: `8d1f16a7cc3dd5184995b7f26c30ee40cd286b47ad8b62a33935651d8a6a4172`
