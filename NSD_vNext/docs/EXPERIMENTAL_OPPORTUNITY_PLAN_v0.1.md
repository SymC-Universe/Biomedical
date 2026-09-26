# NSD Experimental Opportunity Plan v0.1

Status: ACTIVE P0-D DESIGN / INITIAL COLLISION COMPLETE
Date: 14 September 2026

Purpose: design discriminating neurophysiological experiments or observational studies before searching for prior work, then perform a literature-collision pass to determine what remains genuinely unanswered.

## Collision-informed rule

The first collision pass establishes that several broad questions are already substantially answered:
- periodic/aperiodic EEG can be test-retest reliable under some conditions;
- transdiagnostic and dimensional psychopathology is established;
- psychiatric EEG abnormalities and heterogeneity overlap across diagnoses;
- normative healthy-reference EEG modeling already exists;
- basic ASD band-power differences are established;
- generic EEG clinical prediction already exists;
- damped-oscillator, pole, linewidth, and Q-factor concepts already exist in restricted neural models.

Therefore the experiments below are retained only where their **residual NSD question** remains open.

## Candidate experiment family 1 — repeated-session recovery

### Residual question
Which **multilevel** NSD features behave as stable subject traits, which are state-dependent, which recover after perturbation, and is the admission/refusal status of a candidate dynamical mode itself reproducible?

Design concept:
- repeated within-subject recordings;
- standardized baseline plus a controlled state perturbation where ethically appropriate;
- repeated post-perturbation measurements;
- preserve spectral, modal, spatial, scalar-admission, conglomerate, and open-channel outputs;
- estimate within-subject recovery and between-subject variability;
- compare with ordinary periodic/aperiodic and spectral reliability.

Discriminates:
- stable architecture versus session noise;
- local/modal recovery versus whole-system reorganization;
- trait-like versus state-like candidate coordinates;
- stable refusal versus estimator instability.

Falsifiers:
- architecture is no more repeatable or informative than ordinary spectral baselines;
- apparent recovery is dominated by recording or fit noise;
- modal/scalar admission changes erratically across nominally equivalent sessions;
- the more complex representation subtracts reliability without adding interpretable information.

Collision state: `PARTIALLY_ANSWERED FOR SIMPLE FEATURES / OPEN FOR FULL ARCHITECTURE`.

## Candidate experiment family 2 — controlled task/state transition

### Residual question
Can a frozen Engine distinguish expected physiological state changes from changes that would falsely be interpreted as altered damping/stability?

Candidate transitions:
- eyes open/closed;
- resting/task engagement;
- sensory stimulation;
- fatigue or vigilance transition when safely measured.

Design principle:
- predict which native observables should change and which should remain invariant before analysis;
- test whether descriptive width, mode decay, aperiodic structure, and spatial organization separate rather than moving as one manufactured scalar.

High-value use:
A controlled state transition is an adversarial test of the scalar-admission firewall. If ordinary vigilance changes produce large apparent chi shifts while the dynamical model is not identifiable, the scalar route should refuse rather than pathologize normal state variation.

Collision state: `PARTIALLY_ANSWERED FOR SPECTRAL FEATURES / OPEN FOR ADMISSION-FIREWALL TEST`.

## Candidate experiment family 3 — sleep/wake architecture

### Residual question
Do naturally occurring state transitions provide a high-information test of whether NSD preserves modal/system reorganization better than a single scalar or standard spectral summaries?

Why useful:
- large physiological state changes;
- repeated structure within individuals;
- strong native literature for comparison;
- opportunity to test where scalar reduction becomes non-identifiable or misleading.

Critical comparator:
Standard sleep-stage spectral and connectivity features.

Collision state: `OPEN AS NSD COMPARATOR EXPERIMENT / NATIVE PHYSIOLOGY HEAVILY ANSWERED`.

## Candidate experiment family 4 — direct dynamical-model challenge

### Residual question
Can the target EEG/MEG regime support identifiable mode-specific decay/frequency parameters under an explicit generative model, and can the Engine distinguish true damping change from other causes of spectral broadening?

Design:
- choose recordings with a strong, reproducible oscillatory mode;
- fit at least one descriptive periodic model and at least one explicit dynamical model;
- compare with synthetic known-truth recovery;
- perturb analysis duration, stationarity, and model order;
- where feasible use controlled rhythmic stimulation or naturally strong rhythms;
- preserve estimator disagreement as a result.

Required adversaries:
- frequency drift without damping change;
- two unresolved neighboring modes;
- burst-duration change;
- finite-window broadening;
- colored drive;
- aperiodic-only signal.

Success is not “a chi value appears.” Success is accurate recovery or scientifically correct refusal.

Collision state: `PRIOR ART EXISTS FOR DYNAMICAL MODELS / OPEN FOR TARGET-DATA QUALIFICATION`.

