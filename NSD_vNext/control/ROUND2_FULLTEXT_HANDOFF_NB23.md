# NSD N-B2/N-B3 Round-2 Full-Text External APQ Handoff

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


## Fresh untouched packet scaffold
# NSD Fresh Untouched v0.2 Packet Scaffold

**Status:** PREPARATORY / NOT FROZEN / NO EXECUTION AUTHORITY  
**Governance:** SymC GOM v1.0 + Continuity Hardening Addendum  
**Purpose:** reserve the structure of a future untouched qualification packet without selecting scientific values before independent APQ adjudication.

## Freshness firewall

The following v0.1 identities are permanently exposed-development and forbidden from untouched reuse:

- N-B1 seeds: 913103, 927229, 941351, 967403
- N-B1 truth IDs: C_F0, C_F1, C_F2, C_F3, C_F4, L_D_POS, L_D_NEG, L_S_POS, L_S_NEG, L_MEMORY, L_TWO_MODE
- N-B2/N-B3 packet identity: NB2NB3_MATCHED_20260929_A
- all v0.1 matrices, B/C pairings, similarity transform, switching law, and sampling projections when used in the same confirmatory role

They may be retained only as P0-D development evidence.

## Required v0.2 fields after APQ closure

### N-B1

- fresh packet ID
- fresh Function truth identities
- fresh Limit truth identities
- fresh seeds
- generators and parameters
- duration/rates
- observation/reference transforms
- per-class applicability map for P/S/T/F/O/M/R/N/I/U channels
- inherited tolerance provenance
- any development-only tolerance calibration set
- exact machine row schema
- exact refusal grammar
- representative Function coverage
- explicit FRAMEWORK_NOT_OPERATIONAL rule

### N-B2/N-B3

- fresh packet ID
- fresh exact A/B/C matched families
- fresh similarity/invariance adversaries
- physical metric and transformed metric rule
- finite horizons
- perturbation families
- fresh time-varying law and stationary surrogate rule
- fresh sampling/noise contracts
- exact held-fixed identity tolerances
- target functionals
- exact recoverability procedures
- machine-readable evidence schema

## Lane-specific checkpoint contract

Each lane must maintain independently:

- lane state
- last completed scientific-neutral checkpoint
- frozen packet/config/code identities
- completed case identities + artifact hashes
- incomplete case identities
- next exact mechanical action
- active workflow/run identity
- stop reason if any

Cross-lane completion may never mask stagnation in the other lane.

## Authority firewall

No field that materially changes the scientific question may be frozen until independent APQ adjudication closes. GitHub may not fill missing scientific values. This scaffold itself grants no execution authority.


## Operational ceiling
# NSD Long-Run Conveyor Ceiling v0.1

**Status:** FROZEN OPERATIONAL CEILING  
**Date:** 29 September 2026  
**Governance:** SymC General Operations Manual v1.0

## Purpose

This document separates scientific authority from execution plumbing.

GitHub Actions may execute only prospectively frozen work, preserve evidence, verify contracts, checkpoint progress, resume after interruption, and package evidence for review. GitHub Actions may not make scientific decisions.

## Scientific authority

Scientific interpretation, claim promotion, architecture revision, threshold selection, new hypothesis selection, and decisions about chi/Chi/system meaning remain with the researcher and ChatGPT.

The conveyor must never:

- invent or alter a scientific threshold;
- change a frozen generator, comparator, metric, horizon, seed, sampling contract, observation mapping, or perturbation;
- decide whether a result supports or falsifies a scientific claim;
- decide whether local chi is scientifically admitted to real EEG;
- collapse local chi, modal/vector Chi, and system/conglomerate behavior;
- convert designed qualification frequencies into prevalence;
- repair a scientific failure by changing the design.

## Ceiling

The conveyor is authorized to run continuously through the following operational ceiling for both N-B1 and N-B2/N-B3:

1. `PACKET_BOUND`
2. `FROZEN_INPUT_VALIDATED`
3. `IMPLEMENTATION_TESTED`
4. `PREFLIGHT_PASS`
5. `FULL_EXECUTION_COMPLETE`
6. `MERGED_EVIDENCE_COMPLETE`
7. `REPRODUCIBILITY_CHECK_COMPLETE`
8. `SCIENTIFIC_REVIEW_READY`

The conveyor stops at `SCIENTIFIC_REVIEW_READY`. Scientific adjudication occurs outside GitHub.

## Early stop conditions

The conveyor may stop earlier only for:

- `MECHANICAL_FAILURE`
- `FROZEN_CONTRACT_VIOLATION`
- `SOURCE_OR_DEPENDENCY_BLOCK`
- `CHECKPOINT_CORRUPTION`

A numerical result that is surprising, unfavorable, null, pathological, or outlying is not an early-stop condition by itself. It is preserved as evidence.

## Checkpoint contract

A machine-readable checkpoint is written after every ceiling stage. Every checkpoint contains:

- lane;
- stage;
- UTC timestamp;
- git SHA;
- packet/config digest;
- completed case identities;
- incomplete case identities;
- artifact paths and hashes where available;
- next exact mechanical action;
- stop reason if stopped.

On restart, the conveyor resumes from the newest internally consistent checkpoint and must not recompute completed cases unless their artifact is missing or hash-invalid.

## Runtime contract

One GitHub Actions run may execute for up to 330 minutes. The conveyor should keep moving within the same run as long as mechanically authorized work remains. Near the runtime reserve, it must checkpoint and exit cleanly. A scheduled successor run resumes from that checkpoint.

This ceiling does not authorize any real-EEG local-chi inference or new scientific claim.



## Reviewer instruction

This is an isolated APQ-2 review. Do not assume usefulness, do not infer prior reviewer conclusions, and do not vote. Identify BLOCKER, MATERIAL, and MINOR objections. Execution authority is false. Do not request or inspect v0.1 scientific outcome values. Return explicit prospective corrections required before a fresh v0.2 exact packet can be frozen.
