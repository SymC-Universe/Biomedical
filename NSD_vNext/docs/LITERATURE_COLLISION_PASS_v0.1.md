# NSD Experimental Literature Collision Pass v0.1

Status: ACTIVE / DEEPENED PASS
Date: 14 September 2026
Purpose: determine which proposed NSD experiments are already answered, partially answered, or remain open.

## LC-01 — Repeated-session reliability of periodic and aperiodic EEG

Disposition: `PARTIALLY_ANSWERED`.

Existing work already establishes that periodic and aperiodic spectral parameterization can show fair-to-good or excellent test-retest reliability under some conditions, while reliability and model-fit quality vary by state, channel, feature, and developmental context.

Key sources:
- McKeown et al., *Test-retest reliability of spectral parameterization by 1/f characterization using SpecParam*, Cerebral Cortex 34(1), bhad482, DOI `10.1093/cercor/bhad482`. Three sessions in 49 healthy young adults; generally good aperiodic and alpha/beta reliability, but eyes-open periodic parameterization and some fits were substantially weaker.
- *Test-Retest Reliability of EEG Aperiodic Components in Resting and Mental Task States*, 2024. Reliability depended on duration, state, and estimation method.
- *Long-term reliability and stability of parameterized resting state EEG: evidence from a five-year follow-up*, Cerebral Cortex, 2026. Reports fair-to-excellent long-term reliability with age-related change in some parameters.

Residual NSD question:
The novelty is not simply asking whether SpecParam features are reliable. The remaining question is whether a combined spectral/modal/system architecture has reproducible within-subject structure, which components behave as traits versus states, and whether scalar-admission/refusal status itself is stable across sessions and ordinary perturbations.

## LC-02 — Transdiagnostic spectral overlap

Disposition: `ANSWERED_FOR_BASIC_BAND_POWER_OVERLAP`, `OPEN_FOR_FULL_NSD_ARCHITECTURE`.

Existing literature already shows substantial cross-disorder overlap and within-disorder heterogeneity in resting EEG band-power findings.

Key source:
- Newson & Thiagarajan, *EEG Frequency Bands in Psychiatric Disorders: A Review of Resting State Studies*, Frontiers in Human Neuroscience, 2019. Review of 184 studies across depression, ADHD, autism, addiction, bipolar disorder, anxiety, panic disorder, PTSD, OCD, and schizophrenia; reports substantial overlap, contradictory results, and limited disorder specificity.

Recent transdiagnostic literature also explicitly argues for dimensional rather than diagnosis-specific EEG biomarkers.

Residual NSD question:
NSD cannot claim novelty for observing that EEG abnormalities overlap across diagnoses. The residual claim must concern whether a richer architecture combining spectral state, admissible modal/scalar structure, spatial organization, categorical absent-feature states, and system relationships provides reproducible information beyond existing transdiagnostic spectral approaches.

## LC-03 — ASD resting EEG spectral differences

Disposition: `ANSWERED_FOR_BASIC_CASE_CONTROL_BAND_POWER`, `OPEN_FOR_ARCHITECTURE_AND_TRANSFER`.

Key source:
- Neo et al., *Resting-state EEG power differences in autism spectrum disorder: a systematic review and meta-analysis*, Translational Psychiatry, 2023. Forty-one studies, 1,246 autistic and 1,455 neurotypical participants; reduced relative alpha and increased gamma were reported, with substantial heterogeneity across bands and methodological moderators.

Residual NSD question:
A new ASD analysis must not merely reproduce band-power separation. It must test incremental architecture: periodic/aperiodic decomposition, spatial/modal organization, scalar-admission status, subject-aware validation, and native-baseline comparison.

## LC-04 — ASD versus ADHD transdiagnostic EEG

Disposition: `PARTIALLY_ANSWERED`.

A 2026 comparative review reports candidate convergence in low-frequency/theta and alpha-modulation features across ASD and ADHD while emphasizing heterogeneity and the absence of evidence needed for individual-level biomarker-guided treatment assignment.

