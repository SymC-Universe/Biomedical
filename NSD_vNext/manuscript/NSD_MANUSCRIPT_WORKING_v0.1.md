# Working Manuscript — Neuro Stability Disorder

Version: 0.1
Status: ACTIVE DRAFT / NOT FOR SUBMISSION
Date: 14 September 2026
Governing standard: SymC General Operations Manual v0.8.0 + NSD Project Protocol v0.1

> This manuscript is deliberately incomplete. Historical NSD results are not copied forward as current evidence until they are re-audited. Result-dependent sections remain explicitly gated.

## Working title

**Neuro Stability Disorder: A Multiscale Stability-Architecture Framework for Neurophysiological Phenotypes and Comorbidity**

Title status: provisional. The final title must match the evidence ceiling actually reached.

## Abstract

Psychiatric and neurodevelopmental disorders frequently overlap in symptoms, diagnoses, and physiological features, yet overlap does not by itself imply a single mechanism. We develop a neurophysiological Stability Architecture designed to test whether distinct clinical phenotypes can be represented within a shared but non-identical dynamical state space. The framework begins with native signal structure, separates periodic and aperiodic spectral components, resolves modal and spatial organization before scalar compression, and preserves categorical states when no defensible scalar exists. A candidate scalar chi is admitted only when a licensed dynamical model or validated operational estimator supports its interpretation. The resulting architecture combines scalar, vector/modal, and conglomerate/system views while retaining residuals, absent-feature states, and model refusals in an explicit open channel. An independent Neurostability Atlas provides healthy and disease-reference distributions without tuning the Structural Engine.

Historical source reconstruction changes the evidentiary interpretation of the 2025 NSD manuscript. Its figures and numerical disorder maps are retained as architecture-first, hypothesis-generating demonstrations rather than empirical validation because the available source package does not contain the data/code lineage required to treat them as measured results. This correction motivates the present separation between visualization, native observables, licensed estimators, audited datasets, and confirmatory claims.

**PENDING_REAUDIT / PENDING_COMPUTATION:** Final quantitative disorder-specific findings, predictive results, and cross-disorder generalization will be inserted only after current empirical outputs are reconciled under the v0.8.0 standard.

## 1. Introduction

Clinical comorbidity creates a difficult inference problem. Shared symptoms or overlapping diagnoses may reflect shared mechanisms, interacting mechanisms, common upstream constraints, measurement overlap, or merely the coarse resolution of diagnostic categories. A useful cross-disorder framework therefore has to preserve both common structure and disorder-specific structure rather than forcing every condition into one axis.

The NSD program approaches this problem through Stability Architecture. The central question is whether neurophysiological organization can be represented as a structured state space containing local dynamical quantities, mode-resolved organization, and whole-system relationships, and whether clinically distinct phenotypes occupy reproducibly different regions or trajectories within that state space.

The framework does not begin by assigning a universal scalar chi to the brain. It begins with native neurophysiology: signal spectra, time-domain structure, spatial organization, accepted estimators, acquisition architecture, known confounders, and domain-native null models. Where a dynamical reduction genuinely supports a damping-to-frequency coordinate, a local or mode-specific chi may be derived. Where it does not, the relevant feature remains a spectral parameter, empirical coordinate, categorical phenotype, or refused interpretation.

This distinction is important because several quantities that are easy to conflate are not physically identical. Spectral peak center frequency is not automatically an undamped natural frequency. Peak bandwidth is not automatically a damping rate. Quality factor and mode-specific chi are not independent when both arise from the same second-order resonance. A whole-head average can hide regional organization. A session count is not a subject count. Cross-sectional classification is not longitudinal prediction.

The project therefore separates four evidence layers: spectral state, scalar stability coordinates where licensed, vector/modal organization, and conglomerate/system organization, while preserving an open channel for residuals, rejected modes, absent peaks, poor fits, and unclassified records. These layers form a starting architecture rather than a complete ontology of neural stability.

### 1.1 Historical origin and evidentiary correction

