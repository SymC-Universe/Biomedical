# Neural Stability Dynamics Phase 0D v0.2 Protocol Reconciliation

Status: **P0-D DISCOVERY/MAPPING + P0-Q QUALIFICATION. NOT A P1 HOLDOUT.**

This version originated because General Cross-Project Research Protocol v0.7.1 became authoritative on 2026-09-10 before Phase 0D v0.1 was scientifically executed. It is now governed prospectively by **v0.7.1 FINAL plus the authoritative v0.7.1A Functional Mapping and Natural Limit-Testbed Addendum**. Phase 0D v0.1 is preserved as an untouched, superseded candidate and must not be run as a confirmatory holdout.

The v0.7.1A addendum does not rewrite prior results. Phase 0C remains official FAIL / FAIL / FAIL. The frozen P0Q1 rank-signal result remains SSI-COV `SURVIVES_P0Q1` and Subspace DMD `FAILS_P0Q1`; P0Q1 is not retuned.

## Current program object

- System Model: NSD System Model, still under construction.
- Engine: NSD Structural Engine candidate, currently qualified only for P0 synthetic structural-method development/qualification.
- Atlas: Neurostability Atlas not yet qualified.
- Tool: NSD Tool not yet qualified.
- Predictive Tool: not qualified.

## Current P0 modes

### P0-D - discovery and mechanism mapping

Current uses include:

- retrospective diagnosis of the already-seen P0Q1 Subspace-DMD real-pole false admissions;
- Function Map and Limit Map construction on known-truth synthetic systems;
- response surfaces, rank landscapes, recovery curves, estimator disagreements, uncertainty surfaces and open-channel structure;
- candidate mechanism/method hypotheses that remain exploratory until separately qualified.

### P0-Q - qualification and controlled iteration

Current uses include:

- known-truth and known-bad estimator qualification;
- controlled sensitivity and identifiability tests;
- pyOMA2 / SSI-COV point-estimator and uncertainty-reference compatibility;
- future independently generated qualification families after rules are versioned.

Canonical path:

`P0-D -> P0-Q -> P1 frozen confirmation -> P2 release/tool qualification`

## v0.7.1A mapping architecture

NSD now treats the following as coequal scientific targets where applicable:

`FUNCTION MAP + LIMIT MAP`

and seeks explicit research-role coverage across:

- `NOMINAL_FUNCTION`;
- `PERTURBED_FUNCTION`;
- `BOUNDARY_OR_TRANSITION`;
- `RARE_NATURAL_LIMIT`.

At the current synthetic stage, `RARE_NATURAL_LIMIT` is not applicable. It will not be manufactured for symmetry.

P0 mapping may use the descriptive location states `WORKS_HERE`, `STOPS_WORKING_HERE`, and `NOT_KNOWN_HERE`; these are mapping statuses, not P1 confirmation.

## Existing integrity safeguards retained

1. confirmatory execution is fail-closed until a complete P1 readiness record exists;
2. byte-integrity verification is separated from manifest generation;
3. environment capture is explicit;
4. selector inputs pass through a closed production interface that rejects truth, chi, labels, diagnosis, phenotype, treatment and outcomes;
5. semantic result validation is implemented independently for core summary fields;
6. Layer C reports carrier, participation and relational-geometry status separately, and unresolved geometry produces a PARTIAL rather than full ADMIT result;
7. local-order change remains visible as an open-channel event rather than being silently discarded;
8. MFR-14, promotion debt, multiplicity, Atlas independence, open-channel state and reproducibility status are explicit records.

## Deliberate scientific holds

No P1 scientific holdout design or seed is authorized. P1 remains blocked until the comparator-selection route, uncertainty/INDETERMINATE rule, model-adequacy role, unequal-order shared-mode treatment, evidence-independence map and complete MFR-14 are scientifically justified and frozen.

## Development command

`python dev_runner.py`

This runs P0 engineering/compliance tests and environment capture. It does not execute a P1 scientific holdout.

`python local_runner.py` is intentionally blocked until P1 requirements are satisfied and frozen.
