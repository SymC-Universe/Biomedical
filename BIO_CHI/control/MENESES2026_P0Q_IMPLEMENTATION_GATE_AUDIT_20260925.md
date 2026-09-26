# Meneses 2026 P0-Q gate implementation audit and mechanical repair

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-pmf-recovery-p0q-20260925`  
**Authority:** SymC GOM v0.8.6  
**Frozen scientific contract:** `BIO_CHI/config/MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_FREEZE.json`  
**Affected execution:** workflow run `36216125834`, artifact `10898060524`  
**Classification:** IMPLEMENTATION-LEVEL FALSE-NEGATIVE GATE / SCIENTIFIC FREEZE UNCHANGED

## What failed

The first executable implementation returned `SOURCE_REPRODUCTION_FAILURE_PRESERVED` even though every source-reproduction criterion that had actually been frozen was satisfied:

- all immediate motor source-trace counts matched the frozen counts;
- all sustained-adaptation source-trace counts matched the frozen counts;
- every frozen TMRM population-summary value reproduced within tolerance;
- every frozen cell-area population-summary value reproduced within tolerance.

The false negative arose because the executable added a new condition that was not present in the freeze: it required every TMRM and cell-area condition to contain exactly 40 tracks with finite normalized `dff` values and allowed that diagnostic to veto the whole-event result.

## Root cause of the TMRM count discrepancy

The source publication reports 40 source cells per TMRM condition. The executable instead counted only track IDs contributing at least one finite post-normalization value. Those are different quantities. The first run returned finite-normalized TMRM track counts of 39, 40, 39, 39, and 38 for control, 200, 300, 400, and 500 mM, respectively, while the frozen population summaries reproduced essentially exactly. Cell-area finite-normalized counts were 40 in every condition.

The finite-normalized count is retained as a diagnostic but was never a frozen admission rule. It cannot be introduced after result inspection as a new scientific veto.

## Immediate-motor fit audit

The first implementation also imposed a positivity sanity check on fitted time constants after the source-style unconstrained curve fit. That positivity requirement was not part of the frozen source-native fit specification. It caused one 200 mM trace (`cell8`) to be labeled a fit failure after the optimizer returned a nonpositive time constant.

The repair restores source semantics: a source-style fit is considered computationally returned if `curve_fit` returns finite parameters. Parameter sign is retained as a separate diagnostic and is not used to delete the trace. No trace is removed post-result.

## Repair

Version 0.1a changes implementation mechanics only:

1. whole-event source reproduction is adjudicated only by the criteria actually frozen before result inspection: bead trace-count reproduction plus TMRM/cell-area population-summary reproduction;
2. raw source-track count and finite-normalized-track count are reported separately for orthogonal assays;
3. the source-style immediate fit accepts finite unconstrained parameters exactly as returned and records positive/nonpositive tau as a diagnostic rather than a deletion rule;
4. the frozen rate-depth rule, nine-coordinate joint representation, scalar gate, thresholds, source files, concentrations, and claim ceiling remain unchanged.

## Epistemic consequence

Run `36216125834` remains preserved as evidence of an implementation error. It is not deleted or rewritten. The repaired run is a mechanical correction to enforce the prospectively frozen contract and must be cited together with this audit. Any scientific values changed by reinstating the previously rejected source-style motor fit will be reported from the repaired run and not backfilled into the earlier artifact.
