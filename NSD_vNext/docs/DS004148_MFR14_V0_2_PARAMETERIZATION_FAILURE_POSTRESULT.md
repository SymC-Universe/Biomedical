# NSD ds004148 MFR-14 v0.2 Parameterization-Failure Post-Result

Date: 25 September 2026
Status: ROOT CAUSE CLOSED / PRIMARY REPRESENTATION INTACT
Program authority: SymC General Operations Manual v0.8.6

## v0.2 incomplete run

Workflow run: `36156773478`

Artifact: `nsd-ds004148-eyesopen-mfr14-replication-suite-v0-2`

Artifact digest: `sha256:6e22f1ddabc9920056bab5f258db694c67e11edf7d1dac4c5a95486e32855c1e`

Result:
- 11/14 subjects completed;
- sub-21, sub-26 and sub-27 were refused with third-party `NoModelError`;
- no 11-subject partial cohort result is promoted.

## Failure-stage diagnostic

Workflow run: `36157486977`

Artifact: `nsd-mfr14-v0-2-parameterization-failure-diagnostic-v0-1`

Artifact digest: `sha256:6964325ee963c13ce790a60b0e864a0904b3e0c2cb4d6094d4ff7fc4faaa67ee`

The diagnostic reran the frozen Welch representation on the three failed subjects only and separated the fixed primary fit from the knee sensitivity fit for all 57 channels and all three eyes-open sessions.

Total channel/session fits inspected: 513.

### Fixed primary model

Fixed-primary failures: **0 / 513**.

The primary descriptive representation therefore remained admissible on every diagnostic channel.

### Knee sensitivity model

Knee-sensitivity refusals: **4 / 513**.

Exact refusals:
- sub-26, session2, O1;
- sub-26, session3, F3;
- sub-26, session3, F4;
- sub-27, session3, TP7.

Every one of those channels passed the fixed primary fit.

The original sub-21 refusal did not reproduce in the dedicated diagnostic. This is retained as evidence that the sensitivity comparator can itself be operationally unstable or fit-refusing under the frozen release-candidate implementation. It is not converted into a fixed-primary failure.

## Root cause

The replication runner made a sensitivity-lane refusal fatal to the entire subject because its helper fit the fixed and knee models in one indivisible call.

That implementation was stricter than the frozen scientific role of the models:
- fixed = primary descriptive representation;
- knee = sensitivity-only comparator.

The error therefore lies in refusal-state plumbing, not in the frozen primary endpoint.

## Correction rule

The corrected v0.2.1 execution keeps every primary setting, subject, channel space, endpoint and inferential contrast unchanged.

For each channel:
1. the fixed fit remains mandatory;
2. a fixed refusal remains fatal to that subject;
3. the knee fit remains attempted with the same frozen settings;
4. a knee refusal is recorded explicitly as `KNEE_SENSITIVITY_REFUSED`;
5. a knee refusal is not imputed, retried with relaxed settings, or labeled as model-family agreement;
6. model-family disagreement is evaluated only when both fits are available.

The pair-level record adds a separate `MODEL_FAMILY_REFUSED` flag so unavailable sensitivity comparisons remain visible in the Limit Map.

## Scientific consequence

No primary high-shift fraction, peak displacement, parent q95 threshold, subject pairing, sign test, Holm correction, or cohort membership changes.

The corrected run is therefore a completion of the already frozen v0.2 cohort, not a new independent cohort or a post-hoc threshold redesign.

## Claim ceiling

This correction cannot license modal damping, natural frequency, lowercase chi, capital Chi, clinical inference, recovery, or broad population generalization.