The 2025 NSD manuscript was an architecture-first document. It proposed a boundary/timescale/substrate representation, candidate failure types, regional divergence, longitudinal trajectories, treatment mappings, and cross-domain analogies, and it rendered these ideas in figures that looked like population, patient, and longitudinal results.

Reconstruction of the available manuscript and supplementary source files shows that the package does not contain the empirical provenance needed to interpret those visualizations as validated results. There is no recoverable participant table for the displayed `N=100` spectrum, no source-to-coordinate chain for the disorder clusters, no reproducible transformation behind the historical “Live Neural Ticker,” and no code/data package for the plotted values. The lifespan lineage is explicitly described as a simulation. The substrate-inheritance comparison is a conceptual visual argument rather than a derivation.

The present manuscript treats that history as a useful failure analysis rather than hiding it. The historical work demonstrated that the architecture could be drawn. The forward program asks whether any part of that architecture can be **recovered from data under a frozen, falsifiable measurement system**.

The resulting evidentiary sequence is:

`visualizable architecture -> native observable -> qualified model/estimator -> audited data hierarchy -> uncertainty -> frozen comparison -> claim`.

## 2. Conceptual architecture

### 2.1 Spectral state

The spectral layer describes what is directly supported by the signal model: aperiodic offset and exponent, periodic peaks, peak frequencies, bandwidths, powers, quality factors where appropriate, peak counts, and complete peak lists. Periodic and aperiodic structure are retained separately because broadband changes can otherwise masquerade as oscillatory changes and vice versa.

The aperiodic exponent is retained as an empirical spectral coordinate. It is not treated as a direct damping coefficient or direct dynamical chi. Existing literature supports physiological relevance and, in some settings, an association with excitation/inhibition-related changes, but pharmacological and methodological evidence does not support a universal one-to-one mechanistic mapping.

### 2.2 Scalar stability coordinates

A scalar coordinate is admitted only when its mathematical and physiological interpretation is licensed. For a true second-order mode, a mode-specific damping ratio may be derived from a justified generator or validated estimator. An empirically normalized quantity is not promoted to dynamical chi merely because its values cluster around one.

No whole-brain scalar is assumed. The system may require multiple mode-specific coordinates or no defensible scalar at all.

### 2.3 Vector/modal state

The modal layer resolves multidimensional structure hidden by scalar compression. Candidate objects include poles, frequencies, decay rates, mode shapes, subspaces, participation vectors, and output-only state-space structure. The exact object used in each analysis must be named rather than grouped under a generic label.

There is real prior art for model-conditional neural damping. Human MEG alpha has been modeled with second-order stochastic damped-oscillator dynamics, macaque visual gamma has been reproduced by a noise-driven damped harmonic oscillator, intracranial rhythmic responses have been fit with explicit damping-ratio/eigenfrequency models, and neural-mass transfer functions use complex poles whose real and imaginary parts encode decay/growth and oscillatory frequency around an operating point. These results justify testing a dynamical route. They do not justify assigning damping to every spectral peak.

### 2.4 Conglomerate/system organization

The system layer describes organization that emerges from relationships among channels, regions, modes, and networks. Candidate observables include channel participation, inter-regional coupling, relational geometry, network organization, and whole-system quantities that survive explicit validation.

### 2.5 Open channel

The open channel preserves information that does not fit the preferred model: residuals, model error, rejected modes, zero-peak states, poor fits, unclassified sessions, unmatched metadata, and other anomalies. These are not silently imputed into the architecture.

## 3. Methods

### 3.1 Research stages

The forward NSD program uses the GOM maturity ladder:

- P0-D for discovery, functional mapping, and hypothesis generation;
- P0-Q for qualification and controlled iteration;
- P1 for frozen confirmatory tests under MFR-14;
- P2 for qualified reproducible tool release.

The 2025 architecture manuscript is classified as P0-D. Historical empirical analyses are reclassified separately before their results are reused.

### 3.2 Dataset and metadata architecture

