# Stage B2 genomic decomposition audit

Date: 2026-08-30

Status: COMPUTATIONALLY COMPLETE; RETAINED AS A WEAK DISTRIBUTED STATIC GENOMIC DECOMPOSITION LAYER

## Scope

This audit closes the preregistered Stage B2 genomic branch. The branch asks whether five pre-reserved genomic coordinates account for reproducible structure in the Stage A Hallmark RNA map beyond the generic effect of fitting a covariate, and whether any such information remains after the already-audited Stage B1 purity/leukocyte composition adjustment.

The frozen design is `config/stage_b2_integration_plan.json`. It was fixed before Stage A/B1/B2 biological association results were inspected.

This is a static decomposition analysis. It does not establish causality, dynamics, damping, a transition or phase boundary, criticality, an optimum, treatment response, or a biological chi coordinate.

## Frozen genomic coordinates

The five coordinates remained separate throughout the run:

- `ANEUPLOIDY_AS`
- `LOH_SEGMENT_COUNT`
- `LOH_GENOME_FRACTION`
- `SCNA_SEGMENT_COUNT`
- `SCNA_ALTERED_FRACTION`

No genomic burden composite was created. `ASprime` and `n_extrema` remained outside the primary analysis because their primary-source definitions had not been sufficiently verified before association testing.

## Run closure and mechanical integrity

The returned canonical outputs report:

- 306 / 306 frozen cancer-coordinate-analysis tasks completed;
- 158 `PRIMARY` tasks;
- 148 prespecified `INCREMENT_B1` tasks;
- fixed `n = 30` patients per resample;
- 100 / 100 valid resamples for every task;
- 50 Hallmark modules for every task;
- 5,000 raw rows per task;
- 1,530,000 raw module-resample rows total;
- 15,300 module-summary rows;
- 306 cancer-level diagnostic rows;
- no missing values in the three returned tabular canonical outputs;
- zero duplicate cancer-coordinate-analysis task keys;
- task indices 0 through 305 with all 306 indices present;
- one syntactically valid 64-character SHA-256 entry for each raw, module-summary, and diagnostic task artifact, with 306 unique values in each hash field.

The task-cache files themselves remain local because the restart-safe executor intentionally stores one compressed raw file per task. The returned `stage_b2_genomic_task_status.csv` preserves each task's raw/module/diagnostic SHA-256. This audit verifies the ledger structure and all compact returned outputs, but it does not claim an independent byte-for-byte re-hash of all 306 local raw cache files because those files were not transferred for this audit. They must remain untouched locally for forensic reconstruction if later requested.

## Output hashes

- `STAGE_B2_GENOMIC_SUMMARY.json`: `b564f06ba77940ba9c92e6ed2a31c91d7f10965dfea0be48ea894a8ecdaf3064`
- `stage_b2_genomic_cancer_diagnostic.csv`: `c95407fd9019af846ef9c7708d89200ebc42af8391d18815841515b62fcbb9d0`
- `stage_b2_genomic_module_effects.csv`: `4d63690e0a1b1da4cd566bc49006cd9c6c41f1e1a118de2e473d2a298c6aa8bf`
- `stage_b2_genomic_task_status.csv`: `c90c0ab56484d1fe97d3e6eac2de47f2957bf3101dd292fe286e70f31becf614`

Reviewer completion bundle:

- `CSA_STAGE_B2_GENOMIC_COMPLETED_20260830.zip`
- SHA-256: `cfa534417b4d3da028812503da49fb475b6b6427c2d563400095fc9d7fc9c9f5`
- contents: the four exact canonical outputs above plus `SHA256SUMS.txt`.

## Primary genomic decomposition result

The frozen primary effect is the actual genomic-residualized network metric minus the same-patient permuted-genomic-null residualized metric.

Across all 158 primary cancer-coordinate tasks, the median cancer-level specific shifts were small:

- `C_in` pairwise median absolute correlation: approximately `-0.000481`; 101 / 158 task medians were negative;
- `C_in` PC1 variance fraction: approximately `+0.000688`; 114 / 158 task medians were positive;
- `C_out` eigengene median absolute coupling: approximately `+0.000948`; 103 / 158 task medians were positive.

These directions are descriptive consequences of residualization and are not assigned a better/worse or stability interpretation.

The critical structural observation is preservation rather than collapse. Across the five genomic coordinates, the median within-cancer Spearman agreement between the reference and genomic-adjusted 50-module orderings was approximately:

- `0.9954` to `0.9966` for `C_in` pairwise coherence;
- `0.9935` to `0.9964` for `C_in` PC1 variance fraction;
- `0.9856` to `0.9875` for `C_out` coupling.

Thus the genomic adjustments leave the Stage A Hallmark topology almost entirely intact at the rank level.

At the module level, the median absolute specific shift relative to each module's reference magnitude was also small across coordinates:

