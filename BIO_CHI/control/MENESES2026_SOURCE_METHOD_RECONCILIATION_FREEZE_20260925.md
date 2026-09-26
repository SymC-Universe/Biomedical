# Meneses 2026 source-method reconciliation freeze

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-pmf-recovery-p0q-20260925`  
**Status:** FROZEN BEFORE RECONCILIATION OUTPUT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** POST-RESULT SOURCE-METHOD RECONCILIATION / CANNOT RETROACTIVELY PROMOTE PRIMARY P0-Q

## Trigger

The frozen P0-Q implementation used the general four-parameter motor-fit form present in `code/bead-assay/bead_shock_curve_fits.ipynb`. After the repaired frozen run had completed, a source-lineage audit identified that the current manuscript Methods and the manuscript-facing `code/bead-assay/sucrose_shock_analysis.ipynb` use a more constrained source lane for the immediate sucrose shock.

This is a source-method ambiguity, not permission to rewrite the frozen primary analysis. The primary run and its implementation audit remain preserved.

## Pinned upstream source

Repository: `wadhwalab/2026-Meneses-Osmotic`  
Commit: `d14d0caaa07299f13d1b1121d1e4630454fd724b`

Relevant source files:

- `manuscript/manuscript.tex` blob `d7f6f03c355854b3feb0fe7b7cad8383ee5469a1`
- `code/bead-assay/sucrose_shock_analysis.ipynb` blob `d4408e419e7836876019215672a6ecaf6acc2012`
- `code/bead-assay/adaptation_curve_fitting.ipynb` blob `86f8ce55d39681e769b6b3390e11c95da6359ac8`

## Manuscript-facing immediate-motor lane

For each trace:

1. normalize speed by its mean for `time <= 180 s`;
2. define `speed_initial` as the mean normalized speed from 155--175 s;
3. define `speed_final` as the mean normalized speed from 215--235 s;
4. set collapse amplitude `A_dec = speed_initial - speed_final` and `C_dec = speed_final`;
5. fit only `tau_dec` and `t0_dec` on 175--240 s using
   [
   S(t)=\frac{A_{dec}}{1+\exp((t-175-t_0)/\tau_{dec})}+C_{dec},
   ]
   with initial values `[10,10]` and bounds `(0,+inf)`;
6. define `speed_increase_min` as the mean from 240--260 s and `speed_increase_max` as the mean from 330--350 s;
7. fit `tau_inc,t0_inc` on `time > 250 s and <=360 s` using the source logistic recovery form and source initial values `[3,-10]`.

The sustained-adaptation, TMRM, and cell-area lanes remain unchanged from the frozen primary implementation.

## Frozen reconciliation tests

No thresholds are changed.

- Recompute the condition medians for `A_dec`, `tau_dec`, `tau_inc`, sustained `tau_adapt`, and sustained plateau.
- Reapply the original frozen rate-depth rule exactly.
- Rebuild the same nine-coordinate condition matrix and reapply the original one-dimensional adequacy rule exactly.
- Preserve `chi_bio = NOT_OPENED_NOT_LICENSED`; the source fit parameters remain empirical response summaries, not mechanistic modal carriers.
- Compare the reconciliation result with the frozen primary result.

## Decision rule

- If the primary multicoordinate `Chi_bio` conclusion survives, label it `SOURCE_METHOD_ROBUST_AT_P0Q`.
- If it changes, label the representation result `SOURCE_METHOD_SENSITIVE_P0Q`.
- The reconciliation cannot turn a failed frozen rate-depth rule into prospective support. Any change in that rule is descriptive sensitivity only.
- Bio Chi whole-event admission remains governed by source reproduction, not by which source fitting parameterization yields a preferred lower-level result.

## Claim ceiling

This reconciliation addresses implementation fidelity only. It is post-result, literature-open, and incapable of upgrading the evidence tier.