Every dataset is tracked at the subject, session, trial/epoch, channel, and recording-condition levels where those identifiers exist. Joins are session-aware and use all relevant identifiers. Unmatched records are quarantined rather than silently assigned.

Repeated observations are analyzed with subject-aware aggregation, hierarchical modeling, mixed effects, clustered uncertainty, or another method appropriate to the frozen question. Epoch or session multiplicity does not inflate independent subject count.

**PENDING_REAUDIT:** Insert exact current dataset inventory, subject counts, session counts, sites, acquisition systems, diagnostic labels, covariates, exclusion rules, and licensing/provenance after current empirical source reconciliation.

### 3.3 Preprocessing and information-preservation audit

Preprocessing decisions are evaluated for the information they destroy. The pipeline records, where applicable, filtering, referencing, artifact rejection, epoching, channel removal/interpolation, sampling-rate changes, spectral estimation, frequency-range restriction, and spatial aggregation.

Whole-head averaging may be retained as a descriptive comparator but does not replace regional or channel-level structure when those data are available.

### 3.4 Periodic and aperiodic parameterization

The spectral representation separates aperiodic background from periodic peaks using a domain-standard parameterization suitable to the data. Complete peak lists and zero-peak states are retained. Model fit quality and rejected fits remain available in the open channel.

A Gaussian periodic peak width remains a descriptive width. It is not treated as a decay constant simply because a resonance with similar visual shape could possess a linewidth-damping relationship under another model.

### 3.5 Dynamical-scalar admission

A candidate chi is classified as one of:

- dynamically derived;
- validated operational estimator;
- chi-like proxy;
- empirical stability coordinate.

The manuscript will state exactly which frequency and decay/width convention is used. Peak center frequency is not substituted for omega_0 without a justified conversion. Peak width is not interpreted as damping unless the underlying model and broadening assumptions license that step.

Candidate routes include direct stochastic damped-oscillator fitting, neural-mass generative inversion, or qualified output-only state-space modal estimation. These routes must be evaluated against descriptive spectral parameterization rather than assumed equivalent.

### 3.6 Structural Engine qualification

Basic signal structure is qualified before clinical labels are used for evaluation. The preferred sequence is known-truth/synthetic recovery, adversarial testing, frozen holdout, label-blind adequacy on real neurophysiology, then clinical comparison. Negative controls test whether the Engine refuses signals that do not contain admissible structure.

The pre-compute qualification matrix includes single and multiple oscillators, unresolved neighboring modes, frequency drift, finite bursts, aperiodic-only signals, colored-noise drive, nonlinear/limit-cycle dynamics, source mixing, reference changes, finite-window broadening, and estimator disagreement.

### 3.7 Neurostability Atlas

The Atlas is independent of Engine tuning and may contain healthy distributions, age-residualized references, site/acquisition information, spatial organization, modal distributions, scalar distributions where licensed, absent-feature phenotypes, disease cohorts, symptom dimensions, longitudinal states, and uncertainty.

A healthy baseline, once audited and frozen, is reused rather than rebuilt separately to maximize each disease contrast.

### 3.8 Function Map and Limit Map

The Function Map describes ordinary supported behavior across healthy and clinical state space. The Limit Map records where representations degrade, become non-identifiable, fail to transfer, or must refuse. Neither map is subordinate to the other.

### 3.9 Statistical independence and uncertainty

Uncertainty is matched to the estimator and data hierarchy. Candidate methods include subject-level bootstrap intervals, hierarchical models, permutation tests that preserve subject structure, cross-validation with subject-level splitting, site-aware validation, and external datasets.

Multiple endpoints, frequency windows, feature sets, thresholds, and disorder comparisons are accounted for prospectively where they affect confirmatory claims.

### 3.10 Comparator architecture

Every claim of added value is compared with the strongest fair native baseline for the same frozen task. Depending on the question this may include simple spectral features, periodic/aperiodic parameters, band power, conventional clinical covariates, established EEG markers, or standard machine-learning models.

