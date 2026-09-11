# NSD P0-D3 Crowding Response-Surface Result

Date: 2026-09-11
Protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Status: **P0-D RESPONSE-SURFACE EVIDENCE. NOT P0-Q QUALIFICATION. NOT P1.**

## Scientific question

As two fully observed oscillatory modes approach one another in frequency, how do individual carrier identity, joint carrier-subspace recovery, pole recovery and structural completeness reorganize for SSI-COV and Subspace DMD?

This question was intentionally separated from P0-D2 weak observability. P0-D2 weakens one mode through the observation map. P0-D3 keeps both modes fully observed and instead reduces their frequency separation.

## Design

Two complex modes were simulated with:

- decay of each mode: `0.7`;
- first frequency: `6 Hz`;
- second frequency: `6 Hz + separation`;
- separations: `4.0, 2.0, 1.0, 0.5, 0.30, 0.22, 0.15, 0.10, 0.05, 0.02 Hz`;
- six observed channels;
- 5% white measurement noise;
- `dt = 0.02`;
- `2400` samples;
- planted state order `4`;
- eight deterministic replicates per separation and method.

The map preserved separately:

1. complete stable two-mode candidate-set generation at planted order;
2. truth-to-estimator individual carrier assignment quality;
3. joint two-mode carrier-subspace similarity;
4. relative pole recovery;
5. assignment margin;
6. estimated mode separation;
7. data-only adjacent-rank stability and singular spectra.

No MAC, assignment-margin, crowding-ratio, pole-error or subspace threshold was selected from this surface.

## Main result

**Both estimators retained a complete stable two-mode candidate set in all eight replicates at every tested separation.** The crowding transition therefore did not present as disappearance of the two-mode candidate set in this synthetic domain.

Instead, the first strong degradation occurred in **individual carrier identity**, while the **joint two-mode carrier subspace remained essentially unchanged**.

Representative medians:

| Separation | Method | Individual MAC median | Minimum individual MAC median | Joint carrier-subspace similarity | Relative pole-distance median |
|---:|---|---:|---:|---:|---:|
| 4.00 Hz | SSI-COV | 0.99986 | 0.99981 | 0.999986 | 0.00618 |
| 4.00 Hz | Subspace DMD | 0.99988 | 0.99980 | 0.999988 | 0.00396 |
| 0.30 Hz | SSI-COV | 0.98208 | 0.97156 | 0.999981 | 0.00445 |
| 0.30 Hz | Subspace DMD | 0.99021 | 0.98428 | 0.999981 | 0.00304 |
| 0.10 Hz | SSI-COV | 0.93375 | 0.92621 | 0.999976 | 0.00359 |
| 0.10 Hz | Subspace DMD | 0.96264 | 0.95164 | 0.999981 | 0.00405 |
| 0.05 Hz | SSI-COV | 0.69498 | 0.58465 | 0.999991 | 0.00445 |
| 0.05 Hz | Subspace DMD | 0.72588 | 0.67450 | 0.999990 | 0.00461 |
| 0.02 Hz | SSI-COV | 0.76404 | 0.58301 | 0.999986 | 0.00630 |
| 0.02 Hz | Subspace DMD | 0.68292 | 0.52118 | 0.999987 | 0.00431 |

The non-monotonic individual-MAC medians at the two smallest separations are themselves a warning against inferring a sharp numerical boundary from this exploratory surface. Assignment margins also contracted substantially, from roughly `2.6` at 4 Hz separation to roughly `0.6-0.8` at the smallest separations, consistent with increasing ambiguity in one-to-one individual-mode labeling.

The joint carrier-subspace similarity remained approximately `0.99998-0.99999` across the full sweep. Pole-distance medians also remained small across the tested separations.

## Interpretation ceiling

This P0-D surface supports the exploratory statement:

> In the tested fully observed two-mode synthetic family, decreasing frequency separation can make the identity of individual carriers increasingly ambiguous while leaving the joint two-mode carrier subspace and pole set strongly recoverable. Therefore individual-mode identifiability and invariant-subspace identifiability are distinct claim objects and should not share a single admission gate.

This strengthens the prior crowding interpretation discovered after Phase 0C, but does not establish a universal crowding threshold, a biological transition, or global superiority of either estimator.

The data also argue against treating a complete stable pole set as sufficient evidence that every individual eigenvector/carrier label is identifiable. At the smallest separations the pole set survives while individual carrier matching is materially weaker.

## Protocol consequences

1. Preserve the current architecture in which crowded modes may support an invariant-subspace claim even when individual mode identity is unresolved.
2. Keep individual and subspace uncertainty/adjudication separate in any future P0-Q design.
3. Do not infer a crowding cutoff from the present response surface. Any operational threshold or transition rule selected after inspecting this map would be P0-D/data-derived and would require independent P0-Q qualification.
4. Do not use this map to rescue, alter, or reinterpret P0Q1.
5. No P1 design, EEG interpretation, chi coordinate, mechanistic neural boundary or clinical claim is licensed.

## Reproducibility identity

GitHub Actions workflow: `NSD Phase0D P0-D3 Crowding Surface`
Workflow run: `34565360206`
Job: `103156262301`
Artifact ID: `10185803487`
Artifact ZIP SHA-256: `cfeec47296071ca7a345952f8729533a9a65ee3e52b3d2030ddb896512b30b55`
Artifact contents: crowding response-surface JSON + environment JSON.
Source commit for the run: `81f37c2c8fe5c4540ab6314ee0c552cc393de0f5`.

## Disposition

**P0-D3 COMPLETE.** It strengthens an existing post-result crowding hypothesis and improves the Function/Limit map by locating a region where the representation changes from stable individual identity toward stable joint-subspace identity without a corresponding collapse of the recovered pole set. Promotion debt remains unpaid until an independently generated P0-Q qualification tests any operationalized rule.
