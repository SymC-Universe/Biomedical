# NSD Combined Structural-Predictive Refusal Preflight v0.1

Status: PROSPECTIVE QUALIFICATION ONLY  
Date: 27 September 2026  
Authority: SymC General Operations Manual v0.8.6  
Primary investigation: Bio Chi  
Branch: \`nsd-rebuild-gom-v0.8.0\`

## Purpose

The current Bio Chi N-B1 route has two established finite-data failures:

1. C1Q can win BIC on a colored-process truth that contains an additional real pole.
2. Exact second-order recurrence/Hankel identities do not, by themselves, yield a clean finite-sample cutoff at 30 to 300 s.

This preflight defines the next safe qualification experiment. It asks whether **multiple independent consequences of model misspecification move together** on untouched holdout data.

No new estimator family is introduced. No empirical threshold is frozen.

## Core question

Can a second-order one-mode candidate that fits training data well still be distinguished from higher-order or memory-contaminated truth by jointly examining:

- frozen-parameter held-out predictive likelihood;
- held-out innovation autocorrelation;
- held-out innovation scale;
- positive-lag recurrence/Hankel diagnostics;
- C1Q versus D1Q scope behavior;
- current A0/A1/A2 comparison as a descriptive control?

The target is not to find one magic scalar. The target is to determine whether a **refusal pattern** exists that is mechanistically coherent and prospectively calibratable.

## Truth classes

The first map will retain the established reference geometry:

- C interior, g=0;
- C interior, g=-0.75;
- C interior, g=+0.75;
- positive and negative D\C;
- positive and negative S\D;
- colored-process extra-pole truth, phi=0.7;
- genuine separated two-mode truth.

Fine-rate paths are generated at 256 Hz. Where sampling comparison is used, 128 Hz is obtained by deterministic decimation of the same realization.

## Holdout semantics

This experiment intentionally uses the **existing frozen cold-start holdout semantics** as a diagnostic control:

- fit on the training segment;
- retain training mean and standard deviation;
- freeze fitted parameters;
- score the contiguous holdout as a fresh filter segment;
- use the existing burn convention.

This does not silently convert the current holdout into an exact conditional forecast. The distinction from terminal-state carry-forward remains open and is reported explicitly.

## Outputs

For each truth class, seed, candidate, and rate where applicable, report:

- training NLL and BIC;
- held-out NLL per sample;
- held-out innovation maximum absolute autocorrelation over the declared lag range;
- held-out innovation RMS;
- fitted chi;
- fitted g for C1Q;
- fitted h and implied g for D1Q;
- structural recurrence residual and Hankel singular-value ratios on the holdout;
- current A0/A1/A2 holdout results where computationally practical.

Summary output must remain threshold-free and report distributions/quantiles and rank-based discrimination rather than a pass/fail boundary.

## Interpretation rules

The following are forbidden conclusions:

- C1Q held-out superiority implies truth in C;
- low innovation autocorrelation alone licenses local chi;
- low recurrence residual alone proves second order;
- D1Q implied |g|<1 proves C membership;
- any single descriptive cutoff discovered on these rows becomes an admission threshold.

A useful result would be a reproducible multichannel signature that separates valid C interiors from colored/extra-pole truth sufficiently well to justify a later prospectively frozen calibration design.

A null result is also informative. If combined diagnostics still overlap materially, N-B1 must move to a stronger explicit higher-order/memory comparator or a more conservative refusal architecture rather than tuning a threshold until separation appears.

## Scientific ceiling

This experiment does not:

- license real-EEG local chi;
- change production A0/A1/A2;
- promote C1Q or D1Q;
- define a structural-order threshold;
- define a predictive-closure threshold;
- open disorder outcomes;
- modify N-B2 or N-B3.
