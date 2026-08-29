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
- The raw finite-sample dependence is removed by fixed-n calibration while module topology is strongly preserved.
- Static Stage A is closed with separate V, L, Cin, and Cout coordinates and no optimum or chi interpretation.
- Stage B0 official-source probe completed successfully in GitHub Actions using the PanCanAtlas publication-era supplemental data family.
- Primary B1 context sources are frozen as ABSOLUTE tumor purity and DNA-methylation-derived leukocyte fraction. RNA-derived CIBERSORT is secondary sensitivity only.
- Exact Stage A matching is complete. Purity matches 8,750 Stage A samples and clears n>=30 in all 32 cancers. Leukocyte fraction matches 9,310 and clears n>=30 in 30 cancers; DLBC and THYM are absent from that assay. The joint independent set contains 8,541 samples across those 30 cancers.
- Sample matching is overwhelmingly exact through the TCGA primary-sample vial: 8,748/8,750 purity matches and 9,309/9,310 leukocyte matches. Only three total unambiguous patient-level fallbacks are used.
- Stage B1 paired context-adjustment experiment is frozen before any purity/leukocyte-network association result.
- An exact accelerated network implementation has been regression-tested against the frozen Stage A implementation to numerical tolerance, without changing the metrics.

## Current step

Stage B1 composition/context adjustment.

For each eligible cancer and model, the same deterministic n=30 samples are used for:

1. the unadjusted Stage A network baseline;
2. expression residualized against the real context covariate(s);
3. expression residualized against a deterministic within-resample permutation of the same context covariate(s).

The third arm is a construction-aware null for generic changes caused by fitting/residualization itself.

Models:

- PURITY: 32 cancers;
- LEUKOCYTE: 30 cancers, excluding DLBC and THYM;
- JOINT_INDEPENDENT: purity + leukocyte, same 30 cancers.

Every model uses 100 deterministic n=30 resamples and unchanged Cin_pairwise, Cin_pc1, and Cout definitions. No chi, CV/2, composite stability score, causal claim, or optimum claim is permitted.

## Execution status

GitHub now contains the frozen B1 plan, exact source hashes, source/coverage records, matching rules, accelerated implementation, and contract tests.

The full B1 calculation requires the 126 MB Stage A Hallmark expression cache. That cache is intentionally not committed to repository history. The current ChatGPT execution environment cannot complete the full 100-resample B1 matrix within its per-command execution ceiling, so the unchanged frozen computation should run on the local Windows machine using the compact B1 handoff.

## Exact user action

Run the Stage B1 Windows handoff package when provided. Select the existing `hallmark_profile_cache.npz` and `hallmark_membership_snapshot.gmt`. The official ABSOLUTE and leukocyte source files are bundled and hash-verified; the 1.88 GB PanCanAtlas matrix is not required.

Return the compact B1 summary/module/cancer outputs. The larger raw resample output can remain local unless audit requires it.

## After B1

Audit whether the Stage A topology survives independent composition adjustment beyond the permuted-residualization null. If it does, proceed to B2 orthogonal genomic/protein/methylation layers. If it materially changes, retain both unadjusted and context-adjusted coordinates and carry that dependence forward rather than labeling either direction as better.

Dynamic benchmarking remains the next major branch after static context integration. Chi remains unavailable until genuine same-coordinate Gamma and Omega measurements satisfy the admission gates.
