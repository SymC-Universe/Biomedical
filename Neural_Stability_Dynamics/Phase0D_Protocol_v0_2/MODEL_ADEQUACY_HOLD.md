# Model-Adequacy Hold

Status: **P0-D DIAGNOSTIC ARCHITECTURE SUPPORTED / EXACT P0-Q ADJUDICATION NOT YET QUALIFIED / P1 RULE NOT FROZEN**.

SSI-COV can return numerically stable poles and mode shapes even when the local stochastic linear state-space representation is not an adequate description of the observed process. Structural recovery alone is therefore insufficient for P1 use.

Domain-native EEG system-identification evidence supports residual/innovation whiteness as an adequacy test, and published EEG work demonstrates that model stability and high consistency can coexist with non-white residuals. Neural state-space practice also supports out-of-sample neural self-prediction as a distinct model-quality check.

P0-D4 has now tested a deliberately non-aggregated diagnostic architecture on nominal, perturbed and boundary/transition synthetic observations. Two independent diagnostic paths were kept separate:

1. an SSI-COV positive-lag covariance-reconstruction path using the fitted state-transition/output realization, with covariance fitting on training lags and reconstruction evaluated on held-out train lags and the second-half covariance sequence;
2. a generic channel-space AR(1) path using first-half residual temporal structure plus second-half one-step prediction error. These residuals are explicitly not called SSI-COV innovations.

The resulting diagnostics were complementary. For SSI orders 4/6, stationary known-model records had very low held-out-train covariance reconstruction error and comparatively low test-half error, whereas structural/observation switches and 1/f-like observations produced much larger test-half mismatch despite very good training reconstruction and stable fitted dynamics. The generic residual-whiteness path strongly exposed colored/sensor and 1/f-like temporal structure, while second-half prediction exposed the observation-map switch; neither generic metric alone captured every transition.

The supported architectural conclusion is therefore:

- preserve residual/model-error temporal structure;
- preserve out-of-sample reconstruction/prediction;
- preserve fitted stability/admissibility;
- preserve order/window sensitivity;
- do not average contradictory adequacy components into one compensating score;
- do not infer unestimated process/measurement-noise or Kalman innovation quantities merely to obtain a familiar test.

The remaining hold is **not** to identify a metric category. It is to specify an exact claim-specific adequacy/adjudication rule and qualify it prospectively on independently generated P0-Q evidence. Thresholds, alpha levels, lag/window policies, order sensitivity, and the consequence of each failed component must be frozen before any decisive qualification of that rule.

Failure of an adequacy component should limit only claims that logically depend on that adequacy property. Descriptive structural outputs and open-channel failures remain visible.

See `P0D4_MODEL_ADEQUACY_RESULT_20260911.md`, `LITERATURE_GATE_CANDIDATES_20260910.md`, and `FOUR_HOLD_DECISION_PACKET_20260910.md`.
