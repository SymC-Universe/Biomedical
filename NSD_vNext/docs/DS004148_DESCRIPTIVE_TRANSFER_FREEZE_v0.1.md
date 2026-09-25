# NSD ds004148 Independent Descriptive Transfer Freeze v0.1

Date: 24 September 2026  
Status: FROZEN BEFORE SIGNAL-DERIVED TRANSFER OUTCOME  
Maturity: P0-Q independent label-blind transfer qualification  
Program authority: SymC General Operations Manual v0.8.6  
Dataset: OpenNeuro `ds004148`, DOI `10.18112/openneuro.ds004148.v1.0.0`

## 1. Question

Which components of the already-frozen ds003775 descriptive Function/Limit pattern transport to an independent healthy acquisition source when the representation is reused without retuning?

This experiment tests descriptive transport only. It does not test modal damping, local chi, broader Chi, a whole-system scalar, diagnosis, prognosis, treatment response, or recovery.

## 2. Frozen source

The input set is exactly the D4-verified `sub-01` resting set in `ds004148_d4_resting_crosssession_v0.1.json`:

- session 1: eyes closed, eyes open;
- session 2: eyes closed, eyes open;
- session 3: eyes closed, eyes open.

All six BrainVision triplets were pinned before signal-derived transfer analysis. The D4 audit established 61 raw channels, 500 Hz, 300 s, IEEE 32-bit float, multiplexed layout, and exact source identity. The source JSON declaration of 64 channels remains a provenance anomaly and is not repaired by padding or interpolation.

## 3. Metadata firewall

Engine-visible information is limited to:

- participant identity as source identity only;
- session identity;
- recording state, eyes closed or eyes open;
- acquisition and decoding metadata required to read the raw payload;
- exact source file identities.

Questionnaire, symptom, behavioral, age, sex, anthropometric, and other participant variables do not enter feature construction, representation selection, thresholds, or interpretation in this experiment.

## 4. Frozen preprocessing and representation

### 4.1 BrainVision decoding

- read the VHDR channel definitions in source order;
- require 61 unique raw channel labels;
- require `MULTIPLEXED` orientation;
- require `IEEE_FLOAT_32` binary format;
- decode little-endian 32-bit floats;
- apply each channel's VHDR resolution multiplier;
- preserve the source unit label for provenance;
- no synthetic channels;
- no channel interpolation;
- no re-reference;
- no filtering or artifact rejection;
- no amplitude-based exclusion;
- analyze the full 300 s record.

The frozen outcome family is shape/parameterization based. Absolute amplitude is not promoted as a cross-dataset physical quantity in this pilot.

### 4.2 Welch baseline

Reuse the ds003775 frozen descriptive Welch configuration unchanged:

- 4.0 s Hann windows;
- 50% overlap;
- constant detrending;
- density scaling;
- source PSD range 1 to 45 Hz.

Raw Welch log-PSD similarity is the native/simple descriptive comparator.

### 4.3 Periodic/aperiodic candidate

Reuse the ds003775 frozen `specparam==2.0.0rc7` candidate unchanged:

- fixed aperiodic mode as the frozen candidate;
- Gaussian periodic representation;
- peak width limits 0.5 to 12.0 Hz;
- maximum 3 peaks;
- minimum peak height 0.20 log10 power;
- peak threshold 3.0;
- fit range 5 to 35 Hz.

A knee-mode fit is retained only as a sensitivity diagnostic. It cannot replace the frozen fixed-mode candidate after result inspection.

## 5. Channel and hierarchy rules

All 61 ds004148 channels remain in the per-recording result when their descriptive fits are admissible.

Cross-dataset comparison to the ds003775 P0-D reference uses exact channel-label intersection only. A missing, duplicated, or nonmatching label is never silently renamed, imputed, or treated as equivalent.

The independent hierarchy is:

`one subject -> two states -> three sessions per state -> channels nested within recordings`.

Channels are repeated measurements. They are not independent participants and are not used to manufacture population uncertainty.

## 6. Primary within-state contrasts

Only same-state cross-session comparisons are primary. For each of eyes closed and eyes open, the three frozen session pairs are:

- session 1 versus session 2;
- session 1 versus session 3;
- session 2 versus session 3.

For each pair, compute on admitted shared channels:

1. median channel log-PSD correlation;
2. median absolute aperiodic-exponent difference;
3. exact same peak-count fraction;
4. exact same zero-peak-state fraction;
5. median nearest-center difference for the first listed descriptive peak when both records contain at least one peak.

The fifth quantity is explicitly descriptive. It is not mode tracking and is not a natural-frequency estimate.

## 7. Per-recording Limit metrics

For each of the six recordings report:

1. fixed-versus-knee model-family disagreement fraction;
2. zero-peak channel fraction;
3. max-peak-count saturation fraction;
4. width-boundary-hit count per admitted channel;
5. explicit descriptive-fit refusal count and reasons.

## 8. Independent reference comparison

The committed reference is:

`atlas/reference_models/ds003775_repeat_descriptive_reference_p0d_v0.1.json`.

For each state and each predeclared metric:

- report every pair or recording value;
- report the state minimum, median, and maximum;
- compare the state median to the previously observed ds003775 minimum-to-maximum envelope;
- label the comparison `WITHIN_PREVIOUS_ENVELOPE`, `OUTSIDE_PREVIOUS_ENVELOPE`, or `REFUSED_OR_NOT_AVAILABLE`.

These labels are descriptive transport indicators, not tuned pass/fail thresholds. No overall transfer score is computed. An outside-envelope result enters the Limit Map and is not automatically treated as experimental failure.

## 9. Uncertainty and effect-size rule

This is a single-subject transfer pilot. It does not support population confidence intervals, prevalence, subject-level ICC, clinical effect sizes, or population inference.

No bootstrap or permutation distribution over channels will be presented as subject-level uncertainty. The complete pairwise values and state-level range/median are the declared uncertainty-compatible summary for this pilot.

## 10. Refusal and abort rules

The signal-derived outcome is not opened if any frozen source identity or D4 decoding contract fails.

At the descriptive layer:

- a channel fit failure emits `REF_DESCRIPTIVE_FIT` with its reason;
- a cross-dataset channel-label mismatch removes that channel only from the exact-label reference comparison and is reported;
- a pair with no admitted shared channels is refused;
- nonfinite values are refused rather than replaced;
- no post-result parameter relaxation is allowed.

## 11. Interpretation firewall

This experiment cannot license or report:

- modal poles from real EEG;
- damping or Q from descriptive bandwidth;
- local scalar chi;
- broader capital Chi as an empirical neural architecture claim;
- whole-brain/global chi;
- clinical diagnosis, screening, prognosis, or treatment guidance;
- recovery or resilience from repeat-session similarity;
- population generalization from one subject.

## 12. Pre-result decision rule

The experiment returns a metric-by-metric transfer vector and a Limit Map. It deliberately has no single success score.

The scientifically relevant outcomes are therefore:

- which frozen descriptive quantities remain inside the prior empirical envelope;
- which move outside it;
- which become non-identifiable or refused;
- whether the pattern differs between eyes-closed and eyes-open states.

Any result is retained. The ds004148 data will not be used to tune the representation subsequently claimed to have transferred to ds004148.
