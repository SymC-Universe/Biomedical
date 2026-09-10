# Model-Adequacy Hold

Status: **EVIDENCE_IDENTIFIED / P0 IMPLEMENTATION AUTHORIZED / P1 RULE NOT FROZEN**.

SSI-COV can return numerically stable poles and mode shapes even when the local stochastic linear state-space representation is not an adequate description of the observed process. Structural recovery alone is therefore insufficient for P1 use.

Domain-native EEG system-identification evidence supports residual/innovation whiteness as a direct adequacy test, and published EEG work demonstrates that model stability and high consistency can coexist with non-white residuals. Neural state-space practice also supports out-of-sample neural self-prediction as a distinct model-quality check.

The current P0 implementation target is therefore a non-aggregated adequacy panel containing at minimum:

- residual/innovation temporal structure;
- out-of-sample predictive reconstruction;
- stability/admissibility;
- order/window sensitivity;
- preserved residual/model-error outputs.

No single metric may override a contradictory failed gate by weighted averaging. Exact numerical thresholds and P1 adjudication remain unfrozen until P0 calibration and known-bad qualification are complete.

See `LITERATURE_GATE_CANDIDATES_20260910.md` and `FOUR_HOLD_DECISION_PACKET_20260910.md`.
