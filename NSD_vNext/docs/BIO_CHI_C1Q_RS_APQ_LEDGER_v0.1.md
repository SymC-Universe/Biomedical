# Bio Chi C1Q-RS APQ Objection Ledger v0.1

**APQ level:** APQ-2 SUBSTANTIAL  
**Draft plan:** \`BIO_CHI_C1Q_RS_QUALIFICATION_PLAN_v0.1.md\`

| ID | Source | Severity | Failure mechanism | Disposition | Plan consequence |
| --- | --- | --- | --- | --- | --- |
| A1 | Pass A | MATERIAL | Better optimization could be mistaken for C-family admission | ACCEPTED_MODIFIED | Function and Limit conclusions remain separate; semantic refusals are immutable controls |
| A2 | Pass A | MATERIAL | Repair cells are outcome-informed | DEFERRED_CLAIM_LIMITED | Entire C1Q-RS program remains P0-Q repair qualification; no confirmation or promotion |
| B1 | Pass B | BLOCKER | Duplicated legacy-start selection could drift and invalidate strict containment | ACCEPTED_MODIFIED | Refactor legacy start selection into one shared helper used by old C1Q and C1Q-RS; add exact start-set contract tests |
| B2 | Pass B | MATERIAL | Primary/rescue behavior could be changed by recurrence success | ACCEPTED_MODIFIED | C1Q-RS records the best **legacy-only** primary result and triggers the 24-start rescue whenever that legacy result would have triggered current C1Q, independent of whether the recurrence start itself converged |
| B3 | Pass B | MATERIAL | Improvement might come from one extra optimization rather than recurrence information | ACCEPTED_TEST_ADDED | On all 48 root-cause rows, optimize the next-ranked legacy start as a one-extra-start compute control and compare its rescue behavior with recurrence augmentation |

## Evidence-governed resolution

B1 is resolved only if the shared helper mechanically reproduces the pre-refactor inline start ranking. The refactor may change code organization but not numerical start identity, optimizer settings, likelihood, or selected fit. Contract tests compare the helper with an inline reconstruction of the historical algorithm.

B2 is resolved by separating the overall C1Q-RS best result from the legacy-only best result. The wrapper's primary/rescue decision follows the legacy-only result, preserving the current C1Q escalation semantics while allowing the recurrence start to compete within each stage.

B3 is resolved by an explicit compute-matched control on the already-viewed 48-row failure set. For a stage with \(N\) legacy optimized starts, the control locally optimizes the next-ranked legacy candidate \(N+1\) without recurrence information. This is a root-cause attribution control, not a candidate estimator.

## Shared-premise challenge

Both APQ passes assume the existing C1Q likelihood is worth optimizing. That premise is limited to the current qualification question. C1Q-RS may only show that the likelihood can be searched better. It cannot independently validate the likelihood family, continuous-lineage membership, biological prevalence, or the broader Bio Chi interpretation.

A second shared premise is that more complete likelihood maximization is always desirable. On out-of-family truths, better optimization may increase the apparent attractiveness of the wrong C-family approximation. The Limit Map therefore remains mandatory and can prevent promotion even if the Function Map improves dramatically.

## Closure

No unresolved BLOCKER remains once the shared-helper contract is implemented and passes mechanically. No unresolved MATERIAL objection remains in the revised plan. Independent cognition was not available; the two first passes were role-isolated from the same cognition and this limitation remains part of the qualification record.
