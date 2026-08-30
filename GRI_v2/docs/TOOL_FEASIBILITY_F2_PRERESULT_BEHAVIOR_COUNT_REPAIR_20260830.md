# F2 pre-result protocol repair: scored behavior count

**STATUS: FROZEN BEFORE ANY REPLICATED F2 SWEEP OUTPUT**

Date: 2026-08-30

`TOOL_FEASIBILITY_F2_EVALUATION_FREEZE_20260830.md` lists 12 scenario IDs (`S0` through `S11`) but explicitly combines S9 and S10 into one paired autonomy-ordering behavior. Therefore the actual number of scored F2 behaviors is 11, not 12.

This note repairs that bookkeeping inconsistency before any replicated F2 sweep result exists.

## Correct scored behaviors

1. S0 independent
2. S1 one shared mode
3. S2 shared plus private modes
4. S3 measured confounder only
5. S4 global shared / labels scrambled
6. S5 module-specific / weak global
7. S6 technical false concordance
8. S7 feature imbalance / controlled missingness
9. S8 nonlinear-only outside linear scope
10. paired S9/S10 high-autonomy versus low-autonomy behavior, including the requirement that both retain detectable global sharing
11. S11 confounded false autonomy loss

## Correct F2 gate interpretation

### `F2_GO_CANDIDATE`

- mandatory safety scenarios S0, S3, S6, and S11 all pass; and
- at least **10 of the 11** scored behaviors pass.

This is stricter proportionally than the mistaken `10 of 12` wording and therefore does not loosen the gate.

### `F2_NARROW_CANDIDATE`

- all mandatory safety scenarios pass; and
- **7 to 9 of 11** scored behaviors pass.

### `F2_STOP_SIGNAL`

- any mandatory safety scenario fails; or
- fewer than **7 of 11** scored behaviors pass.

All scenario truth definitions, metric thresholds, pass-rate thresholds, null counts as repaired in the separate permutation-resolution note, autonomy formula, and safety design remain unchanged.
