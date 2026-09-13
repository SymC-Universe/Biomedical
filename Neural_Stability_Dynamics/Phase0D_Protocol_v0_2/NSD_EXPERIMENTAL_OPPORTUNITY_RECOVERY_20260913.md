# NSD Experimental Opportunity Sketch: Perturbation Recovery

Date: 2026-09-13
Protocol basis: General Protocol v0.7.4 Section 50.2
Status: **P0-D independent experimental ideation recorded before targeted prior-experiment/literature collision. Not a preregistration. Not P1.**

## E0 - Experimental opportunity trigger
`YES` scientifically. A controlled non-invasive neural perturbation with continuous multichannel recording could directly test whether a pre-perturbation system model predicts recovery organization. Physical execution with human participants is not authorized by this document and would require appropriate ethics approval, trained personnel, equipment, consent, and safety procedures.

## E1 - Native-question statement
Question: **Can a pre-perturbation multichannel neural dynamical model predict the order, timescale, and modal reorganization of recovery after a controlled perturbation better than local/uncoupled descriptions alone?**

Native system: multichannel EEG or another non-invasive neural time series with a precisely timed external perturbation.

Candidate perturbation for the first mechanism-specific design: a brief, standardized visual or auditory stimulation block/pulse followed by a sufficiently long unstimulated recovery interval.

Native observables include, where identifiable without Atlas labels:
- multichannel time series and evoked/recovery trajectories;
- spectral state and complete peak structure;
- state-space poles/eigenvalues and supported modal/subspace structure;
- channel/output participation;
- perturbation-to-recovery decay order and timescale;
- residual structure and model adequacy during recovery.

The scientific distinction is between predictions made from the admitted pre-perturbation system model and predictions made from local/uncoupled or simpler native baselines.

## E2 - Independent experimental game plan

### Design
1. Record a stable pre-perturbation baseline.
2. Fit the candidate System Model / Engine using only baseline and, where explicitly allowed by the model, the known perturbation input definition. Do not use post-perturbation recovery outcomes for model selection or tuning.
3. Deliver the standardized sensory perturbation.
4. Continue recording through the recovery interval.
5. From the pre-perturbation model, generate prospective predictions for supported recovery quantities before opening the corresponding recovery data.
6. Compare predicted and observed recovery trajectories, modal persistence/reorganization, and refusal/adequacy behavior.

### Candidate model form
Where a local linear representation is adequate:
`dx/dt = A x + B u`
`y = C x + v`
with `u(t)` the known perturbation input. After stimulus offset, predicted local return follows the admitted closed-loop dynamics. This representation is a testable approximation, not a claim that neural dynamics are globally linear.

### Primary comparison structure
Compare at least:
- full admitted coupled/closed-loop model;
- local/uncoupled subsystem model or ablated-coupling model;
- strongest domain-native recovery/evoked-response baseline identified later during the literature-collision audit.

No comparator is frozen in this E2 sketch because targeted prior-experiment/comparator searching comes after this record.

### Candidate prediction targets
Where supported by identifiability and measurement quality:
- ordering of recovery across admitted lineages/subspaces;
- asymptotic/local decay scale;
- finite-time transient amplification or overshoot in a justified normalized metric;
- persistence, disappearance, splitting, merging, or reorganization of admitted modes/subspaces;
- whether the pre-perturbation reduction remains adequate during recovery;
- correct refusal when the perturbation drives the system outside the model-validity regime.

### Function Map target
Map ordinary successful recovery across perturbation strengths/conditions that remain ethically and scientifically appropriate. Determine how coupling/feedback architecture changes the recovery trajectory while the system remains in a supported regime.

### Limit Map target
Identify where recovery prediction degrades, modal identity becomes unresolved, the scalar description ceases to be adequate, transient excursions become large, or the Engine correctly refuses. No failure boundary is prespecified here.

### Falsifying outcomes for the candidate predictive idea
The coupled architecture would fail to earn added predictive value if, on genuinely untouched recovery observations, it does not improve the prespecified prediction target relative to the strongest fair local/native comparator, predicts the wrong recovery ordering/trajectory, or requires post-outcome retuning to recover performance.

A model-adequacy/refusal outcome is not automatically a failure of nature and must remain in the method-validity namespace unless separately promoted.

### Uncertainty / confounders to control or record
- trial-to-trial variability;
- vigilance and fatigue;
- eye/muscle artifact;
- electrode impedance / channel loss;
- stimulus timing jitter;
- baseline nonstationarity;
- filtering/reference choices;
- session and subject dependence;
- estimator/order uncertainty;
- observability and crowding;
- multiple tested windows/endpoints;
- state-coordinate scaling used for transient-gain calculations.

### Apparatus / resources
A realistic physical implementation would require an appropriately sampled multichannel EEG system, synchronized stimulus presentation/triggering, artifact monitoring, controlled recording environment, qualified human-subject procedures, analysis workstation, and reproducible acquisition/preprocessing software. A pilot should qualify timing, data quality, observability, and the complete production analysis path before any larger study.

### Replication architecture
Use repeated perturbations within session for estimator qualification while preserving subject/session independence. Any confirmatory claim would require an untouched decisive evidence split and full MFR-14 registration before those data are opened.

### Safety / ethics
Human-participant execution requires ethics/IRB or equivalent institutional review as applicable, informed consent, qualified supervision, and stimulus parameters within accepted non-invasive safety limits. This document does not authorize unsupervised human experimentation.

## E3 - Cross-mechanism challenge
For the first experiment, the claim is intentionally mechanism-specific to a controlled sensory perturbation, so cross-mechanism confirmation is `NOT_APPLICABLE` at this stage.

If the later claim expands to a general neural recovery architecture, a materially different perturbation mechanism must be tested independently, for example an endogenous state transition or another safe domain-native perturbation rather than repeated variants of the same sensory drive.

## Firewall before E4
This record predates the targeted search for prior experiments answering this exact question. The subsequent literature-collision audit must determine what is already answered, what methods/comparators should be inherited, and whether any residual experiment remains worth performing.

Atlas labels, disease/control outcomes, desired chi regions, and the separately timestamped `chi~1.2-1.3` hypothesis are prohibited from selecting the coordinate, coupling architecture, recovery endpoint, or success criterion.