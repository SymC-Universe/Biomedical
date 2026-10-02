# NSD ds004148 Eyes-Open Untouched MFR-14 Replication Freeze v0.1

Date: 25 September 2026
Status: FROZEN BEFORE UNTOUCHED SUBJECT SIGNAL OUTCOMES
Maturity: P0-Q independent-subject replication within ds004148
Program authority: SymC General Operations Manual v0.8.6

## 1. Trigger

The sub-01 explanatory localization showed that the previously flagged eyes-open session2-versus-session3 excursion is better described as a session-3 pattern:

- eyes open session1-session2: 8/35 eligible channels above channel-specific parent q95 = 0.2286;
- eyes open session1-session3: 10/19 = 0.5263;
- eyes open session2-session3: 11/21 = 0.5238.

The same localization showed that high-shift channels are frequently, but not universally, accompanied by fixed-versus-knee model-family disagreement.

These observations were made only in sub-01. They cannot support a subject-level generalization.

## 2. Question

Across untouched independent ds004148 subjects, do the two eyes-open pairs involving session3 show a reproducible increase in the subject-level fraction of channels with unusually large descriptive peak displacement relative to session1-session2?

Secondary question: when high-shift channels occur, how often are they coupled to model-family instability, peak-count change, aperiodic excursion, or low PSD correlation?

## 3. Frozen cohort

The exact cohort is committed in:

`docs/manifests/ds004148_eyesopen_mfr14_replication_v0.1.json`.

Primary subjects:
`sub-02` through `sub-15`, inclusive.

This supplies 14 independent subjects, meeting the current MFR-14 floor for this replication rung.

No replacement subject is allowed after signal-derived outcome inspection. If any primary subject fails D4/source integrity, the MFR-14 replication is incomplete and the failure is investigated rather than silently replaced.

## 4. Frozen source and D4 gate

For each subject and each of sessions 1, 2 and 3:

1. use the pinned OpenNeuro commit `0c740d838a2c33feeec0b6e514aea323d0e65ca4`;
2. resolve the EEG git-annex key from that pinned commit before raw download;
3. parse expected byte size and MD5 from the annex key;
4. obtain VHDR and VMRK from the same pinned commit;
5. download the EEG payload from the declared NEMAR mirror;
6. require exact size and MD5;
7. require 61 unique raw channels, 500 Hz, IEEE_FLOAT_32, MULTIPLEXED layout and 300 s / 150000 samples.

Signal-derived feature extraction does not begin for a recording until these checks pass.

Any failure is retained and investigated for root cause. There is no post-result subject substitution.

## 5. Frozen representation

Reuse the exact descriptive representation used in the closed transfer/localization chain:

- Welch 4.0 s Hann, 50% overlap, constant detrend, density scaling, 1-45 Hz;
- specparam 2.0.0rc7;
- fixed aperiodic candidate;
- Gaussian periodic representation;
- peak widths 0.5-12.0 Hz;
- maximum 3 peaks;
- minimum peak height 0.20 log10 power;
- peak threshold 3.0;
- fit range 5-35 Hz;
- knee model as sensitivity only.

No subject in the replication may alter these settings.

## 6. Frozen parent reference

Rebuild the 59-label channel-specific ds003775 parent reference from the original 42 subject artifacts produced by workflow run `35337659470`, using:

`engine/tools/build_ds003775_channel_localization_reference.py`.

The reference is built without access to any replication outcome.

## 7. Frozen subject-level endpoints

For each subject, analyze all three eyes-open same-state pairs:

- session1-session2;
- session1-session3;
- session2-session3.

For each pair report:

1. eligible peak-shift channel count;
2. number and fraction of eligible channels with `PEAK_SHIFT_HIGH`;
3. median descriptive peak displacement;
4. high-shift regional/hemisphere distribution;
5. within-high-shift co-occurrence with:
   - `APERIODIC_DIFF_HIGH`;
   - `PSD_CORRELATION_LOW`;
   - `MODEL_FAMILY_UNSTABLE`;
   - `PEAK_COUNT_CHANGED`;
   - `ZERO_PEAK_STATE_CHANGED`.

Channels remain repeated measurements. Subject is the independent unit.

## 8. Primary independent-subject contrasts

For each subject compute:

- high-shift fraction delta: session1-3 minus session1-2;
- high-shift fraction delta: session2-3 minus session1-2;
- median peak-displacement delta for the same two comparisons.

Across the 14 subjects report:
- all subject-level values;
- median and range for each pair;
- median paired deltas;
- positive / negative / tied subject counts.

For the two high-shift-fraction contrasts only, perform an exact two-sided sign test on non-tied subjects against 0.5. Apply Holm correction across the two predeclared contrasts.

These tests use subject as N. Channels do not create inferential sample size.

## 9. Interpretation

Evidence that session3 pairs tend to exceed session1-session2 at the subject level supports replication of a dataset-local eyes-open session pattern. It does not establish why the pattern occurs.

A replicated pattern remains compatible with multiple explanations, including:
- state/vigilance change;
- session-order effect;
- state-specific acquisition or compliance differences;
- descriptive peak-identity/model-family instability;
- genuine neural-state change.

Those explanations require later discrimination.

Failure to replicate is retained as a valid negative result and triggers root-cause/outlier investigation rather than threshold adjustment.

## 10. Claim ceiling

This experiment cannot license:
- neural modal tracking;
- natural frequency;
- damping or Q;
- lowercase chi;
- capital Chi as an empirical neural architecture;
- global chi;
- recovery or resilience;
- diagnosis, prognosis, or treatment guidance;
- cross-dataset or clinical population generalization.

## 11. Checkpoint continuation

After this replication closes:

- if the session3 eyes-open pattern is reproduced across independent subjects, continue automatically to the state-specificity test using eyes-closed recordings from a prospectively frozen independent-subject design;
- if it does not reproduce, investigate subject-level failures/outliers and source/model causes before the next experiment;
- no user prompt is required unless the evidence creates a genuinely new scientific choice.
