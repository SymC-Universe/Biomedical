# GRI v2 build status

Status date: 2026-08-29

## Scientific status

The historical scalar branch is closed. `CV/2` remains a historical comparator only and is not chi. No valid biological chi coordinate has yet been identified.

The active project is the Cancer Stability Atlas: a multidimensional predictive-tool development program whose static axes remain separate from any future dynamical chi coordinate.

The development target is not the historical manuscript and not preservation of prior GRI claims. The target is the best falsifiable model supported by the data. Old components may survive only if they earn retention under the new architecture.

## Completed

- GRI v1.1.6 scalar experiment audited and archived.
- Stage A0 static primitives completed from saved v1.1.6 outputs: 20,309 genes, 638,693 within-cancer rows, 32 cancer types.
- Chi admission firewall defined and regression-tested.
- Stage A1 network definitions fixed before network results.
- MSigDB Hallmark v2026.1.Hs chosen as the first external module universe.
- `gri-v2` GitHub development branch established from `main`.
- Project objective explicitly reset to predictive-tool discovery rather than defense or resubmission of the historical manuscript.
- First real Stage A1 launch passed 8/8 tests and then halted before any network statistic because the exact PanCanAtlas source contains non-finite Hallmark expression cells.
- Stage A1 v0.1.1 missing-data policy was frozen after that pre-metric halt and before any `Cin_pairwise`, `Cin_pc1`, `Cout`, eigengene, or leave-one-fold-out result existed.
- The hotfix passes 11/11 tests including exact pairwise-complete Pearson and synthetic missingness regression tests.

## Frozen Stage A1 missing-data policy

1. Non-finite source cells remain missing and are never converted to zero-expression.
2. Within each cancer, genes require at least 95% finite observations, at least 20 finite samples, and nonzero finite variance.
3. `Cin_pairwise` uses exact Pearson correlation on finite overlap; each pair requires at least 80% of cancer samples and at least 20 overlapping samples.
4. PCA/eigengenes z-score each eligible gene on finite observations, then fill remaining standardized missing cells with 0, the within-gene mean in standardized units, only because SVD requires a complete matrix.
5. `Cout` correlates the complete eigengene with each eligible outside gene on that gene's finite samples using the same overlap threshold.
6. Coverage and imputation diagnostics are written into Stage A1 outputs.

## Development sequence

1. Static map: quantify independently defined variability, lineage, and network-organization coordinates.
2. Multiomic map: add independently measured substrate/context layers without folding them into chi.
3. Dynamic benchmark: test ordered perturbation/time-course systems against DNB and ordinary network baselines.
4. Candidate dynamical coordinate: only if the data support admissible `Gamma` and `Omega`, test whether chi adds predictive information.
5. Freeze the selected model before external validation.
6. External validation and calibration determine whether a predictive tool has been earned.
7. Only after that point is a replacement manuscript or resubmission strategy constructed around the validated result.

## Current blocker

No scientific blocker remains for Stage A1. A patched local runner is required because the v0.1 launcher intentionally stopped on non-finite source cells before a missing-data policy had been frozen.

## Exact next scientific/computational step

Run Stage A1 v0.1.1 on the exact PanCanAtlas expression matrix and the Hallmark v2026.1.Hs gene-symbol GMT to compute `Cin_pairwise`, `Cin_pc1`, and `Cout` across eligible cancer types and Hallmark modules, with five-fold deterministic patient-hash leave-one-fold-out stability diagnostics.

No chi, criticality, tipping-point, historical GRI recovery, or composite stability claim is allowed at Stage A1. Stage A1 is a map-building measurement pass.

## User action

Use `CANCER_STABILITY_ATLAS_v0_1_1_A1_NONFINITE_HOTFIX_20260829.zip`, extract it to a fresh folder, and run `RUN_STAGE_A1_WINDOWS.bat`. Select the same PanCanAtlas matrix and Hallmark GMT as before. Return the four named Stage A1 output files for audit.
