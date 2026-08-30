# GRI v2 build status

Status date: 2026-08-30

## Scientific status

The active project is the Cancer Stability Atlas predictive-tool development program. The historical scalar branch remains closed. `CV/2` is historical only and no valid biological chi coordinate has been identified.

Chi, if later earned from genuine same-coordinate dynamic measurements, is a dynamical regime-balance coordinate. Distance to `chi = 1` does not define organization, coherence, health, optimality, pathology, or treatment response.

Stage B2 computation is now closed. The current task is to integrate the completed static RNA, composition, genomic, and protein layers without collapsing them into a master score, then freeze the next modal + scalar + conglomeration architecture before any new predictive or dynamic endpoint is tested.

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

## Stage B1 closure

Independent tumor purity and methylation-derived leukocyte fraction explain a real but concentrated portion of the Stage A network geometry, especially immune/inflammatory Hallmarks. They do not erase the broader internal-coherence/external-coupling topology.

Both raw and adjusted maps are retained. Composition-sensitive modules are context/decomposition information, not failed modules and not evidence that an adjusted state is better.

Full audit: `docs/STAGE_B1_AUDIT_20260829.md`.

## Stage B2 RPPA closure

The RPPA branch shows a reproducible patient-aligned static RNA/protein relationship above its block-permutation construction floor:

- primary median aligned-minus-null coupling approximately `+0.04768`;
- all 31/31 primary cancer-level medians positive;
- composition-adjusted median aligned-minus-null coupling approximately `+0.03989`;
- all 29/29 eligible adjusted cancer-level medians positive.

This earns retention of an orthogonal protein layer and a global RNA/protein cross-assay coupling coordinate for later model competition. It does not establish causality, pathway-specific protein control, an optimum, dynamics, or chi.

Full audit: `docs/STAGE_B2_RPPA_AUDIT_20260829.md`.

## Stage B2 genomic closure

The frozen genomic branch is complete:

- 306/306 cancer-coordinate-analysis tasks;
- 158 `PRIMARY` tasks;
- 148 `INCREMENT_B1` tasks;
- fixed `n = 30`;
- 100/100 valid resamples per task;
- 50 Hallmark modules per task;
- 15,300 module-summary rows;
- 1,530,000 raw module-resample rows.

All five documented genomic coordinates remained separate. No genomic composite was created.

Across primary tasks, cancer-level specific shifts relative to the same-patient permuted-genomic construction null were small:

- `C_in` pairwise coherence median approximately `-0.000481`;
- `C_in` PC1 variance fraction median approximately `+0.000688`;
- `C_out` coupling median approximately `+0.000948`.

The same bounded pattern persists beyond Stage B1 composition, with similarly small median shifts. Module ordering remains extremely stable after genomic adjustment: coordinate-level median reference-versus-adjusted Spearman agreement is approximately 0.993-0.997 for the two internal-coherence metrics and approximately 0.984-0.988 for `C_out`.

The genomic result therefore earns retention as a weak distributed static decomposition layer. It does not support treating genomic burden as a master organizer or as a biological chi coordinate.

Full audit: `docs/STAGE_B2_GENOMIC_AUDIT_20260830.md`.

Canonical compact output:

- `development_outputs/stage_b2_genomic/STAGE_B2_GENOMIC_SUMMARY.json`

Completion artifact:

- `CSA_STAGE_B2_GENOMIC_COMPLETED_20260830.zip`
- SHA-256 `cfa534417b4d3da028812503da49fb475b6b6427c2d563400095fc9d7fc9c9f5`

The 306 raw task-cache gzip files remain local for forensic re-audit and are identified individually by SHA-256 in `stage_b2_genomic_task_status.csv`. They are not required for ordinary next-stage analysis and should not be uploaded one by one.

## Current step: Stage B2 static integration closure

The next scientific product is an integrated static architecture that keeps distinct measurement roles visible:

1. Stage A RNA map: `V`, `L`, `C_in`, `C_out`;
2. Stage B1 composition/context decomposition;
3. Stage B2 genomic decomposition using five separate documented coordinates;
4. Stage B2 orthogonal RPPA/protein coupling;
5. deferred methylation as a separately gated extension.

No master stability score will be constructed at this stage.

The integration will explicitly preserve three complementary views for the next investigation:

- **modal**: mode-resolved/eigenstructure and participation information;
- **scalar**: compressed coordinates only where empirically licensed, without treating a scalar as the whole system;
- **conglomeration**: module-to-module and whole-system organization across measurement layers.

The three views are complementary. A later scalar coordinate may summarize structure but cannot replace the modal or conglomeration evidence that gives it meaning.

## Next scientific gate

1. write and freeze the Stage B2 integrated static-architecture closure;
2. explicitly close or prospectively admit the genome-wide methylation extension under an independent feature-reduction/platform-harmonization rule;
3. preregister the next modal + scalar + conglomeration analysis before testing any new endpoint;
4. advance to ordered perturbation/time-course benchmarking against established dynamic and predictive baselines;
5. admit a biological chi coordinate only if genuine same-coordinate relaxation and intrinsic-response rates satisfy `docs/CHI_ADMISSION_RULES.md`.

No dynamic or chi claim is available from Stage B2.

## Exact user action

No new computation or upload is required right now.

Keep the local `_task_cache` directory intact and unchanged. It is only needed if a forensic re-audit requests raw reconstruction of a specific task.
