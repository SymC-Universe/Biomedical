# Bio Chi N-B2/N-B3 Representation-Sufficiency P0-N v0.2

**Status:** TARGETED COLLISION COMPLETE / RESIDUAL CANDIDATE SURVIVES  
**Date:** 29 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Lifecycle:** Stage 1, P0-N prior to A0/APQ and any new substantial N-B2/N-B3 computation  
**Supersedes for current P0-N interpretation:** `BIO_CHI_NB2_NB3_REPRESENTATION_SUFFICIENCY_P0N_v0.1.md`

## Scientific question

What information about perturbation, transient amplification, and recovery is preserved or lost by progressively richer neural stability representations?

Candidate representation ladder:

1. local modal damping coordinates only;
2. local modal vector plus embedded eigenspectrum;
3. eigenspectrum plus non-normal/reactivity information;
4. propagator, resolvent, or finite-time gain structure;
5. perturbation-direction-dependent response and recovery structure;
6. broader modal/vector and system/conglomerate representation where identifiable.

No universal whole-system scalar is assumed.

## Existing internal known truth

The completed coupled-second-order fixtures already establish that:

- identical local damping ratios plus identical full eigenspectra can produce different transient amplification and recovery;
- identical local damping ratios can coexist with different embedded modal organization;
- locally stable modes can coexist with a globally unstable coupled system.

Canonical internal source:
`NSD_vNext/docs/CHI_SYSTEM_COUPLED_KNOWN_TRUTH_POSTRESULT_v0.1.md`.

These exact fixtures reject local-chi-only and eigenspectrum-only sufficiency for the tested transient/recovery questions but do not provide a broad representation-sufficiency map.

## Targeted prior-art collision

The targeted collision confirms that the following components are established prior art and cannot carry novelty alone.

### Non-normal transient amplification

`Regimes and mechanisms of transient amplification in abstract and biological neural networks` (PMCID: PMC9377633) explicitly separates eigenspectrum from feed-forward/non-normal structure and shows that eigenspectrum alone is insufficient to determine transient behavior.

`Coding with transient trajectories in recurrent neural networks` (PMCID: PMC7043794) develops transient amplification in non-normal recurrent systems using propagator singular values and input/output directions.

Therefore these generic claims are prior art:

- non-normality can support transient amplification;
- asymptotic spectrum is not sufficient for finite-time response;
- perturbation direction matters for amplification.

### Data-driven modal/operator identification in neural data

`Non-Stationary Dynamic Mode Decomposition` (PMCID: PMC10705813 / PMC10441341) extends DMD to time-varying spatiotemporal modes and applies it to multichannel non-human-primate neural recordings.

`Inferring context-dependent computations through linear approximations of prefrontal cortex dynamics` (PMCID: PMC11654703) explicitly quantifies non-normality in fitted neural dynamical models.

Therefore modal/operator estimation, time-varying modes, and fitted non-normal neural dynamics are prior art.

### Perturbation-response and control structure

`Individualized perturbation of the human connectome reveals reproducible biomarkers of network dynamics relevant to cognition` (PMCID: PMC7149310) uses TMS-EEG perturbations to reveal reproducible propagation patterns not captured by canonical resting-state measures.

`Quantifying State-Dependent Control Properties of Brain Dynamics from Perturbation Responses` (PMCID: PMC12873642) estimates control properties from TMS-EEG perturbation responses and distinguishes overall controllability from controllable directions.

A 2026 reviewed preprint, `Designing optimal perturbation inputs for system identification in neuroscience`, further treats perturbation design for system identification and explicitly encounters non-normality as a methodological issue. This is active edge literature, not relied upon as settled novelty ownership.

Therefore perturbation-based system identification, controllability structure, and response-direction information are also established components.

### Recovery and return-to-baseline dynamics

Neural recovery after anesthesia, brain injury, and direct perturbation has been studied using EEG, TMS-EEG, fMRI, and invasive recordings. Existing literature documents return-to-baseline timing, state-transition structure, propagation, and recovery-dependent network reorganization.

Therefore “brain recovery after perturbation” is not itself a novel research target.

## Collision result

**No directly equivalent nested representation-sufficiency benchmark was located in this targeted pass** that prospectively compares a hierarchy such as local damping -> eigenspectrum -> non-normal/reactivity -> finite-time propagator -> recovery structure while asking, for each declared stability question, which representation is sufficient, equivalent, additive, or refusing.

This is **not proof of novelty**. It is the outcome of the current targeted collision and must remain open to additional search.

The residual therefore survives only in narrow form:

`NEW_INTEGRATION` primary / candidate `NEW_DISCRIMINATING_TEST`.

It does not survive as:

- a new theory of non-normality;
- discovery that eigenvalues are insufficient;
- discovery of transient amplification;
- discovery of DMD in neural data;
- discovery of perturbation-response neuroscience;
- discovery of recovery trajectories.

## Residual candidate contribution

A governed representation-sufficiency Function/Limit map that prospectively asks:

- which representation layers preserve declared perturbation/recovery observables;
- where lower-dimensional representations are empirically equivalent to richer ones;
- where richer representations add reproducible information;
- where representation becomes nonidentifiable, projection-dependent, or sampling-sensitive;
- how local chi and broader Chi/system structure should be interpreted jointly without substitution;
- where no coherent scalar or compact representation is justified.

The output is a map, not an overall score or universal hierarchy.

## Prospective known-truth design space

Any later APQ-qualified plan should balance ordinary Function and adversarial Limit regions and vary, without tuning to desired outcomes:

- local damping;
- embedded eigenspectrum;
- eigenvector conditioning/non-normality;
- numerical abscissa/reactivity;
- coupling topology;
- finite-time propagator gain;
- perturbation direction;
- asymptotic stability;
- recovery time and trajectory shape;
- observation projection;
- sampling and finite duration;
- model-order and nonstationarity challenges.

Matched-pair constructions should deliberately include:

- same local chi, different system behavior;
- same local chi plus same spectrum, different transient/recovery behavior;
- different lower-level coordinates but equivalent target response;
- richer representation that adds no useful information;
- richer representation that is necessary;
- representation refusal / nonidentifiability.

## Claim ceiling

P0-N / A0 candidate only.

No empirical neural result, disease inference, real-EEG local-chi admission, whole-system scalar, universal representation ranking, or claim that SymC originated non-normal neural transient theory is licensed.
