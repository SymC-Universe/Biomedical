# NSD Literature Collision Addendum v0.2

Date: 14 September 2026
Status: ACTIVE PRIOR-ART COLLISION
Scope: targeted follow-up on (1) explicit neural damping/model routes, (2) aperiodic-exponent limits, (3) refusal/abstention, and (4) multimodal architecture.

## 1. Explicit neural damping is real prior art, but model-conditional

### 1.1 Macaque V1 gamma

Spyropoulos et al. (2022), *Nature Communications*, `10.1038/s41467-022-29674-x`, modeled visually induced macaque V1 gamma with a noise-driven damped harmonic oscillator. The model reproduced LFP power spectra and cycle-level amplitude/duration structure and was connected to a linear E-I circuit.

Collision result: **ANSWERED IN A RESTRICTED PREPARATION**.

What this closes:
- neural damping is not merely a metaphor;
- a second-order stochastic oscillator can be physically useful for some neural rhythms.

What remains open:
- whether comparable modes are identifiable in the target resting scalp EEG datasets;
- whether damping estimates remain stable under source mixing, nonstationarity, finite windows, and low SNR;
- whether such estimates add information beyond standard spectral/modal features.

### 1.2 Human sEEG auditory responses

Pesnot Lerousseau et al. (2021), *Journal of Neuroscience*, *Frequency Selectivity of Persistent Cortical Oscillatory Responses to Auditory Rhythmic Stimulation*, fit a linear damped harmonic oscillator to sEEG responses. The model included eigenfrequency, transmission delay, and damping ratio. Reported clusters included low-frequency overdamped responses and a high-frequency underdamped cluster near 60 Hz.

Collision result: **ANSWERED IN A STIMULUS-LOCKED HUMAN INTRACRANIAL SETTING**.

Implication for NSD:
- a damping ratio can be estimated from human neural data when the experiment and model explicitly support it;
- this strengthens the case for a model-admission route rather than a blanket ban on neural chi;
- it simultaneously strengthens the firewall against inferring chi from arbitrary resting spectral peaks.

### 1.3 Neural-mass complex poles

Moran et al. (2007), *NeuroImage*, `10.1016/j.neuroimage.2007.05.032`, use neural-mass transfer functions and complex poles. The real component of a pole governs exponential growth/decay around the fixed point and the imaginary component gives oscillatory frequency.

Collision result: **ESTABLISHED NATIVE DYNAMICAL ROUTE**.

Implication:
- pole geometry is a more principled candidate bridge to local stability than relabeling a descriptive bandwidth;
- identifiability and local-linearization assumptions remain mandatory.

## 2. Aperiodic exponent cannot carry the old direct-chi interpretation

### 2.1 Reliability is condition-dependent

McKeown et al. (2023/2024), *Cerebral Cortex*, `10.1093/cercor/bhad482`, found generally useful test-retest reliability for several SpecParam features in 49 healthy young adults, but poorer performance in eyes-open recordings and weaker reliability for some periodic features.

Collision result: **BASIC RELIABILITY PARTIALLY ANSWERED, NOT UNIVERSAL**.

### 2.2 Mechanistic E/I mapping fails as a universal rule

Salvatore et al. (2024), *Journal of Neurophysiology*, `10.1152/jn.00445.2023`, used pharmacological and chemogenetic manipulations and concluded that the aperiodic exponent is not a universally reliable marker of cortical excitation/inhibition ratio.

Collision result: **OLD DIRECT CHAIN REJECTED**.

Frozen NSD rule:

`aperiodic exponent != universal E/I ratio != gamma != dynamical chi`.

The exponent remains useful as an empirical coordinate and may participate in multivariate architecture.

## 3. Refusal and abstention are not themselves novel

A 2026 EEG seizure-detection study in *Computer Methods and Programs in Biomedicine* (`10.1016/j.cmpb.2026.109520`) uses uncertainty-based selective classification to defer unreliable EEG predictions. Other current clinical-ML work likewise treats abstention as a legitimate safety mechanism.

