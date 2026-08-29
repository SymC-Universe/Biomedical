# GRI v2 build status

Status date: 2026-08-29

## Scientific status

The active project is the Cancer Stability Atlas predictive-tool development program. The historical scalar branch remains closed; `CV/2` is historical only and no valid biological chi coordinate has yet been identified.

Chi, if later earned from genuine dynamic measurements, is a dynamical regime-balance coordinate. Distance to `chi = 1` does not define organization, coherence, health, optimality, or pathology.

## Completed

- GRI v1.1.6 scalar experiment audited and archived.
- Stage A0 static variability/lineage primitives completed.
- Stage A1 Hallmark network run completed on 9,546 unique-primary PanCanAtlas samples across 32 cancers and 50 Hallmark modules.
- Stage A1 produced 1,600 cancer-module point estimates and a complete development audit.
- A1 missing-data repair was frozen before any network estimate and the completed run shows only 0.3548% source non-finite Hallmark cells; retained point estimates have zero median PC1 imputation fraction.
- Network coordinates are stable under patient-fold removal.
- Within cancers, the two internal-coherence measures are largely redundant; external coupling is a distinct opposing axis; Stage A0 variability does not explain the network layer.
- A finite-sample construction effect was detected in raw cross-cancer absolute-correlation magnitudes before biological interpretation.

## Current step

Stage A1.1 fixed-n calibration is frozen and ready. It uses the completed Stage A1 `hallmark_profile_cache.npz` and `hallmark_membership_snapshot.gmt`, not the 1.88 GB source matrix.

Every cancer is deterministically subsampled to `n=30` 100 times and the unchanged A1 metrics are recomputed. This closes the finite-sample floor before any cross-cancer comparison.

## User action

Run `RUN_STAGE_A1_1_WINDOWS.bat` from the Stage A1.1 calibration handoff package. Select the cache and Hallmark membership snapshot produced by the completed A1 run. Upload:

- `STAGE_A1_1_SUMMARY.json`
- `stage_a1_1_fixed_n_calibration.csv`
- `stage_a1_1_cancer_level_diagnostic.csv`

No PanCanAtlas matrix reread is required.

## After A1.1

If the fixed-n calibration closes the construction bias without revealing a new mechanical defect, static Stage A closes. The next branch is Stage B multiomic/context integration, followed by genuine ordered perturbation/time-course benchmarking. No chi or optimum claim is allowed from the static stages.
