# GRI v2 build status

Status date: 2026-08-29

## Scientific status

The active project is the Cancer Stability Atlas predictive-tool development program. The historical scalar branch remains closed; `CV/2` is historical only and no valid biological chi coordinate has yet been identified.

Chi, if later earned from genuine dynamic measurements, is a dynamical regime-balance coordinate. Distance to `chi = 1` does not define organization, coherence, health, optimality, or pathology.

## Completed

- GRI v1.1.6 scalar experiment audited and archived.
- Stage A0 static variability/lineage primitives completed.
- Stage A1 Hallmark network run completed on 9,546 unique-primary PanCanAtlas samples across 32 cancers and 50 Hallmark modules.
- Stage A1.1 fixed-n construction calibration completed and Static Stage A closed with separate V, L, Cin, and Cout coordinates and no optimum or chi interpretation.
- Stage B0 official-source probe completed successfully in GitHub Actions using the PanCanAtlas publication-era supplemental data family.
- Primary B1 context sources are frozen as ABSOLUTE tumor purity and DNA-methylation-derived leukocyte fraction. RNA-derived CIBERSORT is secondary sensitivity only.
- Exact Stage A matching is complete. Purity matches 8,750 Stage A samples and clears n>=30 in all 32 cancers. Leukocyte fraction matches 9,310 and clears n>=30 in 30 cancers; DLBC and THYM are absent from that assay. The joint independent set contains 8,541 samples across those 30 cancers.
- Stage B1 paired context-adjustment experiment was frozen before any purity/leukocyte-network association result.
- An exact accelerated network implementation was regression-tested against the frozen Stage A implementation to numerical tolerance without changing the metrics.
- Local Stage B1 computation completed all frozen tasks: 32 PURITY + 30 LEUKOCYTE + 30 JOINT_INDEPENDENT cancer-model jobs, each at 100/100 valid resamples. The expensive network calculation therefore completed successfully.

## Current step

Recover the compact Stage B1 summaries from the already-written raw B1 resample table.

The Windows run crashed only after all 92 cancer-model jobs completed and after `stage_b1_resample_metrics.csv.gz` had been combined. The exception occurred in summary generation because pandas `DataFrame.resample` shadowed the raw column named `resample` when attribute-style access was used.

This is an execution/postprocessing defect, not a scientific or computational failure. No B1 network metric needs to be recomputed.

The canonical GitHub Windows runner now uses a collision-safe summarizer with explicit `rawg["resample"]` column access, and a regression test covers this exact failure mode.

## Exact user action

Run the Stage B1 summary-recovery handoff. Select the existing `stage_b1_outputs/stage_b1_resample_metrics.csv.gz` produced by the completed B1 run.

The recovery validates the full expected structure before summarizing:

- 92 cancer-model tasks;
- 100 resamples per task;
- 50 Hallmark modules per resample;
- 460,000 raw rows total.

It then writes, without recomputation:

- `STAGE_B1_SUMMARY.json`
- `stage_b1_module_context_effects.csv`
- `stage_b1_cancer_level_diagnostic.csv`

Return those three compact outputs for scientific audit. Keep the raw resample table locally unless deeper audit requires it.

## After recovery

Audit whether Stage A topology survives independent purity/leukocyte adjustment beyond the permuted-residualization null. If it does, proceed to B2 orthogonal genomic/protein/methylation layers. If composition materially changes it, retain both unadjusted and context-adjusted coordinates and carry that dependence forward rather than labeling either direction as better.

Dynamic benchmarking remains the next major branch after static context integration. Chi remains unavailable until genuine same-coordinate Gamma and Omega measurements satisfy the admission gates.
