# NSD Non-Computational Workstreams v0.1

Status: ACTIVE
Date: 14 September 2026

These are the workstreams that can proceed without waiting for any currently running NSD computation.

## 1. Historical evidence reconstruction

- Recover the exact `SymC_NSD.zip` contents into a transparent directory structure.
- Inventory manuscript, supplement, code, figures, tables, data manifests, and generated artifacts.
- Trace each published/historical number to code and source input.
- Mark anything that cannot be reconstructed as unresolved rather than silently accepting it.

## 2. Estimator and notation audit

Build a table for every historical or proposed NSD quantity:
- native observable;
- formula;
- units;
- frequency convention;
- width/decay convention;
- model assumptions;
- epistemic class A/B/C/D;
- relation to other features;
- whether it may be called chi;
- refusal conditions.

Priority checks:
- center frequency versus omega_0;
- FWHM/HWHM and angular/ordinary frequency;
- Lorentzian versus Gaussian peak models;
- linewidth versus damping;
- Q versus chi redundancy;
- broadband proxies versus true modal quantities.

## 3. Dataset provenance and hierarchy audit

For every historical/current dataset:
- dataset identifier and source;
- license/access status;
- cohort definition;
- diagnostic labels;
- subject count;
- session count;
- trial/epoch count;
- channels and montage;
- sampling rate;
- acquisition condition;
- site/device;
- available age/sex/medication/state metadata;
- exact subject-session key;
- exclusions and missingness.

The audit must explicitly detect pseudo-replication where sessions or epochs may have been treated as independent subjects.

## 4. Healthy baseline design

Before disorder-specific retesting:
- define one reusable healthy-reference construction;
- specify age handling;
- specify site/acquisition handling;
- preserve spatial organization;
- define uncertainty;
- define absent-feature phenotypes;
- version and lock the reference only after source and covariate audit.

## 5. Structural Engine specification

Write the production-facing specification before rewriting code:
- input contract;
- preprocessing contract;
- spectral-state extraction;
- modal candidate extraction;
- scalar-admission rules;
- categorical/refusal states;
- open-channel outputs;
- spatial/system representation;
- uncertainty outputs.

This specification should be testable independently from clinical labels.

## 6. Known-truth and adversarial qualification design

Design synthetic or known-truth inputs for:
- single clean oscillatory mode;
- multiple close modes;
- no periodic peak;
- aperiodic-only spectrum;
- broad Gaussian-like peak;
- Lorentzian mode with known damping;
- low SNR;
- transient/nonstationary signals;
- spatially heterogeneous modes;
- metadata mismatch;
- duplicated sessions;
- site shift.

Each production check must be shown to fail on a known-bad input.

## 7. Function Map design

Predefine representative maps of:
- healthy occupancy;
- within-subject session variation;
- periodic and aperiodic structure;
- spatial organization;
- mode count and absent-mode states;
- modal/scalar relationship where licensed;
- age/developmental trends;
- ordinary recording/task/state variation where available.

## 8. Limit Map design

Predefine limits/refusals for:
- poor spectral fit;
- no valid peak;
- unresolved overlapping modes;
- insufficient frequency resolution;
- width not interpretable as damping;
- failed scalar reduction;
- severe site/acquisition shift;
- insufficient spatial coverage;
- out-of-atlas state;
- ambiguous metadata joins.

## 9. Native comparator program

For each planned claim, identify and freeze the strongest fair baseline before decisive evaluation.

Potential comparator families depend on task and may include:
- demographics-only models;
- band-power baselines;
- aperiodic exponent/offset;
- peak frequency/power/bandwidth;
- conventional EEG feature sets;
- standard classifiers/regressors;
- disorder-specific accepted biomarkers.

Do not finalize comparator choice from whichever method makes NSD look strongest.

## 10. Cross-disorder design before adding disorders

Freeze what would count as:
- shared architecture;
- disorder-specific architecture;
- partial overlap;
- no common architecture;
- categorical non-comparability.

Define how shared structure will be distinguished from site, medication, age, acquisition, and diagnostic-label artifacts.

## 11. Comorbidity analysis design

Separate:
- categorical diagnosis overlap;
- symptom dimensionality;
- physiological overlap;
- longitudinal co-occurrence.

These are different questions and should not share one conclusion by default.

## 12. Manuscript development

Continue editing:
- Introduction;
- architecture;
- methods;
- non-claims;
- limitations;
- experimental opportunities;
- reproducibility;
- figure/table plan.

Result sections stay gated by `PENDING_*` records.

## 13. Figure/table architecture

Can be prepared now:
- architecture schematic;
- spectral/modal/scalar distinction;
- subject/session/trial hierarchy schematic;
- Engine + independent Atlas architecture;
- Function Map/Limit Map schematic;
- claim-evidence table structure.

Empirical disease-separation plots wait for audited evidence.

## 14. Reproducibility planning

Prepare:
- environment capture;
- manifests;
- hashes;
- dataset identity records;
- split registries;
- regeneration scripts;
- R1/R2/R3 matrix;
- clean-room procedure;
- negative/mutation tests.

## 15. Experimental-opportunity program

Design experiments first, then search literature for prior work. Candidate axes:
- repeated-session recovery;
- controlled task-state perturbation;
- sleep/wake transitions;
- sensory entrainment or stimulation where ethically and scientifically appropriate;
- longitudinal symptom transitions;
- multimodal EEG/MEG or EEG-imaging validation;
- within-subject medication/state changes only when suitable existing data or ethically governed studies exist.

The purpose is to identify discriminating experiments, not to force a laboratory program when published data already answer the question.

## 16. Publication/novelty audit

Before claiming novelty:
- identify established periodic/aperiodic EEG literature;
- identify existing transdiagnostic psychiatry frameworks;
- identify dynamical-systems/state-space approaches to psychiatric EEG;
- identify comorbidity/network-neuroscience explanations;
- identify existing damping/Q-factor interpretations where they exist;
- isolate the residual contribution NSD actually adds.

## Operating order

Recommended non-compute sequence:

`historical reconstruction -> estimator audit -> dataset hierarchy audit -> healthy baseline design -> Engine specification -> synthetic/adversarial qualification design -> Function/Limit Map design -> comparator freeze design -> cross-disorder/comorbidity design -> manuscript/figures/reproducibility -> experimental literature collision`

This work can progress in parallel with computation, but none of it may pre-write a positive numerical result.
