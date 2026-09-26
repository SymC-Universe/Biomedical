# E. coli sensory representation test specification v0.1

**Date frozen:** 25 September 2026  
**Branch:** `bio-chi-ecoli-sensory-p0q-20260925`  
**Status:** FROZEN BEFORE RAW OUTCOME EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Parent freeze:** `BIO_CHI/config/ECOLI2024_SENSORY_TOPDOWN_P0Q_FREEZE_v0_1.json`

## Purpose

This specification fixes the quantitative comparison that will decide whether the frozen whole-event representation requires background-specific distribution width in addition to background-specific central sensitivity. It does not license a dynamical `chi_bio`.

## Source-native cell observable

For each cell and each of five stimulus levels:

1. preserve the first seven source responses at that level;
2. define the pre-stimulus and post-stimulus masks exactly from the source stimulus vector;
3. exclude the first two post-stimulus frames, matching `badBefore=0` and `badAfter=1`;
4. compute the median pre-stimulus value and median post-stimulus value for each response;
5. define `a0` as the median of all pre-stimulus response medians across the five levels;
6. exclude cells with `a0 < 0.15`;
7. define the cell-level normalized post-stimulus activity at each level as the median of its seven post-stimulus medians divided by `a0`.

For each concentration, the empirical CDF count is the number of retained cells whose normalized post-stimulus activity is below 0.5. This reproduces the source code's decision object without requiring the plotting or MCMC layer.

## Distribution model

For background `b` and total ligand concentration `L`:

[
p_b(L)=Phileft(rac{ln L-mu_b}{sigma_b}ight),
]

where `p_b(L)` is the probability that the source CDF event is true, `mu_b` is the log-location of the sensitivity distribution, and `sigma_b>0` is its log-scale.

The likelihood is binomial at the concentration/FOV level, retaining each FOV as an independent source block.

## Competing representations

### R1: location-only compression control

Each background receives its own `mu_b`, but all backgrounds share one common `sigma`.

This is a one-changing-coordinate compression of the whole-event series. It is **not** `chi_bio`.

### R2: location-plus-dispersion representation

Each background receives its own `mu_b` and its own `sigma_b`.

This is the candidate minimum `Chi_bio` representation for the sensory-distribution event.

## Estimation

Fit parameters by maximizing the summed binomial log likelihood. Use deterministic L-BFGS-B optimization with:

- `mu_b` bounded from `ln(L_{min})-5` to `ln(L_{max})+5`;
- `sigma` bounded to `[0.05,5]`;
- identical bounds and initialization logic for training folds and full-data fits.

No outcome-dependent starting-value tuning is permitted.

## Primary predictive comparison

Use leave-one-FOV-out cross-validation within the frozen six-background set.

For every held-out FOV:

1. fit R1 and R2 using all other FOVs;
2. predict the five CDF binomial counts for the held-out FOV;
3. sum held-out binomial log likelihood for each representation.

The primary increment is

[
Delta LL_{CV}=LL_{CV}(R2)-LL_{CV}(R1).
]

Positive values favor retaining background-specific dispersion. Negative values favor the location-only compression.

## Uncertainty

Estimate uncertainty in `Delta LL_{CV}` by a fixed-seed nonparametric bootstrap over held-out FOV score differences, 10,000 resamples, seed 20260925.

The representation disposition is:

- `R2_REQUIRED_P0Q` if the two-sided 95% bootstrap interval for `Delta LL_{CV}` is entirely above zero;
- `R1_SUFFICIENT_P0Q` if the interval is entirely below zero;
- `REPRESENTATION_DIFFERENCE_UNRESOLVED_P0Q` if the interval includes zero.

This classification is limited to this source and event.

## Whole-event descriptive reproduction

The source-open biological event is summarized using the fitted `sigma_b` values across the ordered MeAsp backgrounds 0, 0.1, 0.3, 1, 10, and 100 uM. Report:

- all six `sigma_b` estimates;
- Spearman correlation between background rank and `sigma_b`;
- endpoint difference `sigma_{100}-sigma_0`;
- FOV-level bootstrap intervals for these summaries.

Because the literature direction was known during selection, these are descriptive reproduction statistics, not prospective confirmation statistics.

## Scalar gate

No `chi_bio` value will be calculated from `mu_b`, `sigma_b`, Hill coefficients, adaptation time, or FRET amplitude unless an independently licensed source-native dynamical reduction is identified before such values are inspected.

The default scalar result for this experiment is therefore `NOT_OPENED_NOT_LICENSED`.

## Failure handling

Any data-format mismatch, missing frozen FOV, source-code ambiguity, optimizer failure, or disagreement with source semantics is preserved as an explicit failure/outlier/root-cause record. Mechanical repair may restore execution but may not change the frozen scientific objects or decision rule.
