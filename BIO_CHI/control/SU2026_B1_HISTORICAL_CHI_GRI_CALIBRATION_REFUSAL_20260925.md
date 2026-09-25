# Su M397 B1 static-to-dynamic calibration refusal

**Date:** 25 September 2026
**Branch:** `gri-biochi-bridge-p0q-20260925`
**Task:** `GRI_BIOCHI_B1_STATIC_TO_NATIVE_DYNAMICS_20260925`
**Disposition:** `REFUSED_INDEPENDENT_HISTORICAL_CHI_GRI_CALIBRATION`
**Failure class:** carrier-axis dependence / circularity risk, not scientific contradiction.

## Source facts used for adjudication

The frozen Su/M397 processed RNA source contains one explicit 15-point reversible trajectory:
`Control, D3, D8, D13, D21, D29, D33, D38, D59, dr29.D4, dr29.D10, dr29.D15, dr29.D17, dr29.D30, dr29.D35`.

The source-native two-state generator uses source-defined Mearly/Mlate positive/negative modules and Drug ON/OFF trajectory segments. The generator result already supplies the independently fitted native dynamical object.

## Why historical chi_GRI cannot be calibrated independently here

Historical `chi_GRI = sigma/(2 mu) = CV/2` was defined from an across-sample RNA axis. In the frozen M397 processed carrier, the available expression columns are the ordered trajectory itself rather than an independent replicate-rich static sample family.

Computing per-gene `mu` and `sigma` across these trajectory columns would therefore:
1. use the same ordered perturbation/recovery path that generates the dynamical target;
2. convert time variation into the historical cross-sectional variance proxy;
3. destroy the intended static-to-dynamic separation; and
4. create a relation partly by shared construction.

Computing across genes within a source module at one time point would be a different statistic from historical GRI and is not authorized as a repair.

## Preserved result

Su remains admissible for:
- source-native generator/eigenmode analysis;
- nominal damping/oscillation classification where complex modes exist;
- uncertainty/refusal analysis;
- modal reorganization and recovery questions.

It is **not** an independent B1 calibration of historical `chi_GRI` to native dynamics.

## Scientific meaning

This refusal does not show that historical `chi_GRI` lacks a relationship to independently measured dynamics. It shows that the Su carrier cannot test that relationship without circular reuse of the ordered trajectory or invention of a new proxy.

## Next exact action

Continue targeted source search for a system with:
- independent static/replicate RNA measurements sufficient to compute a frozen GRI-compatible proxy;
- same-carrier ordered dynamics with an independently licensed robust scalar or generator;
- outcome-independent carrier mapping;
- preferably a held-out condition/cell line for transport.

## Safe resume point

After this refusal, before opening any new candidate's target molecular effect.

## Scientific state changed

Yes, locally: Su is now explicitly refused as an independent historical-chi_GRI B1 calibration carrier. No manuscript claim is promoted or weakened by this refusal.
