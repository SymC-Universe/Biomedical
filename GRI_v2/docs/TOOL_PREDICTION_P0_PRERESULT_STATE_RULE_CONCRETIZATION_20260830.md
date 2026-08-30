# P0 pre-result state-rule concretization

**STATUS: FROZEN WITH P0 BEFORE P0 TARGET VALUES OR STAGE C1 BETA-VALUE BIOLOGICAL RESULTS ARE INSPECTED**

Date: 2026-08-30

This note makes the shorthand phrase "construction-aware within-layer organization" in `TOOL_PREDICTION_P0_HOLDOUT_FREEZE_20260830.md` machine-explicit before any P0 result exists.

For each layer in DISCOVERY:

1. compute the layer's spectral concentration `S_spec = 1 - H_norm` using the same modal definition already frozen for C1;
2. generate 39 deterministic construction-null replicates by independently permuting patient values within each feature/probe column, preserving each discovery marginal while destroying cross-feature sample alignment;
3. define `Delta_S_spec = S_spec_observed - median(S_spec_null)`;
4. compute the empirical one-sided p-value `(1 + count(null >= observed)) / 40`;
5. classify the layer as `WITHIN_LAYER_ORGANIZED` only when empirical `p <= 0.05` and `Delta_S_spec > 0`.

No absolute `Delta_S_spec` magnitude threshold is introduced.

State mapping is therefore exact:

- `NO_SHARED_STRUCTURE`: global sharing is not detected and neither layer is `WITHIN_LAYER_ORGANIZED`;
- `WITHIN_LAYER_ONLY`: global sharing is not detected and at least one layer is `WITHIN_LAYER_ORGANIZED`.

All other P0 rules remain exactly as frozen in the P0 protocol and machine-readable config. This note does not modify Stage C1 v2.
