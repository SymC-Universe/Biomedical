# NSD P0-D6 Subspace-DMD Real-Pole Replay Result

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Status: **P0-D RETROSPECTIVE / NON-INDEPENDENT FORENSIC EVIDENCE. HISTORICAL P0Q1 RESULT UNCHANGED. REPLAY DISCREPANCY OPEN.**

## Historical result firewall

The official frozen P0Q1 result remains:

- SSI-COV: `SURVIVES_P0Q1`;
- Subspace DMD: `FAILS_P0Q1`;
- Subspace-DMD real-pole-only family: `2/5` false admissions;
- total P0Q1 mechanical exceptions: `0`.

P0-D6 does not rescore, repair, replace or reinterpret that prospective result.

## Why P0-D6 was run

P0Q1 showed that the frozen truth-blind rank-signal conjunction was not qualified for Subspace DMD because it could admit an oscillatory rank signal in a source system containing only stable real poles.

P0-D6 replayed those deterministic source-generation seeds and exposed the full rank/pole structure using the current unchanged core Subspace-DMD/rank-sweep implementation.

The purpose was mechanism diagnosis only.

## Current replay result

Every replayed real-pole record again produced a dominant Subspace-DMD singular-gap candidate at **rank 4**, despite the source generator containing only two stable real continuous-time poles `-0.7` and `-2.4`.

The candidate gaps were enormous rather than marginal:

- replicate 0: `1.2961e12`;
- replicate 1: `8.3616e11`;
- replicate 2: `2.5461e12`;
- replicate 3: `1.8235e11`;
- replicate 4: `8.8071e11`.

The current replay decisions were:

- replicate 0: `REFUSE_UNSTABLE_SELECTED_POLE`;
- replicate 1: `ADMIT_RANK_SIGNAL`;
- replicate 2: `REFUSE_METHOD_EXCEPTION`;
- replicate 3: `REFUSE_UNSTABLE_SELECTED_POLE`;
- replicate 4: `REFUSE_UNSTABLE_SELECTED_POLE`.

Thus the present replay yields **1/5 false admissions plus one method exception**, not the frozen prospective P0Q1 pattern of 2/5 false admissions and zero exceptions.

## Pole-level pathology in the current replay

Representative rank-4 candidate structures include:

### Replicate 1, false admission

- stable complex pole at the discrete-time negative-real-axis/Nyquist branch, reported after continuous-time logarithm as `25 Hz` with real part about `-93.81 /s`;
- stable complex-conjugate pair around `±1.536 Hz`, real part about `-4.216 /s`;
- one stable real pole around `-2.168 /s`.

The truth contains **no oscillatory pole**.

### Replicate 0, refused for instability

- complex-conjugate pair around `±12.47 Hz`;
- one unstable real pole around `+0.099 /s`;
- one stable real pole around `-3.234 /s`.

### Replicates 3–4

Both contain spurious high-frequency/Nyquist-branch structure plus at least one unstable fitted pole and are therefore refused by the frozen rule.

The current replay therefore supports the narrower mechanistic observation:

> At an overcomplete rank selected by a very large projected singular gap, Subspace DMD can convert a real-pole-only stochastic system into complex/high-frequency and/or unstable reduced dynamics. The failure is not explained by the frozen gap threshold being merely too low.

## Reproducibility discrepancy

The current replay is **not accepted as a byte-for-byte/scientifically faithful reproduction of the frozen P0Q1 per-record outcomes**, because the decision pattern differs from the preserved prospective artifact.

The following facts are already established:

- P0Q1 seeds/rule/source generator are preserved;
- current replay uses the same pinned high-level Python/NumPy/SciPy versions as the P0Q1 workflow;
- the core `src/dmd.py` and `src/rank_sweep.py` logic was not intentionally revised to alter the frozen P0Q1 behavior;
- nevertheless the over-rank rank-4 fit differs at the per-record level.

A plausible but **not yet proven** explanation is numerical sensitivity of near-null/over-rank projected subspaces: when the requested reduced rank extends beyond robustly supported dynamical dimension, singular-vector bases associated with tiny directions can be backend/hardware-sensitive, and downstream eigendecomposition/logarithm can change qualitatively.

This explanation must be tested rather than assumed.

## Consequence

1. Do **not** tune the frozen gap threshold on these records.
2. Do **not** use the present replay to replace the historical 2/5 P0Q1 failure count.
3. Treat the Subspace-DMD issue as comparator implementation/reproducibility debt outside System Model v1.0.
4. Preserve rank-2/3/4 spectra, projected singular values, reduced discrete eigenvalues before logarithm, `Uq1` singular values/conditioning and numerical backend identity in the next forensic run.
5. Run the same frozen seeds on multiple clean runner jobs with deterministic thread settings and full BLAS/LAPACK configuration capture.
6. Any revised Subspace-DMD rank/selection method must be a new version and receive new untouched P0-Q evidence.

## Reproducibility identity

GitHub Actions workflow: `NSD Phase0D P0-D6 DMD Real-Pole Diagnosis`
Workflow run: `34566576823`
Job: `103159820863`
Source commit: `9ae62a8d0babe1fd04417e685934fc76583b5e1c`
Artifact ID: `10186220652`
Artifact ZIP SHA-256: `5db1ca67ff27662a20907484397e1315d83ebc7f806a66a69b6892ec49853d6c`

## Disposition

**P0-D6 COMPLETE AS A RETROSPECTIVE DIAGNOSTIC, BUT REPLAY REPRODUCIBILITY REMAINS OPEN.**

The result strengthens the false-complexification/over-rank hypothesis while simultaneously showing that the comparator is numerically fragile enough that the exact historical per-record failure must be preserved separately from current replay behavior.
