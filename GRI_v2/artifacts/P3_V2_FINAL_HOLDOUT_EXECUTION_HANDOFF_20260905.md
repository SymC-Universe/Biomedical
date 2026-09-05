# P3-v2 FINAL_HOLDOUT execution handoff

Date: 2026-09-05

Status: READY FOR ONE-TIME FINAL_HOLDOUT EXECUTION UNDER THE POST-D4 DEVELOPMENT-INFORMED FREEZE.

Scientific contract:

- `GRI_v2/docs/TOOL_PREDICTION_P3_V2_POST_D4_AMENDMENT_20260905.md`
- `GRI_v2/config/tool_prediction_p3_v2_20260905.json`

P3-v1 categorical selective prediction remains `NOT_EVALUABLE`; this package does not rewrite that result.

User-facing package:

`GRI_Final_Holdout_P3v2.zip`

Package SHA-256:

`07562082dc09a039bbc170127d075cfb51a5bf9ba7534c033af0f6816c082ad0`

Key package source hashes:

- `src/run_final_holdout.py`: `ff554cce5871f56738ce86e308a908aef50f40a34790f38cd1844011aa65a5b7`
- `src/windows_launcher.py`: `ae98b11876fe077fb51c560233ea650491cb77dbaa732205adea7bc565ac0ae0`
- `tests/test_p3_v2.py`: `200efefca79460d07de0b850eb2a0bb3a83c9be438f730661dc2fdff26ada13f`
- `config/p3_v2_execution.json`: `bef548d98b211aa1183c876d1b9b5a04c29b798644b79a0321f57d406a729996`
- `config/p3_v2_science_config.json`: `ef5fce2fb9c26214191f08de9e5722302172747acd9c3e618ac87c96dc4eaa8d`
- `PACKAGE_SHA256SUMS.txt`: `7358066b01d9f99693953595d2fe11a5cba7eee8b50743f52f2a0139bfb94cb4`

Mechanical validation:

- package unit/contract tests: 10/10 PASS;
- clean-room extraction manifest verification: PASS;
- clean-room tests: 10/10 PASS;
- FINAL_HOLDOUT molecular outputs bundled before execution: false;
- projection checkpoints are separate from D4 checkpoints;
- controller retries unexpected hard worker termination up to three attempts;
- no participant reassignment, covariate imputation, model refit, transform refit, composition refit, selector fitting, or final-data threshold fitting is permitted.

Pre-value FINAL_HOLDOUT metadata:

- eligible participants: 1,686;
- composition-complete participants: 1,534;
- primary evaluable cancers under unchanged n>=30 rule: 18;
- PAAD: 26 composition-complete participants, excluded from primary final inference without rescue.

The package uses the exact D4 frozen small inputs plus the exact D4 replication prediction comparison as a development baseline. The user selects only the same two large local files used for D4:

1. the C0-audited 5.02 GB methylation source;
2. `hallmark_profile_cache.npz`.

Expected return:

`RETURN_TO_CHAT/Final_Holdout_Result.zip`

On successful return, the next operation is an independent final audit before interpretation, followed by the component-retention decision and external-validation/C1 sequence as supported by the result.
