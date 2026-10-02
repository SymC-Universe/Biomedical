# NSD ds004148 Independent Descriptive Transfer Post-Result v0.2

Date: 24 September 2026
Status: P0-Q CLOSED / CORRECTED EXACT-LABEL SUITE PASSED
Program authority: SymC General Operations Manual v0.8.6
Dataset: OpenNeuro ds004148 v1.0.0
Target subject: sub-01
Corrected workflow run: 36088323374
Suite artifact: nsd-ds004148-descriptive-transfer-suite-v0-2
Artifact digest: sha256:f6ce93029c38d72016c2bfd17f4e1b7bdc74bdc5d3ac0fac780896052bf170ce

## Status

The independent descriptive-transfer pilot is mechanically closed at P0-Q.

The promoted result is suite v0.2, not the first v0.1 suite. The v0.1 run passed its own smoke test but was withheld during post-result audit because it compared 61-channel ds004148 summaries with 64-channel ds003775 envelopes despite the prospective freeze requiring exact-label intersection. The correction used the original 42 ds003775 subject artifacts to derive a deterministic 59-label matched parent envelope. No target-derived threshold or representation parameter was introduced.

## What happened

The corrected suite reused the frozen ds003775 Welch and periodic/aperiodic representation without retuning on six D4-pinned ds004148 resting recordings:

- three eyes-closed sessions;
- three eyes-open sessions;
- one independent subject;
- 61 raw ds004148 channels retained in the local descriptive record;
- 59 exact channel labels used for every cross-dataset comparison.

For each state, all five frozen cross-session pair metrics and all four frozen recording-level Limit metrics produced state medians inside the matched ds003775 empirical minimum-to-maximum envelopes.

### Eyes closed state medians

| Metric | ds004148 median | matched ds003775 envelope | Transport label |
| --- | ---: | ---: | --- |
| Median channel log-PSD correlation | 0.979606 | 0.634756 to 0.990470 | WITHIN_PREVIOUS_ENVELOPE |
| Median absolute aperiodic-exponent difference | 0.099769 | 0.091766 to 1.463547 | WITHIN_PREVIOUS_ENVELOPE |
| Same peak-count fraction | 0.440678 | 0.220339 to 0.881356 | WITHIN_PREVIOUS_ENVELOPE |
| Same zero-peak-state fraction | 0.762712 | 0.440678 to 1.000000 | WITHIN_PREVIOUS_ENVELOPE |
| Median nearest-center difference, first listed descriptive peak | 0.423698 Hz | 0.039168 to 2.038390 Hz | WITHIN_PREVIOUS_ENVELOPE |
| Fixed-versus-knee disagreement fraction | 0.203390 | 0.118644 to 0.949153 | WITHIN_PREVIOUS_ENVELOPE |
| Max-peak-count fraction | 0.152542 | 0.000000 to 0.525424 | WITHIN_PREVIOUS_ENVELOPE |
| Zero-peak fraction | 0.118644 | 0.000000 to 0.627119 | WITHIN_PREVIOUS_ENVELOPE |
| Width-boundary hits per channel | 0.000000 | 0.000000 to 0.305085 | WITHIN_PREVIOUS_ENVELOPE |

### Eyes open state medians

| Metric | ds004148 median | matched ds003775 envelope | Transport label |
| --- | ---: | ---: | --- |
| Median channel log-PSD correlation | 0.952450 | 0.634756 to 0.990470 | WITHIN_PREVIOUS_ENVELOPE |
| Median absolute aperiodic-exponent difference | 0.248222 | 0.091766 to 1.463547 | WITHIN_PREVIOUS_ENVELOPE |
| Same peak-count fraction | 0.355932 | 0.220339 to 0.881356 | WITHIN_PREVIOUS_ENVELOPE |
| Same zero-peak-state fraction | 0.610169 | 0.440678 to 1.000000 | WITHIN_PREVIOUS_ENVELOPE |
| Median nearest-center difference, first listed descriptive peak | 1.816834 Hz | 0.039168 to 2.038390 Hz | WITHIN_PREVIOUS_ENVELOPE |
| Fixed-versus-knee disagreement fraction | 0.389831 | 0.118644 to 0.949153 | WITHIN_PREVIOUS_ENVELOPE |
| Max-peak-count fraction | 0.033898 | 0.000000 to 0.525424 | WITHIN_PREVIOUS_ENVELOPE |
| Zero-peak fraction | 0.338983 | 0.000000 to 0.627119 | WITHIN_PREVIOUS_ENVELOPE |
| Width-boundary hits per channel | 0.016949 | 0.000000 to 0.305085 | WITHIN_PREVIOUS_ENVELOPE |

