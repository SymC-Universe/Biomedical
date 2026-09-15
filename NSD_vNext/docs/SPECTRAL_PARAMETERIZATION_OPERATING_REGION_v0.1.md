# NSD Descriptive Spectral Parameterization Operating Region v0.1

Date: 14 September 2026
Status: **P0-Q CANDIDATE REGION FROZEN FOR LABEL-BLIND HEALTHY PILOT**
Scope: descriptive periodic/aperiodic parameterization only

## 1. Decision

The first candidate descriptive parameterization region is frozen from **known-truth simulations plus native specparam model guidance**, before looking at periodic/aperiodic results from the healthy EEG pilot.

Frozen candidate:

```text
source PSD: Welch
source PSD window: 4 s
source PSD overlap: 50%
source PSD window function: Hann
source PSD detrend: constant
source PSD scaling: density
parameterizer: specparam 2.0.0rc7
aperiodic mode: fixed
fit frequency range: 5-35 Hz
periodic mode: gaussian
peak_width_limits: 0.5-12 Hz
min_peak_height: 0.20 log10 power units above aperiodic fit
peak_threshold: 3.0 SD
max_n_peaks: 3
```

This is **not** yet an Atlas release configuration. It is the single prespecified candidate allowed into the first label-blind healthy repeat pilot.

## 2. Why the original 1-45 Hz fixed fit was rejected

The first known-truth failure map exposed a severe model-family failure.

When a spectrum generated from a knee-shaped aperiodic background with **zero periodic peaks** was fit with a fixed aperiodic model over 1-45 Hz, the fixed model could invent periodic structure while still achieving a very high goodness-of-fit score.

One noiseless example produced:

- fixed fit R-squared approximately 0.992;
- two invented periodic peaks;
- one fitted bandwidth pinned at the 12-Hz upper width limit.

Therefore:

> **High global R-squared is not sufficient evidence that periodic components are real.**

The wide-range fixed model is not admitted for the current purpose.

## 3. Why permissive peak defaults were rejected

A deterministic-noise known-truth sweep with permissive settings (`min_peak_height = 0`, `peak_threshold = 2`) produced:

- spurious periodic peaks on weak/noisy spectra;
- splitting of one intended component into multiple fitted components;
- fitted widths hitting allowed boundaries;
- excessive dependence on `max_n_peaks`.

The project therefore does not inherit permissive defaults merely because they are common or convenient.

## 4. Initial peak-admission calibration

A prespecified grid tested:

- `peak_threshold`: 2.0, 2.5, 3.0;
- `min_peak_height`: 0.05, 0.10, 0.15, 0.20;
- `max_n_peaks`: 3, 4;
- fixed and knee known-truth backgrounds;
- no-peak spectra;
- single peaks of multiple heights;
- two separated peaks;
- deterministic log-power noise at two amplitudes.

Only configurations with `min_peak_height = 0.20` passed the first fixed-background calibration screen.

That result did **not** solve aperiodic model-family misspecification: a fixed 1-45 Hz fit could still create peaks when knee truth was present.

## 5. Dual fixed/knee consensus was tested and rejected

A conservative policy requiring both fixed and knee fits to agree on a peak was tested prospectively.

Result:

`passing_count = 0`

The consensus policy successfully suppressed false positives but lost too much true periodic structure, especially under knee-background truth. The qualification criteria were **not relaxed after seeing this failure**.

Therefore fixed/knee consensus is not the current admission rule.

## 6. Frequency-range calibration

The next test followed established specparam guidance: fixed aperiodic fitting should be used only over a range in which the background is approximately linear in log-log space, and broad ranges containing a knee should not be forced into the fixed model.

Official guidance:

- https://specparam-tools.github.io/auto_tutorials/plot_05-AperiodicFitting.html
- https://specparam-tools.github.io/faq.html

A prespecified known-truth grid evaluated fixed-mode fits over:

- 1-45 Hz;
- 2-40 Hz;
- 3-35 Hz;
- 3-30 Hz;
- 5-35 Hz.

For each range, the same peak-admission families were tested against both fixed-background and knee-background truths.

### Result

Only **5-35 Hz** produced passing configurations under the frozen criteria.

For 5-35 Hz with `min_peak_height = 0.20`, all tested peak thresholds (2.0, 2.5, 3.0) and both `max_n_peaks` values (3, 4) passed the candidate-region criteria.

Representative metrics for the simpler `max_n_peaks = 3` configuration were the same across peak thresholds in this grid:

- fixed-truth no-peak false-positive rate: **0.00**;
- knee-truth no-peak false-positive rate: **0.00**;
- mean strong-single-peak recovery across fixed/knee backgrounds: **0.9667**;
- mean exact-one-peak rate: **0.9083**;
- mean false-extra-peak count: **0.0833**;
- minimum two-peak recovery across fixed/knee backgrounds: **0.90**.

The broader candidate ranges failed mainly because the fixed model continued to mistake knee/background curvature for periodic structure and/or failed the multi-peak recovery criteria.

## 7. Why 3.0 SD and max 3 were selected among equivalent passing candidates

The known-truth grid did not show a performance advantage for the more permissive alternatives within this tested region.

The project therefore uses the following prespecified tie-breaker:

> when known-truth performance is materially equivalent, prefer the simpler and more conservative configuration.

That yields:

- `peak_threshold = 3.0` rather than 2.0/2.5;
- `max_n_peaks = 3` rather than 4.

This selection was made without inspecting healthy or clinical parameterized spectra.

## 8. What the 5-35 Hz choice does and does not mean

The 5-35 Hz range applies only to the **descriptive periodic/aperiodic parameterizer**.

It does not discard the rest of the recording or the broader PSD.

The Engine continues to retain:

- raw/qualified signal information;
- Welch PSD over the broader declared range;
- low-frequency power below 5 Hz;
- frequencies above 35 Hz where supported;
- future modal/time-domain routes that have their own operating regions.

Thus the parameterizer is one representation layer, not the definition of the signal.

## 9. Real-data warning flags retained

The first healthy pilot must report, not hide:

- peaks pinned at the lower width limit;
- peaks pinned at the upper width limit;
- fits reaching the maximum peak count;
- zero-peak channels;
- fixed-versus-knee descriptive disagreement as a sensitivity diagnostic;
- fit metrics and residual-quality information;
- source PSD configuration and exact software versions.

The warning implementation lives in:

`engine/nsd_engine/spectral_parameterization_qc.py`

A warning is not automatically a universal refusal unless the relevant refusal rule has itself been qualified.

## 10. Interpretation firewall

Even if a 5-35 Hz descriptive peak passes this candidate region:

`peak center frequency != natural frequency omega_0 by default`

`peak bandwidth != damping rate`

`peak != identified dynamical mode`

`peak != chi`

The parameterization layer is descriptive. Dynamical interpretation remains downstream of the independent modal/state-space qualification program.

## 11. Next gate

The frozen candidate now advances to exactly one real-data task:

> run label-blind on the already pinned `ds003775` `sub-069` t1/t2 healthy repeat pair.

That pilot may reveal Limit-Map problems and can reject the candidate. It may **not** be used to tune the configuration to maximize repeat similarity.

If the candidate behaves acceptably, the next scale is all 42 repeat subjects. If it fails, the failure is recorded and the spectral architecture is revised as a new version before further use.
