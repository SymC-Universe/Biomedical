# P0-D9 Carrier/Subspace Uncertainty Plan

Date: 2026-09-11
Status: P0-D DERIVATION / CALIBRATION. NOT P0-Q. NOT P1.
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum

## Motivation

P0-D3 established a critical distinction: under modal crowding, individual carrier identity can become unstable while the joint observable carrier subspace remains strongly recoverable. Therefore uncertainty must be attached to the claim object actually being made. A scalar standard error on an arbitrarily labeled individual carrier is not an adequate uncertainty object when only the joint subspace is identifiable.

Published SSI uncertainty work includes uncertainty propagation to mode shapes. Classical invariant-subspace perturbation theory independently supports treating the subspace itself as the stable geometric object when basis vectors inside a clustered eigenspace are poorly conditioned.

## NSD-native object

For the positive-frequency carrier matrix Phi at fixed supported order, define an orthonormal basis Q for `span(Phi)` and the basis-invariant Hermitian projector

`P = Q Q*`.

Individual columns of Phi may rotate, rescale or mix without changing P. The projector is therefore a natural uncertainty object for a crowded carrier cluster.

## Local sampling-uncertainty propagation

Use the same exact NSD Hankel H and P0-D5 covariance root T used by P0-D7.

For each covariance-root direction t_k:

`H_k+ = H + epsilon t_k`

`H_k- = H - epsilon t_k`

Rerun the fixed-order NSD SSI-COV map and compute the positive-frequency carrier projectors `P_k+` and `P_k-`.

The local directional derivative is

`D_k P = (P_k+ - P_k-) / (2 epsilon)`.

A first-order total projector sampling-variance descriptor is

`V_P = sum_k ||D_k P||_F^2`.

This equals the trace of the first-order covariance of the vectorized projector under the covariance-root approximation. It is not a probability, confidence interval or threshold.

Principal angles between the base and perturbed carrier subspaces are retained as interpretable geometric diagnostics.

## Empirical calibration target

Across independent realizations of the same known-truth system, let `P_i` be the estimated projector and `Pbar` their arithmetic mean in ambient matrix coordinates. Define the empirical total sampling variability

`V_emp = sum_i ||P_i - Pbar||_F^2 / (N - 1)`.

Compare the mean record-wise `V_P` against `V_emp`.

Keep bias separate using the known-truth carrier projector `P_truth`, for example `||Pbar - P_truth||_F^2`, and report principal angles from each estimated subspace to truth.

## P0-D9 conditions

Use fixed-order two-mode systems with equal basic architecture but vary modal separation:

- separated: 6.0 and 8.0 Hz;
- moderately crowded: 6.0 and 6.30 Hz;
- strongly crowded: 6.0 and 6.05 Hz.

Both modes use decay 0.7. Use 4 channels, dt 0.02, current SSI-COV, block rows 12, order 4, 24 independent realizations, and record lengths 3600 and 7200 samples. Test batch counts 6 and 12.

No crowding threshold is inferred from these values. They are a P0-D geometric stress surface selected after P0-D3 and are therefore non-confirmatory.

## Questions

1. Is local projector uncertainty finite and numerically stable under Hankel perturbation?
2. Does predicted total projector variance track empirical across-realization projector variability?
3. Does joint-subspace uncertainty remain better behaved than individual carrier identity as frequency separation contracts?
4. Does the duration/batch scale bias already seen in P0-D5/P0-D7 propagate into this geometric uncertainty object?
5. Do principal-angle diagnostics expose cases where a scalar pole SE would underdescribe ambiguity?

## Nonclaims

- No principal-angle threshold is selected.
- No MAC threshold is selected.
- No crowded-versus-individual adjudication boundary is selected.
- No confidence region on the Grassmann manifold is claimed.
- No neural-data validity is claimed.
- No P1 rule is frozen.

## Promotion logic

If the projector uncertainty behaves coherently, it becomes a candidate uncertainty object for crowded/subspace claims and may later receive independent P0-Q qualification. If it fails, NSD must preserve that failure and seek a different representation rather than forcing individual carrier error bars.