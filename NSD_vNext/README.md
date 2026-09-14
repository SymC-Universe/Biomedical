# NSD vNext — Living Research Workspace

Status: ACTIVE RECONSTRUCTION / NOT A VALIDATED CLINICAL TOOL
Date initialized: 14 September 2026
Governing manual: SymC General Operations Manual v0.8.0
Working branch: `nsd-rebuild-gom-v0.8.0`

This directory is the forward NSD research workspace. Historical NSD PDFs and archives remain provenance, not current evidentiary authority.

The working architecture is:

`NSD System Model -> Structural Engine`

plus

`Independent Neurostability Atlas`

leading, only after validation, to

`NSD Tool`

The project treats scalar, vector/modal, and conglomerate/system representations as starting components of a larger stability architecture. It does not force every subject, session, channel, mode, disorder, or dataset into a single chi value.

## Canonical working files

### Manuscript

- `manuscript/NSD_MANUSCRIPT_WORKING_v0.1.md` — living forward manuscript draft; historical figures/results enter only after evidence reclassification.

### Governance and continuity

- `docs/NSD_PROJECT_PROTOCOL_v0.1.md` — project-local safeguards under GOM v0.8.0.
- `docs/CONTINUITY_STATE_v0.1.md` — current continuity record and permanent historical correction.
- `docs/GOM_v0.8.0_ADOPTION_CHECKLIST_v0.1.md` — project migration/adoption record.
- `docs/CLAIM_LEDGER_v0.1.md` — evidence ceiling for every major manuscript claim.
- `docs/PENDING_RESULT_INSERTS_v0.1.md` — manuscript locations blocked by computation or re-audit.
- `docs/TASK_FREEZE_TEMPLATE_v0.1.md` — task-level preregistration/freeze template for P0-Q/P1 work.

### Historical reconstruction

- `docs/HISTORICAL_SOURCE_AUDIT_v0.1.md` — source-level audit of the recovered 2025 NSD TeX/PDF package, including figure-by-figure evidentiary classification.

### Measurement, datasets, and model qualification

- `docs/ESTIMATOR_LICENSING_MATRIX_v0.1.md` — defines when a feature is dynamically derived, operational, proxy-only, empirical, categorical, or refused.
- `docs/STRUCTURAL_ENGINE_SPEC_v0.1.md` — label-blind executable architecture and refusal rules.
- `docs/KNOWN_TRUTH_ADVERSARIAL_TEST_MATRIX_v0.1.md` — preclinical synthetic/adversarial qualification plan.
- `docs/DATASET_PROVENANCE_AUDIT_v0.1.md` — subject/session/run/trial hierarchy and dataset admission controls plus first real public-data audits.
- `docs/FORWARD_DATASET_CANDIDATES_v0.1.md` — current forward EEG dataset sequence and gate status.
- `docs/ENGINE_IMPLEMENTATION_PLAN_v0.1.md` — staged implementation sequence from provenance through qualified clinical overlay.
- `docs/DHO_CONVENTION_NOTE_v0.1.md` — exact second-order known-truth frequency/damping convention.

### Executable scaffold

- `engine/` — pre-algorithm Structural Engine package.
  - mandatory provenance and result contracts;
  - BIDS hierarchy and metadata-only public-dataset auditing;
  - explicit run/session/subject separation;
  - scans-table session-completeness audit;
  - label-blind metadata-role firewall;
  - descriptive spectral interface that **cannot** license dynamical chi;
  - refusal codes;
  - mode-specific scalar lineage;
  - modal-estimator interface;
  - scalar-admission/refusal firewall;
  - exact second-order known-truth fixtures;
  - deterministic configuration/result serialization;
  - duplicate hierarchy and metadata-join audits;
  - subject-split leakage protection;
  - whole-system chi rejection;
  - regression tests;
  - GitHub Actions contract and public-metadata audit workflows.

The executable scaffold intentionally contains no clinical classifier and no unqualified dynamical estimator.

Public-data auditing is currently **metadata/hierarchy only**. A clean D2 audit does not mean the EEG payload has passed D4 readability/identity verification.

### Atlas, function, limits, and comparators

