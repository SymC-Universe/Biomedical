# F2 pre-result protocol repair: autonomy permutation resolution

**STATUS: FROZEN BEFORE ANY REPLICATED F2 SWEEP OUTPUT**

Date: 2026-08-30

This note repairs one mathematical inconsistency in `TOOL_FEASIBILITY_F2_EVALUATION_FREEZE_20260830.md` before the replicated F2 sweep is generated.

The freeze specified 12 autonomy-calibration patient-row permutations while S11 also requires an empirical permutation-significance decision at the conventional 0.05 boundary. With 12 permutations, the smallest possible corrected empirical p-value is `1/13 ~= 0.0769`, so the criterion cannot be evaluated as written.

## Repair

For the replicated F2 sweep only:

- autonomy calibration uses **19 deterministic patient-row permutations**;
- empirical one-sided p-value is `(1 + count(null >= observed)) / 20`;
- minimum attainable p-value is therefore `0.05`;
- `p <= 0.05` is the significance rule used where S11 refers to empirical permutation significance.

All other F2 scenario definitions, signal/noise settings, global CKA null count (39), semantic-label null count (39), effect thresholds, pass-rate thresholds, safety scenarios, autonomy formula, and GO/NARROW/STOP policy remain unchanged.

No F2 replicated sweep artifact or scenario result existed when this repair was made. This note is a pre-result protocol correction and may not be altered to rescue later F2 outcomes.
