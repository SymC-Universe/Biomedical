# Chi Conglomeration Axioms Draft

Date: 2026-09-11
Status: **P0-D ARCHITECTURE DRAFT. NOT A FROZEN CHI_SYSTEM DEFINITION.**

## Purpose

Define what `conglomeration` means in NSD before the independent Neurostability Atlas is allowed to evaluate functional meaning.

**Correction recorded 2026-09-11:** conglomeration is not an average, weighted average, RMS, or other arithmetic pooling of component chi values. P0-D11/P0-D12 used such an aggregate as a developmental mechanism probe. That construction remains reproducible historical evidence, but it is not the governing definition of conglomeration.

The Atlas may later test whether independently derived coordinates organize nominal function, perturbation, transition and natural limits. It must not choose the coordinate or coupling architecture because a particular construction makes outcomes look attractive.

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

## Governing definition of conglomeration

A conglomerate is a **coupled dynamical entity** composed of subsystems together with the directed transformations by which they affect one another.

For subsystem states `x_i`, a linear local representation is

`dx_i/dt = A_i x_i + sum_{j != i} K_ij x_j`,

where `A_i` describes the subsystem's internal dynamics and `K_ij` maps the state of subsystem `j` into its effect on subsystem `i`.

Stacking all states gives

`dx/dt = A_full x`,

with

`A_full = blockdiag(A_1, ..., A_m) + K`.

The off-diagonal blocks of `K` are not weights. They are directed dynamical transformations.

### Group-to-environment feedback closure

For a grouped subsystem `G` embedded in an environment/remainder `E`, write

`dx_G/dt = A_G x_G + K_GE x_E`,

`dx_E/dt = A_E x_E + K_EG x_G`.

In the Laplace domain, eliminating `E` yields the effective grouped dynamics

`[sI - A_G - Sigma_G(s)] x_G = 0`,

where

`Sigma_G(s) = K_GE (sI - A_E)^(-1) K_EG`.

`Sigma_G(s)` is the feedback-return operator. It represents, at frequency/complex rate `s`, what the group sends into the rest of the system, how the rest transforms that signal through its own dynamics, and what returns to alter the group's behavior.

This is the current mathematical prototype of conglomeration. It is not yet a frozen real-neural estimator.

## Axioms for conglomeration and chi placement

### C1. No averaging definition

No arithmetic mean, weighted mean, RMS, voting rule, or generic pooling of component `chi_j` values defines conglomeration.

Historical aggregate formulas may remain as diagnostic controls, but they must be labeled as aggregates rather than conglomeration.

### C2. Subsystem identity is retained

Each admitted subsystem or lineage retains its own internal dynamics and, where licensed, its own `chi_j`. Coupling does not erase the constituent description.

### C3. Directed contribution

A subsystem's contribution to the larger system is represented by the dynamical effect it exerts through coupling pathways, not by a scalar importance weight alone. Direction matters: the effect `j -> i` need not equal the effect `i -> j`.

### C4. Feedback closure

Conglomeration must include both what a subsystem sends and what it receives back. A one-way influence map is incomplete whenever closed feedback paths are present.

### C5. Transformation matters

The returned influence is not assumed to be a copy of the outgoing signal. Other subsystems may filter, delay, rotate, mix, amplify, suppress or otherwise transform it before it returns. The internal dynamics of intermediary systems are therefore part of the conglomerate object.

### C6. Emergent global dynamics

Coupling may create, destroy, split, merge, stabilize, destabilize or reorganize global modes. Therefore the global modal structure must be derived from the coupled system itself. It cannot in general be inferred by arithmetically combining the uncoupled component chi values.

### C7. Conditional system chi

A scalar `chi_system` is not assumed to exist for every conglomerate. It is reportable only if the coupled system supports a licensed dynamical object for which a scalar chi coordinate is mathematically and empirically justified.

Otherwise the correct output may be a set/field of lineage-level chi coordinates plus the coupling/feedback architecture, or `NO_COHERENT_SYSTEM_CHI`.

### C8. Hierarchical grouping coherence

