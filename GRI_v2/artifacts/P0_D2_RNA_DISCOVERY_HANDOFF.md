# P0 D2 RNA DISCOVERY target handoff

Status: READY FOR LOCAL EXECUTION

D1 is closed PASS. D2 target-construction rules were frozen before real P0 RNA target values were constructed.

## Tested repository implementation

- Freeze: `GRI_v2/docs/TOOL_PREDICTION_P0_D2_RNA_DISCOVERY_TARGET_FREEZE.md`
- Config: `GRI_v2/config/tool_prediction_p0_d2_rna_target.json`
- Engine: `GRI_v2/src/run_tool_prediction_p0_d2_rna_target.py`
- Regression tests: `GRI_v2/tests/test_tool_prediction_p0_d2_rna_target.py`
- CI run: `33350553379`
- CI conclusion: SUCCESS
- Tested code commit: `a520d3cae7c7dc0386b7c137db2ed999ea5179ea`

The regression suite includes an explicit held-out mutation test: changing non-DISCOVERY RNA values by an extreme amount cannot change the D2 DISCOVERY eligibility, transforms, scores, or common-Hallmark inventory.

## User-facing handoff

- File: `GRI_RNA_Discovery_Targets.zip`
- SHA-256: `298a56e678812f5f82c13c81773873d08224cae8f01c2058a7845fb3fbea195a`
- User entry point: `START_HERE.bat`
- Instructions: `README_FIRST.txt`
- Required user-selected reusable inputs:
  1. exact Stage A `hallmark_profile_cache.npz`;
  2. exact Hallmark membership GMT, user-friendly local name `hallmark_membership_snapshot.gmt`.
- Bundled audited prior-step inputs:
  - `REUSE/Discovery_Methylation_Scores.csv.gz`;
  - `REUSE/Hallmark_Eligibility.csv`.
- Return artifact: `RETURN_TO_CHAT/RNA_Discovery_Targets_Result.zip`.

The handoff follows `PROGRAM_FILE_ORGANIZATION_PROTOCOL.md`: short user-facing names and one explicit return ZIP; technical provenance remains inside the frozen config, repository, and result manifest.

## Claim ceiling

D2 constructs DISCOVERY-only RNA targets. It does not generate or evaluate REPLICATION or FINAL_HOLDOUT target scores and cannot establish prediction, replication, selective prediction, biological mechanism, clinical utility, biological chi, or pan-cancer promotion.
