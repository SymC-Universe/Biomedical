# NSD Task Freeze Template v0.1

Date: 14 September 2026
Status: READY FOR FIRST FORWARD DATASET
Purpose: prevent clinical tasks from changing after results become visible.

Copy this template for every P0-Q or later empirical task. P1 confirmatory tasks must additionally satisfy MFR-14.

## 1. Task identity

- Task ID:
- Title:
- Maturity target: `P0-D | P0-Q | P1 | P2`
- Date frozen:
- Engine version:
- Atlas version:
- Dataset version(s):
- Responsible analysis script/entry point:
- Configuration hash:

## 2. Scientific question

State one question in a way that can return a negative result.

Question:

Competing explanation(s):

What observation would count against the NSD interpretation?

## 3. Unit of inference

- primary unit: `subject | session | trial | other`
- repeated-measure structure:
- clustering/hierarchy method:
- train/test grouping key:
- bootstrap/permutation grouping key:

Explicitly state why the reported `N` is the correct independent unit.

## 4. Population

### Inclusion

- dataset(s):
- diagnostic/symptom definition:
- age range:
- recording condition:
- minimum signal requirements:
- required metadata:

### Exclusion

- source-defined exclusions:
- project QC exclusions:
- missing-data rule:
- medication/state rule:
- site/device rule:

No exclusion may be added after final outcome inspection without creating a new task version and labeling it exploratory.

## 5. Structural features frozen before labels

List exact Engine outputs admitted to the task.

### Spectral

- aperiodic:
- periodic:
- fit-quality/open-channel variables:

### Modal

- estimator:
- model order rule:
- admitted mode fields:
- identifiability threshold/source:

### Scalar

- licensed scalar(s):
- derivation version:
- admission rule:
- uncertainty rule:
- refusal states retained:

### Spatial / conglomerate

- regions/channels:
- participation/relationship variables:
- aggregation rule:

## 6. Healthy/reference Atlas rule

- Atlas version:
- reference population:
- covariate model:
- residualization if any:
- out-of-atlas rule:

Confirm:
- [ ] Atlas was not retuned for this disorder/task.
- [ ] test participants were not used to fit the reference model unless the task explicitly evaluates within-sample reference construction.

## 7. Native comparators

List strongest fair comparators before decisive evaluation.

- C0 demographic/acquisition:
- C1 simple spectral:
- C2 periodic/aperiodic:
- C3 spatial:
- C4 native modal/state-space:
- C5 clinical:

State why any omitted comparator is not applicable.

## 8. Endpoint

Primary endpoint:

Secondary endpoints:

Not tested in this task:

Prevent classification, association, and longitudinal prediction from sharing one endpoint label.

## 9. Statistical model

- model family:
- covariates:
- interactions:
- repeated-measure handling:
- regularization:
- feature-selection rule:
- missing-value rule:
- uncertainty method:
- multiple-comparison correction:

## 10. Split / holdout

- development partition:
- qualification partition:
- untouched test partition:
- external dataset if any:
- random seed policy:

Confirm:
- [ ] all sessions/epochs from one subject stay on the same side of a subject-level split.
- [ ] preprocessing that learns parameters is fit inside the training partition where required.
- [ ] clinical labels cannot tune structural Engine thresholds.

## 11. Decision rule

Define in advance what produces:
- `ADDS`:
- `EQUIVALENT`:
- `SUBTRACTS`:
- `INDETERMINATE`:

Define minimum clinically/scientifically relevant effect if appropriate.

## 12. Refusal handling

For each refusal code expected in this task:
- include as categorical feature?
- report prevalence only?
- exclude from a specific estimator comparison?
- treat as out-of-domain?

Prohibit replacing refusals with made-up scalar values.

## 13. Sensitivity analyses

Predeclare only scientifically motivated checks, for example:
- site/device;
- age;
- medication;
- recording duration;
- reference scheme;
- condition/state;
- alternate qualified model family;
- reasonable QC boundary variation.

Do not generate an unlimited multiverse and report only favorable variants.

## 14. Figure/table lock

Before test reveal, define the intended outputs:
- primary result table:
- comparator table:
- refusal/Limit Map table:
- primary figure:
- calibration/uncertainty figure:

Plots may change cosmetically after reveal; analytic content may not change without versioning.

## 15. Reproducibility fields

- dataset manifest hash:
- subject-inclusion hash:
- split-manifest hash:
- Engine config hash:
- Atlas hash/version:
- software lock file:
- analysis commit:
- output manifest:

R1 target:
R2 target:
R3 target:

## 16. Deviations after freeze

Every deviation must record:
- timestamp;
- reason;
- whether prompted by outcome visibility;
- scientific/mechanical classification;
- effect on maturity status;
- new task version if needed.

## 17. Final interpretation ceiling

Complete before running:

If positive, the strongest allowed statement is:

If negative, the interpretation is:

This task does **not** establish:

This final field is intended to stop a clean statistical result from silently becoming a mechanistic, diagnostic, predictive, or treatment claim.