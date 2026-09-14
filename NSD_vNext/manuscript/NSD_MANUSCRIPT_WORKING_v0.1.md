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

**PENDING_REAUDIT / PENDING_COMPUTATION:** Final quantitative findings, disorder-specific comparisons, predictive results, and any cross-disorder generalization will be inserted only after historical NSD evidence and current computational outputs are reconciled under the v0.8.0 standard.

## 1. Introduction

Clinical comorbidity creates a difficult inference problem. Shared symptoms or overlapping diagnoses may reflect shared mechanisms, interacting mechanisms, common upstream constraints, measurement overlap, or merely the coarse resolution of diagnostic categories. A useful cross-disorder framework therefore has to preserve both common structure and disorder-specific structure rather than forcing every condition into one axis.

The NSD program approaches this problem through Stability Architecture. The central question is whether neurophysiological organization can be represented as a structured state space containing local dynamical quantities, mode-resolved organization, and whole-system relationships, and whether clinically distinct phenotypes occupy reproducibly different regions or trajectories within that state space.

The framework does not begin by assigning a universal scalar chi to the brain. It begins with native neurophysiology: signal spectra, time-domain structure, spatial organization, accepted estimators, acquisition architecture, known confounders, and domain-native null models. Where a dynamical reduction genuinely supports a damping-to-frequency coordinate, a local or mode-specific chi may be derived. Where it does not, the relevant feature remains a spectral parameter, empirical coordinate, categorical phenotype, or refused interpretation.

This distinction is important because several quantities that are easy to conflate are not physically identical. Spectral peak center frequency is not automatically an undamped natural frequency. Peak bandwidth is not automatically a damping rate. Quality factor and mode-specific chi are not independent when both arise from the same second-order resonance. A whole-head average can hide regional organization. A session count is not a subject count. Cross-sectional classification is not longitudinal prediction.

The project therefore separates four evidence layers: spectral state, scalar stability coordinates where licensed, vector/modal organization, and conglomerate/system organization, while preserving an open channel for residuals, rejected modes, absent peaks, poor fits, and unclassified records. These layers form a starting architecture rather than a complete ontology of neural stability.

## 2. Conceptual architecture

### 2.1 Spectral state

The spectral layer describes what is directly supported by the signal model: aperiodic offset and exponent, periodic peaks, peak frequencies, bandwidths, powers, quality factors where appropriate, peak counts, and complete peak lists. Periodic and aperiodic structure are retained separately because broadband changes can otherwise masquerade as oscillatory changes and vice versa.

### 2.2 Scalar stability coordinates

A scalar coordinate is admitted only when its mathematical and physiological interpretation is licensed. For a true second-order mode, a mode-specific damping ratio may be derived from a justified generator or validated estimator. An empirically normalized quantity is not promoted to dynamical chi merely because its values cluster around one.

No whole-brain scalar is assumed. The system may require multiple mode-specific coordinates or no defensible scalar at all.

### 2.3 Vector/modal state

The modal layer resolves multidimensional structure hidden by scalar compression. Candidate objects include poles, frequencies, decay rates, mode shapes, subspaces, participation vectors, and output-only state-space structure. The exact object used in each analysis must be named rather than grouped under a generic label.

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

Historical analyses are reclassified under this ladder before their results are reused.

### 3.2 Dataset and metadata architecture

Every dataset is tracked at the subject, session, trial/epoch, channel, and recording-condition levels where those identifiers exist. Joins are session-aware and use all relevant identifiers. Unmatched records are quarantined rather than silently assigned.

Repeated observations are analyzed with subject-aware aggregation, hierarchical modeling, mixed effects, clustered uncertainty, or another method appropriate to the frozen question. Epoch or session multiplicity does not inflate independent subject count.

**PENDING_REAUDIT:** Insert exact current dataset inventory, subject counts, session counts, sites, acquisition systems, diagnostic labels, covariates, exclusion rules, and licensing/provenance after historical source reconciliation.

