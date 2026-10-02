# Bio Chi C1Q-RS Qualification Freeze v1.0

**Status:** APQ-2 QUALIFIED_FROZEN  
**Date:** 27 September 2026  
**Governed by:** SymC General Operations Manual v1.0  
**Qualified plan:** \`NSD_vNext/docs/BIO_CHI_C1Q_RS_QUALIFICATION_PLAN_v0.2.md\`  
**APQ passes:** \`BIO_CHI_C1Q_RS_APQ_PASS_A_v0.1.md\`, \`BIO_CHI_C1Q_RS_APQ_PASS_B_v0.1.md\`  
**Objection ledger:** \`BIO_CHI_C1Q_RS_APQ_LEDGER_v0.1.md\`  
**Plan Delta:** \`BIO_CHI_C1Q_RS_PLAN_DELTA_v0.1.md\`

## Frozen candidate

C1Q-RS is a search-route augmentation of the existing qualification-only C1Q likelihood. It changes no scientific parameter, likelihood term, transform, raw bound, burn-in, parameter count, BIC formula, or C-family semantics.

At each search stage it retains the exact legacy optimized-start set and, when admissible, adds one recurrence/covariance start as an additional forced optimization. No legacy start is displaced.

The current C1Q primary/rescue semantics are preserved by basing rescue activation on the best legacy-only primary result.

## Frozen qualification sequence

1. shared-helper and strict-containment mechanical contracts;
2. compute-matched recurrence-versus-next-legacy attribution on the 48 known failure rows;
3. complete 96-row C-interior Function Map repair;
4. mandatory adversarial/Limit controls for nested A1, anisotropic/rank-1 forcing, colored extra pole, genuine two mode, D\\C, S\\D, and paired-sampling semantics;
5. post-execution deviation/scope audit.

## Frozen mechanical invariants

- historical inline legacy-start ranking equals the shared helper;
- refactored current C1Q behavior remains numerically equivalent on frozen deterministic fixtures;
- C1Q-RS parameter count remains 4;
- recurrence-ready stage contains all legacy optimized starts plus at most one recurrence start;
- recurrence-refusal stage is legacy-equivalent;
- C1Q-RS stage NLL is not worse than the corresponding legacy stage beyond numerical tolerance;
- recurrence success cannot suppress a rescue that the legacy-only primary result would have triggered.

## Claim ceiling

P0-Q repair qualification only. No estimator promotion, real-EEG local chi, biological prevalence, C-family membership, or scientific threshold is licensed.

## APQ limitation

The two adversarial first passes were role-isolated but produced by one cognition. The candidate is therefore subjected to stronger executable Function/Limit controls before any later promotion decision.

## Next action

Implement the shared legacy-start helper, equivalence contracts, and separate C1Q-RS qualification-only module. Scientific execution begins only after those contracts pass.
