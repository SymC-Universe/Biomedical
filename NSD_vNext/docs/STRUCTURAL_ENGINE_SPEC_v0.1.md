# NSD Structural Engine Specification v0.1

Date: 14 September 2026
Status: DESIGN-FROZEN ENOUGH FOR IMPLEMENTATION PLANNING / NOT YET QUALIFIED

## 1. Purpose

The NSD Structural Engine is the executable representation layer that turns neurophysiological recordings into a transparent multilevel architecture without using diagnosis to manufacture structure.

It is **not** a classifier by default and it is **not** a machine that outputs one whole-brain chi.

Primary question:

> What signal, modal, spatial, and system-level structure is recoverable from the recording before clinical labels are consulted?

## 2. Engine boundaries

### Inputs

Minimum supported input schema should permit:
- subject identifier;
- session identifier;
- trial/epoch identifier where present;
- channel/sensor identifier;
- recording condition;
- sampling rate;
- signal array or a fully traceable intermediate;
- acquisition/site/device metadata where available;
- preprocessing provenance;
- optional covariates stored separately from structural feature construction.

Clinical diagnosis and outcome labels may exist in the project dataset but must not enter the structural-fit stage.

### Outputs

The Engine returns a structured record, not a single score:

1. **Spectral state**
   - aperiodic offset;
   - aperiodic exponent;
   - knee parameter where justified;
   - complete periodic peak list;
   - center frequencies;
   - powers/amplitudes;
   - bandwidths and exact model convention;
   - fit residuals and fit quality;
   - zero-peak state.

2. **Vector/modal state**
   - modal frequencies where recoverable;
   - decay/growth rates where recoverable;
   - complex poles/eigenvalues where the chosen estimator supports them;
   - mode shapes/participation where spatial data support them;
   - mode count and model-order uncertainty;
   - rejected/unstable/non-identifiable modes.

3. **Scalar stability coordinates**
   - only quantities admitted by the Estimator Licensing Matrix;
   - mode-specific chi when licensed;
   - explicit provenance from primitive fitted parameters to each scalar;
   - uncertainty interval/distribution;
   - refusal code when a scalar is not admissible.

4. **Conglomerate/system organization**
   - regional distributions;
   - channel participation;
   - interregional relationships;
   - mode co-occurrence/organization;
   - spatial heterogeneity;
   - network or relational summaries that pass independent qualification.

5. **Open channel**
   - missing data;
   - poor fits;
   - rejected modes;
   - absent peaks;
   - ambiguous metadata;
   - artifact flags;
   - out-of-domain states;
   - model disagreements;
   - reasons for scalar refusal.

## 3. Layered execution sequence

### Stage E0 — Provenance and hierarchy gate

Before numerical analysis:
- validate subject/session/trial keys;
- detect duplicate records;
- verify sampling metadata;
- verify channel map;
- record site/device/condition;
- quarantine ambiguous joins;
- refuse silent “first row wins” behavior.

### Stage E1 — Signal integrity gate

Record:
- duration;
- missingness;
- clipping/saturation;
- flat channels;
- line noise;
- gross artifacts;
- effective usable duration;
- preprocessing operations that change frequency content or spatial structure.

The Engine must distinguish “bad signal” from “interesting biology.”

### Stage E2 — Native spectral state

Compute the prespecified spectral estimator with configuration fully serialized.

Required outputs:
- raw/processed PSD summary;
- fit range;
- frequency resolution;
- periodic/aperiodic decomposition;
- residual diagnostics;
- parameter uncertainty where available.

No chi is produced at E2 merely because a parameter is called an exponent, width, or frequency.

### Stage E3 — Candidate modal extraction

At least two conceptual routes should remain separable:

A. **spectral resonance route**
- identify candidate peaks/modes;
- fit candidate generative forms where justified;
- compare Gaussian/descriptive and dynamical resonance models rather than assuming equivalence.

B. **state-space / time-domain route**
- recover candidate complex modes through an output-only/state-space or explicitly generative model;
- estimate decay and oscillation terms;
- quantify model order and stability.

The project may eventually support both. They are not to be merged until equivalence is demonstrated for the relevant data regime.

### Stage E4 — Scalar admission gate

