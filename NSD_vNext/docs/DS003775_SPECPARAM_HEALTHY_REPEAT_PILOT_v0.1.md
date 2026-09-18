# ds003775 Descriptive Spectral Parameterization Healthy Repeat Pilot v0.1

Date: 17 September 2026
Status: T0 LABEL-BLIND PILOT RECORDED / POPULATION SCALE-UP REQUIRED
Dataset: OpenNeuro `ds003775`
Subject: `sub-069`
Sessions: `ses-t1`, `ses-t2`
Workflow: `NSD ds003775 Specparam Repeat Pilot`, run `35304533933`
Workflow result: SUCCESS

## 1. Purpose

This pilot is the first real-EEG application of the known-truth-frozen **descriptive** periodic/aperiodic candidate.

It does not qualify modal damping, natural frequency, local chi, diagnosis, prognosis, or a healthy range.

Frozen candidate:

- Welch source PSD;
- 4 s Hann windows;
- 50% overlap;
- constant detrend;
- density scaling;
- source PSD retained over 1–45 Hz;
- `specparam==2.0.0rc7`;
- fixed aperiodic model over 5–35 Hz;
- Gaussian periodic components;
- peak width limits 0.5–12 Hz;
- minimum peak height 0.20 log10 units;
- peak threshold 3.0 SD;
- maximum 3 peaks.

A knee-mode fit is retained only as a model-family sensitivity diagnostic.

## 2. Mechanical result

The workflow successfully:

1. installed the frozen numerical/parameterization stack;
2. downloaded both pinned public EDF payloads;
3. re-verified exact payload identity;
4. ran the frozen candidate on all 64 channels in both sessions;
5. produced and uploaded the full structured report.

Therefore the candidate is executable on the real healthy repeat pair.

## 3. Repeat-session descriptive results

Across the 64 shared channels:

- median absolute aperiodic-exponent difference: **0.0957045**;
- minimum absolute exponent difference: **0.0007831**;
- maximum absolute exponent difference: **0.9349571**;
- same fitted peak-count fraction: **0.671875**;
- same zero-peak-state fraction: **1.0**;
- median nearest-center difference for the first listed peak when both sessions contained peaks: **0.0992024 Hz**;
- maximum corresponding nearest-center difference: **1.2170047 Hz**.

These are single-subject descriptive quantities only.

## 4. Session-level Limit-Map warnings

### ses-t1

- channels: 64;
- fixed-model mean peak count: **1.359375**;
- fixed zero-peak channels: **0**;
- channels reaching the maximum allowed peak count: **7**;
- total width-boundary hits: **3**;
- fixed-vs-knee model-family disagreement channels: **34 / 64 = 0.53125**.

### ses-t2

- channels: 64;
- fixed-model mean peak count: **1.359375**;
- fixed zero-peak channels: **0**;
- channels reaching the maximum allowed peak count: **5**;
- total width-boundary hits: **1**;
- fixed-vs-knee model-family disagreement channels: **30 / 64 = 0.46875**.

## 5. Scientific interpretation

The pilot does **not** justify promoting the descriptive parameterization layer as a stable subject-level biomarker.

Two different facts coexist:

1. several descriptive quantities are repeat-close in this subject, including a small median first-peak center difference and moderate median exponent difference;
2. peak-count identity is only about 67%, and roughly half the channels show a fixed-versus-knee model-family disagreement warning in each session.

That disagreement is scientifically important because the known-truth program already showed that aperiodic model misspecification can manufacture or alter apparent periodic structure.

The correct response is therefore **not** to tune the settings after seeing this subject, and also not to reject the candidate from one subject using a post-hoc cutoff.

## 6. Decision

Current disposition:

`DESCRIPTIVE_PARAMETERIZATION_PILOT_EXECUTES_WITH_SUBSTANTIAL_MODEL_FAMILY_LIMITS`

The next use of this configuration is **population Limit-Map characterization across the frozen 42 repeat subjects**, not biomarker promotion.

The 42-subject expansion must quantify, subject-aware:

- exponent repeatability;
- peak-count repeatability;
- zero-peak prevalence and repeatability;
- center-frequency repeatability under an explicit peak-matching rule;
- width-boundary-hit prevalence;
- maximum-peak-count saturation;
- fixed-versus-knee disagreement prevalence and repeatability;
- regional/channel dependence;
- sensitivity to the already-declared Welch nuisance settings.

No threshold may be selected to make the repeatability look better after population results are seen.

## 7. Interpretation firewall

Still prohibited:

- descriptive peak center = natural frequency by default;
- descriptive bandwidth = damping;
- descriptive peak = dynamical mode;
- any local chi from this layer;
- whole-brain chi;
- clinical classification;
- prognosis;
- declaring a trait biomarker from one repeat pair.

## 8. Forward consequence

The pilot has done its job: it revealed both usable repeat structure and a large model-family sensitivity that would have been invisible if only the preferred fit were reported.

The population scale-up is now required to determine whether that sensitivity is:

- stable and characterizable;
- region-dependent;
- subject-dependent;
- acquisition/state-dependent;
- or too large for this descriptive layer to support the intended Atlas role.
