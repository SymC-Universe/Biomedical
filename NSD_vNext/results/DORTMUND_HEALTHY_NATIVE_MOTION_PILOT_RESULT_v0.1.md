# Dortmund Healthy Native-Motion Pilot Result v0.1

**Status:** PILOT QUALIFICATION PASS  
**Date:** 2026-10-01  
**Dataset:** OpenNeuro ds005385 v1.0.3  
**Kernel:** `symcuniverse/nsd-dortmund-native-motion-pilot-v0-1`  
**Scientific scope:** independent healthy native EEG baseline only. No NSD-derived quantity entered the run.

## Execution

- selected subjects: 40;
- conditions per subject: EC-pre, EC-post, EO-pre, EO-post;
- expected rows: 160;
- completed rows: 160;
- subject/file failures: 0;
- selection: deterministic age-by-sex stratification from metadata only;
- acquisition-quality rule: `late_ses1=0`.

Exact identities:
- runner SHA-256: `2951450D4B25A271A2974CCE5C01EF41811057DE23A77747ECE38A70DB40D075`;
- summary SHA-256: `DD9C5CF5E9B432706CA0C094C42DCB916862C074C24EC1787AD751A64BADBD0B`;
- feature table SHA-256: `36E83BD950D978ACA60792334AF53B86976D5E9E734492E88C6A6CF98D672389`.

## Native healthy-state result

All four prospectively declared EC-minus-EO directions reproduced without tuning.

| Feature | EC-pre mean | EO-pre mean | EC-EO difference | Paired Cohen d | Literature-direction check |
| --- | ---: | ---: | ---: | ---: | --- |
| posterior alpha relative power | 0.48827 | 0.17741 | +0.31086 | +1.77597 | PASS |
| alpha peak frequency | 10.0952 Hz | 9.4666 Hz | +0.6287 Hz | +0.38421 | PASS |
| theta/beta ratio | 0.68514 | 1.20975 | -0.52461 | -0.59888 | PASS |
| aperiodic exponent | 1.03647 | 1.23865 | -0.20219 | -0.56031 | PASS |

The effect magnitudes differ from the published full-cohort values. No parameter was changed after outcome access. Differences remain evidence to be explained by sample composition, implementation details, and/or estimator choices when the full clean cohort is complete.

## Healthy pre/post-load displacement in the pilot

Mean post-minus-pre displacement:

- posterior alpha relative power: EC -0.00973, EO +0.00541;
- alpha peak frequency: EC -0.18921 Hz, EO +0.21362 Hz;
- theta/beta ratio: EC +0.06421, EO -0.07139;
- aperiodic exponent: EC -0.03644, EO -0.09442.

These are pilot descriptive quantities only. They do not yet define healthy recovery, overshoot, rebound, or migration because the dataset provides pre/post resting snapshots rather than a continuous post-perturbation trajectory.

## Disposition

`PILOT_QUALIFICATION_PASS`.

The native pipeline is sufficiently coherent to scale prospectively. The 40 completed subjects are durable evidence and must not be recomputed merely to simplify the full-cohort run.

A newly documented acquisition-quality field states that nonzero `late_ses1` marks late triggers and probable discontinuity. Because this was identified before full-cohort outcome opening, the full baseline will restrict session-1 analysis to `late_ses1=0`.

Clean session-1 population:
- 517 of 608 participants;
- 91 excluded prospectively for nonzero late-trigger count;
- 173 of the clean session-1 participants also have clean `session2=yes, late_ses2=0` follow-up.

## Next action

Process the remaining 477 clean session-1 participants in neutral checkpointed batches using the same native method, then merge with the already-completed 40-person pilot. No NSD (chi), (Chi), or (Chi_{mathrm{arc}}) enters until the native healthy baseline is frozen.
