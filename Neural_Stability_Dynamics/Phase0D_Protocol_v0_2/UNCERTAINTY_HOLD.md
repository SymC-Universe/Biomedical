# Uncertainty and INDETERMINATE Hold

Status: **HOLD_UNQUALIFIED**.

The current method has deterministic cutoffs but does not yet possess a justified estimator-uncertainty model that can decide when supported uncertainty spans incompatible admission regimes.

No arbitrary gray-zone width is introduced in this P0 reconciliation.

Before P1 freeze, the project must select and validate an uncertainty procedure appropriate to the estimator and define when the result is `INDETERMINATE` rather than forced to ADMIT or REFUSE. Candidate routes include bootstrap, Monte Carlo, perturbation/sensitivity and model-selection uncertainty, subject to native-science justification and known-truth calibration.
