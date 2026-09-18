# NSD Modal Estimator Qualification v0.1

Date: 14 September 2026
Status: ACTIVE T0 / P0-Q
Scope: native dynamical mode estimation before real-EEG admission

## 1. Purpose

The modal layer must earn local pole/frequency/decay quantities independently of descriptive spectral parameterization and independently of diagnosis.

This document records the first executable route and its failure boundary.

## 2. Route M1: direct output-only AR(2) least-squares estimator

Model convention:

```text
x[t] = a1*x[t-1] + a2*x[t-2] + e[t]
```

The fitted discrete poles are roots of:

```text
z^2 - a1*z - a2 = 0
```

For a stable complex-conjugate pair, the estimator maps the discrete pole through:

```text
s = log(z) / dt = -alpha +/- i*omega_d
omega_n = sqrt(alpha^2 + omega_d^2)
zeta = alpha / omega_n
```

This is a legitimate model-specific route only when the AR(2) assumptions and operating region are qualified. It is not a generic EEG-to-damping shortcut.

Implementation:

`engine/nsd_engine/ar2_modal.py`

## 3. Clean known-truth result

Known-truth grid:

- natural frequencies: 5, 10, 20 Hz;
- damping ratios: 0.10, 0.20, 0.40, 0.60, 0.80, 0.90, 0.95;
- durations: 10, 30, 120 s;
- three random seeds per cell;
- 256 Hz sampling.

With **no additive observation/measurement noise**, the route performed well over most of the tested grid:

- 63 grid rows;
- median admission rate: **1.0**;
- mean admission rate: approximately **0.995**;
- median absolute damping-ratio error among admitted rows: **0.0142**;
- median relative natural-frequency error: **0.0080**.

Worst clean median damping errors were concentrated in short, low-frequency, highly damped cases. Examples:

- 5 Hz, zeta 0.95, 10 s: median absolute zeta error about 0.070;
- 5 Hz, zeta 0.90, 10 s: about 0.066;
- 5 Hz, zeta 0.80, 10 s: about 0.058.

Thus even in clean truth, operating-region quality depends on duration, frequency, and damping.

## 4. Observation-noise falsification

The same latent AR(2) truths were then contaminated with additive measurement noise expressed relative to the clean signal standard deviation.

This exposed a decisive limitation of direct least-squares AR(2) fitting.

### Noise ratio 0.25

Across 63 rows:

- mean admission rate fell to approximately **0.138**;
- only 9 rows retained any admitted estimates;
- median absolute damping-ratio error among those admitted rows was approximately **0.525**;
- median relative frequency error among admitted rows was approximately **0.245**;
- `REF_MODE_NONIDENTIFIABLE` dominated refusal behavior.

The few admitted estimates were therefore not trustworthy merely because they survived the mechanical pole gate.

### Noise ratios 0.50 and 1.00

Across the tested grid:

- admission rate: **0**;
- no damping/frequency estimate survived the current complex-stable-pole gate;
- refusals were `REF_MODE_NONIDENTIFIABLE`.

## 5. Scientific decision

Direct output-only AR(2) least squares is **not admitted for real EEG modal inference**.

Current classification:

`M1_AR2_DIRECT = KNOWN_TRUTH_BASELINE / REAL_EEG_NOT_ADMITTED`

Why:

1. clean synthetic recovery demonstrates the pole mapping and convention are mechanically sound;
2. additive observation noise creates severe errors and/or destroys identifiability;
3. real EEG necessarily includes measurement noise, unmodeled sources, source mixing, nonstationarity, and higher-order structure;
4. relaxing refusal gates to obtain more real-data estimates would be backwards and is prohibited.

The negative result is useful. It prevents a superficially elegant local damping-ratio pipeline from being promoted beyond its evidence.

## 6. Next modal route: latent state-space oscillator

The next candidate should explicitly separate latent oscillator dynamics from observation noise.

Native structure:

```text
x[t+1] = A x[t] + w[t]
y[t]   = H x[t] + v[t]
```

with an oscillatory 2D latent transition block, process noise `w`, and explicit observation noise `v`.

The candidate must estimate or otherwise qualify:

- latent decay / pole radius;
- damped frequency;
- observation-noise variance;
- process-noise variance;
- uncertainty/identifiability;
- model adequacy/residual behavior.

The preferred qualification route is likelihood-based state-space estimation / Kalman filtering, with parameters transformed back into established pole and modal damping terminology only after the model is admitted.

## 7. Required known-truth tests for M2

Before real EEG:

1. clean latent oscillator;
2. observation-noise ratios spanning the AR2 failure region;
3. process-noise variation;
4. duration variation;
5. frequency/damping grid;
6. two-mode contamination;
7. colored observation/process disturbances;
8. frequency drift;
9. finite bursts/nonstationarity;
10. non-oscillatory alternatives;
11. model-order mismatch;
12. initialization sensitivity;
13. uncertainty/calibration behavior.

The AR2 route remains as a comparator because agreement/disagreement between naive and observation-noise-aware estimators is itself useful Limit-Map information.

## 8. Consequence for lowercase chi