Residual NSD question:
The open opportunity is not generic convergence. It is whether a prespecified multilevel state-space representation can distinguish shared architecture from disorder-specific organization and whether it generalizes across independent datasets without disorder-specific baseline retuning.

## LC-05 — Longitudinal EEG prediction

Disposition: `PARTIALLY_ANSWERED_BY_DISORDER-SPECIFIC_STUDIES`.

Published work already uses EEG and machine learning to predict treatment response in psychiatric disorders, including longitudinal antidepressant response. Therefore NSD cannot claim novelty simply for using EEG to predict future clinical outcomes.

Residual NSD question:
Any NSD prediction study must test a frozen incremental-value claim against strong native predictive models and show whether stability-architecture features add information beyond conventional EEG and clinical predictors.

## LC-06 — Damping, Q factor, complex poles, and neural oscillations

Disposition: `PARTIALLY_ANSWERED / MODEL-CONDITIONAL ROUTE EXISTS`.

The deeper pass changes the initial conclusion in an important way. Damped-oscillator and pole-based interpretations are not foreign to neurophysiology. There are genuine examples where neural data are explicitly fit with dynamical oscillator models, and some EEG literature uses Q-factor language. What remains unsupported is the **blanket conversion of routine spectral peak width or aperiodic slope into a canonical neural damping ratio**.

### Direct dynamical examples

1. Hindriks et al. (2011), *Dynamics underlying spontaneous human alpha oscillations: A data-driven approach*, NeuroImage 57:440-451, DOI `10.1016/j.neuroimage.2011.04.043`.
   - Uses second-order stochastic differential equations.
   - Human MEG alpha is described as a noise-perturbed damped harmonic oscillator.
   - Parameters are estimated from data rather than inferred from a hand-drawn coordinate.
   - This establishes a legitimate precedent for testing a damped-oscillator model on neural rhythms.

2. Spyropoulos et al. (2022), *Spontaneous variability in gamma dynamics described by a damped harmonic oscillator driven by noise*, Nature Communications 13:2019, DOI `10.1038/s41467-022-29674-x`.
   - Awake macaque V1 LFP/spiking.
   - A noise-driven damped harmonic oscillator reproduces gamma amplitude-duration structure and power spectra.
   - The model is related to a linear E-I circuit.
   - This supports model-specific neural damping, not universal scalp-EEG damping.

3. *Frequency Selectivity of Persistent Cortical Oscillatory Responses to Auditory Rhythmic Stimulation* (2021).
   - Fits intracranial/sEEG responses directly to a damped harmonic oscillator with damping ratio, eigenfrequency, and delay parameters.
   - Demonstrates that underdamped/overdamped oscillator language can be used as an explicit neural-mass phenomenology when the experiment and model justify it.

4. Moran et al. (2007), *A neural mass model of spectral responses in electrophysiology*, NeuroImage 37:706-720, DOI `10.1016/j.neuroimage.2007.05.032`.
   - Uses a neural-mass generative model and transfer-function analysis.
   - Complex poles encode oscillatory frequency and local decay/growth around the operating point.
   - Provides a rigorous modal route that is closer to the current SymC scalar/vector architecture than direct peak-width relabeling.

5. Jansen-Rit and related neural-mass literature formulates cortical population dynamics as coupled second-order nonlinear equations and can produce alpha/background/epileptiform regimes. This further supports a generative-model route to dynamical quantities.

### Q-factor precedent in clinical EEG

Jin et al. (2012), *Alpha EEG guided TMS in schizophrenia*, Brain Stimulation 5:560-568, DOI `10.1016/j.brs.2011.09.005`, used alpha peak frequency and half-power bandwidth to construct a Q factor and discussed it as frequency selectivity / decay behavior. The study reported association between Q-factor change and symptom improvement but explicitly described its findings as preliminary given trial limitations.

This is scientifically useful for NSD because it means “Q-like neural spectral sharpness” is not novel by itself. It also means NSD must avoid claiming that Q or damping language in EEG is unprecedented.

### Crucial unresolved distinction

The literature above does **not** imply:

