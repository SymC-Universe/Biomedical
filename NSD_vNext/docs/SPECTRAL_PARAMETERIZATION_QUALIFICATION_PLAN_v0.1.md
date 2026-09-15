# NSD Spectral Parameterization Qualification Plan v0.1

Date: 14 September 2026
Status: PRE-ADOPTION T0 QUALIFICATION PLAN
Scope: descriptive periodic/aperiodic spectral structure only

## 1. Purpose

The next spectral layer after a transparent Welch PSD is periodic/aperiodic parameterization. This plan prevents a convenient library choice from becoming an unqualified scientific dependency.

The target outputs are descriptive spectral quantities such as:

- aperiodic offset;
- aperiodic exponent;
- knee where the model supports and earns it;
- periodic peak center frequency;
- periodic peak power/amplitude;
- descriptive peak bandwidth;
- peak count;
- model error/fit quality;
- explicit no-peak / failed-fit state.

None of these outputs automatically licenses a modal pole, damping rate, quality factor, or local chi.

## 2. Current software state

As of 14 September 2026, the official specparam documentation identifies `specparam` 2.0 as an upcoming major release and warns that the available package is still a release candidate with possible further breaking changes.

The current PyPI candidate is `specparam 2.0.0rc7` (9 June 2026). The project documentation continues to identify the `fooof` 1.x line as the stable release family while the 2.0 transition is unfinished.

Official sources:

- https://specparam-tools.github.io/
- https://specparam-tools.github.io/api.html
- https://pypi.org/project/specparam/

Consequences for NSD:

1. do not depend on unpinned `specparam` in a confirmatory workflow;
2. do not treat a release-candidate API as a permanent internal data contract;
3. isolate the package behind an NSD descriptive-spectral adapter;
4. record the exact package version and settings in every result;
5. retain a regression path against the stable `fooof` 1.x lineage during qualification if needed to distinguish algorithm changes from data effects.

## 3. Admission hierarchy

### S0 — raw PSD

The accepted Welch PSD primitive remains an independent layer.

No parameterization library is allowed to hide or replace the source PSD.

### S1 — model fit

A candidate parameterization implementation receives:

- frequency array;
- power array;
- frozen fitting range;
- frozen aperiodic-mode option;
- frozen peak-width limits;
- frozen peak threshold settings;
- frozen maximum peak count;
- exact implementation/version.

### S2 — descriptive output

Only descriptive periodic/aperiodic parameters enter the structural record.

### S3 — refusal

The adapter must preserve:

- no periodic peak;
- poor model fit;
- implausible/model-boundary fit;
- model disagreement;
- parameter uncertainty or instability where available;
- out-of-qualified-domain state.

A row does not need a fabricated peak to remain usable downstream.

## 4. Known-truth spectrum families

The candidate implementation must first be tested on simulated spectra where the spectral model truth is known.

### SP-KT-01 — pure fixed aperiodic spectrum

Expected:
- recover offset/exponent within frozen tolerance;
- zero periodic peaks;
- no invented alpha-like peak.

### SP-KT-02 — aperiodic knee

Expected:
- knee model recovers the generating family over its admitted region;
- fixed model exposes structured misspecification rather than being silently treated as equivalent.

### SP-KT-03 — single separated periodic peak

Sweep:
- center frequency;
- amplitude;
- descriptive width;
- SNR/background slope.

Measure:
- frequency bias;
- power bias;
- width bias;
- missed-peak rate.

### SP-KT-04 — two separated peaks

Expected:
- two peaks when resolvable;
- no arbitrary compression into one peak.

### SP-KT-05 — overlapping peaks

Purpose:
- map the resolution/failure boundary;
- quantify when peak count and bandwidth become unreliable.

Expected:
- uncertainty or refusal at the qualified boundary;
- no conversion of merged width into damping.

### SP-KT-06 — weak periodic component near detection boundary

Purpose:
- quantify false-negative/false-positive tradeoffs without clinical labels.

### SP-KT-07 — broad descriptive Gaussian bump

Expected:
- descriptive peak may be admitted;
- dynamical interpretation remains prohibited.

### SP-KT-08 — line-noise / edge contamination

Purpose:
- map fit sensitivity to spectral artifacts and fitting range.

### SP-KT-09 — PSD-resolution perturbation

Generate the same underlying spectrum under different recording durations/Welch resolutions.

Purpose:
- separate parameterization instability from biology.

## 5. Model-choice qualification

At minimum compare:

- fixed versus knee aperiodic model where scientifically plausible;
- candidate specparam 2.0 exact-pinned adapter;
- stable-lineage regression anchor if needed during the 2.0 transition.

Selection is label-blind and based on:

- known-truth recovery;
- fit residual structure;
- false/missed peak behavior;
- repeatability;
- nuisance robustness;
- refusal behavior;
- implementation reproducibility.

Diagnosis separation is not a model-selection criterion.

## 6. Real healthy pilot

After known-truth qualification, use the already pinned `ds003775` repeat-session pair.

Questions are limited to:

1. does the adapter run reproducibly on traceable real PSDs;
2. how many channels return zero, one, or multiple descriptive peaks;
3. how stable are periodic/aperiodic outputs across the two sessions of the same subject;
4. where do model choices disagree;
5. do fit failures/refusals cluster by channel/frequency/configuration;
6. are conclusions robust to a prespecified reasonable PSD-window perturbation.

A single-subject repeat pair cannot establish population reliability.

## 7. Population qualification

Only after the pilot behaves sensibly:

- expand to the 42-repeat-subject subset;
- estimate subject-aware test-retest behavior;
- preserve channel/region structure;
- map no-peak and failed-fit prevalence;
- quantify dependence on age/sex only downstream and without retuning extraction;
- then extend to the full 111-subject healthy set.

## 8. Output contract

Every parameterized spectrum must carry:

```text
source_psd_config
source_psd_version
parameterizer_name
parameterizer_version
parameterizer_settings
frequency_range
aperiodic_model
periodic_peaks[]
fit_metrics
fit_residual_summary
zero_peak_state
refusal_state
configuration_hash
```

## 9. Interpretation firewall

The following mappings remain prohibited at this layer:

`aperiodic exponent -> E/I ratio` as a universal identity

`peak bandwidth -> damping rate`

`peak center frequency -> natural frequency omega_0`

`descriptive peak -> dynamical mode`

`periodic parameter -> diagnosis`

These require separate mechanistic/model qualification.

## 10. Promotion rule

Periodic/aperiodic parameterization can enter the first healthy Atlas only after:

1. exact implementation/version is frozen;
2. known-truth region and failure region are mapped;
3. no-peak and poor-fit states remain visible;
4. nuisance sensitivity is quantified;
5. real healthy repeat behavior is characterized;
6. configuration is frozen before clinical overlay.
