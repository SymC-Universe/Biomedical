# M2 Latent-Oscillator Model-Adequacy Plan v0.1

Date: 18 September 2026  
Status: ACTIVE T0 / PRE-REAL-EEG QUALIFICATION  
Route under test: `M2_LATENT_COVARIANCE`  
Adversarial workflow: `NSD Latent Oscillator Adversarial Map`  
Run: `35304835293`  
Result: SUCCESS  
Artifact digest: `sha256:1439e02d41d74aed68394d307381662c54e6973c432c92f81c0c57c2c72e4b31`

## 1. Purpose

The M2 covariance route successfully solved one important known-truth problem: additive **white** observation noise no longer destroys latent oscillator recovery in the same way that direct AR(2) least squares did.

That success is not sufficient for real EEG.

The first explicit misspecification map has now shown that the current mechanical M2 admission gate is far too permissive. This document freezes the next question:

> Can a single latent damped oscillator be distinguished from plausible alternative generators before its pole, natural frequency, or modal damping ratio is admitted?

No diagnosis or clinical label enters this program.

## 2. Adversarial result

Each scenario used three deterministic seeds, 30 s duration, and 256 Hz sampling.

| Generator | Admission rate | Median covariance-fit R² | Median fitted natural frequency | Median fitted damping ratio |
| --- | ---: | ---: | ---: | ---: |
| Valid single oscillator | 1.00 | 0.9382 | 10.0935 Hz | 0.3206 |
| Two close modes | 1.00 | 0.9403 | 10.7249 Hz | 0.3263 |
| Two separated modes | 1.00 | 0.8476 | 11.0021 Hz | 0.3815 |
| Colored observation noise | 1.00 | 0.9132 | 9.7515 Hz | 0.4921 |
| Mid-record frequency shift | 1.00 | 0.8611 | 10.0248 Hz | 0.4054 |
| Finite bursts | 1.00 | 0.8303 | 9.8400 Hz | 0.1934 |
| Nonoscillatory AR(1) | 1.00 | 0.8785 | 1.5101 Hz | 0.7493 |
| White noise | 1.00 | 0.0151 | 36.2266 Hz | 0.0103 |

For the valid single-oscillator truth, median absolute damping-ratio error was approximately **0.0206** and median relative natural-frequency error approximately **0.0199**.

## 3. Decisive finding

**Every misspecified adversarial generator was admitted by the current gate.**

This means:

`M2_MECHANICAL_ADMISSION != M2_SCIENTIFIC_MODEL_ADEQUACY`

A high covariance-fit R² is also not sufficient. The close two-mode mixture achieved a median R² slightly higher than the valid single-mode truth.

Therefore no post-hoc R² cutoff can solve the model-identification problem by itself.

Current classification remains:

`M2_LATENT_COVARIANCE = KNOWN_TRUTH_BASELINE / REAL_EEG_NOT_ADMITTED`

The route remains scientifically useful as a component and comparator, but it cannot yet license real-EEG modal damping ratios.

## 4. What each adversary teaches us

### A. White noise

Very low covariance-fit R² plus an extremely small fitted latent fraction gives an obvious refusal direction.

This is the easy case.

### B. Nonoscillatory AR(1)

A smooth nonoscillatory covariance can be forced into a low-frequency, highly damped oscillator.

Required implication:

> the oscillator model must compete against a nonoscillatory stochastic alternative.

A frequency bound alone is not a principled solution because the admissible frequency band is a task/model property and an AR-like process can contaminate other bands.

### C. Colored observation noise

The current derivation assumes white observation noise. Colored noise contaminates nonzero-lag covariance and is therefore absorbed into the putative latent oscillator.

Required implication:

> observation-noise color must either be modeled explicitly or detected through an adequacy diagnostic.

### D. Frequency drift and finite bursts

A single stationary oscillator fit returns a plausible compromise parameter even when stationarity is false.

Required implication:

> whole-record fit quality must be supplemented by subwindow/state consistency tests.

### E. Two modes

This is the hardest and most important failure.

Two close modes can fit the single-mode covariance form extremely well. Therefore residual magnitude alone may not identify model-order error.

Required implication:

> the one-oscillator model must compete with a higher-order/multi-mode alternative using a prespecified model-selection or held-out-prediction framework.

## 5. Frozen next qualification architecture

The next route is not “M2 with a nicer cutoff.” It is an **adequacy wrapper** around native candidate models.

The minimum candidate set is:

### A0 — nonoscillatory stochastic alternative

A native AR(1)/relaxation or equivalent nonoscillatory state-space model.

Purpose:
- reject red-noise/relaxational processes that a damped oscillator can mimic.

### A1 — one latent oscillator

Current M2 latent oscillator with explicit observation noise.

Purpose:
- preserve the qualified single-mode route.

### A2 — two latent oscillators

A four-state linear Gaussian state-space model containing two 2D oscillatory blocks, with observation mixing and explicit observation noise.

Purpose:
- test whether a one-mode explanation is actually sufficient.

The eventual fitting route should use a proper innovations/Kalman likelihood where feasible rather than treating correlated covariance residuals as independent likelihood observations.

## 6. Required adequacy tests

Before any real EEG M2/A1 estimate can be admitted, the following must be mapped on known truth.

1. **Model-order discrimination**
   - A0 vs A1;
   - A1 vs A2;
   - separated and close oscillatory modes;
   - amplitude imbalance between modes.

