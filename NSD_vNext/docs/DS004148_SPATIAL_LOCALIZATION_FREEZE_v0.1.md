# NSD ds004148 Spatial/State Localization Freeze v0.1

Date: 25 September 2026
Status: FROZEN BEFORE CHANNEL-LEVEL LOCALIZATION OUTCOME
Maturity: P0-D explanatory follow-up to the closed P0-Q transfer pilot
Program authority: SymC General Operations Manual v0.8.6

## 1. Trigger

Corrected independent descriptive-transfer suite v0.2 showed one pair-level Limit Map excursion that was hidden by an in-envelope state median:

- dataset: ds004148;
- subject: sub-01;
- state: eyes open;
- pair: ses-session2 versus ses-session3;
- frozen metric: median nearest-center displacement for the first listed descriptive peak;
- observed pair median: 4.048975 Hz;
- matched ds003775 subject-level envelope maximum: 2.038390 Hz.

This follow-up is selected after that result and is therefore explanatory P0-D work. It is not untouched confirmation.

## 2. Question

Is the eyes-open session2-versus-session3 descriptive peak-location excursion:

1. spatially concentrated in a small subset of channels or distributed broadly;
2. primarily periodic, or accompanied by aperiodic/model-family instability;
3. unique to the target pair or also present in the five same-state control pairs?

No modal, damping, chi, capital-Chi, diagnostic, recovery, or population claim is tested here.

## 3. Frozen inputs

Target source remains the exact six D4-pinned recordings in:

`docs/manifests/ds004148_d4_resting_crosssession_v0.1.json`.

The frozen descriptive representation remains unchanged:
- Welch: 4.0 s Hann, 50% overlap, constant detrend, density scaling, 1-45 Hz;
- specparam 2.0.0rc7;
- fixed aperiodic candidate;
- Gaussian periodic representation;
- width limits 0.5-12.0 Hz;
- maximum 3 peaks;
- minimum peak height 0.20 log10 power;
- peak threshold 3.0;
- fit range 5-35 Hz;
- knee fit as sensitivity only.

Cross-dataset/reference localization uses the exact 59 channel labels already established in the corrected transfer suite. All 61 ds004148 channels may remain in local provenance, but no nonmatching label may be substituted into the matched analysis.

## 4. Parent channel-level reference

The parent localization reference is derived only from the original 42 ds003775 repeat-subject artifacts produced by workflow run `35337659470`.

For each of the 59 exact shared labels, derive across subjects:
- channel log-PSD correlation distribution;
- absolute aperiodic-exponent difference distribution;
- first-listed-peak nearest-center displacement distribution when both sessions contain at least one peak;
- peak-count match fraction;
- zero-peak-state match fraction;
- fixed-versus-knee disagreement fraction;
- max-peak-count frequency;
- width-boundary-hit distribution.

Quantiles are empirical linear q05, median, and q95. They are descriptive context, not population confidence bounds.

A channel-specific peak-displacement q95 is admissible only when at least 10 parent subjects contribute a peak pair. Otherwise that channel receives no thresholded localization flag.

No ds004148 value may be used to choose a parent threshold.

## 5. Pair-level channel metrics

For every same-state pair, and for each of the 59 exact labels, compute:

1. log-PSD correlation;
2. absolute aperiodic-exponent difference;
3. peak-count match;
4. zero-peak-state match;
5. nearest-center displacement from the first listed descriptive peak in the earlier session when both sessions have at least one descriptive peak;
6. fixed-versus-knee model-family disagreement state in each recording;
7. max-peak-count state in each recording;
8. width-boundary-hit state in each recording.

The five frozen same-state control pairs are retained alongside the target pair:
- eyes closed 1-2;
- eyes closed 1-3;
- eyes closed 2-3;
- eyes open 1-2;
- eyes open 1-3.

The target pair is eyes open 2-3.

## 6. Frozen localization flags

For each channel:

- `PEAK_SHIFT_HIGH`: target/pair peak displacement > that channel's ds003775 q95, with parent peak-pair n >= 10;
- `APERIODIC_DIFF_HIGH`: exponent difference > that channel's ds003775 q95;
- `PSD_CORRELATION_LOW`: log-PSD correlation < that channel's ds003775 q05;
- `MODEL_FAMILY_UNSTABLE`: fixed-versus-knee disagreement is present in either recording;
- `PEAK_COUNT_CHANGED`: frozen fixed peak count differs between the two sessions;
- `ZERO_PEAK_STATE_CHANGED`: zero-peak state differs between the two sessions.

These flags do not constitute hypothesis-test p-values.

## 7. Frozen spatial map

Channel regions are assigned from labels before outcome inspection:

- frontal/anterior: Fp*, AF*, F*, FC*;
- temporal: FT*, T*, TP*;
- central: C*, CP*;
- posterior: P*, PO*, O*.

Prefix matching uses the most specific listed prefix first so FT is temporal, not frontal.

Hemisphere is label-derived:
- trailing odd number = left;
- trailing even number = right;
- trailing z = midline.

No coordinate interpolation, adjacency graph, or source localization is invented.

## 8. Required outputs

For every same-state pair report:
- eligible peak-shift channel count;
- number and fraction of eligible channels with `PEAK_SHIFT_HIGH`;
- region and hemisphere counts for eligible and high-shift channels;
- median peak displacement by region;
- complete channel-level table;
- top ten channels by peak-displacement/q95 ratio where q95 is admissible.

For the target eyes-open 2-3 pair additionally report:
- overlap of `PEAK_SHIFT_HIGH` with aperiodic, PSD-correlation, model-family, peak-count, and zero-peak flags;
- whether high-shift channels are confined to one region, span multiple regions, or are distributed across the scalp, expressed as counts rather than a post-hoc binary threshold;
- comparison with the five same-state control pairs.

## 9. Interpretation rule

A periodic-position excursion may be described as relatively isolated only if high-shift channels do not systematically co-occur with aperiodic/model-family/PSD instability. It may be described as representation-coupled only when those co-occurrences are visible in the channel-level record.

Neither description licenses a physical neural mode, natural frequency, damping rate, local chi, or capital Chi.

## 10. Failure and outlier handling

Any decoding, source-identity, fit, or reference failure is preserved and investigated for root cause.

A channel-level extreme is not discarded. It remains in the Limit Map and is checked against:
- parent channel-specific context;
- model-family disagreement;
- peak-count/zero-peak transitions;
- the five same-state control pairs.

No parameter relaxation is allowed after outcome inspection.

## 11. Checkpoint continuation

When this localization closes:
- if the result is interpretable under the frozen descriptive layer, execution continues automatically to untouched-subject replication within ds004148;
- if the result is non-identifiable or dominated by a mechanical/model-family defect, that failure is investigated and repaired or classified before continuation;
- user prompting is not required unless a new scientific decision is reached.
