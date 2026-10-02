# NSD next science freeze packet v0.1

Date: 22 September 2026  
Status: SCIENTIFIC DECISIONS REQUIRED BEFORE NEXT OUTCOME-BEARING LANES  
Program authority: SymC General Operations Manual v0.8.3

## Purpose

Mechanical/source work has now advanced far enough that the next bottlenecks are scientific rather than operational.

This packet separates three decisions that should be frozen before their next outcome-bearing executions:
1. ds005385 adult Function/Limit representation under unreliable EDF physical calibration;
2. production nonstationarity/refusal logic for the modal Engine;
3. second standard-toolkit comparator design after the first SOMATA lane exposed a resampling confound and no zero-oscillator comparator.

Nothing in this packet authorizes a real-EEG local chi.

---

## Decision A: ds005385 Function/Limit representation

### Earned facts

- D3 metadata roles are closed.
- A prospectively selected repeat subject passed exact D4 structure across 8/8 session x state x pre/post recordings.
- The source explicitly warns EDF physical min/max can be invalid.
- Physical min/max have therefore not been used for amplitude scaling.
- Source payload duration is not exactly constant across recordings.

### Scientific question

What representation may legitimately be compared across eyes-open/eyes-closed, pre/post cognitive block, and five-year repeat when absolute voltage calibration is not trusted?

### A1. Within-record standardized spectral shape only
For each channel/recording:
- operate on digital signal after defensible offset handling;
- standardize within recording/channel;
- compare normalized PSD shape, peak location/state, spectral entropy-like descriptors, and other scale-invariant quantities;
- prohibit absolute power/amplitude claims.

Advantage:
cleanest use of the raw signal without inventing physical calibration.

Limitation:
cannot address absolute amplitude/power organization and may erase biologically meaningful amplitude differences.

### A2. Rank/relative spatial-spectral organization
Retain only quantities invariant to positive linear scale:
- within-record channel ranks;
- relative band fractions;
- normalized topographic distributions;
- correlation/coherence-like normalized structure where estimator assumptions are met.

Advantage:
targets broader spatial/system organization without depending on volts.

Limitation:
relative measures can become compositional and must not be interpreted as absolute gain/loss.

### A3. A1 + A2 as coequal Function/Limit tracks
Use spectral shape and relative spatial organization as separate, coequal representations.

This avoids forcing one compression to stand for the full system and directly tests whether conclusions survive representation changes.

### A4. Hold ds005385 until calibration can be independently recovered
Do not use signal-derived ds005385 results until a trustworthy calibration route is found.

### Recommended discussion target
A3 is the strongest low-risk design for the current GOM question because it preserves both local spectral organization and broader spatial organization while refusing unsupported absolute amplitude. It is not frozen until approved.

### Required freeze details
- digital offset/detrending rule;
- standardization rule;
- Welch/parameterization reuse versus a new version;
- channel/region aggregation;
- subject/session hierarchy;
- handling of late-trigger source warnings;
- primary contrasts;
- native/simple comparator;
- uncertainty/effect-size metrics;
- whether age is downstream descriptive covariate only or part of a separately frozen lifespan task.

---

## Decision B: nonstationarity/refusal qualification

### Earned facts

The existing P0-Q stationarity challenge shows:
- a whole-record A2 can be produced by a frequency shift rather than two simultaneous stationary modes;
- a whole-record A1 can hide a large damping shift;
- finite bursts/amplitude occupancy can remain A1.

Split-window modal disagreement and local RMS occupancy are informative diagnostic channels.

No production threshold was selected from those viewed examples.

### Scientific question

How should the Engine prospectively refuse a stationary modal interpretation when temporal consistency is inadequate?

### B1. Fixed diagnostic thresholds from independent known-truth validation
Before seeing a new validation grid:
- define candidate diagnostics;
- generate a separate known-truth grid with stationary and nonstationary families;
- freeze loss/cost structure;
- choose threshold only inside qualification;
- then lock the rule before real EEG.

### B2. Probabilistic model competition
Explicitly add stationary versus time-varying/switching alternatives and base refusal on held-out likelihood/uncertainty rather than hand thresholds.

Advantage:
closer to the actual generative question.

Cost:
substantially more model complexity and another comparator/prior-art lane.

### B3. Conservative conjunction
Require:
- stationary A0/A1/A2 adequacy;
- plus a separately qualified temporal-consistency gate;
- otherwise emit `REF_NONSTATIONARY`.

This keeps the current stationary Engine and adds refusal rather than making it absorb every process.

### Recommended discussion target
B3, with B1 used to qualify its threshold construction, is the smallest extension consistent with the current failure map. It preserves the existing stationary model and makes nonstationarity a refusal state instead of another forced stationary mode.

No thresholds may be chosen from the already-viewed challenge rows.

---

## Decision C: second standard-toolkit comparator

### Earned facts

First SOMATA iOsc comparator:
- agreed with NSD on several one/two-mode truths;
- disagreed on some close/nonstationary cases;
- had no zero-oscillator candidate;
- required 120 Hz resampling;
- resampling itself changed NSD behavior for some stochastic controls.

The first lane therefore cannot answer zero-vs-oscillator adequacy or cleanly separate method differences from sampling effects.

### C1. Native-120-Hz truth generation + explicit nonoscillatory comparator
Generate the same frozen truth families directly at 120 Hz, avoiding resampling.

Comparator suite:
- SOMATA oscillator search for oscillator-count/modal recovery;
- a standard AR/nonoscillatory model family for zero-vs-oscillator competition under the same native 120 Hz data.

### C2. Native-rate dual-suite
Run two prospectively frozen source grids:
- native 120 Hz for SOMATA fairness;
- native 256 Hz for existing NSD qualification continuity.

Treat sampling rate as an explicit experimental factor rather than trying to make one rate represent both.

### C3. Switch to a toolkit family that natively contains oscillatory and nonoscillatory alternatives
Use a standard state-space family capable of both, if a fair public implementation and task mapping can be pinned.

### Recommended discussion target
C2 is the cleanest diagnosis of the sampling issue. It tests whether conclusions are method-dependent or sampling-dependent without pretending resampling is neutral.

The zero-oscillator gap still needs an explicit standard nonoscillatory baseline within each comparable task.

---

## Decision D: independent healthy transfer

The mechanical preparation lane is already proceeding on OpenNeuro ds004148.

Current status:
- 60 subjects;
- 3 sessions;
- 5 states/session;
- 900 recordings;
- D4 pilot raw payload resolves to 61 channels at 500 Hz and 300 s;
- BIDS JSON's 64-channel declaration is a source metadata error relative to raw VHDR/binary and channels.tsv;
- no signal-derived NSD result has been opened.

A six-recording resting-state D4 expansion across all 3 sessions x eyes-open/eyes-closed is currently the next mechanical gate.

After that passes, the scientific transfer claim still needs a freeze.

Candidate transfer questions include:
- reproducibility of descriptive spectral Function/Limit structure;
- preservation of refusal/absence states;
- transfer of a future modal admission rule only after that rule is frozen;
- local-versus-broader organization without a whole-system scalar.

Do not use ds004148 to tune the rule intended to be tested on it.

---

## Stop line

The following remain unauthorized until the relevant decisions above are frozen:

- real-EEG modal damping;
- real-EEG local scalar chi;
- any whole-brain/global chi;
- diagnostic or disorder inference;
- threshold selection from ds004148;
- using ds005385 absolute voltage/power as calibrated physical amplitude;
- calling agreement between NSD and another toolkit validation by consensus.

Mechanical source/provenance/D4 work may continue.
