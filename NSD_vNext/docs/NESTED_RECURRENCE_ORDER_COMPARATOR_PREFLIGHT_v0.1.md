# NSD Nested Recurrence-Order Comparator Preflight v0.1

Status: QUALIFICATION-ONLY / NO THRESHOLD FREEZE
Date: 27 September 2026
Authority: GOM v0.8.6

## Purpose

Test whether explicit recurrence-order comparison is more sensitive to the known colored-process extra pole than the current order-two residual and Hankel diagnostics.

The comparator is structural only. It does not change A0/A1/A2, C1Q, D1Q, or real-EEG admission.

## Design

For each known-truth realization, split the signal into training and untouched holdout segments. Estimate normalized positive-lag covariance separately in each segment.

Fit nested linear recurrences to training covariance:

- order 2: one second-order mode;
- order 3: one second-order mode plus one distinct real pole;
- order 4: generic two-mode covariance structure.

Freeze recurrence coefficients and score holdout covariance prediction. Report normalized holdout error and the improvement from order 2 to 3 and from order 3 to 4.

Truth controls include C interiors, D outside C, S outside D, colored-process extra-pole truth, and genuine separated two-mode truth. Evaluate multiple durations and deterministic decimation where computationally cheap.

## Interpretation

No empirical cutoff is selected. A useful result is reproducible out-of-sample order-3 improvement for colored truth without comparable improvement for genuine order-2 controls, and order-4 improvement for genuine two-mode truth.

If finite-sample order improvements still overlap materially, preserve refusal and move to an explicit likelihood-based higher-order/memory comparator rather than tune a cutoff.

## Ceiling

This experiment does not license real EEG local chi, promote an estimator, define a threshold, or alter N-B2/N-B3.