The outcome is classified as ADDS, EQUIVALENT, SUBTRACTS, INDETERMINATE, or NOT_TESTED.

## 4. Results

### 4.1 Historical NSD evidence reconciliation

**SOURCE-LEVEL RECONCILIATION COMPLETE FOR AVAILABLE MANUSCRIPT MATERIAL.**

The recovered main and supplementary TeX/PDF package was audited as provenance. The source package contains the full historical prose and figure references but does not contain an auditable data/code chain for the plotted disorder coordinates, numerical thresholds, or cross-domain values. The recovered TeX also contains a bibliography without inline citation commands, so individual historical mechanistic and numerical statements cannot be assumed to be supported by a specific reference merely because that reference appears at the end of the manuscript.

The historical evidentiary status is therefore:

- architecture and experiment design: retained as P0-D;
- historical plotted coordinates: not current results;
- exact disorder thresholds and universal adaptive windows: not earned;
- direct aperiodic-exponent-to-chi mapping: retired;
- direct Gaussian-bandwidth-to-damping mapping: not licensed;
- historical cross-domain validation claims: not transferred;
- longitudinal lineage: simulation/hypothesis, not observed trajectory;
- substrate-inheritance visual comparison: conceptual, not mechanistic proof.

This source audit is itself a completed result of the reconstruction process, but it does not substitute for empirical neurophysiological results.

### 4.2 Healthy reference architecture

**PENDING_REAUDIT / PENDING_ANALYSIS.** Insert the audited healthy baseline with subject-level and session-level counts, covariate handling, spatial distributions, periodic/aperiodic structure, modal distributions, and uncertainty.

### 4.3 ASD / neurodevelopmental phenotype analysis

**PENDING_REAUDIT / PENDING_ANALYSIS.** Historical ASD observations will be revisited using subject-aware independence, explicit spectral-state decomposition, modal structure, and only those scalar coordinates that pass admission. Old scalar values will not be treated as dynamical chi until their derivation is re-established.

### 4.4 Cross-disorder phenotype architecture

**PENDING_DATASET_EXPANSION.** The shared-instability-class hypothesis requires materially distinct diagnostic phenotypes and an analysis that preserves disorder-specific structure. Similarity in one spectral or scalar feature is insufficient.

### 4.5 Comorbidity structure

**PENDING_DESIGN / LITERATURE-BOUNDED.** The analysis will distinguish categorical diagnosis overlap from symptom-dimensional and neurophysiological overlap. A comorbidity explanation must outperform simpler explanations such as shared demographics, acquisition effects, medication, common spectral shifts, or diagnostic measurement overlap. Because transdiagnostic EEG overlap is already well established, novelty cannot rest on overlap alone.

### 4.6 Classification versus prediction

**PENDING_P1 DESIGN.** Cross-sectional separation will be reported only as classification. Any claim regarding future symptom trajectory, conversion, relapse, treatment response, or disease development requires longitudinal or prospective evidence.

### 4.7 Function and limit maps

**PENDING_ANALYSIS.** Report where the architecture is supported, where scalar reduction is licensed, where categorical phenotypes appear, and where the Engine refuses interpretation.

## 5. Discussion

### 5.1 Shared instability does not mean identical disorder

The strongest scientifically useful NSD formulation is not that distinct disorders are the same disease. The testable proposition is narrower: clinically distinct phenotypes may share parts of a neurophysiological stability architecture while differing in modal, spatial, temporal, developmental, and system-level organization.

### 5.2 Why the architecture cannot be reduced to damping alone

Damped-oscillator mathematics is one tractable entry point, not the complete neural model. Spectral, modal, relational, network, and categorical information may carry structure that no single damping ratio can preserve. The purpose of the scalar is compression where licensed, not replacement of the system.

The literature collision materially refines this point. Damped oscillators and pole-based neural models have already been used successfully in restricted MEG, LFP, sEEG, and neural-mass settings. The open question is therefore not whether neural damping can ever be modeled. It is whether the target NSD datasets contain identifiable modes for which such a model survives known-truth, nuisance, and real-data qualification, and whether those quantities add information beyond descriptive spectral features.

