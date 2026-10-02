# Neurophysiology Decision-Support Tool Specification v0.1

Date: 14 September 2026
Status: PRODUCT/SCIENCE TARGET DEFINITION — NOT A CLINICAL CLAIM
Governing baseline: SymC General Operations Manual v0.8.0 + NSD Project Protocol v0.1

## 1. What the eventual tool is

The end-state product is **not one classifier and not one stability score**.

It is a modular neurophysiological decision-support system that uses a frozen, label-blind representation of brain dynamics and a versioned reference Atlas to support four separable clinical/research jobs:

1. **Assessment** — describe what neurophysiological structure is actually recoverable from the recording;
2. **Differential support** — estimate which validated phenotype/diagnostic classes best match the measured architecture, while preserving an unknown/out-of-domain option;
3. **Longitudinal monitoring** — measure within-person change relative to the person’s own prior state and the independent reference Atlas;
4. **Prognosis/forecasting** — only where longitudinal evidence exists, estimate the probability or time-to-event risk of a prespecified future outcome.

A fifth mode, **research/qualification**, exposes full Engine outputs, comparator results, and Function/Limit information for scientific development.

No product brand is assigned at this stage. Parameters and outputs use established neurophysiology, dynamical-systems, statistical, and clinical terminology.

## 2. Core design principle

The tool is a downstream consumer of the existing scientific architecture:

`recording -> provenance/QC -> Structural Engine -> reference Atlas -> task-specific clinical model -> report`

The layers have different jobs and may not silently train each other.

### 2.1 Structural Engine

The Structural Engine remains label-blind. It extracts/rejects:
- periodic and aperiodic spectral structure;
- candidate modes and poles/eigenvalues where identifiable;
- modal damping ratios only where licensed;
- spatial participation and regional organization;
- coupled/system-level descriptors under established mathematical definitions;
- uncertainty;
- refusal/open-channel states.

It does **not** diagnose.

### 2.2 Reference Atlas

The Atlas describes ordinary and reference variation produced by a frozen Engine:
- age/development where available;
- recording state;
- site/device/reference effects;
- within-person and between-person variation;
- spectral/modal/spatial/system distributions;
- admission/refusal prevalence;
- Function and Limit regions.

It does **not** retune itself to make a disorder separate better.

### 2.3 Clinical Model Registry

Diagnosis, differential classification, symptom association, treatment response, and prognosis are separate **task-specific models** registered downstream of the Engine and Atlas.

Every registered model must declare:

```text
model_id
task_type
target_definition
supported_labels_or_outcomes
input_engine_version
input_atlas_version
required_features
population_scope
recording_scope
training_datasets
validation_datasets
split_manifest
calibration_method
performance_metrics
uncertainty_method
out_of_domain_rule
refusal_rule
known_limitations
maturity_status
```

A model validated for one task is not silently reused for another.

## 3. Product modes

### Mode A — Neurophysiological Assessment

This is the foundational mode and can mature before any diagnostic claim.

Output:
- acquisition/provenance status;
- signal-quality status;
- spectral profile;
- modal profile where recoverable;
- spatial/system organization;
- local damping ratios only where admitted;
- refusal/non-identifiability states;
- comparison with the matched Atlas reference distribution;
- uncertainty;
- which outputs are trait-like, state-sensitive, or currently unreliable.

This mode answers:

> What is measurable in this recording, and how unusual is it relative to an appropriate reference population?

### Mode B — Screening / Triage

This is the earliest clinically oriented mode.

It may answer a narrowly frozen question such as:

> Does this recording contain a validated neurophysiological pattern that warrants further evaluation for condition X?

It is not automatically equivalent to diagnosis.

Required output:
- screening probability/score under its established model name;
- calibrated uncertainty;
- sensitivity/specificity for the validated population;
- intended-use population;
- false-positive/false-negative characterization;
- out-of-domain/unknown state;
- data-quality/refusal status.

### Mode C — Differential Diagnostic Support

