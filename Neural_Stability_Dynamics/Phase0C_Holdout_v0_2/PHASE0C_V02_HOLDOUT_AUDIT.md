# Phase 0C v0.2 Three-Layer Holdout Audit

Date: 2026-09-08

Status: **OFFICIAL PROSPECTIVE RESULT = FAIL / FAIL / FAIL. PRESERVE. DO NOT RETUNE ON THIS HOLDOUT.**

This audit interprets the completed frozen Phase 0C v0.2 run. It does not change the preregistered thresholds, decisions, or claim ceiling.

## Provenance

- Config SHA-256: `31db0aa636e884f9a811545a286e3d97a93be35d419b7195213a81d1925163b4`
- Rules SHA-256: `d81e947bfb2050a62a0b43534a7445fe7411f318f6f07db03eddad79472ecab1`
- Mechanical fits failed: 0
- Stationary trials: 216
- Official layer status: scalar FAIL; modal FAIL; system FAIL.

The completed result bundle is preserved independently from this audit. No result below promotes Phase 0C v0.2 to PASS.

## What worked prospectively

The stationary linear regime was strong:

- stationary scalar admission = 1.0000
- stationary modal admission = 1.0000
- strong complex scalar coverage = 0.964912
- spurious admitted complex-mode rate = 0.0000
- admitted complex normalized pole-error p90 = 0.004094
- admitted complex frequency-error p90 = 0.031052 Hz
- admitted complex relative-decay-error p90 = 0.190033
- individual truth MAC p10 = 0.999808
- crowded truth-subspace similarity p10 = 0.999987
- system truth-subspace similarity p10 = 0.999958
- system truth channel-participation TV p90 = 0.002315
- system truth relational-geometry error p90 = 0.032436
- 1/f null refusal = 1.0000 in all three layers.

Therefore the holdout does **not** show general SSI-COV collapse. The failures are localized to order handling and system-geometry identifiability.

## Failure mechanism 1: full-record order inflation contaminated split comparisons

The frozen selector chose one observable order from the **full record** and then evaluated the first and second halves at that same order. In the three switch challenges, the full record is a mixture of two regimes. The mixture requires a larger stochastic realization than either local regime.

Post-hoc mechanism audit using the frozen generator, frozen seed, frozen noise realizations, and unchanged order-selection rule gave:

| challenge | full-record q | first-half q | second-half q |
|---|---:|---:|---:|
| global timescale switch | 8 in 9/9 | 4 in 9/9 | 4 in 9/9 |
| observation-map switch | 8 in 9/9 | 4 in 9/9 | 4 in 9/9 |
| structural switch | 6 in 9/9 | 4 in 9/9 | 4 in 9/9 |

Thus the frozen Phase 0C evaluator compared q=8 or q=6 fits inside halves whose local observable order was q=4. The extra half-record modes were overfit mixture structure, which contaminated scalar matching, modal MAC/subspace, and whole-system metrics.

This is an estimator-selection architecture error, not a reason to reverse the official FAIL.

### Diagnostic only: local-order separation

Using the same frozen data after the holdout, but evaluating each half at its own automatically selected q=4, the intended dissociations became clean without changing any scientific thresholds:

**Global timescale switch**
- split scalar pole distance approximately 0.198 to 0.200, above the frozen 0.03 stationarity limit
- median optimal carrier MAC >= 0.99994
- whole observable-subspace similarity >= 0.99994
- channel-participation TV <= 0.00311
- normalized relational-geometry distance <= 0.00437

This is the expected scalar REFUSE / modal PRESERVE / system PRESERVE pattern.

**Observation-map switch**
- split scalar pole distance <= 0.00180, below 0.03
- median optimal carrier MAC approximately 0.116 to 0.362
- whole observable-subspace similarity approximately 0.156 to 0.415

This is the expected scalar PRESERVE / modal REFUSE / system REFUSE pattern.