- approximately `0.48%` to `0.66%` for `C_in` pairwise coherence;
- approximately `0.72%` to `1.11%` for `C_in` PC1 variance fraction;
- approximately `0.67%` to `1.03%` for `C_out` coupling.

The empirical 5th-to-95th resample interval for the module-specific effect crossed zero for the overwhelming majority of cancer-module rows. Across all primary module rows, only about 0.96% of `C_in` pairwise, 1.14% of PC1, and 0.76% of `C_out` intervals excluded zero. These are empirical resample intervals, not newly introduced post-result significance thresholds.

The primary result therefore does not support a broad claim that genomic burden reorganizes Hallmark network architecture. It supports a more limited result: the admitted genomic coordinates carry small, distributed static information relative to the construction null while the dominant module ordering is preserved.

## Increment beyond Stage B1 composition

The secondary analysis was frozen before results and restricted to the 148 cancer-coordinate tasks with at least 30 jointly matched samples carrying purity, methylation-derived leukocyte fraction, and the genomic coordinate.

After preserving purity/leukocyte adjustment and testing only the additional genomic coordinate against its permutation null, the median cancer-level specific shifts remained small:

- `C_in` pairwise coherence: approximately `-0.000280`; 95 / 148 task medians negative;
- `C_in` PC1 variance fraction: approximately `+0.000753`; 121 / 148 task medians positive;
- `C_out` coupling: approximately `+0.000881`; 107 / 148 task medians positive.

Module-rank preservation remained extremely high:

- median coordinate-level rank agreement approximately `0.9950` to `0.9964` for `C_in` pairwise coherence;
- approximately `0.9945` to `0.9962` for PC1 variance fraction;
- approximately `0.9841` to `0.9875` for `C_out` coupling.

The median absolute module-level specific effect relative to the reference remained below approximately 1% across the five coordinates for all three metrics. The empirical 5th-to-95th resample interval excluded zero in only about 0.46% of `C_in` pairwise rows, 0.68% of PC1 rows, and 0.11% of `C_out` rows.

The paired primary-versus-`INCREMENT_B1` tasks show that the genomic signal is not simply identical to the Stage B1 composition signal, but its magnitude remains modest and its effect is predominantly distributed rather than a strong module-selective reorganization.

## Relationship to the Stage A/B1 topology

The inverse `C_in`/`C_out` relationship remains negative after genomic residualization. Across coordinates, median cancer-level reference and adjusted correlations move only modestly. The result is therefore consistent with the earlier conclusion that composition explains a concentrated part of the network geometry while neither the admitted composition variables nor these five genomic burden coordinates erase the broader Hallmark topology.

## What the result earns

The genomic branch earns retention of the five documented genomic coordinates as separate static decomposition axes for later model competition.

A bounded statement supported by this branch is:

> Across the frozen PanCanAtlas Stage B2 design, five independently documented genomic burden coordinates produce small but directionally non-random distributed changes in Hallmark RNA coherence/coupling relative to same-patient permutation residualization, including after purity/leukocyte adjustment, while preserving the overwhelming majority of the Stage A module ordering.

The phrase `directionally non-random` here refers descriptively to repeated cancer-level effect directions under the frozen construction-null comparison. No post-result p-value or significance threshold is introduced as a promotion criterion.

The result does not establish:

- that genomic burden is the causal substrate of the RNA topology;
- that one genomic coordinate is the preferred master variable;
- that the five coordinates should be combined into a score;
- that any direction is healthier, more pathological, more stable, or closer to an optimum;
- that individual Hallmark modules have robust genomic-specific effects unless separately prospectively validated;
- that static genomic decomposition implies a dynamical mechanism;
- that a biological chi coordinate exists.

## Stage B2 closure interpretation

Stage B2 now contains two orthogonal findings that should remain distinct:

1. the RPPA branch shows a reproducible patient-aligned RNA/protein cross-assay coupling above its block-permutation construction floor, including after composition adjustment;
2. the genomic branch shows much smaller distributed residualization effects with very high preservation of the Hallmark module topology, including beyond Stage B1 composition.

Their effect sizes are not directly comparable because the coordinates and construction-null statistics differ. The combined lesson is architectural rather than scalar: the static cancer state contains multiple partially related measurement layers that should not be collapsed into a single master stability score at this stage.

## Next gate

Stage B2 computation is closed.

The next sequence is:

1. integrate Stage A, B1, genomic B2, and RPPA B2 as a multi-axis static architecture without a master score;
2. explicitly close or prospectively admit the deferred genome-wide methylation extension under its independent acquisition/harmonization gate;
3. freeze the next modal + scalar + conglomeration analysis architecture before testing any new predictive or dynamic endpoint;
4. then advance to ordered perturbation/time-course benchmarking against established dynamic and predictive baselines;
5. admit a biological chi coordinate only if genuine same-coordinate relaxation and intrinsic-response rates satisfy `docs/CHI_ADMISSION_RULES.md`.
