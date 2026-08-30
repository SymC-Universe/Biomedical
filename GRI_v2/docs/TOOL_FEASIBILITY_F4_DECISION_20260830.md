# Tool Feasibility F4 decision

**STATUS: CLOSED — NARROW**

Date: 2026-08-30

This is the Gate F4 engineering-investment decision required by `GRI_V2_TOOL_DISCOVERY_CHARTER_20260830.md` and interpreted under `TOOL_PREDICTION_PROSPECTIVE_OBJECTIVE_AMENDMENT_20260830.md`.

It does not modify the frozen Stage C1 v2 scientific contract and does not inspect Stage C1 methylation beta-value biology.

## 1. Decision

**F4 = NARROW.**

Retain a narrowed cross-omic architecture / integration-readiness auditor for prospectively frozen predictive and replication testing, but do not carry every F1/F2 component forward as a named coordinate or candidate contribution.

This is not a tool validation result and not a novelty declaration. It is an engineering decision that the surviving audit/refusal architecture is worth testing prospectively while redundant or failed components are removed or explicitly scoped out.

## 2. Frozen evidence used

### F2 synthetic known-truth challenge

- GitHub Actions run: `33325429587`
- head commit: `2eadfed2b05842e5a0dc5564fe817e7744331930`
- artifact: `GRI_V2_TOOL_FEASIBILITY_F2_20260830`
- artifact ID: `9736091098`
- artifact digest: `sha256:a9a1a9bf762e96454422b26141f056b8efc91f3381c0a170664892ac03dffc1f`
- machine result: `F2_GO_CANDIDATE`
- scored behaviors: `10 / 11` PASS
- mandatory safety: S0, S3, S6, S11 all PASS
- retained failure: S8 nonlinear-only sharing did not satisfy the frozen linear-under-detection/refusal behavior.

The corrected 10-of-11 GO bookkeeping was frozen before F2 output in `TOOL_FEASIBILITY_F2_PRERESULT_BEHAVIOR_COUNT_REPAIR_20260830.md`.

### F3 simple baselines

- GitHub Actions run: `33325711655`
- head commit: `d0d0736c2fd8b46d7a08ef4319897cf3d8ad4788`
- artifact: `GRI_V2_TOOL_FEASIBILITY_F3_SIMPLE_20260830`
- artifact ID: `9736160710`
- artifact digest: `sha256:5463023ac89c560784131f86d649965a46a57d1e7740bb49d577deda23fb8f69`
- status: `F3_SIMPLE_BASELINES_COMPLETE`
- replicates: 24

Frozen contrast results include:

- S1 > S0: all four simple geometry/prediction baselines win 24/24;
- S3 raw > correctly adjusted: all four win 24/24;
- S6 raw > technical-mask representation: all four win 24/24;
- S11 raw > correctly adjusted: all four win 24/24;
- S10 low-autonomy construction > S9 high-autonomy construction: ordinary cross-validated modal predictive R2 wins 24/24 with median margin `0.9174889980372976`;
- naive same-module absolute Spearman distinguishes S5 from S4 in 24/24 with median margin `0.82893225503985`.

### F3 established comparators

- GitHub Actions run: `33340405304`
- head commit: `3301a20ce47fc2ff72cd6440ea5d7b7796fed478`
- Python artifact ID: `9740415552`
- Python artifact digest: `sha256:e863b151d2ef5d3cad4f068c1b43ebe1b7954cd1e17db7e560233468bf52067a`
- DIVAS artifact ID: `9740382168`
- DIVAS artifact digest: `sha256:461352c21689352e0a924d933c1dca9e3d6577a773e7643a81e4e4a8a805ec93`
- frozen-input artifact ID: `9740358278`
- frozen-input digest: `sha256:8c5b4a2c000688e2e90ee227d0154dd652dd34d5fcf7653187ee8d6653007377`

AJIVE + MOFA2 status: `F3_ESTABLISHED_PYTHON_COMPLETE`, 104/104 records, zero failures.

Representative established-method behavior:

- AJIVE: S0 median joint rank 0; S1 median joint rank 1; S3 adjusted median joint rank 0; S6 masked median joint rank 0; S11 adjusted median joint rank 0.
- AJIVE does not supply semantic-label specificity: S4 remains strongly joint (median joint rank 3; source/target joint-energy fractions approximately 0.957/0.958).
- AJIVE already expresses shared/private structure in S9 versus S10, so shared/private decomposition is not a new coordinate by itself.
- MOFA2 similarly separates near-zero shared mass in S0 and adjusted/masked null representations from large shared mass in S1, S3 raw, S4, S6 raw, and S10.

