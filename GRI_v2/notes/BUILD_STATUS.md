# GRI v2 build status

Status date: 2026-08-30

## Scientific status

The active project is the Cancer Stability Atlas predictive-tool and substrate-architecture development program. The historical scalar branch remains closed. `CV/2` is historical only and no valid biological chi coordinate has been identified.

Chi, if later earned from genuine same-coordinate dynamic measurements, is a dynamical regime-balance coordinate. Distance to `chi = 1` does not define organization, coherence, health, optimality, pathology, or treatment response.

Stage B2 computation and static integration are closed. **Stage C0 DNA-methylation source acquisition/audit is now prospectively frozen and ready for local execution.** No methylation biological association has been inspected.

## Closed milestones

- GRI v1.1.6 historical scalar experiment audited and archived.
- Stage A0 variability/lineage primitives completed.
- Stage A1 Hallmark RNA network map completed on 9,546 unique-primary PanCanAtlas samples, 32 cancers, and 50 Hallmark modules.
- Stage A1.1 fixed-n construction calibration completed; Stage A closed with separate `V`, `L`, `C_in`, and `C_out` observables.
- Stage B1 independent tumor-purity / methylation-derived-leukocyte decomposition completed and audited.
- Stage B2 reserved-source probe completed and audited.
- Stage B2 coordinate/integration design frozen before any Stage A/B1/B2 association result.
- Stage B2 RPPA orthogonal-assay branch completed and audited.
- Stage B2 genomic decomposition completed and audited: 306/306 tasks, 100/100 resamples per task, 1,530,000 raw module-resample rows.
- Stage B2 static multiomic architecture integrated and closed without constructing a master score.
- Stage C0 methylation source contract frozen before methylation acquisition or association.
- Stage C0 metadata-only CI gate passed against the live GDC endpoint.

## Stage B2 closed architecture

The closed static evidence supports a layered representation:

1. Stage A RNA variability/lineage and Hallmark organization (`V`, `L`, `C_in`, `C_out`);
2. Stage B1 purity/leukocyte composition/context decomposition;
3. five separate Stage B2 genomic burden/decomposition coordinates;
4. Stage B2 orthogonal RPPA/protein coupling;
5. genome-wide methylation as the now-preregistered Stage C0/C1 regulatory-substrate extension;
6. future ordered/dynamic measurements kept separate from the static layers.

Full integration closure: `docs/STAGE_B2_STATIC_INTEGRATION_CLOSURE_20260830.md`.

### Genomic branch

The frozen genomic run completed 306/306 tasks with 100/100 resamples per task. Its specific effects are small and distributed, and reference-versus-adjusted Hallmark module ordering remains extremely stable. The genomic branch is retained as a weak static decomposition layer, not as a master organizer.

Full audit: `docs/STAGE_B2_GENOMIC_AUDIT_20260830.md`.

Canonical compact output: `development_outputs/stage_b2_genomic/STAGE_B2_GENOMIC_SUMMARY.json`.

Completion artifact:

- `CSA_STAGE_B2_GENOMIC_COMPLETED_20260830.zip`
- SHA-256 `cfa534417b4d3da028812503da49fb475b6b6427c2d563400095fc9d7fc9c9f5`

The 306 raw task-cache gzip files remain local for forensic re-audit and are identified individually by SHA-256 in `stage_b2_genomic_task_status.csv`. They are not required for ordinary next-stage analysis and should not be uploaded one by one.

### RPPA branch

The completed RPPA branch retains a reproducible patient-aligned RNA/protein relationship above its block-permutation construction floor, including after purity/leukocyte adjustment. It remains static and non-causal.

Full audit: `docs/STAGE_B2_RPPA_AUDIT_20260829.md`.

## Current step: Stage C0 DNA-methylation source gate

The primary methylation representation is now frozen **before download or biological association**.

Frozen source:

