# N-B2/N-B3 v0.5 Isolated APQ Re-review Handoff

**Isolation rule:** the reviewer receives only this handoff and scholarly literature. Do not provide sibling review conclusions or exposed v0.1 scientific outcome values.

## Review task

Perform an independent APQ-2 re-review after prospectively accepted material revisions. Identify BLOCKER, MATERIAL, and MINOR objections. Decide whether architecture-level closure is supportable so that exact packet-level APQ may begin. Do not vote. Challenge the finite-suite sufficiency definition, equivalence classes, exact-versus-recoverability separation, controllability/observability/minimal-realization collision, metric and coordinate semantics, B/C/x0 target meaning, global peak procedure, aliasing, switched systems, partial observation, DMD/Koopman boundary, provenance validation, checkpoint identity, and claim ceiling. Every BLOCKER/MATERIAL objection must state the exact prospective correction required.

## Complete authority text

# Bio Chi N-B2/N-B3 Representation-Sufficiency Plan v0.5

**Status:** ROUND-2 APQ REVISED / INDEPENDENT RE-REVIEW REQUIRED / NOT FROZEN  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum

## Scope

Claims are limited to an exhaustively enumerated frozen finite suite. For a target f and representation R, exact sufficiency means f is mathematically constant on every prospectively declared R-equivalence class in that suite. Floating-point tolerances only verify computations; they do not define scientific equivalence after outcomes.

Recoverability is separate. For an observation contract O and observed record y, define the compatible set K_O(y) as the subset of the frozen suite that produces observations compatible with y under the frozen rule. A target is recoverable only when its values over K_O(y) are single-valued under the prospectively frozen recovery comparison. Exact latent descriptors unavailable under O cannot be used by the recovery procedure.

The primary v0.2 recovery layer is deterministic/noiseless sampled observation. A stochastic-noise extension requires separate packet-level APQ that freezes its noise law, RNG, seeds, and compatibility rule.

## Representation maps

Candidate maps include local modal damping/frequency, eigenvalue multiset, separately declared non-normal/reactivity descriptors, finite-time propagator information, B, C, and the full frozen operator. One representation is above another only when the lower representation is a declared deterministic projection of the higher one. There is no universal ladder.

Learned DMD/Koopman estimators are outside the v0.2 claim scope. They remain prior-art comparators unless a later protocol freezes dictionary, rank, noise, and input treatment.

## Coordinate contract

For x'=Sx, transform A'=SAS^-1, B'=SB, C'=CS^-1, G'=S^-T G S^-1, and x0'=Sx0. State norm is sqrt(x^T G x). Physical invariant claims use the transformed metric. Raw Euclidean numerical abscissa and eigenvector condition number are coordinate-dependent diagnostics only.

## Executable targets

Asymptotic stability: alpha(A)=max Re(lambda(A)). If numerical alpha lies within the frozen verification tolerance of zero, the numerical state is NEED_MORE_INFO.

Finite-time state gain: Phi(t)=exp(At), g_G(t)=||G^(1/2) Phi(t) G^(-1/2)||_2, with peak gain max over t in [0,T]. Peak time is the argmax set. If the dominant singular value is numerically degenerate, peak direction is represented by the dominant subspace/projector rather than an arbitrary vector.

Initial-condition response for frozen x0: r(t)=||Phi(t)x0||_G/||x0||_G. Integrated burden is integral of r(t) over [0,T], not squared norm.

B-driven impulse response: x_B(t)=Phi(t)B. When C is part of the target, h(t)=C Phi(t) B. Full curves and prospectively declared norm integrals are separate targets.

C-observed recovery for frozen x0: y(t)=C Phi(t)x0. This licenses only the observed target, not hidden-state recovery.

For piecewise time-varying truth, use the chronological ordered product of segment propagators. Switching order, phase, segment duration, horizon, and continuity with no hidden reset are frozen. A stationary surrogate is an outcome-independent comparator and is never presumed dynamically equivalent.

## Numerical verification

Before execution the packet freezes the horizon, base grid, matrix-exponential method, numerical-only equality tolerances, endpoint handling, tied-peak handling, a global/adaptive peak search over all candidate maxima, and an independent dense/reference peak check. Disagreement beyond the numerical contract is a numerical refusal, not a scientific result.

## Function and Limit recipes

Every matched case names the two or more model identities, the representation held fixed, the target queried, Function versus Limit role, the mathematical expected equality/difference, and numerical verification rule.

Required families include low-order normal Function controls; normal reciprocal spectral Function controls; same local coordinates with different spectra; same local coordinates and eigenvalues with different non-normal response; same A/different B for B-dependent targets; same A,B/different C for observed targets; similarity-related realizations with transformed B/C/G/x0; partial-observation cases; time-varying truth versus frozen stationary surrogate; finite-duration and system-aliasing recoverability cases; and model/observation misspecification controls.

Sampling rates are part of O but cannot by themselves identify a continuous generator. At least one aliasing control must contain more than one continuous model compatible with the same sampled information unless extra information resolves it. Such a case cannot be called uniquely recoverable.

## Independent generator/provenance validation

Before outcome evaluation, an outcome-blind stage verifies every held-fixed equality, same-spectrum identity, A/B/C relationship, similarity and metric transformation, switching sequence/phase, sampling projection, disjoint cross-lane case IDs, and packet/config/code/environment hashes. Failure is a frozen-contract or data-contract refusal and is not repaired from outcomes.

## Firewalls and authority

N-B2/N-B3 confirmatory identities are disjoint from N-B1. No cross-lane confirmatory outcome may tune the other lane before both freezes. v0.1 scientific values remain quarantined development evidence and are not design inputs.

GitHub may validate frozen identity, execute, checkpoint/resume, hash, merge, and package evidence. It cannot choose thresholds, alter metrics, determine sufficiency, rank representations, combine lane verdicts, or promote claims. It stops at SCIENTIFIC_REVIEW_READY for researcher + ChatGPT adjudication.

## Claim ceiling and exact-packet gate

Results are suite-, target-, and observation-contract-specific only. No universal hierarchy, biological prevalence, disease meaning, real-EEG local chi, or whole-system scalar is licensed.

Exact packet-level APQ must bind the exhaustive suite, equivalence classes, target formulas, B/C/x0 contracts, metric transformations, observation-compatible-set rule, numerical tolerances, global peak procedure, switching semantics, alias controls, generator/provenance checks, code/environment identity, disjointness proof, checkpoint mismatch behavior, and access audit before any substantive compute.

