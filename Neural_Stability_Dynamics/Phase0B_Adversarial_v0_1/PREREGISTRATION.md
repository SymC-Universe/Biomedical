# Phase 0B Adversarial Synthetic Identification Preregistration

Frozen before Phase 0B execution.

## Epistemic role

Phase 0B is a development/calibration layer. It cannot by itself admit the estimator to EEG. Its purpose is to expose failure boundaries and supply evidence for freezing a separate Phase 0C holdout test.

Sequence:

`Phase 0A in-model recovery -> Phase 0B adversarial development -> freeze selector/refusal rules and thresholds -> Phase 0C untouched synthetic holdout -> label-blind EEG adequacy`

## Representation firewall

Primary objects are poles/eigenvalues, observable mode shapes, invariant/modal subspaces when individual eigenvectors are not stable, cross-order persistence, split-record consistency, and observability strength. Damping ratio is not the optimization target and no whole-system scalar is constructed here.

## Paired perturbation rule

For each system family and replicate, the same underlying generator, observation map, process realization, and standardized measurement-noise realization are reused across duration and measurement-noise profiles wherever the system definition permits it.

- duration uses prefixes of the same realization;
- white-noise amplitude uses the same white-noise realization scaled by the frozen fraction;
- the colored-noise profile uses a separately generated but fixed AR(1) realization for that base system.

No new generator or observation map is drawn merely because a challenge condition changes.

## Model order

Truth order is not supplied to the estimator. The estimator is run at every frozen candidate order: `2, 4, 6, 8`.

No order is selected during Phase 0B. We retain the full stabilization/order sweep. Phase 0B results may be used to design an automatic selector, but that selector must be frozen before Phase 0C.

## In-model families

1. `separated_normal`: two clearly separated oscillatory modes.
2. `crowded_normal`: two closer oscillatory modes.
3. `near_degenerate`: two very close oscillatory modes, specifically included to test whether individual eigenvectors become unstable while the joint subspace remains recoverable.
4. `nonnormal_cond30`: two separated oscillatory modes under a non-orthogonal similarity transform with target condition number 30.
5. `weak_observable`: the second modal block is attenuated in the observation map.
6. `mixed_complex_real`: one complex-conjugate oscillatory pair plus two distinct stable real poles.

## Adversarial off-model families

7. `null_1f`: correlated multichannel 1/f-like noise with no finite-dimensional modal truth supplied.
8. `nonstationary_switch`: a piecewise stationary system whose second half changes its modal frequencies/decays.

The off-model cases are not scored against fabricated modal truth. Their purpose is to quantify how much apparently stable structure the candidate estimator produces when its stationary finite-dimensional assumptions are violated.

## Frozen challenge profiles

Durations: 60 s, 120 s, 300 s.

Measurement profiles:
- low white: 1% of each channel's clean standard deviation;
- high white: 15%;
- high colored: 15%, AR(1) rho = 0.8.

Sampling interval: 0.01 s (100 Hz).

Replicates: 4 per system family.

## Segmentation

Every condition is fit on the full record, first half, and second half. This is diagnostic evidence for stationarity and repeatability. Phase 0B does not yet impose an acceptance threshold on split consistency.

## Metrics retained

For truth-bearing families: normalized pole error, absolute frequency error, absolute decay-rate error, MAC, matched-truth fraction, and observable-subspace similarity where applicable.

For all families: singular-value spectrum information, estimated pole set at each model order, stable/unstable pole sign, order, and segment.

## No favorable deletion

Every system, replicate, duration, noise profile, order, segment, failed fit, unmatched truth mode, unstable estimate, and off-model output remains machine-readable.

## No Phase 0B pass threshold

This is deliberate. Phase 0A proved only that the candidate works in its easy model class. Phase 0B is the adversarial development set. Numerical admission thresholds chosen after seeing Phase 0B would be overfit if tested on Phase 0B itself.

Therefore Phase 0B can kill an obviously unusable estimator; otherwise it informs a frozen selector/refusal design, and final synthetic admission belongs to untouched Phase 0C.

## Clinical firewall

TDBRAIN EEG, TDBRAIN labels, diagnostic tables, replication labels, and treatment-response outcomes remain outside this package.
