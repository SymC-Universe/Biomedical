# E. coli osmotic perturbation-path transport freeze v0.1

**Date:** 25 September 2026  
**Branch:** `bio-chi-ecoli-path-transport-p0q-20260925`  
**Status:** FROZEN BEFORE SYMC-SPECIFIC PATH-TRANSPORT OUTPUT EXTRACTION  
**Authority:** SymC GOM v0.8.6  
**Evidence class:** P0-Q literature-open direct experimental transport qualification

## Parent result

The parent Meneses lineage is already closed and establishes, at P0-Q, a direct experimental collapse/recovery Bio Chi relation with a multicoordinate motor/orthogonal-assay representation and no licensed scalar `chi_bio`.

Canonical parent closure:
`BIO_CHI/control/MENESES2026_ECOLI_PMF_RECOVERY_CLOSURE_20260925.md`.

This experiment asks a new question: whether the measured motor-response organization transports when the perturbation path or motor context changes while the organism and nominal shock-strength series are retained.

## Pinned upstream source

Repository: `wadhwalab/2026-Meneses-Osmotic`  
Commit: `d14d0caaa07299f13d1b1121d1e4630454fd724b`

### Canonical sucrose / CCW path

- 200 mM: `data/time-series/bead/sucrose_200mM.parquet`, blob `41c7e7837d7f6e0418180d85ded212a102af0621`
- 300 mM: blob `78d915b2264dd6fa273ba061e605ee8597a28a06`
- 400 mM: blob `36ebcaa9c817ba8c11527e69d6f8b49669b1f2d6`
- 500 mM: blob `dd3b2ef0b1b77c43c02080c88080abb5b0cd3f61`

### Sorbitol / CCW path

- 200 mM: blob `f105b4efa5815bff50bbe51ef493550b49c91d36`
- 300 mM: blob `cec88379c5da5a07dc444fd25c2f0be8937ec81e`
- 400 mM: blob `f3fd7373b2944f01b945b7259661f3fc6a75fc85`
- 500 mM: blob `1833accfa1e4405bebfd0e9430008854e3492567`

### Sodium-buffer assay path

- 200 mM: blob `57ec489e1a19cc3a20ea6dea270152b86b359fa0`
- 300 mM: blob `5496ff4a54d4631fd0349d63966926d7ae065b7f`
- 400 mM: blob `fe51858b5cc7b6e6e7d1eb94a4bcb165ce1d312c`
- 500 mM: blob `52ab687a447fb5681492e4a25e7cf7814b2270c2`

### Clockwise-locked sucrose path

- 200 mM: blob `c09ed5d53afd435097e26d5b10330dfd09e3538e`
- 300 mM: blob `c38f3e0ccffd884aee46732917233a73cd573212`
- 400 mM: blob `342d9c3c9164a20b3ec9d9ee7749989221854f41`
- 500 mM: blob `7a42570406646d9f329f1c9a32c870ffaf6fc56a`

The source paper reports qualitative robustness of motor slowdown to nonionic osmolyte choice, buffer composition, and motor rotation direction. Those qualitative outcomes are literature-open. The new SymC-specific multicoordinate transport result is not.

## Frozen biological question

Does the four-coordinate motor response architecture identified in the canonical sucrose/CCW path transport across:
1. nonionic osmolyte substitution;
2. buffer/context substitution;
3. motor rotation-direction substitution?

The whole event remains osmotic perturbation -> motor-speed collapse -> post-removal recovery.

## Frozen per-cell representation

Use the manuscript-facing source method inherited from the completed source-method reconciliation.

For every trace:

1. normalize speed by mean speed for `time <= 180 s`;
2. define `speed_initial` as mean normalized speed from 155-175 s;
3. define `speed_final` as mean normalized speed from 215-235 s;
4. set `A_dec = speed_initial - speed_final`;
5. fit positive `tau_dec` and `t0_dec` on 175-240 s with the fixed-amplitude logistic source form;
6. define recovery anchors from 240-260 s and 330-350 s;
7. fit source logistic `tau_inc` and `t0_inc` on >250-360 s;
8. compute `recovery_fraction = (speed_330_350 - speed_240_260)/(1 - speed_240_260)` when the denominator is finite and nonzero.

The frozen `Chi_bio` motor vector is:
`[A_dec, log(tau_dec), log(abs(tau_inc)), recovery_fraction]`.

The sign of `tau_inc` is retained separately as a diagnostic. A nonpositive fitted `tau_inc` is not silently removed if the source fit returned finite parameters.

## Primary matched-dose path transport test

For each alternate path versus canonical sucrose, and for each concentration:

1. pool the two path groups at that concentration;
2. standardize each of the four coordinates using the pooled robust scale `1.4826 * MAD`; if MAD is zero, use pooled standard deviation;
3. calculate the four-coordinate median vector for each path;
4. calculate Euclidean distance between the standardized median vectors.

Aggregate the four matched-dose distances by their arithmetic mean to obtain `D_path`.

Use 10,000 label permutations within each concentration, preserving group sizes, seed `20260925`, to obtain the null distribution of `D_path`.

Holm-correct the three path-comparison p-values.

## Practical transport band

Statistical non-rejection alone does not establish transport.

For every alternate path, also calculate the maximum absolute standardized median difference across all 16 feature-by-dose comparisons.

Frozen disposition:

- `TRANSPORT_COMPATIBLE_P0Q`: Holm-adjusted p >= 0.05 **and** maximum absolute standardized median difference <= 0.50.
- `PATH_DEPENDENT_REORGANIZATION_P0Q`: Holm-adjusted p < 0.05 **or** maximum absolute standardized median difference > 0.50.
- `TRANSPORT_UNRESOLVED_SOURCE_LIMITED_P0Q`: fewer than three valid cells exist in any required path-by-dose cell or a required coordinate is non-identifiable.

The 0.50 pooled-scale threshold is a prospective practical-equivalence band for this qualification only. It is not a universal biological threshold.

## Coordinate-level decomposition

If a path is classified as reorganization, report which coordinate-by-dose deviations exceed the 0.50 band. This is descriptive localization, not a new post-result admission criterion.

## Hierarchy disposition

- **Biological chi:** transport or reorganization of the whole osmotic perturbation/recovery relation across path contexts.
- **Chi_bio:** the four-coordinate motor response organization defined above.
- **chi_bio:** remains `NOT_OPENED_NOT_LICENSED`; sigmoid time constants are empirical response summaries, not identified damping modes.

## Failure rules

All fit failures and nonpositive recovery-tau diagnostics remain in the audit trail. No cell is removed for being an outlier. A required source or fitting failure triggers source-limited disposition rather than threshold retuning.

## Claim ceiling

One *E. coli* system, literature-open P0-Q path-transport qualification. This cannot establish universal biological invariance, substrate inheritance across species, or a universal scalar boundary.
