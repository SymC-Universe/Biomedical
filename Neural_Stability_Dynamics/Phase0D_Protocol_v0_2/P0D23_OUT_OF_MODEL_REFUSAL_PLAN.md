# P0-D23 Deliberate Out-of-Model Refusal Challenge Plan

Date: 2026-09-14
Status: **P0-D exploratory known-truth refusal challenge. Existing development rules are reused unchanged. No threshold is tuned or promoted.**
Purpose: `LIMIT_MAPPING + ENGINE_REFUSAL`

## Question
When a stable measurement record violates the current stationary shared-dynamics comparison assumption through an abrupt mid-record structural switch, does the existing NSD Structural Engine preserve that problem as refusal/partial information rather than forcing a licensed stability or recovery prediction?

## Why this matters
A predictive Engine must know when it does not have a defensible model. Stable poles alone are not sufficient evidence that one stationary representation describes the full record. This challenge deliberately supplies a scientifically out-of-model case while leaving the existing selector rules untouched.

## Construction
Two synthetic families are generated with the existing shared-basis switch simulator:

1. `STATIONARY_CONTROL`: first-half and second-half latent generators are identical.
2. `STRUCTURAL_SWITCH`: both halves remain individually stable, but decay/frequency structure changes abruptly at the midpoint while the latent basis and observation map are shared.

Common settings:
- 8 observed channels;
- `dt = 0.01 s`;
- 4000 samples;
- fixed midpoint switch;
- fixed process-noise scale;
- deterministic replicate seeds;
- candidate SSI orders `[2, 4, 6]`;
- existing `configs/development_rules.json` used byte-for-byte for selector decisions;
- scalar, modal, and system layers evaluated separately;
- Atlas and outcomes excluded.

## Readout
For each record, preserve:
- selected local orders;
- scalar decision;
- modal decision;
- system decision;
- explicit partial/unresolved state where returned;
- whether any current layer refuses the comparison;
- a disposition field that is `REFUSE_CURRENT_MODEL` whenever a refusal is returned.

No recovery trajectory is predicted in this challenge. Even if all structural layers admit, the output remains `STRUCTURAL_OUTPUT_ONLY_NO_RECOVERY_PREDICTION`; structural admission is not silently upgraded into a recovery claim.

## Falsification logic
The workflow itself does not require the switched family to hit a preregistered refusal rate. An unexpected admission is a scientific result and must be recorded rather than hidden or repaired by threshold retuning.

The test suite checks only mechanical/scientific invariants:
- all native generators are stable;
- the structural-switch halves genuinely differ;
- stationary-control halves are identical;
- existing development rules are loaded without mutation;
- a returned refusal cannot be represented as a licensed prediction.

## Firewalls
- No selector threshold is tuned.
- No truth or condition label enters the selector.
- No P0Q1 result is rescored.
- No empirical neural, clinical, diagnostic, treatment, Atlas, preferred-chi, or chi-system claim is made.
- A failure to refuse does not trigger an automatic repair. It becomes Limit-Map evidence for the post-run audit.
