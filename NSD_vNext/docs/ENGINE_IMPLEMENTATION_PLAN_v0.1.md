# NSD Structural Engine Implementation Plan v0.1

Date: 14 September 2026
Status: PRE-ALGORITHM IMPLEMENTATION PLAN

## 1. Current executable state

The repository now contains a tested contract scaffold under `NSD_vNext/engine/`.

Local verification at scaffold creation:
- 8 contract tests passed;
- no clinical labels are accepted or required by the core result contract;
- no estimator exists yet that could manufacture a chi value;
- whole-system chi names are rejected;
- mode-specific scalar lineage is mandatory;
- no-peak states and refusals are first-class outputs.

This establishes the mechanical shell before scientific estimators are implemented.

## 2. Proposed package structure

```text
NSD_vNext/engine/
  pyproject.toml
  nsd_engine/
    __init__.py
    schema.py                 # implemented contract layer
    provenance.py             # dataset/subject/session/run validation
    qc.py                     # signal-integrity metrics and flags
    spectral/
      base.py                 # common spectral interface
      periodic_aperiodic.py   # descriptive periodic/aperiodic adapter
    modal/
      base.py                 # candidate-mode interface
      state_space.py          # explicit oscillator/state-space candidate
      dmd.py                  # DMD candidate
      oma.py                  # output-only modal-analysis candidate
      neural_mass.py          # optional generative route, later stage
    admission.py              # scalar admission/refusal policy
    spatial.py                # regional/channel/mode participation
    conglomerate.py           # relational/system outputs
    uncertainty.py            # common uncertainty contract
    atlas_io.py               # Engine-output -> Atlas record serialization
    cli.py                    # reproducible execution entry point
  tests/
    test_contracts.py         # implemented
    test_provenance.py
    test_qc.py
    test_spectral_contract.py
    test_modal_known_truth.py
    test_admission.py
    test_refusal.py
    test_spatial.py
    test_config_freeze.py
```

The exact algorithms may change after qualification. The interfaces should change only with an explicit version/migration record.

## 3. Stage I — provenance implementation

Implement before signal modeling:
- dataset identity;
- subject/session/run/trial keys;
- duplicate detection;
- join cardinality audit;
- ambiguous-join quarantine;
- source file/hash record;
- sampling metadata;
- recording condition;
- site/device fields where available.

Tests:
- duplicate session key fails;
- ambiguous many-to-many join fails/quarantines;
- missing subject ID fails;
- two sessions from one subject remain linked to one subject;
- deterministic dataset manifest hash.

Scientific dependency: none beyond dataset schema.

## 4. Stage II — signal-integrity implementation

Implement generic QC that does not depend on diagnosis:
- readable data;
- duration;
- usable duration;
- missing samples;
- clipping/saturation;
- flat channels;
- basic line-noise measurement;
- channel count/map;
- preprocessing lineage.

Do not hard-code a universal acceptance threshold until the target data regime is defined.

Tests:
- synthetic flat channel flagged;
- clipping flagged;
- usable duration cannot exceed total duration;
- QC failure can coexist with a preserved open-channel record.

## 5. Stage III — descriptive spectral layer

First scientific implementation target because it is established native methodology and a mandatory comparator.

Output contract:
- PSD configuration;
- aperiodic parameters;
- full periodic peak list;
- no-peak state;
- fit residual/quality;
- model family/version;
- exact frequency range/resolution.

Critical rule:
This stage outputs **descriptive spectral parameters**, not dynamical chi.

Qualification:
- reproduce known package behavior on fixtures;
- zero-peak fixtures;
- two-peak fixtures;
- aperiodic-only fixtures;
- fit-range sensitivity;
- window/resolution sensitivity.

## 6. Stage IV — modal candidates

Implement candidates as independent adapters so methods can be compared rather than silently blended.

### Candidate M1 — state-space oscillator

Purpose:
Explicit first/second-order stochastic oscillator decomposition where poles and oscillator structure are part of the model.

Primary comparator/prior art:
Beck, Stephen & Purdon state-space oscillator models.

### Candidate M2 — Dynamic Mode Decomposition

Purpose:
Coupled spatial-temporal modes with complex eigenvalues carrying frequency and growth/decay.

