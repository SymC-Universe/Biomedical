# GRI v2 build status

Status date: 2026-08-29

## Scientific status

The active project is the Cancer Stability Atlas predictive-tool development program. The historical scalar branch remains closed; `CV/2` is historical only and no valid biological chi coordinate has yet been identified.

Chi, if later earned from genuine dynamic measurements, is a dynamical regime-balance coordinate. Distance to `chi = 1` does not define organization, coherence, health, optimality, or pathology.

## Completed

- GRI v1.1.6 scalar experiment audited and archived.
- Stage A0 static variability/lineage primitives completed.
- Stage A1 Hallmark network run completed on 9,546 unique-primary PanCanAtlas samples across 32 cancers and 50 Hallmark modules.
- Stage A1 missing-data policy was frozen before any network estimate and the completed run retained only sparse source missingness.
- Stage A1 patient-fold stability audit completed.
- Stage A1.1 fixed-n construction calibration completed: 32 cancers x 50 modules x 100 n=30 resamples = 160,000 complete resample measurements.
- Raw cancer-level absolute-correlation coordinates showed finite-sample dependence, but after fixed-n calibration residual Spearman correlations with original cohort size are only -0.0317, -0.0880, and -0.0563 for pairwise Cin, PC1 fraction, and Cout respectively.
- Original-to-calibrated module rank ordering is strongly preserved, with median within-cancer rho approximately 0.989, 0.990, and 0.920 for pairwise Cin, PC1 fraction, and Cout.
- In the calibrated map, the two internal-coherence measures are largely redundant (median rho approximately 0.943), while internal coherence and external coupling are inversely related in all 32 cancers.

## Stage A closure

Static Stage A is closed as a development measurement layer.

The retained static coordinates are independent observables, not a master stability score:

- V: expression-adjusted variability/fluctuation structure;
- L: lineage/context dependence;
- Cin: internal Hallmark-module coherence;
- Cout: coupling of Hallmark modules to the external Hallmark-union background.

No direction of any coordinate is defined as optimal. No static coordinate is chi.

## Current step

Stage B multiomic/context integration.

The immediate task is to freeze a source and harmonization plan for independently measured layers that can be matched to the PanCanAtlas sample/patient universe without using the Stage A network results to choose favorable features.

Priority candidate layers are broad-coverage TCGA measurements such as DNA methylation, protein abundance, copy-number/context, and independently sourced purity/composition measures. ATAC or other lower-coverage layers may be treated as secondary/validation strata rather than forced into the primary map.

## User action

None at this moment. Source selection, provenance review, and the Stage B acquisition/harmonization specification can be advanced in GitHub first. A local run will be requested only when a frozen Stage B data pull or computation actually benefits from the user's machine.

## Next scientific gate

Before any Stage B association is interpreted:

1. freeze data sources and versions;
2. freeze patient/sample matching rules;
3. freeze missingness/coverage requirements;
4. define each multiomic coordinate independently of Stage A outcomes;
5. define redundancy and incremental-information tests;
6. preserve static claim ceiling.

Dynamic benchmarking remains the next major branch after Stage B. Chi remains unavailable until genuine same-coordinate Gamma and Omega measurements satisfy the admission gates.
