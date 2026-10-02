# NSD state-space stationarity challenge post-result audit v0.1

Date: 22 September 2026  
Status: COMPLETE P0-Q STATIONARITY/INTERMITTENCY MAP  
Program authority: SymC General Operations Manual v0.8.3  
Workflow: `NSD State-Space Stationarity Challenge`  
Run: `35758951850`  
Artifact: `nsd-state-space-stationarity-v0-1`  
Artifact ID: `10709971910`  
Artifact ZIP SHA-256: `c9bfe7c9cd602f27232d5f5adc18516c2f2aaf23c7047a7fd1039a4aa5a3a12e`

## Purpose

Test whether whole-record model order alone can be supplemented by temporal-consistency and occupancy diagnostics without changing the frozen A0/A1/A2 model family.

No production threshold was frozen.

## Stationary controls

### Stationary single oscillator

Whole record:
- A1 in 3/3.

Median diagnostics:
- half frequency symmetric relative difference: ~0.0115;
- half damping absolute difference: ~0.0145;
- quarter frequency range/median: ~0.0435;
- quarter damping range: ~0.0517;
- RMS-window coefficient of variation: ~0.0386;
- RMS max/min ratio: ~1.120.

### Stationary colored observation-noise control

Whole record:
- A1 in 3/3.

Median diagnostics:
- half frequency difference: ~0.0108;
- half damping difference: ~0.0216;
- quarter frequency range/median: ~0.0960;
- quarter damping range: ~0.0502;
- RMS CV: ~0.0363;
- RMS max/min: ~1.123.

These controls establish the scale of temporal variability under the two frozen stationary constructions.

## Frequency reorganization

Mid-record 8 -> 13 Hz truth:

Whole record:
- A2 in 3/3.

Temporal diagnostics:
- median half frequency symmetric relative difference: ~0.5075;
- median quarter frequency range/median: ~0.5304;
- median half damping difference remained small: ~0.0185;
- RMS CV remained low: ~0.0579.

Therefore the whole-record A2 result is not sufficient to identify “two simultaneous modes.” The same A2 model-order outcome is consistent with sequential frequency reorganization, and the split-record frequency diagnostic exposes that distinction.

## Damping reorganization

Mid-record zeta 0.20 -> 0.70 at fixed 10 Hz:

Whole record:
- A1 in 3/3.

Temporal diagnostics:
- median half damping difference: ~0.4968;
- median quarter damping range: ~0.5786;
- median half frequency difference remained small: ~0.0237;
- RMS CV remained low: ~0.0385.

Thus whole-record A1 can hide a major time-varying damping process. A modal damping estimate cannot be interpreted as stationary merely because a one-oscillator model wins globally.

## Finite bursts / occupancy

Finite bursts:

Whole record:
- A1 in 3/3.

Median diagnostics:
- half same-winner fraction: 2/3;
- RMS CV: ~0.4721;
- RMS max/min ratio: ~3.297;
- quarter latent-fraction range: ~0.0624.

The whole-record stationary A1 family therefore admits finite-burst signals. Occupancy/intermittency diagnostics are necessary if the target claim requires a persistent mode.

## Amplitude-step control

Stationary pole structure with a two-fold second-half amplitude step:

Whole record:
- A1 in 3/3.

Median diagnostics:
- RMS CV: ~0.3420;
- RMS max/min ratio: ~2.277;
- half frequency difference: ~0.0385;
- half damping difference: ~0.0445.

This separates amplitude/occupancy nonstationarity from the much larger pole-parameter shifts in the dedicated frequency/damping-change fixtures.

## What the map earns

The P0-Q map now shows three distinguishable failure/reorganization channels:

1. **frequency nonstationarity**
   - large cross-window frequency inconsistency;
2. **damping nonstationarity**
   - large cross-window damping inconsistency;
3. **occupancy/amplitude nonstationarity**
   - large local RMS heterogeneity without necessarily large pole shifts.

These diagnostics add information that whole-record A0/A1/A2 model order does not contain.

## What it does not earn

No numerical refusal threshold is frozen from these same rows.

The current result cannot be used to:
- declare a real EEG mode stationary;
- promote `REF_NONSTATIONARY` production thresholds;
- infer biological state transition;
- infer local chi from whole-record damping.

A thresholded production rule requires a new prospectively frozen validation version evaluated on separate known-truth realizations/scenarios.
