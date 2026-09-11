# NSD P0Q1 Rank-Signal Prospective Qualification

Date: 2026-09-10/11
Status: **FROZEN P0 PROSPECTIVE QUALIFICATION. NOT P1.**

The candidate rule in `configs/P0Q1_RANK_SIGNAL_FREEZE.json` was derived only after inspection of the earlier structured/null P0 development stress and is therefore explicitly `DATA_DERIVED_POST_RESULT` under promotion debt `NSD-DEBT-004`.

## Candidate rule under challenge

For SSI-COV and Subspace DMD independently:

1. sweep the frozen candidate grid;
2. identify the rank with the largest finite adjacent singular-value ratio;
3. refuse if that rank is the grid maximum;
4. refuse if the maximum gap ratio is below `3.0`;
5. refuse if any selected pole is unstable;
6. refuse if the selected model contains no stable positive-frequency complex mode above `0.25 Hz`;
7. otherwise return `ADMIT_RANK_SIGNAL`.

This is intentionally a **small claim**. `ADMIT_RANK_SIGNAL` means only that the record contains enough data-only evidence for an oscillatory rank candidate to survive this gate. It does not mean the selected modes are physically correct, the model is adequate, the system is stationary, the comparator is superior, or the record has a neural phenotype.

## Untouched P0Q1 challenge

The freeze changes the development distribution before execution:

- 8 observed channels rather than 6;
- new seed base;
- new oscillatory frequencies and decay rates;
- one-, two-, and three-mode systems;
- stronger white and colored sensor noise;
- a weaker second observable mode;
- closer crowding;
- condition number 50;
- AR backgrounds at rho 0.6 and 0.95;
- new 1/f exponents 0.7, 1.4 and 2.3;
- a real-pole-only linear control.

Five independent replicates are frozen per family.

## Prospective survival rule

A method survives P0Q1 only if:

- there are zero mechanical exceptions;
- every oscillatory family admits at least 4/5 records;
- every refusal family has zero false admissions.

The weak-observability family is **not** required to recover latent order 4. Admission at lower observable rank is acceptable.

If the candidate fails, the failure is preserved. The rule may not be retuned on P0Q1 records. Any revision is a new version requiring new untouched qualification evidence.

Success would pay only the first prospective installment on `NSD-DEBT-004`; it would not authorize P1 or EEG.
