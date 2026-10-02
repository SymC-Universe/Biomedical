# NSD Function Map and Limit Map v0.1

Status: ACTIVE WORKING MAP
Date: 14 September 2026

## Function Map

| Domain | Function question | Current state | Next closure |
| --- | --- | --- | --- |
| Healthy spectral state | What periodic and aperiodic states are normally occupied? | 42-subject / 84-recording label-blind repeat population mapped for frozen descriptive Welch + candidate periodic/aperiodic layer | Extend subject-aware channel/region summaries; serialize first Atlas-P0-Q candidate reference artifacts without clinical tuning |
| Session stability | Which features are stable within subjects across repeated sessions? | Population repeat structure mapped; channel-wise ICC(A,1) and categorical agreement added as frozen subject-aware outputs | Inspect channel/region reliability distributions and preserve poor/negative reliability regions in the Limit Map |
| Spatial organization | Which regional/channel relationships survive preprocessing and aggregation? | Underdeveloped historically | Preserve channel/regional structure and compare with whole-head summaries |
| Modal organization | Which poles/modes/subspaces are reproducibly identifiable? | M1 rejected for real EEG; M2 recovers single-oscillator truth under white observation noise but fails model-adequacy adversaries | Complete A0/A1/A2 state-space adequacy, stationarity, residual/innovation, identifiability, held-out, and operating-region qualification before real-EEG modal admission |
| Scalar licensing | Where can a true dynamical chi be recovered? | No real-EEG scalar currently licensed; descriptive peaks and current M2 fits do not earn local chi | Freeze a qualified modal route first; then license only mode-specific scalars with explicit lineage, uncertainty, and refusal |
| Conglomerate organization | How do modes, channels, and regions organize at system level? | Exact coupled-second-order known truth now proves local damping, embedded asymptotic structure, transient gain, and recovery are not interchangeable; no real-EEG system operator yet licensed | Preserve native local/modal and system descriptors; next empirical gate is identifiable coupling/operator structure without forcing scalar collapse |
| Healthy-to-clinical comparison | Which structures shift in ASD or other phenotypes? | Intentionally blocked downstream of T0/T1; historical findings remain non-authoritative | Lock qualified healthy/reference layers first, then freeze a subject-level clinical task with simple/native baselines and untouched evidence |
| Development/age | How does architecture change with age? | Atlas target | Age-residualized reference design |
| Perturbation/recovery | How does the system respond to state changes? | Candidate future track | Repeated-state or longitudinal datasets |
| Comorbidity | Are shared clinical features reflected in shared neurophysiological organization? | Hypothesis | Multi-disorder data and competing explanations |

## Limit Map

| Limit ID | Boundary / failure | Required response |
| --- | --- | --- |
| NSD-L01 | No licensed second-order mode | Refuse dynamical chi; retain native feature/modal representation |
| NSD-L02 | Peak center frequency cannot be converted to omega_0 | Do not use it as omega_0 |
| NSD-L03 | Width contains unresolved non-damping broadening | Do not interpret width as gamma |
| NSD-L04 | Peak absent or fit rejected | Preserve categorical/absent-feature state |
| NSD-L05 | Whole-head average erases material spatial structure | Retain spatial representation |
| NSD-L06 | Trial/session multiplicity dominates subject count | Use subject-aware inference; refuse pseudo-replication |
| NSD-L07 | Metadata join ambiguous | Quarantine unmatched/ambiguous records |
| NSD-L08 | Healthy baseline changes by disorder comparison | Version change or refuse claimed common reference |
| NSD-L09 | Site/acquisition effects dominate phenotype | Lower clinical claim ceiling and model site explicitly |
| NSD-L10 | Scalar and modal features are algebraically redundant | Count as one information dimension |
| NSD-L11 | Clinical labels used to tune basic structure extraction | Treat as development/calibration, not independent validation |
| NSD-L12 | Cross-sectional separation interpreted as future prediction | Refuse predictive wording |
| NSD-L13 | Simple/native baseline matches or beats NSD architecture | Classify EQUIVALENT or SUBTRACTS, not ADDS |
| NSD-L14 | Disorder-specific result fails external transfer | Restrict scope to tested cohort/site |
| NSD-L15 | No coherent shared architecture across disorders | Retire or narrow shared-instability claim |
| NSD-L16 | Method failure suggests biology but lacks independent test | Treat as new hypothesis, not biological transition evidence |
| NSD-L17 | Single-oscillator covariance model fits multimode/nonstationary/nonoscillatory truth | Refuse real-EEG modal damping until explicit model adequacy/order qualification is satisfied |
| NSD-L18 | Alternative-model diagnostic improves by adding complexity even for valid single-mode truth | Do not freeze pseudo-BIC/model-order threshold; require statistically justified likelihood/held-out adequacy framework |\n| NSD-L19 | Identical local modal damping ratios can coexist with different embedded spectra, transient gain, or global stability | Do not use local chi vector or any average of local chi as a sufficient system-level descriptor |\n| NSD-L20 | Identical full eigenspectra can coexist with materially different transient amplification and recovery in non-normal coupled systems | Do not treat eigenspectrum/spectral abscissa alone as sufficient for perturbation or resilience claims; retain reactivity/transient/recovery descriptors where the question requires them |
| NSD-L21 | Whole-record A2 can arise from sequential frequency reorganization rather than two simultaneous stationary modes | Require temporal-consistency/stationarity evidence before interpreting A2 as concurrent modal multiplicity |
| NSD-L22 | Whole-record A1 can hide large damping changes or finite-burst/amplitude occupancy nonstationarity | Require split-window pole stability and occupancy/intermittency diagnostics when a persistent stationary mode is claimed |
| NSD-L23 | A standard-toolkit comparator without a zero-oscillator candidate cannot fairly test nonoscillatory refusal | Mark zero-versus-oscillator rows NOT_DIRECTLY_COMPARABLE and add a comparator family with an explicit nonoscillatory alternative before adequacy claims |
| NSD-L24 | Deterministic resampling can change A0/A1/A2 model-order behavior for stochastic controls | Treat sampling/preprocessing as part of model qualification; do not assume a matched-rate transform is semantically neutral |