Primary comparator/prior art:
Brunton et al. DMD for neural recordings.

### Candidate M3 — Output-Only Modal Analysis

Purpose:
Alternative system-identification route to modes/eigenstructure.

Primary comparator:
Published EEG/brain system-identification comparisons with DMD.

### Candidate M4 — neural-mass/generative model

Purpose:
Mechanistically richer inference where the dataset/question justifies it.

Restriction:
Do not add simply because it produces biologically named parameters. Identifiability must be demonstrated.

## 7. Stage V — known-truth harness

Create deterministic signal generators separate from estimator code:
- single DHO;
- two modes;
- unresolved modes;
- frequency drift;
- burst oscillator;
- aperiodic-only;
- colored input;
- nonlinear alternative;
- coupled spatial modes.

Each generator emits a truth manifest.

Each estimator is scored against:
- bias;
- RMSE;
- coverage;
- false modes;
- missed modes;
- false admission;
- correct refusal;
- model-order recovery;
- nuisance sensitivity.

No clinical data are used to set these pass regions.

## 8. Stage VI — scalar admission policy

Implement only after at least one modal route has qualification results.

Inputs:
- mode identity;
- model family;
- parameter estimates;
- uncertainty;
- fit diagnostics;
- identifiability diagnostics;
- broadening/adversarial checks;
- natural-frequency conversion status;
- dependency lineage.

Outputs:
- licensed mode-specific scalar; or
- refusal code.

No fallback rule may substitute an aperiodic exponent or Gaussian bandwidth just to avoid missing scalar values.

## 9. Stage VII — spatial/conglomerate layer

Begin with transparent quantities:
- channel/region feature distributions;
- mode participation vectors;
- mode-shape similarity;
- spatial gradients;
- interregional relationships under named estimators.

Every system summary must point to its lower-level inputs.

Do not introduce a whole-system scalar unless a separate derivation/validation earns one.

## 10. Stage VIII — Atlas serialization

Every Engine result should serialize into a versioned Atlas record containing:
- all hierarchy IDs;
- Engine version;
- config hash;
- signal QC;
- spectral state;
- mode list;
- licensed scalars;
- refusal list;
- spatial/system outputs;
- open channel;
- uncertainty;
- provenance hashes.

Atlas aggregation occurs downstream. The Atlas cannot alter Engine parameters.

## 11. Stage IX — label-blind real-data qualification

Before diagnostic comparisons:
- run healthy/repeated-session recordings;
- map fit success/failure;
- test reliability;
- test condition sensitivity;
- test site/device dependence;
- test admission/refusal repeatability;
- characterize ordinary variation.

This is where the first empirical Function and Limit Maps begin.

## 12. Stage X — clinical overlay

Only after the previous stages:
- join diagnosis/symptom variables;
- freeze task;
- select native comparators;
- split by subject;
- evaluate shared and disorder-specific structure;
- report ADDS/EQUIVALENT/SUBTRACTS/INDETERMINATE.

## 13. CI gates

Minimum future CI should run:
1. import/package test;
2. schema contract tests;
3. provenance mutation tests;
4. config hash determinism;
5. known-truth small fixtures;
6. deliberate bad-input refusal tests;
7. no-label dependency check for structural modules;
8. test preventing `whole_brain_chi`/equivalent output;
9. dependency-lineage check for every licensed scalar;
10. frozen fixture result hashes where appropriate.

## 14. Current implementation stop line

It is scientifically safe to implement:
- provenance;
- QC;
- serialization;
- test harness;
- descriptive spectral adapter;
- synthetic generators;
- modal adapters behind qualification flags.

It is **not** yet scientifically safe to implement as a production assumption:
- universal neural chi;
- universal healthy chi band;
- direct aperiodic-slope chi;
- direct Gaussian-width damping;
- disease-specific chi thresholds;
- treatment recommendations;
- clinical prediction.

## 15. Immediate next coding sequence

When executable development resumes, use:

`provenance -> QC -> spectral descriptive adapter -> known-truth generators -> modal adapter interfaces -> first state-space/DMD candidates -> qualification -> admission policy -> spatial/conglomerate -> Atlas I/O`.

This order maximizes useful progress while keeping the science reversible.