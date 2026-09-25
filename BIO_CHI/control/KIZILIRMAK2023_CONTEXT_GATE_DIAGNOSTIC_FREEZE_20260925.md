# Kizilirmak TNF vs IL-1beta context-gating diagnostic freeze

**Date:** 25 September 2026  
**Task:** `GRI_BIOCHI_KIZILIRMAK_CONTEXT_GATE_20260925`  
**Status:** POST-TRANSPORT ROOT-CAUSE DIAGNOSTIC

## Purpose

Explain the clone-G transport failure without rescuing the historical scalar claim.

## Frozen questions

1. Reproduce TNF and IL-1beta native dynamics with the same peak/AUC implementation and compute stimulus-induced changes in oscillatory fraction, AUC, and first-peak amplitude for B/R/G.
2. Extract untreated source-native means, SDs, and historical chi_GRI for the two source-defined limiting receptors:
   - TNF: `Tnfrsf1a`
   - IL-1beta: `Il1rap`
3. Test descriptively whether the source-native receptor **mean abundance** ordering tracks the source-native first-peak ordering within each stimulus. n=3 is descriptive only.
4. Compare receptor abundance changes in rank structure with the observed G stimulus shift. No fitted multivariable model is allowed.
5. Report the five circuit-component means/SDs/chi values (`Tnfrsf1a`, `Il1rap`, `Rela`, `Nfkbia`, `Tnfaip3`) to distinguish abundance control from variability-proxy behavior.
6. Do not derive a new scalar, optimize weights, combine receptor mean with chi_GRI, or select a favorable component after seeing the result.

## Adjudication

- If the source-native receptor mean ranks reproduce the source first-peak ranks for both stimuli while global chi_GRI fails on G, classify the failure as `CONTEXT_GATING_LIMIT_OF_GLOBAL_STATIC_SCALAR`.
- If receptor mean does not reproduce the first-peak rank, classify `CONTEXT_GATE_EXPLANATION_INCOMPLETE`.
- Regardless of outcome, the IL-1beta result remains a failure of context-independent global chi_GRI transport.
