# Tool Feasibility F3 baseline-competition freeze

**STATUS: FROZEN BEFORE THE REPLICATED F2 RESULT IS INSPECTED**

Date: 2026-08-30

This baseline plan is fixed while the replicated F2 sweep is still running. It prevents selection of conveniently weak comparators after synthetic outcomes are known. It does not modify Stage C1 v2 and does not inspect C1 beta-value biology.

## 1. F3 question

The proposed cross-omic architecture auditor is not required to beat every integration method at factor recovery, clustering, or prediction. It must instead demonstrate a scientifically useful **audit / decomposition / refusal decision** that is not already supplied adequately by simpler or established methods.

The key contrasts are:

- true sharing versus independence;
- true sharing versus measured-confounder-only sharing;
- global sample sharing versus matched biological-module specificity;
- robust sharing versus sharing manufactured by a known technical subset;
- strong cross-layer coupling with retained target-private structure versus dominant target predictability from the other layer.

## 2. Immediate executable baselines

### B0 — CKA-only

Use the same linear CKA statistic and patient permutation, without semantic, confounder, technical-track, or autonomy logic.

Purpose: establish exactly what the multi-stage auditor adds beyond its own global alignment primitive.

### B1 — principal-angle / shared-subspace only

Use top-k sample subspace principal angles without the auditor's semantic, confounder, or technical decision layers.

Purpose: test whether the multi-stage decision is reducible to ordinary sample-subspace overlap.

### B2 — ordinary PCA/ridge cross-validated predictability

Use source PCA scores to predict target PCA scores under the same cross-validation scheme but without the autonomy interpretation, permutation calibration, or explicit refusal state.

Purpose: test whether the autonomy candidate is merely a relabeled predictive R2.

### B3 — CCA / PLS-style linear multiview association

Use a standard linear cross-view latent association method under fixed, prospectively specified component counts and cross-validation.

Purpose: test whether apparent cross-layer dependence is already captured adequately by standard latent association.

### B4 — AJIVE

Use the open-source Python AJIVE implementation (`jive`) to decompose paired blocks into joint and individual variation under fixed initial-rank settings appropriate to the synthetic rank family.

Purpose: AJIVE directly tests the closest established concept to "shared structure plus retained autonomy". If the proposed autonomy statistic is effectively monotone-equivalent to AJIVE individual/joint decomposition without adding calibration or decision value, the autonomy branch should be narrowed or dropped.

Reference implementation: `idc9/py_jive`, package install `pip install jive`.

### B5 — MOFA2

Use the Python `mofapy2` implementation of Multi-Omics Factor Analysis with fixed factor count for the synthetic benchmark and no outcome supervision.

Purpose: compare against an established probabilistic shared-factor integration framework. The auditor does not have to recover factors better than MOFA2; it must show added value in refusal, confounder/semantic/technical diagnosis, or traceable state distinction.

Reference implementation: `bioFAM/mofapy2`, stable install `pip install mofapy2`.

## 3. Publication-level required comparator

### B6 — DIVAS

Before any methodological novelty claim about regulatory autonomy, shared/private modes, or integration readiness, benchmark against the current open-source DIVAS implementation.

DIVAS explicitly decomposes multi-block data into jointly shared, partially shared, and individual subspaces and includes inference using angular subspace methods. Its open-source R package was published in Bioinformatics in August 2026.

This comparator is mandatory because it overlaps directly with the proposed modal shared/private structure question.

If immediate CI installation of the R implementation becomes a mechanical blocker, F3 may proceed provisionally with AJIVE/MOFA2/simple baselines, but **no autonomy novelty claim may be promoted until DIVAS is tested**.

## 4. Semantic baseline

### B7 — naive same-module correlation

Use median absolute same-module Spearman correlation without a Hallmark/module-label permutation null.

Purpose: quantify how much the semantic-label null protects against generic module correlation and mislabeled correspondence.

## 5. Baseline parameter policy

- no parameter is tuned separately to make the proposed auditor look favorable;
- component counts are fixed from the known synthetic rank family, not from auditor outcomes;
- where a method requires rank initialization, use the same fixed rank budget across paired scenarios;
- cross-validation splits are deterministic and shared where comparable;
- no outcome labels are introduced;
- if a third-party method cannot run on a scenario for a documented mathematical/software reason, record `NOT_EVALUABLE` rather than substituting a weaker baseline.

## 6. Contrast-based evaluation

The principal F3 output is a decision matrix, not a single leaderboard score.

For each baseline and the proposed auditor, record whether it distinguishes the following prospectively defined pairs:

1. S0 independent versus S1 shared;
2. S1 genuine shared versus S3 confounder-only before/after covariate control;
3. S1/S2 shared geometry versus S4 global-shared-but-semantically-scrambled;
4. S1 genuine shared versus S6 technical false concordance before/after mask;
5. S5 module-specific weak-global sharing versus S0 independent;
6. S9 high-coupling/high-autonomy versus S10 high-coupling/low-autonomy;
7. S11 raw confounded predictability versus S11 after true covariate projection.

## 7. Autonomy redundancy test

Regulatory autonomy remains a candidate only.

Compare the candidate autonomy score against:

- ordinary cross-validated predictive R2;
- AJIVE joint/individual variance decomposition;
- MOFA2 view-specific versus shared factor structure where extractable;
- DIVAS individual/shared subspace structure before any novelty claim.

### `AUTONOMY_NONREDUNDANT_CANDIDATE`

Requires that the candidate provides at least one stable, calibrated decision that the simpler predictive score and joint/individual decomposition do not provide equivalently, especially under confounding or patient permutation.

### `AUTONOMY_REDUNDANT_NARROW`

If the autonomy score is effectively a monotone restatement of existing joint/individual or predictive quantities and adds no calibration/refusal advantage, remove it as a named new coordinate. The underlying shared/private decomposition may remain useful.

No correlation cutoff will be invented after results as proof of redundancy. Evidence will include direct scenario decisions, ordering, calibration, and the mathematical relationship among quantities.

## 8. F3 progression rule

- If F2 returns `F2_STOP_SIGNAL`, do not spend substantial compute on full third-party baseline fitting. Record F3 as unnecessary for a stopped standalone architecture.
- If F2 returns `F2_NARROW_CANDIDATE`, compare only the surviving components against their direct baselines.
- If F2 returns `F2_GO_CANDIDATE`, execute B0-B5 and B7 immediately, then add DIVAS B6 before any methodological novelty claim.

## 9. Claim ceiling

F3 can establish only relative methodological feasibility on synthetic known-truth systems. It cannot establish biomedical relevance, clinical utility, cancer mechanism, treatment response, biological chi, substrate inheritance, or C1 biological validity.