## Priority balance check

Current NSD work has now materially strengthened representative healthy/function mapping through the 42-subject repeat population while also exposing substantial descriptive and modal limits. The balance rule still favors continued ordinary healthy/channel/region mapping in parallel with the M2 adequacy challenge. The project should not become failure-only: the next Atlas work should preserve both the high-occupancy functioning interior and the outlier/refusal structure rather than allowing adversarial modal work to displace representative neurophysiology.


## 22 September coupled-system known-truth update

Run `35759456553` closed the first explicit second-order GOM v0.8.3 local-chi / broader-system known-truth task.

The exact fixtures establish:
- same local `zeta_i` + same full eigenvalues can still produce maximum transient gain 1.0 versus ~2.34 and different sustained return behavior;
- same local `zeta_i` can reorganize the embedded modal spectrum under reciprocal coupling;
- stable isolated modes can become globally unstable after coupling.

This is a Limit-Map result about representation sufficiency. It is not evidence that these particular matrices describe human EEG.

Canonical audit:
`CHI_SYSTEM_COUPLED_KNOWN_TRUTH_POSTRESULT_v0.1.md`.


## 22 September stationarity and first-toolkit update

### Stationarity challenge

Run `35758951850` shows that whole-record model order is insufficient for temporal interpretation:

- frequency-shift truth produced A2 in 3/3, but half-record frequency disagreement was ~0.507 versus ~0.012 for stationary single-mode truth;
- damping-shift truth remained A1 in 3/3 while half-record damping disagreement rose to ~0.497 versus ~0.014 for the stationary control;
- finite bursts remained A1 in 3/3 but produced RMS-window CV ~0.472 and max/min ~3.30 versus ~0.039 and ~1.12 in the stationary control;
- an amplitude-step control likewise remained A1 while producing strong RMS occupancy heterogeneity.

These are candidate diagnostic channels only. No production threshold is frozen from the same rows.

Canonical audit:
`STATE_SPACE_STATIONARITY_POSTRESULT_v0.1.md`.

### SOMATA first matched-information comparator

Run `35758411626` mechanically and scientifically completed the first P0-Q SOMATA 0.5.6 iOsc comparison.

On directly comparable oscillator-count tasks, gross model-count agreement was present for valid single truth, separated two-mode truth, colored-observation challenge and finite bursts, with partial disagreement on close modes and mid-record frequency shift.

However, the shared 120 Hz resampling transform changed NSD behavior relative to its native 256 Hz qualification map for colored observation noise and nonoscillatory AR(1). Therefore the first lane exposes a sampling/preprocessing confound as well as inter-method differences.

Because iOsc has no zero-oscillator candidate, nonoscillatory refusal remains not directly comparable.

Canonical audit:
`SOMATA_COMPARATOR_POSTRESULT_v0.1.md`.
