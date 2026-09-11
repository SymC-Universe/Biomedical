# NSD System Model v1.0 Lock Audit

Date: 2026-09-11
Governing protocol: General Cross-Project Research Protocol v0.7.1 FINAL + authoritative v0.7.1A Addendum
Disposition: **LOCK CONFIRMED. SYSTEM MODEL v1.0 MAY REMAIN ARCHITECTURE_FROZEN_P0.**

## Audit question

Do the completed P0-D/P0-Q results require changing the NSD System Model object ontology or logical relationships, or do they only constrain implementation/qualification beneath the already-declared model?

## Result

No completed result requires reopening the System Model v1.0 ontology.

### P0-D2 weak observability

Supports the frozen distinction:

`latent state dimension != observable structural dimension`

The result changes how an Engine must qualify observable-order claims, not the System Model object hierarchy.

### P0-D3 crowding

Supports the frozen distinction:

`individual carrier identity != invariant/crowded-subspace identity`

The result constrains future adjudication/uncertainty rules but does not require a new object class.

### P0-D4 model adequacy

Supports the existing open-channel and model-adequacy architecture. Residual/model-error structure, out-of-sample reconstruction/prediction, fitted stability and order/window sensitivity fail in complementary directions and therefore remain separate claim-support objects.

No aggregate adequacy scalar is added to the System Model.

### pyOMA2 P0-Q reference

Supports the frozen principle that uncertainty must correspond to the estimator/object actually computed. Direct finite-sample uncertainty transfer is refused because the external covariance-Hankel estimator differs from NSD's.

This narrows the Engine uncertainty implementation problem and does not alter the System Model.

### P0-D5 NSD-native Hankel sampling covariance

The NSD-native batch candidate reproduces the *shape* of empirical Hankel sampling variance strongly across the tested nominal/white-noise conditions, with log-variance correlations approximately 0.967-0.975. Scale remains duration/batch dependent: median predicted/empirical variance ratios ranged approximately 0.899-1.263 across tested settings.

Therefore estimator-native uncertainty remains a valid frozen System-Model requirement, while the uncertainty procedure itself remains unfrozen Engine/P0-Q work.

Workflow run: `34566463681`
Artifact ID: `10186186058`
Artifact SHA-256: `d879dd78443b6780eafd6baee2bd292d8b48ad7bdc311cb37b4010b8ab7a7103`

### P0-D6 Subspace-DMD real-pole diagnosis

The retrospective frozen-record diagnosis localizes the P0Q1 Subspace-DMD failure to method-specific false complexification/instability/exception behavior at selected rank 4 for the real-pole-only family.

Observed selected-rank outcomes:

- replicate 0: false complex pair plus one unstable real pole -> refused;
- replicate 1: stable false complex structure -> false admission;
- replicate 2: method exception -> refused;
- replicate 3: false complex structure plus unstable real pole -> refused;
- replicate 4: false complex structure plus unstable real pole -> refused.

The diagnosis reinforces why estimator disagreement, failed fits and invented structure belong in the open channel. It is an Engine/comparator defect and does not require a System Model revision.

Workflow run: `34566576823`
Artifact ID: `10186220652`
Artifact SHA-256: `5db1ca67ff27662a20907484397e1315d83ebc7f806a66a69b6892ec49853d6c`

The official P0Q1 result remains unchanged.

## Lock criteria

System Model v1.0 is considered architecture-locked because the following are now both conceptually specified and supported by P0 evidence as necessary distinctions:

1. spectral/pole, modal/carrier, conglomerate/system and open-channel views remain separate but complementary;
2. latent and observable dimension are separate objects;
3. individual carrier and crowded-subspace identity are separate claim objects;
4. partial/refusal/unresolved/indeterminate states are preserved claim-specifically;
5. model adequacy is distinct from structural recovery;
6. estimator-native uncertainty/identifiability is part of epistemic state;
7. Function Map and Limit Map are coequal;
8. Atlas and Engine roles remain separated;
9. whole-system chi and unlicensed pole-to-chi transformations remain withheld;
10. repeated open-channel structure may motivate a future v1.x/v2 model revision but is not silently promoted into v1.0.

## What remains outside the lock

The following are explicitly **not** reasons to reopen v1.0 unless they later force a new object ontology:

- final SSI-COV uncertainty propagation;
- confidence or multiplicity convention;
- operational observable-rank rule;
- crowding adjudication threshold;
- model-adequacy thresholds/search space;
- Subspace-DMD repair or replacement;
- final comparator choice;
- P1 challenge/freeze details;
- Atlas coordinate values/ranges;
- biological, phenotypic or clinical interpretation;
- any future chi admission/derivation.

## Final disposition

**NSD SYSTEM MODEL v1.0 = LOCKED AT THE ARCHITECTURE LEVEL.**

The next queued scientific object is the Neurostability Atlas coordinate map. Atlas construction must begin from the locked System-Model objects and explicit provenance/independence rules; it must not back-drive the Engine toward desired biological or chi coordinates.
