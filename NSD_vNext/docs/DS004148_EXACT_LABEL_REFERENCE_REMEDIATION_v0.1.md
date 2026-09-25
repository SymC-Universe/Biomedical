# NSD ds004148 Exact-Label Reference Remediation v0.1

Date: 24 September 2026
Status: POST-RESULT MECHANICAL REMEDIATION / FIRST SUITE NOT PROMOTED
Program authority: SymC General Operations Manual v0.8.6

## What was found

The first green ds004148 descriptive-transfer workflow, run `36087919213`, correctly preserved the six frozen recordings, produced all predeclared descriptive metrics, passed the interpretation-firewall smoke test, and reported a 59-channel exact label intersection with the ds003775 reference.

The post-result audit found one implementation mismatch with the pre-result freeze. The freeze requires cross-dataset comparison to use exact channel-label intersection only. The first runner computed the ds004148 within-state summaries over all 61 available ds004148 channels and compared those summaries with the previously committed ds003775 64-channel population envelopes.

The first result is therefore retained as provenance but is not promoted as the final transfer result.

## Why this is a mechanical correction rather than a scientific retune

The rule being enforced was committed before the ds004148 signal-derived outcome was opened:

> Cross-dataset comparison to the ds003775 P0-D reference uses exact channel-label intersection only.

No threshold, model parameter, fit range, state definition, metric family, or interpretation rule is changed after result inspection.

The correction does only two things:

1. derives the ds003775 reference envelopes over the exact 59 labels shared with ds004148;
2. computes the ds004148 reference-comparison summaries over those same 59 labels.

All 61 ds004148 channels remain eligible for the dataset-local per-recording descriptive record, as required by the freeze.

## Frozen parent material reused

Parent workflow run: `35337659470`

Parent subject artifacts: 42 preserved ds003775 repeat artifacts pinned in:

`docs/manifests/ds003775_matched59_source_artifacts_v0.1.json`

Deterministic rebuild tool:

`engine/tools/build_ds003775_matched59_reference.py`

Matched reference:

`atlas/reference_models/ds003775_repeat_descriptive_reference_p0d_matched59_v0.1.json`

The matched reference contains 42 subject-level repeat comparisons and 84 recording-level Limit observations. It does not use ds004148 signal values to choose any threshold or tune any representation.

## Treatment of the global median PSD metric

The pre-result freeze declares median channel log-PSD correlation as the native/simple cross-session Welch comparator. The first suite also emitted a global median-PSD correlation inherited from an earlier ds003775 summary.

That extra quantity is not part of the exact-label reference comparison because the preserved parent subject artifacts do not contain per-channel PSD arrays needed to reconstruct an exact 59-channel global median spectrum. It is therefore removed from the promoted transfer vector rather than approximated post hoc.

No predeclared primary metric is removed.

## Promotion rule

A corrected suite must:
- use the exact 59 labels for every cross-dataset reference comparison;
- retain the 61-channel local descriptive summaries separately;
- reproduce all five frozen pair metrics and four frozen recording Limit metrics;
- preserve all interpretation firewalls;
- pass the master smoke test;
- package the matched reference and its provenance.

Only the corrected suite may supply the manuscript/reproducibility result language.

## Scientific ceiling

This remediation does not promote:
- modal damping;
- natural frequency;
- lowercase chi;
- capital Chi as an empirical neural architecture;
- a whole-brain/global scalar;
- diagnosis or screening;
- recovery or resilience;
- population generalization.

The experiment remains a one-subject, six-recording, P0-Q independent descriptive-transfer pilot.
