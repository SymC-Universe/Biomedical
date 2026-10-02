# Bio Chi N-B2/N-B3 Representation-Sufficiency Plan v0.4

**Status:** ROUND-1 EXTERNAL APQ ADJUDICATED / ROUND-2 REQUIRED / NOT FROZEN  
**Date:** 29 September 2026  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum  
**Supersedes:** v0.3 for prospective planning

## Residual scientific target

The program does not claim a new minimal-realization theorem or universal representation hierarchy.

For a prospectively frozen model class \(\mathcal M\), target functional \(f\), and representation map \(R\), define exact representation sufficiency by:

\[
R(m_1)=R(m_2) \implies f(m_1)=f(m_2)
\]

for all frozen matched models \(m_1,m_2\in\mathcal M\), up to a prospectively frozen numerical identity tolerance appropriate to \(f\).

A representation is minimal only relative to the frozen partial order of available information and the specific target. No universal ranking is permitted.

## Exact sufficiency versus recoverability

Layer E uses generating truth and asks whether the target is constant on representation-equivalence classes.

Layer R uses only the declared observation/sampling contract. Recoverability asks whether models compatible with the observed information contract yield the same target within the frozen recovery tolerance.

Exact sufficiency never implies empirical recoverability, and empirical recoverability cannot establish a richer latent representation that is not identifiable from observations.

## Representation information sets

Candidate information sets may contain:

- local modal damping/frequency coordinates;
- embedded eigenspectrum;
- non-normal/reactivity structure;
- finite-time propagator structure;
- explicit input/perturbation operator B;
- observation operator C;
- full frozen state-space/operator representation.

These form a partial order of information for the frozen target, not a single ladder.

“Embedded eigenspectrum” means eigenvalues only unless eigenvectors are explicitly added as a separate representation component.

## Perturbation and observation semantics

Three target families are separated prospectively:

1. autonomous/initial-condition response, using frozen initial-state normalization;
2. B-driven input response, using frozen input norm and input class;
3. C-observed response, using frozen observation map and output norm.

Same-A/different-B contrasts may only inform B-dependent targets. Same-A,B/different-C contrasts may only inform observed-output targets.

No B/C contrast is interpreted for a target mathematically invariant to that operator.

## Metric and invariance contract

State-norm finite-time quantities require a declared physical SPD metric G.

Under similarity transform \(x'=Sx\), the physical metric transforms as:

\[
G' = S^{-T}GS^{-1}.
\]

Physical gain must be compared using the transformed metric. Raw Euclidean gain and eigenvector condition number may be recorded as coordinate-dependent diagnostics but cannot support coordinate-invariant sufficiency claims.

Input and output norms are frozen separately.

Round-2 APQ must receive the exact invariance contract and numerical tolerance before execution.

## Target functionals

Primary targets are defined separately:

- asymptotic stability via spectral abscissa/sign;
- embedded modal organization via frozen spectral descriptors;
- finite-horizon peak physical-metric propagator gain;
- peak time and normalized peak direction;
- full perturbation-specific response trajectory;
- integrated response burden over the frozen horizon;
- B-driven input-output response;
- C-observed recovery trajectory;
- explicit time-varying reorganization.

Primary recovery evidence uses full curves and continuous functionals. Thresholded return times are secondary only.

Integrated burden must specify norm versus squared norm before freeze.

## Peak capture and numerical accuracy

The execution packet must prospectively define:

- finite horizon;
- base time grid;
- peak-refinement/interpolation procedure;
- numerical matrix-exponential tolerances;
- equality tolerance for held-fixed quantities;
- anti-aliasing/resampling procedure for sampled recoverability.

A grid-point maximum alone is not sufficient if the peak can lie materially between grid points.

## Function Map

Function cases must include:

- ordinary normal/decoupled systems where low-order information suffices for the declared target;
- normal coupled systems where eigenspectrum suffices for asymptotic/modal targets;
- strongly non-normal stable systems where propagator/non-normal information is demonstrably necessary and sufficient for a finite-time target within the frozen suite;
- B/C-aligned cases where input/output structure reduces the relevant target space;
- partially observed cases where the declared observable target remains recoverable;
- stationary and explicitly time-varying cases where the correct representation is known.

## Limit Map

Limit cases must include:

- same local damping with different embedded spectra;
- same local damping and same eigenvalues with different non-normal response;
- same A with different B for B-dependent targets;
- same A and B with different C for observation-dependent targets;
- similarity-related realizations;
- hidden/unobservable modes;
- time-varying operator truth versus a prospectively defined stationary surrogate;
- finite-duration, noise, and sampling/aliasing challenges;
- model/observation misspecification outside the assumed generator family.

## Time-varying truth

The time-varying truth is a separate model class with a frozen switching law, switching phase, segment boundaries, and operator sequence. A stationary surrogate is generated by a frozen rule independent of observed discrepancy. The surrogate is not presumed dynamically equivalent.

## Scope of conclusions

Finite matched cases can establish necessity/sufficiency only for the frozen suite/model class and target. Individual counterexamples demonstrate insufficiency of a representation for that target; they do not establish a universal ranking.

## Cross-lane and exposure firewall

N-B2/N-B3 confirmation cases are disjoint from N-B1 confirmation cases. No confirmatory outcome from one lane may tune the other before both freezes close.

The exposed v0.1 scientific values are not used to choose v0.4/v0.2 criteria. Fresh v0.2 identities are generated only after round-2 APQ from frozen rules.

## GitHub authority

GitHub may validate frozen identity, execute cases, checkpoint, resume, hash, merge, and package evidence. It may not decide scientific sufficiency, rank representations, choose thresholds, alter metrics, or promote a claim. It stops at `SCIENTIFIC_REVIEW_READY`.

## Claim ceiling

The result can establish only target-specific known-truth sufficiency/recoverability behavior for the frozen model classes and observation contracts. It cannot establish a universal representation hierarchy, real-EEG validity, disease meaning, biological prevalence, or a whole-system scalar.
