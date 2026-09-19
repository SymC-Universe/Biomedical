# GRI Chi-bio conglomerate v0.1 source-binding map

**Date:** 2026-09-18  
**Status:** CURRENT DEVELOPMENT BINDING MAP  
**Branch:** `gri-chi-bio-conglomerate-v01-20260918`

This map answers a narrow question: what already-frozen evidence can populate each capital-Chi biological block, and what still has to be materialized before a real patient/system-level conglomerate run is legitimate?

| Block | Existing evidence/source | Present status | Immediate need |
|---|---|---|---|
| R RNA/regulatory | Stage A1.1 fixed-n RNA architecture; post-C1 cross-assay geometry | source identities and compact summaries available | recover/recompute patient-level frozen RNA feature table |
| S methylation/substrate | C0/C0.1 source/identity, C1A exact annotation, completed C1/post-C1 evidence | biological architecture completed historically; compact source/result audits available | recover/recompute patient-level frozen methylation feature table |
| E embedding/context | B1 purity/leukocyte composition-adjusted architecture | source hashes and completed summary available | materialize patient-level covariates under frozen identities |
| G genomic | B2 genomic burden coordinates | completed 306-task static branch | materialize matched patient-level genomic coordinates |
| P protein/phosphoprotein | B2 RPPA | completed 60-task orthogonal branch, 6,887 matched Stage-A samples | materialize matched patient-level RPPA representation where available |
| M modal/vector | Stage A1.1 + C1/post-C1 top-mode/residual geometry | modal behavior is supported and top-mode ablation characterized | bind exact patient-level modal carrier; do not scalarize |
| T temporal/operator | short-term and chronic SCC25 G2; R0 embedding preflight | genuine ordered evidence exists but is system-specific | keep as a separate system/temporal block; do not paste SCC25 values onto TCGA patients |
| Q quality/confidence | P0 predictive final summary + P3-v2 continuous geometry confidence | internal predictive confidence supported; categorical selector failed | carry continuous confidence + technical/composition/identifiability metadata |

## Verified predictive spine

The current internally supported predictive spine is not speculative:

- D4 REPLICATION: ALL_METHYLATION_RIDGE beat COVARIATE_ONLY in 18/19 cancers.
- FINAL_HOLDOUT: ALL_METHYLATION_RIDGE beat COVARIATE_ONLY in 17/18 primary cancers.
- FINAL_HOLDOUT median nMSE: 0.4440 versus 0.7018 for COVARIATE_ONLY.
- FINAL_HOLDOUT median held-out R2: 0.5074 versus 0.1878.
- continuous GLOBAL_GEOMETRY_CONFIDENCE prospectively ranked final prediction risk: rho = -0.56037, one-sided permutation p = 0.00795.
- categorical ACCEPT/CAUTION/REFUSE is not retained as a validated predictive selector.

These are internal TCGA results and remain below external/clinical promotion.

## R0 reconciliation

The earlier provenance map had not yet recorded the completed R0 run. Live GitHub verification on 2026-09-18 confirms:

```text
workflow_run = 34844761409
workflow = GRI Chi_bio G1 restoration R0 embedding preflight
head_sha = 375be1ffc39376e70120d71f435d8e94f50de08f
conclusion = success
artifact_id = 10347102753
artifact_name = gri-chi-bio-g1-restoration-r0-embedding-preflight-v1
artifact_digest = sha256:aa9b27063a2b476740f76061390659dbb1e3c55fe57056534daf09eeee6b4220
```

R0 remains a representation-specific identifiability/embedding result. It is not a required gate for capital Chi-bio and does not populate a scalar.

## Computational consequence

The synthetic carrier gate can run entirely in GitHub. The first real-data bottleneck is **not mathematics**. It is materializing the already-frozen patient-level block tables under exact source identities without using clinical outcomes to choose features.

TCGA FINAL_HOLDOUT has already been opened for the older P0 architecture. It may be used for development/ablation of the new conglomerate version, but it cannot be called untouched confirmation of that new version.

The next confirmatory diagnostic/predictive result must therefore come from an independently frozen external dataset/task.

## Remote-compute note

The materialization preflight is delegated to GitHub Actions. Large R/S biological matrices remain unmaterialized until exact remote acquisition and resource-safe streaming rules are bound; no local user computation is required for this preflight.