- PanCanAtlas merged HumanMethylation27/HumanMethylation450 beta-value matrix;
- GDC UUID `d82e2c44-89eb-43d9-b6d3-712732bf6a53`;
- expected size `5,022,150,019` bytes;
- expected GDC-manifest MD5 `5cec086f0b002d17befef76a3241e73b`;
- expected publication-era common representation: 22,601 probes.

The 41.54 GB 450K-only matrix remains separately deferred as robustness-only.

Frozen C0 records:

- `config/stage_c0_methylation_source_plan.json`
- `docs/STAGE_C0_METHYLATION_PREREGISTRATION_20260830.md`
- `src/probe_stage_c0_methylation.py`
- `tests/test_stage_c0_methylation_contract.py`
- `RUN_STAGE_C0_METHYLATION_WINDOWS.bat`

### Pre-acquisition validation

GitHub Actions run `33292691811` passed the Stage C0 gate on commit `009245507d8fc22740bc24f57f878a1fd73d5eb4`:

- full GRI v2 suite: 29/29 tests PASS;
- live GDC source probe: PASS;
- endpoint-reported content length: exactly `5,022,150,019` bytes;
- no biological association performed;
- tested Windows handoff artifact built successfully.

Execution handoff:

- `CSA_STAGE_C0_METHYLATION_WINDOWS_20260830.zip`
- SHA-256 `69dcaa00e96c9668c97b1b20047d121db3f61533f6e6f5bb55e41f22a11916eb`

The local source gate streams the large matrix rather than loading it into memory, verifies exact size, GDC MD5, SHA-256, 22,601 unique nonblank probe IDs, TCGA sample identifiers, and Stage A primary-tumor coverage. It writes only compact audit outputs.

C0 is forbidden from calculating methylation-RNA/RPPA/genomic/outcome associations, selecting probes from favorable outcomes, building Hallmark methylation scores, constructing a master stability score, or making substrate-inheritance/dynamic/chi claims.

## What follows C0

If the source/schema/coverage gate passes, the next stage is **not immediate association testing**. First, an annotation/feature-reduction protocol must prospectively freeze the annotation source, genome build, probe-to-gene/regulatory mapping, multi-mapping handling, promoter/regulatory-region definition, missing/unmapped handling, and construction nulls.

The later biological protocol must preserve three complementary views:

- **modal**: mode-resolved/eigenspectrum and participation structure;
- **scalar**: compressed coordinates only where empirically licensed;
- **conglomeration**: module-to-module and whole-system organization across layers.

The scalar view is not permitted to replace the modal or conglomeration views. None of these static methylation quantities is biological chi.

Substrate inheritance itself still requires ordered or temporal evidence. Static cross-assay relationships cannot establish inheritance. After the static regulatory extension is admitted or closed, the next major branch advances to ordered perturbation/time-course benchmarking.

## Next scientific gate

1. execute and audit Stage C0 source identity/schema/coverage;
2. freeze the methylation annotation and feature-reduction specification before biological association;
3. freeze the Stage C1 modal + scalar + conglomeration analysis and construction nulls;
4. only then calculate methylation relationships to the previously closed static layers;
5. advance to ordered perturbation/time-course benchmarking;
6. test biological chi only if genuine same-coordinate `Gamma` and `Omega` satisfy `docs/CHI_ADMISSION_RULES.md`.

## Exact user action

1. Download and extract `CSA_STAGE_C0_METHYLATION_WINDOWS_20260830.zip`.
2. Double-click `RUN_STAGE_C0_METHYLATION_WINDOWS.bat`.
3. When prompted, select the existing completed Stage A `hallmark_profile_cache.npz`.
4. Leave the run active. The approximately 5.02 GB source download uses a resumable `.part` file.
5. When `STAGE C0 METHYLATION SOURCE GATE COMPLETE` appears, return only:
   - `stage_c0_methylation_outputs/STAGE_C0_METHYLATION_SOURCE_SUMMARY.json`
   - `stage_c0_methylation_outputs/stage_c0_methylation_cancer_coverage.csv`

Keep the downloaded methylation matrix and the existing B2 `_task_cache` local and unchanged. Neither should be uploaded to ChatGPT or committed to GitHub.