For every candidate dynamical scalar:
- identify source mode;
- identify parameter convention;
- verify estimator qualification status;
- compute uncertainty;
- check non-damping broadening controls;
- check center-frequency versus natural-frequency conversion;
- check algebraic dependency with Q or related features;
- emit either a value or a refusal code.

### Stage E5 — Spatial and conglomerate construction

Preserve channel and regional structure before aggregation.

Candidate outputs:
- regional feature distributions;
- posterior-anterior gradients;
- hemispheric differences;
- participation maps;
- mode-shape similarity;
- interregional covariance/coupling under a declared estimator;
- cross-layer relationships.

Whole-head summaries are allowed as comparators but do not replace the spatial representation.

### Stage E6 — Reliability and ordinary-state mapping

Before diagnosis:
- within-session stability;
- between-session reliability;
- condition sensitivity;
- trait versus state components;
- acquisition/site effects;
- age/development trends where data permit;
- scalar-admission/refusal stability.

This stage feeds the Neurostability Atlas.

### Stage E7 — Clinical overlay

Only after E0-E6 structural qualification are labels joined for:
- group comparisons;
- dimensional symptom analysis;
- disorder-specific architecture;
- shared versus distinct phenotype tests;
- classification;
- later, if longitudinal data support it, prediction.

## 4. Refusal codes

The Engine must make non-results machine-readable.

Proposed initial codes:

| Code | Meaning |
| --- | --- |
| `REF_META_AMBIGUOUS` | subject/session/trial linkage cannot be resolved safely |
| `REF_SIGNAL_INSUFFICIENT` | insufficient usable signal duration/quality |
| `REF_SPECTRAL_POOR_FIT` | periodic/aperiodic model does not fit adequately |
| `REF_NO_PEAK` | no qualifying periodic peak exists |
| `REF_MODE_NONIDENTIFIABLE` | dynamical mode cannot be uniquely/reliably recovered |
| `REF_MODEL_DISAGREEMENT` | candidate dynamical models disagree beyond frozen tolerance |
| `REF_WIDTH_NOT_DAMPING` | width exists but damping interpretation is not licensed |
| `REF_FREQ_NOT_OMEGA0` | observed center frequency cannot be mapped to required natural frequency |
| `REF_BROADENING_UNRESOLVED` | non-damping broadening is not bounded |
| `REF_UNCERTAINTY_TOO_LARGE` | parameter/chi uncertainty exceeds admissible bound |
| `REF_OUT_OF_DOMAIN` | signal lies outside qualified Engine regime |

Refusal rates are themselves part of the Limit Map and must not be silently excluded from reporting.

## 5. No-label construction rule

The following are prohibited during Engine construction/qualification:
- choosing peak thresholds because they separate diagnoses better;
- choosing regions because they maximize case-control effects before freezing;
- changing fit ranges separately by disorder without an independent physical reason;
- retuning the healthy baseline for each disease;
- selecting scalar-admission thresholds on clinical accuracy;
- dropping zero-peak or poor-fit subjects because they harm separation.

Diagnosis may evaluate structure. It may not define the structure being evaluated.

## 6. Minimum result object

A production result should be serializable as a structured object containing at least:

```text
subject_id
session_id
recording_condition
signal_qc
spectral_state
periodic_peaks[]
aperiodic_state
candidate_modes[]
mode_qualification[]
licensed_scalars[]
scalar_refusals[]
spatial_state
conglomerate_state
open_channel
provenance
software_version
configuration_hash
```

## 7. Versioning rule

Any change to:
- preprocessing;
- spectral parameterization;
- model family;
- mode-order selection;
- scalar-admission rule;
- refusal threshold;
- region definition;
- feature dependency logic;

requires an Engine version increment and a migration note.

The Atlas must record which Engine version generated every coordinate.

## 8. Engine qualification target

The Engine does not earn the word “qualified” by producing plausible plots. Qualification requires:
- known-truth recovery;
- adversarial failure tests;
- robustness to reasonable nuisance variation;
- documented refusal behavior;
- repeatability;
- label-blind adequacy on real neurophysiology;
- a frozen configuration before confirmatory clinical tests.

The historical NSD paper demonstrated why this separation is necessary: an architecture can be visually compelling before its numerical estimators are scientifically licensed.