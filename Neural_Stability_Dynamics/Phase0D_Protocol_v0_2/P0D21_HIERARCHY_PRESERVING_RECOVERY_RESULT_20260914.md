# P0-D21 Hierarchy-Preserving Recovery Result

Date recorded: 2026-09-14
Execution date: 2026-09-14
Status: **P0-D exploratory synthetic evidence; not P0-Q or P1. No reduction threshold, chi_system rule, neural hierarchy rule, or Atlas interpretation frozen.**
Purpose: `FUNCTION_MAPPING + LIMIT_MAPPING`

## Source of record
- Run `34796996958`, job `103831912585`
- Source commit `265d58f0a84cb27e198ac2576f2a94adc8af129c`
- Dedicated workflow conclusion: `success`
- Hierarchy-preserving recovery tests: `5 passed`
- Branch-wide P0 validation run `34796996918`: `success`
- Artifact `10330151472`
- Artifact ZIP SHA-256 `6295d579ac041ef9bb085b7ba4f070c9618d84c4ddec0b64a62833a6762f2a4f`

## Question
When an internally coupled pair of subsystems is grouped into a higher-level entity, does preserving its internal state preserve the outer subsystem's recovery response, and what happens if the internally coupled component is incorrectly dropped?

## Fixed construction
- Three stable second-order synthetic subsystems with local chi values `[0.55, 0.75, 0.90]` and frequencies `[3, 5, 7] Hz`.
- Outer `G <-> B` coupling norm fixed at `4`.
- Internal `B <-> C` coupling strength `h` scanned over `[0, 1, 2, 3, 4, 5, 6, 8, 10]`.
- Exact grouped representation retains the complete `B+C` internal state.
- Truncated control drops subsystem `C`.
- Atlas not used. The firewalled prospective `chi ~ 1.2-1.3` note was not used.

## Results

The exact grouped construction reproduced the full generator and the observed outer recovery response to numerical precision for every scanned `h` (`grouped_matrix_error = 0`; grouped outer-response errors = 0 in the recorded implementation).

The truncated construction agreed when `h=0`, where the omitted subsystem is dynamically disconnected from the retained internal subsystem, but diverged progressively as internal coupling increased.

| h | Position outer error, truncated | Velocity outer error, truncated | tau full (s) | tau truncated (s) |
|---:|---:|---:|---:|---:|
| 0 | 5.90e-16 | 5.30e-16 | 0.09263283 | 0.09263283 |
| 1 | 9.17e-06 | 7.18e-06 | 0.09262595 | 0.09263283 |
| 2 | 3.67e-05 | 2.87e-05 | 0.09260550 | 0.09263283 |
| 3 | 8.27e-05 | 6.48e-05 | 0.09257208 | 0.09263283 |
| 4 | 1.47e-04 | 1.15e-04 | 0.09252675 | 0.09263283 |
| 5 | 2.31e-04 | 1.81e-04 | 0.09247106 | 0.09263283 |
| 6 | 3.34e-04 | 2.62e-04 | 0.09240713 | 0.09263283 |
| 8 | 5.99e-04 | 4.70e-04 | 0.09226631 | 0.09263283 |
| 10 | 9.47e-04 | 7.44e-04 | 0.09213401 | 0.09263283 |

All full systems remained asymptotically stable over the scanned surface.

## Supported P0-D interpretation
1. Exact regrouping that retains the complete internal dynamical state can preserve the higher-level recovery response exactly in this synthetic construction.
2. Grouping is therefore not equivalent to arbitrary dimensionality reduction.
3. Dropping a subsystem that participates in internal feedback can alter the outer realized recovery even when the external coupling interface is otherwise unchanged.
4. The magnitude of the truncation error increased with the strength of the omitted internal feedback over the tested surface.
5. This extends P0-D18 from feedback-return algebra to explicit recovery trajectories.
6. The result supports a distinction between `HIERARCHICAL_REPRESENTATION_PRESERVED` and `INTERNAL_DYNAMICS_TRUNCATED`; it does not select a numerical adequacy threshold.

## Nonclaims
- No biological hierarchy law is inferred.
- No dimensional-reduction threshold is selected.
- No `chi_system` is defined.
- No empirical neural recovery threshold or safety margin is selected.
- No Atlas coordinate or reference zone is used.
- No support is claimed for the firewalled `chi ~ 1.2-1.3` note.
- Exact regrouping here is an algebraic/state-preserving re-expression, not evidence that arbitrary coarse-graining in nature is lossless.

## Next safe P0-D work
1. Run the effective-dimension / observability / conditioning null-floor challenge with latent dynamics held fixed.
2. Run a deliberate out-of-model/refusal challenge without changing existing selector thresholds.
3. Perform the General Protocol v0.7.7 milestone, foundational-dependency robustness, and monitor-coverage audit.
4. Only then ask whether a recovery-related object is mature enough to propose for claim-specific P0-Q qualification.
