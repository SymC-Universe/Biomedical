# GRI post-C1 v2.2 foundational robustness audit

**Date:** 2026-09-13  
**Protocol:** Final v0.7.5 Section 11.3  
**Timing status:** `POST_RESULT_ROBUSTNESS_AUDIT`  
**Original evidence class:** P0-Q qualification  
**Original historical promotion:** unchanged  
**Biological Chi:** `NOT_ADMITTED`

## Minimum dependency record

`FOUNDATION_ID | FOUNDATION_STATUS | DEPENDENT_CLAIMS_OR_STAGES | CHALLENGE_TRIGGER | CHALLENGE_SPEC | TIMING_STATUS | FREEZE_ID | STOP_RULE | OUTCOME | DEPENDENCY_EFFECT`

- **FOUNDATION_ID:** `GRI_POST_C1_SENSITIVITY_V2_2_RESULT_20260912`
- **FOUNDATION_STATUS:** completed P0-Q post-C1 adversarial-sensitivity result; final archive SHA-256 `85955af9e0d2333c651e445d75392b60ca9d25942a364fa29dc5c67b55bb3dd1`
- **DEPENDENT_CLAIMS_OR_STAGES:** read-only Chi_bio dependency/identifiability export; future internal mapping that cites completed C1/post-C1 evidence
- **CHALLENGE_TRIGGER:** substantial downstream architecture will inherit the result, while historical resume checkpoints are weaker provenance objects than the final result archive
- **CHALLENGE_SPEC:** reconcile final archive integrity, manifest hashes, canonical S0 reconstruction, scientific-worker lineage, corrected S2 eligibility semantics, and checkpoint/result identity separation
- **TIMING_STATUS:** `POST_RESULT_ROBUSTNESS_AUDIT`
- **FREEZE_ID:** `GRI_V075_POST_C1_FOUNDATION_AUDIT_20260913_V0_1`
- **STOP_RULE:** close after all listed final-result checks are reconciled and downstream provenance explicitly forbids recovery-checkpoint substitution; no rerun or harder internal attack is implied
- **OUTCOME:** `ROBUSTNESS_SUPPORTED`
- **DEPENDENCY_EFFECT:** final result remains usable at P0-Q only; recovery checkpoints are provenance/restart artifacts only; no promotion or Chi_bio admission

## 1. Final archive identity and integrity

The audited returned archive is `POST_C~1.ZIP` with SHA-256:

`85955af9e0d2333c651e445d75392b60ca9d25942a364fa29dc5c67b55bb3dd1`

The existing result audit records:

- ZIP structural integrity: PASS;
- 15 archive members;
- 14 member hashes in `SHA256SUMS.json`, all verified exactly;
- `RUN_SUMMARY.json` status `POST_C1_SENSITIVITY_V2_2_COMPLETE`;
- frozen C1 contract SHA-1 `a39414c5990c234dc513569bd405b0237117d434`;
- C1 implementation `stage-c1-frozen-v2-exec-20260906.3`;
- 32 cancers, 100 resamples per cancer, B=199 repeated patient-permutation nulls.

This final archive, not a resume checkpoint, is the evidentiary post-C1 source.

## 2. Canonical reconstruction challenge

S0 reconstructed canonical C1 before interpreting sensitivity output:

- 32/32 cancers passed;
- 6,400 canonical keys checked;
- maximum absolute reconstruction error `9.71445146547012e-17`;
- frozen tolerance `1e-10`.

The final post-C1 result therefore reconciles to frozen C1 far inside the frozen tolerance.

## 3. Launcher/scientific-worker lineage

The v2.2 to v2.2A repair changed packaging/launch behavior but not the scientific worker. The SHA-256 of `run_post_c1_sensitivities_v2.py` is identical across v2.2 and v2.2A (`e6f3cc65...`).

The launcher repair is therefore not evidence of a silent scientific-worker substitution.

## 4. S2 semantic correction

The original descriptive S2 sign-count summary counted all 32 cancer medians although only five cancers had interpretable S2 draws. The underlying resample calculations retained interpretability counts, and the result audit preserved a separate interpretable-only correction.

Correct primary-publication S2 evidentiary summary:

- eligible cancers: 5;
- positive: 5;
- negative: 0;
- median interpretable-only delta: approximately `0.247768`.

The erroneous descriptive denominator must not be inherited by downstream exports. The original archive remains unchanged and the correction remains explicit.

## 5. Checkpoint vulnerability and bounded disposition

Historical inspection of the post-C1 worker shows that per-cancer resume checkpoints are plain serialized recovery payloads and are not adequate as standalone final-result identities. Allowing such a checkpoint to substitute for the final result would create an avoidable provenance ambiguity.

The bounded response is **not** to rerun completed C1/post-C1 science. Instead:

1. downstream evidentiary inheritance is bound to the final hashed result archive;
2. `WORKING_STATE` is tagged recovery/provenance-only;
3. downstream export schemas must refuse checkpoint/result interchangeability;
4. future long runs should bind checkpoint configuration/input/version identities prospectively.

This removes the identified dependency vulnerability from downstream inheritance without pretending that the historical checkpoint format was stronger than it was.

## 6. Outcome

**OUTCOME: `ROBUSTNESS_SUPPORTED`.**

Meaning:

- the final hashed post-C1 result remains internally reconciled and suitable as a P0-Q upstream dependency;
- the outcome does not upgrade the evidence class;
- the outcome does not create untouched confirmation;
- the outcome does not admit a biological Chi;
- the outcome does not authorize a cancer Chi map or a biological unity boundary;
- no additional C1/post-C1 computation is required by this challenge.

The robustness stopping condition is satisfied once the v0.2 downstream export schema enforcing final-result identity is in place. Any further escalation requires a new scientific reason.