No local `chi_i` / modal damping ratio is admitted on real NSD EEG merely because a descriptive peak exists or an AR(2) fit returns complex poles.

The sequence remains:

`signal -> qualified latent/modal model -> pole/decay/frequency -> modal damping ratio zeta_i -> SymC correspondence only where warranted`

not:

`PSD peak -> width -> damping -> chi`.


## 9. M2 covariance-route first known-truth map

Workflow:

- `NSD Latent Oscillator Covariance Map`
- run `35304534021`
- result: **SUCCESS**
- estimator: `engine/nsd_engine/latent_oscillator_covariance.py`

This route models a scalar observation of a latent two-dimensional damped rotation with additive white measurement noise. It fits the non-zero-lag covariance structure, allowing zero-lag observation noise to be represented separately under the stated stationary/isotropic assumptions.

### Aggregate known-truth behavior

Each observation-noise stratum contained 36 grid rows. Median results were:

| measurement-noise SD / latent SD | median admission rate | median absolute damping-ratio error | median relative natural-frequency error | median absolute latent-fraction error | median autocorrelation R-squared |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00 | 1.0 | 0.0311 | 0.0306 | 0.0092 | 0.9292 |
| 0.25 | 1.0 | 0.0305 | 0.0413 | 0.0182 | 0.9324 |
| 0.50 | 1.0 | 0.0331 | 0.0390 | 0.0183 | 0.9297 |
| 1.00 | 1.0 | 0.0358 | 0.0353 | 0.0180 | 0.9031 |

This is a major improvement over direct AR(2) least squares in the specific known-truth problem for which the covariance route was designed: additive white observation noise no longer destroys median recovery across the tested grid.

### Failure region remains real

The aggregate medians hide a clear difficult corner. The largest damping-ratio errors were concentrated in short, low-frequency, highly damped signals.

Examples from the worst rows include:

- 5 Hz, zeta 0.95, 10 s, noise ratio 1.0: median absolute zeta error about **0.204**, median relative frequency error about **0.182**;
- 10 Hz, zeta 0.95, 10 s, noise ratio 1.0: damping error about **0.197**, relative frequency error about **0.239**;
- 5 Hz, zeta 0.95, 10 s, noise ratio 0.5: damping error about **0.185**;
- 5 Hz, zeta 0.95, 30 s: damping error remained roughly **0.15–0.17** across several noise conditions.

Therefore the current mechanical admission flag is **not yet a scientifically sufficient admission rule**. A method can return an estimate in a region where the estimate is too biased for the intended use.

## 10. M2 decision and next qualification boundary

Current classification:

`M2_LATENT_COVARIANCE = PROMISING_KNOWN_TRUTH_ROUTE / REAL_EEG_NOT_YET_ADMITTED`

What is now supported:

1. the estimator can separate a latent oscillator from additive white measurement noise under its own stated model much better than naive AR(2);
2. median damping/frequency recovery remains stable across the tested observation-noise strata;
3. the route deserves continued qualification rather than rejection.

What is **not** yet supported:

1. applying the estimator to arbitrary EEG;
2. treating its fitted oscillator as a unique biological mode;
3. admitting real-EEG modal damping ratios;
4. assuming the current all-admitted mechanical gate is adequate;
5. robustness to two modes, colored noise, drift, bursts, non-oscillatory alternatives, model-order mismatch, source mixing, or initialization effects.

The next M2 work must therefore map those adversaries and derive an **error-aware operating region/refusal rule from known truth before real EEG is allowed**.

No clinical label enters this process.



## 11. M2 adversarial model-adequacy result

Workflow:

- `NSD Latent Oscillator Adversarial Map`
- run `35304835293`
- result: **SUCCESS**
- artifact digest: `sha256:1439e02d41d74aed68394d307381662c54e6973c432c92f81c0c57c2c72e4b31`

The first explicit misspecification map tested the current single-oscillator covariance estimator against:

- valid single-oscillator truth;
- two close oscillatory modes;
- two separated oscillatory modes;
- colored observation noise;
- a mid-record frequency shift;
- finite bursts;
- nonoscillatory AR(1) dynamics;
- white noise.

**All eight generator families were mechanically admitted in all three seeds.**

Representative median covariance-fit R-squared values were:

- valid single oscillator: 0.9382;
- two close modes: 0.9403;
- colored observation noise: 0.9132;
- nonoscillatory AR(1): 0.8785;
- white noise: 0.0151.

The close two-mode generator fitting at least as well as the valid single-mode generator is decisive: a scalar fit-quality threshold cannot establish single-mode adequacy.

Therefore the classification is tightened to:

`M2_LATENT_COVARIANCE = KNOWN_TRUTH_BASELINE / REAL_EEG_NOT_ADMITTED`

The route remains useful because it recovers single-mode truth under white measurement noise, but the current mechanical gate cannot distinguish that truth from important misspecified alternatives.

The next qualification layer is frozen in:

`docs/M2_MODEL_ADEQUACY_PLAN_v0.1.md`

It requires explicit competition among nonoscillatory, one-oscillator, and two-oscillator native models plus stationarity, colored-noise, residual/innovation, identifiability, and operating-region tests before real EEG may receive an admitted modal damping ratio.
