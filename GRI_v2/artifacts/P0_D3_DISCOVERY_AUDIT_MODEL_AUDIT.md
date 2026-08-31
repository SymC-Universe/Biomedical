# P0 D3 DISCOVERY audit-state and P1 model audit

Status: CLOSED PASS AS A DISCOVERY-ONLY GATE

## Provenance

D3 was frozen after D2 PASS and before any D3 real cross-layer discovery statistic was computed. The initial D3 freeze was followed, before execution, by the explicit pre-compute seed-lineage correction that restored the existing F2 `stable_seed` algorithm rather than introducing a new seed conversion.

The exact frozen B1 covariate sources were recovered from successful Stage B0 workflow run `33279981442`, artifact `gri-v2-stage-b0-source-inventory` (`9722689564`). Their SHA-256 values exactly match the P0/B1 frozen identities:

- ABSOLUTE purity: `f430a975433d82e0098d7405619d4f12a0c765fcd97e7d63cc9b1de7f2d763cd`
- methylation-derived leukocyte fraction: `5a8268caedbf8dc98a75be0528d583238d7355761d9fc746e42002f223a982d9`

Final D3 result ZIP SHA-256: `770c88f44813e99f9c02ad04fd5a7571426d06f6ea9fb545618b271cc3c43ae6`.

Final `RUN_SUMMARY.json` SHA-256: `60a9d3ad37e8617e5b80c664bd5fd905002d17710dad15f35b6ec79df170fee0`.

All files listed in the returned result `SHA256SUMS.txt` independently match their recorded hashes.

## Projection-parameter closure

The first completed D3 execution exposed a mechanical reproducibility-output gap: the scientific audit/model calculations completed, but the frozen D3 output contract also requires the discovery-fitted composition residualization parameters and explicit discovery target reference mean/variance needed for later untouched projection.

Before any REPLICATION value was opened, the runner was extended to emit:

- `Composition_Parameters.csv.gz`
- `Target_Reference.csv`

and one synthetic regression test was added proving that persisted residualization parameters exactly reproduce the fitted residuals.

The D3 gate was rerun with no changes to participants, features, nulls, thresholds, endpoints, state logic, model architecture, alpha grid, CV folds, or interpretation. Core deterministic CSV outputs (`Discovery_Audit.csv`, `Discovery_Audit_Metrics.csv`, `Within_Layer_Audit.csv`, `Modal_Trace.csv`, `Discovery_Covariates.csv`, and `Model_Summary.csv`) retained their exact hashes. The added parameter tables independently reconstruct the adjusted CKA values and discovery target references with zero mismatches. This was an execution/projection closure, not scientific retuning.

## Independent mechanical audit

Final row counts:

- `Discovery_Audit.csv`: 19
- `Discovery_Audit_Metrics.csv`: 76 = 19 cancers x 2 scopes x 2 technical tracks
- `Within_Layer_Audit.csv`: 38 = 19 cancers x 2 layers
- `Audit_Nulls.csv.gz`: 10,374
- `Discovery_Covariates.csv`: 4,863
- `Composition_Parameters.csv.gz`: 2,660
- `Target_Reference.csv`: 950 = 19 cancers x 50 RNA targets
- `Model_Summary.csv`: 1,007
- `Model_CV.csv.gz`: 7,144
- `Model_Parameters.csv.gz`: 52,820

Audit checks:

- zero manifest/hash mismatches;
- zero metric/null reconstruction mismatches;
- zero discovery-state reconstruction mismatches;
- zero direct raw-CKA reconstruction mismatches from the frozen D1/D2 score matrices;
- zero adjusted-CKA reconstruction mismatches from the persisted composition parameters;
- zero target-reference mean/variance reconstruction mismatches;
- zero selected-alpha versus CV-argmin mismatches;
- zero non-finite model coefficients;
- all selected alphas belong to the frozen grid;
- all 19 cancers support all required P1 DISCOVERY models;
- no covariate imputation was performed.

Composition-complete P1 sample sizes range from 81 to 593 and all exceed the frozen minimum of 30. Across the 4,863 D3 discovery participants, all 4,863 have the frozen methylation-derived leukocyte fraction and 4,451 have both composition covariates; 412 are missing an eligible ABSOLUTE-purity attachment and are excluded only from composition-adjusted/P1 model fitting as prospectively specified.

