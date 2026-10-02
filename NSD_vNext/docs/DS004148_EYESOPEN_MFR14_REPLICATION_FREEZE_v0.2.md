# NSD ds004148 Eyes-Open Untouched MFR-14 Replication Freeze v0.2

Date: 25 September 2026
Status: FROZEN BEFORE V0.2 SIGNAL OUTCOMES
Maturity: P0-Q independent-subject replication within ds004148
Program authority: SymC General Operations Manual v0.8.6

## 1. Why v0.2 exists

The v0.1 replication was invalidated before cohort inference by a real source-topology assumption: the sub-01-derived 59-label coordinate set was not exact-label stable across the independent cohort. Nine of fourteen v0.1 subjects carried `Cpz` rather than `CPz` in eyes-open session3.

The failure was preserved and investigated rather than repaired by silent case normalization.

A header-only audit then verified all 180 eyes-open VHDR files across 60 subjects and three sessions. It established three 61-channel signatures and a 57-label exact cross-dataset stable space after excluding the case-variable `CPz` and `Fpz` labels.

No signal-derived outcome from the v0.2 subjects was used to derive that space.

## 2. Question

Across untouched independent ds004148 subjects, do the two eyes-open pairs involving session3 show a reproducible increase in the subject-level fraction of channels with unusually large descriptive peak displacement relative to session1-session2?

Secondary question: when high-shift channels occur, how often are they coupled to model-family instability, peak-count change, aperiodic excursion, or low PSD correlation?

## 3. Frozen cohort

Exact cohort:
`sub-16` through `sub-29`, inclusive.

Independent subject count: 14.

The cohort is frozen in:
`docs/manifests/ds004148_eyesopen_mfr14_replication_v0.2.json`.

These subjects were not used in the incomplete v0.1 signal cohort. Their headers were inspected only in the dataset-wide source/topology audit.

No replacement subject is allowed after v0.2 signal-derived outcomes open.

## 4. Frozen coordinate space

Use exactly the 57 labels in:

`docs/manifests/ds004148_eyesopen_dataset_stable57_v0.1.json`.

Those labels are:
1. exact-label present across all 180 audited ds004148 eyes-open headers; and
2. exact-label present in the previously frozen ds003775 parent space.

No case normalization, renaming, interpolation, imputation, or post-result channel substitution is allowed.

## 5. Source/D4 gate

For each subject and all three eyes-open sessions:

1. use pinned OpenNeuro commit `0c740d838a2c33feeec0b6e514aea323d0e65ca4`;
2. resolve VHDR, VMRK and EEG git-annex identities before raw download;
3. download all three payloads from the declared NEMAR mirror;
4. require exact annex byte size and MD5 for every file;
5. require 61 unique raw channels, 500 Hz, IEEE_FLOAT_32, MULTIPLEXED and 300 s / 150000 samples;
6. require all 57 frozen replication labels to be present under exact semantics.

A subject failing any gate is retained as a failure. There is no post-result replacement.

## 6. Frozen representation

Unchanged from the closed transfer/localization lineage:

- Welch 4.0 s Hann;
- 50% overlap;
- constant detrending;
- density scaling;
- 1-45 Hz source PSD;
- specparam 2.0.0rc7;
- fixed aperiodic candidate;
- Gaussian periodic representation;
- peak-width limits 0.5-12.0 Hz;
- maximum 3 peaks;
- minimum peak height 0.20 log10 power;
- peak threshold 3.0;
- fit range 5-35 Hz;
- knee model as sensitivity only.

## 7. Frozen parent reference

Rebuild the channel-specific ds003775 parent reference from the original 42 subject artifacts produced by workflow run `35337659470`, restricted prospectively to the same 57-label manifest.

No v0.2 outcome may enter parent threshold construction.

## 8. Frozen subject-level endpoints

For each subject analyze:

- session1-session2;
- session1-session3;
- session2-session3.

Per pair report:
1. eligible peak-shift channel count;
2. high-shift channel count;
3. high-shift fraction among eligible channels;
4. median descriptive peak displacement;
5. high-shift regional/hemisphere distribution;
6. within-high-shift co-occurrence with aperiodic, PSD-correlation, model-family, peak-count and zero-peak flags.

Subject is the independent unit. Channels remain nested repeated measurements.

## 9. Primary independent-subject contrasts

For each subject compute:

- high-shift fraction: session1-3 minus session1-2;
- high-shift fraction: session2-3 minus session1-2;
- median peak-displacement deltas for the same contrasts.

Across 14 subjects report every value, median/range, and positive/negative/tied counts.

For the two predeclared high-shift-fraction contrasts only:
- exact two-sided sign test on non-tied subjects;
- Holm correction across the two contrasts.

## 10. Interpretation

Replication means the dataset-local eyes-open session3 pattern is reproduced across independent subjects under the prospectively audited exact coordinate space.

Non-replication is a valid negative result and must not trigger threshold relaxation.

Even a replicated pattern does not identify cause. Candidate explanations remain state/vigilance, session order, acquisition/compliance, descriptive peak-identity instability, model-family instability, or genuine neural-state change.

## 11. Claim ceiling

This experiment cannot license:
- modal tracking;
- natural frequency;
- damping or Q;
- lowercase chi;
- capital Chi as an empirical neural architecture;
- global chi;
- recovery/resilience;
- diagnosis, prognosis or treatment;
- clinical or cross-dataset population generalization.

## 12. Checkpoint continuation

If v0.2 closes interpretable:
- continue automatically to an eyes-closed state-specificity test using a separately frozen untouched-subject design;
- preserve failures/outliers and investigate root cause before any scientific promotion.

No user prompt is required unless a genuinely new scientific decision is reached.