### 3.3 Preprocessing and information-preservation audit

Preprocessing decisions are evaluated for the information they destroy. The pipeline records, where applicable, filtering, referencing, artifact rejection, epoching, channel removal/interpolation, sampling-rate changes, spectral estimation, frequency-range restriction, and spatial aggregation.

Whole-head averaging may be retained as a descriptive comparator but does not replace regional or channel-level structure when those data are available.

### 3.4 Periodic and aperiodic parameterization

The spectral representation separates aperiodic background from periodic peaks using a domain-standard parameterization suitable to the data. Complete peak lists and zero-peak states are retained. Model fit quality and rejected fits remain available in the open channel.

### 3.5 Dynamical-scalar admission

A candidate chi is classified as one of:

- dynamically derived;
- validated operational estimator;
- chi-like proxy;
- empirical stability coordinate.

The manuscript will state exactly which frequency and decay/width convention is used. Peak center frequency is not substituted for omega_0 without a justified conversion. Peak width is not interpreted as damping unless the underlying lineshape and broadening assumptions license that step.

### 3.6 Structural Engine qualification

Basic signal structure is qualified before clinical labels are used for evaluation. The preferred sequence is known-truth/synthetic recovery, adversarial testing, frozen holdout, label-blind adequacy on real neurophysiology, then clinical comparison. Negative controls test whether the Engine refuses signals that do not contain admissible structure.

### 3.7 Neurostability Atlas

The Atlas is independent of Engine tuning and may contain healthy distributions, age-residualized references, site/acquisition information, spatial organization, modal distributions, scalar distributions where licensed, absent-feature phenotypes, disease cohorts, symptom dimensions, longitudinal states, and uncertainty.

A healthy baseline, once audited and frozen, is reused rather than rebuilt separately to maximize each disease contrast.

### 3.8 Function Map and Limit Map

The Function Map describes ordinary supported behavior across healthy and clinical state space. The Limit Map records where representations degrade, become non-identifiable, fail to transfer, or must refuse. Neither map is subordinate to the other.

### 3.9 Statistical independence and uncertainty

Uncertainty is matched to the estimator and data hierarchy. Candidate methods include subject-level bootstrap intervals, hierarchical models, permutation tests that preserve subject structure, cross-validation with subject-level splitting, site-aware validation, and external datasets.

Multiple endpoints, frequency windows, feature sets, thresholds, and disorder comparisons are accounted for prospectively where they affect confirmatory claims.

### 3.10 Comparator architecture

Every claim of added value is compared with the strongest fair native baseline for the same frozen task. Depending on the question this may include simple spectral features, aperiodic parameters, band power, conventional clinical covariates, established EEG markers, or standard machine-learning models.

The outcome is classified as ADDS, EQUIVALENT, SUBTRACTS, INDETERMINATE, or NOT_TESTED.

## 4. Results

### 4.1 Historical NSD evidence reconciliation

**PENDING_REAUDIT.** The historical NSD manuscript, source archive, supplementary materials, datasets, and code will be reconstructed into an evidence ledger before any numerical result is treated as current. This section will explicitly identify which prior conclusions survive, narrow, become proxy-only, or are retired.

### 4.2 Healthy reference architecture

**PENDING_REAUDIT / PENDING_ANALYSIS.** Insert the audited healthy baseline with subject-level and session-level counts, covariate handling, spatial distributions, periodic/aperiodic structure, modal distributions, and uncertainty.

### 4.3 ASD / neurodevelopmental phenotype analysis

**PENDING_REAUDIT / PENDING_ANALYSIS.** Historical ASD observations will be revisited using subject-aware independence, explicit spectral-state decomposition, modal structure, and only those scalar coordinates that pass admission. Old scalar values will not be treated as dynamical chi until their derivation is re-established.

### 4.4 Cross-disorder phenotype architecture

