# GRI / SymC brain-state known-truth reproduction audit

**Date:** 2026-09-21/22  
**Status:** P0-D SOURCE-NATIVE KNOWN-TRUTH REPRODUCTION COMPLETE  
**SymC scalar chi:** NOT LICENSED IN THIS TEST  
**SymC incremental value:** NOT TESTED

## Status

The source-native network-dependence result from `grabuffo/State_Dependent_Brain_Stimulation` was reproduced from pinned derived data at source commit:

`84afcf934c3798b2a40dc8da22d0840e60a4b0f9`.

GRI execution:

- workflow: `SymC brain-state source-native known-truth reproduction`
- run: `35671352024`
- head SHA: `885791c4799090c00f7776da4575cbf1f6f0eb6d`
- conclusion: `success`
- artifact: `SYMC_BRAIN_STATE_KNOWN_TRUTH_SOURCE_REPRODUCTION_V01`
- artifact ID: `10671395900`
- artifact digest: `sha256:116649a13cef743964857a8902c4c983995ba69d75e0d69ff645b853fb2379e4`

The reproduction validates source-native summaries only. It does not relabel the source variables as SymC variables.

## What reproduced

### SEEG

At the source notebook's 100-radius condition:

- rows: 7,900;
- 25 metric pairs;
- Friedman chi-square: `88.85142857142864`;
- p: `5.2473662766591425e-17`;
- median ordered-network gradient rho: `0.8214285714285715`;
- mean gradient rho: `0.7342857142857144`;
- positive gradient pairs: `25 / 25`;
- exact signed-rank p: `2.9802322387695312e-08`.

Mean squared pre/post correlations increased across the source's ordered network sequence from:

`DMN 0.143669 -> LIM 0.164443 -> CON 0.171445 -> DAN 0.178338 -> VAN 0.192850 -> SMN 0.190580 -> VIS 0.204415`

with the small VAN-to-SMN non-monotonicity handled by the rank statistic rather than hidden.

### hdEEG

At the same source-native radius convention:

- rows: 7,950;
- 25 metric pairs;
- Friedman chi-square: `40.26857142857148`;
- p: `4.0337335128700496e-07`;
- median ordered-network gradient rho: `-0.03571428571428572`;
- mean gradient rho: `0.02571428571428573`;
- positive gradient pairs: `12 / 25`;
- exact signed-rank p: `0.5315985679626465`.

Thus network identity matters to the distribution of source-native pre/post predictability in both measurement modalities, but the strong monotonic network gradient reproduced in SEEG does **not** transport to hdEEG.

## Mechanical/runtime fault discovered and repaired

The first modern-runtime reproduction matched the source means, counts, Friedman statistics and gradient summaries but did not match the archived source notebook's Wilcoxon p-values.

A separate diagnostic was run before modifying the reproduction rule:

- workflow: `SymC brain network Wilcoxon method diagnostic`
- run: `35671050037`;
- runtime SciPy: `1.18.1`.

For SEEG:

- modern `method=auto`: `6.001696098658608e-06`;
- modern `method=approx`: `6.001696098658608e-06`;
- `method=exact`: `2.9802322387695312e-08`;
- archived source notebook: `2.980232e-08`.

For hdEEG:

- modern `method=auto`: `0.5214903346718707`;
- `method=exact`: `0.5315985679626465`;
- archived source notebook: `0.531599`.

The archived outputs are therefore reproduced by exact signed-rank evaluation, while current SciPy `auto` selects an asymptotic route for the tied rank structures. The source reproduction pins `method="exact"` explicitly and records why. This is implementation-version drift, not a biological discrepancy.

Two intermediate mechanical failures were preserved:

1. JSON serialization of a NumPy boolean;
2. a generated source-edit syntax/comment fault.

Neither produced scientific output and neither changed the frozen numerical target.

## Why this matters for the chi <-> Chi investigation

This source supplies an independent empirical known-truth case for a weaker but essential proposition:

> realized response depends on broader system/network state, and the relationship itself can be measurement/representation dependent.

It is particularly useful because the SEEG/hdEEG contrast prevents the program from turning a successful system-level effect into a universal statement.

The evidence does **not** yet establish:

- a local scalar `chi`;
- a capital-`Chi` brain ontology;
- a direction `Chi -> chi` in SymC notation;
- SymC added value over the source-native metrics;
- universality across measurement modalities.

## Current joint-meaning disposition

```text
SOURCE_NATIVE_NETWORK_DEPENDENCE = REPRODUCED
NETWORK_GRADIENT_SEEG = SUPPORTED_IN_SOURCE_REPRODUCTION
NETWORK_GRADIENT_HDEEG = NOT_SUPPORTED
MEASUREMENT_REPRESENTATION_DEPENDENCE = OBSERVED
LOCAL_SCALAR_CHI = NOT_LICENSED
CAPITAL_CHI = NOT_CONSTRUCTED
SYMC_INCREMENTAL_VALUE = NOT_TESTED
```

This is therefore a successful **known-truth calibration and Limit-Map result**, not a SymC confirmation result.

## Residual experiment

The residual SymC question is narrower than the source paper:

1. preserve the source-native local and network predictors;
2. independently test whether a native local oscillatory factor licenses scalar `chi`;
3. if licensed, compare local-only, broader-system-only, additive joint and interaction models under the same held-out split;
4. if scalar admission fails, continue with the admitted local/modal object rather than manufacturing a scalar;
5. require any SymC representation to equal or outperform the source-native standard-toolkit baseline before claiming incremental value.

Exact trial-level reproduction of the source's Figure-1D local predictive analysis is not currently possible from the pinned GitHub repository alone because the notebooks reference `df_9MOIs_*.csv` files not present in the repository. The upstream OSF archive is available but multi-gigabyte. Under run-economy rules, that acquisition is deferred until the residual experiment requires information unavailable from the current derived data.
