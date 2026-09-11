# Uncertainty and INDETERMINATE Hold

Status: **EXTERNAL SSI ROUTE EXECUTED / DIRECT TRANSFER REFUSED / NSD-NATIVE DERIVATION + CALIBRATION REQUIRED / P1 RULE NOT FROZEN**.

Published SSI-COV uncertainty work provides a principled first-order sensitivity/covariance route for uncertainty in poles and modal parameters from output-only data. That literature is method-native but primarily validated in structural/mechanical applications, so direct neural validity is not assumed.

The P0-Q pyOMA2 external-reference run has now established that a maintained independent implementation of covariance-SSI uncertainty can execute on the NSD known-truth synthetic construction and return finite modal standard errors. Across 12 matched modes, descriptive `estimate ± 1.96 SE` coverage was 10/12 for frequency and 11/12 for damping. Those small-sample coverage values are informative but do not establish a confidence convention.

The required compatibility audit also found a finite-sample estimator mismatch. NSD currently computes each lag covariance using all available pairs with denominator `n-lag`, whereas the pyOMA2 covariance-Hankel route uses a common aligned interval across Hankel blocks. The resulting point/Hankel differences shrink with record length, but the finite-sample Hankel covariance objects are not identical.

Therefore **direct reuse of pyOMA2's uncertainty matrix/covariance propagation for the current NSD estimator is not authorized**. Close point estimates are insufficient because the uncertainty calculation is tied to the estimator whose sampling covariance is being propagated.

The open problem is now specific:

1. derive or implement uncertainty for the actual NSD finite-sample covariance/Hankel estimator, or change that estimator only through a separately justified and versioned scientific decision;
2. propagate that uncertainty to poles/frequency/decay and carrier/subspace quantities where mathematically justified;
3. calibrate the implementation on new known-truth P0-Q evidence and against an independent executable/literature reference;
4. separately carry model-order, crowding and assignment ambiguity where a scalar standard error is not the right object;
5. only after calibration propose a P1 `INDETERMINATE` adjudication convention for review and freeze.

`INDETERMINATE` must not be defined by an arbitrary fixed gray-zone width. It should arise when supported uncertainty spans incompatible adjudication states, when alternative admissible model orders produce incompatible structural assignments, or when crowding prevents a unique claim at the requested level.

Exact confidence level, simultaneous-versus-marginal coverage, replicate count, multiplicity adjustment and final P1 thresholds remain unfrozen.

See `PYOMA2_UNCERTAINTY_REFERENCE_RESULT_20260911.md`, `PYOMA2_UNCERTAINTY_REFERENCE_PLAN.md`, `LITERATURE_GATE_CANDIDATES_20260910.md`, and `FOUR_HOLD_DECISION_PACKET_20260910.md`.