### 5.3 Chi = 1 is not a presumed healthy optimum

Where a true second-order reduction supports a critical boundary, chi = 1 may serve as a mathematical reference. It is not assumed to represent health, maximum cognition, ideal psychiatric function, or a universal neural optimum. Any attraction, avoidance, or transition near that boundary must be established independently.

### 5.4 Historical architecture without historical validation

The 2025 manuscript is retained as an explicit part of the project lineage because it contains useful scientific questions and a useful warning. It showed that a coherent architecture can become visually persuasive before the measurement chain has earned the labels placed on it.

The rebuild treats that as a methodological asset: every attractive picture now has to answer what raw data produced it, which estimator transformed those data, what assumptions were required, what uncertainty remains, what null or adversary could produce the same appearance, and what result would make the interpretation fail.

### 5.5 Clinical interpretation ceiling

Group-level physiology does not by itself establish a diagnostic test, treatment target, or therapeutic recommendation. Clinical utility requires external validation, calibrated individual-level performance, appropriate comparators, prospective endpoints where relevant, and evidence that the tool adds useful information beyond established practice.

Historical treatment protocols and exact treatment-to-chi mappings are not transferred into the forward evidence base.

### 5.6 Limitations

The final limitation section will include acquisition heterogeneity, site transfer, medication and state effects, age/development, sample-size imbalance, diagnostic-label limitations, repeated-session dependence, spectral-model assumptions, missing spatial information, estimator non-equivalence, absent-feature states, and the possibility that no single cross-disorder stability architecture generalizes.

An additional limitation is fundamental: the architecture may prove visually coherent but empirically low-dimensional in ways already captured by standard spectral analysis. The comparator program is designed to allow that outcome to be reported as EQUIVALENT or SUBTRACTS rather than forcing novelty.

## 6. Experimental and observational opportunities

The project designs falsifiable experiments or data-collection protocols before searching the literature for prior answers. Candidate classes include within-subject perturbations, repeated-session recovery measurements, sleep/wake or task-state transitions, longitudinal symptom tracking, medication-independent replication where feasible, and multimodal EEG/MEG or EEG-imaging comparisons.

Each candidate experiment must identify the native observable, predicted response, competing explanation, decision rule, and the result that would count against the hypothesis.

The first literature collision has already narrowed several candidate experiments: ordinary SpecParam reliability, generic transdiagnostic EEG overlap, basic ASD band-power differences, generic EEG-based prediction, and generic use of damped-oscillator/Q language are not themselves novel. Residual experiments must test multilevel architecture, model qualification, incremental information, transfer, recovery, and preserved disorder-specific organization.

## 7. Reproducibility and data availability

The final release will distinguish R1 release integrity, R2 recomputation, and R3 primary evidence/provenance reconstruction. Dataset licenses and privacy constraints will determine which raw data can be redistributed, but identities, hashes where permitted, acquisition metadata, preprocessing configuration, split definitions, and regeneration instructions will be preserved.

Historical source files currently available for the 2025 paper are hash-recorded in the reconstruction audit. They are provenance, not a reproducible empirical data package.

## 8. Conclusion

NSD is being rebuilt as a falsifiable multiscale neurophysiological framework rather than a universal scalar diagnosis. The historical paper demonstrated the architecture visually but did not establish its numerical coordinates empirically. The forward program therefore separates what can be drawn from what can be measured.

The architecture permits shared structure across disorders but requires disorder-specific differences, failures, and non-admissible reductions to remain visible. Neural damping remains a legitimate model-conditional target where an explicit generative or modal model earns it; it is not assigned by visual resemblance, aperiodic slope, or generic peak width. The final scientific conclusion will be written only after current data reconstruction, Engine qualification, Atlas construction, native comparators, and prospective tests have been reconciled under the current evidence standard.