- `docs/NEUROSTABILITY_ATLAS_SPEC_v0.1.md` — independent healthy/reference Atlas specification.
- `docs/FUNCTION_LIMIT_MAP_v0.1.md` — coequal functioning and failure maps.
- `docs/NATIVE_COMPARATOR_PROGRAM_v0.1.md` — frozen native-baseline and incremental-value program.
- `docs/CROSS_DISORDER_COMORBIDITY_TEST_PLAN_v0.1.md` — shared-versus-specific architecture and comorbidity test design.

### Literature, attribution, and experiments

- `docs/LITERATURE_COLLISION_PASS_v0.1.md` — main prior-art collision pass.
- `docs/LITERATURE_COLLISION_ADDENDUM_v0.1.md` — dimensional psychiatry, normative modeling, and patient-heterogeneity collision.
- `docs/NOVELTY_ATTRIBUTION_AUDIT_v0.1.md` — separates established prior art from candidate residual contribution.
- `docs/NOVELTY_ATTRIBUTION_ADDENDUM_v0.1.md` — narrows residual novelty after peak-absence, identifiability, DMD, state-space, and modal prior-art review.
- `docs/CURRENT_REFERENCE_LEDGER_v0.1.md` — claim-level source ledger rebuilding citation support from scratch.
- `docs/EXPERIMENTAL_OPPORTUNITY_PLAN_v0.1.md` — experiment-first, literature-collision workflow.

### Reporting and release planning

- `docs/FIGURE_TABLE_PLAN_v0.1.md` — method/result figure and table gates, including historical-figure firewall.
- `docs/REPRODUCIBILITY_MATRIX_v0.1.md` — R1/R2/R3 closure plan.
- `docs/NONCOMPUTE_WORKSTREAMS_v0.1.md` — closure state of work that can advance before large computations.

## Historical correction now locked

The recovered 2025 manuscript is treated as a P0-D architecture/discovery artifact. Its figures showed a proposed Stability Architecture but the available package does not supply the empirical data/code lineage needed to treat its disorder coordinates, thresholds, trajectories, or cross-domain displays as validated results.

The forward workspace therefore preserves the architecture while rebuilding the evidence path from native data upward.

The permanent methodological lesson is:

> **Graphability is not measurement, and measurement is not validation.**

The forward evidence path is therefore:

`architecture -> native observable -> qualified estimator/model -> audited hierarchy -> uncertainty -> frozen comparator -> held-out/external evidence -> claim`.

## First real public-data gate results

The provenance layer has now been exercised against real OpenNeuro BIDS repositories rather than only fixtures.

- `ds003775`: **D2 hierarchy verified** — 111 subjects, 153 sessions, 42 repeat-session subjects, no participant/tree mismatch.
- `ds005385`: **D2 hierarchy verified** — 608 subjects, 816 sessions, 208 repeat participants, no session-table mismatch.
- `ds006780` / SFARI_EEG: **D2 blocked/quarantined** — README count 138, participants.tsv count 136, public tree count 139; three tree subjects lack participant-table rows; the README describes two physical resting-session days but the audited BIDS hierarchy does not currently expose a recoverable day/session mapping.

The clinically tempting dataset failing the gate is a useful result. The architecture is now refusing to convert provenance ambiguity into apparent certainty.

## Novelty correction now locked provisionally

NSD does not claim invention of:
- dimensional/transdiagnostic psychiatry;
- healthy-reference normative modeling;
- periodic/aperiodic EEG parameterization;
- psychiatric EEG heterogeneity;
- neural damped-oscillator/Q/pole modeling;
- peak-absence categories;
- spatiotemporal modal decomposition;
- dynamical-model identifiability analysis.

The central open question is whether a **stability-oriented integration and qualification architecture** adds reproducible scientific information beyond those established native methods while preserving disorder-specific structure and refusing unsupported scalar compression.

## Status rule

No draft prose may convert an old exploratory result, historical scalar, proxy, attractive visualization, classification result, individually legitimate method component, clean-looking public dataset, or unfinished computation into a current mechanistic or predictive claim. Pending results remain explicitly pending until their evidence path closes.