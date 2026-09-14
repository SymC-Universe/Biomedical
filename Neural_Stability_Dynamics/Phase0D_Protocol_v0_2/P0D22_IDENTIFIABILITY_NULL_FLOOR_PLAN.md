# P0-D22 Identifiability Null-Floor Challenge Plan

Date: 2026-09-14
Status: **P0-D exploratory falsification plan. No threshold, empirical Atlas zone, recovery rule, or P1 decision is frozen.**
Purpose: `FUNCTION_MAPPING + LIMIT_MAPPING`

## Question
Can changes in observation geometry and effective identifiability manufacture apparent changes in estimated modal chi or recovery-related coordinates when the latent dynamical generator and latent recovery are held exactly fixed?

## Why this is required
Recent GRI work demonstrated that an attractive cross-system relationship can collapse after controlling a geometry/effective-dimension null floor. NSD therefore tests the analogous failure mode before any empirical chi-recovery relationship is eligible for promotion.

This is a confounding challenge, not an import of a cancer-specific mechanism.

## Frozen construction for this P0-D run
- One fixed four-state stable latent generator containing two complex mode pairs.
- Same latent state trajectory within each replicate across all observation conditions.
- Same measurement-noise realization and absolute noise scale within each replicate across all observation conditions.
- Only the observation map is changed by progressively weakening access to the second latent mode pair.
- Observation weak-scale grid: `[1.0, 0.3, 0.1, 0.03, 0.01, 0.003]`.
- SSI-COV estimator: existing implementation, fixed order `4`, fixed block rows `18`.
- Eight deterministic replicates.
- Atlas is not used.
- The prospective `chi ~ 1.2-1.3` note is not used.

## Outputs
For each replicate and observation condition, record separately:
1. observability-matrix singular-value ratio;
2. weak-to-strong observation-column norm ratio;
3. Hankel singular-spectrum participation/effective-rank proxy;
4. estimator success / insufficiency / exception state;
5. estimated positive-complex poles;
6. matched modal chi error where the estimator supports it;
7. estimated spectral abscissa and corresponding asymptotic time constant where stable;
8. error in estimated time constant relative to the unchanged latent truth.

All summaries are descriptive P0-D coordinates. No numerical cutoff is an admission rule.

## Falsification logic
The latent generator, its exact poles, exact modal chi coordinates, spectral abscissa, and latent asymptotic time constant are invariant by construction. Therefore any systematic movement in their estimates across the weak-observability grid is estimator/identifiability structure, not a real change in the underlying dynamics.

A strong apparent chi-recovery relationship generated solely by this manipulation would be evidence that an empirical NSD claim requires explicit identifiability/null-floor control before promotion.

## Firewalls
- Truth is used only to construct and score the known-truth P0-D challenge. It is not passed into SSI-COV.
- No selector threshold is tuned.
- No P0Q1 result is rescored.
- No recovery, safety, diagnostic, clinical, or biological threshold is selected.
- No `chi_system` is defined.
- Failure to recover a mode is preserved as insufficient information, not converted to chi=0 or mode absence.

## Promotion consequence
This run can identify a confounding limit and a required future control. It cannot confirm a neural chi-recovery law or promote an empirical relationship by itself.
