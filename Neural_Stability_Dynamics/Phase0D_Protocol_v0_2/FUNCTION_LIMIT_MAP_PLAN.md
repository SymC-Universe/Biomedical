# NSD P0-D Function Map + Limit Map Plan

Date: 2026-09-11
Protocol: General Protocol v0.7.1 FINAL + v0.7.1A Addendum
Status: **P0-D EXPLORATORY MAPPING PLAN. NOT P1. NO SCIENTIFIC THRESHOLD IS FROZEN HERE.**

## Purpose

Recent NSD qualification work has mapped several failure and refusal boundaries more deeply than the supported interior. v0.7.1A requires the functioning interior and the limits to become coequal targets.

This plan therefore asks:

> Across the known-truth synthetic domain already licensed for P0 development, where do the current estimators recover stable and interpretable structure, how does that structure change under ordinary perturbations, where does recovery degrade or reorganize, and where is the correct answer unresolved or refusal?

This is a method-landscape question. It is not a claim about human neurobiology and it does not define a neural regime boundary.

## Research modes

- Primary mode: `P0-D` discovery and mechanism mapping.
- P0-Q outputs may be overlaid only when they are already independently qualified or clearly labeled qualification evidence.
- No P1 evidence is opened.

## Coverage roles

Every map condition receives one of the v0.7.1A research roles:

- `NOMINAL_FUNCTION`: ordinary well-conditioned synthetic systems inside the estimator's supported construction;
- `PERTURBED_FUNCTION`: noise, duration, observability, conditioning, channel-count, frequency/decay or other perturbations while useful structure remains recoverable;
- `BOUNDARY_OR_TRANSITION`: crowding, weak observability, rank ambiguity, false complexification, model inadequacy or another transition/degradation region;
- `RARE_NATURAL_LIMIT`: `NOT_APPLICABLE_CURRENT_SYNTHETIC_STAGE`.

The role is descriptive and does not determine success in advance.

## Initial map axes

Use only axes already scientifically meaningful to the synthetic System Model or existing estimator construction. Candidate axes include:

1. mode count / observable rank;
2. modal frequency;
3. decay rate;
4. inter-mode frequency separation / crowding;
5. observation strength / weak observability;
6. process noise and measurement-noise family/intensity;
7. record duration / sample count;
8. channel count;
9. similarity-transform conditioning;
10. stationary versus declared piecewise/observation perturbation where an existing synthetic generator supports it.

Ranges and resolution are P0-D choices and must be recorded with provenance. They are not promoted merely because a visually coherent landscape appears.

## Estimator outputs to preserve

For each method/condition where applicable, preserve rather than collapse:

### Structural outputs

- full singular spectrum;
- all requested order/rank fits;
- continuous-time poles;
- carrier/mode-shape or invariant-subspace quantities;
- channel participation;
- adjacent-rank/cross-rank persistence and assignment margins;
- selected rank/order only when an already declared P0 gate is intentionally being evaluated.

### Known-truth comparisons

Where truth is available:

- pole/frequency/decay error;
- individual carrier similarity where identifiable;
- invariant-subspace similarity where individual modes are crowded/non-identifiable;
- recovered observable-rank relation;
- added/lost/shared structure under controlled perturbations.

### Open-channel/model-adequacy outputs

- residual temporal structure;
- predictive/reconstruction error where implemented;
- fitted stability/instability;
- method exceptions;
- rejected/unmatched modes;
- refusal reason;
- uncertainty or indeterminacy when a justified method exists;
- unresolved structure.

## Function Map

The Function Map records regions and trajectories where useful structure is recoverable without requiring perfection. It asks:

- What is recovered?
- At what observable resolution?
- Which modes remain individually identifiable versus subspace-identifiable?
- How do outputs move as controls change?
- Which perturbations are absorbed with stable carrier/system organization?
- When do multiple internal organizations produce observationally similar outputs?
- What information is lost by scalar/order/rank reduction?

A condition may be mapped as `WORKS_HERE` only for the specific claim/object supported there. This does not imply all NSD layers work there.

## Limit Map

The Limit Map records where a specific object or method degrades, changes interpretation, becomes non-identifiable, or must refuse. It asks:

- Which quantity changes first?
- Is degradation gradual, abrupt or unresolved?
- Does coupling/crowding protect a subspace while destroying individual mode identity?
- Does the estimator invent oscillatory structure in a non-oscillatory system?
- Does model adequacy fail before structural recovery visibly collapses?
- Does a different representation become necessary?

Use `STOPS_WORKING_HERE` only for the specific method/claim whose support is actually lost. Use `NOT_KNOWN_HERE` when the evidence cannot distinguish the alternatives.

## Comparator treatment

SSI-COV and Subspace DMD are mapped independently before any added-value comparison. Their different rank constructions are not forced into identical semantics simply for symmetry.

The preserved P0Q1 result is an overlay on the Limit Map, not a target to be optimized away.

## Balance rule

Each substantial map batch should include ordinary/supported conditions and adversarial/transition conditions when the synthetic model permits both. Equal sample counts are not required.

At each mapping milestone, record:

1. what was learned about where the representation works;
2. what was learned about where it stops working;
3. whether the next P0 stage should emphasize function or limits to restore scientific balance.

## Promotion firewall

Any new boundary, favorable region, candidate mechanism, rank heuristic, uncertainty rule, or cross-method relationship discovered from the map is `P0-D` / post-result evidence. It may motivate a P0-Q qualification design but cannot confirm itself and cannot retroactively rescue P0Q1.
