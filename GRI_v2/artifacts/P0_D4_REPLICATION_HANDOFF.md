# P0 D4 REPLICATION execution handoff

Status: READY FOR UNTOUCHED REPLICATION EXECUTION

The D4 scientific/evaluation contract was frozen before any REPLICATION target score was generated:

- `GRI_v2/docs/TOOL_PREDICTION_P0_D4_REPLICATION_FREEZE.md`
- `GRI_v2/docs/TOOL_PREDICTION_P0_D4_PRECOMPUTE_CONCRETIZATION.md`
- `GRI_v2/config/tool_prediction_p0_d4_replication.json`

User-facing package: `GRI_Replication_Check.zip`

Package SHA-256:

`d070d845f2302baaf51e63050cd3e46d44345771eb5867b59a279a5a475f971c`

Package source hashes include:

- `src/run_replication.py`: `f6a02bb39f6cfedb8fd034b0f2ea3f0bb84dddff019c891c20a1725ee73efdbe`
- `src/run_discovery_model.py` frozen helper copy: `b1d98f941599936d9332bd278cce72b4cc7c1784f0028b4baa688df881013e6a`
- `tests/test_replication.py`: `20a512362192bab26f8373ca86212683ea8cb1ac75f32dd9be90403875094b55`

Clean-room verification:

- internal package SHA manifest: PASS
- synthetic/contract tests: 8/8 PASS
- includes a regression test proving a deliberately nonnumeric FINAL-like methylation column is not parsed when only a REPLICATION column is selected.

The package bundles all small frozen dependencies, including D1/D2 transforms, D3 model/composition parameters, split/eligibility manifests, B1 composition covariates, and the compact frozen TSS200 projection map.

The user is asked to select only two reusable large files:

1. the same C0-audited 5.02 GB methylation data file;
2. `hallmark_profile_cache.npz`.

Expected return is exactly one file:

`RETURN_TO_CHAT/Replication_Result.zip`

D4 parses numeric methylation values only for the 1,625 eligible REPLICATION participants, projects frozen D1/D2 features, applies frozen D3 models/composition residualizers, evaluates P1 prediction and P2 audit-state replication, and leaves FINAL_HOLDOUT sealed.

Pre-value metadata closure:

- 1,625 eligible REPLICATION participants across the same 19 cancers;
- 1,478 have both frozen B1 covariates and are eligible for P1 evaluation;
- every cancer retains >=30 complete cases, with PCPG exactly 30;
- no rebalancing or rescue is permitted.
