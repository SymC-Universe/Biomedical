# NSD P0-D2 Weak-Observability Response Surface Result

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + v0.7.1A Addendum
Status: **P0-D POST-RESULT RESPONSE-SURFACE EVIDENCE. NOT P0-Q REQUALIFICATION. NOT P1.**

## Why this surface was run

P0-D1 localized all five planted-rank candidate-set stops to the weak-observability condition. The weak-observability axis was therefore selected after seeing P0-D1 and is explicitly data-derived/post-result.

The run reused the exact frozen P0Q1 rank-signal rule only as a **non-independent diagnostic overlay**. This cannot change the official P0Q1 outcomes:

- SSI-COV: `SURVIVES_P0Q1`;
- Subspace DMD: `FAILS_P0Q1`;
- no P0Q1 threshold or family was retuned.

## Design

The same two-mode, four-state synthetic family was evaluated while the second mode's observation scale varied through:

`1.0, 0.5, 0.25, 0.10, 0.05, 0.03, 0.02, 0.01, 0.005`

Eight deterministic replicates were generated per scale for SSI-COV and Subspace DMD. The exact P0Q1 candidate grid `1..8` and frozen gap/admission logic were retained for the diagnostic overlay.

The map deliberately kept separate:

1. planted latent state order (`4`);
2. data-only rank selected by the historical P0Q1 gate;
3. truth-based recovery evaluated only after estimation.

## Main result

The response surface supports a **latent-completeness versus observable-structure distinction**.

At strong observability, both methods selected rank 4 in every replicate:

- weak scale 1.0: SSI-COV 8/8 rank 4; Subspace DMD 8/8 rank 4;
- weak scale 0.5: SSI-COV 8/8 rank 4; Subspace DMD 8/8 rank 4.

As the second mode became weaker, the operational rank transitioned toward 2, but the transition occurred at different points for the two estimators:

- scale 0.25: SSI-COV selected rank 2 in 3/8 and rank 4 in 5/8; Subspace DMD remained rank 4 in 8/8;
- scale 0.10: SSI-COV selected rank 2 in 8/8; Subspace DMD remained rank 4 in 8/8;
- scale 0.05: SSI-COV rank 2 in 8/8; Subspace DMD rank 2 in 6/8 and rank 4 in 2/8;
- scale 0.03: SSI-COV rank 2 in 8/8; Subspace DMD rank 2 in 7/8 and rank 4 in 1/8;
- scale 0.02: SSI-COV rank 2 in 8/8; Subspace DMD rank 2 in 7/8 and rank 4 in 1/8;
- scales 0.01 and 0.005: both methods selected rank 2 in 8/8.

The truth-side output-mode norm ratio fell continuously from approximately `0.871` at scale 1.0 to `0.0124` at scale 0.005. No threshold is inferred from this exploratory surface.

## The important asymmetry

The frozen rank-signal overlay returned `ADMIT_RANK_SIGNAL` for every record across this surface. That does **not** mean the four-state latent system remained fully observable. It means a strong admissible rank signal remained present, sometimes at rank 4 and increasingly at rank 2.

At low observability, the rank-2 candidate retained very strong recovery of the dominant observable structure. Representative medians:

- SSI-COV scale 0.03, rank-2 candidate: relative pole error `0.00487`, carrier-subspace similarity `0.999990`;
- Subspace DMD scale 0.03, candidate rank mostly 2: relative pole error `0.00324`, carrier-subspace similarity `0.999992`;
- SSI-COV scale 0.005, rank-2 candidate: relative pole error `0.00432`, carrier-subspace similarity `0.999994`;
- Subspace DMD scale 0.005, rank-2 candidate: relative pole error `0.00333`, carrier-subspace similarity `0.999994`.

Meanwhile, forcing the planted rank 4 became progressively less defensible. For SSI-COV the planted-rank median pole error rose from about `0.00227` at scale 1.0 to `0.278` at 0.03, `0.315` at 0.01 and `0.286` at 0.005; the planted-rank median unstable fraction reached `0.5` at scale 0.01 and `0.25` at scale 0.005. Subspace DMD's forced rank-4 degradation occurred later and was generally smaller, but its rank selection also eventually collapsed to 2.

## Interpretation ceiling

This P0-D surface supports the following exploratory interpretation:

> When a latent mode becomes sufficiently weak in the observation map, effective observable rank can fall below latent state count while a lower-rank estimate continues to recover the dominant observable structure accurately. Therefore failure to reconstruct the full planted latent order is not equivalent to failure of observable structural recovery.

It also shows that the location/shape of that transition is estimator-dependent. The present surface does **not** license a universal weak-observability threshold or a claim that either estimator is globally superior.

## Protocol consequences

1. P0-D1's five planted-rank `STOPS_WORKING_HERE` records remain valid for their narrow claim object, but must not be generalized into whole-estimator failure.
2. Future Function/Limit maps must distinguish at least:
   - latent-completeness recovery;
   - observable-rank recovery;
   - pole/carrier accuracy;
   - model adequacy;
   - refusal/indeterminacy.
3. A future P0-Q test may ask prospectively whether an observable-rank transition can be recovered without access to latent truth, but any such rule/version requires independent qualification evidence.
4. No P1 design, threshold, uncertainty rule, chi coordinate, biological interpretation or neural boundary is frozen from this surface.

## Reproducibility identity

GitHub Actions workflow: `NSD Phase0D P0-D2 Weak Observability Surface`
Workflow run: `34565054637`
Artifact ID: `10185711989`
Artifact ZIP SHA-256: `a7c7903ca0aa50ad3ca6b587a6fac455cb9d0f20816877dd466761c2ad3c786b`
Artifact contents: response-surface JSON + environment JSON.

## Disposition

**P0-D2 COMPLETE.** The result is scientifically useful discovery/mechanism mapping and creates promotion debt if converted into a future operational rule. It does not pay existing promotion debt and does not reopen P0Q1.
