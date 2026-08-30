# Stage B1 composition/context audit

Date: 2026-08-29

Status: DEVELOPMENT STATIC MAP ONLY

## Execution integrity

The frozen B1 computation completed before the postprocessing crash. Recovery summarized the already-written raw table without recomputation.

- 92 cancer-model tasks: 32 PURITY, 30 LEUKOCYTE, 30 JOINT_INDEPENDENT.
- 100/100 valid deterministic n=30 resamples for every task.
- 50 Hallmark modules per resample.
- 460,000 raw module-resample rows.
- 4,600 module summary rows and 92 cancer summary rows.
- No chi, CV/2, composite stability score, causal claim, transition claim, phase claim, or optimum claim.
- Raw B1 resample SHA-256: `86c7659f47d8f0af52ed6f63b0ef604590b5ed79b77cb2098ffe227b96742042`.

## Primary result

Independent bulk-sample composition explains a real but concentrated part of the Stage A network structure. It does not erase the broader network topology.

The relevant comparison is the context-specific delta: real-context residualization minus the deterministic permuted-context residualization. This subtracts the generic effect of fitting and residualizing an extra covariate.

### Module-rank preservation

Median within-cancer baseline-versus-adjusted module-rank Spearman correlations:

| model | Cin pairwise | Cin PC1 | Cout |
|---|---:|---:|---:|
| PURITY | 0.969 | 0.951 | 0.936 |
| LEUKOCYTE | 0.939 | 0.908 | 0.895 |
| JOINT_INDEPENDENT | 0.931 | 0.896 | 0.890 |

Under the joint independent adjustment, 29/30 cancers retain Cin-pairwise rank rho >=0.8, 25/30 retain PC1 rank rho >=0.8, and 27/30 retain Cout rank rho >=0.8.

### Typical context-specific magnitude

Across all joint cancer-module cells, median context-specific shifts are:

- Cin pairwise: -0.00527 on a baseline median about 0.1982, approximately -2.7% in relative magnitude.
- Cin PC1 variance fraction: -0.00639 on a baseline median about 0.2070, approximately -3.2%.
- Cout: -0.00578 on a baseline median about 0.2700, approximately -2.0%.

These are descriptive effect magnitudes, not promotion p-values and not directional claims of improvement or deterioration.

At the cancer-summary level, the joint median Cin-pairwise context-specific delta is negative in 30/30 cancers. PC1 is negative in 28/30. Cout is negative in 22/30 and positive in 8/30, consistent with Cout being more context-dependent and heterogeneous.

### Topology after adjustment

The inverse relation between internal coherence and external coupling survives composition adjustment.

- Joint-adjusted Cin-pairwise versus Cout is negative in 30/30 cancers; median rho is approximately -0.45.
- Joint-adjusted PC1 versus Cout is negative in 29/30 cancers; UVM is the sole exception and is near zero/slightly positive (rho approximately +0.042), not evidence of a reversed universal relation.
- PURITY-adjusted and LEUKOCYTE-adjusted Cin-pairwise versus Cout are negative in every eligible cancer.

Therefore B1 supports retention of Cin and Cout as separate context-aware static coordinates. It does not support treating either direction as optimal.

## Composition-sensitive sector

The largest and most reproducible reductions are concentrated in immune/inflammatory Hallmarks, which is consistent with bulk cellular composition contributing strongly to their apparent coexpression.

Under JOINT_INDEPENDENT adjustment, median context-specific Cin-pairwise changes across cancers include:

- HALLMARK_ALLOGRAFT_REJECTION: -0.0507; 90% resample interval below zero in 29/30 cancers.
- HALLMARK_INTERFERON_ALPHA_RESPONSE: -0.0434; below zero in 14/30 cancers.
- HALLMARK_INTERFERON_GAMMA_RESPONSE: -0.0428; below zero in 26/30 cancers.
- HALLMARK_IL6_JAK_STAT3_SIGNALING: -0.0396; below zero in 27/30 cancers.
- HALLMARK_INFLAMMATORY_RESPONSE: -0.0382; below zero in 27/30 cancers.
- HALLMARK_TNFA_SIGNALING_VIA_NFKB: -0.0213; below zero in 20/30 cancers.

For PC1 coherence, allograft rejection is reduced beyond the null in 30/30 cancers, inflammatory response in 28/30, and IL6/JAK/STAT3 in 27/30.

This sector must not be interpreted as intrinsic tumor-cell network organization without composition context.

## What B1 closes

B1 rejects two overstatements:

1. `Composition explains the Stage A network map.` The broad module ordering and Cin/Cout topology remain strongly preserved after independent adjustment.
2. `Composition is negligible.` It materially contributes to a concentrated immune/inflammatory portion of the static network geometry.

The retained interpretation is therefore a context-aware static map: Stage A network coordinates are real reproducible observables, but some modules, especially immune/inflammatory modules, contain substantial bulk-composition signal.

## Carry-forward rule

Both unadjusted and context-adjusted information are retained. Composition-sensitive module effects are carried as context/decomposition information rather than being deleted, relabeled as noise, or assigned a better/worse direction.

The next stage is B2 orthogonal genomic/protein/methylation integration using sources reserved before B1 results. B1 outcomes may affect interpretation and covariate handling, but may not be used to cherry-pick favorable B2 assays or features.
