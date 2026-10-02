# NSD state-space high-damping boundary extension freeze v0.1

Date: 22 September 2026  
Status: FROZEN BEFORE EXTENSION RESULT  
Program authority: SymC General Operations Manual v0.8.3  
Maturity: P0-Q qualification only

## Why this extension exists

The hardened A0/A1/A2 operating-region result showed a concentrated boundary:
- damping ratios 0.2 and 0.5 selected A1 in 54/54 rows each;
- damping ratio 0.8 selected A1 in 33/54 rows;
- all 21 non-A1 rows occurred at damping ratio 0.8;
- 14/21 occurred at 10 s and 7/21 at 30 s;
- 13/21 occurred at observation-noise ratio 1.0, 7/21 at 0.5, and 1/21 at 0.0.

The hardened search diagnostics no longer support the earlier explanation that these rows are simple optimizer collapse.

This extension asks a narrower prospective question:

> Does the A0-versus-A1 boundary move systematically as underdamped truth approaches the high-damping/near-critical side, and can additional duration rescue identifiability under low versus high observation noise?

It does not assume that A1 must win. A0 preference may be the scientifically correct result when oscillatory information is insufficient.

## Frozen grid

Natural frequency:
- 5 Hz
- 10 Hz
- 20 Hz

Truth damping ratio:
- 0.80
- 0.90
- 0.95

Duration:
- 30 s
- 120 s

Observation-noise SD / latent SD:
- 0.0
- 1.0

Seeds:
- 0
- 1
- 2

Sampling rate:
- 256 Hz

The 30 s, zeta=0.80 cells intentionally overlap part of the prior map as an anchor/regression check. No prior result is discarded.

## Model and search

Unchanged:
- A0 nonoscillatory latent relaxation;
- A1 one latent oscillator;
- A2 two latent oscillators;
- steady-state innovations likelihood;
- BIC within-record model comparison;
- hardened multistart search;
- optimizer_maxiter=80;
- fmin=1 Hz;
- fmax=45 Hz.

No threshold, model equation, or admission rule changes.

## Required outputs

For every row:
- BIC winner and margin;
- A0/A1/A2 fit diagnostics;
- A1 natural-frequency relative error;
- A1 damping-ratio absolute error;
- A1 latent fraction and pole radius;
- innovation autocorrelation;
- near-optimal start count;
- near-optimal parameter ranges.

Summaries must preserve frequency, damping, duration, and noise strata rather than reducing the result to one overall rate.

## Interpretation firewall

This run may establish a candidate high-damping Limit Map. It may not:
- freeze a production operating boundary by inspection alone;
- call A0 selection a fitting failure merely because A1 truth generated the signal;
- call A1 selection adequate merely because the truth is oscillatory;
- license real-EEG damping or local chi;
- define a universal critical boundary;
- tune thresholds from these results and then relabel the same rows as confirmation.

If longer duration fails to recover A1 at high damping, that is a real candidate identifiability limit. If longer duration systematically rescues A1, duration becomes an explicit information requirement for later admission design.
