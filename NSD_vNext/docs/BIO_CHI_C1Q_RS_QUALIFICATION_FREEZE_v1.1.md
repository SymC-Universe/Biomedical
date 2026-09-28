# Bio Chi C1Q-RS Qualification Freeze v1.1

**Status:** APQ-2 QUALIFIED_FROZEN  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Qualified Plan:** \`NSD_vNext/docs/BIO_CHI_C1Q_RS_QUALIFICATION_PLAN_v0.2.md\`  
**Plan commit:** \`8b850a138ab307a206b68bfb799bb3ab383e2618\`  
**APQ ledger:** \`NSD_vNext/docs/BIO_CHI_C1Q_RS_APQ_LEDGER_v0.1.md\`  
**Plan Delta:** \`NSD_vNext/docs/BIO_CHI_C1Q_RS_PLAN_DELTA_v0.1.md\`

This v1.1 freeze supersedes the earlier v1.0 candidate-freeze note because the APQ blocker-resolution pass added the shared-helper requirement, preserved legacy rescue semantics, and the compute-matched extra-start attribution control before any scientific C1Q-RS outcome was observed.

## Frozen candidate definition

C1Q-RS preserves the existing C1Q likelihood, four parameters, transforms, raw bounds, burn-in, frequency bounds, parameter count, BIC formula, and C-family semantics.

At each optimization stage:
- the exact legacy optimized-start set is obtained from one shared helper used by current C1Q and C1Q-RS;
- an admissible recurrence/covariance start is added without removing any legacy start;
- best legacy-only and best overall solutions are tracked separately;
- rescue activation follows the legacy-only primary result, so recurrence success cannot suppress a rescue that current C1Q would have performed.

## Frozen pre-science mechanical gate

Before Function/Limit scientific execution:
1. shared-helper selected starts equal an independent reconstruction of the historical inline algorithm;
2. legacy-only RS optimum equals current C1Q optimum under the same stage settings;
3. RS overall NLL cannot be worse than the legacy optimum beyond numerical tolerance;
4. parameter count and BIC formula remain identical;
5. recurrence refusal preserves the legacy route.

Candidate/module code may be implemented before this gate completes, but no scientific C1Q-RS result is interpreted until the gate passes.

## Frozen scientific qualification sequence

1. 48-row recurrence-specific versus next-ranked-legacy compute control;
2. complete 96-row C-interior Function Map repair;
3. nested A1, anisotropic/rank-1, colored-process, genuine two-mode, D\\C, S\\D, and paired-sampling Limit requalification;
4. post-execution deviation/scope audit.

## Claim ceiling

P0-Q repair qualification only. No production promotion, C-family membership, biological prevalence, real-EEG local chi, or empirical scientific threshold.

## Pre-freeze implementation note

The shared-helper refactor and separate C1Q-RS module/test scaffolding were committed while the v0.2 plan was already APQ-qualified but before this freeze record was written. No C1Q-RS scientific outcome had been executed or inspected. These commits are classified as mechanical implementation under the unchanged qualified design, not as outcome-informed plan changes.
