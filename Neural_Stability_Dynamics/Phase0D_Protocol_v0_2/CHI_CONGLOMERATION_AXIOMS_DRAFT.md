# Chi Conglomeration Axioms Draft

Date: 2026-09-11
Status: **P0-D ARCHITECTURE DRAFT. NOT A FROZEN CHI_SYSTEM DEFINITION.**

## Purpose

Define what a legitimate system-level chi construction must do **before** the independent Neurostability Atlas is allowed to evaluate its functional meaning.

The Atlas may later test whether an independently derived coordinate organizes nominal function, perturbation, transition and natural limits. It must not choose the formula because a particular formula makes those outcomes look attractive.

## Starting object: an admitted second-order lineage

For one licensed real two-dimensional dynamical lineage with generator block `B`,

`chi_j = -tr(B_j) / (2 sqrt(det(B_j)))`,

provided the block is stable under the adopted convention and `det(B_j)>0`.

Equivalently,

`chi_j^2 - 1 = (tr(B_j)^2 - 4 det(B_j)) / (4 det(B_j))`.

This makes the component coordinate branch-complete:

- `chi_j < 1`: complex-conjugate / underdamped side;
- `chi_j = 1`: repeated-root boundary;
- `chi_j > 1`: real-split / overdamped side.

The component must first be admitted as a real dynamical lineage. Algebraic availability alone does not license arbitrary real-pole pairing.

## Axioms for a candidate system coordinate

### C1. Single-component consistency

If exactly one component participates, the system coordinate must reduce to that component chi.

### C2. Common-chi consistency

If every admitted participating component has the same chi, the system coordinate must equal that common chi regardless of their natural frequencies, basis coordinates or ordering.

### C3. Basis invariance

Changing coordinates within an admitted invariant subspace must not change the component or system coordinate.

### C4. Permutation invariance

Relabeling components must not change the scalar.

### C5. Branch completeness

The construction must not cease to exist merely because a supported lineage crosses from complex poles through a repeated root to a real split. Loss of coordinate is allowed only when the lineage itself becomes unsupported/unresolved.

### C6. Participation coherence

Components should affect the system coordinate according to an independently justified measure of their participation in the supported system organization. Latent existence alone is insufficient. P0-D12 demonstrates that a weakly participating component can be present in the generator while being poorly reconstructable from the observed covariance.

No specific neural participation weight is selected by this axiom.

### C7. Refinement coherence

Purely representational duplication or subdivision of one physical contribution must not arbitrarily move system chi when total physical participation is conserved. A future weighting architecture should therefore distinguish additional physical participation from bookkeeping duplication.

### C8. Missingness honesty

An unsupported component must not be silently assigned zero weight as though its dynamical contribution were known to be zero. Missing/unresolved structure must remain explicit and may force a partial or indeterminate system coordinate.

### C9. No epistemic contamination of value

Model adequacy, uncertainty, rank support, crowding, estimator agreement and lineage confidence determine whether a coordinate may be reported and at what resolution. They must not automatically be mixed into the numerical chi value as generic quality penalties.

A physical participation weight may depend on a validated dynamical contribution measure, but an epistemic confidence score is conceptually different.

### C10. Decomposition transparency

Every reported system chi must retain the component-level decomposition needed to understand how that scalar was obtained. At minimum this includes admitted lineage identifiers, component chi, natural scale, participation weight/proxy, resolution status and uncertainty state.

The scalar never replaces the modal or conglomerate structure.

### C11. Atlas independence

No formula, component admission rule, participation weight, gray zone or target range may be selected because of Atlas phenotype/outcome structure. Atlas evidence is evaluative, not formative, for the pre-Atlas coordinate architecture.

### C12. Refusal is valid

If no coherent supported conglomeration exists, the correct output is `NO_COHERENT_SYSTEM_CHI` or another explicit unresolved state, not a forced scalar.

## Current developmental candidate

P0-D11/P0-D12 use

`chi_C = sqrt(sum_j w_j (chi_j omega_n,j)^2) / sqrt(sum_j w_j omega_n,j^2)`.

This can be rewritten as

`chi_C^2 = sum_j pi_j chi_j^2`,

where

`pi_j = w_j omega_n,j^2 / sum_k w_k omega_n,k^2`.

So the current candidate is a weighted RMS of component chi under natural-scale-adjusted weights.

This identity makes two things explicit:

1. the chosen `w_j` matters scientifically;
2. even with equal input weights, higher natural-frequency components receive greater effective weight through `omega_n^2`.

P0-D12 shows that **equal input weights must not be confused with equal observable participation**. The current formula remains a developmental candidate, not a validated system coordinate.

## Candidate participation concepts to investigate without Atlas

Potential pre-Atlas participation measures include:

- modeled contribution to stationary output covariance;
- modeled contribution to lag-covariance/Hankel structure;
- modal residue or output-mode energy under a scale-invariant normalization;
- persistence/occupancy across windows;
- invariant-subspace contribution when individual carriers are unresolved.

These candidates must be tested for basis invariance, sensor-scaling sensitivity, decomposition dependence and reproducibility before any one becomes a weight.

## Important separation

A future NSD report may therefore contain three different kinds of information:

1. **modal coordinates:** the component lineages and their `chi_j` values;
2. **conglomerate coordinate:** a system `chi_C` only when an admitted participation architecture exists;
3. **epistemic state:** adequacy, uncertainty, crowding, missingness and resolution attached to those coordinates.

That structure matches the standing rule that the fullest picture is modal structure + scalar chi/stability coordinates + conglomeration/system-level organization.
