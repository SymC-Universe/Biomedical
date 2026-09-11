# P0-D17 Feedback Transformation Geometry Result

Date: 2026-09-11
Status: **P0-D RESULT. NOT P0-Q. NOT P1. NO ATLAS OUTCOME USED.**
Workflow run: `34622603758`
Job: `103339950812`
Artifact ID: `10273247397`
Artifact ZIP SHA256: `05f1c586ca5035108786307a8eb191e42d010539b735be7cbafdd255a437e13c`

## Question

At equal directed edge norms, does changing the transformation applied along the outgoing and return pathways change the feedback-return operator and the emergent global dynamical coordinates?

## Mechanical result

Nine dedicated feedback-geometry tests passed. These included a basis-invariance test showing that consistent coordinate changes inside subsystems preserve the full coupled spectrum, and tests showing that equal coupling-matrix norms do not imply equal feedback-return operators or equal coupled spectra.

## Design

The local subsystem dynamics were held fixed:

- local chi coordinates: `0.55` and `0.85`;
- local natural frequencies: `3 Hz` and `5 Hz`.

Five feedback architectures were compared. Every outgoing and return coupling template had spectral norm `1`, so at fixed coupling rate `g` every architecture had the same edge norms. Only the transformation geometry differed.

The variants were:

- position-like outgoing / position-like return;
- position-like outgoing / velocity-like return;
- velocity-like outgoing / position-like return;
- velocity-like outgoing / velocity-like return;
- mixed outgoing / mixed return.

No Atlas phenotype, outcome, target range or preferred chi value was used.

## Representative result at g = 12

All edge norms were exactly `12.0` in both directions.

| transformation variant | feedback-return norm DC | feedback-return norm at 3 Hz | global chi lineages | spectral displacement from uncoupled |
|---|---:|---:|---|---:|
| position / position | 4.5837 | 3.8065 | 0.9078, 0.7331 | 36.0179 |
| position / velocity return | 0.0000 | 2.2839 | 0.4857, 0.8294 | 11.5027 |
| velocity outgoing / position return | 4.5837 | 3.8065 | 0.4431, 0.8208 | 17.2560 |
| velocity / velocity | 0.0000 | 2.2839 | 0.4667, 0.9618 | 23.0838 |
| mixed / mixed | 3.2411 | 3.1389 | 0.5432, 0.8563 | 5.6820 |

Every displayed g=12 full system remained stable under this synthetic construction.

## Central result

**Equal coupling magnitude does not determine conglomerate behavior.**

When the local subsystem dynamics and directed edge norms were held fixed, changing only the transformation geometry produced materially different feedback-return operators, global eigenstructure and global chi lineages.

Therefore the conglomerate object must preserve more than scalar connection strength. It must retain at least the directed dynamical mapping and the transformation performed by the receiving/intermediary system before feedback returns.

## Why the DC-zero cases matter

Some velocity-oriented return geometries had zero feedback-return norm at DC while remaining nonzero at 3 Hz. This directly demonstrates that feedback can be frequency dependent: a pathway may be dynamically silent for one class of perturbation and active for another.

Thus a single static coupling weight can lose important conglomerate information even before biological complications are introduced.

## Basis-invariance firewall

A separate test applied invertible coordinate transforms independently inside both subsystems and transformed all coupling blocks consistently. The full coupled spectrum remained unchanged to numerical precision.

This distinguishes physical transformation geometry from arbitrary coordinate relabeling. P0-D17 therefore does not rely on a basis artifact.

## Consequence for the conglomeration axioms

P0-D17 directly supports the following bounded statements:

1. directed coupling magnitude alone is insufficient;
2. feedback transformation geometry matters;
3. feedback is generally frequency dependent;
4. local chi values alone do not determine global chi lineages;
5. the receiving system's internal dynamics and input/output pathway orientation are part of the conglomerate object;
6. basis relabeling must not be confused with physical pathway changes.

## Relationship to the prospective chi 1.2-1.3 note

A separate prospective non-targeted hypothesis was timestamped during this development stating that a natural organizational concentration around approximately `chi ~ 1.2-1.3` may later appear.

P0-D17 did **not** target, select, optimize, bin, stop, or interpret toward that range. Its design and result remain independent of that hypothesis.

## Next P0-D question

The next natural mechanism test is hierarchical closure:

**If a subsystem sends influence through one or more intermediary subsystems before feedback returns, can the grouped intermediary network be reduced to an effective feedback-return operator without losing the relevant coupled eigenstructure?**

This tests whether a conglomerate can itself become a subsystem of a larger conglomerate, which is necessary for the user's intended hierarchy of grouped systems contributing to larger systems.

## Nonclaims

- No neural coupling pathway is inferred.
- No biological transformation family is preferred.
- No universal coupling metric is defined.
- No chi target zone is inferred.
- No single system chi is frozen.
- No Atlas evidence is used.
- No P0-Q or P1 rule is changed.
