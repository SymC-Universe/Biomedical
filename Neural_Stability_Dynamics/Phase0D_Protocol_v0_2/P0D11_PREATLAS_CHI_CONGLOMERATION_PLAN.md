# P0-D11 Pre-Atlas Chi Reconstruction and Conglomeration Plan

Date: 2026-09-11
Status: **P0-D MATHEMATICAL / SYNTHETIC MAPPING ONLY. NOT ATLAS CALIBRATION. NOT P0-Q. NOT P1.**
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum

## Purpose

Test whether the current NSD structural engine can reconstruct a known second-order chi coordinate **before** the independent Neurostability Atlas supplies any empirical neural reference map, and test one transparent candidate for conglomerating multiple admitted second-order components into a system-level coordinate.

The Atlas is not used to choose formulas, weights, thresholds, target values or expected ranges in this experiment.

## Single-component construction

Start from the second-order equation

`q'' + 2 chi omega_n q' + omega_n^2 q = 0`.

Using the dimensionless state `x = [q, u]^T` with `u = q'/omega_n` gives

`dx/dt = A_chi x`

with

`A_chi = omega_n * [[0, 1], [-1, -2 chi]]`.

This scaling keeps the two synthetic state coordinates dimensionally compatible for the isotropic process-noise stress used here. It does not claim literal neural displacement or velocity variables.

The characteristic polynomial is

`s^2 + 2 chi omega_n s + omega_n^2 = 0`.

Therefore chi is known exactly by construction across all three branches:

- `chi < 1`: stable complex-conjugate poles;
- `chi = 1`: repeated critical pole / defective boundary case;
- `chi > 1`: two stable real poles.

For **one explicitly licensed second-order pole pair**, the pair invariants give

`gamma = -(lambda_1 + lambda_2)`

`omega_n^2 = lambda_1 lambda_2`

and hence

`chi_pair = gamma / (2 omega_n)`

or

`chi_pair = -(lambda_1 + lambda_2) / (2 sqrt(lambda_1 lambda_2))`.

This formula works on both the complex and real branches when the two poles are legitimately members of the same second-order factor. It does not authorize arbitrary pairing of unrelated real poles in neural data.

## Candidate conglomerate coordinate

For `m` admitted second-order components with component chi values `chi_j`, natural frequencies `omega_n,j` and nonnegative weights `w_j`, define the developmental candidate

`chi_C = sqrt(sum_j w_j (chi_j omega_n,j)^2) / sqrt(sum_j w_j omega_n,j^2)`.

Equivalently, if `gamma_j = 2 chi_j omega_n,j`,

`chi_C = gamma_RMS / (2 omega_n,RMS)`

under the same weights.

This choice is being tested because it has useful algebraic properties without requiring Atlas-derived tuning:

1. one component reduces exactly to its ordinary chi;
2. if all components have the same chi, the conglomerate equals that chi regardless of their natural frequencies;
3. it is permutation invariant;
4. it can represent values below, at or above 1;
5. it is a ratio of conglomerated damping scale to conglomerated natural-dynamic scale rather than an arithmetic average of labels.

Initial P0-D11 uses **equal component weights** only. No neural participation weighting is selected here.

## Why conglomeration is not the same as epistemic quality

The candidate chi value is constructed only from admitted dynamical quantities. The following remain **gates/companions**, not numerical ingredients mixed into chi:

- model adequacy;
- observable-rank support;
- individual versus subspace identifiability;
- assignment ambiguity;
- estimator agreement;
- uncertainty calibration;
- persistence across windows/conditions.

These determine whether a coordinate may be reported, and at what resolution. They do not make a poorly supported system numerically more or less damped.

## P0-D11 surfaces

### Surface A: one second-order component across the boundary

At fixed natural frequency, generate known-truth systems at

`chi = [0.20, 0.50, 0.80, 0.95, 0.99, 1.00, 1.01, 1.05, 1.20, 1.50, 2.00]`.

Fit the current SSI-COV realization at fixed known development order 2 and compare reconstructed pair-invariant chi against truth. The exact critical point is retained rather than skipped.

### Surface B: two-component conglomeration

Generate block-diagonal two-component systems spanning:

- both comfortably underdamped;
- both near a common subcritical value;
- one underdamped plus one overdamped;
- both overdamped;
- strong heterogeneous cross-boundary mixtures;
- a near-boundary mixed pair.

Fit at fixed known development order 4, truth-match estimated poles only for diagnostic scoring, reconstruct each component chi, and then reconstruct `chi_C`.

### Surface C: information-loss demonstration

Show analytically that different modal compositions can share the same `chi_C`. This is intentional evidence that the scalar is a coordinate, not a replacement for modal structure. The component chi set, frequencies and dispersion must remain beside the conglomerate coordinate.

## Success and failure are both informative

P0-D11 does **not** define a pass threshold.

Useful outcomes include:

- smooth reconstruction through the underdamped branch;
- instability or uncertainty inflation near `chi = 1`;
- inability to recover paired real poles above the boundary;
- accurate system-level conglomeration despite component noise;
- failure of one scalar to distinguish heterogeneous architectures that share the same aggregate.

Any of these constrains the eventual chi admission architecture.

## Nonclaims

- No neural population chi is estimated.
- No Atlas reference range is used or inferred.
- No healthy, pathological, optimal or critical neural zone is defined.
- Equal component weighting is not a proposed final biological weighting rule.
- Truth pairing in the synthetic multi-component surface is diagnostic only and is not available to a future blind neural engine.
- This experiment does not authorize `chi_system` in System Model v1.0.
- No P1 threshold, target or adjudication rule is frozen.

## Next decision after execution

If pair-level chi is reconstructable across a meaningful portion of the known-truth surface, the next P0-D question is not "what neural chi should be." It is **what data-derived, Atlas-independent rule licenses component grouping and system weighting without phenotype or outcome leakage**.
