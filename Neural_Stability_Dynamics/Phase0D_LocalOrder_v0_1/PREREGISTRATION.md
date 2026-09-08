# Phase 0D v0.1 Preregistration

## Status

Prospective synthetic holdout. Do not execute during development or modify after first scientific execution.

## Fixed estimator family

Multichannel output-only SSI-COV with candidate state orders `[2,4,6,8,10,12,14,16]`.

Each full record, first half, and second half selects observable order independently using the smallest singular-value gap >= 10. A selected order at the candidate-grid maximum is refused for that local segment. Unstable selected poles are refused.

## Layer A

- scalar split median normalized pole distance <= 0.03
- local selected-to-next-order median normalized pole distance <= 0.02 in each half
- real-pole scalar interpretation refused

## Layer B

- individual carrier split MAC >= 0.95
- individual local cross-order MAC >= 0.95
- crowding ratio <= 1.0 invokes subspace-only treatment
- crowded split subspace similarity >= 0.99
- crowded local cross-order subspace similarity >= 0.99
- carrier assignment uses MAC/subspace, not pole proximity

## Layer C

- at least one positive complex observable mode is sufficient to test carrier organization
- split whole-subspace similarity >= 0.98
- local cross-order whole-subspace similarity >= 0.98
- split channel-participation TV <= 0.10
- local cross-order channel-participation TV <= 0.10
- resolved-cluster relational geometry distance <= 0.05
- if fewer than two resolved clusters remain after crowding collapse, relational geometry is `UNRESOLVED_NOT_FAILURE`
- cluster-count/signature change is system reorganization and is refused

## Holdout families

Stationary families include separated 3- and 4-mode systems, resolved-close modes, near-degenerate modes, non-normal dynamics, weak and moderate fourth-mode observability, a single complex mode, and a mixed complex/real system.

Layer-dissociation challenges are scored only at N=30000, where the switch is exactly at the half-record boundary:

- global timescale switch: expected scalar REFUSE, modal ADMIT, system ADMIT
- observation-map switch: expected scalar ADMIT, modal REFUSE, system REFUSE
- structural relative-spectrum switch: expected scalar REFUSE, modal ADMIT, system REFUSE
- resolved-to-crowded transition: expected scalar REFUSE, modal ADMIT, system REFUSE

Two 1/f null families are scored at all durations and must be refused by all layers.

## Admission targets

Stationary admission >= 0.90 per scored layer. Strong complex scalar coverage >= 0.90. Modal truth coverage >= 0.90. Crowded truth coverage >= 0.90. Spurious admitted complex mode rate <= 0.05. Pole/frequency/decay accuracy and MAC/subspace/system metrics are frozen in `configs/frozen_rules.json`.

Exact equality between selected order and synthetic strong-state count is diagnostic only, not an admission gate. Phase 0C showed that practical identifiability can be lower than latent/strong state count while recovered modes remain precise and non-spurious.

Each layer challenge must meet its frozen expected-behavior rate. Mechanical failures must be zero.

## Promotion rule

Only prospectively passing layers may enter label-blind EEG adequacy. A failed layer is preserved and is not retuned on this holdout.
