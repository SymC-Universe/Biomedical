# Bio Chi Single-Series Uncertainty Method APQ Ledger v0.1

**Plan reviewed:** `BIO_CHI_SINGLE_SERIES_UNCERTAINTY_METHOD_PLAN_v0.1.md`  
**APQ level:** APQ-2 SUBSTANTIAL  
**Review limitation:** two role-isolated passes from one cognition; not independent reviewers.

| ID | Severity | Issue | Disposition | Required change |
| --- | --- | --- | --- | --- |
| A1 | MATERIAL | one observed realization per case can be seed-specific | ACCEPTED_MODIFIED | interpret method comparison against full 12-realization truth distribution; no one-seed coverage claim |
| A2 | MATERIAL | parametric bootstrap is conditional on fitted model, not truth | ACCEPTED_MODIFIED | label bootstrap as fitted-model conditional calibration; compare explicitly with known-truth distribution |
| A3 | MATERIAL | true chi location must remain visible | ACCEPTED_TEST_ADDED | report profile delta-NLL at true chi and fitted chi |
| A4 | MINOR | profile should mechanically precede bootstrap | ACCEPTED_MODIFIED | staged preflight validates likelihood/profile machinery before bootstrap/full execution |
| B1 | BLOCKER | physical-coordinate profile may not be likelihood-equivalent to C1Q | ACCEPTED_TEST_ADDED | add exact/numerical equivalence contract before plan freeze |
| B2 | MATERIAL | profile nuisance optimization can create false bumps | ACCEPTED_MODIFIED | each profile point uses continuation plus frozen multistart nuisance starts and retains the best finite NLL |
| B3 | MATERIAL | Hessian is coordinate dependent | DEFERRED_CLAIM_LIMITED | Hessian is a local comparator only; physical coordinate/units are explicit and no invariant meaning is claimed |
| B4 | MINOR | 32 bootstrap replicates are descriptive | ACCEPTED_MODIFIED | no CI/coverage threshold from bootstrap sample |

## Current disposition

APQ remains **OPEN** because B1 is a BLOCKER until a mechanical physical-parameter likelihood equivalence contract passes.

No scientific outcome has been exposed.

## Required blocker-resolution contract

For multiple admissible C parameter tuples and both 256/128 Hz:

1. convert physical (A,f_n,chi,g) to the exact raw C1Q coordinates;
2. verify the candidate state-space parameters from the raw route reproduce the intended physical coordinates within numerical tolerance;
3. evaluate NLL through the current raw implementation and the physical-coordinate wrapper on the same standardized signal;
4. require agreement to floating-point tolerance;
5. verify fitted C1Q-RS coordinates round-trip into the physical wrapper without changing NLL.

If this contract fails, the profile plan remains on scientific hold and must not execute.

If it passes, B1 becomes `ACCEPTED_TEST_ADDED` and a revised plan may be frozen.
