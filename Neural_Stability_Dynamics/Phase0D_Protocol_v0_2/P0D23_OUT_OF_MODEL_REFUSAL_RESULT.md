# P0-D23 Deliberate Out-of-Model Refusal Challenge Result

Date: 2026-09-14
Status: **P0-D exploratory known-truth refusal result. Not confirmatory. P1 remains closed.**
Governing interpretation: General Protocol v0.8.0, with the run itself executed under the then-current v0.7.7 construction.

## Execution identity

- GitHub Actions run: `34807746382`
- Artifact ID: `10333577281`
- Downloaded artifact SHA-256: `f498149490f3a36bce63e5708ed7de90f23312a4e1686d059646e1b08809d2db`
- Scientific JSON: `out_of_model_refusal_v1.json`
- Scientific JSON SHA-256: `ef9405f0e9b2e5833d8d4fe82bfcb43febf7b0f73ac5972bda3d1e17fc7624c2`
- Environment JSON SHA-256: `07fce4cb6553ee33132f5519f6459eba2523ce2e38c354ef85f17db2db98d75d`
- Workflow/process result: completed successfully.

## Construction preserved

The existing `configs/development_rules.json` was reused without threshold tuning. Eight stationary-control records and eight stable midpoint structural-switch records were generated. Scalar, modal, and system layers were evaluated separately. No Atlas, clinical outcome, preferred chi value, or recovery prediction entered the selector.

## Aggregate result

The Structural Engine produced `REFUSE_CURRENT_MODEL` for all eight `STRUCTURAL_SWITCH` records. Six switched records returned no admissible order at all, while two returned explicit order-change refusals across scalar, modal, and system layers. No switched record produced a recovery prediction.

However, the stationary control also produced `REFUSE_CURRENT_MODEL` for all eight records. Seven controls returned no admissible order across scalar, modal, and system layers. One control admitted modal structure and system organization but still refused the scalar layer as nonstationary, so the overall disposition remained refusal. No control produced a recovery prediction.

The decisive descriptive counts are therefore:

- `STRUCTURAL_SWITCH`: 8/8 current-model refusals;
- `STATIONARY_CONTROL`: 8/8 current-model refusals;
- switched modal/system refusal: 8/8;
- control modal/system refusal: 7/8;
- scalar refusal: 8/8 in both families.

## Scientific interpretation

The positive part of the challenge is real: the current Engine did not force a licensed structural/recovery interpretation onto the deliberately switched out-of-model records, and it never silently upgraded structural output into a recovery prediction.

But **this run does not establish discriminating refusal behavior**, because refusal was also universal in the stationary control under this construction. The current test therefore reveals a Limit-Map problem: the existing refusal/admission machinery is conservative enough to reject the target out-of-model family, but on this known-truth design it also rejects the nominal control family too often to support a claim that refusal specifically detects the structural switch.

This is a scientific/method result, not a mechanical defect. The protocol forbids repairing it by post-hoc threshold tuning against these outcomes.

## Consequence

P0-D23 closes one risk and opens another:

1. **Closed risk:** the tested out-of-model structural switch was not converted into an unsupported recovery prediction.
2. **Open qualification problem:** current admission/refusal specificity is inadequate in this known-truth construction because nominal controls are also refused.

Before refusal can become a claim-specific P0-Q object, the project must define what refusal is supposed to discriminate and qualify that definition on known-truth/calibration evidence without converting this P0-D outcome into confirmatory evidence. A future version may be developed in P0-Q, but the P0-D23 controls cannot later be presented as untouched proof of that revised version.

## Nonclaims and firewalls preserved

- No refusal-rate threshold is frozen.
- No selector threshold is retuned.
- No EEG, clinical, diagnostic, treatment, Atlas-zone, preferred-chi, or `chi_system` claim is made.
- No recovery prediction is licensed by this run.
- The universal control refusal is preserved rather than hidden behind the successful switched-family refusals.
