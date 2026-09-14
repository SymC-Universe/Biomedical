# NSD Experimental Literature Collision Pass v0.1

Status: ACTIVE / INITIAL PASS
Date: 14 September 2026
Purpose: determine which proposed NSD experiments are already answered, partially answered, or remain open.

## LC-01 — Repeated-session reliability of periodic and aperiodic EEG

Initial disposition: `PARTIALLY_ANSWERED`.

Existing work already establishes that periodic and aperiodic spectral parameterization can show fair-to-good or excellent test-retest reliability under some conditions, while reliability and model-fit quality vary by state, channel, feature, and developmental context.

Key initial sources:
- McKeown et al., *Test-retest reliability of spectral parameterization by 1/f characterization using SpecParam*, Cerebral Cortex, 2023/2024. Three sessions in 49 healthy young adults; generally good aperiodic and alpha/beta reliability, but eyes-open periodic parameterization and some fits were substantially weaker.
- *Test-Retest Reliability of EEG Aperiodic Components in Resting and Mental Task States*, 2024. Reliability depended on duration, state, and estimation method.
- *Long-term reliability and stability of parameterized resting state EEG: evidence from a five-year follow-up*, Cerebral Cortex, 2026. Reports fair-to-excellent long-term reliability with age-related change in some parameters.

Residual NSD question:
The novelty is not simply asking whether SpecParam features are reliable. The remaining question is whether a combined spectral/modal/system architecture has reproducible within-subject structure, which components behave as traits versus states, and whether scalar-admission/refusal status itself is stable across sessions and ordinary perturbations.

## LC-02 — Transdiagnostic spectral overlap

Initial disposition: `ANSWERED_FOR_BASIC_BAND_POWER_OVERLAP`, `OPEN_FOR_FULL_NSD_ARCHITECTURE`.

Existing literature already shows substantial cross-disorder overlap and within-disorder heterogeneity in resting EEG band-power findings.

Key initial source:
- Newson & Thiagarajan, *EEG Frequency Bands in Psychiatric Disorders: A Review of Resting State Studies*, Frontiers in Human Neuroscience, 2019. Review of 184 studies across depression, ADHD, autism, addiction, bipolar disorder, anxiety, panic disorder, PTSD, OCD, and schizophrenia; reports substantial overlap, contradictory results, and limited disorder specificity.

Recent transdiagnostic literature also explicitly argues for dimensional rather than diagnosis-specific EEG biomarkers.

Residual NSD question:
NSD cannot claim novelty for observing that EEG abnormalities overlap across diagnoses. The residual claim must concern whether a richer architecture combining spectral state, admissible modal/scalar structure, spatial organization, categorical absent-feature states, and system relationships provides reproducible information beyond existing transdiagnostic spectral approaches.

## LC-03 — ASD resting EEG spectral differences

Initial disposition: `ANSWERED_FOR_BASIC_CASE_CONTROL_BAND_POWER`, `OPEN_FOR_ARCHITECTURE_AND_TRANSFER`.

Key initial source:
- Neo et al., *Resting-state EEG power differences in autism spectrum disorder: a systematic review and meta-analysis*, Translational Psychiatry, 2023. Forty-one studies, 1,246 autistic and 1,455 neurotypical participants; reduced relative alpha and increased gamma were reported, with substantial heterogeneity across bands and methodological moderators.

Residual NSD question:
A new ASD analysis must not merely reproduce band-power separation. It must test incremental architecture: periodic/aperiodic decomposition, spatial/modal organization, scalar-admission status, subject-aware validation, and native-baseline comparison.

## LC-04 — ASD versus ADHD transdiagnostic EEG

Initial disposition: `PARTIALLY_ANSWERED`.

A 2026 comparative review reports candidate convergence in low-frequency/theta and alpha-modulation features across ASD and ADHD while emphasizing heterogeneity and the absence of evidence needed for individual-level biomarker-guided treatment assignment.

Residual NSD question:
The open opportunity is not generic convergence. It is whether a prespecified multilevel state-space representation can distinguish shared architecture from disorder-specific organization and whether it generalizes across independent datasets without disorder-specific baseline retuning.

## LC-05 — Longitudinal EEG prediction

Initial disposition: `PARTIALLY_ANSWERED_BY_DISORDER-SPECIFIC_STUDIES`.

Published work already uses EEG and machine learning to predict treatment response in psychiatric disorders, including longitudinal antidepressant response. Therefore NSD cannot claim novelty simply for using EEG to predict future clinical outcomes.

Residual NSD question:
Any NSD prediction study must test a frozen incremental-value claim against strong native predictive models and show whether stability-architecture features add information beyond conventional EEG and clinical predictors.

## LC-06 — Damping/Q-factor interpretation of neural oscillations

Initial disposition: `OPEN / REQUIRES DEEPER TARGETED REVIEW`.

The first search did not establish a standard psychiatric EEG practice that directly interprets routine scalp-EEG peak width as a canonical mechanical damping ratio. However, resonance, oscillator, linewidth, decay-time, and neural-mass literatures are broad, so absence cannot yet be claimed.

Required next search:
- neural mass/model pole damping;
- stochastic oscillator models of EEG/MEG;
- resonance linewidth and Q in cortical oscillations;
- damped harmonic oscillator fitting to neural spectra;
- relationships among spectral bandwidth, autocorrelation time, and pole decay;
- methods distinguishing lifetime broadening from nonstationary/heterogeneous broadening in neural signals.

Until that review closes, routine EEG bandwidth must remain a spectral feature rather than a dynamical damping rate unless the individual model explicitly licenses the conversion.

## Collision conclusion from initial pass

Several broad experimental ideas are already substantially represented in the literature. This is useful rather than damaging:

- basic repeated-session spectral reliability is not novel;
- basic transdiagnostic band-power overlap is not novel;
- basic ASD resting-state band-power differences are not novel;
- EEG-based clinical prediction is not novel as a general idea.

The residual NSD opportunity is narrower and scientifically stronger: test whether a rigorously licensed, multilevel stability architecture provides incremental, reproducible structure beyond periodic/aperiodic spectral parameterization and standard clinical/neurophysiological baselines, while preserving refusal, spatial organization, subject hierarchy, and disorder-specific differences.
