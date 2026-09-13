# NSD Recovery Experimental Opportunity: Literature Collision Audit

Date: 2026-09-13
Protocol basis: General Protocol v0.7.4 Section 50.2 E4-E6
Status: **P0-D LITERATURE COLLISION. NOT A NOVELTY CERTIFICATE. NOT P1.**
Pre-search ideation record: `NSD_EXPERIMENTAL_OPPORTUNITY_RECOVERY_20260913.md`, committed before this targeted search at `d5ad6c65953fb5cf5821e6af70abc9848d40350b`.

## E4 classification

- `PARTIALLY_ANSWERED`
- `METHOD_AVAILABLE`
- `KNOWN_TRUTH_TESTBED`
- `RESIDUAL_QUESTION_IDENTIFIED`

`NO_CLOSE_PRECEDENT_FOUND` is **not** assigned. The targeted search found close and important prior work.

## Source-of-record table

Retrieval date for all entries: 2026-09-13.

| Source | Evidence tier | What it already establishes | Relation to residual NSD question |
|---|---|---|---|
| Bonnard et al., **Resting state brain dynamics and its transients: a combined TMS-EEG study**, *Scientific Reports* 6, 31220 (2016), DOI `10.1038/srep31220` | FULL primary article | TMS-EEG was used explicitly to study relaxation toward rest after a transient perturbation; perturbing MPFC versus SPL produced different transient lifetime/amplitude and supported coupling-dependent relaxation. | Direct prior art for perturbation-and-recovery mapping. It does not by itself test the current residual question of a pre-perturbation identified closed-loop model prospectively predicting recovery order/modal reorganization against local/native baselines. |
| Chang et al., **Assessing Recurrent Interactions in Cortical Networks: Modeling EEG Response to Transcranial Magnetic Stimulation**, *Journal of Neuroscience Methods* 312, 93-104 (2019 issue; online/final edited 2018), DOI `10.1016/j.jneumeth.2018.11.006` | ABSTRACT / primary indexed record | Develops a state-space / multivariate autoregressive model with exogenous TMS input and observation equation; integrated recurrent-interaction model better explains complex wakeful TMS-EEG than segregated independent oscillators. | Very close prior art for the core mathematical architecture and for the importance of recurrent feedback. Model parameters are estimated using TMS-EEG response data; this is not the same as freezing a pre-perturbation model and prospectively scoring untouched recovery. |
| Momi et al., **Perturbation of resting-state network nodes preferentially propagates to structurally rather than functionally connected regions**, *Scientific Reports* 11, 12458 (2021), DOI `10.1038/s41598-021-90663-z` | ABSTRACT / primary indexed record | In 24 healthy participants with repeated TMS-EEG visits, perturbation propagation across DMN/DAN targets was predicted more strongly by structural than functional connectivity. | Establishes native propagation/connectivity comparators and that network architecture matters for perturbation spread. Does not resolve the proposed modal recovery/order/transient-resilience prediction question. |
| Maschke et al., **Critical dynamics in spontaneous EEG predict anesthetic-induced loss of consciousness and perturbational complexity**, *Communications Biology* 7, 946 (2024), DOI `10.1038/s42003-024-06613-8` | FULL primary article | Resting-state EEG dynamical/criticality measures predict individual TMS-derived perturbational complexity index values with high accuracy. | Strong prior art that pre-perturbation spontaneous dynamics can predict a later perturbation-response quantity. The predicted target is PCI, not the full recovery trajectory, modal reorganization, directed feedback response, or hierarchical closure. |
| Kabir et al., **Influence of Large-Scale Brain State Dynamics on the Evoked Response to Brain Stimulation**, *Journal of Neuroscience* 44(39):e0782242024 (2024), DOI `10.1523/JNEUROSCI.0782-24.2024` | ABSTRACT / PubMed primary record | Fast-fluctuating global EEG microstate before TMS changes the magnitude of the evoked response for up to about 80 ms; effect repeated within subjects, absent in sham, and replicated independently. | Strong evidence for state-dependent perturbation response and a required baseline comparator/stratification concept. It does not identify the current residual closed-loop recovery architecture. |
| Callaert et al., **Exploratory decoding of TMS-EEG: Predicting TEP response to intermittent and continuous theta burst stimulation**, *NeuroImage* 334, 121957 (2026), DOI `10.1016/j.neuroimage.2026.121957` | ABSTRACT / primary article record | Resting-state EEG spectral power and connectivity features were used with linear/nonlinear machine-learning models to predict post-iTBS/cTBS TEP component changes; authors report performance above random baselines and explicitly call the small-sample result exploratory. | Closest current predictive prior art located for baseline EEG -> later stimulation response. It supplies a serious predictive baseline but does not use the proposed licensed modal chi + directed closed-loop recovery architecture or predict the full recovery trajectory. |
| Shikauchi et al., **Quantifying State-Dependent Control Properties of Brain Dynamics from Perturbation Responses** (2026), PMID `41419330` | FULL open primary article / PMC | Uses perturbation input with network control theory and estimates controllability Gramian structure from TMS-EEG responses across brain states; emphasizes that perturbations reveal control properties not captured by unperturbed observation alone. | Direct native control-theory comparator for multivariate perturbation-response structure. It estimates control properties from perturbation responses rather than prospectively scoring a frozen baseline model against an untouched recovery trajectory. |
| Ogino et al., **Designing optimal perturbation inputs for system identification in neuroscience**, eLife reviewed preprint v2 (9 Sep 2026), DOI `10.7554/eLife.110030.2` | FULL primary reviewed preprint | Formalizes neural dynamics as a control system with external input, shows passive recordings can miss fast damped/weakly observable modes, and derives perturbation-design principles to improve system identification. It explicitly treats TMS-like impulses, tDCS-like steps, and tACS-like sinusoids. | Extremely close theoretical/methodological prior art. It strongly supports using perturbation to identify hidden dynamics and must be inherited rather than reinvented. Its primary target is system-identification accuracy/perturbation design, not the residual prospective recovery prediction described below. |
| **A Whole-Brain Dynamical Framework Linking Resting-State Activity to TMS-Evoked Responses**, bioRxiv (2026) | FULL preprint page | Fits a whole-brain dynamical model to resting-state activity and simulates TMS-evoked responses; for TMS prediction, stimulation-induced effective connectivity is additionally estimated/refit using a subset of TMS trials. | Very close whole-brain dynamical prior art. Because TMS-response data enter the response-model fitting, it does not close the specific question of whether a model frozen from pre-perturbation data alone can predict untouched recovery organization. |

