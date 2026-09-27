# Meneses 2026 E. coli perturbation-path transport freeze v0.1

**Date:** 26 September 2026  
**Branch:** `bio-chi-meneses-path-transport-p0q-20260926`  
**Status:** FROZEN BEFORE PATH-TRANSPORT OUTPUT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q literature-open direct-experimental path-transport qualification  
**Parent scientific record:** `MENESES2026_ECOLI_PMF_RECOVERY_P0Q_V01_RESULT_PIN.json`

## Why this is the next experiment

The canonical Meneses direct-experimental lineage already established a whole perturbation/recovery relation, rejected one-dimensional recovery compression, refused an unlicensed scalar `chi_bio`, and showed that a stronger rate-depth invariance rule fails. Repeating that dose-response test would not add independent evidence.

The next question is whether the *organization of recovery itself* is conserved or reorganized when the perturbation path changes while the organism and motor readout remain the same.

## Source

Pinned upstream repository:

- `wadhwalab/2026-Meneses-Osmotic`
- commit `d14d0caaa07299f13d1b1121d1e4630454fd724b`

The source paper reports that the gross motor-speed reduction is robust to non-ionic osmolyte identity, buffer context, and rotation direction. Those qualitative source conclusions are already visible and therefore cannot count as blinded confirmation here.

## Frozen assay families

At 200, 300, 400, and 500 mM, analyze the following direct motor-trace families:

1. **Sucrose / standard CCW lane**: `data/time-series/bead/sucrose_*mM.parquet`
2. **Sorbitol / standard CCW lane**: `data/time-series/bead/sorbitol_*mM.parquet`
3. **Sodium assay / buffer-context lane**: `data/time-series/bead/sodium_*mM.parquet`
4. **Clockwise motor lane**: `data/time-series/bead/clockwise_*mM.parquet`

The sodium family is treated only as the source-defined buffer-context assay. No new molecular interpretation is assigned from its label.

## Source-facing per-cell feature extraction

Use the manuscript-facing fit lane already reconciled in
`MENESES2026_SOURCE_METHOD_RECONCILIATION_V01_RESULT_PIN.json`.

For each cell:

- baseline-normalize by mean speed at `t <= 180 s`;
- collapse depth `A_dec` is the difference between mean normalized speed at 155--175 s and 215--235 s;
- collapse timescale `tau_dec` is fit on 175--240 s with fixed source-facing amplitude/offset and positive bounds;
- removal-recovery timescale `tau_inc` is fit on 250--360 s using the source-facing recovery sigmoid;
- recovery gain `G_rec` is mean normalized speed at 330--350 s minus mean normalized speed at 240--260 s.

The frozen representation vector is

[
R = [A_{dec}, log 	au_{dec}, log 	au_{inc}, G_{rec}].
]

A cell is representation-eligible only when all four coordinates are finite and both fitted timescales are strictly positive. Every rejected cell remains in a failure ledger with path, concentration, cell identity, and reason.

No numerical outlier is deleted merely for being extreme.

## Primary question: does path identity leave a multicoordinate signature beyond dose?

Use leave-one-concentration-out path classification.

For each held-out concentration:

1. train only on the other three concentrations;
2. standardize the four representation coordinates using training-fold means and standard deviations;
3. fit multinomial logistic regression with fixed L2 regularization `C=1.0`, balanced class weights, and no hyperparameter tuning;
4. predict the four path labels in the held-out concentration.

Aggregate all four held-out folds and compute balanced accuracy.

### Frozen null

Generate 2,000 permutations using seed `20260926`.

Within each concentration separately, permute path labels while preserving representation vectors. For every permutation, repeat the entire leave-one-concentration-out pipeline.

### Primary decision

- `PATH_REORGANIZATION_DETECTED_P0Q` if observed full-vector balanced accuracy is strictly greater than the 97.5th percentile of the concentration-stratified permutation null.
- `NO_DETECTABLE_PATH_REORGANIZATION_P0Q` otherwise.

The second outcome is not proof of equivalence or universal transport.

## Depth-only control

Repeat the identical classifier/null using only `A_dec`.

Compare the full-vector and depth-only observed balanced accuracies.

- If the full-vector test detects path reorganization and exceeds depth-only balanced accuracy by at least 0.10, classify the added structure as `DYNAMICAL_PATH_INFORMATION_BEYOND_DEPTH_P0Q`.
- If both detect and the full-vector increment is <0.10, classify `PATH_INFORMATION_NOT_SEPARATED_FROM_DEPTH_P0Q`.
- If only depth detects, classify `DEPTH_DOMINANT_PATH_SIGNATURE_P0Q`.
- If neither detects, classify `PATH_SIGNATURE_UNRESOLVED_P0Q`.

This secondary classification cannot override the primary permutation result.

## Condition-level transport matrix

For descriptive auditing only, report path-by-concentration medians for:

- `A_dec`
- `tau_dec`
- `tau_inc`
- `G_rec`

and Spearman dose trends within each path.

These summaries do not create a pass/fail criterion.

## Biological chi hierarchy

- **Biological chi:** the whole relation among osmotic dose, perturbation path, motor-energy displacement, and realized recovery.
- **Chi_bio:** the multicoordinate dynamic representation (R) when supported by the data.
- **chi_bio:** remains closed. The source sigmoids are empirical response summaries and do not identify a mechanistic second-order modal carrier.

No `chi_bio=1` rule is used.

## Failure/outlier rules

A fit failure, source retrieval failure, nonpositive timescale, insufficient data window, or zero-variance training coordinate is preserved explicitly. A failed family or concentration is not silently replaced.

If any path lacks usable cells at any one of the four frozen concentrations, the primary four-path transport gate returns `INSUFFICIENT_PATH_COVERAGE`. Pairwise or reduced-family analyses opened afterward are exploratory and cannot replace the frozen primary result.

## Claim ceiling

This experiment can establish only whether path identity is detectably encoded in the released multicoordinate motor-recovery representation at P0-Q. It cannot establish a universal Bio Chi law, a causal mechanism, scalar `chi_bio`, or biological equivalence across perturbations.