DIVAS status: `F3_DIVAS_NOT_EVALUABLE_PUBLISHED_IMPLEMENTATION`, 104/104 records classified under exact documented published-implementation failures, zero unexpected failure signatures. Under the frozen F3 rule this is `NOT_EVALUABLE`; it does not authorize substitution of a weaker baseline or a novelty claim about shared/private modes.

## 3. Component decisions

### Global cross-layer geometry

**Classification: ESTABLISHED PRIMITIVE — RETAIN, NO NOVELTY CLAIM.**

CKA, principal angles, CCA-like association, AJIVE, and MOFA2 already recover much of the global shared-versus-independent and raw-versus-adjusted/masked behavior. The tool may use these objects as established ingredients, but global alignment is not itself the justification for a standalone new method.

### Measured-confounder and technical attack tracks

**Classification: COMPLEMENTARY GUARDRAILS — RETAIN.**

F2 mandatory safety scenarios S3, S6, and S11 pass. Simple and established baselines can also respond to the correct adjusted/masked representations, so the mathematical act of adjustment or masking is not novel. Their retained value is as prospectively fixed attacks in an integrated decision/refusal workflow.

### Semantic / conglomeration specificity

**Classification: COMPLEMENTARY — RETAIN FOR PROSPECTIVE ABLATION.**

Geometry-only methods treat S4 as genuinely shared because its sample geometry is intentionally shared. A semantic layer is therefore necessary to distinguish `GLOBAL_SHARED_ONLY` from biologically corresponding module-level sharing. The naive same-module Spearman baseline also separates S5 from S4, so the raw same-module statistic is not independently distinctive. The calibrated label-null and its contribution to refusal/decision quality must justify themselves prospectively.

### Regulatory autonomy scalar

**Classification: `AUTONOMY_REDUNDANT_NARROW`.**

The frozen candidate autonomy is a deterministic transform of permutation-calibrated cross-validated modal predictability. F3 B2 shows ordinary cross-validated prediction already supplies the decisive S9/S10 ordering with a 24/24 win rate and median margin `0.9174889980372976`. AJIVE and MOFA2 additionally expose shared/private structure directly.

Therefore do not carry "regulatory autonomy" forward as a named independent coordinate or novelty candidate in v0.1. Retain transparent predictive dependence, residual/private structure, permutation calibration, and refusal logic only where they add prospective utility.

### Modal shared/private decomposition

**Classification: ESTABLISHED / COMPLEMENTARY — RETAIN FOR TRACEABILITY, NO NOVELTY CLAIM.**

AJIVE and MOFA2 already provide relevant decomposition information. DIVAS could not be evaluated under the pinned published implementation, so no claim that the proposed shared/private representation improves on DIVAS is licensed.

### Nonlinear-only scope

**Classification: FAILED CAPABILITY — EXCLUDE FROM v0.1 CLAIMS.**

S8 remains a genuine F2 failure. The initial linear auditor is not licensed to claim calibrated refusal for nonlinear-only dependence. A nonlinear extension, if pursued, must be a separately frozen future version and cannot retroactively convert S8 into a pass.

### Integrated decision/refusal architecture

**Classification: SURVIVING F4 CANDIDATE.**

The synthetic evidence supports carrying forward the integration-readiness workflow that combines patient-alignment evidence, semantic specificity, measured-confounder attacks, technical tracks, modal traceability, uncertainty/calibration, and explicit refusal states. F3 does not validate this integrated system. Its retained justification is that no single tested baseline supplies the complete multi-attack decision state, and the program objective requires this combined behavior to prove its value prospectively.

## 4. F4 outcome

`NARROW` means:

1. continue development only of the reduced audit/refusal architecture;
2. drop autonomy as a named independent scalar coordinate for v0.1;
3. treat global geometry and modal decomposition as established ingredients;
4. retain semantic/confounder/technical/refusal layers only subject to prospective component ablation;
5. explicitly exclude nonlinear-only dependence from the v0.1 supported scope;
6. make no shared/private novelty claim against DIVAS while its frozen comparator is `NOT_EVALUABLE`;
7. move next to prospectively frozen predictive, replication, and selective-prediction testing before opening data used for those targets.

## 5. Next gate

The next authorized scientific-design action is to freeze the prediction/holdout protocol required by `TOOL_PREDICTION_PROSPECTIVE_OBJECTIVE_AMENDMENT_20260830.md` before any biological values used as predictive targets are inspected.

The frozen Stage C1 v2 preregistration remains unchanged. F4 does not itself authorize changing C1 endpoints, thresholds, nulls, resample design, or interpretation.

## 6. Claim ceiling

F4 NARROW establishes only an engineering decision to continue a reduced architecture into prospective testing. It does not establish biomedical relevance, generalization, clinical utility, causal biology, treatment response, substrate inheritance, recoverability, biological chi, or methodological novelty.
