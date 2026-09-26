# Meneses 2026 depth-conditioned path transport freeze v0.1

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-depth-conditioned-p0q-20260925`  
**Status:** FROZEN BEFORE DEPTH-CONDITIONED OUTPUT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q post-result conditional transport qualification

## Parent result

The immediately preceding frozen path-transport gate found path-dependent four-coordinate motor-response organization across sorbitol, sodium-buffer, and clockwise-motor contexts relative to canonical sucrose/CCW.

Parent result pin:
`BIO_CHI/config/MENESES2026_PATH_TRANSPORT_P0Q_V01_RESULT_PIN.json`.

That result is known. This follow-up cannot count as independent confirmation of path dependence. It asks a new conditional question prospectively: **does path identity still add information once collapse depth is accounted for?**

## Frozen object

Outcome vector:
[
Y=[log(	au_{dec}),log(|	au_{inc}|),recovery_fraction].
]

Depth coordinate:
[
A=A_{dec}.
]

Path categories:
- sucrose/CCW (reference);
- sorbitol/CCW;
- sodium-buffer assay;
- clockwise-locked sucrose.

All per-cell source-method fits are recomputed from the pinned upstream source using the exact path-transport source method. No result table from the parent analysis is used as an input.

## Competing predictive models

### M0: depth-only

For each outcome coordinate independently:
[
Y = eta_0+eta_1 z_A+eta_2 z_A^2.
]

### M1: depth plus path

For each outcome:
[
Y = eta_0+eta_1 z_A+eta_2 z_A^2
+sum_p alpha_p I_p
+sum_p delta_p I_p z_A,
]
where the three nonreference paths receive intercept and linear-depth interaction terms.

No higher-order interaction or post-result feature selection is permitted.

## Cross-validation

Use leave-one-concentration-out cross-validation over 200, 300, 400, and 500 mM.

For each fold:

1. standardize (A) from training cells only;
2. standardize each outcome coordinate from training cells only;
3. fit M0 and M1 by ordinary least squares on training cells;
4. predict all held-out cells at the omitted concentration;
5. compute squared standardized residuals.

Primary metrics:
- total held-out MSE across all cells and all three outcome coordinates;
- per-coordinate held-out MSE;
- fractional improvement
[
I=(MSE_{M0}-MSE_{M1})/MSE_{M0}.
]

## Bootstrap uncertainty

Use 2,000 nonparametric block-bootstrap resamples, seed `20260925`.

Within every path-by-concentration block, resample cells with replacement to the original block size. Re-run the full leave-one-concentration-out pipeline and store fractional improvement (I).

Report the percentile 95% interval.

## Frozen decision rule

- `DEPTH_INSUFFICIENT_PATH_CONTEXT_REQUIRED_P0Q` if:
  - observed fractional improvement >= 0.25; and
  - bootstrap 95% CI lower bound > 0.

- `DEPTH_MEDIATED_REORGANIZATION_P0Q` if:
  - observed fractional improvement <= 0.10; and
  - bootstrap 95% CI upper bound <= 0.10.

- otherwise:
  - `DEPTH_CONDITIONING_UNRESOLVED_P0Q`.

The thresholds are local representation criteria, not universal biological constants.

## Coordinate localization

Per-coordinate improvements are descriptive only. They identify whether collapse timing, removal-recovery timing, or recovery fraction contributes most strongly after conditioning on collapse depth. They do not alter the primary disposition.

## Hierarchy

- **Biological chi:** whole perturbation/recovery relation and its dependence on path context after controlling gross response depth.
- **Chi_bio:** multicoordinate motor response organization.
- **chi_bio:** remains `NOT_OPENED_NOT_LICENSED`; neither collapse amplitude nor source empirical time constants are independently licensed as a universal scalar stability carrier.

## Failure rules

All source-fit failures are preserved. No outlier removal is permitted. If any path-by-dose block has fewer than three valid cells, the analysis returns `SOURCE_LIMITED` rather than changing the model or pooling rule.

## Claim ceiling

Same-source, same-organism, post-result conditional qualification. A positive result would show that path context adds predictive information beyond collapse depth in this dataset. It would not establish a causal mechanism or universal substrate-inheritance law.