Ultimate diagnostic ambition: given a prespecified set of validated alternatives, estimate the evidence for each while allowing **none/unknown/out-of-domain**.

This is preferable to a collection of independent one-vs-control classifiers because real clinical use requires alternatives to compete.

Example task structure, without implying current validation:

```text
reference / no supported disorder pattern
phenotype A
phenotype B
phenotype C
...
unknown / out of supported domain
```

Required output:
- calibrated class probability or likelihood representation;
- confidence/credible interval where supported;
- model uncertainty;
- out-of-domain score/status;
- strongest alternative classes;
- contribution summary by native feature layer;
- explicit statement of validated differential scope;
- relevant comparator performance.

The report must never imply that absence from the supported class set means absence of disease.

### Mode D — Longitudinal Monitoring

Repeated measurements are compared against:
1. the individual’s prior qualified recordings;
2. the Atlas distribution for the relevant state/covariates;
3. expected measurement variability.

Candidate outputs:
- change in native spectral/modal/spatial/system descriptors;
- within-person standardized change;
- change beyond known test-retest variation;
- change in admission/refusal pattern;
- recovery/return behavior after perturbation where a protocol supports it;
- transition between empirically defined phenotype states, if those states have been qualified.

The monitoring layer must distinguish **measurement variation**, **ordinary state variation**, and **potential biological change**.

### Mode E — Prognosis / Forecasting

Prediction is a separate model family and remains disabled until longitudinal evidence exists.

Every prognostic model must define:
- the event/outcome;
- prediction origin (`t0`);
- prediction horizon(s);
- censoring/competing-event handling where relevant;
- covariates available at prediction time;
- whether repeated trajectories are used;
- calibration and external validation.

Possible future tasks include, only if the datasets support them:
- conversion to a prespecified diagnosis within a fixed horizon;
- symptom worsening/remission;
- relapse/recurrence;
- treatment response;
- change in functional status;
- transition between empirically identified neurophysiological states.

A cross-sectional classifier is never relabeled as a predictor.

## 4. What the tool should show the user

The clinical/research interface should produce a **layered report**, not a single traffic-light score.

### Panel 1 — Data validity

- recording usable / partially usable / refused;
- usable duration;
- channels/regions retained;
- artifacts;
- site/device/reference status;
- out-of-domain warnings.

### Panel 2 — Native neurophysiology

- periodic/aperiodic spectral state;
- qualified modes;
- mode frequencies and decay/growth where identifiable;
- mode shapes/participation;
- spatial organization;
- system-level descriptors actually computed;
- local damping ratios where licensed;
- open-channel/refusal states.

### Panel 3 — Reference comparison

For each qualified feature/layer:
- reference percentile or standardized deviation under the frozen Atlas model;
- expected ordinary variability;
- site/state/covariate context;
- uncertainty.

A single global “abnormality score” is not required and must not be manufactured for display convenience.

### Panel 4 — Diagnostic support, if the task is validated

- supported differential set;
- calibrated probabilities/evidence;
- uncertainty;
- unknown/out-of-domain status;
- strongest competing alternatives;
- model version and validation scope.

### Panel 5 — Longitudinal change

When repeated qualified sessions exist:
- current versus personal baseline;
- slope/trajectory where meaningful;
- change beyond expected measurement/state variation;
- new or resolved refusal/admission states.

### Panel 6 — Prognosis, only if validated

- exact predicted outcome;
- horizon;
- absolute risk/probability or time-to-event estimate;
- interval/uncertainty;
- calibration scope;
- comparison with conventional clinical predictor model;
- explicit no-forecast state when unsupported.

## 5. Refusal is a product feature

The tool must be allowed to return **no diagnosis**, **no scalar**, or **no forecast**.

Refusal families include:
- insufficient signal quality;
- ambiguous provenance;
- unsupported acquisition state;
- out-of-reference-population input;
- non-identifiable modes;
- model disagreement;
- uncertainty exceeding the frozen task threshold;
- classification out-of-domain;
- unsupported diagnostic differential;
- insufficient longitudinal information for prediction.

