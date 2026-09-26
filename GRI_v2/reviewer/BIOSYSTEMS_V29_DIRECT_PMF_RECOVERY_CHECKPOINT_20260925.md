# BioSystems V29 Direct PMF Recovery Checkpoint

**Date:** 25 September 2026  
**Authority:** SymC GOM v0.8.6  
**Status:** CLOSED FOR THIS ITERATION  
**Reviewer branch:** `biosystems-v29-direct-pmf-recovery-20260925`  
**Immediate parent:** `biosystems-v28-biochi-continuation-20260925` @ `58eb8b4777fae0fb79ab50d38b738dfee556b2a3`

## Status

The original C1/P1 oncology evidence spine remains unchanged. V29 adds a separately frozen direct experimental Bio Chi qualification from Meneses et al. (2026) E. coli hyperosmotic-shock data, plus the complete implementation-failure and source-method-reconciliation lineage.

Primary scientific branch: `bio-chi-ecoli-pmf-recovery-p0q-20260925`.

## Direct experimental result

The repaired frozen run reproduced the source bead-trace inventories and all frozen TMRM/cell-area population summaries. The whole event is therefore admitted at P0-Q as:

`DIRECT_EXPERIMENTAL_COLLAPSE_RECOVERY_RELATION_REPRODUCED_P0Q`.

The nine-coordinate recovery representation failed the frozen one-dimensional adequacy rule:

- PC1 variance fraction: `0.6620977810898341`
- maximum absolute standardized one-dimensional reconstruction residual: `1.1144697154328063`
- `Chi_bio`: `MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_P0Q`

Scalar `chi_bio` remains `NOT_OPENED_NOT_LICENSED` because the source-fitted time constants are empirical response summaries, not independently licensed mechanistic modal carriers.

## Failed stronger hypothesis

The frozen rate-depth simplification failed. Collapse amplitude increased monotonically with shock strength and sustained plateau decreased monotonically, but the three rate coordinates did not jointly satisfy the frozen dose-robustness rule.

Disposition: `FROZEN_RATE_DEPTH_RULE_NOT_MET_P0Q`.

This negative result is retained as part of the scientific outcome.

## Implementation failure preserved

Workflow run `36216125834` returned a false-negative whole-event result because implementation code introduced an unfrozen finite-normalized-track-count veto. The error was audited before rerun in:

`BIO_CHI/control/MENESES2026_P0Q_IMPLEMENTATION_GATE_AUDIT_20260925.md`.

The erroneous artifact remains preserved. The repaired run is `36216252676`, artifact `10897836350`, digest `sha256:33e2c253ffb19abe1d3679116df768e08012cc6181cd910a38c3976b4bf77c3f`.

## Source-method reconciliation

A post-result reconciliation tested the authors' manuscript-facing sucrose fitting method rather than the older/general four-parameter lane.

The representation result remained multicoordinate:

- PC1 variance fraction: `0.7719879506509367`
- maximum standardized one-dimensional residual: `1.2036796471330158`
- `Chi_bio`: `MULTICOORDINATE_RECOVERY_ARCHITECTURE_REQUIRED_POSTRESULT`
- comparison disposition: `SOURCE_METHOD_ROBUST_AT_P0Q`

The rate-depth rule also failed in the reconciliation, and scalar `chi_bio` remained unlicensed.

Reconciliation run: `36216368561`; artifact: `10897991063`; digest: `sha256:0534f1173b51a4d4fc4459bdb28a800a7759968f96119434d5f7ea35c1308dc9`.

## Publication metadata

Meneses et al., *Osmotic stress triggers fast and reversible PMF collapse in Escherichia coli*, *Biophysical Journal* 125(11):2618-2631 (2026), DOI `10.1016/j.bpj.2026.04.014`.

## Private authoring artifacts

The V29 manuscript and Supplementary Information remain private authoring files. They incorporate the direct experimental result, the failed rate-depth hypothesis, the scalar refusal, the source-method robustness result, and the bounded claim ceiling without altering the original oncology evidence tier.

## What happens next and why

The next experiment should test transport of the **multicoordinate recovery architecture**, either across a different perturbation path in a directly measured system or across an independent biological system with comparable recovery observables. Repeating scalar-first compression has low information value after two distinct systems have now independently refused one-dimensional recovery representation under frozen rules.

## What the user needs to do

Nothing is required at this checkpoint.
