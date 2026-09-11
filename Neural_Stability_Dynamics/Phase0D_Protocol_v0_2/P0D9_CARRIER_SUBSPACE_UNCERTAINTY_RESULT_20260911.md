# P0-D9 Carrier/Subspace Uncertainty Result

Date: 2026-09-11
Status: P0-D RESULT. NOT P0-Q. NOT P1.
Workflow run: `34611913154`
Job: `103304242179`
Artifact ID: `10267959493`
Artifact ZIP SHA256: `0e8c2702dd8c4bc12590c07ab4e66f297a22831de9838ded5c8bd908b5a489ca`

## Question

Can estimator-native sampling uncertainty be attached to the joint observable carrier subspace when individual carrier identity becomes fragile under modal crowding?

## Result

Yes, within the tested P0-D synthetic regimes. The basis-invariant carrier projector `P = Q Q*` remained a well-behaved uncertainty object across separated, moderately crowded and strongly crowded two-mode systems.

All requested perturb-and-refit propagations completed successfully. Five dedicated modal/subspace uncertainty unit tests passed in the workflow.

### Individual identity versus joint subspace

| separation | samples | median individual MACs | median max principal angle to truth (rad) |
|---|---:|---|---:|
| 2.0 Hz | 3600 | 0.999951, 0.999972 | 0.002463 |
| 2.0 Hz | 7200 | 0.999972, 0.999982 | 0.001421 |
| 0.30 Hz | 3600 | 0.997609, 0.995237 | 0.003436 |
| 0.30 Hz | 7200 | 0.997480, 0.997638 | 0.002542 |
| 0.05 Hz | 3600 | 0.893490, 0.888810 | 0.002755 |
| 0.05 Hz | 7200 | 0.913008, 0.939738 | 0.001696 |

At 0.05 Hz separation the one-to-one carrier labels degrade substantially, while the joint two-dimensional observable carrier subspace remains close to the truth subspace. This independently reproduces the qualitative resolution hierarchy seen in P0-D3 using a different uncertainty-focused calculation.

### Predicted versus empirical projector variance

For the joint carrier projector, mean predicted first-order variance divided by empirical across-realization projector variance ranged approximately from `0.821` to `1.148` across all tested conditions, durations and batch counts.

Representative values at epsilon 0.50:

| separation | samples | batches | predicted / empirical projector variance |
|---|---:|---:|---:|
| 2.0 Hz | 3600 | 6 | 0.900 |
| 2.0 Hz | 3600 | 12 | 0.897 |
| 2.0 Hz | 7200 | 6 | 1.030 |
| 2.0 Hz | 7200 | 12 | 1.148 |
| 0.30 Hz | 3600 | 6 | 0.940 |
| 0.30 Hz | 3600 | 12 | 1.025 |
| 0.30 Hz | 7200 | 6 | 0.822 |
| 0.30 Hz | 7200 | 12 | 0.870 |
| 0.05 Hz | 3600 | 6 | 0.870 |
| 0.05 Hz | 3600 | 12 | 0.977 |
| 0.05 Hz | 7200 | 6 | 0.837 |
| 0.05 Hz | 7200 | 12 | 0.846 |

The finite-difference calculation is again locally stable. Median absolute log differences in predicted projector variance between epsilon 0.25 and 0.50 were only about `0.00040-0.00362`.

## Interpretation

P0-D9 supports a resolution-aware uncertainty architecture:

1. **Resolvable individual mode:** pole coordinate uncertainty and carrier-specific evidence may be meaningful.
2. **Crowded but coherent cluster:** the joint carrier subspace/projector can remain identifiable and admit a stable geometric uncertainty object even when individual carrier labels degrade.
3. **Insufficiently resolved structure:** if neither individual objects nor a stable cluster representation is supported, the appropriate state is unresolved/indeterminate/refusal rather than forced labeling.

This is consistent with the locked System Model v1.0 distinction between individual carrier identity and crowded-subspace identity. It does not require reopening the System Model.

## Important restraint

P0-D9 does not define a crowding boundary. The 2.0, 0.30 and 0.05 Hz separations were selected after earlier P0-D crowding work and are development stresses. No MAC, principal-angle, projector-variance or resolution threshold may be frozen from these records.

No confidence region on a Grassmann manifold is claimed. The projector variance is a first-order total sampling-variability descriptor.

## Next implication

Carrier/subspace uncertainty is no longer an undefined MFR-09 concept. A concrete estimator-native candidate object now exists. Independent P0-Q qualification and a later resolution/adjudication convention remain required before prospective use.