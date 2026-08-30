# Stage B2 RPPA orthogonal-assay audit

Date: 2026-08-29

Status: COMPUTATIONALLY COMPLETE; RETAINED AS A STATIC CROSS-ASSAY COUPLING LAYER

## Scope

This audit covers the preregistered Stage B2 reverse-phase protein array (RPPA) branch. The branch tests whether the Stage A Hallmark RNA eigengenes show patient-aligned coupling to an independently measured protein/phosphoprotein panel beyond the finite-sample absolute-correlation floor created by random cross-assay alignment.

This is a static cross-assay analysis. It does not establish causality, dynamics, damping, a transition boundary, an optimum, treatment response, or a biological chi coordinate.

Machine-readable design: `config/stage_b2_integration_plan.json`.

## Input and implementation integrity

Frozen inputs were verified by SHA-256 before the run:

- Stage A profile cache: `e65f6788aa6037fef407169794f29d63322de2769343bb6e594fe469dfeb8e63`
- Stage A module eigengenes: `c305246d83732931060ff60049b67ce38751101e15b21798b973fcae8bb94433`
- Stage B1 matched context: `fe9221bdf7bfe94f3a53bbd9f01154142365e4328231d0c84f14406c432451dd`
- PanCanAtlas RPPA source: `06246573836865589134bd9424189f81b0d9fb436fcbf5e72024225442c400de`

The final RPPA source contains 198 protein/phosphoprotein measurement columns. The preregistered common-panel rule retained the 189 measurements with at least 95% finite values across all Stage-A-matched primary RPPA samples and nonzero finite variance. In the matched set, all 189 retained measurements are complete.

The primary cross-assay statistic was not altered after seeing results:

`RNA_RPPA_GLOBAL_COUPLING` = for each Hallmark RNA eigengene, the median absolute Pearson correlation across the fixed 189 RPPA measurements in the same n=30 patients.

The construction null permutes RPPA patient rows as a block relative to RNA. This preserves the protein-panel covariance structure and the fixed sample size while breaking patient-level RNA/protein alignment.

An initially incorrect synthetic unit-test expectation assumed one or two perfectly aligned proteins should force the median across the whole protein panel upward. That expectation was repaired before the biological run. The statistic itself was not changed. The replacement tests verify the median-correlation formula directly and verify that panel-wide alignment is broken by row permutation.

Final implementation tests: 10/10 PASS in the Stage B2 execution suite.

## Run closure

The completed RPPA run contains:

- 31 primary cancer tasks;
- 29 composition-sensitivity tasks;
- 60 total cancer/mode tasks;
- 100/100 valid resamples for every task;
- 50 Hallmark RNA modules for every task;
- 300,000 raw module-resample rows;
- 3,000 cancer-module summary rows;
- 60 cancer-level diagnostic rows.

UVM remains below the primary RPPA coverage gate. DLBC and THYM pass the primary RPPA gate but do not have at least 30 jointly matched RPPA + purity + leukocyte cases, so they are absent from the composition-sensitivity branch.

## Primary cross-assay result

Across the primary fixed-n resamples:

- median patient-aligned RNA/RPPA coupling = approximately `0.17664`;
- median row-permutation null coupling = approximately `0.12794`;
- median aligned-minus-null coupling = approximately `+0.04768`.

At the cancer-module summary level:

- 1,488 / 1,550 cancer-module median specific-coupling values are positive (96.0%);
- all 31 / 31 cancer-level medians are positive.

This establishes a reproducible patient-aligned static cross-assay relationship under the frozen construction null. It does not establish why the relationship exists.

## Composition sensitivity

The prespecified B1 sensitivity analysis residualized both the Hallmark RNA eigengenes and each RPPA feature on independently measured tumor purity plus methylation-derived leukocyte fraction before the cross-assay coupling was recalculated.

Across the 29 eligible cancers:

- median adjusted coupling = approximately `0.16820`;
- median adjusted row-permutation null = approximately `0.12736`;
- median adjusted aligned-minus-null coupling = approximately `+0.03989`;
- 1,432 / 1,450 cancer-module median specific-coupling values are positive;
- all 29 / 29 cancer-level medians are positive.

On the same context-sensitivity resamples, the median change in coupling after purity/leukocyte adjustment is small overall, approximately `-0.00205`, but the adjustment is not uniform across cancers or modules.

The median within-cancer Spearman agreement between raw and composition-adjusted module coupling ranks is approximately `0.812`, with substantial heterogeneity. GBM and CHOL show particularly low raw-versus-adjusted module-rank agreement in this development analysis. These cases are retained as context-sensitive rather than treated as failures or corrected away.

The interpretation is therefore two-part:

1. purity/leukocyte composition does not erase the pan-cancer patient-aligned RNA/protein coupling signal;
2. composition can materially reorganize which Hallmark RNA modules carry the strongest protein-panel coupling in individual cancers.

Neither the raw nor adjusted map is defined as the better state.

## Protein-only static coordinates

The preregistered protein-only coordinates are also retained as descriptive static measurements:

- median across cancer-level `RPPA_PAIRWISE_MEDIAN_ABS` values: approximately `0.2121`;
- median across cancer-level `RPPA_PC1_VARIANCE_FRACTION` values: approximately `0.2167`.

These values quantify protein-panel cofluctuation/coherence. Higher or lower values are not assigned an optimal, healthy, pathological, or stability direction.

## What the result does and does not earn

The RPPA branch earns retention of an orthogonal protein layer and a global RNA/protein cross-assay coupling coordinate for later model competition.

It supports the bounded statement:

> Hallmark-level RNA state in PanCanAtlas carries patient-aligned information that is detectably coupled to an independently measured 189-feature protein/phosphoprotein panel above a row-permutation construction floor, and most of that broad cross-assay coupling persists after adjustment for tumor purity and methylation-derived leukocyte fraction.

It does not establish:

- that the coupling is causal;
- that a specific RPPA feature belongs to or drives a Hallmark module;
- that the coupling is cancer-specific rather than reflecting a broad biological state shared across assays;
- that residual technical factors or unmeasured composition cannot contribute;
- that stronger coupling is better, worse, more stable, or closer to an optimum;
- that the coordinate predicts an independent outcome;
- that a biological chi coordinate exists.

No post-result significance threshold or p-value was introduced. The result is evaluated against the preregistered construction null and carried forward as a development coordinate for later held-out predictive model comparison.

## Output hashes

- `STAGE_B2_RPPA_SUMMARY.json`: `7e981badc16dc3da7b56defd14af7d043047fa75a0664f7c9d3fd858fb4b1af5`
- `stage_b2_rppa_cancer_diagnostic.csv`: `21c9cb8ddd780d65a1f0004de46661b8640afbc2f521a166e01883f93f297fde`
- `stage_b2_rppa_common_panel.txt`: `e923c7200e2b4485daafffc1d84f3a6b2f603fca30700227e14a757c1088bb7e`
- `stage_b2_rppa_module_effects.csv`: `cb619ae9a58e83e801674ae637d75de225fb26d6950b6299758b4e2865311b8f`
- `stage_b2_rppa_resample_metrics.csv.gz`: `1109a15f9f542aae21584c14d78e76ab347960641ec7ff2d17109a7f970c5d30`
- `stage_b2_rppa_task_status.csv`: `e7a2163b084d2f5da5d030a17e65aab99e0042e077f6494c5020f72d7301485b`

## Next gate

The RPPA arm is computationally closed. Stage B2 is not closed until the separately preregistered genomic decomposition finishes across all eligible cancer-coordinate tasks.

The genomic branch keeps the five documented genomic coordinates separate and tests both their primary RNA-map decomposition and their incremental contribution beyond Stage B1 purity/leukocyte composition. Partial genomic checkpoints are not biologically interpreted.