**PENDING_DATASET_EXPANSION.** The shared-instability-class hypothesis requires materially distinct diagnostic phenotypes and an analysis that preserves disorder-specific structure. Similarity in one spectral or scalar feature is insufficient.

### 4.5 Comorbidity structure

**PENDING_DESIGN.** The analysis will distinguish categorical diagnosis overlap from symptom-dimensional and neurophysiological overlap. A comorbidity explanation must outperform simpler explanations such as shared demographics, acquisition effects, medication, common spectral shifts, or diagnostic measurement overlap.

### 4.6 Classification versus prediction

**PENDING_P1 DESIGN.** Cross-sectional separation will be reported only as classification. Any claim regarding future symptom trajectory, conversion, relapse, treatment response, or disease development requires longitudinal or prospective evidence.

### 4.7 Function and limit maps

**PENDING_ANALYSIS.** Report where the architecture is supported, where scalar reduction is licensed, where categorical phenotypes appear, and where the Engine refuses interpretation.

## 5. Discussion

### 5.1 Shared instability does not mean identical disorder

The strongest scientifically useful NSD formulation is not that distinct disorders are the same disease. The testable proposition is narrower: clinically distinct phenotypes may share parts of a neurophysiological stability architecture while differing in modal, spatial, temporal, developmental, and system-level organization.

### 5.2 Why the architecture cannot be reduced to damping alone

Damped-oscillator mathematics is one tractable entry point, not the complete neural model. Spectral, modal, relational, network, and categorical information may carry structure that no single damping ratio can preserve. The purpose of the scalar is compression where licensed, not replacement of the system.

### 5.3 Chi = 1 is not a presumed healthy optimum

Where a true second-order reduction supports a critical boundary, chi = 1 may serve as a reference. It is not assumed to represent health, maximum cognition, ideal psychiatric function, or a universal neural optimum. Any attraction, avoidance, or transition near that boundary must be established independently.

### 5.4 Clinical interpretation ceiling

Group-level physiology does not by itself establish a diagnostic test, treatment target, or therapeutic recommendation. Clinical utility requires external validation, calibrated individual-level performance, appropriate comparators, prospective endpoints where relevant, and evidence that the tool adds useful information beyond established practice.

### 5.5 Limitations

The final limitation section will include acquisition heterogeneity, site transfer, medication and state effects, age/development, sample-size imbalance, diagnostic-label limitations, repeated-session dependence, spectral-model assumptions, missing spatial information, estimator non-equivalence, absent-feature states, and the possibility that no single cross-disorder stability architecture generalizes.

## 6. Experimental and observational opportunities

The project will design falsifiable experiments or data-collection protocols before searching the literature for prior answers. Candidate classes include within-subject perturbations, repeated-session recovery measurements, sleep/wake or task-state transitions, longitudinal symptom tracking, medication-independent replication where feasible, and multimodal EEG/MEG or EEG-imaging comparisons.

Each candidate experiment must identify the native observable, predicted response, competing explanation, decision rule, and the result that would count against the hypothesis.

**PENDING_LITERATURE_COLLISION:** These candidate classes require systematic prior-art searches before being called novel experiments.

## 7. Reproducibility and data availability

The final release will distinguish R1 release integrity, R2 recomputation, and R3 primary evidence/provenance reconstruction. Dataset licenses and privacy constraints will determine which raw data can be redistributed, but identities, hashes where permitted, acquisition metadata, preprocessing configuration, split definitions, and regeneration instructions will be preserved.

## 8. Conclusion

NSD is being rebuilt as a falsifiable multiscale neurophysiological framework rather than a universal scalar diagnosis. The architecture permits shared structure across disorders but requires disorder-specific differences, failures, and non-admissible reductions to remain visible. The final scientific conclusion will be written only after historical results, current computation, Atlas construction, native comparators, and prospective tests have been reconciled under the current evidence standard.
