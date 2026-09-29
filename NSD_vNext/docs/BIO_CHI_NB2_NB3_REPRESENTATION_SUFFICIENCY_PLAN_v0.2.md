# Bio Chi N-B2/N-B3 Representation-Sufficiency Plan Packet v0.2

**Status:** FORMAL APQ CANDIDATE / NOT FROZEN  
**Date:** 29 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Parent novelty records:** `BIO_CHI_NB2_NB3_REPRESENTATION_SUFFICIENCY_P0N_v0.2.md`, `BIO_CHI_NB2_NB3_REPRESENTATION_SUFFICIENCY_A0_v0.1.md`

## Residual scientific target

The surviving question is not whether non-normality, perturbation direction, DMD, controllability, or recovery dynamics exist. Those are prior art.

The target is:

> For a declared stability observable, what is the least representation that remains sufficient, and where must reduction be refused?

The result is a Function/Limit map of representation sufficiency, not a universal ranking.

## Representation ladder

Representations are nested only by information content, not by presumed scientific superiority.

- **R0 Local modal damping vector:** local natural frequencies and damping coordinates for individually defined modes.
- **R1 Embedded eigenspectrum:** full-system poles/eigenvalues and asymptotic stability information.
- **R2 Non-normal/reactivity structure:** R1 plus left/right eigenspace geometry, numerical abscissa, and other native finite-time structural descriptors.
- **R3 Finite-time propagator structure:** state-transition / propagator information sufficient to derive direction-dependent transient growth under a declared state metric.
- **R4 Input-output perturbation structure:** explicit `(A,B,C)` or equivalent perturbation and observation operators, preserving perturbation direction and measured projection.
- **R5 Full frozen operator/state-space representation:** the generating or identified model needed when lower representations are insufficient or when time variation requires an explicitly indexed operator sequence.

No whole-system chi scalar is defined.

## Target observables

Each target is adjudicated separately.

- **T0 asymptotic stability:** sign and margin of the dominant asymptotic growth/decay rate.
- **T1 embedded modal organization:** frequency/decay content of the coupled system.
- **T2 peak transient amplification:** maximum physically declared response gain over the frozen horizon.
- **T3 transient peak timing and direction:** time of peak and perturbation direction producing it.
- **T4 perturbation-specific recovery trajectory:** full response trajectory after a declared perturbation.
- **T5 integrated recovery burden:** threshold-free integral functional of the declared response norm over the frozen horizon.
- **T6 observed recovery under partial projection:** recovery in the measured output after applying `C`.
- **T7 reorganization under time variation:** change in modal/operator organization when the generating operator is explicitly time varying.

No single target is allowed to stand in for all others.

## Primary sufficiency labels

For each representation-target pair:

- `SUFFICIENT`
- `ADDITIVE`
- `EQUIVALENT`
- `REFUSED_NOT_IDENTIFIABLE`
- `REFUSED_NOT_INVARIANT`
- `NEED_MORE_INFO`
- `NOT_APPLICABLE`

No global winner or score is computed.

## Function Map families

The plan must include ordinary cases where reduction genuinely works.

- **F0 decoupled normal modes:** local modal vector sufficient for local and asymptotic questions.
- **F1 normal coupled system:** eigenspectrum sufficient for T0/T1 and richer layers add no value for those targets.
- **F2 weakly non-normal system:** richer descriptors may be equivalent within the declared observable and horizon.
- **F3 input-output aligned system:** R4 collapses to lower representation for the declared perturbation because B/C excite and observe only the sufficient subspace.
- **F4 stable stationary system with reproducible finite-time response:** all required quantities identifiable and sampling stable.

Function cases are required so the experiment does not become a catalog of failure.

## Limit Map families

Matched pairs must isolate the missing information.

- **L0 same local damping, different embedded eigenspectrum.**
- **L1 same local damping and same eigenspectrum, different non-normality and transient gain.**
- **L2 same A, different B:** identical autonomous dynamics but different perturbation accessibility.
- **L3 same A and B, different C:** identical latent response but different observed recovery.
- **L4 same eigenspectrum, similarity-related state coordinates:** test coordinate dependence of state-norm transient gain and eigenvector conditioning.
- **L5 stationary generator versus time-varying generator with a stationary surrogate fit.**
- **L6 partial-observation / unobservable mode:** richer latent representation exists but is not recoverable from the declared measurement.
- **L7 sampling / finite-duration challenge:** representation changes because the observation contract cannot identify the richer object.
- **L8 higher-order or multimode system whose local damping vector is correct but insufficient for target response.**

## Invariance firewall

State-coordinate quantities are not automatically scientific observables.

For every similarity transform `x' = Sx`:

- `A' = SAS^{-1}`
- `B' = SB`
- `C' = CS^{-1}`

