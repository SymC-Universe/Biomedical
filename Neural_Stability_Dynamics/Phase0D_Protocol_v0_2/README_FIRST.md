# Neural Stability Dynamics Phase 0D v0.2

Status: **SYSTEM MODEL v1.0 ARCHITECTURE LOCKED / STRUCTURAL ENGINE P0-D + P0-Q ACTIVE / NEUROSTABILITY ATLAS v0.1 ACTIVE / P1 CLOSED.**

This branch is governed prospectively by **General Cross-Project Research Protocol v0.7.1 FINAL plus the authoritative v0.7.1A Functional Mapping and Natural Limit-Testbed Addendum**.

The addendum does not rewrite prior results. Phase 0C remains official FAIL / FAIL / FAIL. Phase 0D v0.1 remains unexecuted/superseded. The frozen P0Q1 result remains SSI-COV `SURVIVES_P0Q1` and Subspace DMD `FAILS_P0Q1`; P0Q1 is not retuned.

## Current program objects

- **System Model:** NSD System Model v1.0, architecture frozen in `SYSTEM_MODEL.md` and `registries/SYSTEM_MODEL_LOCK.json`.
- **Structural Engine:** P0-D/P0-Q implementation and claim-specific qualification remain active. Numerical thresholds, uncertainty propagation, comparator mechanics and P1 rules are not part of the System Model architecture lock.
- **Neurostability Atlas:** v0.1 A0 coordinate ontology and A1 source-selection architecture are frozen. A2 independent coordinate reconstruction is active in `../Neurostability_Atlas_v0_1/`.
- **NSD Tool:** not yet qualified. It requires a qualified Engine plus qualified independent Atlas.
- **Predictive NSD Tool:** not qualified and requires prospective empirical validation beyond the current stage.

## Locked System Model v1.0 architecture

The frozen scientific object hierarchy is:

`scalar/spectral + modal/carrier + conglomerate/system organization + open-channel state`

with the following distinctions preserved:

- latent dimension is not automatically observable dimension;
- individual carrier identity is not automatically invariant-subspace identity;
- structural recovery is not model adequacy;
- point estimates are not estimator-native uncertainty;
- Function Map and Limit Map are coequal scientific targets;
- Engine and Atlas are separate evidence objects.

`chi` is withheld by default. Generic complex poles do not automatically license a second-order chi coordinate, and no whole-system chi is part of the frozen model unless separately derived and validated.

## Current P0 modes

### P0-D: discovery and mechanism mapping

Current uses include:

- Function/Limit mapping on known-truth synthetic systems;
- weak-observability and crowding response surfaces;
- model-adequacy mapping;
- NSD-native Hankel sampling-covariance calibration;
- retrospective diagnosis of the preserved P0Q1 Subspace-DMD real-pole failure;
- Atlas coordinate reconstruction and provenance mapping before any claim-specific qualification rule is frozen.

### P0-Q: qualification and controlled iteration

Current uses include:

- known-truth and known-bad estimator qualification;
- preserved P0Q1 prospective rank-signal qualification;
- pyOMA2 external SSI uncertainty-reference qualification;
- future independently generated Engine qualification families;
- future Atlas qualification on unopened evidence reservoirs after reconstruction/scoring rules are frozen.

Canonical path:

`P0-D -> P0-Q -> P1 frozen confirmation -> P2 release/tool qualification`

## v0.7.1A Function/Limit architecture

NSD treats:

`FUNCTION MAP + LIMIT MAP`

as coequal targets and seeks coverage across:

- `NOMINAL_FUNCTION`;
- `PERTURBED_FUNCTION`;
- `BOUNDARY_OR_TRANSITION`;
- `RARE_NATURAL_LIMIT` where a genuinely qualified natural case exists.

The Atlas intentionally leaves its rare-natural slot empty rather than manufacturing one for symmetry.

## Current mapped findings and open implementation debt

P0-D mapping has established, within its tested synthetic scope, that:

- weak observability can reduce effective observable rank while dominant observable structure remains recoverable;
- crowding can degrade individual carrier identity while preserving a joint carrier subspace;
- model-adequacy diagnostics fail in complementary directions and should remain non-aggregated;
- pyOMA2 supplies a viable external covariance-SSI uncertainty lineage but cannot be copied directly into NSD because the finite-sample Hankel estimator differs;
- the NSD-native batch-Hankel uncertainty candidate tracks the shape of empirical sampling variance strongly but retains duration/batch-dependent scale bias.

Subspace DMD remains a comparator/reproducibility debt after its preserved P0Q1 failure. A current replay differs at the per-record level from the frozen prospective artifact, so historical P0Q1 remains the source of record.

## Atlas handoff

The active Atlas lane is an Engine-independent observational CSD-SVD reconstruction on a frozen SRM repeatability pilot. It uses a predeclared 1–45 Hz grid, no peak picking, source-pinned cleaned derivatives, exact byte verification, and no age/sex/cognitive/diagnostic target inputs. Thirty-four additional SRM repeat participants are sealed as a prospective P0-Q reservoir.

No Atlas value is Structural-Engine selector eligible.

## Existing integrity safeguards

1. confirmatory execution is fail-closed until complete P1 readiness exists;
2. byte-integrity verification is separated from manifest/freeze generation;
3. environment capture is explicit;
4. selector inputs reject truth, desired chi, labels, diagnosis, phenotype, treatment and outcomes;
5. layer-specific and partial/unresolved results remain visible;
6. local observable-order change is preserved as open-channel structure;
7. MFR-14, promotion debt, multiplicity, pathway-specific independence, open-channel state and reproducibility status are explicit records;
8. the System Model content identity is regression-tested;
9. Atlas A0/A1 content locks and A2 method/reservoir freezes are regression-tested separately.

## Deliberate scientific holds

P1 remains blocked until the claim-specific comparator route, estimator-native uncertainty/INDETERMINATE rule, model-adequacy adjudication, unequal-order/crowding treatment required by the proposed P1 scope, evidence-independence map, multiplicity plan and complete MFR-14 are scientifically justified and frozen.

## Development command

`python dev_runner.py`

This runs P0 engineering/compliance tests and environment capture. It does not execute a P1 scientific holdout.

`python local_runner.py` remains intentionally fail-closed until P1 requirements are satisfied and frozen.
