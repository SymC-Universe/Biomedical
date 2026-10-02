# NSD Substrate Closure Qualification Preflight v0.1

Status: PREDECISION ANALYTIC / KNOWN-TRUTH QUALIFICATION ONLY  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Branch: `nsd-rebuild-gom-v0.8.0`

## Purpose

This preflight integrates the Substrate Inheritance closure/projection requirement into NSD Bio Chi without changing the production A0/A1/A2 estimator family or licensing real EEG local chi.

A local continuous-time mode may be structurally identifiable and sampling-invariant yet still be scientifically incomplete if the chosen modal subspace is not sufficiently autonomous relative to omitted substrate/interface states. This record therefore separates exact projection mechanisms before any empirical closure threshold is considered.

## Block decomposition

For a linear generator L and an orthogonal state-space split into candidate modal subspace P and complement Q,

[
L =
\begin{bmatrix}
L_{PP} & L_{PQ}\\
L_{QP} & L_{QQ}
\end{bmatrix}.
]

The following are distinct:

- `L_QP`: P-to-Q leakage. If nonzero, a trajectory initialized entirely in P generally leaves P.
- `L_PQ`: Q-to-P hidden-input exposure. If nonzero, hidden/substrate state can directly alter P even when P itself does not leak.
- `Sigma(z)=L_PQ (zI-L_QQ)^{-1} L_QP`: return-memory / self-energy. This is nonzero only when a pathway exists from P into Q and back to P.

These are not interchangeable diagnostics.

## Exact structural statements

1. P is an exactly invariant subspace for P-only initial conditions iff `L_QP=0`.
2. P dynamics are independent of arbitrary hidden Q state iff `L_PQ=0`.
3. Bidirectional P<->Q coupling generically induces a frequency-dependent reduced generator through `Sigma(z)`.
4. The exact projected resolvent obeys the Schur-complement identity

[
P(zI-L)^{-1}P
=
[zI-L_{PP}-\Sigma(z)]^{-1}
]

when the relevant inverses exist.
5. The same isolated/local oscillator block can therefore belong to different closure classes depending on substrate/interface coupling. Local chi alone does not establish closure.

## Known-truth closure classes

The prospective contract fixtures distinguish:

- exact closed / memory-free: `L_QP=0`, `L_PQ=0`;
- invariant but hidden-input exposed: `L_QP=0`, `L_PQ!=0`;
- leaky without return: `L_QP!=0`, `L_PQ=0`;
- bidirectional return-memory: `L_QP!=0`, `L_PQ!=0`, generically `Sigma(z)!=0`.

No numerical cutoff is frozen. The first qualification stage uses exact zero/nonzero known truths and exact algebraic identities only.

## Relation to N-B1

Continuous-lineage family C remains the prospective N-B1 target. Closure qualification is an additional gate, not a replacement for C membership.

Prospective local-chi admission therefore requires evidence for:

- continuous modal lineage;
- structural identifiability;
- alias-safe sampling lineage;
- adequate closure/projection behavior for the claimed local mode;
- successful refusal controls.

A future empirical closure tolerance, if required, is a scientific decision and must be prospectively frozen rather than inferred after real-EEG outcomes.

## Relation to A1/A2 false-mode behavior

A2 preference does not by itself establish a second biological mode. Extra fitted state can compensate for omitted forcing geometry, hidden-state input, P-to-Q leakage, return-memory, projection error, or a genuine second mode.

The closure contracts therefore provide adversarial explanations that must be distinguished from true multimodality before N-B1 promotion.

## Executable contracts

Test module:

`NSD_vNext/engine/tests/test_substrate_closure_contracts.py`

Dedicated CI:

`.github/workflows/nsd-state-space-lineage-sampling-contracts.yml`

The tests verify exact zero/nonzero closure classes and the Schur-complement projected-resolvent identity. They do not fit real EEG and do not define a biological closure threshold.

## Current interpretation ceiling

This preflight supports qualification design only. It does not:

- license real-EEG local chi;
- change A0/A1/A2;
- define MODE_NOT_CLOSED as a production refusal code;
- define an empirical closure cutoff;
- imply that any observed A2 selection is caused by closure failure;
- alter N-B2 or N-B3 claims.
