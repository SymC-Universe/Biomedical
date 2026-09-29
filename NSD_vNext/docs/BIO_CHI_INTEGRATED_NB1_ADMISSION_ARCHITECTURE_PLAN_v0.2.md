# Bio Chi Integrated N-B1 Admission/Refusal Architecture Plan v0.2

**Status:** FORMAL APQ CANDIDATE / NOT FROZEN  
**Date:** 29 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Supersedes for planning:** `BIO_CHI_INTEGRATED_NB1_ADMISSION_ARCHITECTURE_PLAN_v0.1.md`

## Scientific target

Define a prospective, qualification-only admission/refusal architecture for candidate local biological chi that keeps practical identifiability separate from semantic model admissibility.

The architecture must answer a narrower question than “can the model fit?”:

> Under known truth, when is a local chi coordinate scientifically licensed by all required upstream evidence, and when must the system retain only modal/vector/system information?

No real-EEG admission is authorized by this plan.

## Evidence channels

Each channel is recorded independently. No weighted score or compensatory total is permitted.

1. **P — provenance / data identity**
   - source identity, sampling rate, duration, transform lineage, generator identity for known truth.
2. **S — signal / sampling validity**
   - alias risk, resolution sufficiency, paired-rate consistency where the design provides it.
3. **T — stationarity / declared time variation**
   - stationary claim supported, or explicit time variation modeled rather than hidden.
4. **F — model-family admissibility**
   - C-family representation must survive direct family competitors and semantic controls.
5. **O — order / multiplicity**
   - one-mode local coordinate requires order adequacy; unresolved or genuine multimode truth cannot be collapsed into one local scalar.
6. **M — memory / closure**
   - colored-memory, hidden-state, closure, and substrate-memory alternatives remain independent gates.
7. **R — observation / reference sensitivity**
   - where applicable, candidate local quantities must not depend on an unqualified observation projection or reference transform.
8. **N — numerical / search integrity**
   - basin coverage, boundary behavior, optimizer reproducibility, and invariant likelihood reproduction.
9. **I — practical identifiability**
   - profile likelihood is the primary single-record geometry; compactness is not a family-membership test.
10. **U — uncertainty / rate sensitivity**
    - uncertainty, finite-sample dispersion, and paired-rate behavior are preserved as separate evidence.

## Decision grammar

Allowed integrated outputs are:

- `QUALIFICATION_ELIGIBLE`
- `REFUSED`
- `NEED_MORE_INFO`
- `NOT_APPLICABLE`

`REFUSED` must carry one or more structured reason labels from the evidence channels above.

Examples:

- `REFUSED[FAMILY]`
- `REFUSED[ORDER,MEMORY]`
- `REFUSED[NONSTATIONARY,PROFILE_NONIDENTIFIABLE]`
- `NEED_MORE_INFO[REFERENCE_SENSITIVITY]`

No favorable channel can cancel a refusal in another required channel.

## Hard logical rules

The following are logical refusals, not empirical tolerances:

- known truth outside C cannot become C because profile geometry is compact;
- genuine multimode truth cannot be reduced to one-mode chi without a separately licensed mode-specific decomposition;
- a nonstationary truth cannot be interpreted as a stationary local scalar unless the time-varying model itself is the qualified object;
- unresolved memory/closure failure blocks a memoryless local scalar interpretation;
- optimizer nonreproducibility or an unverified lower likelihood basin blocks coordinate admission;
- absent provenance or sampling identity blocks scientific interpretation.

## Empirical tolerances

No new numerical tolerance is frozen from the already-viewed 72-row Profile Function/Limit packet.

Any future empirical tolerance must be:

1. defined on a prospectively separated development population;
2. linked to a declared error consequence;
3. frozen before untouched qualification;
4. evaluated on untouched known truth;
5. reported as an operating-region tolerance, not a universal biological boundary.

Existing previously frozen tolerances from qualified subcomponents may be retained only for the exact role for which they were qualified.

## Qualification packet architecture

The later untouched packet must contain both Function and Limit truth and must not use biological prevalence as its class proportion.

### Function roles

- regular one-mode interior;
- low-information but semantically valid one-mode;
- near-critical valid one-mode;
- near-nuisance-boundary valid one-mode;
- high-frequency / sampling-edge valid one-mode;
- valid time-varying local mode only where the time-varying representation is explicitly declared.

### Limit roles

- D outside C;
- S outside D;
- colored-memory / extra-pole truth;
- genuine separated multimode truth;
- close/unresolved multimode truth;
- stationary surrogate versus actual nonstationary truth;
- observation/reference-sensitive truth where the latent object is not invariantly recoverable;
- numerical basin challenge where the semantic family is valid but the estimator route is not reliable.

The packet must include representative functioning cases as well as adversarial failures. Designed class counts are qualification coverage, not prevalence.

## Primary scientific questions

1. Can all semantically invalid truth classes be refused even when local C fits are compact?
2. Can representative valid C truths remain eligible when the information is genuinely sufficient?
3. Can the architecture distinguish semantic refusal from estimator failure?
4. Can valid-but-weak cases be labeled NEED_MORE_INFO rather than misclassified as family failure?
5. Does refusal preserve the broader modal/vector/system information needed by N-B2/N-B3?
6. Are refusal reasons stable under the declared paired-sampling and uncertainty contract?

## Anti-circularity

The completed 72-row profile packet may justify the separation of roles but may not supply newly optimized cutoffs for the integrated test.

The untouched qualification packet must be generated from a new frozen identity set after APQ closure.

## Claim ceiling

Passing this architecture would establish only a known-truth qualification gate for future local-chi work.

It would not establish:

- biological prevalence;
- clinical meaning;
- a universal neural threshold;
- real-EEG local chi;
- production-estimator promotion;
- a whole-system scalar;
- equivalence between local chi and broader Chi/system architecture.

## APQ questions required before freeze

- Are any required evidence channels redundant enough to create hidden double counting?
- Which channels are logical gates and which require empirical tolerance calibration?
- Can NEED_MORE_INFO be distinguished prospectively from REFUSED without outcome tuning?
- Does the packet include enough ordinary Function cases to avoid becoming failure-only?
- Are observation/reference sensitivity and stationarity tested only where scientifically meaningful?
- Does the architecture preserve modal/vector/system information after scalar refusal?
- Are all thresholds either inherited from prior frozen qualifications or prospectively separated from untouched evaluation?

No substantial integrated computation is authorized until these questions receive APQ adjudication.
