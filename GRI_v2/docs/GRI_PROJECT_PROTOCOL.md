# GRI Project Protocol

**Status:** Active project-local protocol index  
**Effective date:** 2026-09-14  
**Program authority:** SymC General Operations Manual v0.8.0

## Purpose

This file implements the v0.8.0 General Operations Manual transfer principle for the GRI program.

It is intentionally an authority map rather than a second copy of every rule. The GOM defines transferable program-wide safeguards. The files below remain the GRI-local source of record for project-specific scientific definitions, admission rules, atlas architecture, data conventions, comparator work, freezes, and candidate state.

If two active GRI-local documents appear to conflict, resolve the conflict through the explicit supersession/freeze record before changing science. Historical freeze/result artifacts are not rewritten merely because this index or the GOM is newer.

## Authority order

1. `CURRENT_PROTOCOL_AUTHORITY.md` — identifies the active GOM baseline, verified identities, and non-retroactivity rule.
2. `GRI_Project_Guardrails.md` — preserves GRI-specific claim ceilings intentionally removed from the program-wide manual during consolidation.
3. `EPISTEMIC_CONSTITUTION.md` — project-level scientific constitution and claim firewalls.
4. Frozen claim/config/state-definition artifacts — govern the exact scientific object for the run to which they apply.
5. Project-specific technical rules and schemas listed below.
6. Executable production code and tests implementing those frozen rules.
7. Result, audit, refusal, and dead-end artifacts recording what actually happened.

A later document cannot silently rescue or reinterpret an earlier frozen failure.

## Canonical GRI-local sources

### GRI consolidation guardrails

- `GRI_Project_Guardrails.md`

This file is the local source of record for the GRI-specific safeguards intentionally moved out of the program-wide GOM during consolidation. In particular it controls the claim ceiling for `chi_RNA = sigma/(2 mu) = CV/2`, native RNA-seq count-statistical challenges, cross-sectional-versus-temporal inference, and manuscript-language reconciliation for any stronger EP2/damping interpretation.

### Chi architecture and epistemic status

- `EPISTEMIC_CONSTITUTION.md`
- `CHI_SCALAR_MODAL_CONGLOMERATION_FIREWALL_20260830.md`
- `CHI_ADMISSION_RULES.md`

These files govern whether a biological coordinate may be called chi, which interpretation it earns, and how scalar, vector/modal, conglomerate/system, and open-channel evidence remain separated.

### Current Chi_bio admission lineage

The completed v0.1 admission lineage remains `NOT_ADMITTED`.

Current and historical candidate/freeze/refusal artifacts under `docs/chi_admission/` are the source of record for branch-specific states. A new candidate may proceed only as a new version/freeze. Existing failures and refusals remain preserved.

### Regulatory Substrate Atlas

- `GRI_REGULATORY_SUBSTRATE_ATLAS_V0_1_SCHEMA_20260910.md`
- subsequent Atlas extension, closure, and evidence-state records in `docs/`

These govern GRI-specific atlas modalities, schema, evidence state, and provenance. The Atlas remains independent of coordinate construction under the GOM.

### Native comparator and simple baselines

- `GRI_NATIVE_COMPARATOR_CANDIDATE_SURVEY_P0D_20260910.md`
- `GRI_COMPARATOR_PROVENANCE_RECOVERY_20260910.md`
- any later frozen comparator-selection record for the exact claim being tested

Comparator choice must answer the same frozen scientific question and may not be weakened after outcome inspection.

### Protocol integration and supersession records

- `GRI_V071_INTEGRATION_CONTROL_20260910.md`
- `GRI_V071A_PROTOCOL_AUDIT_20260910.md`
- `GRI_V074_DELTA_AUDIT_20260912.md`
- `GRI_V075_DELTA_AUDIT_20260913.md`
- `GRI_V080_DELTA_AUDIT_20260914.md`
- `GRI_CONTROL_DOCUMENT_SUPERSESSION_MAP_20260910.md`

Historical integration audits remain historical records. New prospective authority comes from the definitive current GOM plus this project protocol, `GRI_Project_Guardrails.md`, and the applicable frozen local artifacts.

## GRI-specific scientific rules delegated from the GOM

The following belong locally even when a generalized version also appears in the GOM:

- exact GRI proxy/coordinate definitions and their epistemic classes;
- assay-specific statistical models and mean-variance/normalization controls;
- TCGA and other cohort-specific limitations on temporal, causal, prognostic, or treatment interpretation;
- exact System Model and Engine implementation details;
- regulatory-state and B3 representation definitions;
- Regulatory Substrate Atlas modalities, schemas, and locked evidence identities;
- domain-specific simple baselines and strongest-native-comparator candidates;
- local dataset identities, joins, inclusion/exclusion rules, and preprocessing conventions;
- candidate-specific MFR-14 records, freezes, admission/refusal rules, and outcome records;
- project-specific experimental opportunities and literature-collision records.

## Current scientific boundary

At this protocol index version:

- `chi_RNA = sigma/(2 mu) = CV/2` is an operational proxy unless and until a validated mechanistic derivation earns a stronger classification;
- no numerical biological `Chi_bio` coordinate is admitted;
- no biological `Chi_bio = 1` boundary is licensed;
- algebraic resemblance to a damping-ratio form does not license EP2, critical-damping, or exceptional-point interpretation;
- native count-statistical structure and relevant RNA-seq nuisance structure remain mandatory challenges for any use of the proxy;
- cross-sectional TCGA ordering cannot by itself support temporal progression, warning lead time, recovery, irreversibility, treatment response, or causal direction;
- the short-term G2 lane remains closed at its earned prospective refusal;
- the chronic SCC25 G2 lane and bounded feature-gate robustness audit remain completed evidence;
- the B3 lane has progressed to a prospective state-definition/representation choice that changes the scientific object and therefore requires an explicit science decision/freeze before outcome-bearing execution;
- normalized empirical G1 remains separately blocked until its restoration problem is independently resolved.

The active PR and its current frozen artifacts, not this summary paragraph, control the exact detailed state if later work advances the project.

## Work allowed autonomously

Without changing frozen science, routine work may continue on:

- provenance verification;
- documentation synchronization;
- schema and authority routing;
- code/test mechanics;
- run preflight and checkpointing;
- monitoring and recovery of real active dependencies;
- reproducibility checks;
- result landing-zone preparation;
- audit of stale active references;
- preservation and indexing of failures, refusals, and open-channel evidence.

## Work requiring a science decision or new freeze

Do not autonomously choose or alter:

- a new B3 state coordinate definition;
- the exact outcome-bearing dimensionality/reduction rule when not already frozen;
- a threshold, endpoint, comparator, or inclusion rule that changes a frozen claim;
- a new biological unity interpretation;
- a new system-level scalar;
- a mechanistic or predictive claim unsupported by the existing evidence class.

## v0.8.0 migration rule

The definitive GOM v0.8.0 changes where project-specific rules live; it does not by itself change the scientific result of an existing GRI calculation.

No already-running calculation is restarted, retuned, or reinterpreted solely because of this governance promotion. New prospective decisions use the definitive GOM v0.8.0, this project-local authority stack, and the applicable frozen scientific artifacts.
