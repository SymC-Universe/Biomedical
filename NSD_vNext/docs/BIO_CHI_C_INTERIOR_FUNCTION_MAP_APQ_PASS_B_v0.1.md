# Bio Chi Function Map APQ First Pass B v0.1

**APQ level:** APQ-2 SUBSTANTIAL  
**Review lens:** method, falsification, uncertainty, computation, reproducibility, provenance  
**Plan reviewed:** `BIO_CHI_C_INTERIOR_FUNCTION_MAP_PLAN_PACKET_v0.1.md` at commit `673bbd477d87819165a0740426ee5619f0b30575`  
**Isolation statement:** this pass was produced from the frozen Plan Packet without access to another APQ review conclusion. It is role-isolated but not independently cognized.

## 1. Strongest justified feature

The plan freezes coordinates, seeds, sampling, sentinel cells, optimization rescue, output fields, and claim ceiling before execution. It also treats fine/coarse observations as paired metamorphic views of one realization rather than independent evidence.

## 2. Strongest scientific assumption

The plan assumes that 16 space-filling parameter cells with three stochastic realizations each are sufficient for a useful P0-D Function Map. That is defensible for exploratory coverage but not for estimating a stable failure probability, prevalence, or tight uncertainty surface.

## 3. Most likely failure mode

A small number of stochastic realizations can make isolated cells appear systematically difficult or easy. Because C1Q is optimized with multiple starts, numerical failures can also be mistaken for statistical nonidentifiability if optimizer diagnostics are not retained at row level.

## 4. Most dangerous hidden dependency

Fine/coarse comparison changes sample count while preserving duration. Apparent cross-rate drift combines sampling-frequency effects with changed information density and estimator variance. It is useful as a practical metamorphic test, but not a pure estimate of discretization invariance.

## 5. Plausible competing explanation

Any parameter-dependent error surface may reflect the fitter's box constraints, spectral start generation, or finite likelihood burn rather than the mathematical C family itself.

## 6. Circularity / leakage / provenance concern

The plan is P0-D and outcome exposure is acceptable, but rescue logic must remain mechanical. Rescue settings must not change cell inclusion, parameter ranges, estimator family, or reporting based on whether a scientific result looks favorable.

## 7. Missing control / comparator

The plan should record distance to the optimizer's effective parameter bounds and flag fits that land near those bounds. It should also preserve the complete attempted/converged-start diagnostics and distinguish optimizer failure from valid but inaccurate recovery.

## 8. Cheaper / cleaner discriminating test

The frozen four-cell preflight is appropriate. It should be required to pass only mechanical invariants: exact truth construction, PSD covariances, output schema, reproducible design identity, finite execution, and successful artifact serialization. Scientific error magnitude observed in the pilot must not be used to retune the envelope.

## 9. Refusal condition

If the pilot reveals a shared implementation defect, invalid covariance, alias-safety violation, or non-reproducible coordinate generation, stop and repair before the full map. If only scientific recovery is poor, preserve the result and continue the frozen P0-D map unless computation becomes invalid.

## 10. Objection classification

- **B1 MATERIAL:** parameter-bound proximity is not currently separated from scientific recovery failure.
- **B2 MATERIAL:** the same-path fine/coarse drift cannot be interpreted as a pure sampling-invariance statistic.
- **B3 MATERIAL:** three seeds support descriptive dispersion only; the plan must forbid prevalence or stable failure-rate language.
- **B4 MINOR:** stochastic repeatability class must be declared under GOM Section 33.1.2.