**Structural switch**
- split scalar pole distance approximately 0.0789 to 0.0819, above 0.03
- median optimal carrier MAC >= 0.99990
- whole observable-subspace similarity >= 0.99994
- normalized relational-geometry distance approximately 0.210 to 0.222, above 0.05

This is the expected scalar REFUSE / modal PRESERVE / system REFUSE pattern.

These are post-hoc diagnostics only. They justify a new estimator version and new untouched holdout; they do not rescue Phase 0C v0.2.

## Failure mechanism 2: system relational geometry ignored the crowding firewall

The near-degenerate stationary family had nearly perfect carrier/subspace recovery but poor raw relational-pole-geometry stability:

- split whole-subspace similarity minimum > 0.99991
- split channel-participation TV maximum < 0.00455
- split relational-geometry distance exceeded 0.05 in 18/27 trials
- system admission was only 6/27.

The modal layer already treats sufficiently crowded modes as an invariant subspace because individual decomposition is not identifiable. The system layer nevertheless demanded stable pairwise pole geometry **inside the same crowded cluster**. That is internally inconsistent.

For a nearly degenerate pair, the denominator of the normalized pairwise-geometry comparison becomes small, so tiny admissible pole errors produce a large relative geometry error. The next estimator must collapse crowded modes to an identifiable cluster/subspace before system-level relational geometry is scored. If fewer than two resolved clusters remain, relational geometry should be explicitly `UNRESOLVED`, not converted into a false system failure.

## Failure mechanism 3: exact effective-order truth was too rigid

The frozen target effective order was based on strong observable mode-shape amplitude. Two realizations showed deterministic lower selected order across all durations and noise profiles:

- `v02_moderate_third`, replicate 0: selected q=4 in all 9 conditions although target q=6.
- `v02_nonnormal_cond70`, replicate 2: selected q=2 in all 9 conditions although target q=4.

Because these outcomes persisted across noise profile and duration, they are properties of the realization/conditioning, not random noise failures. Meanwhile strong-complex recovery remained 0.964912 and spurious admitted complex modes remained 0.

For real data, effective observable rank is an identifiability statement, not simply latent state count. The next holdout should score strong-mode recall, false/spurious mode rate, uncertainty, and explicit partial observability rather than require exact equality to a synthetic state-count target in every realization.

## Phase 0D design consequence

Phase 0D must be developed separately from this holdout and then frozen before a new independent holdout is executed.

Required architecture:

1. **Segment-local order selection.** Estimate `q_full`, `q_first`, and `q_second` independently. Full-record order inflation is a diagnostic of mixture complexity and must not be imposed on local segments.
2. **Layer-A scalar spectrum.** Compare locally selected segment poles; keep cross-order stability checks local to each segment.
3. **Layer-B carrier structure independent of scalar matching.** Align individual carriers by MAC and crowded carriers by invariant-subspace similarity rather than using eigenvalue proximity as the primary carrier matcher.
4. **Layer-C crowding-aware organization.** Preserve projector/subspace and channel-participation structure; compute relational spectral geometry only between resolved modal clusters. Mark unidentifiable intra-cluster geometry `UNRESOLVED`.
5. **Partial observability is explicit.** Score strong-mode recall and spurious-mode precision. Do not force an unobservable mode into the result to satisfy latent-order truth.
6. **New independent holdout.** Development may use Phase 0C only as calibration/postmortem evidence. Final Phase 0D admission must use a new seed and withheld systems/perturbations.
7. **No EEG gate yet.** Label-blind TDBRAIN adequacy begins only for prospectively passing Phase 0D layers.

## Scientific interpretation

The strongest conclusion from Phase 0C v0.2 is not that the three-layer concept failed. The prospective implementation failed because the layer evaluator allowed full-record mixture order to leak into local comparisons and because the system layer demanded a pole-geometry quantity precisely where the modal layer had already declared individual modes non-identifiable.

The three-layer separation remains a live hypothesis because the frozen synthetic generator exhibits the intended dissociations when the local observable order is respected. That statement is **post-hoc development evidence only** until reproduced prospectively on the next untouched holdout.
