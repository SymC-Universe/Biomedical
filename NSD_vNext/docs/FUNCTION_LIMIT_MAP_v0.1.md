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
| Conglomerate organization | How do modes, channels, and regions organize at system level? | Candidate architecture | Build relational/network measures without forcing scalar collapse |
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
| NSD-L18 | Alternative-model diagnostic improves by adding complexity even for valid single-mode truth | Do not freeze pseudo-BIC/model-order threshold; require statistically justified likelihood/held-out adequacy framework |

## Priority balance check

Current NSD work has now materially strengthened representative healthy/function mapping through the 42-subject repeat population while also exposing substantial descriptive and modal limits. The balance rule still favors continued ordinary healthy/channel/region mapping in parallel with the M2 adequacy challenge. The project should not become failure-only: the next Atlas work should preserve both the high-occupancy functioning interior and the outlier/refusal structure rather than allowing adversarial modal work to displace representative neurophysiology.