A clinically mature tool is safer when it knows when not to answer.

## 6. Diagnostic architecture

The diagnostic layer should be open-set and hierarchical rather than a mandatory one-shot multiclass label.

A practical sequence is:

1. **technical admissibility** — can the recording be interpreted?
2. **reference-domain admissibility** — is the person/recording inside the Atlas scope?
3. **normative deviation** — is there reproducible deviation from ordinary/reference structure?
4. **phenotype matching** — which qualified architecture(s) does the deviation resemble?
5. **differential support** — among validated alternatives, what evidence favors each?
6. **unknown/other** — can none of the validated alternatives be supported confidently?

This structure prevents the system from forcing every patient into a known disease class.

## 7. Prediction architecture

The prognostic layer should favor task-appropriate models rather than reuse the diagnostic classifier.

Candidate model families depend on the outcome:
- calibrated binary risk models for fixed-horizon events;
- survival/time-to-event models for censored outcomes;
- mixed-effects or state-space trajectory models for repeated continuous outcomes;
- competing-risk models where multiple endpoints preclude each other;
- sequential models only where the data volume and external validation support them.

Performance must include calibration, not discrimination alone.

For fixed-horizon risk:
- AUROC/AUPRC where relevant;
- Brier score;
- calibration intercept/slope or calibration curve;
- sensitivity/specificity at prespecified operating points;
- decision-curve/net-benefit analysis if a genuine clinical action threshold exists.

For time-to-event:
- concordance/time-dependent discrimination;
- horizon-specific calibration;
- Brier/integrated Brier where suitable;
- event/censoring counts;
- external transfer.

## 8. Explanation architecture

Interpretability must remain native to the analysis rather than being added as an opaque post-hoc story.

The report should distinguish contributions from:
- spectral state;
- modal dynamics;
- spatial organization;
- embedded system descriptors;
- categorical absence/refusal states;
- ordinary clinical/demographic predictors.

If a machine-learning explanation method is used, it must not be presented as proof of biological mechanism.

The tool should be able to answer:

> What measured information moved this task-specific estimate, and which parts of the recording were not admissible?

not:

> What disease mechanism did the algorithm discover?

unless that stronger claim has separate evidence.

## 9. First implementation target

The first practical implementation should be **EEG-first**, because the current project architecture, available historical lineage, public data ecosystem, periodic/aperiodic methods, and candidate state-space/modal methods make EEG the most tractable common input.

The architecture remains modality-extensible.

Later adapters may support, where independently qualified:
- MEG;
- intracranial/LFP recordings;
- evoked responses;
- source-localized signals;
- neuroimaging or other physiological measures as separate native layers.

Multimodal fusion must preserve modality-specific information rather than converting everything into one common scalar by construction.

## 10. First scientific/product sequence

### Phase T0 — Engine qualification

Goal: prove the representation layer can recover known truth and refuse invalid reductions.

Exit requirements:
- known-truth recovery map;
- Chi-vs-chi / local-versus-embedded tests;
- nuisance/adversarial Limit Map;
- deterministic provenance;
- CI regression coverage.

No diagnostic feature is released here.

### Phase T1 — Healthy/reference assessment product

Goal: produce a research-grade individual neurophysiological assessment against a versioned Atlas.

Exit requirements:
- audited healthy data hierarchy;
- ordinary-state Function Map;
- test-retest characterization;
- covariate/site/device characterization;
- locked first Atlas;
- subject-level report generator.

This is the first usable **assessment tool**, even before diagnosis.

### Phase T2 — First phenotype classifier

Current logical first clinical phenotype: ASD, because the project already has historical ASD lineage to re-audit. This is a starting point, not a presumption that ASD will validate.

Task should begin as a narrowly frozen research question, for example:

`ASD vs matched reference under recording condition X`

