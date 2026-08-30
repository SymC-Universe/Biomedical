# Tool Feasibility F1 — General Kernel Audit

Date: 2026-08-30

## Status

**F1 INITIAL KERNEL REGRESSION PASS — CONTINUE TO F2 SYNTHETIC CHALLENGE**

This is a mathematical/software feasibility checkpoint only. It is not a biological result, not a Stage C1 result, and not evidence that the candidate tool is novel or useful relative to established baselines.

Stage C1 beta-value biology remained sealed throughout this checkpoint.

## Locked context

Canonical program charter:

`docs/GRI_V2_TOOL_DISCOVERY_CHARTER_20260830.md`

Frozen synthetic feasibility plan:

`config/tool_feasibility_plan_v0_1.json`

Frozen Stage C1 v2 preregistration remains unchanged:

`docs/STAGE_C1_ANALYSIS_PREREGISTRATION_20260830.md`

## Implemented general kernel

`src/tool_feasibility_kernel.py`

Implemented capabilities:

- deterministic SHA-256 seed construction;
- column-centered sample-space modal decomposition;
- normalized eigenspectrum, spectral entropy, effective rank, participation ratio, and spectral concentration;
- top-mode feature contribution tracing;
- exact within-feature marginal permutation;
- sample-row permutation;
- linear CKA;
- top-k principal angles;
- measured-covariate residual projection;
- same-module absolute Spearman coupling;
- semantic/module-label permutation effect;
- cross-validated modal predictability candidate;
- predictability permutation calibration;
- a provisional autonomy score derived from predictability excess over a patient-permutation null.

The autonomy quantity is explicitly **candidate mathematics only**. It is not an admitted biomedical coordinate and may be narrowed, replaced, or discarded after F2/F3.

## New synthetic regression tests

`tests/test_tool_feasibility_kernel.py`

The new tests verify, under deterministic synthetic ground truth:

1. seed reproducibility and token-order sensitivity;
2. modal normalization and mode-to-feature contribution closure;
3. exact preservation of feature marginals under the construction null;
4. stronger spectral concentration for coordinated structure than its marginal-permuted null;
5. shared patient geometry above an independent-layer patient-alignment effect;
6. small principal angles for genuinely shared modes versus independent modes;
7. collapse of confounder-only cross-layer alignment after correct covariate projection;
8. separation of same-module semantic coupling from a label-scrambled case while global linear geometry remains unchanged;
9. cross-validated modal predictability separating shared from independent layers;
10. candidate autonomy separating a dominantly substrate-predictable target from a shared-plus-private target;
11. removal of confounder-generated false autonomy loss after correct covariate projection;
12. deterministic Spearman handling including ties.

These are unit/regression challenges, not the complete prespecified F2 scenario battery.

## CI evidence

GitHub Actions workflow: `GRI v2 tests`

- run: `33324684019`
- head commit: `c54458f5f6eec71591476f2afed9377fe2fccaea`
- conclusion: **SUCCESS**
- full repository result: **60 passed, 7 warnings in 1.28 s**

The seven warnings are the existing NumPy invalid-divide warnings from `tests/test_stage_b1_summarize.py`; they are not introduced by F1 and did not fail the suite.

## Interpretation

F1 establishes only that the initial mathematical implementation is internally coherent enough to proceed to the larger ground-truth challenge.

It does **not** yet establish:

- calibrated false-positive/refusal behavior across the complete F2 battery;
- robustness across synthetic parameter ranges;
- superiority or nonredundancy relative to established integration/decomposition methods;
- usefulness on real biomedical data;
- regulatory autonomy as a valid biological quantity;
- substrate capture;
- recoverability;
- biological chi;
- a clinical application.

## Next gate

Proceed to **F2 synthetic ground-truth challenge**, generating the complete frozen scenario family from `tool_feasibility_plan_v0_1.json`, reporting quantitative separation and failure cases rather than only assertion-level unit tests.

After F2, proceed to F3 baseline competition before any GO/NARROW/STOP tool decision or full Stage C1 biological execution.
