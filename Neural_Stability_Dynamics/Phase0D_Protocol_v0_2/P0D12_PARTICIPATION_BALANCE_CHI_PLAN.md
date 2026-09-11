# P0-D12 Participation-Balance Chi Diagnosis Plan

Date: 2026-09-11
Status: **P0-D MECHANISM DIAGNOSIS. NOT ATLAS CALIBRATION. NOT P0-Q. NOT P1.**
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum

## Question

P0-D11 showed that a single known second-order chi can be reconstructed through much of the underdamped branch, while forced two-component chi reconstruction was poor. Is that multi-component failure primarily caused by unequal participation of the latent components in the observed covariance record?

This experiment changes **excitation allocation only** while holding the generator, observation map, sample rate, record length, SSI-COV estimator and fixed development order constant.

## Why this matters

For a stable discrete linear system

`x_(k+1) = F x_k + eta_k`,

stationary covariance satisfies

`P = F P F^T + Q`.

If two independent dynamical blocks receive equal state-noise amplitude, they need not contribute equal stationary variance. Different natural frequencies, damping and observation loadings can make one block dominate the output covariance. A forced latent order can then ask the estimator to reconstruct structure that is mathematically present but weakly observable.

P0-D12 isolates that mechanism rather than introducing a biological weighting rule.

## Fixed two-component systems

Use the P0-D11 natural frequencies

- component 1: `omega_n = 2*pi*2 Hz`;
- component 2: `omega_n = 2*pi*7 Hz`.

Use three component-chi cases:

1. `both_under = [0.35, 0.55]`;
2. `common_subcritical = [0.75, 0.75]`;
3. `mixed_cross_boundary = [0.65, 1.25]`.

The first two isolate multi-component observability while both components remain on the better-recovered underdamped branch. The mixed case is retained as a harder branch-crossing reference and must not be used to infer a weighting rule.

## Three excitation conditions

### E0: equal state-noise amplitude

Reproduce the P0-D11-style incumbent: each latent state receives the same process-noise standard deviation.

### E1: latent-stationary-trace balance

For each 2D block, compute its stationary covariance under unit isotropic process covariance using the discrete Lyapunov equation. Rescale that block's process-noise amplitude so both blocks have equal stationary latent covariance trace while preserving the total stationary latent trace of the E0 construction.

### E2: observable-output-trace balance

Using the same fixed observation map `C`, compute each block's contribution to stationary output covariance under unit block noise. Rescale block process-noise amplitude so both blocks contribute equal output covariance trace while preserving the total E0 output covariance trace.

E2 is a controlled synthetic observability diagnosis. It is **not** a candidate biological weighting rule and is not available as a truth-based adjustment in future neural data.

## Estimation

For every case and excitation condition:

- simulate 8 independent records;
- add the same 3% channel-SD white measurement-noise stress;
- fit current SSI-COV at fixed development order 4;
- truth-match the four fitted poles only for P0-D scoring;
- reconstruct each paired chi using the pair invariant;
- form the same equal-input-weight developmental `chi_C` used in P0-D11;
- retain singular support and pole-assignment diagnostics.

## Primary diagnostic comparisons

No pass threshold is defined. Compare across E0/E1/E2:

- component stationary participation fractions;
- successful pair-invariant reconstructions;
- component chi absolute error;
- conglomerate chi absolute error;
- `s4/s1` support of the fourth SSI singular direction;
- truth-assignment pole distance;
- stability of fitted poles.

## Interpretation logic

If balancing participation substantially improves component and conglomerate reconstruction in the underdamped cases, P0-D12 supports the mechanism statement that **conglomeration must be participation-aware because latent presence alone does not guarantee observable support**.

If it does not improve reconstruction, the P0-D11 failure must be sought elsewhere, such as estimator order interaction, modal interference, observation geometry, record length or inadequacy of the candidate conglomerate.

Neither outcome licenses a final weight.

## Nonclaims

- No Atlas values are used.
- No neural empirical chi is estimated.
- No healthy/optimal/pathological chi zone is defined.
- No participation threshold is selected.
- No latent-trace or output-trace balancing rule is proposed for real neural data.
- No `chi_system` admission rule is frozen.
- No P0-Q or P1 rule changes.

## Next step if the mechanism is supported

Use a participation-supported two-component construction to test **lineage-preserving chi through the `chi=1` repeated-root boundary**, so pairing on the real-pole side is supplied by tracked dynamical lineage rather than arbitrary static pole pairing.
