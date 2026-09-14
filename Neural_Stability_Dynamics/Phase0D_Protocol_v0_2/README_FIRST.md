# Neural Stability Dynamics Phase 0D v0.2

Status: **SYSTEM MODEL v1.0 ARCHITECTURE LOCKED / STRUCTURAL ENGINE P0-D + P0-Q ACTIVE / NEUROSTABILITY ATLAS v0.1 ACTIVE / P1 CLOSED.**

Current governing baseline: **General Cross-Project Research Protocol v0.7.7, dated 13 September 2026, status `Active Baseline`.** The branch name ending in `protocol-v0.7.1` is a historical/execution identifier only.

The protocol transition does not rewrite prior results. Phase 0C remains official FAIL / FAIL / FAIL. Phase 0D v0.1 remains unexecuted/superseded. Frozen P0Q1 remains SSI-COV `SURVIVES_P0Q1` and Subspace DMD `FAILS_P0Q1`; P0Q1 is not retuned or rescored.

## Current program objects

- **System Model:** NSD System Model v1.0, architecture frozen in `SYSTEM_MODEL.md` and `registries/SYSTEM_MODEL_LOCK.json`.
- **Structural Engine:** P0-D/P0-Q implementation and claim-specific qualification remain active. Numerical thresholds, uncertainty propagation, comparator mechanics, recovery criteria, and P1 rules are not part of the System Model architecture lock.
- **Neurostability Atlas:** v0.1 A0 coordinate ontology and A1 source-selection architecture are frozen. A2 independent coordinate reconstruction remains active in `../Neurostability_Atlas_v0_1/`.
- **NSD Tool:** not yet qualified. It requires a qualified Engine plus qualified independent Atlas.
- **Predictive NSD Tool:** not qualified and requires prospective empirical validation beyond the current stage.

## Locked System Model v1.0 architecture

The frozen starting representation hierarchy is:

`scalar/spectral + vector/modal/carrier + conglomerate/system organization + open-channel state`

These are complementary starting views from which a fuller chi/stability architecture may be progressively reconstructed. They are not asserted to be exhaustive, statistically independent, ontologically separate, or arithmetically combinable.

The following distinctions remain mandatory:

- latent dimension is not automatically observable dimension;
- individual carrier identity is not automatically invariant-subspace identity;
- local dynamical identity is not embedded realized behavior;
- structural recovery is not model adequacy;
- asymptotic return is not finite-time resilience;
- exact state-preserving grouping is not arbitrary dimensionality reduction;
- point estimates are not estimator-native uncertainty;
- Function Map and Limit Map are coequal scientific targets;
- Engine and Atlas are separate evidence objects.

`chi` is withheld by default. Generic complex poles do not automatically license a second-order chi coordinate, and no whole-system chi is part of the frozen model unless separately derived and validated. Lower-level chi values are not averaged into `chi_system`.

## Current P0 modes

### P0-D: discovery and mechanism mapping

Current uses include:

- Function/Limit mapping on known-truth synthetic systems;
- weak-observability, crowding, conditioning, and identifiability response surfaces;
- model-adequacy and explicit refusal mapping;
- NSD-native Hankel sampling-covariance calibration;
- relational coupling, feedback transformation, hierarchy, and recovery mapping;
- retrospective diagnosis of the preserved P0Q1 Subspace-DMD real-pole failure;
- Atlas coordinate reconstruction and provenance mapping before claim-specific qualification rules are frozen.

### P0-Q: qualification and controlled iteration

Current uses include:

- known-truth and known-bad estimator qualification;
- preserved P0Q1 prospective rank-signal qualification;
- external uncertainty-reference qualification;
- future independently generated Engine qualification families;
- future Atlas qualification on unopened evidence reservoirs after reconstruction/scoring rules are frozen.

Canonical path:

`P0-D -> P0-Q -> P1 frozen confirmation -> P2 release/tool qualification`

