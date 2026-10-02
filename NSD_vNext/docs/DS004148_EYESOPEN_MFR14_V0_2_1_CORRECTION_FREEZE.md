# NSD ds004148 Eyes-Open MFR-14 v0.2.1 Refusal-Semantics Correction Freeze

Date: 25 September 2026
Status: FROZEN BEFORE CORRECTED COHORT RE-EXECUTION
Program authority: SymC General Operations Manual v0.8.6

## Purpose

This is not a new cohort, new threshold, or new hypothesis.

It completes the already frozen v0.2 replication after the failure-stage diagnostic established that:
- fixed-primary failures = 0 / 513 diagnostic channel fits;
- knee-sensitivity refusals = 4 / 513;
- the v0.2 runner incorrectly made a sensitivity-only refusal fatal to the entire subject.

The exact evidence and root cause are recorded in:

`DS004148_MFR14_V0_2_PARAMETERIZATION_FAILURE_POSTRESULT.md`.

## Frozen science retained unchanged

v0.2.1 reuses:
- subjects sub-16 through sub-29;
- all three eyes-open sessions;
- exact stable57 channel space;
- exact source/D4 gate;
- exact frozen Welch settings;
- exact fixed and knee specparam settings;
- exact ds003775 57-label parent reference derivation;
- exact subject-level pair endpoints;
- exact two predeclared high-shift-fraction contrasts;
- exact sign tests and Holm correction;
- exact claim ceiling.

## Only correction

For each channel:

1. fixed primary fit remains mandatory;
2. fixed refusal remains a subject-level refusal;
3. knee sensitivity fit is still attempted with unchanged settings;
4. knee refusal is retained as `KNEE_SENSITIVITY_REFUSED`;
5. knee refusal is not retried with relaxed settings, imputed, or counted as agreement;
6. model-family disagreement is evaluated only when the sensitivity comparison is available;
7. pair-level `MODEL_FAMILY_REFUSED` is reported independently from `MODEL_FAMILY_UNSTABLE`.

The primary high-shift endpoint uses fixed-model descriptive peaks and is mathematically unchanged by this correction.

## Reproducibility note

The diagnostic also found that the original sub-21 sensitivity refusal did not reproduce on rerun. That non-reproducibility is preserved as a Limit-Map property of the sensitivity comparator and is another reason not to let the sensitivity lane veto an otherwise admissible fixed-primary result.

## Promotion rule

The corrected cohort may be promoted only if:
- all 14 frozen subjects pass source/D4 and fixed-primary processing;
- no subject replacement occurs;
- parent reference remains 57-label and 42-subject;
- all primary contrasts are produced at subject level;
- knee refusals remain explicitly visible;
- modal/damping/chi/capital-Chi/clinical firewalls remain false.

## Checkpoint continuation

If the corrected v0.2.1 result closes interpretable, proceed automatically to the prospectively frozen eyes-closed state-specificity test. If it fails, investigate the new failure before continuing.
