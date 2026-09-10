# Model-Adequacy Hold

Status: **HOLD_UNQUALIFIED**.

SSI-COV can return numerically stable poles and mode shapes even when the local stochastic linear state-space representation is not an adequate description of the observed process. Structural recovery alone is therefore insufficient for P1 use.

Before a P1 holdout is frozen, the project must justify and precommit model-adequacy diagnostics from domain-native system-identification/neurophysiology practice. Candidate categories may include residual/innovation structure, predictive reconstruction, stationarity/sensitivity diagnostics and model-selection uncertainty, but no diagnostic or threshold is adopted merely because it helps the engine pass.

Until this hold is resolved, a future EEG engine must not interpret successful pole extraction as evidence that the governing neural process is literally the fitted linear generator.
