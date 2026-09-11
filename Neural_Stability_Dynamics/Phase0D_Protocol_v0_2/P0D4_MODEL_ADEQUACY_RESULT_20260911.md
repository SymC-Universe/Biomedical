# NSD P0-D4 Model-Adequacy Response-Surface Result

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Status: **P0-D MODEL-ADEQUACY MAPPING. NO ADEQUACY GATE OR P1 RULE IS FROZEN.**

## Purpose

Structural recovery is not sufficient to establish that a fitted local stochastic linear representation adequately describes the observed process. P0-D4 therefore mapped two intentionally separate diagnostic paths before selecting any numerical gate:

1. **SSI-COV positive-lag covariance reconstruction**, using the fitted SSI state transition/output matrices plus a fitted positive-lag covariance Markov parameter;
2. **generic channel-space AR(1) output diagnostics**, using first-half one-step prediction residuals, temporal-structure/surrogate-whiteness descriptors, and second-half prediction error.

The generic AR(1) residuals are not called SSI-COV innovations. No process-noise covariance, measurement-noise covariance, Kalman gain, or innovation covariance is inferred by P0-D4.

## Design

Six conditions, eight deterministic replicates each:

- `stationary_linear` — `NOMINAL_FUNCTION`;
- `stationary_white_sensor_10pct` — `PERTURBED_FUNCTION`;
- `stationary_colored_sensor_10pct_rho0p8` — `PERTURBED_FUNCTION`;
- `structural_frequency_switch` — `BOUNDARY_OR_TRANSITION`;
- `observation_map_switch_0p6` — `BOUNDARY_OR_TRANSITION`;
- `one_over_f_beta1p5` — `BOUNDARY_OR_TRANSITION`.

Records had 4800 samples and were split into 2400-sample train and test halves. SSI-COV was examined at orders 2, 4 and 6. Its covariance Markov parameter was fit on train lags 1–12; reconstruction was then evaluated on held-out train lags 13–24 and on test-half lags 1–24. Generic output residual structure used 12 lags and 99 temporal-permutation surrogates as descriptive P0-D quantities only.

## Execution identity

GitHub Actions workflow: `NSD Phase0D P0-D4 Model Adequacy Surface`
Run: `34566038058`
Job: `103158247155`
Source commit: `4014f3f8dbb821ec5c6743b53a3d0a018594308b`
Artifact ID: `10186037566`
Artifact ZIP SHA-256: `7dc11f95fce6a2c836b4cb94db5aa7df413dd46f2d996da8b9e503a5f1a0e64e`
Artifact contents: adequacy response-surface JSON + environment JSON.

## SSI-COV covariance-reconstruction result

No mechanical exceptions occurred.

At the correct/overcomplete orders 4 and 6, the stationary known-model conditions showed very small fit and held-out-train covariance errors, while second-half error remained low relative to the transition/non-model cases.

Representative **order-4** medians:

| Condition | fit lags | held-out train lags | test-half lags |
|---|---:|---:|---:|
| stationary linear | 0.0000294 | 0.0000912 | 0.01865 |
| white sensor 10% | 0.0000280 | 0.0001516 | 0.08551 |
| colored sensor 10%, rho=.8 | 0.0000291 | 0.0001067 | 0.02863 |
| structural frequency switch | 0.0000507 | 0.0001262 | 1.14772 |
| observation-map switch | 0.0000549 | 0.0001699 | 1.47297 |
| 1/f beta=1.5 | 0.0006261 | 0.0006246 | 0.63703 |

The order-6 pattern was qualitatively similar: very small training reconstruction error did not protect against large second-half mismatch when the system/observation process changed or the 1/f-like process fell outside the intended finite-order construction.

This directly demonstrates why a fitted/stable pole set cannot be equated with adequacy. Models can reconstruct their training covariance extremely closely while failing badly on an independently evaluated covariance sequence.

Order 2 behaved as an under-modeling sensitivity case, with substantially larger fit/held-out errors even on the stationary two-mode family.

## Generic output diagnostic result

The generic AR(1) path showed a different pattern, which is scientifically useful rather than contradictory.

Representative medians:

| Condition | residual autocorrelation energy | surrogate median | descriptive upper-tail p | test normalized prediction error |
|---|---:|---:|---:|---:|
| stationary linear | 0.1659 | 0.1792 | 0.725 | 0.0309 |
| white sensor 10% | 0.4057 | 0.1801 | 0.01 | 0.0518 |
| colored sensor 10%, rho=.8 | 1.2199 | 0.1776 | 0.01 | 0.0391 |
| structural frequency switch | 0.1705 | 0.1799 | 0.675 | 0.0449 |
| observation-map switch | 0.1713 | 0.1767 | 0.615 | 1.3122 |
| 1/f beta=1.5 | 0.3392 | 0.1780 | 0.01 | 0.0546 |

The descriptive p-like values are Monte-Carlo upper-tail locations from 99 surrogate permutations. No alpha level is selected or implied.

The generic first-half residual structure clearly flagged colored/sensor contamination and the 1/f-like process, but it did not identify every cross-half system change because those changes occur after the training residuals are computed. Conversely, second-half prediction error strongly exposed the observation-map switch but was comparatively modest for the structural frequency switch at the one-step channel-space level.

## Central P0-D finding

The two diagnostic families fail in **complementary directions**.

The present evidence supports the architectural statement:

> Model adequacy for NSD cannot be represented by pole stability, training reconstruction, residual whiteness, or one-step prediction alone. A defensible adequacy layer must preserve distinct within-window residual/model-error structure, out-of-sample reconstruction/prediction, fitted stability/admissibility, and order/window sensitivity. Contradictory diagnostics must remain visible rather than being averaged into a single score.

This is an architectural finding, not a frozen decision rule.

## Protocol consequences

1. Preserve a non-aggregated adequacy panel.
2. Preserve the distinction between SSI positive-lag covariance reconstruction and generic output residuals.
3. Do not label generic AR residuals as SSI innovations.
4. Preserve order/window sensitivity as part of the open channel.
5. A future operational adequacy gate must be qualified prospectively on independently generated P0-Q cases after its logic is specified.
6. A future gate should be claim-specific: failure of one adequacy component need not erase unrelated descriptive structure, but it can limit the epistemic class of claims that depend on adequate local dynamics.
7. No numerical adequacy cutoff, diagnostic weighting, preferred model order, alpha level, P1 rule, EEG interpretation, chi coordinate, or biological boundary is frozen from P0-D4.

## Disposition

**P0-D4 COMPLETE.** Model-adequacy method categories are no longer an evidence-empty hold. The remaining hold is to define and independently qualify the exact role/adjudication of these complementary diagnostics without fitting their thresholds to P0-D4.