Collision result: **ABSTENTION / REFUSAL AS A GENERAL METHOD IS PRIOR ART**.

Therefore NSD must not claim novelty for “the model can refuse.”

Residual NSD question:
- whether **structural non-admission patterns** such as no admissible mode, unresolved mode, failed dynamical identification, or persistent estimator disagreement are themselves reproducible neurophysiological phenotypes after technical causes are controlled.

This is materially different from classifier confidence abstention and remains open.

Required test:
1. freeze refusal reasons before labels;
2. measure repeated-session reliability of each refusal class;
3. control SNR, montage, duration, device/site, and preprocessing;
4. test whether refusal prevalence/geometry associates with phenotype on held-out subjects;
5. compare against simple data-quality explanations;
6. classify the result ADDS/EQUIVALENT/SUBTRACTS/INDETERMINATE.

## 4. Multimodal integration is established prior art

Concurrent EEG-fMRI reviews and multimodal DCM work already establish that complementary modalities can constrain latent neural dynamics better than one modality alone. Wei et al. (2020), *NeuroImage*, `10.1016/j.neuroimage.2020.116595`, explicitly ask whether EEG/fMRI fusion better characterizes functional brain architectures using a shared neuronal generative model.

Collision result: **MULTIMODAL INTEGRATION ITSELF IS NOT NSD NOVELTY**.

Residual NSD question:
- whether the same frozen stability architecture, including admission/refusal logic and independent Atlas reference, produces coherent but non-identical projections across modalities.

A valid future multimodal test must avoid converting every modality into the same scalar by construction.

## 5. Non-identifiability remains a native modeling problem

Recent neural-model literature continues to show that parameter non-identifiability can bias interpretation. This supports the NSD requirement that an apparently clean parameter estimate is not admissible merely because an optimizer returned it.

Collision result: **IDENTIFIABILITY CONTROL IS PRIOR ART AND MANDATORY, NOT NOVELTY**.

Residual contribution can only lie in how the forward NSD architecture operationalizes this control across spectral, modal, scalar, spatial, and clinical layers.

## 6. Revised residual novelty boundary

The following are now explicitly removed from novelty language:
- neural damped-oscillator fitting;
- neural-mass pole analysis;
- periodic/aperiodic decomposition;
- normative EEG deviation modeling;
- cross-disorder EEG overlap;
- multimodal EEG/fMRI integration;
- no-peak handling;
- model abstention/refusal in the generic ML sense;
- parameter-identifiability safeguards.

The strongest remaining candidate contribution is the **governed conjunction**:

`native observables + qualified modal structure + dynamically admitted local scalars where earned + spatial/conglomerate organization + explicit structural refusals + independent Atlas + Function/Limit Maps + native comparator accounting`.

This conjunction is still only a candidate contribution until it demonstrates incremental empirical value.

## 7. New falsification pressure created by this collision

The forward NSD program should fail or narrow if any of the following occur:

1. descriptive periodic/aperiodic features match or beat the full architecture on frozen tasks;
2. modal/damping routes are non-identifiable in the target data regime;
3. structural refusal patterns are explained entirely by SNR/site/device/preprocessing;
4. spatial organization adds no reproducible information beyond global summaries;
5. disorder differences collapse after age/medication/site controls;
6. cross-disorder common structure disappears when disorder-specific organization is preserved;
7. multimodal projections disagree beyond expected measurement differences;
8. healthy-reference geometry changes materially when transferred across datasets without retuning.

These are not implementation failures to hide. They define the Limit Map and the evidence ceiling.

## 8. Immediate design consequence

No more broad literature search is needed to establish whether “neural damping exists.” It does, under restricted explicit models.

The next literature work should be narrower:
- scalp-EEG identifiability of second-order/state-space oscillator parameters;
- empirical effects of montage/reference/source mixing on modal decay estimates;
- repeated-session reliability of modal/state-space parameters;
- whether structural model failures carry phenotype information after quality control.

Those searches can proceed while computation is pending, but the next major scientific gain now requires executing the qualification matrix on real and known-truth data.