# GRI v2 build status

Status date: 2026-08-29

## Scientific status

The active project is the Cancer Stability Atlas predictive-tool development program. The historical scalar branch remains closed. `CV/2` is historical only and no valid biological chi coordinate has been identified.

Chi, if later earned from genuine same-coordinate dynamic measurements, is a dynamical regime-balance coordinate. Distance to `chi = 1` does not define organization, coherence, health, optimality, pathology, or treatment response.

## Closed milestones

- GRI v1.1.6 historical scalar experiment audited and archived.
- Stage A0 variability/lineage primitives completed.
- Stage A1 Hallmark RNA network map completed on 9,546 unique-primary PanCanAtlas samples, 32 cancers, and 50 Hallmark modules.
- Stage A1.1 fixed-n construction calibration completed; Stage A closed with separate `V`, `L`, `C_in`, and `C_out` observables.
- Stage B1 independent tumor-purity / methylation-derived-leukocyte decomposition completed and audited.
- Stage B2 reserved-source probe completed and audited.
- Stage B2 coordinate/integration design frozen before any Stage A/B1/B2 association result.
- Stage B2 RPPA orthogonal-assay branch completed and audited.

## Stage B1 closure

Independent tumor purity and methylation-derived leukocyte fraction explain a real but concentrated portion of the Stage A network geometry, especially immune/inflammatory Hallmarks. The broader internal-coherence/external-coupling topology remains strongly preserved after adjustment.

Both raw and adjusted maps are retained. Composition-sensitive modules are context/decomposition information, not failed modules and not evidence that an adjusted state is better.

Full audit: `docs/STAGE_B1_AUDIT_20260829.md`.

## Stage B2 source and preregistration closure

The B2 sources were reserved before B1 results. The frozen B2 integration plan is `config/stage_b2_integration_plan.json`; scientific rationale is `docs/STAGE_B2_PREREGISTRATION_20260829.md`.

Five documented genomic coordinates are retained separately:

1. `ANEUPLOIDY_AS` - arm-level aneuploidy count;
2. `LOH_SEGMENT_COUNT` - number of loss-of-heterozygosity segments;
3. `LOH_GENOME_FRACTION` - fraction of the genome with LOH;
4. `SCNA_SEGMENT_COUNT` - copy-number segment count;
5. `SCNA_ALTERED_FRACTION` - fraction of profiled base pairs in altered copy-number segments.

No genomic master score is created. `ASprime` and `n_extrema` remain non-primary because sufficiently explicit primary-source definitions were not verified before association testing.

The RPPA primary panel contains 189 common protein/phosphoprotein measurements selected only by the frozen source-completeness/variance rule.

Full source audit: `docs/STAGE_B2_SOURCE_AUDIT_20260829.md`.

## Stage B2 RPPA closure

The RPPA branch is computationally complete:

- 31 primary cancer tasks;
- 29 purity/leukocyte context-sensitivity tasks;
- 60 total tasks;
- 100/100 valid resamples per task;
- 50 Hallmark modules per task;
- 300,000 module-resample rows.

Primary fixed-n RNA/protein coupling:

- median patient-aligned coupling approximately `0.17664`;
- median row-permutation construction null approximately `0.12794`;
- median aligned-minus-null approximately `+0.04768`;
- all 31/31 cancer-level median specific-coupling values are positive.

After B1 purity/leukocyte adjustment:

- median adjusted coupling approximately `0.16820`;
- median adjusted null approximately `0.12736`;
- median adjusted aligned-minus-null approximately `+0.03989`;
- all 29/29 eligible cancer-level median specific-coupling values are positive.

This earns retention of a static orthogonal protein layer and global RNA/protein cross-assay coupling coordinate for later predictive model competition. It does not establish causality, pathway-specific protein control, an optimum, dynamics, or chi.

Full audit: `docs/STAGE_B2_RPPA_AUDIT_20260829.md`.

## Current step: Stage B2a genomic execution

The remaining B2 closure computation is the preregistered genomic decomposition.

For each eligible cancer and each of the five genomic coordinates the frozen run uses:

- fixed `n = 30` patients;
- 100 deterministic without-replacement resamples;
- unchanged Stage A `C_in` pairwise, `C_in` PC1, and `C_out` metrics;
- an actual genomic residualization;
- a same-patient construction null with the genomic coordinate permuted;
- a secondary `INCREMENT_B1` branch testing the genomic coordinate after purity + leukocyte composition is already accounted for.

The full design contains 306 eligible cancer-coordinate-analysis tasks. Partial checkpoints are not biologically interpreted.

## Execution status

The Stage B2 genomic runner is implemented in `src/run_stage_b2_genomic.py` and the restart-safe executor in `src/run_stage_b2_genomic_resume.py`.

The restart-safe executor:

- writes every completed 100-resample task atomically;
- records SHA-256 hashes for each task's raw, module-summary, and diagnostic checkpoint;
- validates those hashes before reusing a checkpoint;
- resumes only unfinished tasks after interruption;
- keeps raw task files separate so final summarization does not require loading the entire 1.53-million-row run into memory at once.

The B2 implementation suite passes locally and the latest GitHub `GRI v2 tests` workflow passes on commit `f28bcf1cb8c1823363b7a1b9ff7ab69c2f71e71e`.

Local execution handoff:

- `CSA_STAGE_B2_GENOMIC_RESUMABLE_20260829.zip`
- SHA-256 `a153f54ac0d0ac5d48cb8951a5aff8e8914e0652ce73f9e1c6183e63eaf09b2a`
- clean-room manifest verification PASS;
- clean-room test suite 10/10 PASS;
- includes the completed Stage B2 RPPA outputs as reference artifacts.

## Exact user action

Run `RUN_STAGE_B2_GENOMIC_WINDOWS.bat` from the Stage B2 handoff package and select the existing Stage A `hallmark_profile_cache.npz` when asked.

If the process is interrupted, launch the same BAT again and select the same cache. Valid completed tasks are reused automatically.

When `STAGE B2A GENOMIC COMPLETE` appears, return these four files from `stage_b2_genomic_outputs`:

- `STAGE_B2_GENOMIC_SUMMARY.json`
- `stage_b2_genomic_module_effects.csv`
- `stage_b2_genomic_cancer_diagnostic.csv`
- `stage_b2_genomic_task_status.csv`

Keep `_task_cache` locally unless a forensic re-audit specifically requests it.

## Next scientific gate

After the complete genomic output is returned:

1. verify all 306 frozen tasks and 100/100 resamples;
2. audit each genomic coordinate against its construction null;
3. distinguish primary genomic decomposition from incremental information beyond B1 composition;
4. integrate the genomic and RPPA B2 results without collapsing them into a master stability score;
5. close or explicitly defer the genome-wide methylation extension under its independent acquisition/harmonization gate;
6. then advance to ordered perturbation/time-course benchmarking.

No dynamic or chi claim is available from Stage B2.
