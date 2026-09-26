# Meneses duplicate reanalysis source-method audit

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-pmf-recovery-p0q-20260925`  
**Authority:** SymC GOM v0.8.6  
**Classification:** POST-RESULT IMPLEMENTATION AUDIT / NO SCIENTIFIC PROMOTION

## Trigger

The timeout-resume duplicate Meneses execution (workflow run `36218469203`) returned a failed independent-observable threshold in its post-result robustness reanalysis. The duplicate lineage was already reclassified as post-result by `MENESES2026_DUPLICATE_LINEAGE_GOVERNANCE_AUDIT_20260925.md`. A source-method comparison identified an additional implementation difference in the TMRM normalization.

## Source method

At upstream commit `d14d0caaa07299f13d1b1121d1e4630454fd724b`, the maintained source script

`code/TMRM-anaylsis/analyze_tmrm_population_dff.py`

defines the per-track TMRM quantity as

[
\Delta F/F_0 = (F-F_0)/(F_0-1),
]

because the curated input is already an intracellular/background fluorescence ratio near 1.

## Duplicate implementation

The duplicate reanalysis used

[
(F-F_0)/F_0.
]

This changes the numerical TMRM amplitude and produced much smaller shock minima than the source-facing analysis.

## Consequence

The duplicate run's TMRM threshold failure is an implementation/source-method divergence and is not evidence against the canonical Meneses whole-event result.

The canonical primary Meneses lineage remains:

- prospective source reproduction and direct P0-Q result: `MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json`;
- implementation false-negative audit: `MENESES2026_P0Q_IMPLEMENTATION_GATE_AUDIT_20260925.md`;
- source-method reconciliation: `MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json`;
- closure: `MENESES2026_ECOLI_PMF_RECOVERY_CLOSURE_20260925.md`.

No value from the duplicate TMRM lane is used to revise, rescue, or downgrade the canonical P0-Q conclusion.

## Root-cause classification

`TIMEOUT_CONTINUITY_DUPLICATION + SOURCE_NORMALIZATION_MISMATCH`.

Both components are retained as reproducibility evidence. Neither changes the prospective scientific freeze that preceded the canonical Meneses analysis.