## What is already answered

The following broad propositions are not candidate NSD novelties:

1. TMS-EEG can be used to study brain relaxation/transients after perturbation.
2. Recurrent/inter-regional interactions are important for explaining complex TMS-EEG responses.
3. Baseline or prestimulation EEG state can influence and predict aspects of the evoked response.
4. Structural/functional network organization can predict perturbation propagation.
5. Linear/state-space/control-system representations with explicit perturbation inputs are established tools for neural system identification.
6. Perturbations can reveal damped or weakly observable modes that passive observations miss.

These ideas must be credited/inherited, not claimed as SymC discoveries.

## Residual question after collision

The current residual question is narrowed to:

> **Can an independently identified pre-perturbation multichannel closed-loop dynamical model, with licensed local/modal chi coordinates only where mathematically supported and with explicit directed coupling/feedback, prospectively predict the order, timescale, modal/subspace reorganization, transient amplification, and/or justified refusal of an untouched recovery response better than local/uncoupled and strongest fair native baselines?**

Important distinctions from the closest prior work located in this pass:

- the model is frozen before the decisive recovery response is opened;
- recovery data do not tune the pre-perturbation model;
- the target is recovery organization/trajectory, not only a scalar PCI, TEP component delta, clinical outcome, or post-perturbation fitted connectivity;
- local identity and embedded closed-loop behavior are tested separately;
- modal/subspace structure and scalar chi are not averaged into a system scalar;
- hierarchical reduction/refusal is part of the candidate prediction architecture;
- asymptotic return and finite-time resilience remain separate outcomes.

This residual question is **not yet certified novel**. A broader prior-art search, including citations/references from the closest sources and specialist system-identification/TMS literature, is still required before publication-level novelty language.

## Comparator implications

The eventual P0-Q/P1 comparator search should at minimum consider:

1. established TMS-EEG evoked-response / TEP features;
2. prestimulation EEG spectral power and connectivity prediction models;
3. EEG microstate/state-dependence models;
4. structural and functional connectivity propagation predictors;
5. state-space / MVAR-with-exogenous-input recurrent models;
6. network-control / controllability-Gramian measures;
7. perturbation-based system-identification methods, including Ogino et al.'s perturbation-design framework;
8. whole-brain dynamical TMS models where technically comparable.

No final comparator identity is frozen by this P0-D audit.

## E5 - Prior-work disposition

- Bonnard/Chang/Momi/Kabir/Maschke/Callaert/Shikauchi/Ogino are treated as inherited native evidence/method constraints, not obstacles to be worked around.
- The existing literature substantially reduces the need to invent a stimulation paradigm from scratch.
- Any eventual physical experiment should reuse validated TMS-EEG or other domain-native perturbation methods where feasible and alter them only to test the residual question.
- Existing prior work may serve as known-truth/qualification targets for the Engine, but cannot be used as untouched confirmation if it influenced model development.

## E6 - Experiment disposition

`MODIFY_TO_TEST_RESIDUAL_QUESTION`

Do not build a generic 'perturb the brain and observe recovery' experiment as though that were new. If physical testing becomes justified, modify established perturbation/EEG methodology specifically to test the frozen residual question, with an untouched recovery outcome and the strongest fair native comparators.

## Current claim ceiling

- Experimental opportunity: supported.
- Broad perturbation/recovery concept: established prior art.
- Baseline-state -> perturbation-response prediction: established/active prior art.
- NSD closed-loop/modal recovery prediction residual: plausible open question, **not yet prospectively validated and not yet certified novel**.
- P1: closed.
