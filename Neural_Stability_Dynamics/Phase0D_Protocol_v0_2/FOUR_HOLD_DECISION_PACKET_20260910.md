# NSD Four-Hold Decision Packet

Date: 2026-09-10
Status: **P0 EVIDENCE-BASED PROPOSAL FOR SCIENCE REVIEW. NOT P1-FROZEN.**

This packet resolves the previous evidence vacuum around the four P1 scientific holds without pretending that evidence review itself constitutes a preregistered decision. It preserves General Protocol v0.7.1 and the existing NSD Scientific Contract.

## Hold 1: strongest fair native comparator

### Proposed P1 method-scope comparison

For known-truth multichannel stochastic systems within the declared local-linear/output-only validity regime, compare NSD SSI-COV structural recovery against **Dynamic Mode Decomposition (DMD)** as the primary independent structural/modal comparator.

Why DMD is currently the strongest fair candidate:

- it is an established reduced-order state-space/eigenmode method;
- it has explicit neural applications on large-scale recordings;
- a peer-reviewed EEG system-identification study directly compared DMD with output-only modal analysis;
- it addresses spatiotemporal modal structure rather than only spectra or connectivity;
- it is algorithmically distinct enough from SSI-COV to provide a meaningful comparator.

Not proposed for synthetic P1 as the primary comparator:

- specparam/FOOOF: spectral-state comparator, different object;
- PLI/wPLI: connectivity comparator, different object;
- OMA/SSI family: important neural-domain precedent but too close to the NSD estimator lineage to be the only independent comparator.

**Review disposition proposed:** `COMPARATOR_IDENTIFIED_DMD`, contingent on freezing an identical known-truth target set and scoring rule for both methods.

## Hold 2: model adequacy

No single adequacy statistic is sufficient. The proposed architecture is a conjunctive/open-channel panel with independent statuses:

1. **innovation/residual whiteness**: test for remaining temporal dependence after fitting;
2. **out-of-sample predictive reconstruction**: fit on one portion and quantify prediction/reconstruction on untouched samples;
3. **stability/physical admissibility**: reject unstable identified dynamics when stability is required by the synthetic truth family;
4. **order/window sensitivity**: report whether admitted quantities survive reasonable predeclared identification orders/windows;
5. **residual covariance/structure exposure**: preserve residual summaries rather than converting them into a hidden pass score.

A model may therefore be numerically stable yet model-inadequate. A high reconstruction score may coexist with structured residuals and must not override that contradiction.

**Review disposition proposed:** add a first-class `MODEL_ADEQUACY` object with `ADMIT`, `REFUSE`, and `INDETERMINATE` substatuses; do not reduce all diagnostics to a weighted aggregate.

## Hold 3: estimator uncertainty and INDETERMINATE

The leading method-native route is the published first-order SSI-COV covariance/sensitivity framework for poles, frequencies, damping and mode shapes. Because its validation lineage is mechanical/structural rather than EEG, the proposal is deliberately two-stage:

- **primary estimator uncertainty candidate:** first-order SSI-COV uncertainty propagation;
- **independent P0 calibration check:** known-truth Monte Carlo / replicate coverage and disagreement analysis on synthetic systems.

The P1 decision rule should not use an invented fixed gray-zone width. Instead, `INDETERMINATE` should be triggered when the uncertainty object for the claimed quantity materially spans incompatible adjudication states, or when the estimator/model-order ambiguity prevents a unique admissible structural assignment.

Exact confidence level, simultaneous-vs-marginal coverage rule, replicate count and multiplicity treatment remain to be frozen only after implementation/calibration on P0 development systems.

**Review disposition proposed:** `UNCERTAINTY_ROUTE_IDENTIFIED_NOT_CALIBRATED`.

## Hold 4: unequal-order shared/added/lost modes

Established stabilization-diagram modal analysis provides a defensible precedent for identifying recurring physical modes across models of different order. Therefore unequal local observable order should not automatically erase every shared structural claim.

Proposed decomposition:

- `SHARED_MODE`: assignment supported across segments/orders;
- `ADDED_MODE`: supported only in the later/higher-order segment;
- `LOST_MODE`: supported only in the earlier/higher-order segment;
- `AMBIGUOUS_MODE_ASSIGNMENT`: several assignments remain compatible;
- `ORDER_CHANGE_UNRESOLVED`: order changes but no assignment survives the uncertainty/crowding rules.

For crowded modes, matching must occur at the invariant-subspace/cluster level rather than forcing unstable individual eigenvectors. Scalar claims may be made only for actually matched shared poles. Added/lost structure remains an open-channel/system-reorganization output rather than being zero-filled or averaged away.

Exact matching cost, thresholds and uncertainty-aware assignment rule are **not** frozen here.

**Review disposition proposed:** permit P0 implementation and qualification of unequal-order tracking; keep production behavior fail-closed until known-bad and known-truth tests pass.

## Consequence for the next code milestone

The next safe implementation work, before P1 freeze, is:

1. implement DMD behind the same synthetic input/target firewall;
2. implement first-class residual/innovation and out-of-sample adequacy outputs;
3. implement an uncertainty API that can carry covariance/interval/status information without yet fixing confidence thresholds;
4. implement shared/added/lost/ambiguous mode tracking as P0-only behavior;
5. add known-bad tests showing each new gate can fail;
6. run only P0 development/calibration systems;
7. perform a milestone audit;
8. only then freeze MFR-14, thresholds, P1 seed, P1 challenge matrix and frozen manifest.

Until that audit, **P1 remains closed and Phase 0D v0.1 remains untouched/superseded-before-execution.**