## Frozen discovery audit result

All 19 cancers satisfy the frozen global cross-layer geometry gate on PRIMARY_PUBLICATION, and all 19 also satisfy it on MASKED_TECHNICAL. The result survives the composition attack as a global-geometry result in all 19 cancers on both technical tracks.

For PRIMARY_PUBLICATION raw geometry:

- observed linear CKA range: approximately `0.1381` to `0.5499`;
- median observed CKA: approximately `0.3137`;
- minimum `Delta_CKA`: approximately `0.1256`, above the frozen `0.05` effect floor;
- all empirical global p-values are `0.025`, the minimum attainable with 39 null permutations.

For PRIMARY_PUBLICATION composition-adjusted geometry:

- observed CKA range: approximately `0.0710` to `0.4266`;
- median observed CKA: approximately `0.1841`;
- minimum `Delta_CKA`: approximately `0.0591`, still above the frozen `0.05` effect floor;
- all 19 global gates pass.

Patient alignment is also detected for the same-Hallmark semantic statistic in all 19 cancers, raw and adjusted, but the independent Hallmark-label specificity gate fails everywhere. Across all 76 raw/adjusted x technical-track screens, **zero** satisfy the frozen label-specific semantic rule. In PRIMARY_PUBLICATION raw data, the largest observed `Delta_A_label` is approximately `0.0816`, below the prospectively frozen `0.10` floor. No threshold is relaxed.

Therefore all 19 cancers receive the frozen discovery state:

`GLOBAL_SHARED_ONLY`

and decision class:

`CAUTION`.

No cancer receives `SEMANTIC_SHARED_ROBUST` / ACCEPT in D3.

Both individual layers separately show construction-aware within-layer spectral organization in all 19 cancers. These within-layer results do not rescue semantic label specificity and do not alter the D3 state because global cross-layer sharing already passes.

## P1 DISCOVERY fitting diagnostic

All 19 `ALL_METHYLATION_RIDGE` models and all 19 `COVARIATE_ONLY` models fit under the frozen deterministic 5-fold discovery CV and alpha grid. The SAME_HALLMARK baseline fits exactly 45 targets per cancer; the five source-mapping-ineligible targets remain `NOT_EVALUABLE_SOURCE_MAPPING`, yielding 855 fitted and 95 refused cancer-target baseline tasks.

As a DISCOVERY-only model-selection diagnostic, the selected `ALL_METHYLATION_RIDGE` CV normalized MSE is lower than the independently selected `COVARIATE_ONLY` CV normalized MSE in 19/19 cancers. The median paired difference (`ALL_METHYLATION_RIDGE - COVARIATE_ONLY`) is approximately `-0.21685`. Selected all-methylation discovery CV normalized MSE ranges approximately `0.4031` to `0.6656`.

This is **not** a held-out prediction result and does not promote predictive utility. It only establishes that the frozen methylation feature set contains substantial discovery-fold information beyond the two composition covariates under the frozen fitting procedure. Whether that information generalizes is the purpose of the untouched REPLICATION gate.

## Claim boundary

D3 establishes a strong, recurrent, composition- and technical-robust **global patient-aligned cross-layer geometry** in DISCOVERY and a favorable discovery-CV modeling diagnostic. It simultaneously rejects promotion to Hallmark-label-specific semantic sharing under the frozen semantic effect floor.

D3 does not establish a biological mechanism, causal substrate inheritance, clinical utility, temporal dynamics, biological damping, exceptional points, biological chi, or held-out predictive performance. The 24-cancer pan-cancer promotion floor remains unreachable with 19 P0-evaluable cancers, so any pan-cancer P0 summary remains descriptive.

## Decision

D3 is CLOSED PASS as an execution/audit/model-fitting gate with discovery state `GLOBAL_SHARED_ONLY` / `CAUTION` in all 19 cancers.

Next: freeze and regression-test untouched REPLICATION projection/evaluation while FINAL_HOLDOUT remains sealed. The D3 architecture, thresholds, nulls, transforms, model parameters, and state rules are not modified in response to the replication result.
