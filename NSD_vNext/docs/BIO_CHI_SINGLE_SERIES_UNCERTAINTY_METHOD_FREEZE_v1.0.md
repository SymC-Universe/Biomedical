# Bio Chi Single-Series Uncertainty Method Comparison Freeze v1.0

**Status:** APQ-2 QUALIFIED_FROZEN  
**Date:** 27 September 2026  
**Plan:** `NSD_vNext/docs/BIO_CHI_SINGLE_SERIES_UNCERTAINTY_METHOD_PLAN_v0.2.md`  
**APQ ledger:** `NSD_vNext/docs/BIO_CHI_SINGLE_SERIES_UNCERTAINTY_APQ_LEDGER_v0.1.md`  
**Physical-likelihood equivalence contract:** PASS, workflow run `36373236094`

Frozen scientific design:

- cells 0, 1, 6, and 2 from the completed repeated-realization uncertainty map;
- realization seed `989969`;
- both 256 Hz and exact-decimated 128 Hz cases;
- unchanged C1Q-RS point estimator;
- local observed-Hessian comparator in physical (A,f_n,chi,g) coordinates;
- 61-point chi profile grid on [0.05,0.98] plus exact fitted/truth chi points;
- frozen nuisance-search recipe;
- 32 fitted-model bootstrap seeds `700001` through `700032`;
- full comparison against the already-completed 12-realization known-truth distributions;
- no LR cutoff, confidence level, admission threshold, production promotion, model-membership claim, biological prevalence, or real-EEG license.

The method comparison is exploratory P0-Q calibration. It may select a method family for later qualification but may not define an empirical admission rule.

Stage A mechanical preflight is cell 0 fine and cell 2 coarse. A profile implementation failure stops dependent execution. Scientific profile/uncertainty shape does not authorize retuning.
