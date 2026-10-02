# Bio Chi C1Q-RS Search-Route Qualification Plan v0.2

**Status:** APQ-2 QUALIFIED CANDIDATE  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0, Section 15.4  
**Lifecycle stage:** Stage 3, P0-Q estimator/search qualification  
**APQ ledger:** \`BIO_CHI_C1Q_RS_APQ_LEDGER_v0.1.md\`  
**Plan Delta:** \`BIO_CHI_C1Q_RS_PLAN_DELTA_v0.1.md\`

## Scientific target and claim ceiling

C1Q-RS tests whether the existing four-parameter C1Q likelihood can be optimized more reliably by augmenting, rather than replacing, its search route. It is qualification-only. It cannot establish C-family membership, biological prevalence, a real-data threshold, or real-EEG local \(\chi\).

## Frozen candidate definition

The C1Q likelihood, transforms, bounds, burn-in, four parameters, parameter count, BIC formula, and physical interpretation remain unchanged.

A shared helper selects the exact legacy starts current C1Q optimizes. Current C1Q is mechanically refactored to call that helper without changing its behavior.

At each search stage with legacy budget \(N\):

1. obtain the exact same \(N\) legacy starts current C1Q would optimize;
2. construct the frozen recurrence/covariance seed from the data;
3. if admissible, add it as one additional forced start without removing any legacy start;
4. optimize all legacy starts and the optional recurrence start with identical L-BFGS-B settings;
5. retain separate metadata for the best legacy-only solution and the overall best solution.

The wrapper preserves the existing primary/rescue semantics: whether the 24-start rescue stage runs is determined by whether the **legacy-only primary best** would have triggered rescue in current C1Q. Recurrence-start convergence cannot suppress a rescue that current C1Q would have performed.

If the recurrence seed refuses, C1Q-RS follows the exact legacy search route.

## Mechanical invariants

Before scientific execution:

- shared helper output equals an inline reconstruction of the historical legacy start-ranking algorithm;
- refactored current C1Q matches pre-refactor behavior on frozen deterministic fixtures;
- C1Q-RS uses the same \(k=4\), BIC, likelihood, burn, bounds, and transforms;
- recurrence-ready search contains every legacy optimized start plus at most one recurrence start;
- recurrence-refusal route is legacy-equivalent;
- on the same realized input and same stage, RS best NLL cannot exceed legacy best NLL beyond the mechanical tolerance.

Any invariant failure is a code defect and blocks interpretation.

## Gate 1. Recurrence-specific versus extra-compute attribution

On the 48 already-viewed root-cause rows, compare:

- immutable archived C1Q selected NLL;
- recurrence-augmented local/search result;
- one compute-matched additional legacy start, defined prospectively as the next-ranked finite legacy candidate immediately after the frozen stage budget.

Record how often each additional start reaches a better basin and the continuous NLL improvement. This is attribution evidence only.

## Gate 2. Full C-interior Function Map repair

Regenerate the exact 16 cells x 3 seeds x two rates from run \`36368579380\`. Fit C1Q-RS with the preserved primary/rescue logic and compare against the immutable archived C1Q rows.

Report all 96 rows:
- archived and RS NLL;
- strict-invariant result;
- truth \(\chi,g,f_n\) errors;
- raw-bound proximity;
- recurrence-seed readiness/projection;
- winning-start origin;
- same-path practical rate drift;
- residual failure rows.

No error threshold defines pass/fail. The full distributions and cell structure are interpreted.

## Gate 3. Mandatory Limit Map requalification

Use the existing frozen generators/seeds and add C1Q-RS to:

1. isotropic one-mode \(g=0\);
2. anisotropic 4:1 and rank-1 white forcing;
3. colored-process \(\phi=0.7\) extra-pole truth;
4. genuine separated two-mode truth;
5. signed D\C controls;
6. signed S\D controls;
7. paired fine/coarse C, D\C, and S\D sampling semantics.

Where A0/A1/A2 form part of the original control, they remain the native comparison and C1Q-RS is added without changing their code.

Truth-family labels are immutable. A better RS likelihood on colored, D\C, or S\D truth cannot turn those cases into C.

## Gate 4. Post-execution audit

Classify:
- repaired interior search failures;
- residual search failures;
- recurrence-seed refusals;
- recurrence-specific rescue versus generic extra-compute rescue;
- nested-model regressions;
- multimode regressions;
- unchanged or strengthened semantic Limit failures;
- runtime/compute cost;
- plan deviations.

## Outcome architecture

**Repair supported:** interior boundary collapse is substantially reduced, strict mechanical invariants pass, and no new nested/multimode regression appears.

**Partial repair:** improvement is real but important interior failures remain.

**Recurrence-specific mechanism supported:** recurrence augmentation reaches better basins materially more often than the compute-matched next legacy start.

**Extra-compute explanation:** recurrence and the extra legacy start rescue comparable rows, weakening the claim that recurrence structure is specifically informative.

**Regression:** A1 nested truth or A2 genuine multimode truth is newly mis-selected because of C1Q-RS.

**Semantic limits persist:** C1Q-RS fits colored or out-of-C truths well. This preserves, rather than repairs, the need for independent admission/refusal gates.

**Repair falsified:** strict invariants fail or interior failures persist without material improvement.

No result alone authorizes production promotion.

## Provenance and evidence status

All Function/Limit datasets in this plan are synthetic known truths and already-viewed P0 evidence. This is outcome-informed repair qualification. Later production promotion would require a separately frozen qualification package that is not tuned on these exact outcomes.

## APQ closure

Two role-isolated first passes were completed. B1 BLOCKER is resolved by shared-helper factoring plus historical-equivalence contract tests. B2 and B3 are resolved by preserved rescue semantics and a compute-matched extra-start control. A1/A2 are resolved by claim limitation and mandatory Limit Map requalification.

No unresolved BLOCKER or MATERIAL objection remains. The plan is eligible for freeze before implementation.
