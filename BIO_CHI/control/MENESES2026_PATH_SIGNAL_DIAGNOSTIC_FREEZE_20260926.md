# Meneses 2026 path-signal post-result diagnostic freeze v0.1

**Date:** 26 September 2026  
**Branch:** `bio-chi-meneses-path-transport-p0q-20260926`  
**Classification:** POST-RESULT ROOT-CAUSE / FEATURE-ABLATION DIAGNOSTIC  
**Authority:** SymC GOM v0.8.6  
**Primary parent:** `MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json`

## Trigger

The prospective primary gate detected perturbation-path reorganization in the four-coordinate recovery vector, while collapse depth alone did not pass its frozen detection threshold. The observed full-minus-depth balanced-accuracy increment was 0.0879, below the prespecified 0.10 threshold, and the freeze did not assign a named secondary class to the realized combination "full detects, depth does not, increment <0.10."

This diagnostic investigates that edge case without changing it.

## Evidence rule

All outputs are post-result explanatory diagnostics. They:

- cannot promote the primary evidence class;
- cannot rename the frozen secondary disposition;
- cannot be used to adjust the 0.10 threshold;
- cannot delete cells or redefine the four primary coordinates.

## Frozen feature diagnostics

Using the same 143 eligible cells and same leave-one-concentration-out logistic classifier:

Single-coordinate lanes:
1. `A_dec`
2. `log_tau_dec`
3. `log_tau_inc`
4. `G_rec`

Leave-one-coordinate-out lanes:
1. all except `A_dec`
2. all except `log_tau_dec`
3. all except `log_tau_inc`
4. all except `G_rec`

Each lane uses a 1,000-replicate concentration-stratified label-permutation null with fixed seed 20261027.

## Frozen pairwise diagnostics

For all six path pairs, run the full four-coordinate classifier under leave-one-concentration-out validation with a 1,000-replicate concentration-stratified permutation null.

Pairs:

- sucrose vs sorbitol
- sucrose vs sodium/buffer context
- sucrose vs clockwise
- sorbitol vs sodium/buffer context
- sorbitol vs clockwise
- sodium/buffer context vs clockwise

Report nominal upper-tail permutation values and Benjamini-Hochberg adjusted values across the six pairwise tests.

## Interpretation ceiling

The diagnostic may identify where the already-detected path signal is concentrated. It cannot establish causal mechanisms, equivalence, a new representation class, or scalar `chi_bio`.