## Limit Map

State-median transport does not erase pair-level excursions.

Two of the six same-state session pairs produced one metric outside its matched parent envelope:

1. Eyes closed, session 1 versus session 2: median absolute aperiodic-exponent difference = 0.084240, below the matched ds003775 minimum of 0.091766.
2. Eyes open, session 2 versus session 3: median nearest-center difference for the first listed descriptive peak = 4.048975 Hz, above the matched ds003775 maximum of 2.038390 Hz.

The first excursion indicates stronger exponent agreement than any parent subject in the matched 42-subject sample. It is not evidence of failure.

The second excursion is a substantive descriptive instability in the first-listed-peak location for that session pair. It is not mode tracking, a natural-frequency change, or evidence of altered damping. It remains a Limit Map observation for follow-up.

No recording-level Limit metric produced an individual-session value outside its matched parent envelope.

## Why it matters

The result supports a narrow transport statement: the frozen ds003775 descriptive Function/Limit representation remains usable on an independent acquisition source without retuning, and its state-level summaries remain inside the previously observed matched-label healthy envelopes for this one ds004148 subject.

The result does not establish population generality. There is only one independent ds004148 subject, and sessions and channels are repeated measurements rather than independent participants.

The difference between states is also descriptive rather than inferential. Eyes-open recordings show lower median channel log-PSD repeat correlation, lower zero-peak-state agreement, higher exponent difference, and a larger nearest-first-peak displacement than eyes-closed recordings, but no population-level state effect is licensed from one subject.

## Claim ceiling

This experiment does not license:
- real-EEG modal damping;
- damping ratios or Q;
- natural-frequency estimates from descriptive peak centers;
- lowercase chi;
- capital Chi as an empirically reconstructed neural architecture;
- a whole-brain or global chi scalar;
- diagnosis, screening, prognosis, or treatment guidance;
- recovery or resilience from session repeatability;
- population confidence intervals or prevalence claims.

## Reproducibility closure

Corrected workflow run: `36088323374`

Artifact:
`nsd-ds004148-descriptive-transfer-suite-v0-2`

Artifact digest:
`sha256:f6ce93029c38d72016c2bfd17f4e1b7bdc74bdc5d3ac0fac780896052bf170ce`

The suite contains:
- prospective freeze;
- exact-label remediation record;
- D4 source manifest;
- original ds003775 P0-D reference;
- 59-label matched reference;
- 42-artifact source provenance manifest;
- deterministic matched-reference builder;
- corrected transfer runner;
- pinned dependency declaration;
- machine-readable result;
- verification summary;
- exact run command;
- SHA-256 ledger.

Raw EEG payloads are not redistributed in the suite.

## What happens next

The next scientific move should not be another scalar promotion. The strongest unresolved signal in this pilot is the state-dependent and session-dependent periodic/aperiodic descriptive structure, especially the eyes-open session 2 versus session 3 peak-location excursion.

The next experiment should therefore test whether that excursion reflects:
1. a localized channel subset versus a broad spatial reorganization;
2. a periodic component shift versus aperiodic/model-family instability;
3. a stable state-specific pattern across additional independent subjects rather than a one-subject session anomaly.

That next experiment must remain descriptive until an admitted modal estimator exists. Lowercase chi and broader capital Chi stay behind the current stop line.