`any EEG Gaussian peak width -> damping rate -> chi`

A direct dynamical fit, a neural-mass pole, and a Gaussian spectral bandwidth are different inferential objects.

Residual NSD question:
Can one or more model families recover reproducible mode-specific decay/frequency structure from the target EEG datasets, with known-truth validation and refusal when the model is not identifiable, and do those dynamical quantities add information beyond descriptive spectral features?

### Current decision

- Neural damping is a legitimate **candidate model layer**, not merely metaphor.
- Q/linewidth language has prior clinical EEG precedent.
- Routine SpecParam Gaussian bandwidth stays descriptive until a dynamical bridge is earned.
- Complex-pole / explicitly fitted stochastic-oscillator routes deserve priority testing because their dynamics are part of the model rather than attached after the fact.

## LC-07 — Aperiodic exponent as excitation/inhibition and historical NSD chi proxy

Disposition: `PARTIALLY_SUPPORTED_AS_CONTEXT-DEPENDENT_PROXY`, `REJECTED_AS_UNIVERSAL_DIRECT_CHI`.

The historical NSD supplement treated the aperiodic exponent as a direct chi proxy and assigned universal underdamped/adaptive/overdamped ranges. Current literature does not support that conversion.

Key evidence:
- Gao et al. (2017) motivated a relationship between field-potential spectral slope and excitation/inhibition balance under a specific modeling framework.
- Salvatore et al. (2024), *Periodic and aperiodic changes to cortical EEG in response to pharmacological manipulation*, Journal of Neurophysiology 131:529-540, DOI `10.1152/jn.00445.2023`, tested pharmacological and chemogenetic manipulations and concluded that the aperiodic exponent is not a universally reliable marker of cortical E/I ratio.
- Recent clinical papers continue to use the exponent as a promising E/I-related marker, but explicitly note limited biological specificity and the lack of universal cutoff values.
- A 2026 systematic review of aperiodic EEG and cognition supports functional relevance while also emphasizing methodological standardization and context dependence.

Residual NSD question:
Use the aperiodic exponent as a native spectral coordinate, test its reliability and regional organization, and only connect it to a mechanistic quantity through a separately validated model or perturbational experiment.

Current decision:

`aperiodic exponent != direct gamma != direct dynamical chi`

No historical exponent cutoffs transfer into the vNext evidence base.

## LC-08 — Spectral width as damping versus nonstationarity

Disposition: `OPEN_FOR_TARGET_DATA / PRINCIPLE ALREADY CLEAR`.

Neural spectra can broaden because of finite lifetime/decay, but also because of frequency drift, burstiness, source mixing, multiple unresolved modes, finite windows, and other nonstationarities. Oscillator and eigenmode papers derive linewidth/sharpness relationships only under specific generative assumptions.

Residual NSD task:
The Engine must compare at least one descriptive peak model with an explicit dynamical model and use adversarial simulations where broadening is generated without changing damping. This is now encoded in `KNOWN_TRUTH_ADVERSARIAL_TEST_MATRIX_v0.1.md`.

## Collision conclusion from the deepened pass

Several broad experimental ideas are already substantially represented in the literature:
- basic repeated-session spectral reliability is not novel;
- basic transdiagnostic band-power overlap is not novel;
- basic ASD resting-state band-power differences are not novel;
- EEG-based clinical prediction is not novel as a general idea;
- damped-oscillator models of neural rhythms are not novel;
- Q-factor descriptions in EEG are not novel;
- aperiodic exponent as an E/I-related proxy is not novel and is not universally mechanistic.

This narrows the scientifically defensible NSD opportunity in a productive way:

> **Test whether a rigorously qualified multilevel architecture can recover reproducible signal, modal, spatial, and system-level stability structure from neurophysiology; admit local dynamical chi only where a generative model earns it; preserve refusals and categorical absence; and determine whether this architecture adds information beyond standard periodic/aperiodic and clinical baselines while preserving disorder-specific structure.**

That residual question remains open and materially stronger than the 2025 claim that the architecture was already validated.