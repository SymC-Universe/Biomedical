# NSD state-space stationarity challenge freeze v0.1

Date: 22 September 2026  
Status: FROZEN BEFORE RESULT  
Program authority: SymC General Operations Manual v0.8.3  
Maturity: P0-Q qualification only

## Purpose

The current A0/A1/A2 whole-record model competition distinguishes several static model families, but it can mistake temporal reorganization for simultaneous model order and can admit finite-burst signals as a stationary A1 process.

This challenge prospectively maps temporal inconsistency without changing A0/A1/A2.

The question is:

> Can whole-record, half-record, and quarter-record model behavior expose nonstationary frequency, damping, and occupancy changes while preserving a stationary single-oscillator control?

No production threshold is frozen from this first map.

## Frozen scenarios

All scenarios use 30 s at 256 Hz and seeds 0, 1, 2.

1. `stationary_single`
   - 10 Hz
   - zeta 0.30
   - observation-noise SD / latent SD 0.50

2. `frequency_shift_mid_record`
   - first half: 8 Hz, zeta 0.25
   - second half: 13 Hz, zeta 0.25
   - observation-noise ratio 0.25

3. `damping_shift_mid_record`
   - first half: 10 Hz, zeta 0.20
   - second half: 10 Hz, zeta 0.70
   - observation-noise ratio 0.25

4. `finite_bursts`
   - existing frozen burst generator from the adequacy map

5. `amplitude_step_control`
   - stationary 10 Hz, zeta 0.30 latent dynamics
   - second half amplitude multiplied by 2
   - additive observation noise retained
   - purpose: distinguish nonstationary amplitude/occupancy from a change in pole parameters

6. `colored_observation_stationary_control`
   - existing frozen colored-observation generator
   - purpose: determine whether a stationary noise-model mismatch falsely appears as temporal pole instability

## Frozen diagnostics

For each scenario/seed:

### Whole record
- A0/A1/A2 BIC winner and margin;
- A1 frequency, damping, latent fraction;
- innovation autocorrelation.

### Halves
Fit the first and second 15 s intervals independently with unchanged model/search settings.

Record:
- winner agreement;
- symmetric relative A1 natural-frequency difference;
- A1 damping-ratio absolute difference;
- A1 latent-fraction absolute difference.

### Quarters
Fit four 7.5 s intervals independently.

Record:
- winner sequence;
- A1 natural-frequency range normalized by the quarter median;
- A1 damping-ratio range;
- A1 latent-fraction range.

### Local amplitude occupancy
Split the same standardized record into eight equal windows and record:
- RMS coefficient of variation;
- maximum/minimum RMS ratio.

These are diagnostics only. They are not production refusal thresholds.

## Model/search freeze

Unchanged:
- A0/A1/A2 equations;
- steady-state innovations likelihood;
- BIC;
- hardened multistart search;
- fmin 1 Hz;
- fmax 45 Hz;
- optimizer_maxiter 80.

No scenario-specific tuning is allowed.

## Interpretation firewall

The first map may show candidate diagnostics for:
- `REF_NONSTATIONARY`;
- burst/intermittency;
- temporal pole changes;
- amplitude occupancy changes.

It may not:
- freeze a threshold after inspection and reuse the same rows as confirmation;
- treat whole-record A2 as proof of two simultaneous biological modes;
- treat window disagreement as biological state transition without independent evidence;
- license real-EEG modal damping or local chi.

A later production stationarity/refusal rule requires a new prospective version with thresholds frozen from this qualification map and evaluated on separate known-truth evidence.
