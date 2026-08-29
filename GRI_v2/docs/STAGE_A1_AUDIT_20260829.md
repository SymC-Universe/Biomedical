# Stage A1 audit — static Hallmark network map

Status: COMPLETE DEVELOPMENT MEASUREMENT; cross-cancer raw magnitudes require fixed-n calibration before biological comparison.

## Integrity

- Exact frozen PanCanAtlas expression SHA-256 matched: `674b19b7ed9ae4c5ef35ee2824936429aa5d46c0735a3d180f41552fcbbdb658`.
- 9,546 unique-primary samples across 32 cancer types.
- 50 externally defined Hallmark modules.
- 1,600 cancer-module point estimates, exactly 32 x 50.
- `chi` absent; `CV/2` absent from network construction.
- Source non-finite Hallmark cells: 141,836 / 39,978,648 = 0.3548%, preserved as missing under the pre-result hotfix.
- Retained module/cancer point estimates have median gene finite fraction 1.0 and PC1 imputed fraction 0.0, so the accepted module metrics are not being numerically driven by imputed cells.

## Leave-one-fold-out stability

31 cancers support all five deterministic leave-one-fold-out folds. CHOL supports three folds because two holdouts would reduce the retained cohort below the frozen minimum of 30 samples; all 50 CHOL modules therefore have three usable folds rather than five.

Median relative LOO standard deviation across the 1,600 point estimates:

- `Cin_pairwise`: 0.02315 (2.3%)
- `Cin_PC1`: 0.02914 (2.9%)
- `Cout`: 0.03558 (3.6%)

95th-percentile relative LOO SD:

- `Cin_pairwise`: 5.38%
- `Cin_PC1`: 7.61%
- `Cout`: 9.48%

Interpretation: the static network coordinates are reproducible under patient-fold removal at development scale.

## Topology across Hallmark modules within cancer

Within each cancer, cohort size is fixed across its 50 modules, so module-rank relationships are not affected by between-cancer sample-count differences.

- `Cin_pairwise` vs `Cin_PC1`: median within-cancer Spearman rho = 0.9090, range 0.8161 to 0.9608. These are largely redundant views of internal module coherence.
- `Cin_pairwise` vs `Cout`: median within-cancer Spearman rho = -0.4907, range -0.7395 to -0.1472; negative in all 32/32 cancers. Greater internal coherence therefore tends to accompany lower coupling to the Hallmark-union background, but this is a descriptive static topology, not an optimum or stability claim.
- Stage A0 module variability vs `Cin_pairwise`: median within-cancer rho = -0.1158.
- Stage A0 module variability vs `Cin_PC1`: median within-cancer rho = 0.00425.
- Stage A0 module variability vs `Cout`: median within-cancer rho = -0.0701.

Interpretation: the Stage A1 network layer is not simply a restatement of the Stage A0 variability coordinate.

## Construction issue discovered before cross-cancer interpretation

Across all 1,600 raw cancer-module points, original cohort size has a modest negative Spearman association with absolute-correlation coordinates:

- n vs `Cin_pairwise`: rho = -0.2789
- n vs `Cin_PC1`: rho = -0.1293
- n vs `Cout`: rho = -0.2646

Absolute correlation has a finite-sample floor, so raw cross-cancer magnitude comparisons are not yet biologically interpretable. The prospectively frozen Stage A1.1 calibration therefore resamples every cancer to the same `n=30`, 100 deterministic resamples per cancer, and recomputes the unchanged A1 metrics.

## Claim ceiling

Stage A1 supports only a reproducible static network topology. It does not establish dynamics, criticality, damping, a phase transition, a stability optimum, or chi. In particular, higher internal coherence or lower external coupling is not defined as closer to chi=1 or as universally "more organized." Organization/coherence observables remain independent of any future dynamical balance coordinate.