## Function / Limit architecture

NSD treats `FUNCTION MAP + LIMIT MAP` as coequal targets and preserves `NOMINAL_FUNCTION`, `PERTURBED_FUNCTION`, `BOUNDARY_OR_TRANSITION`, `RARE_NATURAL_LIMIT`, `NOT_APPLICABLE`, `NOT_AVAILABLE`, and `UNRESOLVED` where appropriate.

Rare/extreme cases are high-information probes rather than default representatives. Scope is earned across tested systems and regimes; universality is not a protocol target.

## Current mapped findings

Within the tested P0-D synthetic scope:

- weak observability can reduce effective observable rank while dominant observable structure remains recoverable;
- crowding can degrade individual carrier identity before destroying a joint carrier subspace;
- model-adequacy diagnostics fail in complementary directions and should remain non-aggregated;
- arithmetic pooling or participation-weighted averaging of local chi values is not a defensible definition of conglomeration;
- reciprocal coupling can reorganize global modal lineages while local dynamical identities remain fixed;
- matched coupling norms do not determine embedded behavior because feedback transformation geometry matters;
- closed-loop recovery can improve and then erode non-monotonically while all tested systems remain asymptotically stable;
- exact state-preserving hierarchical grouping can preserve the outer recovery response, while dropping an internally coupled component changes that response;
- finite-sample conditioning and identifiability remain central limits near/above the chi=1 branch transition.

P0-D22 now challenges whether observation/effective-dimension structure can manufacture apparent chi/recovery relationships while latent truth is fixed. P0-D23 deliberately violates the stationary comparison assumption and tests whether the existing Engine refuses or preserves partial information rather than forcing a prediction.

## Atlas handoff

The Atlas remains Engine-independent. No Atlas value is Structural-Engine selector eligible. The firewalled prospective note `chi ~ 1.2-1.3` is excluded from model construction, selection, tuning, binning, stopping, and interpretation until independent Atlas mapping exists.

## Current v0.7.7 execution controls

1. confirmatory execution remains fail-closed until complete P1 readiness exists;
2. byte-integrity verification is separated from manifest/freeze generation;
3. environment capture is explicit;
4. selector inputs reject truth, desired chi, labels, diagnosis, phenotype, treatment and outcomes;
5. layer-specific refusal, partial, unresolved, and indeterminate results remain visible;
6. local observable-order change is preserved as open-channel structure;
7. MFR-14, promotion debt, multiplicity, pathway-specific independence, open-channel state and reproducibility status remain explicit records;
8. System Model identity and Atlas freezes are regression-tested independently;
9. materially inherited foundations are subject to the v0.7.5 robustness-activation rule;
10. active dependencies receive monitoring proportional to their runtime, checkpoint, recovery, and silent-stall risk;
11. new research sessions load the current GP and current source-of-record state before inheriting work;
12. monitoring liveness is not treated as scientific progress.

Current P0-D jobs are short-lived GitHub Actions jobs with direct workflow/step status, logs, artifact + digest capture, branch-wide validation, and source-of-record result notes. A separate persistent watchdog is not proportionate for this workload class; that determination must be revisited if the dependency class changes.

## Deliberate scientific holds

P1 remains blocked until the claim-specific comparator route, estimator-native uncertainty/INDETERMINATE rule, model-adequacy adjudication, unequal-order/crowding treatment required by the proposed P1 scope, evidence-independence map, multiplicity plan and complete MFR-14 are scientifically justified and frozen.

The current recovery sequence must additionally finish its null-floor and deliberate-refusal challenges and then undergo a v0.7.7 milestone/foundational-dependency/monitor-coverage audit before any recovery-related P0-Q proposal.

## Development command

`python dev_runner.py`

This runs P0 engineering/compliance tests and environment capture. It does not execute a P1 scientific holdout.

`python local_runner.py` remains intentionally fail-closed until P1 requirements are satisfied and frozen.
