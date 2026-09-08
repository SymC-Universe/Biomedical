# Neural Stability Dynamics Phase 0C v0.2
## Untouched Three-Layer Synthetic Holdout Preregistration

Frozen before any Phase 0C v0.2 scientific execution.

## Why v0.2 exists
Phase 0C v0.1 was prospectively frozen but was superseded before scientific execution. The revision was made after the recent GRI C1 result changed the appropriate interpretation of the preceding neural Phase 0B result. The GRI result is used only as a methodological prompt: organized cross-layer structure can remain meaningful without elevating a historical scalar interpretation to the organizing principle. It does not supply neural thresholds, neural labels, a shared mechanism, or a biological chi target.

Phase 0B independently showed the neural-side reason for the same methodological caution: poles/eigenvalues could remain accurately recoverable while individual eigenvectors became unstable near degeneracy, with the joint observable subspace remaining stable. Therefore subspace and whole-system organization are not treated as exceptions to a scalar-first analysis in v0.2.

## Prospective sequence
`Phase 0A easy recovery -> Phase 0B adversarial development -> perspective revision before Phase 0C execution -> freeze three-layer rules -> Phase 0C v0.2 untouched holdout -> label-blind EEG adequacy only for prospectively passing layers`

No Phase 0C v0.2 result may be used to change its thresholds and then be rescored as a prospective pass.

## Three separable evidential layers

### Layer A: scalar-spectrum state
Primary objects are individually identifiable complex poles/eigenvalues. This layer asks whether temporal decay/frequency coordinates are stable across record halves and model order.

It does not create a whole-system scalar. Individual real-pole scalar values remain refused in this version.

### Layer B: modal/carrier structure
Primary objects are observable mode shapes when individually identifiable and invariant/modal subspaces when crowding makes individual eigenvectors unstable.

A scalar-spectrum failure does not automatically imply modal failure. Conversely, a stable pole does not establish a correct carrier.

### Layer C: whole-system organization
The whole-system object is deliberately not a single number. It is the structured tuple:

`(effective observable order, observable-subspace projector, normalized channel-participation profile, normalized pairwise pole geometry)`

This layer asks whether collective organization is preserved even when one lower-level coordinate changes, and whether it refuses when relational organization genuinely reorganizes.

## Common frozen order gate
Candidate orders are defined in `configs/phase0c_design.json`.

For candidate order q:

`g_q = S_q / S_(q+1)`

The selected observable order is the smallest q with `g_q >= 10`. No truth quantity is available to this selector. No order is selected if no candidate qualifies. A selected order at the maximum candidate value is refused because higher-order persistence cannot be checked. Any selected full-record unstable pole also causes refusal at all three layers.

## Layer A frozen rules
For positive-frequency complex poles:
- median first-half vs second-half normalized pole-set distance <= 0.03;
- median selected-order vs next-higher-order normalized pole-set distance <= 0.02;
- individual real-pole scalar values remain `REFUSE_REAL_POLE_SCALAR`.

Normalized pole distance is `|a-b| / max(|a|,|b|)`.

## Layer B frozen rules
For noncrowded modes:
- first-half vs second-half mode-shape MAC >= 0.95;
- selected-order vs next-higher-order mode-shape MAC >= 0.95.

For positive-frequency modes i,j define the crowding ratio:

`c_ij = |omega_i-omega_j| / (alpha_i+alpha_j)`, with `lambda=-alpha+i*omega`.

If `c_ij <= 1`, individual eigenvector claims are suppressed. The corresponding joint observable subspace is primary and requires:
- split-record subspace similarity >= 0.99;
- cross-order subspace similarity >= 0.99.

Layer B does not require Layer A's absolute split-pole threshold. This is deliberate so a carrier can remain identifiable while temporal scalar state changes.

## Layer C frozen representation and rules
At least two positive-frequency complex modes are required for a relational system claim.

The Layer C tuple contains:
1. effective observable order;
2. the observable subspace spanned by the selected positive-frequency modes;
3. the normalized channel-participation profile from the diagonal of that subspace projector;
4. the matrix of pairwise complex-pole separations normalized by the median pole magnitude.

No weighted average of these quantities is produced.

Prospective requirements:
- split whole-subspace similarity >= 0.98;
- cross-order whole-subspace similarity >= 0.98;
- split channel-participation total-variation distance <= 0.10;
- cross-order channel-participation total-variation distance <= 0.10;
- split normalized relational-pole-geometry distance <= 0.05;
- cross-order normalized relational-pole-geometry distance <= 0.05.

Layer C does not require Layer A's absolute pole stationarity. Therefore a coherent global timescale change may fail Layer A while preserving Layer C if modal carrier geometry and normalized inter-mode organization are conserved.

## Prospectively frozen layer-dissociation challenges
The holdout contains three explicit synthetic interventions, scored only on the 280 s record where the frozen switch occurs exactly at the midpoint.

### Global timescale switch
All complex poles are multiplied by the same positive factor while their carrier geometry is preserved.
Expected prospective pattern:
- Layer A: REFUSE, because absolute scalar poles changed;
- Layer B: ADMIT, because carriers are preserved;
- Layer C: ADMIT, because normalized inter-mode geometry and collective carrier organization are preserved.

### Observation-map switch
Latent poles are unchanged while the observation/carrier map is rotated in channel space.
Expected prospective pattern:
- Layer A: ADMIT;
- Layer B: REFUSE;
- Layer C: REFUSE.

### Structural switch
Carrier map is preserved while the relative geometry of the complex pole set changes non-uniformly.
Expected prospective pattern:
- Layer A: REFUSE;
- Layer B: ADMIT;
- Layer C: REFUSE.

### 1/f null
No finite-dimensional modal truth is supplied.
Expected prospective pattern:
- Layer A: REFUSE;
- Layer B: REFUSE;
- Layer C: REFUSE.

These are intentionally asymmetric. The purpose is to test whether the three evidential layers can disagree for principled reasons rather than being collapsed into one pass/fail surrogate.

## Stationary truth families
The holdout also includes new unseen stationary families with two, three, and four oscillatory modes, resolved-close modes, a near-degenerate pair, stronger non-normality, weak and moderate observability challenges, and a mixed complex/real system.

Truth is used only after automatic layer decisions are made. It is never passed to the selector.

## Strong observability scoring rule
A true state counts as strongly observable only for post-decision scoring if its true observable mode-shape norm is at least 0.20 of the maximum true observable mode-shape norm in that realization.

This truth criterion cannot affect the selected order or layer decision.

## Prospective pass logic
Each evidential layer receives its own PASS or FAIL. The exact numerical targets are machine-readable in `configs/frozen_rules.json`.

Only a prospectively passing layer may advance to label-blind EEG model-adequacy testing. A full scalar + modal + system neural program requires all three layers to pass. If one layer fails, the failure is preserved and the scope narrows to the layers that passed rather than borrowing certainty across layers.

## Scientific firewalls
No EEG, TDBRAIN participant table, diagnosis, phenotype, treatment response, historical neuro-spectrum coordinate, GRI outcome, damping target, whole-system chi, or preferred chi value is available to selection.

The recent GRI result does not establish a shared neural/cancer mechanism and does not justify importing any molecular coordinate into the neural analysis.

## Claim ceiling
A Phase 0C v0.2 pass supports only prospective synthetic admission of the specific observable layer(s) that pass. It does not establish EEG validity, disease separation, treatment prediction, causality, a universal stability coordinate, a whole-system scalar, or a preferred chi value.
