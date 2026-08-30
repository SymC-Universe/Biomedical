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
- Stage B1 closed as a context/decomposition layer: composition contributes materially to a concentrated immune/inflammatory sector but does not erase the broader network topology.
- Stage B2 pre-reserved source probe completed after two mechanical workflow repairs that did not alter the scientific source contract.
- The final B2 source-probe workflow and the general GRI v2 test workflow pass.

## Stage B1 closure

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

## Stage B2 source closure

B2 sources were reserved before B1 results and therefore are not selected for favorable agreement with the network map.

Terminology:

- LOH = loss of heterozygosity.
- RPPA = reverse-phase protein array.
- `n` = sample count; the current primary coverage gate is at least 30 matched samples within a cancer type.

Final repaired source probe:

- Aneuploidy/LOH `ABSOLUTE_scores.tsv`: 456,006 bytes; SHA-256 `4e115fd7408a06b002f34678fa46df0b05aa20ac71db57acf535238f37aa64c8`; 9,167 Stage A matches; coverage gate passes 32/32 cancers.
- Copy-number `seg_based_scores.tsv`: 454,662 bytes; SHA-256 `4b63eefb164866a3c49c50c04ee423d3ad1c25540f7cf39e08d997b454a189d0`; 9,308 Stage A matches; gate passes 31/32 cancers. SKCM has no eligible primary-tumor source row and metastatic samples are not substituted.
- RPPA `TCGA-RPPA-pancan-clean.txt`: 18,901,234 bytes; SHA-256 `06246573836865589134bd9424189f81b0d9fb436fcbf5e72024225442c400de`; 6,887 Stage A matches, of which 6,884 are exact sample-root matches and 3 are unambiguous patient-level fallbacks; gate passes 31/32 cancers. UVM has 12 and is excluded from the primary RPPA cross-cancer layer.
- Merged 27K/450K methylation source: 5,022,150,019 bytes, deferred until a feature-reduction/harmonization plan is frozen.
- 450K-only methylation robustness source: 41,541,692,788 bytes, deferred unless a specific preregistered robustness need justifies acquisition.

The earlier current-GDC `/files/{uuid}` metadata lookup failure was a legacy-indexing issue, not a missing source. The repaired probe uses a one-byte range request against the working `/data/{uuid}` endpoint and successfully obtains full content length without downloading deferred large sources.

Full audit: `docs/STAGE_B2_SOURCE_AUDIT_20260829.md`.

## Current step

Freeze the Stage B2 biological coordinate and analysis contract before calculating any association with Stage A/B1 outcomes.

Immediate tasks:

1. define each genomic variable from source documentation rather than observed agreement with the RNA map;
2. freeze treatment of correlated genomic variables so redundancy is reported rather than hidden in a tuned composite;
3. freeze RPPA feature representation and missingness rules without RNA-outcome-guided feature selection;
4. define incremental-information tests against Stage A and B1 context baselines;
5. decide prospectively whether the approximately 5.02 GB merged methylation layer adds enough independent value to justify acquisition and, if used, freeze its feature reduction before download/analysis;
6. preserve the static claim ceiling.

## User action

None at this moment.

The B2 coordinate/source-documentation review and analysis preregistration can continue in GitHub. A local run will be requested only if the frozen analysis genuinely requires the user's machine or the deferred methylation source is prospectively admitted.

## Next scientific gate

No B2 biological association is interpreted until the coordinate definitions, missingness rules, redundancy checks, incremental-information tests, and any methylation acquisition decision are frozen.

Dynamic perturbation/time-course benchmarking remains the next major branch after static B2 integration. Chi remains unavailable until genuine same-coordinate Gamma and Omega measurements satisfy the admission gates.