with:
- subject-level splits;
- strong native comparators;
- calibration;
- held-out evaluation;
- unknown/OOD behavior;
- no disorder-specific Atlas retuning.

If the architecture does not add value, record EQUIVALENT or SUBTRACTS and simplify.

### Phase T3 — External replication of the first phenotype

Goal: establish whether the result survives another dataset/site/population without refitting the reference architecture to the external cohort.

This is the point at which a screening claim may become plausible if the evidence supports it.

### Phase T4 — Differential expansion

Add disorders one at a time using the same frozen Engine and compatible Atlas.

Each addition requires:
- dataset audit;
- same-feature measurability check;
- comparator test;
- calibration;
- cross-disorder confusion analysis;
- unknown/other behavior.

The intended product evolves from binary research classification to differential support only when multiple alternatives have independent validation.

### Phase T5 — Longitudinal monitoring

Use repeated sessions to establish which descriptors can detect meaningful within-person change beyond measurement and ordinary-state variation.

### Phase T6 — Prognostic qualification

Only after a dataset contains appropriate longitudinal outcomes:
- freeze target and horizon;
- build conventional clinical baseline;
- add neurophysiological architecture incrementally;
- evaluate calibration and external transfer;
- enable the forecast panel only if it ADDS useful information.

### Phase T7 — P2 release candidate

A clinical/research tool release requires:
- locked supported-use cases;
- validated model registry;
- versioned Engine/Atlas/model bundle;
- reproducible build;
- audit log;
- refusal/OOD behavior;
- human-readable and machine-readable report;
- external validation appropriate to every enabled claim.

## 11. Repository/product separation

The codebase should preserve the following dependency direction:

```text
engine/
  label-blind signal and structural inference

atlas/
  independent normative/reference models

clinical_models/
  task-specific diagnostic/prognostic models

reporting/
  human + machine readable result rendering

tool/
  orchestration/API/UI only
```

Prohibited dependency:

`clinical_models -> change Engine feature definitions to improve the same clinical task`.

Clinical findings can motivate a future separately versioned scientific revision, but cannot silently mutate the frozen representation used for the current confirmatory test.

## 12. Minimum machine-readable report contract

```text
report_id
subject_id
session_id
acquisition_scope
engine_version
atlas_version
signal_quality_status
out_of_domain_status
structural_profile
atlas_deviations
refusals
clinical_models_run[]
  model_id
  task_type
  supported_scope
  estimate
  uncertainty
  calibration_scope
  result_status
longitudinal_change
forecasts[]
provenance_hashes
software_build
report_maturity
```

`estimate` is task-specific. It is not universally named chi or a stability score.

## 13. Tool maturity labels

Every report carries the maturity of the enabled function.

Suggested product maturity:

- `RESEARCH_STRUCTURE_ONLY`
- `RESEARCH_REFERENCE_ASSESSMENT`
- `RESEARCH_CLASSIFIER`
- `EXTERNALLY_VALIDATED_SCREENING`
- `EXTERNALLY_VALIDATED_DIFFERENTIAL_SUPPORT`
- `EXTERNALLY_VALIDATED_MONITORING`
- `EXTERNALLY_VALIDATED_PROGNOSIS`
- `P2_RELEASE_SCOPE`

Functions mature independently. A tool may have a mature assessment module while prognosis remains disabled.

## 14. What success would actually look like

The strongest successful outcome is not “one EEG number diagnoses everything.”

It is a system that can:

1. ingest a recording with full provenance;
2. determine what can and cannot be measured reliably;
3. describe the subject’s multilevel neurophysiological architecture;
4. compare it with a locked reference Atlas;
5. support a differential only within independently validated conditions;
6. recognize unknown/out-of-domain cases;
7. monitor an individual over time;
8. forecast a prespecified outcome only when longitudinal evidence earns that function;
9. show exactly which native measurements contributed;
10. refuse unsupported conclusions.

That is the target tool the current NSD program should build toward.