# P0-D15 Chi / Discriminant Uncertainty Result

Date: 2026-09-11
Status: **P0-D RESULT. NOT P0-Q. NOT P1. NO CONFIDENCE RULE FROZEN.**
Workflow run: `34617004601`
Job: `103321309854`
Artifact ID: `10271086414`
Artifact ZIP SHA256: `50c9eaae2a2f0b64dc85fcd54a124d65a1c12b7ccc2cd5ab1512f84784b6efc2`

## Question

Can the NSD-native batch Hankel covariance root be propagated directly to the branch-complete component coordinate `chi` and normalized discriminant `delta_chi = chi^2 - 1`, and does that propagated variance behave well enough to support a confidence/branch rule?

## Mechanical result

Three dedicated chi-uncertainty tests passed. The run completed across `chi = 0.80, 0.95, 0.99, 1.00, 1.01, 1.05, 1.20, 1.50`, record lengths `8000` and `32000`, batch counts `6` and `12`, and finite-difference epsilons `0.25` and `0.50`.

## Central result

**The branch-complete uncertainty object is computationally viable, but its present batch-Hankel calibration is not globally reliable enough to freeze a confidence or branch-adjudication rule.**

The useful result is therefore architectural rather than operational: uncertainty can be attached directly to the same invariant chi/discriminant coordinate on both sides of the repeated-root boundary, but the current sampling-covariance approximation and first-order propagation require further qualification.

## Representative behavior

### Longer-record subcritical regimes

At `n=32000`, some subcritical conditions showed encouraging variance calibration.

For `chi=0.95`:

- predicted/empirical variance ratio for chi was about `1.07-1.13` with 12 batches and about `1.11-1.13` with 6 batches;
- predicted/empirical variance ratio for `delta_chi` was about `1.12-1.22`;
- all 16 base fits propagated successfully across the reported settings.

For `chi=0.80` at `n=32000`, the method was more conservative, with predicted/empirical variance ratios around `2.23-2.37`.

Thus the native propagation can land in the correct order of magnitude in some well-resolved regimes, but it is not uniformly calibrated.

### Near-boundary regimes

At `chi=0.99`, `1.00`, and `1.01`, both point estimates and propagated uncertainty remained branch-sensitive.

Examples:

- `chi=0.99`, `n=32000`: only `62.5%` of point estimates had the true discriminant sign; predicted/empirical variance ratios were roughly `2.6-3.0`.
- `chi=1.00`, `n=32000`: propagated variance was generally conservative by roughly `2.4-3.2`, depending on batch count and epsilon.
- `chi=1.01`, `n=8000`: propagated variance strongly **underestimated** empirical spread in several settings, with chi variance ratios near `0.12-0.21` and discriminant variance ratios near `0.055-0.098`.
- `chi=1.01`, `n=32000`: calibration improved materially, with ratios roughly `1.6-1.9`.

This is not compatible with freezing a universal Gaussian-style branch-confidence convention.

### More strongly overdamped regimes

The method becomes less reliable as the second dynamical direction weakens and the finite-sample fit becomes more nonlinear/fragile.

At `chi=1.20`:

- propagation failures occurred in several `n=8000` settings;
- `n=32000` variance ratios ranged from roughly `3` to more than `8` depending on quantity and epsilon.

At `chi=1.50`:

- propagation failures were common;
- calibration direction changed with setting, including severe overestimation in some 8000-sample cases and underestimation in some 32000-sample cases.

This is consistent with P0-D14, which showed progressive loss of finite-sample support for the second population direction on the deep overdamped branch.

## Important positive result

The uncertainty formulation itself is branch-complete. It does not require a prior decision that the fitted factor is underdamped or overdamped. The same two-pole invariant factor produces:

`chi = gamma / (2 omega_n)`

and

`delta_chi = chi^2 - 1`.

Uncertainty can therefore be propagated to a continuous coordinate and to its signed distance from the repeated-root boundary without first hard-classifying the branch.

That avoids a circular architecture in which the estimator would need to decide the branch before deciding whether branch placement is uncertain.

## Interpretation

P0-D15 supports the following bounded conclusions:

1. **Coordinate uncertainty belongs beside chi, not inside chi.** It is epistemic metadata, not a conglomeration term or a numerical penalty to the coordinate.
2. **The same uncertainty object can span both sides of the EP/repeated-root boundary.** No separate underdamped and overdamped uncertainty definitions are required at the invariant-factor level.
3. **The current batch-Hankel covariance root is not yet a qualified global sampling-covariance model for chi.** Calibration varies materially by regime, record length, batching and local conditioning.
4. **Near-boundary and deep-overdamped cases require explicit indeterminacy/refusal capability.** A point estimate alone is insufficient.
5. **No confidence multiplier, gray-zone width, batch count, epsilon or branch rule is licensed by this P0-D surface.** Those choices require independent P0-Q qualification.

## Consequence for current conglomeration architecture

This result reinforces the separation between physical and epistemic structure:

- local/global dynamical lineages and coupling/feedback determine the physical coordinate architecture;
- uncertainty determines how sharply those coordinates can be placed;
- the Atlas later evaluates functional meaning;
- none of these should be averaged together into one score.

## Next uncertainty work

Before any P0-Q confidence rule, investigate why the batch-Hankel approximation changes calibration direction across overdamped regimes. Candidate causes include dependence among contiguous batches, nonlinear pole-factor sensitivity, finite-difference breakdown near branch changes, and non-Gaussian/heavy-tailed estimator behavior under weak second-direction support.

That investigation must remain separate from any Atlas outcome information.

## Nonclaims

- No uncertainty method is validated for neural data.
- No 95% interval or other confidence level is frozen.
- No branch-indeterminate threshold is selected.
- No batch count or epsilon is selected.
- No neural chi range is inferred.
- No Atlas evidence is used.
- No P0-Q or P1 decision is changed.