2. **Innovation/residual adequacy**
   - residual temporal autocorrelation;
   - residual spectral structure;
   - whiteness diagnostics;
   - systematic oscillatory residuals.

3. **Stationarity**
   - full-record versus half/quarter-window estimates;
   - frequency-shift truth;
   - damping-shift truth;
   - finite-burst truth.

4. **Noise structure**
   - white observation noise;
   - colored observation noise;
   - process-noise variation;
   - mixed process/observation noise.

5. **Identifiability**
   - repeated initializations;
   - likelihood/profile curvature or another prespecified uncertainty route;
   - parameter boundary occupancy;
   - mode swapping in A2;
   - minimum resolvable separation.

6. **Held-out behavior**
   - fit one interval/subset and assess predictive innovations on data not used to choose model order where the generator permits it;
   - avoid selecting the model on the same scalar criterion later used to claim adequacy.

7. **Operating region**
   - frequency;
   - damping;
   - duration;
   - sampling rate;
   - SNR/noise ratio;
   - mode separation.

## 7. Admission logic to be earned, not assumed

The desired future output is not merely:

`admitted = optimizer_converged`

It should distinguish at least:

- `MODE_ADEQUATE_SINGLE_OSCILLATOR`;
- `REF_NONOSCILLATORY_ALTERNATIVE_PREFERRED`;
- `REF_MULTIMODE_REQUIRED`;
- `REF_NONSTATIONARY`;
- `REF_COLORED_NOISE_UNRESOLVED`;
- `REF_MODE_NONIDENTIFIABLE`;
- `REF_UNCERTAINTY_TOO_LARGE`;
- `REF_OUT_OF_OPERATING_REGION`.

Exact codes/thresholds are not frozen until known-truth calibration supports them.

## 8. Relationship to Chi-vs-chi

This negative result strengthens rather than weakens the current architecture.

A descriptive spectral peak can exist without a unique dynamical mode.

A good one-mode fit can exist without a true one-mode generator.

A local modal damping ratio therefore belongs **after** model-order and model-adequacy qualification.

The sequence remains:

`signal -> native candidate models -> model adequacy/order -> identified poles -> modal damping ratio zeta_i -> SymC correspondence where warranted`

not:

`peak -> width -> damping -> chi`

and not:

`optimizer returned a pole -> therefore the brain has that mode`.

## 9. Real-EEG firewall

Until this adequacy program closes, the following remain prohibited for real EEG:

- M2-derived modal damping ratios;
- M2-derived local chi;
- biological interpretation of a fitted latent mode;
- clinical feature selection using M2 outputs;
- diagnosis or prognosis from M2 outputs.

The next code work is model-adequacy qualification, not real-data application.


## 10. Interim adequacy-diagnostic pass

Date: 18 September 2026
Implementation commit lineage includes the diagnostic extension in engine/tools/probe_latent_oscillator_adversaries.py.

Purpose:
Test whether simple alternative-model competition and within-record stability diagnostics can expose the failure classes already discovered, without changing the production M2 admission rule.

Added diagnostics:
- single-oscillator covariance fit versus a nonoscillatory AR(1)-like covariance alternative;
- single-oscillator covariance fit versus a two-oscillator covariance alternative;
- split-half frequency and damping stability;
- explicitly labeled pseudo-BIC summaries.

Important statistical ceiling:
The covariance-lag residuals are correlated. These pseudo-BIC values are qualification diagnostics only. They are not formal likelihood-based information criteria and are not frozen as admission thresholds.

Observed median behavior across the deterministic three-seed adversarial map:

- valid single oscillator:
  - pseudo-BIC single minus AR1 approximately -483.9;
  - pseudo-BIC two minus single approximately -77.7;
  - split-half frequency symmetric relative difference approximately 0.060;
  - split-half damping absolute difference approximately 0.016.

- nonoscillatory AR(1):
  - pseudo-BIC single minus AR1 approximately +261.4, correctly favoring the nonoscillatory alternative;
  - pseudo-BIC two minus single approximately +16.8.

- two close modes:
  - pseudo-BIC two minus single approximately -41.3.

- two separated modes:
  - pseudo-BIC two minus single approximately -228.1.

- mid-record frequency shift:
  - split-half frequency symmetric relative difference approximately 0.508.

- finite bursts:
  - split-half damping absolute difference approximately 0.137, but frequency stability alone did not reject the case.

- colored observation noise:
  - neither split-half frequency stability nor the single-versus-AR1 comparison by itself resolves the misspecification.

- white noise:
  - covariance fit remains extremely poor, but this easy case cannot define the general adequacy rule.

Scientific interpretation:

1. A0 versus A1 competition is promising for the explicit nonoscillatory AR(1) failure.
2. Split-window stability is informative for strong nonstationarity such as the frequency-shift generator.
3. The covariance-based A2 pseudo-BIC is not a sufficient model-order rule because it improves the diagnostic criterion for both true two-mode cases and the valid single-mode truth.
4. No post-hoc combination of these first diagnostics is promoted as the production gate.

Decision:
The frozen Section 5 architecture remains unchanged. The next substantive modal implementation should use proper innovations/Kalman likelihood or another statistically justified state-space equivalent for A0/A1/A2 competition, then add residual/innovation, stationarity, identifiability, held-out, and operating-region qualification.

Current route status remains:

M2_LATENT_COVARIANCE = KNOWN_TRUTH_BASELINE / REAL_EEG_NOT_ADMITTED

This pass is recorded in P0Q_QUALIFICATION_SEARCH_LEDGER_v0.1.md.
