# GRI v2 build status

Status date: 2026-08-30

## Scientific status

The active project is the Cancer Stability Atlas predictive-tool and substrate-architecture development program. The historical scalar branch remains closed. `CV/2` is historical only and no valid biological chi coordinate has been identified.

Chi, if later earned from genuine same-coordinate dynamic measurements, is a dynamical regime-balance coordinate. Distance to `chi = 1` does not define organization, coherence, health, optimality, pathology, or treatment response.

Stage B2 computation and static integration are now closed. The active step is prospective design of the next substrate investigation before any new endpoint is inspected.

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

## Stage B2 closed architecture

The closed static evidence supports a layered representation:

1. Stage A RNA variability/lineage and Hallmark organization (`V`, `L`, `C_in`, `C_out`);
2. Stage B1 purity/leukocyte composition/context decomposition;
3. five separate Stage B2 genomic burden/decomposition coordinates;
4. Stage B2 orthogonal RPPA/protein coupling;
5. genome-wide methylation retained only as a prospectively gated extension;
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

## Current step: prospective substrate extension design

The next investigation must be frozen before new association, prediction, or dynamic outcomes are inspected.

The architecture will preserve three complementary views:

- **modal**: mode-resolved/eigenspectrum and participation structure;
- **scalar**: compressed coordinates only where empirically licensed;
- **conglomeration**: module-to-module and whole-system organization across layers.

The scalar view is not permitted to replace the modal or conglomeration views.

### Methylation gate

Genome-wide methylation remains deferred, not rejected. The exact PanCanAtlas merged 27K/450K source is already reserved and is approximately 5.02 GB. Published PanCanAtlas processing indicates that this merged source uses between-platform normalization and a common 22,601-probe representation.

No methylation association result will be inspected until a prospective specification freezes platform handling, feature reduction, matching, construction nulls, context sensitivity, and claim ceiling. The 41.54 GB 450K-only source remains robustness-only and will not be casually acquired.

### Dynamic gate

Substrate inheritance itself still requires ordered or temporal evidence. Static cross-assay relationships cannot establish inheritance. After the static regulatory extension is either admitted or closed, the next major branch will benchmark ordered perturbation/time-course data against established predictive and dynamical baselines.

## Next scientific gate

1. freeze the methylation extension specification or explicitly close it without inspecting its association results;
2. freeze the next modal + scalar + conglomeration protocol before new endpoints;
3. build/test the corresponding execution engine and construction nulls;
4. only then acquire/run the required next dataset;
5. advance to ordered perturbation/time-course benchmarking;
6. test biological chi only if genuine same-coordinate `Gamma` and `Omega` satisfy `docs/CHI_ADMISSION_RULES.md`.

No dynamic or chi claim is available from Stage B2.

## Exact user action

No new upload or computation is required right now.

Keep the local `_task_cache` directory intact and unchanged. It is only needed if a forensic re-audit requests raw reconstruction of a specific task.
