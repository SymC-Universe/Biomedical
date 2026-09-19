# Neurophysiology decision-support tool scaffold

Status: ORCHESTRATION SCAFFOLD / NO CLINICAL CLAIMS

This directory is reserved for the eventual user-facing orchestration layer.

The tool may call qualified components, but it must not contain hidden scientific logic that changes feature definitions, Atlas references, or clinical model behavior.

Dependency direction:

```text
recording
  -> engine/
  -> atlas/
  -> clinical_models/ (only for explicitly supported tasks)
  -> reporting/
  -> tool/ UI/API orchestration
```

The tool is intended to support, as independently matured functions:

1. neurophysiological assessment;
2. screening/triage;
3. open-set differential diagnostic support;
4. longitudinal monitoring;
5. prognosis/forecasting only when longitudinal validation exists.

## Hard rules

- no whole-brain/project-branded stability score;
- no diagnostic output directly from the label-blind Engine;
- no forecast from a cross-sectional classifier;
- no forcing every case into a supported diagnosis;
- unknown/out-of-domain and refusal are first-class outputs;
- every clinical model declares its scope, calibration, Engine version, Atlas version, and maturity;
- the UI cannot suppress uncertainty/refusal information for presentation convenience.

Canonical product definition: `../docs/NEUROPHYSIOLOGY_DECISION_SUPPORT_TOOL_SPEC_v0.1.md`.