# Reporting layer scaffold

Status: OUTPUT-CONTRACT PLACEHOLDER / NO CLINICAL REPORT ENABLED

This directory will render qualified Engine, Atlas, and task-specific clinical-model outputs into machine-readable and human-readable reports.

The reporting layer may format results. It may not invent, smooth away, or reinterpret scientific outputs.

## Required report concepts

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

## Mandatory display rules

- uncertainty and refusal cannot be hidden;
- local modal quantities retain native names;
- no universal whole-brain stability score is generated for UI convenience;
- diagnostic outputs display the validated differential set and an unknown/out-of-domain state;
- prediction displays the exact target and horizon;
- unsupported modules remain visibly disabled rather than emitting placeholders that resemble results;
- report maturity is function-specific.

Canonical product definition: `../docs/NEUROPHYSIOLOGY_DECISION_SUPPORT_TOOL_SPEC_v0.1.md`.