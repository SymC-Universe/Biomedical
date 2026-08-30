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
- Stage B1 composition/context experiment was frozen before biological results and completed as 92 cancer-model tasks x 100 resamples x 50 modules = 460,000 module-resample rows.
- Recovery summarized the completed B1 raw table without recomputation after the original postprocessing-only pandas name-collision failure.

## Stage B1 closure

Stage B1 is closed as a composition/context decomposition layer.

Independent tumor purity and methylation-derived leukocyte fraction explain a real but concentrated portion of the Stage A network geometry. They do not erase the broader map.

Under the JOINT_INDEPENDENT adjustment:

- median baseline-versus-adjusted module rank rho is approximately 0.931 for pairwise Cin, 0.896 for PC1 coherence, and 0.890 for Cout;
- 29/30 cancers retain pairwise Cin module-rank rho >=0.8, 25/30 retain PC1 rho >=0.8, and 27/30 retain Cout rho >=0.8;
- the median context-specific pairwise-Cin shift is approximately -0.00527 on a baseline median approximately 0.1982, a typical relative change of about -2.7%;
- joint-adjusted pairwise Cin versus Cout remains negatively related in 30/30 cancers;
- joint-adjusted PC1 versus Cout remains negative in 29/30 cancers, with UVM the sole near-zero/slightly positive exception;
- the strongest reproducible composition-sensitive effects are concentrated in immune/inflammatory Hallmarks, especially allograft rejection, interferon responses, IL6/JAK/STAT3, inflammatory response, and TNF/NF-kB.

The interpretation is not that composition is noise or that adjustment improves the system. Both unadjusted and adjusted information are retained. Composition-sensitive modules carry explicit context/decomposition status rather than being treated as intrinsic tumor-cell organization.

Full audit: `docs/STAGE_B1_AUDIT_20260829.md`.

## Current step

Stage B2 orthogonal static integration.

B2 sources were reserved before B1 results and therefore are not selected for favorable agreement with the network map. The immediate candidate layers are:

1. copy-number/genomic context from the reserved PanCanAtlas ABSOLUTE/segmentation-derived score files;
2. RPPA protein-abundance measurements as an orthogonal assay;
3. PanCanAtlas DNA methylation as a deeper substrate/state layer, subject to coverage and data-volume review before full acquisition.

B1 context variables are carried forward as covariates/decomposition coordinates where appropriate. They do not determine which B2 features are admitted.

## User action

None at this moment.

B2 source metadata, exact coverage, acquisition size, harmonization rules, and incremental-information tests should be frozen in GitHub before another local computation is requested. A local run will be used only if the frozen B2 data volume or computation makes the user's machine the appropriate execution engine.

## Next scientific gate

Before B2 biological interpretation:

1. verify reserved source identity and publication-era provenance;
2. freeze exact sample/patient matching and coverage gates;
3. define each B2 coordinate independently of Stage A/B1 outcomes;
4. distinguish redundant context from genuinely incremental orthogonal information;
5. retain both raw and context-adjusted relationships where B1 composition materially matters;
6. preserve the static claim ceiling.

Dynamic perturbation/time-course benchmarking remains the next major branch after static B2 integration. Chi remains unavailable until genuine same-coordinate Gamma and Omega measurements satisfy the admission gates.