A subsystem may itself be a conglomerate. Cells, local circuits, regions, networks and larger grouped entities can be represented at different levels if the reduction preserves the relevant input-output and feedback behavior. Changing bookkeeping boundaries must not silently change the physical claim.

### C9. Basis invariance

Changing coordinates inside an admitted state subspace must not change physical conclusions. Component chi from trace/determinant is basis invariant, and coupling analyses must be formulated in a way that distinguishes physical transformations from coordinate relabeling.

### C10. Lineage continuity

A supported lineage should remain trackable through representation changes, including complex-pair -> repeated-root -> real-split transitions, when the underlying dynamical object remains coherent.

### C11. Participation is dynamical, not a weight prescription

P0-D12 showed that whether a component materially appears in the observed system matters for reconstruction. In the revised architecture, participation is evidence about a subsystem's realized contribution to the coupled dynamics and observables. It is not a license to average component chi values.

### C12. Missingness honesty

An unresolved pathway, subsystem or feedback return must remain explicit. It must not be silently replaced by zero coupling or zero contribution unless that zero is independently justified.

### C13. Epistemic separation

Model adequacy, uncertainty, rank support, crowding, estimator agreement and lineage confidence determine whether a coordinate/coupling statement may be reported and at what resolution. They are not generic numerical penalties inside chi.

### C14. Decomposition transparency

Every system-level report must retain enough structure to reconstruct the claim: subsystem identities, local lineages, local chi where licensed, directed coupling pathways, relevant feedback loops, grouping level, observability/resolution state and uncertainty.

The scalar never replaces the modal or conglomerate structure.

### C15. Atlas independence

No coupling pathway, subsystem boundary, scalar reduction, gray zone or target range may be selected because of Atlas phenotype/outcome structure. Atlas evidence is evaluative, not formative, for the pre-Atlas dynamical architecture.

### C16. Refusal is valid

If no coherent supported coupled reduction exists, or if a scalar chi is not licensed, the correct output is an explicit unresolved/non-scalar state rather than a forced number.

## Historical developmental RMS aggregate: retained but rejected as conglomeration

P0-D11/P0-D12 used

`chi_RMS = sqrt(sum_j w_j (chi_j omega_n,j)^2) / sqrt(sum_j w_j omega_n,j^2)`.

This was useful diagnostically because it exposed how unequal observability/participation can corrupt arithmetic pooling. It is now explicitly classified as a **historical developmental aggregate**, not as `chi_system` and not as the definition of conglomeration.

P0-D12 remains scientifically useful: it demonstrated that latent presence, observable participation and identifiability are distinct. Those findings now inform admission/resolution and coupling analysis rather than a weighting prescription.

## Pre-Atlas quantities to investigate next

Without using Atlas outcomes, NSD can investigate:

- directed coupling blocks or transfer operators between admitted subsystems;
- closed-loop feedback-return operators `Sigma_G(s)`;
- changes in global eigenstructure caused by adding/removing a coupling pathway;
- sensitivity of global lineages to specific directed couplings;
- pathway gain, phase, delay and frequency dependence where identifiable;
- subsystem-to-global modal participation without collapsing it to an averaging weight;
- preservation or loss of effective second-order structure after coupling;
- conditions under which a coherent scalar chi exists at a chosen grouping level;
- conditions under which the correct representation is instead multiple chi coordinates plus a coupling map.

## Current reporting architecture

A mature NSD report should distinguish at least:

1. **local/modal coordinates:** admitted lineages and their `chi_j` values;
2. **conglomerate architecture:** grouped subsystems, directed couplings, feedback loops and transformations;
3. **emergent/global coordinates:** chi only for coupled global/effective lineages that independently earn a scalar description;
4. **epistemic state:** adequacy, uncertainty, crowding, missingness, identifiability and resolution attached to all of the above;
5. **Atlas interpretation:** independent Function Map and Limit Map over the previously derived dynamical objects.

This preserves the standing rule that the fullest picture is modal structure + scalar chi/stability coordinates + conglomeration/system-level organization, while making `conglomeration` explicitly interactional rather than arithmetic.
