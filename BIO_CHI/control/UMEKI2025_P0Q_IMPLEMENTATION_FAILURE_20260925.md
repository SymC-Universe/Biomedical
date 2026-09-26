# Umeki 2025 P0-Q implementation failure checkpoint

**Date:** 25 September 2026  
**Branch:** `bio-chi-erk-egf-depth-rate-p0q-20260925`  
**Authority:** SymC GOM v0.8.6  
**Status:** MECHANICAL FAILURE PRESERVED / SCIENTIFIC TEST NOT OPENED

## Failure

Workflow run `36219324933` failed before the first source CSV was downloaded or parsed.

Root cause:

`http.client.InvalidURL` because the frozen upstream path `EGF dose dynamics data/...` contains spaces and the raw URL builder did not percent-encode the path.

## Scientific consequence

No trajectory values, source cell counts, response features, cross-validation metrics, bootstrap results, or representation outcomes were inspected.

The prospective freeze remains intact.

## Allowed repair

Percent-encode the already-frozen source path before HTTP retrieval. No source identity, file list, time window, feature definition, model, threshold, bootstrap rule, or scientific decision may change.

**Disposition:** `IMPLEMENTATION_TRANSPORT_FAILURE_REPAIRABLE`.