Input-output behavior is preserved under the transformed realization, but Euclidean state norms, eigenvector conditioning, and some transient-gain summaries can change.

Therefore:

1. Euclidean state-norm gain is descriptive only unless the state coordinates have a declared physical metric.
2. A physical state metric `G`, if used, must transform consistently and be frozen before outcome inspection.
3. Input-output response functions and transfer behavior are preferred invariance controls when B/C are part of the scientific question.
4. Any representation feature that changes under a mere state reparameterization without a changed observable must be labeled `REFUSED_NOT_INVARIANT` for cross-realization interpretation.

## Recovery firewall

No arbitrary return-to-baseline threshold is allowed to become the primary result.

Primary recovery objects are:

- the full response curve;
- integrated response burden over the frozen horizon;
- peak amplitude;
- peak time;
- decay envelope or modal content where licensed;
- output-specific response after C.

Thresholded return times may be retained only as secondary diagnostics with frozen thresholds and sensitivity analysis.

## Observation and perturbation firewall

A and its eigenspectrum do not determine what can be excited or observed.

The plan therefore treats B and C as first-class scientific objects for T3-T6.

If B or C is absent from the data-generating/measurement contract, claims requiring them must be `NOT_APPLICABLE` or `NEED_MORE_INFO`, not silently inferred.

## Sampling and time-variation firewall

Sampling, finite duration, and model stationarity are part of representation qualification.

The packet must include paired sampling and duration controls and must separate:

- a stationary system observed imperfectly;
- a genuinely time-varying operator;
- a stationary surrogate fitted to a time-varying truth.

No whole-record eigenstructure may be interpreted as persistent organization without temporal-consistency evidence.

## Prospective matched-pair architecture

The computation should be organized around matched pairs or small matched families in which exactly one information layer changes while lower layers are held fixed where mathematically possible.

Each row must preserve:

- generator matrices/operators;
- local modal coordinates;
- full eigenspectrum;
- non-normal/reactivity descriptors;
- B and C where defined;
- state metric if one is used;
- exact perturbation vector or family;
- full response curves;
- sampling identity;
- representation-target adjudication;
- refusal reason when applicable.

## Primary scientific questions

1. For T0 and T1, how often are R0 or R1 genuinely sufficient?
2. For T2 and T3, when does R2 or R3 become necessary?
3. For T4-T6, when are B/C indispensable even if A is known exactly?
4. Which candidate descriptors fail under similarity/state rescaling?
5. When does a richer representation add no information for the declared target?
6. When does richer representation exist mathematically but remain unidentifiable from the observation contract?
7. Can the Function/Limit map preserve ordinary sufficiency regions while locating exact reduction failures?

## Native comparators

The plan must include, where applicable:

- eigenspectrum / spectral abscissa;
- numerical abscissa/reactivity;
- propagator singular-value analysis;
- input-output impulse response;
- controllability/observability quantities;
- DMD/Koopman-style fitted operator summaries where estimation rather than exact truth is being tested.

These are native comparators, not SymC-derived novelty claims.

## Outcome architecture

- **A REPRESENTATION_MAP_SUPPORTED:** target-specific sufficiency/refusal structure is reproducible and lower versus richer layers separate by question.
- **B MOSTLY_NATIVE_EQUIVALENCE:** native lower-dimensional descriptors already suffice for most declared targets; report equivalence rather than force additional architecture.
- **C IDENTIFIABILITY_DOMINATED:** richer representations are theoretically relevant but cannot be recovered reliably under the frozen observation contract.
- **D NO_STABLE_MAP:** sampling, realization, or coordinate dependence prevents a reproducible sufficiency map.
- **E NEED_MORE_INFO:** current packet cannot distinguish competing interpretations without a new prospectively frozen design.

## Claim ceiling

This experiment cannot establish:

- a universal representation hierarchy;
- a whole-brain chi;
- biological prevalence;
- disease meaning;
- real-EEG local-chi admission;
- discovery of non-normality, DMD, controllability, or perturbation-response dynamics.

It can establish only a known-truth representation-sufficiency map for the frozen targets and observation contracts.

## APQ questions required before freeze

- Are the Function cases sufficient to prevent adversarial overrepresentation?
- Are R2/R3 descriptors defined in coordinate-invariant or explicitly metric-dependent form?
- Are B/C controls sufficient to isolate perturbation and observation effects?
- Are recovery targets threshold free at the primary level?
- Are time-varying and stationary-surrogate cases distinguishable without using outcome-tuned thresholds?
- Are native comparators bound to the same information and observation contract?
- Can any proposed representation-target adjudication be reproduced without a subjective ranking?

No substantial N-B2/N-B3 computation is authorized until APQ closes these questions.
