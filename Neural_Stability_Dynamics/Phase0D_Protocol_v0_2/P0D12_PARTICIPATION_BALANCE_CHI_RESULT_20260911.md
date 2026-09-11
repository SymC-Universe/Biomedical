# P0-D12 Participation-Balance Chi Diagnosis Result

Date: 2026-09-11
Status: **P0-D RESULT. NOT ATLAS CALIBRATION. NOT P0-Q. NOT P1.**
Workflow run: `34615694676`
Job: `103316945880`
Artifact ID: `10269799755`
Artifact ZIP SHA256: `a2634646533e91340d215a7b29c6394b9273d7930143b7101155fd1c098ff6be`

## Question

Was the poor forced two-component chi reconstruction in P0-D11 substantially caused by unequal stationary participation of the latent components in the observed covariance record?

## Mechanical result

Nine dedicated chi/participation tests passed. The discrete Lyapunov construction correctly preserves the requested incumbent total variance while equalizing either latent stationary trace or observable-output covariance trace.

## Central result

**Yes, unequal participation was a major cause in at least one clean two-underdamped regime, but participation balance is not sufficient to solve all multi-component reconstruction problems.**

### Both-under case: chi = [0.35, 0.55]

The equal-state-noise incumbent produced output participation fractions of approximately `[0.810, 0.190]`.

- successful pair reconstructions: `5/8`;
- median component-1 chi error: `0.024`;
- median component-2 chi error: `0.440`;
- median conglomerate chi error: `0.303`;
- median `s4/s1`: `0.0457`;
- median maximum truth-assignment pole distance: `35.4`.

Latent-trace balancing produced output participation approximately `[0.509, 0.491]`:

- successful: `8/8`;
- component-1 error: `0.016`;
- component-2 error: `0.033`;
- conglomerate error: `0.030`;
- `s4/s1`: `0.140`;
- truth-assignment distance: `4.17`.

Output-trace balancing produced exactly `50/50` output participation:

- successful: `8/8`;
- component-1 error: `0.016`;
- component-2 error: `0.033`;
- conglomerate error: `0.030`;
- `s4/s1`: `0.145`;
- truth-assignment distance: `4.13`.

Thus balancing participation reduced median conglomerate error by roughly a factor of ten and dramatically improved both recovery of the second component and rank-4 singular support.

## Common-subcritical case: chi = [0.75, 0.75]

The equal-state-noise condition had output participation approximately `[0.767, 0.233]` and produced no successful pair-invariant reconstruction (`0/8`).

Balancing helped but did not solve the problem:

- latent-trace balance: `2/8` successful, median conglomerate error `0.160`;
- output-trace balance: `3/8` successful, median conglomerate error `0.113`.

The rank-4 support remained modest (`s4/s1` about `0.084-0.089`) and pole-assignment distances remained large.

This shows that equal observable variance does not guarantee separable/identifiable modal structure.

## Mixed cross-boundary case: chi = [0.65, 1.25]

Equal-state-noise output participation was approximately `[0.770,0.230]`. All three excitation designs yielded `6/8` successful records.

Median conglomerate error changed from:

- equal state noise: `0.255`;
- latent-trace balance: `0.169`;
- output-trace balance: `0.177`.

Rank-4 singular support improved from about `0.090` to `0.123-0.124`, but truth-assignment pole distances remained very large (`~83`). The overdamped/high-frequency component therefore remains a difficult identification object even when stationary participation is balanced.

## Interpretation

P0-D12 supports a more precise conglomeration architecture:

1. **Latent presence is not enough.** A component that contributes little to the observable covariance can corrupt a forced system-level chi if it is treated as equally known.
2. **Participation matters materially.** In a clean underdamped case, making the second component comparably observable transformed the reconstruction from poor/fragile to accurate and complete.
3. **Participation is not identifiability.** Equal variance does not guarantee that damping/frequency structure is separable at the requested estimator resolution.
4. **A future system chi should not blindly average or RMS every latent component.** Candidate components must first earn admission at an appropriate resolution level.
5. **Participation, model adequacy, branch/timescale resolution, crowding and uncertainty should remain explicit companion/gating information.** They should not be silently converted into a generic goodness weight inside chi.

## Consequence for the user's coordinate interpretation

The data are compatible with the working idea that chi is a placement coordinate formed from the dynamical components that actually participate in the supported system organization. The Atlas can later map function and limits over those independently derived coordinates.

However, the current evidence does **not** yet identify the correct real-data participation weight. Controlled balancing is a mechanism probe, not a weighting prescription.

## Next P0-D step

Proceed with a lineage experiment only on a construction where both components are demonstrably recoverable. Track one low-frequency second-order lineage across `chi<1 -> chi=1 -> chi>1` while a separately identifiable companion remains present. Use data-only continuity to preserve pair identity across the repeated-root transition and truth only for retrospective P0-D scoring.

The key question is whether lineage plus trace/determinant invariants can preserve a continuous chi coordinate when individual pole labels become branch-ambiguous near the exceptional point.

## Nonclaims

- No Atlas value was used.
- No neural population chi is estimated.
- No biological participation weight is selected.
- No participation threshold is selected.
- No system-level chi admission rule is frozen.
- No P0-Q or P1 rule is changed.
