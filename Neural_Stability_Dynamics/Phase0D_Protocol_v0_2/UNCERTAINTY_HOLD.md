# Uncertainty and INDETERMINATE Hold

Status: **ESTIMATOR-NATIVE HANKEL -> POLE -> CARRIER-SUBSPACE UNCERTAINTY CHAIN IMPLEMENTED IN P0-D / ABSOLUTE SCALE CALIBRATION REMAINS OPEN / P0-Q CONFIDENCE AND P1 RULE NOT FROZEN**.

Published SSI-COV uncertainty work provides a principled first-order sensitivity/covariance route for uncertainty in poles and modal parameters from output-only data. That literature is method-native but primarily validated in structural/mechanical applications, so direct neural validity is not assumed.

The P0-Q pyOMA2 external-reference run established that a maintained independent implementation of covariance-SSI uncertainty can execute on the NSD known-truth synthetic construction and return finite modal standard errors. Across 12 matched modes, descriptive `estimate ± 1.96 SE` coverage was 10/12 for frequency and 11/12 for damping. Those small-sample coverage values are informative but do not establish a confidence convention.

The compatibility audit found a finite-sample estimator mismatch. NSD currently computes each lag covariance using all available pairs with denominator `n-lag`, whereas the pyOMA2 covariance-Hankel route uses a common aligned interval across Hankel blocks. The resulting point/Hankel differences shrink with record length, but the finite-sample Hankel covariance objects are not identical. Therefore direct reuse of pyOMA2's uncertainty matrix/covariance propagation for the current NSD estimator remains unauthorized.

## P0-D5: native Hankel sampling covariance

P0-D5 implemented an NSD-native contiguous-batch sampling-covariance root for the exact current Hankel estimator. It reproduced the *shape* of empirical Hankel sampling variance strongly, with log-variance correlations about `0.967-0.975`, but showed duration/batch-dependent scale bias.

## P0-D7: native pole-coordinate propagation

P0-D7 propagated that native Hankel covariance root through the exact fixed-order NSD SSI-COV realization into native pole decay and frequency variance estimates. Across 192 requested evaluations, all completed. The symmetric finite-difference propagation was locally very stable: changing epsilon from 0.25 to 0.50 produced median absolute log variance differences of about `0.00041-0.00211`. Predicted/empirical modal variance ratios were approximately `0.73-1.03` at 3600 samples and `1.04-1.79` at 7200 samples, with frequency generally closer than decay.

This localizes the main pole-uncertainty problem to sampling-covariance scale calibration rather than instability of the Hankel-to-pole sensitivity calculation.

## P0-D9: carrier/subspace uncertainty

P0-D9 derived and calibrated a basis-invariant uncertainty object for crowded carrier claims: the observable carrier-subspace projector `P = Q Q*`.

Across separated, moderately crowded and strongly crowded two-mode systems, all requested projector uncertainty propagations completed. Mean predicted projector variance divided by empirical across-realization projector variance ranged approximately `0.821-1.148` across all tested conditions, durations and batch counts. The finite-difference calculation remained locally stable.

Most importantly, at 0.05 Hz mode separation individual carrier MAC medians fell to about `0.89-0.94`, while the joint carrier subspace remained very close to truth, with median maximum principal angles only about `0.0017-0.0028` radians. This supports using different uncertainty objects at different resolution levels rather than forcing individual-mode error bars when only a cluster/subspace is identifiable.

## P0-D10: dependence-aware covariance diagnosis

P0-D10 tested whether serial dependence in the lag-product contributions explains the remaining sampling-variance scale problem. The exact contribution representation was mechanically verified: its sample mean equals the native NSD lag-covariance vector.

The IID/zero-bandwidth variance estimate failed badly, with median predicted/empirical ratios around `0.05-0.08`. Increasing Bartlett-HAC bandwidth consistently raised predicted scale and generally produced high log-variance correlations, reaching roughly `0.965-0.989` at bandwidth 128. Thus serial dependence is a major component of the sampling variance.

However, the tested HAC bandwidths did **not** provide a generally superior calibrated replacement for the incumbent disjoint-batch route. Bandwidth 128 still underpredicted variance in many cells, while disjoint batches were often closer to empirical scale. Therefore no HAC bandwidth or estimator replacement is licensed.

## Resolution-aware uncertainty architecture now supported in P0-D

The development evidence now supports the following architecture, without freezing thresholds:

1. **Resolvable individual mode:** native pole-coordinate uncertainty and carrier-specific evidence may be reported.
2. **Crowded but coherent cluster:** a basis-invariant carrier-subspace/projector uncertainty object may remain meaningful when individual labels are unstable.
3. **Unsupported requested resolution:** unresolved/indeterminate/refusal is preferable to fabricated individual labels or a compensating aggregate score.
4. **Model/order/crowding ambiguity:** remains separate from local sampling uncertainty and must not be hidden inside a scalar SE.

## Remaining uncertainty debts

1. **Absolute sampling-covariance calibration:** compare principled dependence-aware candidate classes without tuning to the completed P0-D outcomes. Current candidates include the incumbent disjoint-batch route, established automatic-bandwidth HAC as a method, and dependence-preserving block-resampling routes.
2. **Full covariance structure:** a diagonal HAC diagnostic is not yet a positive-semidefinite full covariance root suitable for propagation.
3. **Independent P0-Q qualification:** after a candidate uncertainty estimator is versioned/frozen, qualify pole and subspace uncertainty on untouched known-truth evidence.
4. **Resolution/adjudication convention:** later define when an individual claim gives way to a subspace claim or INDETERMINATE state using independent evidence rather than P0-D3/P0-D9 tuning.
5. **Confidence and multiplicity:** only after estimator calibration/qualification propose marginal versus simultaneous confidence conventions and multiplicity control.
6. **P1 INDETERMINATE:** only after the above may an operational P1 convention be proposed for review and freeze.

`INDETERMINATE` must not be defined by an arbitrary fixed gray-zone width. It should arise when supported uncertainty spans incompatible adjudication states, when alternative admissible model orders produce incompatible structural assignments, or when crowding prevents a unique claim at the requested level.

Exact confidence level, simultaneous-versus-marginal coverage, replicate count, multiplicity adjustment, final P1 thresholds and final uncertainty-estimator identity remain unfrozen.

See `P0D7_NATIVE_MODAL_UNCERTAINTY_RESULT_20260911.md`, `P0D9_CARRIER_SUBSPACE_UNCERTAINTY_RESULT_20260911.md`, `P0D10_DEPENDENCE_AWARE_COVARIANCE_RESULT_20260911.md`, `PYOMA2_UNCERTAINTY_REFERENCE_RESULT_20260911.md`, and `FOUR_HOLD_DECISION_PACKET_20260910.md`.