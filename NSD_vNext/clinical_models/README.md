# Clinical model registry scaffold

Status: EMPTY REGISTRY / NO CLINICAL MODEL ADMITTED

This directory will contain task-specific diagnostic, monitoring, and prognostic models only after the Structural Engine and relevant Atlas version are frozen for the task.

The clinical layer is downstream of the label-blind representation layer.

Each admitted model must ship with a manifest declaring at minimum:

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

## Model families remain separate

Do not reuse one model label across materially different tasks:

- screening;
- present-state classification;
- differential diagnostic support;
- dimensional symptom estimation;
- treatment-response prediction;
- longitudinal monitoring;
- fixed-horizon prognosis;
- time-to-event prognosis.

A cross-sectional classifier is not a prognostic model.

## Admission rule

The first candidate clinical model is expected to be a narrowly frozen research classifier after T0/T1 qualification. ASD is the current logical first phenotype because historical project lineage exists, but no ASD model is admitted merely by this scaffold.

Every clinical result remains subject to the native-comparator decision: `ADDS`, `EQUIVALENT`, `SUBTRACTS`, `INDETERMINATE`, or `NOT_TESTED`.

## Machine-readable registry contract

Every future registry entry must validate conceptually against `clinical_model_registry_schema_v0.1.json` and retain the native-comparator outcome and full version/provenance linkage. The presence of this schema does not admit any clinical model.
