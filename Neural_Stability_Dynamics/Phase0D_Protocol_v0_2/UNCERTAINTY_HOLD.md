# Uncertainty and INDETERMINATE Hold

Status: **NSD-NATIVE HANKEL COVARIANCE ROOT + POLE PROPAGATION IMPLEMENTED / SCALE CALIBRATION REMAINS OPEN / P0-Q CONFIDENCE AND P1 RULE NOT FROZEN**.

Published SSI-COV uncertainty work provides a principled first-order sensitivity/covariance route for uncertainty in poles and modal parameters from output-only data. That literature is method-native but primarily validated in structural/mechanical applications, so direct neural validity is not assumed.

The P0-Q pyOMA2 external-reference run established that a maintained independent implementation of covariance-SSI uncertainty can execute on the NSD known-truth synthetic construction and return finite modal standard errors. Across 12 matched modes, descriptive `estimate ± 1.96 SE` coverage was 10/12 for frequency and 11/12 for damping. Those small-sample coverage values are informative but do not establish a confidence convention.

The compatibility audit found a finite-sample estimator mismatch. NSD currently computes each lag covariance using all available pairs with denominator `n-lag`, whereas the pyOMA2 covariance-Hankel route uses a common aligned interval across Hankel blocks. The resulting point/Hankel differences shrink with record length, but the finite-sample Hankel covariance objects are not identical. Therefore direct reuse of pyOMA2's uncertainty matrix/covariance propagation for the current NSD estimator remains unauthorized.

P0-D5 then implemented an NSD-native contiguous-batch sampling-covariance root for the exact current Hankel estimator. It reproduced the *shape* of empirical Hankel sampling variance strongly, with log-variance correlations about `0.967-0.975`, but showed duration/batch-dependent scale bias.

P0-D7 has now propagated that native Hankel covariance root through the exact fixed-order NSD SSI-COV realization into native pole decay and frequency variance estimates. Across 192 requested evaluations, all completed. The symmetric finite-difference propagation was locally very stable: changing epsilon from 0.25 to 0.50 produced median absolute log variance differences of about `0.00041-0.00211`. Predicted/empirical modal variance ratios were approximately `0.73-1.03` at 3600 samples and `1.04-1.79` at 7200 samples, with frequency generally closer than decay. The white-sensor perturbation preserved the same pattern.

Therefore the uncertainty problem is now narrower:

1. **Sampling-covariance scale calibration:** diagnose and reduce the duration/batch-dependent scale bias while preserving the exact NSD finite-sample estimator.
2. **Independent qualification:** once a candidate sampling-covariance route is frozen, qualify its pole-level uncertainty on untouched known-truth evidence rather than the P0-D7 records used to develop it.
3. **Carrier/subspace uncertainty:** separately derive uncertainty or identifiability objects for mode shapes, invariant subspaces and crowded assignments where scalar pole SE is insufficient.
4. **Order/crowding/model ambiguity:** keep model-order, crowding and assignment ambiguity separate from local sampling SE.
5. **Confidence and multiplicity:** only after calibration/qualification propose marginal versus simultaneous confidence conventions and multiplicity control.
6. **P1 INDETERMINATE:** only after the above may an operational P1 convention be proposed for review and freeze.

`INDETERMINATE` must not be defined by an arbitrary fixed gray-zone width. It should arise when supported uncertainty spans incompatible adjudication states, when alternative admissible model orders produce incompatible structural assignments, or when crowding prevents a unique claim at the requested level.

Exact confidence level, simultaneous-versus-marginal coverage, replicate count, multiplicity adjustment and final P1 thresholds remain unfrozen.

See `P0D7_NATIVE_MODAL_UNCERTAINTY_RESULT_20260911.md`, `P0D7_NATIVE_MODAL_UNCERTAINTY_PLAN.md`, `PYOMA2_UNCERTAINTY_REFERENCE_RESULT_20260911.md`, `PYOMA2_UNCERTAINTY_REFERENCE_PLAN.md`, `LITERATURE_GATE_CANDIDATES_20260910.md`, and `FOUR_HOLD_DECISION_PACKET_20260910.md`.