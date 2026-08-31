# P0 D4 REPLICATION execution handoff

Status: READY FOR UNTOUCHED REPLICATION EXECUTION AFTER MECHANICAL WINDOWS COMPATIBILITY REPAIR

The D4 scientific/evaluation contract was frozen before any REPLICATION target score was generated:

- `GRI_v2/docs/TOOL_PREDICTION_P0_D4_REPLICATION_FREEZE.md`
- `GRI_v2/docs/TOOL_PREDICTION_P0_D4_PRECOMPUTE_CONCRETIZATION.md`
- `GRI_v2/config/tool_prediction_p0_d4_replication.json`

The first two Windows attempts did not produce a REPLICATION result. The first exposed a launcher-visibility defect. The second exposed a pandas Copy-on-Write compatibility defect before methylation projection completed:

`ValueError: assignment destination is read-only`

The failure occurred when applying the already-frozen DISCOVERY imputation medians to a NumPy view returned by pandas. It is mechanical only. No REPLICATION scientific result was generated and FINAL_HOLDOUT remains sealed.

The repaired user-facing package is:

`GRI_Replication_Check_Repair.zip`

Package SHA-256:

`903e5c438a0575067edd667bd1aaee772c6b4e67c2d04ae7dd38d647463876ad`

Repaired package source hashes:

- `src/run_replication.py`: `6fbc7b674a41e1ca2817297e13a25313019cdea9b85823d28425f8ce632d0002`
- `src/run_discovery_model.py` frozen helper copy: `9725c6c6f90b5570cfafb469586526ad49e5cbd66b4b25f646a143e4b7c5bea7`
- `tests/test_replication.py`: `93bc51bade91511df745ed61c62a80d511d5e51a662bb61ff401742e81a1d508`

Mechanical changes only:

1. methylation projection explicitly materializes a writable NumPy copy before applying the unchanged frozen DISCOVERY imputation medians;
2. rank normalization likewise materializes a writable copy before its existing in-place centering operation, preventing the same pandas Copy-on-Write failure later in the D4 audit;
3. no formula, threshold, split, transform, model parameter, null count, seed namespace, covariate rule, state rule, or interpretation changed.

Regression protection:

- clean-room package integrity: PASS;
- contract/regression tests: 10/10 PASS;
- includes the existing FINAL-like-column leakage test;
- adds a regression test reproducing the read-only methylation NumPy view under pandas Copy-on-Write;
- adds a second regression test for the same compatibility condition in rank normalization.

The package bundles all small frozen dependencies, including D1/D2 transforms, D3 model/composition parameters, split/eligibility manifests, B1 composition covariates, and the compact frozen TSS200 projection map.

The user selects only two reusable large files:

1. the same C0-audited 5.02 GB methylation data file;
2. `hallmark_profile_cache.npz`.

Expected return is exactly one file:

`RETURN_TO_CHAT/Replication_Result.zip`

D4 parses numeric methylation values only for the 1,625 eligible REPLICATION participants, projects frozen D1/D2 features, applies frozen D3 models/composition residualizers, evaluates P1 prediction and P2 audit-state replication, and leaves FINAL_HOLDOUT sealed.

Pre-value metadata closure remains unchanged:

- 1,625 eligible REPLICATION participants across the same 19 cancers;
- 1,478 have both frozen B1 covariates and are eligible for P1 evaluation;
- every cancer retains >=30 complete cases, with PCPG exactly 30;
- no rebalancing or rescue is permitted.