## Candidate experiment family 5 — multimodal structural validation

### Residual question
Do EEG-derived modal/system quantities correspond to independently measured organization, and do those correspondences survive stronger native comparators?

Potential independent modalities:
- MEG;
- fMRI connectivity;
- source-localized EEG where justified;
- structural/functional imaging covariates;
- perturbational/stimulation measurements where appropriate.

Purpose:
Validate system organization, not force one-to-one equivalence between modalities.

Collision state: `TARGETED PRIOR-ART PASS STILL REQUIRED`.

## Candidate experiment family 6 — longitudinal symptom transition

### Residual question
Can frozen NSD features predict change in symptom burden, relapse, conversion, treatment response, or recovery **beyond** clinical and conventional EEG predictors?

Requirements:
- prospective or genuinely untouched longitudinal outcomes;
- MFR-14;
- strong clinical/native comparator;
- subject-level split;
- calibration and uncertainty;
- no threshold retuning on outcome data;
- separate classification from prediction.

Collision state: `GENERIC EEG PREDICTION ALREADY EXISTS / INCREMENTAL NSD QUESTION OPEN`.

## Candidate experiment family 7 — transdiagnostic shared-versus-specific challenge

### Residual question
Do different diagnostic groups share reproducible architecture while preserving distinct phenotypic organization beyond RDoC/HiTOP-style dimensions, normative EEG deviations, and standard EEG feature spaces?

Design principle:
- freeze shared and disorder-specific metrics before combined outcome inspection;
- use common healthy Atlas reference;
- include multiple materially distinct diagnoses;
- model age/site/medication/state where available;
- compare diagnosis labels against symptom-dimensional models;
- quantify within-diagnosis heterogeneity rather than only group centroids;
- require shared structure **and** preserved disorder-specific structure for a shared-instability claim.

Collision state: `TRANSDIAGNOSTIC DIRECTION ESTABLISHED / NSD-SPECIFIC ARCHITECTURE OPEN`.

## Candidate experiment family 8 — refusal as measurable phenotype

### Residual question
Is the inability to identify a qualifying mode a reproducible biological/signal phenotype rather than random fitting failure?

Design:
- prespecify fit and signal-quality gates;
- distinguish no-peak, poor-fit, non-identifiable-mode, model-disagreement, and out-of-domain states;
- test repeatability across sessions;
- test dependence on SNR, duration, hardware, and state;
- only after technical controls, compare refusal distributions across phenotypes.

Falsifier:
Refusal status is mostly explained by recording quality, duration, site, or arbitrary fitting thresholds.

Collision state: `CANDIDATE HIGH-VALUE RESIDUAL / TARGETED PRIOR-ART SEARCH REQUIRED`.

## Candidate experiment family 9 — preserved-spatial-information challenge

### Residual question
Does retaining channel/regional/modal participation provide reproducible information beyond whole-head or global spectral summaries?

Design:
- same subjects and same frozen task;
- compare global summary, regional representation, and full qualified spatial/modal representation;
- assess transfer, reliability, and clinical incremental value;
- explicitly model reference/volume-conduction sensitivity.

Falsifier:
Spatial architecture adds no stable information beyond conventional regional/simple spectral features.

Collision state: `OPEN AS INCREMENTAL COMPARATOR QUESTION`.

## Literature-collision sequence

For each candidate family:
1. freeze the scientific question and discriminating observation;
2. list the simplest experiment that could answer it;
3. identify expected native comparators and confounders;
4. search peer-reviewed literature and open datasets for experiments that already answer the question;
5. classify each proposed experiment as `ANSWERED`, `PARTIALLY_ANSWERED`, `OPEN`, or `NOT_FEASIBLE_CURRENTLY`;
6. inherit existing results where adequate;
7. retain only the residual experiment that would add information.

## Updated priority order

1. direct dynamical-model qualification and broadening adversaries;
2. refusal-status prior art and repeatability;
3. repeated-session multilevel architecture and scalar-admission stability;
4. preserved spatial/modal information versus simpler baselines;
5. multimodal validation of modal/system organization;
6. transdiagnostic shared-versus-specific architecture beyond normative EEG and dimensional psychopathology;
7. longitudinal incremental prediction only after earlier layers qualify.

## Immediate experimental conclusion

The project no longer needs to spend novelty capital proving facts the field already knows. The most discriminating experiments are now the ones that test the **measurement architecture itself**:

- can it recover a dynamical quantity when one is truly present;
- can it refuse when the quantity is not identifiable;
- can it distinguish damping from drift, burstiness, multiple modes, and noise;
- can it preserve useful spatial/modal structure;
- and only then, does any of that add reproducible information about clinical phenotypes?

No experiment is called novel until its specific collision pass is complete.