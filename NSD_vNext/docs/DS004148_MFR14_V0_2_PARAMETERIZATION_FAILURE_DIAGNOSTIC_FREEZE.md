# NSD ds004148 MFR-14 v0.2 Parameterization-Failure Diagnostic Freeze

Date: 25 September 2026
Status: FROZEN BEFORE FAILURE-STAGE DIAGNOSTIC
Program authority: SymC General Operations Manual v0.8.6

## Trigger

The untouched v0.2 cohort used sub-16 through sub-29 and the prospectively audited 57-label exact coordinate space.

Workflow run `36156773478` completed 11/14 subjects. Three subjects were refused:
- sub-21;
- sub-26;
- sub-27.

Each emitted the same third-party `NoModelError: No model fit results are available, can not proceed.`

No 11-subject partial cohort result is promoted.

## Diagnostic question

For each failed subject/session/channel, does the refusal occur in:

1. the frozen fixed aperiodic model, which is the primary descriptive representation; or
2. the knee aperiodic model, which was frozen as sensitivity-only?

## Frozen diagnostic scope

- subjects: sub-21, sub-26, sub-27 only;
- task: eyesopen;
- sessions: 1, 2, 3;
- exact stable channel space: 57 labels;
- same Welch spectrum and specparam settings as v0.2;
- exact source/D4 identities preserved.

For every subject/session/channel:
- compute the frozen Welch PSD;
- attempt the fixed fit and record success/failure plus exception type/text;
- only if fixed succeeds, attempt the knee sensitivity fit and record success/failure plus exception type/text;
- do not compute pairwise replication endpoints or cohort inference.

## Decision rule

- Any fixed-primary refusal remains a primary descriptive refusal and cannot be bypassed post hoc.
- A knee-only refusal is retained as a sensitivity-model refusal. Because the knee model was prospectively frozen as sensitivity-only, the next correction may allow the fixed primary result to survive while explicitly recording `KNEE_SENSITIVITY_REFUSED`, provided no fixed-model quantity is changed or imputed.
- Mixed fixed and knee failures require separate handling and no automatic promotion.

No thresholds or fit settings may be altered.

## Claim ceiling

This diagnostic is failure localization only. It cannot support the eyes-open replication claim, modal damping, natural frequency, lowercase chi, capital Chi, clinical inference, recovery, or population generalization.
